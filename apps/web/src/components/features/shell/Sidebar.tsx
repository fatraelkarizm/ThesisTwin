"use client";

import { BookOpenCheck, Share2 } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Button } from "@/components/ui/Button";
import { copy } from "@/lib/copy";
import { navItems } from "./nav";

const itemBase = "flex min-h-11 items-center gap-3 rounded-lg px-3 text-sm";

export function Sidebar() {
  const pathname = usePathname();
  const s = copy.shell;

  return (
    <aside className="hidden w-60 shrink-0 flex-col border-r border-line bg-surface md:flex">
      <div className="flex h-16 items-center gap-2 px-5">
        <span className="flex size-8 items-center justify-center rounded-lg bg-brand text-brand-fg">
          <BookOpenCheck aria-hidden="true" className="size-4" />
        </span>
        <span className="text-lg font-semibold">{s.appName}</span>
      </div>

      <nav aria-label={s.navLabel} className="flex-1 px-3 py-2">
        <p className="px-3 pb-2 text-xs font-medium text-muted">{s.menu}</p>
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
                    <span className="text-[11px]">{copy.soon}</span>
                  </span>
                </li>
              );
            }
            const active = pathname === href;
            return (
              <li key={label}>
                <Link
                  href={href}
                  aria-current={active ? "page" : undefined}
                  className={`${itemBase} focus-visible:outline-2 focus-visible:outline-brand ${
                    active
                      ? "border border-brand bg-brand-soft font-medium text-foreground"
                      : "text-foreground hover:bg-surface-muted"
                  }`}
                >
                  <Icon aria-hidden="true" className="size-4" />
                  {label}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      <div className="m-3 rounded-card bg-brand p-4 text-brand-fg">
        <Share2 aria-hidden="true" className="mb-2 size-5" />
        <p className="text-sm font-semibold">{s.shareTitle}</p>
        <p className="mt-1 text-xs">{s.shareBody}</p>
        <Button variant="secondary" disabled title={s.soonHint} className="mt-3 w-full">
          {s.shareAction} · {copy.soon}
        </Button>
      </div>
    </aside>
  );
}
