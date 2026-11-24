import { ChevronRight, FileOutput, GitCompare, ScanSearch, ShieldQuestion, type LucideIcon } from "lucide-react";
import { SimulatedBadge } from "@/components/domain/SimulatedBadge";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { copy } from "@/lib/copy";

interface Tool {
  key: keyof typeof copy.dashboard.tools.items;
  icon: LucideIcon;
  // Anchor di halaman ini bila tool sudah bisa dicoba; tanpa href = belum dibangun.
  href?: string;
}

const tools: Tool[] = [
  { key: "consistency", icon: ScanSearch, href: "#temuan" },
  { key: "compare", icon: GitCompare },
  { key: "brief", icon: FileOutput },
  { key: "stressTest", icon: ShieldQuestion },
];

const row = "flex items-center gap-3 rounded-xl border border-line p-3";

export function ToolsPanel() {
  const t = copy.dashboard.tools;
  return (
    <Card title={t.title} description={t.description}>
      <ul className="space-y-2">
        {tools.map(({ key, icon: Icon, href }) => {
          const item = t.items[key];
          const body = (
            <>
              <span className="flex size-10 shrink-0 items-center justify-center rounded-lg bg-brand-soft text-brand">
                <Icon aria-hidden="true" className="size-5" />
              </span>
              <span className="min-w-0 flex-1">
                <span className="block text-sm font-semibold">{item.title}</span>
                <span className="mt-1 block">{href ? <SimulatedBadge /> : <Badge>{copy.soon}</Badge>}</span>
                <span className="mt-1 block text-xs text-muted">{item.body}</span>
              </span>
              <ChevronRight aria-hidden="true" className={`size-4 shrink-0 ${href ? "text-foreground" : "text-muted"}`} />
            </>
          );
          return (
            <li key={key}>
              {href ? (
                <a
                  href={href}
                  className={`${row} hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-brand`}
                >
                  {body}
                </a>
              ) : (
                <div aria-disabled="true" title={copy.shell.soonHint} className={`${row} cursor-not-allowed`}>
                  {body}
                </div>
              )}
            </li>
          );
        })}
      </ul>
    </Card>
  );
}
