import { Card } from "@/components/ui/Card";
import { copy } from "@/lib/copy";
import type { VersionSummary } from "./sample";

export function VersionCards({ versions }: { versions: VersionSummary[] }) {
  const c = copy.dashboard.check;
  return (
    <Card title={c.title} description={c.description}>
      <ul className="grid gap-3 sm:grid-cols-2">
        {versions.map((v) => (
          <li key={v.version} className="rounded-xl border border-line p-4">
            <div className="flex items-center gap-2">
              <span
                className={`flex size-6 items-center justify-center rounded-md text-xs font-semibold ${
                  v.latest ? "bg-brand text-brand-fg" : "bg-surface-muted text-foreground"
                }`}
              >
                v{v.version}
              </span>
              <span className="text-sm font-medium">{copy.dashboard.proposal} v{v.version}</span>
            </div>
            <div className="mt-3 flex items-end justify-between gap-2 rounded-lg border border-line p-3">
              <span className="text-sm text-muted">{c.openFindings}</span>
              <span className={`text-3xl font-semibold ${v.latest ? "text-brand" : "text-foreground"}`}>
                {v.openFindings}
              </span>
            </div>
            <p className="mt-3 text-sm">{v.summary}</p>
            <p className="mt-3 inline-block rounded-md bg-surface-muted px-2 py-1 text-xs text-muted">
              {c.uploaded}: {v.uploadedAt}
            </p>
          </li>
        ))}
      </ul>
    </Card>
  );
}
