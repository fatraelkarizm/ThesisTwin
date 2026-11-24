import { copy } from "@/lib/copy";

export function ConfidenceMeter({ value }: { value: number }) {
  const pct = Math.round(Math.min(1, Math.max(0, value)) * 100);
  return (
    <span className="text-xs text-muted">
      {copy.confidence}: <strong className="text-foreground">{pct}%</strong>
    </span>
  );
}
