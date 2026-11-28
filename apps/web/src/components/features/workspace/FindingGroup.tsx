import { AiLabel } from "@/components/domain/AiLabel";
import { EvidenceChip } from "@/components/domain/EvidenceChip";
import { FindingCard } from "@/components/domain/FindingCard";
import { FindingGuidance } from "@/components/domain/FindingGuidance";
import { PriorityTag } from "@/components/domain/PriorityTag";
import { StatusBadge } from "@/components/domain/StatusBadge";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { copy } from "@/lib/copy";
import type { Finding, Priority } from "@/types/domain";

const RANK: Record<Priority, number> = { high: 0, medium: 1, low: 2 };
export const isOpen = (f: Finding) => f.status === "ai_suggested" || f.status === "needs_user_confirmation";
// Rincian per temuan ditambahkan engine sebagai " (rincian)" di akhir alasan.
const DETAIL_SUFFIX = /\s*\([^()]*\)$/;

export interface Group {
  ruleId: string;
  findings: Finding[];
}

/** Kelompokkan per aturan, urut prioritas. Satu aturan bisa memicu beberapa temuan
 *  (mis. empat bagian wajib yang belum ada); mengulang landasan & arahnya empat kali tidak membantu. */
export function groupFindings(findings: Finding[]): Group[] {
  const byRule = new Map<string, Finding[]>();
  for (const f of findings) byRule.set(f.ruleId, [...(byRule.get(f.ruleId) ?? []), f]);
  return [...byRule]
    .map(([ruleId, list]) => ({ ruleId, findings: list }))
    .sort((a, b) => RANK[a.findings[0].priority] - RANK[b.findings[0].priority]);
}

/** Judul aturan bersama: bagian sebelum ": rincian" bila semua judul berbagi awalan itu. */
function sharedTitle(findings: Finding[]): { base: string; details: string[] } {
  const base = findings[0].title.split(": ")[0];
  const prefix = `${base}: `;
  return findings.every((f) => f.title.startsWith(prefix))
    ? { base, details: findings.map((f) => f.title.slice(prefix.length)) }
    : { base: findings[0].ruleId, details: findings.map((f) => f.title) };
}

interface FindingGroupProps {
  group: Group;
  onConfirm?: (id: string) => void;
  onReject?: (id: string) => void;
}

export function FindingGroup({ group, onConfirm, onReject }: FindingGroupProps) {
  const [first] = group.findings;
  if (group.findings.length === 1) {
    return isOpen(first) ? <FindingCard finding={first} onConfirm={onConfirm} onReject={onReject} /> : <FindingCard finding={first} />;
  }
  const { base, details } = sharedTitle(group.findings);
  return (
    <article className="space-y-3 rounded-card border border-line bg-surface p-4 shadow-card">
      <header className="flex flex-wrap items-center gap-2">
        <PriorityTag priority={first.priority} />
        {group.findings.some((f) => f.aiGenerated) ? <AiLabel /> : <Badge>{copy.ruleBased} {group.ruleId}</Badge>}
        <span className="text-xs text-muted">{copy.workspace.groupCount(group.findings.length)}</span>
      </header>
      <h3 className="text-base font-semibold">{base}</h3>
      <p className="text-sm">
        <span className="font-medium">{copy.whyFlagged}: </span>
        {first.whyFlagged.replace(DETAIL_SUFFIX, "")}
      </p>
      <p className="text-sm">
        <span className="font-medium">{copy.suggestion}: </span>
        {first.suggestedClarification}
      </p>
      <ul className="divide-y divide-line rounded-lg border border-line">
        {group.findings.map((f, i) => {
          const hasEvidence = f.evidence.length > 0;
          return (
            <li key={f.id} className="flex flex-wrap items-center gap-2 px-3 py-2.5">
              <span className="min-w-0 flex-1 basis-48 space-y-1.5">
                <span className="block text-sm font-medium">{details[i]}</span>
                <span className="flex flex-wrap gap-1.5">
                  {hasEvidence ? (
                    f.evidence.map((e, k) => <EvidenceChip key={`${e.element}-${e.page}-${k}`} evidence={e} />)
                  ) : (
                    <span className="text-xs text-muted">{copy.noEvidence}</span>
                  )}
                </span>
              </span>
              <StatusBadge status={hasEvidence ? f.status : "needs_user_confirmation"} />
              {(onConfirm || onReject) && isOpen(f) ? (
                <span className="flex gap-2">
                  {onConfirm ? (
                    <Button onClick={() => onConfirm(f.id)} aria-label={`${copy.confirm}: ${details[i]}`}>
                      {copy.confirm}
                    </Button>
                  ) : null}
                  {onReject ? (
                    <Button
                      variant="secondary"
                      onClick={() => onReject(f.id)}
                      aria-label={`${copy.reject}: ${details[i]}`}
                    >
                      {copy.reject}
                    </Button>
                  ) : null}
                </span>
              ) : null}
            </li>
          );
        })}
      </ul>
      <FindingGuidance finding={first} />
    </article>
  );
}
