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
    <main className="grid flex-1 lg:grid-cols-[minmax(0,1fr)_360px]">
      {/* Kolom utama putih, kolom kanan berwarna lembut: pola Notalx. */}
      <div className="space-y-8 bg-surface p-4 md:p-6">
        <header className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <h1 className="text-2xl font-semibold tracking-tight">{d.title}</h1>
            <p className="text-sm text-muted">{d.subtitle}</p>
          </div>
          <div className="flex max-w-sm items-start gap-2">
            <SimulatedBadge />
            <p className="text-xs text-muted">{d.simulatedNote}</p>
          </div>
        </header>
        <VersionCards versions={versions} />
        <FindingQueue initial={findings} />
        <VersionHistory versions={versions} />
      </div>
      <div className="space-y-8 border-t border-line bg-background p-4 md:p-6 lg:border-l lg:border-t-0">
        <ToolsPanel />
        <StatTiles stats={stats} />
      </div>
    </main>
  );
}
