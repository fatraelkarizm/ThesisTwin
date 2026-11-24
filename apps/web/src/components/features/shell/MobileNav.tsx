"use client";

import { Menu, X } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useId, useState } from "react";
import { copy } from "@/lib/copy";
import { navItems } from "./nav";

// Pengganti sidebar di layar < 768px.
export function MobileNav() {
  const s = copy.shell;
  const [open, setOpen] = useState(false);
  const pathname = usePathname();
  const panelId = useId();

  return (
    <div className="md:hidden">
      <button
        type="button"
        aria-expanded={open}
        aria-controls={panelId}
        onClick={() => setOpen((v) => !v)}
        className="flex size-11 items-center justify-center rounded-lg border border-line"
      >
        {open ? <X aria-hidden="true" className="size-5" /> : <Menu aria-hidden="true" className="size-5" />}
        <span className="sr-only">{s.menu}</span>
      </button>
      {open ? (
        <nav
          id={panelId}
          aria-label={s.navLabel}
          className="absolute inset-x-0 top-16 z-20 border-b border-line bg-surface p-3 shadow-card"
        >
          <ul className="space-y-1">
            {navItems
              .filter((item) => item.href)
              .map(({ label, icon: Icon, href }) => (
                <li key={label}>
                  <Link
                    href={href!}
                    onClick={() => setOpen(false)}
                    aria-current={pathname === href ? "page" : undefined}
                    className={`flex min-h-11 items-center gap-3 rounded-lg px-3 text-sm ${
                      pathname === href ? "bg-brand-soft font-medium text-brand-strong" : ""
                    }`}
                  >
                    <Icon aria-hidden="true" className="size-4" />
                    {label}
                  </Link>
                </li>
              ))}
          </ul>
        </nav>
      ) : null}
    </div>
  );
}
