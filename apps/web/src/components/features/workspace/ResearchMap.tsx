"use client";

import { ArrowDown, ArrowLeft, ArrowRight, CircleAlert } from "lucide-react";
import { Fragment } from "react";
import { Badge } from "@/components/ui/Badge";
import type { ElementOut, ElementType, GraphOut, OntologyOut } from "@/lib/api";
import { copy } from "@/lib/copy";

export type TypeInfo = OntologyOut["element_types"][number];

export interface Numbered {
  el: ElementOut;
  code: string; // R1, T2, ... dari `code` di ontologi
}

/** Nomori elemen per tipe sesuai urutan halaman: R1, R2, T1, ... */
export function numberElements(elements: ElementOut[], ontology: OntologyOut): Numbered[] {
  const codes = new Map(ontology.element_types.map((t) => [t.id, t.code]));
  const counter = new Map<ElementType, number>();
  return [...elements]
    .sort((a, b) => a.page - b.page)
    .map((el) => {
      const n = (counter.get(el.type) ?? 0) + 1;
      counter.set(el.type, n);
      return { el, code: `${codes.get(el.type) ?? "?"}${n}` };
    });
}

/** "Representasi Geometris: Bagaimana ..." -> judul + isi. Judul hanya diambil bila mahasiswa
 *  sendiri menulis label Title Case sebelum titik dua; tidak pernah dikarang. Kata pendek
 *  ("dan", "di") boleh huruf kecil. */
export function splitTitle(content: string): { title: string | null; body: string } {
  const i = content.indexOf(":");
  const label = content.slice(0, i).trim();
  const isLabel =
    i > 0 && i <= 60 && label.split(/\s+/).every((word) => word.length <= 3 || /^\p{Lu}/u.test(word));
  return isLabel ? { title: label, body: content.slice(i + 1).trim() } : { title: null, body: content };
}

interface ResearchMapProps {
  ontology: OntologyOut;
  numbered: Numbered[];
  gaps: GraphOut["gaps"];
  selected: ElementType;
  onSelect: (type: ElementType) => void;
}

const COLS = 3;

/** Peta alur proposal: kotak per tipe elemen (urutan dari `map` di ontologi), berkelok tiga kolom
 *  agar terbaca seperti alur Bab I -> Bab III. */
export function ResearchMap({ ontology, numbered, gaps, selected, onSelect }: ResearchMapProps) {
  const w = copy.workspace;
  const types = new Map(ontology.element_types.map((t) => [t.id, t]));
  const slots = ontology.map.map((id, i) => {
    const row = Math.floor(i / COLS);
    const col = row % 2 === 0 ? i % COLS : COLS - 1 - (i % COLS);
    return { id, row, col };
  });
  const cell = (row: number, col: number) => ({ gridRow: row * 2 + 1, gridColumn: col * 2 + 1 });

  return (
    <div className="rounded-card border border-line bg-surface">
      <div className="flex items-center justify-between border-b border-line px-4 py-3">
        <h2 className="text-base font-semibold">{w.mapTitle}</h2>
        <p className="flex gap-3 text-xs text-muted">
          <span>● {w.mapRead}</span>
          <span>○ {w.mapUnread}</span>
        </p>
      </div>
      <div className="overflow-x-auto bg-background p-4 md:p-6">
        <div className="grid min-w-140 grid-cols-[1fr_2rem_1fr_2rem_1fr] items-center gap-y-1">
          {slots.map((s, i) => {
            const info = types.get(s.id);
            const items = numbered.filter((n) => n.el.type === s.id);
            const next = slots[i + 1];
            const isSelected = selected === s.id;
            return (
              <Fragment key={s.id}>
                <button
                  type="button"
                  aria-pressed={isSelected}
                  onClick={() => onSelect(s.id)}
                  style={cell(s.row, s.col)}
                  className={`min-h-20 rounded-card px-3 py-2.5 text-left focus-visible:outline-2 focus-visible:outline-brand ${
                    isSelected
                      ? "border-2 border-brand bg-brand-soft"
                      : items.length
                        ? "border border-foreground/40 bg-surface"
                        : "border border-dashed border-line bg-surface-muted"
                  }`}
                >
                  <span className="block text-sm font-semibold">{info?.short ?? s.id}</span>
                  <span className={`mt-1 block text-xs ${items.length ? "text-brand-strong" : "text-muted"}`}>
                    {items.length ? `● ${items.map((n) => n.code).join(" · ")}` : `○ ${w.mapUnread}`}
                  </span>
                </button>
                {next ? <Connector from={s} to={next} /> : null}
              </Fragment>
            );
          })}
        </div>
      </div>
      {gaps.length ? (
        <div className="flex flex-wrap gap-2 border-t border-line px-4 py-3">
          {gaps.map((g) => (
            <Badge key={`${g.from_type}-${g.to_type}`} tone="warning" icon={<CircleAlert className="size-3" />}>
              {w.graphGap(types.get(g.from_type)?.label ?? g.from_type, types.get(g.to_type)?.label ?? g.to_type)}
            </Badge>
          ))}
        </div>
      ) : null}
    </div>
  );
}

