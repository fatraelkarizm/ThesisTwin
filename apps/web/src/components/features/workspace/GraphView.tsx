"use client";

import { CircleAlert } from "lucide-react";
import { useState } from "react";
import { Badge } from "@/components/ui/Badge";
import { Section } from "@/components/ui/Section";
import type { ElementType, GraphOut } from "@/lib/api";
import { copy } from "@/lib/copy";

// Kolom tampilan mengikuti rantai dependency (sama dengan LAYER di apps/api/app/domain/graph.py).
const LAYER: Record<ElementType, number> = {
  research_question: 0,
  objective: 1,
  variable: 2,
  population: 2,
  method: 3,
  instrument: 3,
  analysis: 4,
  claim: 5,
  limitation: 5,
};
const W = 176;
const H = 64;
const GAP_X = 56;
const GAP_Y = 20;

export function GraphView({ graph, unit }: { graph: GraphOut; unit: "page" | "section" }) {
  const w = copy.workspace;
  const [selected, setSelected] = useState<string | null>(null);

  if (graph.nodes.length === 0) {
    return (
      <Section title={w.graphTitle} description={w.graphDescription}>
        <p className="text-sm text-muted">{w.graphEmpty}</p>
      </Section>
    );
  }

  const columns = new Map<number, string[]>();
  for (const n of graph.nodes) {
    const col = LAYER[n.type];
    columns.set(col, [...(columns.get(col) ?? []), n.id]);
  }
  const usedCols = [...columns.keys()].sort((a, b) => a - b);
  const pos = new Map<string, { x: number; y: number }>();
  usedCols.forEach((col, ci) =>
    columns.get(col)!.forEach((id, ri) => pos.set(id, { x: ci * (W + GAP_X), y: ri * (H + GAP_Y) })),
  );
  const width = usedCols.length * (W + GAP_X) - GAP_X;
  const height = Math.max(...[...columns.values()].map((c) => c.length)) * (H + GAP_Y) - GAP_Y;
  const node = graph.nodes.find((n) => n.id === selected);
  const where = unit === "section" ? w.form.section : w.form.page;

  return (
    <Section title={w.graphTitle} description={w.graphDescription}>
      <div className="overflow-x-auto rounded-card border border-line bg-background p-4">
        <div className="relative" style={{ width, height }}>
          <svg aria-hidden="true" className="absolute inset-0" width={width} height={height}>
            {graph.edges.map((e) => {
              const a = pos.get(e.src);
              const b = pos.get(e.dst);
              if (!a || !b) return null;
              const x1 = a.x + W;
              const y1 = a.y + H / 2;
              const x2 = b.x;
              const y2 = b.y + H / 2;
              const mid = (x1 + x2) / 2;
              const active = selected === e.src || selected === e.dst;
              return (
                <path
                  key={`${e.src}-${e.dst}`}
                  d={`M${x1},${y1} C${mid},${y1} ${mid},${y2} ${x2},${y2}`}
                  fill="none"
                  className={active ? "stroke-brand" : "stroke-line"}
                  strokeWidth={active ? 2 : 1.5}
                />
              );
            })}
          </svg>
          {graph.nodes.map((n) => {
            const p = pos.get(n.id)!;
            return (
              <button
                key={n.id}
                type="button"
                aria-pressed={selected === n.id}
                onClick={() => setSelected(selected === n.id ? null : n.id)}
                style={{ left: p.x, top: p.y, width: W, height: H }}
                className={`absolute flex flex-col items-start justify-center rounded-lg border bg-surface px-2.5 text-left shadow-card focus-visible:outline-2 focus-visible:outline-brand ${
                  selected === n.id ? "border-brand" : n.verified ? "border-line" : "border-dashed border-tone-warning-fg"
                }`}
              >
                <span className="text-[11px] font-semibold text-brand-strong">{copy.elementTypes[n.type]}</span>
                <span className="line-clamp-2 text-xs">{n.content}</span>
              </button>
            );
          })}
        </div>
      </div>

      {node ? (
        <div className="mt-3 rounded-card border border-brand bg-surface p-3 text-sm shadow-card">
          <p className="font-semibold">
            {copy.elementTypes[node.type]} · {where} {node.page}
          </p>
          <p className="mt-1">{node.content}</p>
          <p className="mt-1 border-l-2 border-line pl-2 text-xs italic text-muted">
            {w.graphQuote}: “{node.quote}”
          </p>
          <p className="mt-2 text-xs text-muted">
            {graph.edges
              .filter((e) => e.src === node.id || e.dst === node.id)
              .map((e) => {
                const other = graph.nodes.find((x) => x.id === (e.src === node.id ? e.dst : e.src));
                const rel = w.relations[e.type as keyof typeof w.relations] ?? e.type;
                return e.src === node.id
                  ? `${rel} ${other ? copy.elementTypes[other.type] : ""}`
                  : `${other ? copy.elementTypes[other.type] : ""} ${rel} ini`;
              })
              .join(" · ")}
          </p>
        </div>
      ) : null}

      <div className="mt-3 flex flex-wrap gap-2">
        {graph.gaps.length === 0 ? (
          <span className="text-xs text-muted">{w.graphNoGaps}</span>
        ) : (
          graph.gaps.map((g) => (
            <Badge key={`${g.from_type}-${g.to_type}`} tone="warning" icon={<CircleAlert className="size-3" />}>
              {w.graphGap(copy.elementTypes[g.from_type], copy.elementTypes[g.to_type])}
            </Badge>
          ))
        )}
      </div>
    </Section>
  );
}
