import { ChevronDown } from "lucide-react";
import { copy } from "@/lib/copy";
import type { Finding } from "@/types/domain";
import { BasisNote } from "./BasisNote";

type Guidance = Pick<Finding, "directions" | "basis" | "sourceTypes" | "references">;

/** Arah, landasan, dan rujukan sebuah temuan, dilipat secara default agar daftar temuan tetap
 *  bisa dipindai. Dipakai kartu temuan tunggal dan kartu kelompok temuan. */
export function FindingGuidance({ finding }: { finding: Guidance }) {
  const directions = finding.directions ?? [];
  const references = finding.references ?? [];
  if (!directions.length && !finding.basis && !references.length) return null;
  return (
    <details className="group rounded-lg border border-line">
      <summary className="flex min-h-11 cursor-pointer list-none items-center gap-2 px-3 text-sm font-medium text-brand-strong [&::-webkit-details-marker]:hidden">
        <ChevronDown aria-hidden="true" className="size-4 transition-transform group-open:rotate-180" />
        {copy.guidanceSummary(directions.length)}
      </summary>
      <div className="space-y-3 border-t border-line p-3">
        {directions.length ? (
          <div>
            <p className="text-sm font-semibold">{copy.directionsTitle}</p>
            <p className="text-xs text-muted">{copy.directionsNote}</p>
            <ul className="mt-2 space-y-2 text-sm">
              {directions.map((d) => (
                <li key={d.option} className="border-l-2 border-brand pl-2">
                  <p className="font-medium">{d.option}</p>
                  <p className="text-muted">
                    <span className="font-medium">{copy.directionImplication}: </span>
                    {d.implication}
                  </p>
                </li>
              ))}
            </ul>
          </div>
        ) : null}
        {finding.basis ? <BasisNote basis={finding.basis} sourceTypes={finding.sourceTypes} /> : null}
        {references.length ? (
          <div className="text-xs">
            <p className="font-medium">{copy.referencesTitle(references.length)}</p>
            <ul className="mt-1.5 space-y-1 pl-4 text-muted">
              {references.map((r) => (
                <li key={r} className="-indent-4 pl-4">
                  {r}
                </li>
              ))}
            </ul>
            <p className="mt-1 italic text-muted">{copy.referencesNote}</p>
          </div>
        ) : null}
      </div>
    </details>
  );
}
