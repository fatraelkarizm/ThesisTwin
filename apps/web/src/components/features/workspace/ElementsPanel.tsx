"use client";

import { CheckCircle2, CircleAlert, Plus } from "lucide-react";
import { useId, useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import type { ElementOut, ElementType } from "@/lib/api";
import { copy } from "@/lib/copy";

// Urutan rantai dependency proposal (Bab 1 -> Bab 3).
const ORDER: ElementType[] = [
  "research_question",
  "objective",
  "variable",
  "population",
  "method",
  "instrument",
  "analysis",
  "claim",
  "limitation",
];

export function ElementList({ elements, unit }: { elements: ElementOut[]; unit: "page" | "section" }) {
  const w = copy.workspace;
  if (elements.length === 0) return <p className="text-sm text-muted">{w.noElements}</p>;
  const where = unit === "section" ? w.form.section : w.form.page;
  const groups = ORDER.map((t) => [t, elements.filter((e) => e.type === t)] as const).filter(([, l]) => l.length);

  return (
    <div className="space-y-6">
      {groups.map(([type, list]) => (
        <section key={type} aria-labelledby={`el-${type}`}>
          <h3 id={`el-${type}`} className="mb-2 flex items-center gap-2 text-sm font-semibold">
            {copy.elementTypes[type]}
            <span className="rounded-full bg-surface-muted px-2 py-0.5 text-xs font-medium text-muted">{list.length}</span>
          </h3>
          <ol className="divide-y divide-line rounded-card border border-line bg-surface">
            {list.map((el, i) => (
              <li key={el.id} className="flex gap-3 px-4 py-3">
                <span className="w-5 shrink-0 pt-0.5 text-right text-xs font-semibold tabular-nums text-muted">
                  {i + 1}.
                </span>
                <div className="min-w-0 flex-1">
                  <p className="text-sm">{el.content}</p>
                  <div className="mt-1.5 flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-muted">
                    <span>
                      {where} {el.page}
                    </span>
                    <span className={`inline-flex items-center gap-1 ${el.verified ? "text-tone-success-fg" : "text-tone-warning-fg"}`}>
                      {el.verified ? (
                        <CheckCircle2 aria-hidden="true" className="size-3.5" />
                      ) : (
                        <CircleAlert aria-hidden="true" className="size-3.5" />
                      )}
                      {el.verified ? w.verified : w.notVerified}
                    </span>
                    <span>{el.source === "ai" ? w.fromAi : el.source === "auto" ? w.fromAuto : w.fromStudent}</span>
                    <details className="w-full">
                      <summary className="cursor-pointer text-brand-strong">{w.showQuote}</summary>
                      <p className="mt-1 border-l-2 border-line pl-2 italic">“{el.quote}”</p>
                    </details>
                  </div>
                </div>
              </li>
            ))}
          </ol>
        </section>
      ))}
    </div>
  );
}

interface AddElementFormProps {
  unit: "page" | "section";
  onAdd: (body: { type: ElementType; content: string; quote: string; page: number }) => Promise<void>;
}

const field = "mt-1 w-full rounded-lg border border-line bg-surface px-3 py-2 text-sm";

export function AddElementForm({ unit, onAdd }: AddElementFormProps) {
  const w = copy.workspace;
  const ids = { type: useId(), content: useId(), quote: useId(), page: useId() };
  const [type, setType] = useState<ElementType>("research_question");
  const [content, setContent] = useState("");
  const [quote, setQuote] = useState("");
  const [page, setPage] = useState(1);
  const [busy, setBusy] = useState(false);
  const where = unit === "section" ? w.form.section : w.form.page;

  async function submit(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    try {
      await onAdd({ type, content: content.trim(), quote: quote.trim(), page });
      setContent("");
      setQuote("");
    } finally {
      setBusy(false);
    }
  }

  return (
    <details className="rounded-card border border-dashed border-line bg-surface">
      <summary className="flex min-h-11 cursor-pointer items-center gap-2 px-4 text-sm font-medium">
        <Plus aria-hidden="true" className="size-4" />
        {w.addManual}
      </summary>
      <form onSubmit={submit} className="space-y-3 px-4 pb-4">
        <p className="text-xs text-muted">{w.addManualHint}</p>
        <div className="grid gap-3 sm:grid-cols-[1fr_120px]">
          <label htmlFor={ids.type} className="text-sm font-medium">
            {w.form.type}
            <select id={ids.type} name="type" value={type} onChange={(e) => setType(e.target.value as ElementType)} className={field}>
              {Object.entries(copy.elementTypes).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>
          <label htmlFor={ids.page} className="text-sm font-medium">
            {where}
            <input id={ids.page} name="page" type="number" min={1} value={page} onChange={(e) => setPage(Math.max(1, Number(e.target.value)))} className={field} />
          </label>
        </div>
        <label htmlFor={ids.content} className="block text-sm font-medium">
          {w.form.content}
          <textarea id={ids.content} name="content" required rows={2} value={content} onChange={(e) => setContent(e.target.value)} className={field} />
        </label>
        <label htmlFor={ids.quote} className="block text-sm font-medium">
          {w.form.quote}
          <textarea id={ids.quote} name="quote" required rows={2} value={quote} onChange={(e) => setQuote(e.target.value)} className={field} />
        </label>
        <Button type="submit" disabled={busy || !content.trim() || !quote.trim()}>
          {w.form.add}
        </Button>
      </form>
    </details>
  );
}
