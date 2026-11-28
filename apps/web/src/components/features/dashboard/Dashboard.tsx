"use client";

import { ArrowRight, Check, Circle, CircleDot, Clock3, type LucideIcon } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";
import { EvidenceChip } from "@/components/domain/EvidenceChip";
import { PriorityTag } from "@/components/domain/PriorityTag";
import { StatusBadge } from "@/components/domain/StatusBadge";
import { buttonClass } from "@/components/ui/Button";
import { Section } from "@/components/ui/Section";
import { SegmentedBar } from "@/components/ui/SegmentedBar";
import { api, ApiError, toFinding, type ProjectOut, type VersionOut } from "@/lib/api";
import { copy } from "@/lib/copy";
import { savedProjectId } from "@/lib/project";
import type { Finding, Priority } from "@/types/domain";
import { journey, type Journey, type StepState } from "./journey";

const OPEN = new Set(["ai_suggested", "needs_user_confirmation"]);
const RANK: Record<Priority, number> = { high: 0, medium: 1, low: 2 };

export interface Live {
  project: ProjectOut;
  latest: VersionOut;
  journey: Journey;
  open: Finding[];
}

async function loadLive(projectId: string): Promise<Live | null> {
  const [project, versions] = await Promise.all([api.project(projectId), api.versions(projectId)]);
  const latest = versions.at(-1);
  if (!latest) return null;
  const [elements, findings, questions, comments, links] = await Promise.all([
    api.elements(latest.id),
    api.findings(latest.id),
    api.getStressTest(latest.id),
    api.comments(projectId),
    api.shareLinks(projectId),
  ]);
  const unit = latest.media_type === "application/pdf" ? "page" : "section";
  const open = findings.filter((f) => OPEN.has(f.status));
  return {
    project,
    latest,
    open: open.map((f) => toFinding(f, unit)).sort((a, b) => RANK[a.priority] - RANK[b.priority]),
    journey: journey({
      elements: elements.length,
      verified: elements.filter((e) => e.verified).length,
      findingsTotal: findings.length,
      findingsOpen: open.length,
      questions: questions.length,
      answered: questions.filter((q) => q.answer?.trim()).length,
      versions: versions.length,
      commentsPending: comments.filter((c) => c.confirmed === null).length,
      linksCreated: links.length,
    }),
  };
}

type State =
  | { kind: "loading" }
  | { kind: "none" }
  | { kind: "error"; message: string }
  | { kind: "ready"; live: Live };

export function Dashboard() {
  const [state, setState] = useState<State>({ kind: "loading" });

  useEffect(() => {
    const pid = savedProjectId();
    (pid ? loadLive(pid) : Promise.resolve(null)).then(
      (live) => setState(live ? { kind: "ready", live } : { kind: "none" }),
      (e: unknown) =>
        setState(
          e instanceof ApiError && e.status === 404
            ? { kind: "none" }
            : { kind: "error", message: e instanceof ApiError ? e.message : copy.home.loadError },
        ),
    );
  }, []);

  if (state.kind === "loading") return <p className="p-6 text-sm text-muted">{copy.workspace.loading}</p>;
  if (state.kind === "none") return <Onboarding />;
  if (state.kind === "error")
    return (
      <p role="alert" className="m-6 rounded-lg bg-tone-danger-bg p-3 text-sm text-tone-danger-fg">
        {state.message}
      </p>
    );
  return <Home live={state.live} />;
}

const stateIcon: Record<StepState, LucideIcon> = { done: Check, next: CircleDot, todo: Circle, later: Clock3 };
const stateClass: Record<StepState, string> = {
  done: "bg-brand text-brand-fg",
  next: "bg-brand-soft text-brand-strong",
  todo: "bg-surface-muted text-muted",
  later: "bg-surface-muted text-muted",
};

