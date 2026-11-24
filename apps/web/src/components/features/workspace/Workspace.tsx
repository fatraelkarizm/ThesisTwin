"use client";

import { CircleAlert, Play } from "lucide-react";
import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { FindingCard } from "@/components/domain/FindingCard";
import { Button, buttonClass } from "@/components/ui/Button";
import { Section } from "@/components/ui/Section";
import {
  api,
  ApiError,
  toFinding,
  type CommentStatusOut,
  type ElementOut,
  type ElementType,
  type FindingApi,
  type GraphOut,
  type VersionOut,
} from "@/lib/api";
import { copy } from "@/lib/copy";
import { savedProjectId } from "@/lib/project";
import { ElementsPanel } from "./ElementsPanel";
import { GraphView } from "./GraphView";
import { BriefPanel, CommentsPanel } from "./SidePanels";

const OPEN = new Set(["ai_suggested", "needs_user_confirmation"]);

export function Workspace() {
  const w = copy.workspace;
  const [projectId, setProjectId] = useState<string | null>(null);
  const [loaded, setLoaded] = useState(false);
  const [versions, setVersions] = useState<VersionOut[]>([]);
  const [versionId, setVersionId] = useState<string | null>(null);
  const [elements, setElements] = useState<ElementOut[]>([]);
  const [findings, setFindings] = useState<FindingApi[]>([]);
  const [graph, setGraph] = useState<GraphOut | null>(null);
  const [comments, setComments] = useState<CommentStatusOut[]>([]);
  const [brief, setBrief] = useState("");
  const [checking, setChecking] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fail = (e: unknown) => setError(e instanceof ApiError ? e.message : String(e));

  const refreshProject = useCallback((pid: string) => {
    Promise.all([api.comments(pid), api.briefText(pid)])
      .then(([c, b]) => {
        setComments(c);
        setBrief(b);
      })
      .catch(fail);
  }, []);

  useEffect(() => {
    const pid = savedProjectId();
    if (!pid) {
      Promise.resolve().then(() => setLoaded(true));
      return;
    }
    api
      .versions(pid)
      .then((list) => {
        setProjectId(pid);
        setVersions(list);
        setVersionId(list.at(-1)?.id ?? null);
        refreshProject(pid);
      })
      .catch(fail)
      .finally(() => setLoaded(true));
  }, [refreshProject]);

  useEffect(() => {
    if (!versionId) return;
    Promise.all([api.elements(versionId), api.findings(versionId), api.graph(versionId)])
      .then(([e, f, g]) => {
        setElements(e);
        setFindings(f);
        setGraph(g);
      })
      .catch(fail);
  }, [versionId]);

  const version = versions.find((v) => v.id === versionId);
  const unit = version?.media_type === "application/pdf" ? "page" : "section";

  if (!loaded) return <p className="p-6 text-sm text-muted">{w.loading}</p>;
  if (!projectId || !version) {
    return (
      <div className="rounded-card border border-dashed border-line bg-surface p-8 text-center">
        <p className="text-sm text-muted">{w.empty}</p>
        <Link href="/upload" className={buttonClass("primary", "mt-4")}>
          {w.goUpload}
        </Link>
      </div>
    );
  }

  async function addElement(body: { type: ElementType; content: string; quote: string; page: number }) {
    try {
      const el = await api.addElement(version!.id, body);
      setElements((prev) => [...prev, el]);
      setGraph(await api.graph(version!.id));
      setError(null);
    } catch (e) {
      fail(e);
    }
  }

  async function runCheck() {
    setChecking(true);
    try {
      setFindings(await api.check(version!.id));
      refreshProject(projectId!);
    } catch (e) {
      fail(e);
    } finally {
      setChecking(false);
    }
  }

  async function decide(id: string, target: "student_confirmed" | "rejected") {
    try {
      const updated = await api.setStatus(id, target);
      setFindings((prev) => prev.map((f) => (f.id === id ? updated : f)));
      refreshProject(projectId!);
    } catch (e) {
      fail(e);
    }
  }

  async function reviewComment(commentId: string, addressed: boolean) {
    const previous = versions.at(-2);
    if (!previous) return;
    try {
      await api.reviewComment(previous.id, commentId, addressed);
      refreshProject(projectId!);
    } catch (e) {
      fail(e);
    }
  }

  async function share() {
    const s = await api.share(projectId!);
    return `${window.location.origin}${s.path}`;
  }

  return (
    <div className="grid flex-1 lg:grid-cols-[minmax(0,1fr)_380px]">
      <div className="space-y-8 bg-surface p-4 md:p-6">
        <div className="flex flex-wrap items-center gap-2" role="group" aria-label={w.version}>
          {versions.map((v) => (
            <button
              key={v.id}
              type="button"
              aria-pressed={v.id === versionId}
              onClick={() => setVersionId(v.id)}
              className={`min-h-9 rounded-full border px-3 text-sm ${
                v.id === versionId ? "border-brand bg-brand-soft font-medium text-brand-strong" : "border-line"
              }`}
            >
              v{v.version_no} · {v.filename}
            </button>
          ))}
        </div>

        {error ? (
          <p role="alert" className="flex items-start gap-2 rounded-lg bg-tone-danger-bg p-3 text-sm text-tone-danger-fg">
            <CircleAlert aria-hidden="true" className="mt-0.5 size-4 shrink-0" />
            {error}
          </p>
        ) : null}

        <ElementsPanel elements={elements} unit={unit} onAdd={addElement} />

        {graph ? <GraphView graph={graph} unit={unit} /> : null}

        <Section
          id="temuan"
          title={w.findingsTitle}
          description={w.findingsDescription}
          action={
            <Button onClick={runCheck} disabled={checking || elements.length === 0}>
              <Play aria-hidden="true" className="size-4" />
              {checking ? w.running : w.runCheck}
            </Button>
          }
        >
          {findings.length === 0 ? (
            <p className="text-sm text-muted">{w.noFindings}</p>
          ) : (
            <ul className="space-y-3">
              {findings.map((f) => (
                <li key={f.id}>
                  <FindingCard
                    finding={toFinding(f, unit)}
                    onConfirm={OPEN.has(f.status) ? (id) => decide(id, "student_confirmed") : undefined}
                    onReject={OPEN.has(f.status) ? (id) => decide(id, "rejected") : undefined}
                  />
                </li>
              ))}
            </ul>
          )}
        </Section>
      </div>

      <div className="space-y-8 border-t border-line bg-background p-4 md:p-6 lg:border-l lg:border-t-0">
        <CommentsPanel comments={comments} onReview={reviewComment} />
        <BriefPanel text={brief} onShare={share} />
      </div>
    </div>
  );
}
