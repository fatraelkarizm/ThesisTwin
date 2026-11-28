import { BookOpenCheck, Check, X } from "lucide-react";
import type { ReactNode } from "react";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Section } from "@/components/ui/Section";
import type { BriefFindingOut, BriefOut, StressQuestionOut } from "@/lib/api";
import { copy, programLabel } from "@/lib/copy";
import { BasisNote } from "./BasisNote";
import { EvidenceChip } from "./EvidenceChip";
import { PriorityTag } from "./PriorityTag";
import { StatusBadge } from "./StatusBadge";

interface BriefDocumentProps {
  brief: BriefOut;
  stress: StressQuestionOut[];
  // Tanpa handler = pratinjau mahasiswa: isi sama persis, tombol dosen diganti keterangan.
  onDecide?: (finding: BriefFindingOut, confirm: boolean) => void;
  onRate?: (questionId: string, score: number) => void;
  decided?: Record<string, BriefFindingOut["status"]>;
  actions?: ReactNode;
}

/** Supervision Brief seperti yang dibaca dosen. Dipakai halaman dosen dan pratinjau mahasiswa. */
export function BriefDocument({ brief, stress, onDecide, onRate, decided = {}, actions }: BriefDocumentProps) {
  const s = copy.supervisor;
  return (
    <div className="space-y-8">
      <header className="flex items-center gap-3">
        <span className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-brand text-brand-fg">
          <BookOpenCheck aria-hidden="true" className="size-5" />
        </span>
        <div className="min-w-0">
          <h2 className="text-xl font-semibold tracking-tight">{s.title}</h2>
          <p className="text-sm text-muted">
            {brief.project_title} · {programLabel(brief.program)} · {s.versions}{" "}
            {brief.from_version ? `v${brief.from_version} → v${brief.to_version}` : `v${brief.to_version}`}
          </p>
        </div>
      </header>

      <div className="flex flex-wrap items-start justify-between gap-3">
        <p className="max-w-xl rounded-card border border-line bg-surface p-3 text-xs text-muted">{s.note}</p>
        {actions}
      </div>

      <Section title={s.awaiting}>
        {brief.awaiting_supervisor.length === 0 ? (
          <p className="text-sm text-muted">{s.noAwaiting}</p>
        ) : (
          <ul className="space-y-2.5">
            {brief.awaiting_supervisor.map((f) => (
              <li key={f.id} className="rounded-card border border-line bg-surface p-4 shadow-card">
                <PriorityTag priority={f.priority} />
                <p className="mt-2 text-sm font-semibold">{f.title}</p>
                {f.why_flagged ? <p className="mt-1 text-sm">{f.why_flagged}</p> : null}
                {f.evidence.length ? (
                  <div className="mt-2 flex flex-wrap gap-2">
                    {f.evidence.map((e, i) => (
                      <EvidenceChip
                        key={`${e.element}-${e.page}-${i}`}
                        evidence={{ ...e, document: `v${brief.to_version}`, unit: brief.unit }}
                      />
                    ))}
                  </div>
                ) : null}
                {f.basis ? (
                  <div className="mt-2">
                    <BasisNote basis={f.basis} sourceTypes={f.source_types} />
                  </div>
                ) : null}
                {decided[f.id] ? (
                  <p className="mt-3 flex items-center gap-2 text-sm">
                    <StatusBadge status={decided[f.id]} /> {s.decided}
                  </p>
                ) : onDecide ? (
                  <div className="mt-3 flex flex-wrap gap-2 print:hidden">
                    <Button onClick={() => onDecide(f, true)}>
                      <Check aria-hidden="true" className="size-4" />
                      {s.agree}
                    </Button>
                    <Button variant="secondary" onClick={() => onDecide(f, false)}>
                      <X aria-hidden="true" className="size-4" />
                      {s.disagree}
                    </Button>
                  </div>
                ) : (
                  <p className="mt-3 text-xs text-muted">{s.previewDecision}</p>
                )}
              </li>
            ))}
          </ul>
        )}
      </Section>

      {stress.length > 0 ? (
        <Section title={copy.stress.title} description={onRate ? copy.stress.rateLabel : undefined}>
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
                {onRate ? (
                  <div
                    className="mt-3 flex flex-wrap items-center gap-1.5 print:hidden"
                    role="group"
                    aria-label={copy.stress.rating}
                  >
                    {[1, 2, 3, 4, 5].map((n) => (
                      <button
                        key={n}
                        type="button"
                        aria-pressed={q.rating === n}
                        aria-label={`${copy.stress.rating} ${n}`}
                        onClick={() => onRate(q.id, n)}
                        className={`size-11 rounded-lg border text-sm font-semibold ${
                          q.rating === n ? "border-brand bg-brand text-brand-fg" : "border-line bg-surface"
                        }`}
                      >
                        {n}
                      </button>
                    ))}
                  </div>
                ) : q.rating ? (
                  <p className="mt-2 text-xs text-muted">
                    {copy.stress.rating}: {q.rating}/5
                  </p>
                ) : null}
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

      {brief.open_summary.length > 0 ? (
        <Section title={s.open}>
          <ul className="list-disc space-y-1 pl-5 text-sm">
            {brief.open_summary.map((line) => (
              <li key={line}>{line}</li>
            ))}
          </ul>
        </Section>
      ) : null}

      {brief.resolved_titles.length > 0 ? (
        <Section title={s.resolved}>
          <ul className="list-disc space-y-1 pl-5 text-sm text-muted">
            {brief.resolved_titles.map((t) => (
              <li key={t}>{t}</li>
            ))}
          </ul>
        </Section>
      ) : null}
    </div>
  );
}
