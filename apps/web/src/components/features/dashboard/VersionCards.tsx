import { Section } from "@/components/ui/Section";
import { copy } from "@/lib/copy";
import type { VersionSummary } from "./sample";

export function VersionCards({ versions }: { versions: VersionSummary[] }) {
  const c = copy.dashboard.check;
  return (
    <Section title={c.title} description={c.description}>
      <ul className="grid gap-4 sm:grid-cols-2">
        {versions.map((v) => (
          <li key={v.version} className="rounded-card border border-line bg-surface p-3 shadow-card">
            <div className="flex items-center gap-2 px-1 pb-2">
              <span
                className={`flex size-6 items-center justify-center rounded-md text-xs font-semibold ${
                  v.latest ? "bg-brand-soft text-brand-strong" : "bg-surface-muted text-muted"
                }`}
              >
                v{v.version}
              </span>
              <span className="text-sm font-semibold">
                {copy.dashboard.proposal} v{v.version}
              </span>
              <span className="ml-auto text-xs text-muted">{v.latest ? c.latest : c.archived}</span>
            </div>
            <div className="rounded-lg border border-line p-3">
              <div className="flex items-center justify-between gap-2">
                <span className="text-xs text-muted">{c.openFindings}</span>
                <span
                  className={`text-3xl font-semibold tabular-nums ${v.latest ? "text-brand-strong" : "text-foreground"}`}
                >
                  {v.openFindings}
                </span>
              </div>
              <p className="mt-2 line-clamp-2 text-xs text-muted">{v.summary}</p>
            </div>
            <p className="mt-3 inline-block rounded-full bg-surface-muted px-2.5 py-1 text-[11px] text-muted">
              {c.uploaded}: {v.uploadedAt}
            </p>
          </li>
        ))}
      </ul>
    </Section>
  );
}
