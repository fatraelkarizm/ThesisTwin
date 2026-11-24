"use client";

import { CheckCircle2, CircleAlert } from "lucide-react";
import { useId, useState, type FormEvent } from "react";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Section } from "@/components/ui/Section";
import type { ElementOut, ElementType } from "@/lib/api";
import { copy } from "@/lib/copy";

interface ElementsPanelProps {
  elements: ElementOut[];
  unit: "page" | "section";
  onAdd: (body: { type: ElementType; content: string; quote: string; page: number }) => Promise<void>;
}

const field = "mt-1 w-full rounded-lg border border-line bg-surface px-3 py-2 text-sm";

export function ElementsPanel({ elements, unit, onAdd }: ElementsPanelProps) {
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
    <Section title={w.elementsTitle} description={w.elementsDescription}>
      {elements.length === 0 ? (
        <p className="mb-4 text-sm text-muted">{w.noElements}</p>
      ) : (
        <ul className="mb-4 space-y-2.5">
          {elements.map((el) => (
            <li key={el.id} className="rounded-card border border-line bg-surface p-3 shadow-card">
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-sm font-semibold">{copy.elementTypes[el.type]}</span>
                <span className="text-xs text-muted">
                  {where} {el.page}
                </span>
                <Badge tone={el.verified ? "success" : "warning"} icon={el.verified ? <CheckCircle2 className="size-3" /> : <CircleAlert className="size-3" />}>
                  {el.verified ? w.verified : w.notVerified}
                </Badge>
                <span className="ml-auto text-xs text-muted">
                  {el.source === "ai" ? w.fromAi : w.fromStudent}
                </span>
              </div>
              <p className="mt-1.5 text-sm">{el.content}</p>
              <p className="mt-1 border-l-2 border-line pl-2 text-xs italic text-muted">“{el.quote}”</p>
            </li>
          ))}
        </ul>
      )}

      <form onSubmit={submit} className="space-y-3 rounded-card border border-dashed border-line bg-surface p-4">
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
    </Section>
  );
}
