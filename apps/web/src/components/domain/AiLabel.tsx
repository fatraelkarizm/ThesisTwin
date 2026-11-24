import { Badge } from "@/components/ui/Badge";
import { copy } from "@/lib/copy";

export function AiLabel() {
  return (
    <Badge tone="info" icon="✦">
      {copy.aiLabel}
    </Badge>
  );
}
