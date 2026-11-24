import { Badge, type BadgeTone } from "@/components/ui/Badge";
import { copy } from "@/lib/copy";
import type { Priority } from "@/types/domain";

const tone: Record<Priority, BadgeTone> = { high: "danger", medium: "warning", low: "neutral" };
const icon: Record<Priority, string> = { high: "▲", medium: "■", low: "▼" };

export function PriorityTag({ priority }: { priority: Priority }) {
  return (
    <Badge tone={tone[priority]} icon={icon[priority]}>
      {copy.priority[priority]}
    </Badge>
  );
}