export function Home({ live }: { live: Live }) {
  const h = copy.home;
  const { project, latest, journey: jr, open } = live;
  const when = new Date(latest.uploaded_at).toLocaleDateString("id-ID", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
  const progress = h.progress(jr.done, jr.steps.length);

  return (
    <main className="flex-1 bg-surface px-4 py-6 md:px-8">
      <div className="mx-auto max-w-5xl space-y-8">
        <header className="flex flex-wrap items-end justify-between gap-4">
          <div className="min-w-0">
            <h1 className="text-2xl font-semibold tracking-tight">{project.title}</h1>
            <p className="mt-1 text-sm text-muted">{h.latest(latest.version_no, when)}</p>
          </div>
          <div className="w-full sm:w-56">
            <p className="mb-1.5 text-xs font-medium text-muted sm:text-right">{progress}</p>
            <SegmentedBar value={jr.done} total={jr.steps.length} label={progress} />
          </div>
        </header>

        <section
          aria-labelledby="next-title"
          className="flex flex-col gap-4 rounded-card border border-brand/30 bg-brand-soft/60 p-5 sm:flex-row sm:items-center"
        >
          <div className="min-w-0 flex-1">
            <p className="text-xs font-semibold uppercase tracking-wide text-brand-strong">{h.nextLabel}</p>
            <h2 id="next-title" className="mt-1 text-lg font-semibold">
              {jr.next.title}
            </h2>
            <p className="mt-1 max-w-2xl text-sm text-muted">{jr.next.body}</p>
          </div>
          <Link href={jr.next.href} className={buttonClass("primary", "shrink-0")}>
            {jr.next.cta}
            <ArrowRight aria-hidden="true" className="size-4" />
          </Link>
        </section>

        <div className="grid gap-8 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.3fr)]">
          <Section title={h.journeyTitle} description={h.journeyDescription}>
            <ol className="space-y-1">
              {jr.steps.map((s, i) => {
                const Icon = stateIcon[s.state];
                return (
                  <li key={s.href}>
                    <Link
                      href={s.href}
                      className={`flex min-h-14 items-center gap-3 rounded-lg border px-3 py-2 hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-brand ${
                        s.state === "next" ? "border-brand/40" : "border-transparent"
                      }`}
                    >
                      <span
                        aria-hidden="true"
                        className={`flex size-7 shrink-0 items-center justify-center rounded-full ${stateClass[s.state]}`}
                      >
                        <Icon className="size-4" />
                      </span>
                      <span className="min-w-0 flex-1">
                        <span className="block text-sm font-medium">
                          {i + 1}. {s.title}
                        </span>
                        <span className="block text-xs text-muted">{s.detail}</span>
                      </span>
                      <span className="shrink-0 text-xs text-muted">{h.state[s.state]}</span>
                    </Link>
                  </li>
                );
              })}
            </ol>
          </Section>

          <Section
            title={h.topTitle}
            description={h.topDescription}
            action={
              open.length > 0 ? (
                <Link
                  href="/temuan"
                  className="flex min-h-11 shrink-0 items-center text-sm font-medium text-brand-strong underline-offset-2 hover:underline"
                >
                  {h.seeAll(open.length)}
                </Link>
              ) : undefined
            }
          >
            {open.length === 0 ? (
              <p className="rounded-card border border-dashed border-line p-4 text-sm text-muted">{h.topEmpty}</p>
            ) : (
              <ul className="space-y-2.5">
                {open.slice(0, 3).map((f) => (
                  <li key={f.id} className="space-y-2 rounded-card border border-line bg-surface p-4 shadow-card">
                    <div className="flex flex-wrap items-center gap-1.5">
                      <PriorityTag priority={f.priority} />
                      <StatusBadge status={f.evidence.length ? f.status : "needs_user_confirmation"} />
                    </div>
                    <p className="text-sm font-semibold">{f.title}</p>
                    <div className="flex flex-wrap gap-1.5">
                      {f.evidence.length ? (
                        f.evidence.map((e, k) => <EvidenceChip key={`${e.element}-${e.page}-${k}`} evidence={e} />)
                      ) : (
                        <span className="text-xs text-muted">{copy.noEvidence}</span>
                      )}
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </Section>
        </div>
      </div>
    </main>
  );
}

function Onboarding() {
  const o = copy.home.onboarding;
  return (
    <main className="flex-1 bg-surface px-4 py-10 md:px-8 md:py-16">
      <div className="mx-auto max-w-3xl">
        <h1 className="text-3xl font-semibold tracking-tight">{o.title}</h1>
        <p className="mt-3 max-w-2xl text-base text-muted">{o.body}</p>
        <div className="mt-6 flex flex-wrap items-center gap-3">
          <Link href="/upload" className={buttonClass("primary")}>
            {o.cta}
            <ArrowRight aria-hidden="true" className="size-4" />
          </Link>
          <span className="text-sm text-muted">{o.formats}</span>
        </div>
        <h2 className="mt-12 text-sm font-semibold uppercase tracking-wide text-muted">{o.stepsTitle}</h2>
        <ol className="mt-3 grid gap-3 sm:grid-cols-2">
          {copy.steps.map((s, i) => (
            <li key={s.href} className="rounded-card border border-line bg-background p-4">
              <p className="flex items-center gap-2 text-sm font-semibold">
                <span className="flex size-6 items-center justify-center rounded-full bg-brand-soft text-xs text-brand-strong tabular-nums">
                  {i + 1}
                </span>
                {s.short}
              </p>
              <p className="mt-1.5 text-sm text-muted">{s.description}</p>
            </li>
          ))}
        </ol>
      </div>
    </main>
  );
}
