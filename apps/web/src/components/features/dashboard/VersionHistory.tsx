import { FileText } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { SegmentedBar } from "@/components/ui/SegmentedBar";
import { copy } from "@/lib/copy";
import type { VersionSummary } from "./sample";

export function VersionHistory({ versions }: { versions: VersionSummary[] }) {
  const h = copy.dashboard.history;
  return (
    <Card title={h.title} description={h.description}>
      <ul className="space-y-3">
        {versions.map((v) => {
          const label = `${v.sectionsChecked} ${copy.dashboard.of} ${v.sectionsTotal} ${h.sectionsChecked}`;
          return (
            <li key={v.version} className="flex items-center gap-4 rounded-xl border border-line p-3">
              <span className="flex size-10 shrink-0 items-center justify-center rounded-lg bg-brand-soft text-brand">
                <FileText aria-hidden="true" className="size-5" />
              </span>
              <div className="min-w-0 flex-1">
                <p className="text-sm font-medium">{copy.dashboard.proposal} v{v.version}</p>
                <p className="text-xs text-muted">{v.uploadedAt}</p>
              </div>
              <div className="w-32 shrink-0 sm:w-48">
                <SegmentedBar value={v.sectionsChecked} total={v.sectionsTotal} label={label} />
                <p className="mt-1 text-right text-xs text-muted">{label}</p>
              </div>
            </li>
          );
        })}
      </ul>
    </Card>
  );
}
