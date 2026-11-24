import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { copy } from "@/lib/copy";
import type { Finding } from "@/types/domain";
import { AiLabel } from "./AiLabel";
import { ConfidenceMeter } from "./ConfidenceMeter";
import { EvidenceChip } from "./EvidenceChip";
import { PriorityTag } from "./PriorityTag";
import { StatusBadge } from "./StatusBadge";

interface FindingCardProps {
  finding: Finding;
  onConfirm?: (id: string) => void;
  onReject?: (id: string) => void;
}

export function FindingCard({ finding, onConfirm, onReject }: FindingCardProps) {
  const hasEvidence = finding.evidence.length > 0;
  return (
    <article className="space-y-3 rounded-card border border-line bg-surface p-4 shadow-card">
      <header className="flex flex-wrap items-center gap-2">
        <PriorityTag priority={finding.priority} />
        <StatusBadge status={hasEvidence ? finding.status : "needs_user_confirmation"} />
        {finding.aiGenerated ? <AiLabel /> : <Badge>{copy.ruleBased} {finding.ruleId}</Badge>}
        <ConfidenceMeter value={finding.confidence} aiGenerated={finding.aiGenerated} />
      </header>
      <h3 className="text-base font-semibold">{finding.title}</h3>
      <p className="text-sm">
        <span className="font-medium">{copy.whyFlagged}: </span>
        {finding.whyFlagged}
      </p>
      <p className="text-sm">
        <span className="font-medium">{copy.suggestion}: </span>
        {finding.suggestedClarification}
      </p>
      {finding.directions?.length ? (
        <div className="rounded-lg bg-brand-soft/60 p-3">
          <p className="text-sm font-semibold text-brand-strong">{copy.directionsTitle}</p>
          <p className="text-xs text-muted">{copy.directionsNote}</p>
          <ul className="mt-2 space-y-2 text-sm">
            {finding.directions.map((d) => (
              <li key={d.option} className="border-l-2 border-brand pl-2">
                <p className="font-medium">{d.option}</p>
                <p className="text-muted">
                  <span className="font-medium">{copy.directionImplication}: </span>
                  {d.implication}
                </p>
              </li>
            ))}
          </ul>
        </div>
      ) : null}
      {finding.basis ? (
        <p className="border-l-2 border-line pl-2 text-xs text-muted">
          <span className="font-medium">
            {copy.basis}
            {finding.sourceTypes?.length
              ? ` (${finding.sourceTypes.map((t) => copy.sourceType[t]).join(", ")})`
              : ""}
            :{" "}
          </span>
          {finding.basis}
        </p>
      ) : null}
      {finding.references?.length ? (
        <details className="text-xs">
          <summary className="cursor-pointer font-medium text-brand-strong">
            {copy.referencesTitle(finding.references.length)}
          </summary>
          <ul className="mt-1.5 space-y-1 pl-4 text-muted">
            {finding.references.map((r) => (
              <li key={r} className="-indent-4 pl-4">
                {r}
              </li>
            ))}
          </ul>
          <p className="mt-1 italic text-muted">{copy.referencesNote}</p>
        </details>
      ) : null}
      <div className="flex flex-wrap gap-2">
        {hasEvidence ? (
          finding.evidence.map((e, i) => <EvidenceChip key={`${e.element}-${e.page}-${i}`} evidence={e} />)
        ) : (
          <span className="text-xs text-muted">{copy.noEvidence}</span>
        )}
      </div>
      {onConfirm || onReject ? (
        <footer className="flex gap-2">
          {onConfirm ? <Button onClick={() => onConfirm(finding.id)}>{copy.confirm}</Button> : null}
          {onReject ? (
            <Button variant="secondary" onClick={() => onReject(finding.id)}>
              {copy.reject}
            </Button>
          ) : null}
        </footer>
      ) : null}
    </article>
  );
}
