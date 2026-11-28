"use client";

import { CircleAlert, Printer } from "lucide-react";
import { useEffect, useState } from "react";
import { BriefDocument } from "@/components/domain/BriefDocument";
import { Button } from "@/components/ui/Button";
import { api, ApiError, type BriefFindingOut, type BriefOut, type StressQuestionOut } from "@/lib/api";
import { copy } from "@/lib/copy";

export function SupervisorBrief({ token }: { token: string }) {
  const s = copy.supervisor;
  const [brief, setBrief] = useState<BriefOut | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [decided, setDecided] = useState<Record<string, BriefFindingOut["status"]>>({});
  const [stress, setStress] = useState<StressQuestionOut[]>([]);

  useEffect(() => {
    Promise.all([api.sharedBrief(token), api.sharedStress(token)]).then(
      ([b, q]) => {
        setBrief(b);
        setStress(q);
      },
      (e: unknown) => setError(e instanceof ApiError && e.status === 404 ? s.invalid : String(e)),
    );
  }, [token, s.invalid]);

  async function rate(questionId: string, score: number) {
    try {
      const updated = await api.rate(token, questionId, score);
      setStress((prev) => prev.map((q) => (q.id === questionId ? updated : q)));
    } catch (e) {
      setError(e instanceof ApiError ? e.message : String(e));
    }
  }

  async function decide(f: BriefFindingOut, confirm: boolean) {
    try {
      const updated = await api.decide(token, f.id, confirm);
      setDecided((prev) => ({ ...prev, [f.id]: updated.status }));
    } catch (e) {
      setError(e instanceof ApiError ? e.message : String(e));
    }
  }

  return (
    <main className="mx-auto w-full max-w-3xl space-y-6 p-4 md:p-8">
      <h1 className="sr-only">{s.title}</h1>
      {error ? (
        <p role="alert" className="flex items-start gap-2 rounded-lg bg-tone-danger-bg p-3 text-sm text-tone-danger-fg">
          <CircleAlert aria-hidden="true" className="mt-0.5 size-4 shrink-0" />
          {error}
        </p>
      ) : null}
      {!brief && !error ? <p className="text-sm text-muted">{copy.workspace.loading}</p> : null}
      {brief ? (
        <BriefDocument
          brief={brief}
          stress={stress}
          decided={decided}
          onDecide={decide}
          onRate={rate}
          actions={
            <Button variant="secondary" className="print:hidden" onClick={() => window.print()}>
              <Printer aria-hidden="true" className="size-4" />
              {s.print}
            </Button>
          }
        />
      ) : null}
    </main>
  );
}
