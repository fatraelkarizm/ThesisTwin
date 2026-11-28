"use client";

import { Eye, FileText, RefreshCw } from "lucide-react";
import { useCallback, useEffect, useState } from "react";
import { BriefDocument } from "@/components/domain/BriefDocument";
import { Button } from "@/components/ui/Button";
import { Section } from "@/components/ui/Section";
import {
  api,
  ApiError,
  toFinding,
  type BriefOut,
  type CommentStatusOut,
  type ElementOut,
  type ElementType,
  type GraphOut,
  type StressQuestionOut,
} from "@/lib/api";
import { copy } from "@/lib/copy";
import type { Finding } from "@/types/domain";
import { AddElementForm, ElementList } from "./ElementsPanel";
import { FindingGroup, groupFindings, isOpen } from "./FindingGroup";
import { GraphView } from "./GraphView";
import { ProjectPage, type ProjectContext } from "./ProjectPage";
import { CommentsPanel, SharePanel } from "./SidePanels";
import { StressPanel } from "./StressPanel";

const message = (e: unknown) => (e instanceof ApiError ? e.message : String(e));

function ErrorNote({ error }: { error: string | null }) {
  return error ? (
    <p role="alert" className="rounded-lg bg-tone-danger-bg p-3 text-sm text-tone-danger-fg">
      {error}
    </p>
  ) : null;
}

/** Muat data untuk versi terpilih; dimuat ulang saat versi berganti. */
function useVersionData<T>(versionId: string, load: (id: string) => Promise<T>) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<string | null>(null);
  const refresh = useCallback(() => {
    load(versionId).then(setData, (e: unknown) => setError(message(e)));
  }, [versionId, load]);
  useEffect(refresh, [refresh]);
  return { data, setData, error, setError, refresh };
}

// ---- 1. Isi proposal ----------------------------------------------------------------------

const loadProposal = (id: string) => Promise.all([api.elements(id), api.graph(id)]);

export function ProposalView({ version, unit }: ProjectContext) {
  const w = copy.workspace;
  const [tab, setTab] = useState<"elements" | "graph">("elements");
  const { data, setData, error, setError } = useVersionData(version.id, loadProposal);
  const elements: ElementOut[] = data?.[0] ?? [];
  const graph: GraphOut | null = data?.[1] ?? null;

  async function add(body: { type: ElementType; content: string; quote: string; page: number }) {
    try {
      const el = await api.addElement(version.id, body);
      setData([[...elements, el], await api.graph(version.id)]);
      setError(null);
    } catch (e) {
      setError(message(e));
    }
  }

  return (
    <>
      <p className="flex items-center gap-2 text-sm">
        <FileText aria-hidden="true" className="size-4 text-brand-strong" />
        {w.summaryDetected(elements.length, elements.filter((e) => e.verified).length)}
      </p>
      <div role="tablist" aria-label={w.tabElements} className="flex gap-1 border-b border-line">
        {(["elements", "graph"] as const).map((t) => (
          <button
            key={t}
            role="tab"
            type="button"
            aria-selected={tab === t}
            onClick={() => setTab(t)}
            className={`-mb-px min-h-11 border-b-2 px-4 text-sm ${
              tab === t ? "border-brand font-semibold text-brand-strong" : "border-transparent text-muted"
            }`}
          >
            {t === "elements" ? `${w.tabElements} (${elements.length})` : w.tabGraph}
          </button>
        ))}
      </div>
      <ErrorNote error={error} />
      {tab === "elements" ? (
        <div className="space-y-6">
          <ElementList elements={elements} unit={unit} />
          <AddElementForm unit={unit} onAdd={add} />
        </div>
      ) : graph ? (
        <GraphView graph={graph} unit={unit} />
      ) : null}
    </>
  );
}

// ---- 2. Cek konsistensi -------------------------------------------------------------------

type Filter = "open" | "high" | "reviewed" | "all";

