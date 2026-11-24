"use client";

import { useState } from "react";
import { AiLabel } from "@/components/domain/AiLabel";
import { EvidenceChip } from "@/components/domain/EvidenceChip";
import { PriorityTag } from "@/components/domain/PriorityTag";
import { StatusBadge } from "@/components/domain/StatusBadge";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { copy } from "@/lib/copy";
import type { Finding, Status } from "@/types/domain";

// Cermin sisi-klien dari state machine API (apps/api/app/domain/status.py) untuk demo.
// Saat data nyata tersambung, transisi dikirim ke API dan hasilnya dipakai di sini.
const studentNext: Partial<Record<Status, { confirm: Status; reject: Status }>> = {
  ai_suggested: { confirm: "student_confirmed", reject: "rejected" },
  needs_user_confirmation: { confirm: "student_confirmed", reject: "rejected" },
};

export function FindingQueue({ initial }: { initial: Finding[] }) {
  const [items, setItems] = useState(initial);
  const q = copy.dashboard.queue;

  const move = (id: string, to: "confirm" | "reject") =>
    setItems((prev) =>
      prev.map((f) => {
        const next = studentNext[f.status];
        return f.id === id && next ? { ...f, status: next[to] } : f;
      }),
    );

  return (
    <Card title={q.title} description={q.description}>
      {items.length === 0 ? (
        <p className="text-sm text-muted">{q.empty}</p>
      ) : (
        <ul className="divide-y divide-line">
          {items.map((f) => {
            const open = Boolean(studentNext[f.status]);
            return (
              <li key={f.id} className="space-y-2 py-4 first:pt-0 last:pb-0">
                <div className="flex flex-wrap items-center gap-2">
                  <PriorityTag priority={f.priority} />
                  <StatusBadge status={f.status} />
                  <AiLabel />
                  <span className="text-xs text-muted">{f.ruleId}</span>
                </div>
                <h3 className="text-sm font-semibold">{f.title}</h3>
                <p className="text-sm text-muted">{f.whyFlagged}</p>
                <p className="text-sm">
                  <span className="font-medium">{copy.suggestion}: </span>
                  {f.suggestedClarification}
                </p>
                <div className="flex flex-wrap gap-2">
                  {f.evidence.length > 0 ? (
                    f.evidence.map((e) => <EvidenceChip key={`${e.element}-${e.page}`} evidence={e} />)
                  ) : (
                    <span className="text-xs text-muted">{copy.noEvidence}</span>
                  )}
                </div>
                {open ? (
                  <div className="flex gap-2 pt-1">
                    <Button onClick={() => move(f.id, "confirm")}>{copy.confirm}</Button>
                    <Button variant="secondary" onClick={() => move(f.id, "reject")}>
                      {copy.reject}
                    </Button>
                  </div>
                ) : null}
              </li>
            );
          })}
        </ul>
      )}
    </Card>
  );
}
