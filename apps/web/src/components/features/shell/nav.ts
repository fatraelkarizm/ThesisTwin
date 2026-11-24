import {
  FileOutput,
  FileText,
  GitCompare,
  LayoutDashboard,
  ListChecks,
  Settings,
  ShieldQuestion,
  type LucideIcon,
} from "lucide-react";
import { copy } from "@/lib/copy";

export interface NavItem {
  label: string;
  icon: LucideIcon;
  // Tanpa href = rute belum dibangun; ditampilkan non-aktif dengan label "Segera".
  href?: string;
}

const n = copy.shell.nav;

export const navItems: NavItem[] = [
  { label: n.dashboard, icon: LayoutDashboard, href: "/" },
  { label: n.proposals, icon: FileText },
  { label: n.findings, icon: ListChecks },
  { label: n.versions, icon: GitCompare },
  { label: n.brief, icon: FileOutput },
  { label: n.stressTest, icon: ShieldQuestion },
  { label: n.settings, icon: Settings },
];
