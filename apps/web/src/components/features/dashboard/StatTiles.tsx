import { CheckCircle2, Clock, MessageSquareText, type LucideIcon } from "lucide-react";
import { Section } from "@/components/ui/Section";
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
    <Section title={s.title} description={s.description}>
      <ul className="grid grid-cols-3 gap-2.5">
        {tiles.map(({ icon: Icon, label, value, unit }) => (
          <li key={label} className="flex flex-col rounded-card border border-line bg-surface p-3 shadow-card">
            <Icon aria-hidden="true" className="size-4 text-brand-strong" />
            <p className="mt-1.5 text-xs font-medium leading-snug">{label}</p>
            <p className="mt-auto pt-4 text-2xl font-semibold tabular-nums">{value}</p>
            <p className="text-[11px] text-muted">{unit}</p>
          </li>
        ))}
      </ul>
    </Section>
  );
}
