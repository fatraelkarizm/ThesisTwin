"use client";

import { Plus } from "lucide-react";
import { useId, useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import type { ElementType } from "@/lib/api";
import { copy } from "@/lib/copy";

interface AddElementFormProps {
  unit: "page" | "section";
  types: { id: ElementType; label: string }[];
  onAdd: (body: { type: ElementType; content: string; quote: string; page: number }) => Promise<void>;
}

const field = "mt-1 w-full rounded-lg border border-line bg-surface px-3 py-2 text-sm";

export function AddElementForm({ unit, types, onAdd }: AddElementFormProps) {
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
              {types.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.label}
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