function Connector({ from, to }: { from: { row: number; col: number }; to: { row: number; col: number } }) {
  const icon = "mx-auto size-4 text-muted";
  if (from.row !== to.row) {
    return (
      <ArrowDown aria-hidden="true" className={icon} style={{ gridRow: from.row * 2 + 2, gridColumn: from.col * 2 + 1 }} />
    );
  }
  const Icon = to.col > from.col ? ArrowRight : ArrowLeft;
  return (
    <Icon
      aria-hidden="true"
      className={icon}
      style={{ gridRow: from.row * 2 + 1, gridColumn: Math.min(from.col, to.col) * 2 + 2 }}
    />
  );
}

interface TypePanelProps {
  info: TypeInfo | undefined;
  items: Numbered[];
  where: string;
}

/** Daftar elemen dari tipe yang dipilih di peta. */
export function TypePanel({ info, items, where }: TypePanelProps) {
  const w = copy.workspace;
  return (
    <aside className="rounded-card border border-line bg-surface" aria-live="polite">
      <div className="border-b border-line px-4 py-3">
        <h2 className="text-base font-semibold">{info?.label}</h2>
        <p className="text-xs text-muted">{w.panelCount(items.length)}</p>
      </div>
      {items.length ? (
        <ol className="divide-y divide-line">
          {items.map(({ el, code }) => {
            const { title, body } = splitTitle(el.content);
            return (
              <li key={el.id} className="flex gap-3 px-4 py-3">
                <span className="w-7 shrink-0 text-sm font-semibold text-brand-strong">{code}</span>
                <div className="min-w-0">
                  <p className="line-clamp-2 text-sm font-medium">{title ?? body}</p>
                  <p className={`mt-0.5 text-xs ${el.verified ? "text-muted" : "text-tone-warning-fg"}`}>
                    {where} {el.page} · {el.verified ? w.verified.toLowerCase() : w.notVerified.toLowerCase()}
                  </p>
                </div>
              </li>
            );
          })}
        </ol>
      ) : (
        <p className="px-4 py-6 text-sm text-muted">{w.panelEmpty}</p>
      )}
    </aside>
  );
}

/** Kartu satu elemen: kode, tipe, lokasi, isi, dan kutipan asli yang bisa dibuka. */
export function ElementCard({ item, info, where }: { item: Numbered; info: TypeInfo | undefined; where: string }) {
  const w = copy.workspace;
  const { el, code } = item;
  const { title, body } = splitTitle(el.content);
  const source = el.source === "ai" ? w.fromAi : el.source === "auto" ? w.fromAuto : w.fromStudent;
  return (
    <article className="flex flex-col rounded-card border border-line bg-surface">
      <header className="flex items-center justify-between gap-2 border-b border-line px-4 py-2.5 text-xs">
        <span className="font-semibold text-brand-strong">
          {code} <span className="font-normal text-muted">· {info?.short ?? el.type}</span>
        </span>
        <span className="text-muted">
          {where} {el.page}
        </span>
      </header>
      <div className="flex-1 px-4 py-3">
        {title ? <h3 className="text-base font-semibold leading-snug">{title}</h3> : null}
        <p className={`line-clamp-4 text-sm ${title ? "mt-1 text-muted" : ""}`}>{body}</p>
      </div>
      <details className="border-t border-line px-4 py-2.5 text-sm">
        <summary className="cursor-pointer font-medium">{w.showQuote}</summary>
        <p className="mt-2 border-l-2 border-line pl-2 text-xs italic">“{el.quote}”</p>
        <p className={`mt-2 text-xs ${el.verified ? "text-tone-success-fg" : "text-tone-warning-fg"}`}>
          {el.verified ? w.verified : w.notVerified} · {source}
        </p>
      </details>
    </article>
  );
}
