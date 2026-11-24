"use client";

import { Check, CircleDashed, X } from "lucide-react";
import { useState } from "react";
import { AiLabel } from "@/components/domain/AiLabel";
import { EvidenceChip } from "@/components/domain/EvidenceChip";
import { PriorityTag } from "@/components/domain/PriorityTag";
import { StatusBadge } from "@/components/domain/StatusBadge";
import { Button } from "@/components/ui/Button";
import { Section } from "@/components/ui/Section";
import { copy } from "@/lib/copy";
import type { Finding, Status } from "@/types/domain";

// Cermin sisi-klien dari state machine API (apps/api/app/domain/status.py) untuk demo.
// Saat data nyata tersambung, transisi dikirim ke API dan hasilnya dipakai di sini.
const studentNext: Partial<Record<Status, { confirm: Status; reject: Status }>> = {
  ai_suggested: { confirm: "student_confirmed", reject: "rejected" },
  needs_user_confirmation: { confirm: "student_confirmed", reject: "rejected" },
};

interface FindingQueueProps {
  initial: Finding[];
  // Data nyata: transisi dikirim ke API. Tanpa ini (demo) transisi hanya lokal.
  onDecide?: (id: string, target: "student_confirmed" | "rejected") => Promise<Finding>;
}

export function FindingQueue({ initial, onDecide }: FindingQueueProps) {
  const [items, setItems] = useState(initial);
  const q = copy.dashboard.queue;

  const move = async (id: string, to: "confirm" | "reject") => {
    if (onDecide) {
      const updated = await onDecide(id, to === "confirm" ? "student_confirmed" : "rejected");
      setItems((prev) => prev.map((f) => (f.id === id ? updated : f)));
      return;
    }
    setItems((prev) =>
      prev.map((f) => {
        const next = studentNext[f.status];
        return f.id === id && next ? { ...f, status: next[to] } : f;
      }),
    );
  };

  return (
    <Section id="temuan" title={q.title} description={q.description}>
      {items.length === 0 ? (
        <p className="text-sm text-muted">{q.empty}</p>
      ) : (
        <ul className="space-y-3">
          {items.map((f) => {
            const open = Boolean(studentNext[f.status]);
            return (
              <li key={f.id} className="flex gap-3 rounded-card border border-line bg-surface p-4 shadow-card">
                <span
                  aria-hidden="true"
                  className={`mt-0.5 flex size-5 shrink-0 items-center justify-center rounded-full ${
                    f.status === "student_confirmed"
                      ? "bg-brand text-brand-fg"
                      : f.status === "rejected"
                        ? "bg-surface-muted text-muted"
                        : "text-muted"
                  }`}
                >
                  {f.status === "student_confirmed" ? (
                    <Check className="size-3.5" />
                  ) : f.status === "rejected" ? (
                    <X className="size-3.5" />
                  ) : (
                    <CircleDashed className="size-5" />
                  )}
                </span>
                <div className="min-w-0 flex-1 space-y-2">
                  <div className="flex flex-wrap items-start justify-between gap-2">
                    <h3 className="text-sm font-semibold">{f.title}</h3>
                    <span className="flex flex-wrap items-center gap-1.5">
                      <PriorityTag priority={f.priority} />
                      <StatusBadge status={f.status} />
                    </span>
                  </div>
                  <p className="text-xs text-muted">{f.whyFlagged}</p>
                  <p className="text-sm">
                    <span className="font-medium">{copy.suggestion}: </span>
                    {f.suggestedClarification}
                  </p>
                  <div className="flex flex-wrap items-center gap-2">
                    {f.evidence.length > 0 ? (
                      f.evidence.map((e) => <EvidenceChip key={`${e.element}-${e.page}`} evidence={e} />)
                    ) : (
                      <span className="text-xs text-muted">{copy.noEvidence}</span>
                    )}
                  </div>
                  <div className="flex flex-wrap items-center gap-2 pt-1">
                    {f.aiGenerated ? <AiLabel /> : null}
                    <span className="text-xs text-muted">{f.ruleId}</span>
                    {open ? (
                      <span className="ml-auto flex gap-2">
                        <Button variant="secondary" onClick={() => move(f.id, "reject")}>
                          {copy.reject}
                        </Button>
                        <Button onClick={() => move(f.id, "confirm")}>{copy.confirm}</Button>
                      </span>
                    ) : null}
                  </div>
                </div>
              </li>
            );
          })}
        </ul>
      )}
    </Section>
  );
}
