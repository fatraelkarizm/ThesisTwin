"use client";

import { RefreshCw, ShieldQuestion } from "lucide-react";
import { useId, useState } from "react";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Section } from "@/components/ui/Section";
import type { StressQuestionOut } from "@/lib/api";
import { copy } from "@/lib/copy";

interface StressPanelProps {
  questions: StressQuestionOut[];
  onGenerate: (regenerate: boolean) => Promise<void>;
  onAnswer: (questionId: string, answer: string) => Promise<void>;
}

export function StressPanel({ questions, onGenerate, onAnswer }: StressPanelProps) {
  const s = copy.stress;
  const [busy, setBusy] = useState(false);

  async function generate() {
    setBusy(true);
    try {
      await onGenerate(questions.length > 0);
    } finally {
      setBusy(false);
    }
  }

  return (
    <Section
      id="stress-test"
      title={s.title}
      description={s.description}
      action={
        questions.length > 0 ? (
          <Button variant="secondary" onClick={generate} disabled={busy}>
            <RefreshCw aria-hidden="true" className="size-4" />
            {s.regenerate}
          </Button>
        ) : undefined
      }
    >
      {questions.length === 0 ? (
        <div className="flex flex-col items-center gap-3 rounded-card border border-dashed border-line px-6 py-10 text-center">
          <ShieldQuestion aria-hidden="true" className="size-8 text-brand-strong" />
          <p className="text-base font-semibold">{s.empty}</p>
          <p className="max-w-md text-sm text-muted">{s.emptyBody}</p>
          <Button onClick={generate} disabled={busy}>
            {s.generate}
          </Button>
        </div>
      ) : (
        <ol className="space-y-3">
          {questions.map((q, i) => (
            <StressItem key={q.id} index={i + 1} question={q} onAnswer={onAnswer} />
          ))}
        </ol>
      )}
    </Section>
  );
}

function StressItem({
  index,
  question,
  onAnswer,
}: {
  index: number;
  question: StressQuestionOut;
  onAnswer: (questionId: string, answer: string) => Promise<void>;
}) {
  const s = copy.stress;
  const id = useId();
  const [draft, setDraft] = useState(question.answer ?? "");
  const [saved, setSaved] = useState(false);
  const dirty = draft.trim() !== (question.answer ?? "");

  async function save() {
    await onAnswer(question.id, draft.trim());
    setSaved(true);
  }

  return (
    <li className="rounded-card border border-line bg-surface p-4 shadow-card">
      <div className="flex flex-wrap items-center gap-2">
        <span className="flex size-6 items-center justify-center rounded-full bg-brand-soft text-xs font-semibold text-brand-strong">
          {index}
        </span>
        <Badge>{s.source}</Badge>
        {question.rating ? (
          <Badge tone="success">
            {s.rating}: {question.rating}/5
          </Badge>
        ) : null}
      </div>
      <p className="mt-2 text-sm font-semibold">{question.text}</p>
      <p className="mt-1 text-xs text-muted">
        {s.why}: {question.reason}
      </p>
      <label htmlFor={id} className="mt-3 block text-sm font-medium">
        {s.answerLabel}
        <textarea
          id={id}
          name={`answer-${question.id}`}
          rows={3}
          value={draft}
          onChange={(e) => {
            setDraft(e.target.value);
            setSaved(false);
          }}
          className="mt-1 w-full rounded-lg border border-line bg-surface px-3 py-2 text-sm"
        />
      </label>
      <div className="mt-2 flex items-center gap-2">
        <Button variant="secondary" onClick={save} disabled={!draft.trim() || !dirty}>
          {s.save}
        </Button>
        {saved && !dirty ? <span className="text-xs text-tone-success-fg">{s.saved}</span> : null}
      </div>
    </li>
  );
}
