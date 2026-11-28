import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { copy } from "@/lib/copy";
import type { Finding } from "@/types/domain";
import { AiLabel } from "./AiLabel";
import { ConfidenceMeter } from "./ConfidenceMeter";
import { EvidenceChip } from "./EvidenceChip";
import { FindingGuidance } from "./FindingGuidance";
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
      <div className="flex flex-wrap gap-2">
        {hasEvidence ? (
          finding.evidence.map((e, i) => <EvidenceChip key={`${e.element}-${e.page}-${i}`} evidence={e} />)
        ) : (
          <span className="text-xs text-muted">{copy.noEvidence}</span>
        )}
      </div>
      <FindingGuidance finding={finding} />
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
