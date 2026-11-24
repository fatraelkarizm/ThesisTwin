"use client";

import { Check, Copy, Link2 } from "lucide-react";
import { useState } from "react";
import { Badge, type BadgeTone } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Section } from "@/components/ui/Section";
import type { CommentStatusOut } from "@/lib/api";
import { copy } from "@/lib/copy";

const stateTone: Record<CommentStatusOut["state"], BadgeTone> = {
  possibly_addressed: "success",
  not_addressed: "warning",
  unknown: "neutral",
};

export function CommentsPanel({
  comments,
  onReview,
}: {
  comments: CommentStatusOut[];
  onReview: (commentId: string, addressed: boolean) => void;
}) {
  const w = copy.workspace;
  return (
    <Section title={w.commentsTitle} description={w.commentsDescription}>
      {comments.length === 0 ? (
        <p className="text-sm text-muted">{w.noComments}</p>
      ) : (
        <ul className="space-y-2.5">
          {comments.map((c) => (
            <li key={c.comment_id} className="rounded-card border border-line bg-surface p-3 shadow-card">
              <p className="text-sm">“{c.text}”</p>
              <p className="mt-0.5 text-xs text-muted">{c.author}</p>
              <div className="mt-2 flex flex-wrap items-center gap-2">
                <Badge tone={stateTone[c.state]}>{w.commentState[c.state]}</Badge>
                <span className="ml-auto flex gap-1.5">
                  {([true, false] as const).map((value) => (
                    <button
                      key={String(value)}
                      type="button"
                      aria-pressed={c.confirmed === value}
                      onClick={() => onReview(c.comment_id, value)}
                      className={`min-h-9 rounded-lg border px-3 text-xs font-medium ${
                        c.confirmed === value ? "border-brand bg-brand-soft text-brand-strong" : "border-line"
                      }`}
                    >
                      {value ? w.addressedYes : w.addressedNo}
                    </button>
                  ))}
                </span>
              </div>
            </li>
          ))}
        </ul>
      )}
    </Section>
  );
}

export function BriefPanel({ text, onShare }: { text: string; onShare: () => Promise<string> }) {
  const w = copy.workspace;
  const [copied, setCopied] = useState(false);
  const [link, setLink] = useState<string | null>(null);

  async function copyText(value: string) {
    await navigator.clipboard.writeText(value);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  }

  return (
    <Section id="brief" title={w.briefTitle} description={w.briefDescription}>
      <pre className="max-h-80 overflow-auto whitespace-pre-wrap rounded-card border border-line bg-surface p-3 font-sans text-xs leading-relaxed shadow-card">
        {text}
      </pre>
      <div className="mt-3 flex flex-wrap gap-2">
        <Button variant="secondary" onClick={() => copyText(text)}>
          {copied ? <Check aria-hidden="true" className="size-4" /> : <Copy aria-hidden="true" className="size-4" />}
          {copied ? w.copied : w.copy}
        </Button>
        <Button onClick={async () => setLink(await onShare())}>
          <Link2 aria-hidden="true" className="size-4" />
          {w.shareLink}
        </Button>
      </div>
      {link ? (
        <div className="mt-3 rounded-card border border-brand bg-brand-soft p-3 text-xs">
          <p className="break-all font-mono text-brand-strong">{link}</p>
          <p className="mt-1.5 text-muted">{w.shareNote}</p>
        </div>
      ) : null}
    </Section>
  );
}
