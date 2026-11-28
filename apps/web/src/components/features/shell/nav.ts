import {
  FileOutput,
  FileText,
  GitCompare,
  House,
  ListChecks,
  Settings,
  ShieldQuestion,
  type LucideIcon,
} from "lucide-react";
import { copy } from "@/lib/copy";

export interface NavItem {
  label: string;
  icon: LucideIcon;
  href: string;
  step?: number; // nomor langkah alur kerja; sama dengan penunjuk langkah di tiap halaman
}

const stepIcons: Record<string, LucideIcon> = {
  "/proyek": FileText,
  "/temuan": ListChecks,
  "/stress-test": ShieldQuestion,
  "/versi": GitCompare,
  "/brief": FileOutput,
};

// Diturunkan dari copy.steps agar urutan & nama sidebar tidak bisa berbeda dari stepper.
export const homeItem: NavItem = { label: copy.shell.home, icon: House, href: "/" };
export const stepItems: NavItem[] = copy.steps.map((s, i) => ({
  label: s.short,
  icon: stepIcons[s.href],
  href: s.href,
  step: i + 1,
}));
export const settingsItem: NavItem = { label: copy.shell.settings, icon: Settings, href: "/pengaturan" };
