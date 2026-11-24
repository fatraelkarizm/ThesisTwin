"use client";

import { BookOpenCheck } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { copy } from "@/lib/copy";
import { navItems } from "./nav";

const itemBase = "flex min-h-11 items-center gap-3 rounded-lg px-3 text-sm";

export function Sidebar() {
  const pathname = usePathname();
  const s = copy.shell;

  return (
    <aside className="sticky top-0 hidden h-dvh w-60 shrink-0 flex-col border-r border-line bg-background md:flex">
      <div className="flex h-16 items-center gap-2.5 px-5">
        <span className="flex size-8 items-center justify-center rounded-lg bg-brand text-brand-fg shadow-card">
          <BookOpenCheck aria-hidden="true" className="size-4" />
        </span>
        <span className="text-lg font-semibold tracking-tight">{s.appName}</span>
      </div>

      <nav aria-label={s.navLabel} className="flex-1 overflow-y-auto px-3 py-2">
        <ul className="space-y-1">
          {navItems.map(({ label, icon: Icon, href }) => {
            if (!href) {
              return (
                <li key={label}>
                  <span
                    aria-disabled="true"
                    title={s.soonHint}
                    className={`${itemBase} cursor-not-allowed text-muted`}
                  >
                    <Icon aria-hidden="true" className="size-4" />
                    <span className="flex-1">{label}</span>
                    <span className="rounded-full bg-surface-muted px-2 py-0.5 text-[11px]">{copy.soon}</span>
                  </span>
                </li>
              );
            }
            // Beberapa menu menunjuk bagian di /proyek (#anchor); yang aktif hanya yang path-nya persis.
            const active = pathname === href;
            return (
              <li key={label}>
                <Link
                  href={href}
                  aria-current={active ? "page" : undefined}
                  className={`${itemBase} focus-visible:outline-2 focus-visible:outline-brand ${
                    active
                      ? "border border-brand bg-surface font-medium text-foreground shadow-card"
                      : "text-foreground hover:bg-surface"
                  }`}
                >
                  <Icon aria-hidden="true" className={`size-4 ${active ? "text-brand-strong" : ""}`} />
                  {label}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

    </aside>
  );
}
