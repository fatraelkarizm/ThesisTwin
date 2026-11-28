"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { copy } from "@/lib/copy";
import { homeItem, settingsItem, stepItems, type NavItem } from "./nav";

function Item({ item, active, onNavigate }: { item: NavItem; active: boolean; onNavigate?: () => void }) {
  const { label, icon: Icon, href, step } = item;
  return (
    <li>
      <Link
        href={href}
        onClick={onNavigate}
        aria-current={active ? "page" : undefined}
        className={`flex min-h-11 items-center gap-3 rounded-lg px-3 text-sm focus-visible:outline-2 focus-visible:outline-brand ${
          active ? "bg-brand-soft font-medium text-brand-strong" : "text-foreground hover:bg-surface-muted"
        }`}
      >
        {step ? (
          <span
            aria-hidden="true"
            className={`flex size-5 shrink-0 items-center justify-center rounded-full text-[11px] font-semibold tabular-nums ${
              active ? "bg-brand text-brand-fg" : "bg-surface-muted text-muted"
            }`}
          >
            {step}
          </span>
        ) : (
          <Icon aria-hidden="true" className="size-4 shrink-0" />
        )}
        <span className="flex-1">{label}</span>
        {step ? <Icon aria-hidden="true" className="size-4 shrink-0 text-muted" /> : null}
      </Link>
    </li>
  );
}

/** Beranda, 5 langkah alur kerja (bernomor), lalu Pengaturan. Dipakai sidebar & menu mobile. */
export function NavList({ onNavigate }: { onNavigate?: () => void }) {
  const pathname = usePathname();
  const item = (it: NavItem) => (
    <Item key={it.href} item={it} active={pathname === it.href} onNavigate={onNavigate} />
  );
  return (
    <div className="flex h-full flex-col gap-4">
      <ul className="space-y-1">{item(homeItem)}</ul>
      <div>
        <p className="px-3 pb-1.5 text-xs font-semibold uppercase tracking-wide text-muted">{copy.shell.workflow}</p>
        <ul className="space-y-1">{stepItems.map(item)}</ul>
      </div>
      <ul className="mt-auto space-y-1 border-t border-line pt-3">{item(settingsItem)}</ul>
    </div>
  );
}
