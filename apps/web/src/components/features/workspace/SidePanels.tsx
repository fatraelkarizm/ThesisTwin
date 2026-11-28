"use client";

import { Check, Copy, Link2, MessageSquareText } from "lucide-react";
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

interface SharePanelProps {
  text: string;
  links: number; // tautan yang pernah dibuat untuk proyek ini
  onShare: () => Promise<string>;
}

/** Dua cara mengirim brief: tautan tanpa akun (utama) atau teks untuk chat. */
export function SharePanel({ text, links, onShare }: SharePanelProps) {
  const w = copy.workspace;
  const [copied, setCopied] = useState<"text" | "link" | null>(null);
  const [link, setLink] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function copyValue(value: string, what: "text" | "link") {
    await navigator.clipboard.writeText(value);
    setCopied(what);
    setTimeout(() => setCopied(null), 1500);
  }

  async function share() {
    setBusy(true);
    try {
      setLink(await onShare());
    } finally {
      setBusy(false);
    }
  }

  return (
    <aside className="space-y-4 rounded-card border border-line bg-surface p-5 shadow-card">
      <div>
        <h2 className="text-base font-semibold">{w.sendTitle}</h2>
        <p className="mt-1 text-sm text-muted">{w.sendBody}</p>
      </div>
      {link ? (
        <div className="space-y-2 rounded-lg border border-brand bg-brand-soft p-3">
          <p className="break-all font-mono text-xs text-brand-strong">{link}</p>
          <Button className="w-full" onClick={() => copyValue(link, "link")}>
            {copied === "link" ? <Check aria-hidden="true" className="size-4" /> : <Copy aria-hidden="true" className="size-4" />}
            {copied === "link" ? w.copied : w.copyLink}
          </Button>
          <p className="text-xs text-muted">{w.shareNote}</p>
        </div>
      ) : (
        <Button className="w-full" onClick={share} disabled={busy}>
          <Link2 aria-hidden="true" className="size-4" />
          {w.shareLink}
        </Button>
      )}
      <Button variant="secondary" className="w-full" onClick={() => copyValue(text, "text")} disabled={!text}>
        {copied === "text" ? <Check aria-hidden="true" className="size-4" /> : <MessageSquareText aria-hidden="true" className="size-4" />}
        {copied === "text" ? w.copied : w.copy}
      </Button>
      <p className="border-t border-line pt-3 text-xs text-muted">{w.linksMade(links)}</p>
    </aside>
  );
}
