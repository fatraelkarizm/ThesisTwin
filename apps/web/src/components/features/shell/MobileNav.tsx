"use client";

import { Menu, X } from "lucide-react";
import { useId, useState } from "react";
import { copy } from "@/lib/copy";
import { NavList } from "./NavList";

// Pengganti sidebar di layar < 768px.
export function MobileNav() {
  const s = copy.shell;
  const [open, setOpen] = useState(false);
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
          <NavList onNavigate={() => setOpen(false)} />
        </nav>
      ) : null}
    </div>
  );
}
