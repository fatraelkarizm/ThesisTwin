import { SimulatedBadge } from "@/components/domain/SimulatedBadge";
import { FindingQueue } from "@/components/features/dashboard/FindingQueue";
import { StatTiles } from "@/components/features/dashboard/StatTiles";
import { ToolsPanel } from "@/components/features/dashboard/ToolsPanel";
import { VersionCards } from "@/components/features/dashboard/VersionCards";
import { VersionHistory } from "@/components/features/dashboard/VersionHistory";
import { findings, stats, versions } from "@/components/features/dashboard/sample";
import { copy } from "@/lib/copy";

export default function DashboardPage() {
  const d = copy.dashboard;
  return (
    <main className="mx-auto w-full max-w-7xl space-y-5 p-4 md:p-6">
      <header className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-2xl font-semibold">{d.title}</h1>
          <p className="text-sm text-muted">{d.subtitle}</p>
        </div>
        <div className="flex items-center gap-2">
          <SimulatedBadge />
          <p className="max-w-xs text-xs text-muted">{d.simulatedNote}</p>
        </div>
      </header>

      <div className="grid gap-5 lg:grid-cols-[minmax(0,1fr)_340px]">
        <div className="space-y-5">
          <VersionCards versions={versions} />
          <div id="temuan" className="scroll-mt-4">
            <FindingQueue initial={findings} />
          </div>
          <VersionHistory versions={versions} />
        </div>
        <div className="space-y-5">
          <ToolsPanel />
          <StatTiles stats={stats} />
        </div>
      </div>
    </main>
  );
}