export function FindingsView({ version, unit }: ProjectContext) {
  const w = copy.workspace;
  const { data, setData, error, setError } = useVersionData(version.id, api.findings);
  const [checking, setChecking] = useState(false);
  const [filter, setFilter] = useState<Filter>("open");
  const findings = (data ?? []).map((f) => toFinding(f, unit));
  const subsets: Record<Filter, Finding[]> = {
    open: findings.filter(isOpen),
    high: findings.filter((f) => isOpen(f) && f.priority === "high"),
    reviewed: findings.filter((f) => !isOpen(f)),
    all: findings,
  };
  const groups = groupFindings(subsets[filter]);

  async function runCheck() {
    setChecking(true);
    try {
      setData(await api.check(version.id));
    } catch (e) {
      setError(message(e));
    } finally {
      setChecking(false);
    }
  }

  async function decide(id: string, target: "student_confirmed" | "rejected") {
    try {
      const updated = await api.setStatus(id, target);
      setData((data ?? []).map((f) => (f.id === id ? updated : f)));
    } catch (e) {
      setError(message(e));
    }
  }

  return (
    <>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div role="group" aria-label={w.filterLabel} className="flex flex-wrap gap-1.5">
          {(Object.keys(w.filters) as Filter[]).map((k) => (
            <button
              key={k}
              type="button"
              aria-pressed={filter === k}
              onClick={() => setFilter(k)}
              className={`inline-flex min-h-11 items-center gap-1.5 rounded-full border px-3.5 text-sm ${
                filter === k ? "border-brand bg-brand-soft font-medium text-brand-strong" : "border-line hover:bg-surface-muted"
              }`}
            >
              {w.filters[k]}
              <span className="tabular-nums text-muted">{subsets[k].length}</span>
            </button>
          ))}
        </div>
        <Button variant="secondary" onClick={runCheck} disabled={checking}>
          <RefreshCw aria-hidden="true" className="size-4" />
          {checking ? w.running : w.runCheck}
        </Button>
      </div>
      <ErrorNote error={error} />
      {groups.length === 0 ? (
        <p className="rounded-card border border-dashed border-line p-6 text-center text-sm text-muted">
          {filter === "open" ? w.noneToReview : w.noneInFilter}
        </p>
      ) : (
        <ul className="space-y-3">
          {groups.map((g) => (
            <li key={g.ruleId}>
              <FindingGroup
                group={g}
                onConfirm={(id) => decide(id, "student_confirmed")}
                onReject={(id) => decide(id, "rejected")}
              />
            </li>
          ))}
        </ul>
      )}
    </>
  );
}

// ---- 3. Defense Stress-Test ---------------------------------------------------------------

export function StressView({ version }: ProjectContext) {
  const { data, setData, error, setError } = useVersionData(version.id, api.getStressTest);
  const questions: StressQuestionOut[] = data ?? [];
  return (
    <>
      <ErrorNote error={error} />
      <StressPanel
        questions={questions}
        onGenerate={async (regenerate) => {
          try {
            setData(await api.stressTest(version.id, regenerate));
          } catch (e) {
            setError(message(e));
          }
        }}
        onAnswer={async (id, text) => {
          try {
            const updated = await api.answer(id, text);
            setData(questions.map((q) => (q.id === id ? updated : q)));
          } catch (e) {
            setError(message(e));
          }
        }}
      />
    </>
  );
}

// ---- 4. Riwayat versi ---------------------------------------------------------------------

