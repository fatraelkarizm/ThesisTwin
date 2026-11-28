import { Badge } from "@/components/ui/Badge";
import { copy } from "@/lib/copy";

// Wajib di setiap tampilan yang memakai data simulasi (AGENTS.md §3).
export function SimulatedBadge() {
  return (
    <Badge tone="warning" icon="◇">
      {copy.simulated}
    </Badge>
  );
}
