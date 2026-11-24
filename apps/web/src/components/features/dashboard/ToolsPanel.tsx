import { ChevronRight, FileOutput, GitCompare, ScanSearch, ShieldQuestion, type LucideIcon } from "lucide-react";
import { SimulatedBadge } from "@/components/domain/SimulatedBadge";
import { Badge } from "@/components/ui/Badge";
import { Section } from "@/components/ui/Section";
import { copy } from "@/lib/copy";

interface Tool {
  key: keyof typeof copy.dashboard.tools.items;
  icon: LucideIcon;
  // Anchor di halaman ini bila tool sudah bisa dicoba; tanpa href = belum dibangun.
  href?: string;
}

const demoTools: Tool[] = [
  { key: "consistency", icon: ScanSearch, href: "#temuan" },
  { key: "compare", icon: GitCompare },
  { key: "brief", icon: FileOutput },
  { key: "stressTest", icon: ShieldQuestion },
];

// Dengan proyek nyata tiap tool punya halaman sendiri.
const liveTools: Tool[] = [
  { key: "consistency", icon: ScanSearch, href: "/temuan" },
  { key: "compare", icon: GitCompare, href: "/versi" },
  { key: "brief", icon: FileOutput, href: "/brief" },
  { key: "stressTest", icon: ShieldQuestion, href: "/stress-test" },
];

const row = "flex items-center gap-3 rounded-card border border-line bg-surface p-3 shadow-card";

export function ToolsPanel({ live = false }: { live?: boolean }) {
  const t = copy.dashboard.tools;
  const tools = live ? liveTools : demoTools;
  return (
    <Section title={t.title} description={t.description}>
      <ul className="space-y-2.5">
        {tools.map(({ key, icon: Icon, href }) => {
          const item = t.items[key];
          const body = (
            <>
              <span
                className={`flex size-10 shrink-0 items-center justify-center rounded-full border-2 border-dashed ${
                  href ? "border-brand text-brand-strong" : "border-line text-muted"
                }`}
              >
                <Icon aria-hidden="true" className="size-4" />
              </span>
              <span className="min-w-0 flex-1">
                <span className="block text-sm font-semibold">{item.title}</span>
                <span className="mt-1 flex flex-wrap items-center gap-1.5">
                  {!href ? <Badge>{copy.soon}</Badge> : live ? <Badge tone="success">{t.available}</Badge> : <SimulatedBadge />}
                </span>
                <span className="mt-1 block text-xs text-muted">{item.body}</span>
              </span>
              <ChevronRight aria-hidden="true" className={`size-4 shrink-0 ${href ? "text-foreground" : "text-muted"}`} />
            </>
          );
          return (
            <li key={key}>
              {href ? (
                <a href={href} className={`${row} hover:border-brand focus-visible:outline-2 focus-visible:outline-brand`}>
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
    </Section>
  );
}