export function VersionsView({ project, versions }: ProjectContext) {
  const w = copy.workspace;
  const [brief, setBrief] = useState<BriefOut | null>(null);
  const [comments, setComments] = useState<CommentStatusOut[]>([]);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(() => {
    Promise.all([api.brief(project.id), api.comments(project.id)]).then(
      ([b, c]) => {
        setBrief(b);
        setComments(c);
      },
      (e: unknown) => setError(message(e)),
    );
  }, [project.id]);
  useEffect(load, [load]);

  async function review(commentId: string, addressed: boolean) {
    const previous = versions.at(-2);
    if (!previous) return;
    try {
      await api.reviewComment(previous.id, commentId, addressed);
      load();
    } catch (e) {
      setError(message(e));
    }
  }

  return (
    <>
      <ErrorNote error={error} />
      <Section title={w.versionsListTitle}>
        <ol className="divide-y divide-line rounded-card border border-line">
          {[...versions].reverse().map((v) => (
            <li key={v.id} className="flex flex-wrap items-center gap-3 px-4 py-3 text-sm">
              <span className="rounded-md bg-brand-soft px-2 py-0.5 text-xs font-semibold text-brand-strong">
                v{v.version_no}
              </span>
              <span className="min-w-0 flex-1 truncate">{v.filename}</span>
              <span className="text-xs text-muted">
                {new Date(v.uploaded_at).toLocaleString("id-ID", { dateStyle: "medium", timeStyle: "short" })}
              </span>
            </li>
          ))}
        </ol>
      </Section>
      {versions.length < 2 ? (
        <p className="rounded-card border border-dashed border-line p-4 text-sm text-muted">{w.singleVersion}</p>
      ) : (
        <div className="grid gap-6 lg:grid-cols-2">
          <Section title={w.changesTitle} description={w.changesDescription}>
            {brief?.changes.length ? (
              <ul className="space-y-1.5 text-sm">
                {brief.changes.map((c) => (
                  <li key={c} className="rounded-lg border border-line px-3 py-2">
                    {c}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-muted">{copy.supervisor.noChanges}</p>
            )}
          </Section>
          <Section title={w.impactsTitle} description={w.impactsDescription}>
            {brief?.impacts.length ? (
              <ul className="space-y-1.5 text-sm">
                {brief.impacts.map((c) => (
                  <li key={c} className="rounded-lg border border-tone-warning-bg bg-surface px-3 py-2">
                    {c}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-muted">{w.noImpacts}</p>
            )}
          </Section>
        </div>
      )}
      <CommentsPanel comments={comments} onReview={review} />
    </>
  );
}

// ---- 5. Supervision Brief -----------------------------------------------------------------

export function BriefView({ project, versions }: ProjectContext) {
  const w = copy.workspace;
  const latest = versions.at(-1)!;
  const [data, setData] = useState<{ brief: BriefOut; stress: StressQuestionOut[]; text: string; links: number } | null>(
    null,
  );
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    Promise.all([
      api.brief(project.id),
      api.getStressTest(latest.id),
      api.briefText(project.id),
      api.shareLinks(project.id),
    ]).then(
      ([brief, stress, text, links]) => setData({ brief, stress, text, links: links.length }),
      (e: unknown) => setError(message(e)),
    );
  }, [project.id, latest.id]);

  return (
    <>
      <ErrorNote error={error} />
      {data ? (
        <div className="grid items-start gap-6 lg:grid-cols-[minmax(0,1fr)_300px]">
          <section aria-label={w.previewLabel} className="rounded-card border border-line bg-background p-2">
            <p className="flex items-center gap-2 px-3 py-2 text-xs font-medium text-muted">
              <Eye aria-hidden="true" className="size-4" />
              {w.previewLabel}
            </p>
            <div className="rounded-lg border border-line bg-surface p-4 md:p-6">
              <BriefDocument brief={data.brief} stress={data.stress} />
            </div>
          </section>
          <div className="lg:sticky lg:top-20">
            <SharePanel
              text={data.text}
              links={data.links}
              onShare={async () => {
                const path = (await api.share(project.id)).path;
                setData((d) => (d ? { ...d, links: d.links + 1 } : d));
                return `${window.location.origin}${path}`;
              }}
            />
          </div>
        </div>
      ) : null}
    </>
  );
}

// ---- Halaman (client) ---------------------------------------------------------------------
// Server Component tidak bisa mengoper fungsi ke Client Component, jadi tiap halaman dibungkus di sini.

export const ProposalPage = () => <ProjectPage step={1}>{(ctx) => <ProposalView {...ctx} />}</ProjectPage>;
export const FindingsPage = () => <ProjectPage step={2}>{(ctx) => <FindingsView {...ctx} />}</ProjectPage>;
export const StressPage = () => <ProjectPage step={3}>{(ctx) => <StressView {...ctx} />}</ProjectPage>;
// Riwayat & brief berlaku untuk seluruh proyek (versi terbaru vs sebelumnya), tanpa pilihan versi.
export const VersionsPage = () => (
  <ProjectPage step={4} versionPicker={false}>
    {(ctx) => <VersionsView {...ctx} />}
  </ProjectPage>
);
export const BriefPage = () => (
  <ProjectPage step={5} versionPicker={false}>
    {(ctx) => <BriefView {...ctx} />}
  </ProjectPage>
);
