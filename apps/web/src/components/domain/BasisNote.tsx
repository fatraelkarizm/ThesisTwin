import { copy } from "@/lib/copy";
import type { SourceType } from "@/types/domain";

export function BasisNote({ basis, sourceTypes = [] }: { basis: string; sourceTypes?: SourceType[] }) {
  const sources = sourceTypes.map((t) => copy.sourceType[t]).join(", ");
  return (
    <p className="border-l-2 border-line pl-2 text-xs text-muted">
      <span className="font-medium">
        {copy.basis}
        {sources ? ` (${sources})` : ""}:{" "}
      </span>
      {basis}
    </p>
  );
}
