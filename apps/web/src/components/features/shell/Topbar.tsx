import { BookOpenCheck, Plus, Search, Upload } from "lucide-react";
import Link from "next/link";
import { buttonClass } from "@/components/ui/Button";
import { copy } from "@/lib/copy";

export function Topbar() {
  const s = copy.shell;
  return (
    <header className="sticky top-0 z-10 flex h-16 items-center gap-3 border-b border-line bg-surface/90 px-4 backdrop-blur md:px-6">
      <span className="flex size-8 items-center justify-center rounded-lg bg-brand text-brand-fg md:hidden">
        <BookOpenCheck aria-hidden="true" className="size-4" />
        <span className="sr-only">{s.appName}</span>
      </span>

      <label className="relative hidden max-w-xs flex-1 sm:block">
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
        <Link href="/upload" aria-label={s.upload} className={buttonClass("secondary")}>
          <Upload aria-hidden="true" className="size-4" />
          <span className="hidden sm:inline">{s.upload}</span>
        </Link>
        <Link href="/upload" aria-label={s.newProject} className={buttonClass("primary")}>
          <Plus aria-hidden="true" className="size-4" />
          <span className="hidden sm:inline">{s.newProject}</span>
        </Link>
        <div className="ml-1 hidden items-center gap-2 rounded-full border border-line py-1 pl-1 pr-3 lg:flex">
          <span
            aria-hidden="true"
            className="flex size-8 items-center justify-center rounded-full bg-brand-soft text-xs font-semibold text-brand-strong"
          >
            M
          </span>
          <span className="leading-tight">
            <span className="block text-sm font-medium">{s.project}</span>
            <span className="block text-xs text-muted">{s.program}</span>
          </span>
        </div>
      </div>
    </header>
  );
}
