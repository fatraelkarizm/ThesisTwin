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
  { label: n.proposals, icon: FileText, href: "/proyek" },
  { label: n.findings, icon: ListChecks, href: "/temuan" },
  { label: n.versions, icon: GitCompare, href: "/versi" },
  { label: n.brief, icon: FileOutput, href: "/brief" },
  { label: n.stressTest, icon: ShieldQuestion, href: "/stress-test" },
  { label: n.settings, icon: Settings, href: "/pengaturan" },
];
