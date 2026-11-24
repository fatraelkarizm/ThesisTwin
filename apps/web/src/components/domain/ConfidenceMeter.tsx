import { copy } from "@/lib/copy";

// AI: perkiraan keyakinan model. Aturan: proporsi evidence yang kutipannya terverifikasi.
export function ConfidenceMeter({ value, aiGenerated = true }: { value: number; aiGenerated?: boolean }) {
  const pct = Math.round(Math.min(1, Math.max(0, value)) * 100);
  return (
    <span className="text-xs text-muted">
      {aiGenerated ? copy.confidence : copy.evidenceVerified}: <strong className="text-foreground">{pct}%</strong>
    </span>
  );
}
