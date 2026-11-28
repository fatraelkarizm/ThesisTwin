"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { SimulatedBadge } from "@/components/domain/SimulatedBadge";
import { Badge } from "@/components/ui/Badge";
import { buttonClass } from "@/components/ui/Button";
import { api, toFinding, type ElementType } from "@/lib/api";
import { copy } from "@/lib/copy";
import { savedProjectId } from "@/lib/project";
import type { Finding } from "@/types/domain";
import { FindingQueue } from "./FindingQueue";
import { StatTiles } from "./StatTiles";
import { ToolsPanel } from "./ToolsPanel";
import { VersionCards } from "./VersionCards";
import { VersionHistory } from "./VersionHistory";
import * as sample from "./sample";
import type { VersionSummary } from "./sample";

// Elemen inti proposal Bab 1–3; dipakai untuk bar "elemen inti tercatat" per versi.
const CORE: ElementType[] = ["research_question", "objective", "variable", "method", "instrument", "analysis"];
const OPEN = new Set(["ai_suggested", "needs_user_confirmation"]);

interface Live {
  title: string;
  program: string;
  versions: VersionSummary[];
  findings: Finding[];
  stats: typeof sample.stats;
  unit: "page" | "section";
}

const fmt = (iso: string) =>
  new Date(iso).toLocaleString("id-ID", { day: "numeric", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" });

async function loadLive(projectId: string): Promise<Live | null> {
  const versions = await api.versions(projectId);
  if (versions.length === 0) return null;
  const perVersion = await Promise.all(
    versions.map(async (v) => {
      const [elements, findings] = await Promise.all([api.elements(v.id), api.findings(v.id)]);
      return { v, elements, findings };
    }),
  );
  const [brief, comments] = await Promise.all([api.brief(projectId), api.comments(projectId)]);
  const latest = perVersion.at(-1)!;
  const unit = latest.v.media_type === "application/pdf" ? "page" : "section";
  const days = Math.floor((Date.now() - new Date(latest.v.uploaded_at).getTime()) / 86_400_000);
  return {
    unit,
    title: brief.project_title,
    program: brief.program,
    versions: perVersion
      .map(({ v, elements, findings }) => ({
        version: v.version_no,
        openFindings: findings.filter((f) => OPEN.has(f.status)).length,
        summary: copy.dashboard.summary(elements.length, elements.filter((e) => e.verified).length),
        uploadedAt: fmt(v.uploaded_at),
        sectionsChecked: CORE.filter((t) => elements.some((e) => e.type === t)).length,
        sectionsTotal: CORE.length,
        latest: v.id === latest.v.id,
      }))
      .reverse(),
    findings: latest.findings.filter((f) => OPEN.has(f.status)).map((f) => toFinding(f, unit)),
    stats: {
      verified: latest.elements.filter((e) => e.verified).length,
      extracted: latest.elements.length,
      commentsDone: comments.filter((c) => c.confirmed === true).length,
      commentsTotal: comments.length,
      waitingDays: Math.max(0, days),
    },
  };
}

export function Dashboard() {
  const d = copy.dashboard;
  const [live, setLive] = useState<Live | null>(null);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    const pid = savedProjectId();
    (pid ? loadLive(pid) : Promise.resolve(null))
      .then(setLive, () => setLive(null)) // API mati / proyek hilang: tampilkan contoh berlabel
      .finally(() => setLoaded(true));
  }, []);

  if (!loaded) return <p className="p-6 text-sm text-muted">{copy.workspace.loading}</p>;

  const data = live ?? {
    title: d.title,
    program: d.subtitle,
    versions: sample.versions,
    findings: sample.findings,
    stats: sample.stats,
    unit: "page" as const,
  };

  async function decide(id: string, target: "student_confirmed" | "rejected") {
    const updated = toFinding(await api.setStatus(id, target), data.unit);
    const pid = savedProjectId();
    if (pid) loadLive(pid).then(setLive, () => undefined); // perbarui angka kartu & statistik
    return updated;
  }

  return (
    <main className="grid flex-1 lg:grid-cols-[minmax(0,1fr)_360px]">
      <div className="space-y-8 bg-surface p-4 md:p-6">
        <header className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <h1 className="text-2xl font-semibold tracking-tight">{data.title}</h1>
            <p className="text-sm text-muted">{data.program}</p>
          </div>
          {live ? (
            <Badge tone="success">{d.liveNote}</Badge>
          ) : (
            <div className="flex max-w-md flex-wrap items-start gap-2">
              <SimulatedBadge />
              <p className="text-xs text-muted">{d.demoCta}</p>
              <Link href="/upload" className={buttonClass("primary")}>
                {copy.workspace.goUpload}
              </Link>
            </div>
          )}
        </header>
        <VersionCards versions={data.versions} />
        <FindingQueue
          initial={data.findings}
          onDecide={live ? decide : undefined}
        />
        <VersionHistory versions={data.versions} unitLabel={live ? d.coreElements : undefined} />
      </div>
      <div className="space-y-8 border-t border-line bg-background p-4 md:p-6 lg:border-l lg:border-t-0">
        <ToolsPanel live={Boolean(live)} />
        <StatTiles stats={data.stats} />
      </div>
    </main>
  );
}
