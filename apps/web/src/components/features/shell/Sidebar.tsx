import { BookOpenCheck } from "lucide-react";
import { copy } from "@/lib/copy";
import { NavList } from "./NavList";

export function Sidebar() {
  const s = copy.shell;
  return (
    <aside className="sticky top-0 hidden h-dvh w-60 shrink-0 flex-col border-r border-line bg-background md:flex">
      <div className="flex h-16 items-center gap-2.5 px-5">
        <span className="flex size-8 items-center justify-center rounded-lg bg-brand text-brand-fg shadow-card">
          <BookOpenCheck aria-hidden="true" className="size-4" />
        </span>
        <span className="text-lg font-semibold tracking-tight">{s.appName}</span>
      </div>
      <nav aria-label={s.navLabel} className="flex-1 overflow-y-auto px-3 pt-2 pb-4">
        <NavList />
      </nav>
    </aside>
  );
}
