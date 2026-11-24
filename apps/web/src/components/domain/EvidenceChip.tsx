import type { Evidence } from "@/types/domain";

export function EvidenceChip({ evidence }: { evidence: Evidence }) {
  const where = evidence.unit === "section" ? "bagian" : "hal.";
  return (
    <span className="inline-flex items-center gap-1 rounded-md border border-line bg-surface-muted px-2 py-1 text-xs">
      <span className="font-medium">{evidence.element}</span>
      <span className="text-muted">
        · {evidence.document}, {where} {evidence.page}
      </span>
    </span>
  );
}
