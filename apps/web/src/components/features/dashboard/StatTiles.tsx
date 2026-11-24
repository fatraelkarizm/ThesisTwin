import { CheckCircle2, Clock, MessageSquareText, type LucideIcon } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { copy } from "@/lib/copy";
import type { stats as Stats } from "./sample";

interface Tile {
  icon: LucideIcon;
  label: string;
  value: string;
  unit: string;
}

export function StatTiles({ stats }: { stats: typeof Stats }) {
  const s = copy.dashboard.stats;
  const tiles: Tile[] = [
    { icon: CheckCircle2, label: s.verified, value: `${stats.verified}/${stats.extracted}`, unit: s.verifiedUnit },
    { icon: MessageSquareText, label: s.comments, value: `${stats.commentsDone}/${stats.commentsTotal}`, unit: s.commentsUnit },
    { icon: Clock, label: s.waiting, value: String(stats.waitingDays), unit: s.waitingUnit },
  ];
  return (
    <Card title={s.title} description={s.description}>
      <ul className="space-y-2">
        {tiles.map(({ icon: Icon, label, value, unit }) => (
          <li key={label} className="flex items-center gap-3 rounded-xl border border-line p-3">
            <span className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-brand-soft text-brand">
              <Icon aria-hidden="true" className="size-4" />
            </span>
            <span className="min-w-0 flex-1">
              <span className="block text-sm font-medium">{label}</span>
              <span className="block text-xs text-muted">{unit}</span>
            </span>
            <span className="text-2xl font-semibold">{value}</span>
          </li>
        ))}
      </ul>
    </Card>
  );
}
