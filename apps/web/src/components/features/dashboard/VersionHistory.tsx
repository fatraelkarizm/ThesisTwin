import { FileText } from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { Section } from "@/components/ui/Section";
import { SegmentedBar } from "@/components/ui/SegmentedBar";
import { copy } from "@/lib/copy";
import type { VersionSummary } from "./sample";

export function VersionHistory({ versions, unitLabel }: { versions: VersionSummary[]; unitLabel?: string }) {
  const h = copy.dashboard.history;
  const c = copy.dashboard.check;
  return (
    <Section title={h.title} description={h.description}>
      <ul className="space-y-3">
        {versions.map((v) => {
          const label = `${v.sectionsChecked} ${copy.dashboard.of} ${v.sectionsTotal} ${unitLabel ?? h.sectionsChecked}`;
          return (
            <li
              key={v.version}
              className="flex flex-wrap items-center gap-4 rounded-card border border-line bg-surface p-3 shadow-card"
            >
              <span className="flex size-10 shrink-0 items-center justify-center rounded-lg bg-brand-soft text-brand-strong">
                <FileText aria-hidden="true" className="size-5" />
              </span>
              <div className="min-w-0 flex-1">
                <p className="flex items-center gap-2 text-sm font-semibold">
                  {copy.dashboard.proposal} v{v.version}
                  <Badge>{v.latest ? c.latest : c.archived}</Badge>
                </p>
                <p className="text-xs text-muted">
                  {c.uploaded}: {v.uploadedAt}
                </p>
              </div>
              <div className="w-full sm:w-64">
                <p className="mb-1.5 text-right text-xs font-medium tabular-nums">{label}</p>
                <SegmentedBar value={v.sectionsChecked} total={v.sectionsTotal} label={label} />
              </div>
            </li>
          );
        })}
      </ul>
    </Section>
  );
}
