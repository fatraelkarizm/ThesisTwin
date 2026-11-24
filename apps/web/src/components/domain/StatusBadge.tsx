import { Badge, type BadgeTone } from "@/components/ui/Badge";
import { copy } from "@/lib/copy";
import type { Status } from "@/types/domain";

// Satu-satunya pemetaan status -> tampilan. Jangan buat badge status di tempat lain.
const map: Record<Status, { tone: BadgeTone; icon: string }> = {
  ai_suggested: { tone: "info", icon: "✦" },
  needs_user_confirmation: { tone: "warning", icon: "?" },
  student_confirmed: { tone: "success", icon: "✓" },
  supervisor_confirmed: { tone: "success", icon: "✓✓" },
  rejected: { tone: "neutral", icon: "✕" },
  resolved: { tone: "neutral", icon: "●" },
};

export function StatusBadge({ status }: { status: Status }) {
  const { tone, icon } = map[status];
  return (
    <Badge tone={tone} icon={icon}>
      {copy.status[status]}
    </Badge>
  );
}
