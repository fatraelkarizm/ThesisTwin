interface SegmentedBarProps {
  value: number;
  total: number;
  label: string;
}

// Bar bersegmen ala referensi: satu segmen per unit, agar jumlah terbaca tanpa persentase palsu.
export function SegmentedBar({ value, total, label }: SegmentedBarProps) {
  return (
    <div role="img" aria-label={label} className="flex gap-1">
      {Array.from({ length: total }, (_, i) => (
        <span key={i} className={`h-2 flex-1 rounded-full ${i < value ? "bg-brand" : "bg-surface-muted"}`} />
      ))}
    </div>
  );
}
