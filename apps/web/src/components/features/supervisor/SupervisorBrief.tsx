"use client";

import { BookOpenCheck, Check, CircleAlert, X } from "lucide-react";
import { useEffect, useState } from "react";
import { PriorityTag } from "@/components/domain/PriorityTag";
import { StatusBadge } from "@/components/domain/StatusBadge";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Section } from "@/components/ui/Section";
import { api, ApiError, type BriefFindingOut, type BriefOut, type StressQuestionOut } from "@/lib/api";
import { copy } from "@/lib/copy";

export function SupervisorBrief({ token }: { token: string }) {
  const s = copy.supervisor;
  const [brief, setBrief] = useState<BriefOut | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [decided, setDecided] = useState<Record<string, string>>({});
  const [stress, setStress] = useState<StressQuestionOut[]>([]);

  useEffect(() => {
    Promise.all([api.sharedBrief(token), api.sharedStress(token)]).then(
      ([b, q]) => {
        setBrief(b);
        setStress(q);
      },
      (e: unknown) => setError(e instanceof ApiError && e.status === 404 ? s.invalid : String(e)),
    );
  }, [token, s.invalid]);

  async function rate(questionId: string, score: number) {
    try {
      const updated = await api.rate(token, questionId, score);
      setStress((prev) => prev.map((q) => (q.id === questionId ? updated : q)));
    } catch (e) {
      setError(e instanceof ApiError ? e.message : String(e));
    }
  }

  async function decide(f: BriefFindingOut, confirm: boolean) {
    try {
      const updated = await api.decide(token, f.id, confirm);
      setDecided((prev) => ({ ...prev, [f.id]: updated.status }));
    } catch (e) {
      setError(e instanceof ApiError ? e.message : String(e));
    }
  }

  return (
    <main className="mx-auto w-full max-w-3xl space-y-8 p-4 md:p-8">
      <header className="flex items-center gap-3">
        <span className="flex size-9 items-center justify-center rounded-lg bg-brand text-brand-fg">
          <BookOpenCheck aria-hidden="true" className="size-5" />
        </span>
        <div>
          <h1 className="text-xl font-semibold tracking-tight">{s.title}</h1>
          {brief ? (
            <p className="text-sm text-muted">
              {brief.project_title} · {brief.program} · {s.versions}{" "}
              {brief.from_version ? `v${brief.from_version} → v${brief.to_version}` : `v${brief.to_version}`}
            </p>
          ) : null}
        </div>
      </header>

      {error ? (
        <p role="alert" className="flex items-start gap-2 rounded-lg bg-tone-danger-bg p-3 text-sm text-tone-danger-fg">
          <CircleAlert aria-hidden="true" className="mt-0.5 size-4 shrink-0" />
          {error}
        </p>
      ) : null}

      {brief ? (
        <>
          <p className="rounded-card border border-line bg-surface p-3 text-xs text-muted">{s.note}</p>

          <Section title={s.awaiting}>
            {brief.awaiting_supervisor.length === 0 ? (
              <p className="text-sm text-muted">{s.noAwaiting}</p>
            ) : (
              <ul className="space-y-2.5">
                {brief.awaiting_supervisor.map((f) => (
                  <li key={f.id} className="rounded-card border border-line bg-surface p-4 shadow-card">
                    <div className="flex flex-wrap items-center gap-2">
                      <PriorityTag priority={f.priority} />
                      <span className="text-xs text-muted">{f.rule_id}</span>
                    </div>
                    <p className="mt-2 text-sm font-semibold">{f.title}</p>
                    {decided[f.id] ? (
                      <p className="mt-3 flex items-center gap-2 text-sm">
                        <StatusBadge status={decided[f.id] as BriefFindingOut["status"]} /> {s.decided}
                      </p>
                    ) : (
                      <div className="mt-3 flex flex-wrap gap-2">
                        <Button onClick={() => decide(f, true)}>
                          <Check aria-hidden="true" className="size-4" />
                          {s.agree}
                        </Button>
                        <Button variant="secondary" onClick={() => decide(f, false)}>
                          <X aria-hidden="true" className="size-4" />
                          {s.disagree}
                        </Button>
                      </div>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </Section>

          {stress.length > 0 ? (
            <Section title={copy.stress.title} description={copy.stress.rateLabel}>
              <ol className="space-y-2.5">
                {stress.map((q, i) => (
                  <li key={q.id} className="rounded-card border border-line bg-surface p-4 shadow-card">
                    <p className="text-sm font-semibold">
                      {i + 1}. {q.text}
                    </p>
                    <p className="mt-1 text-xs text-muted">
                      {copy.stress.why}: {q.reason}
                    </p>
                    <p className="mt-2 border-l-2 border-brand pl-3 text-sm">
                      {q.answer ?? <span className="text-muted">{copy.stress.noAnswer}</span>}
                    </p>
                    <div className="mt-3 flex flex-wrap items-center gap-1.5" role="group" aria-label={copy.stress.rating}>
                      {[1, 2, 3, 4, 5].map((n) => (
                        <button
                          key={n}
                          type="button"
                          aria-pressed={q.rating === n}
                          aria-label={`${copy.stress.rating} ${n}`}
                          onClick={() => rate(q.id, n)}
                          className={`size-11 rounded-lg border text-sm font-semibold ${
                            q.rating === n ? "border-brand bg-brand text-brand-fg" : "border-line bg-surface"
                          }`}
                        >
                          {n}
                        </button>
                      ))}
                    </div>
                  </li>
                ))}
              </ol>
            </Section>
          ) : null}

          <Section title={s.changes}>
            {brief.changes.length === 0 ? (
              <p className="text-sm text-muted">{s.noChanges}</p>
            ) : (
              <ul className="list-disc space-y-1 pl-5 text-sm">
                {brief.changes.map((c) => (
                  <li key={c}>{c}</li>
                ))}
              </ul>
            )}
          </Section>

          {brief.impacts.length > 0 ? (
            <Section title={s.impacts}>
              <ul className="space-y-1.5 text-sm">
                {brief.impacts.map((line) => (
                  <li key={line} className="rounded-lg border border-tone-warning-bg bg-surface px-3 py-2">
                    {line}
                  </li>
                ))}
              </ul>
            </Section>
          ) : null}

          {brief.comments.length > 0 ? (
            <Section title={s.comments}>
              <ul className="space-y-2">
                {brief.comments.map((c) => (
                  <li key={c.comment_id} className="rounded-card border border-line bg-surface p-3 text-sm">
                    “{c.text}”
                    <span className="mt-1.5 flex flex-wrap gap-2">
                      <Badge>{copy.workspace.commentState[c.state]}</Badge>
                      {c.confirmed === null ? null : (
                        <Badge tone={c.confirmed ? "success" : "warning"}>
                          {c.confirmed ? s.studentSays.yes : s.studentSays.no}
                        </Badge>
                      )}
                    </span>
                  </li>
                ))}
              </ul>
            </Section>
          ) : null}

          {brief.open_findings.length > 0 ? (
            <Section title={s.open}>
              <ul className="space-y-1 text-sm">
                {brief.open_findings.map((f) => (
                  <li key={f.id}>
                    [{f.rule_id}] {f.title}
                  </li>
                ))}
              </ul>
            </Section>
          ) : null}

          {brief.resolved_rules.length > 0 ? (
            <p className="text-sm text-muted">
              {s.resolved}: {brief.resolved_rules.join(", ")}
            </p>
          ) : null}
        </>
      ) : null}
    </main>
  );
}
