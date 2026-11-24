import { BookOpenCheck, Plus, Search, Upload } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { copy } from "@/lib/copy";

export function Topbar() {
  const s = copy.shell;
  return (
    <header className="flex h-16 items-center gap-3 border-b border-line bg-surface px-4 md:px-6">
      <span className="flex size-8 items-center justify-center rounded-lg bg-brand text-brand-fg md:hidden">
        <BookOpenCheck aria-hidden="true" className="size-4" />
        <span className="sr-only">{s.appName}</span>
      </span>

      <label className="relative hidden max-w-sm flex-1 sm:block">
        <span className="sr-only">{s.search}</span>
        <Search aria-hidden="true" className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted" />
        <input
          type="search"
          name="q"
          disabled
          title={s.soonHint}
          placeholder={s.search}
          className="h-10 w-full rounded-lg border border-line bg-surface pl-9 pr-3 text-sm placeholder:text-muted disabled:cursor-not-allowed"
        />
      </label>

      <div className="ml-auto flex items-center gap-2">
        <div className="hidden text-right lg:block">
          <p className="text-sm font-medium">{s.project}</p>
          <p className="text-xs text-muted">{s.program}</p>
        </div>
        <Button variant="secondary" disabled title={s.soonHint} aria-label={s.upload}>
          <Upload aria-hidden="true" className="size-4" />
          <span className="hidden sm:inline">{s.upload}</span>
        </Button>
        <Button disabled title={s.soonHint} aria-label={s.newProject}>
          <Plus aria-hidden="true" className="size-4" />
          <span className="hidden sm:inline">{s.newProject}</span>
        </Button>
      </div>
    </header>
  );
}
