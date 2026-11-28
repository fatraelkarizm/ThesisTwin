import { BookOpenCheck, Upload } from "lucide-react";
import Link from "next/link";
import { buttonClass } from "@/components/ui/Button";
import { copy } from "@/lib/copy";
import { MobileNav } from "./MobileNav";
import { ProjectChip } from "./ProjectChip";

export function Topbar() {
  const s = copy.shell;
  return (
    <header className="sticky top-0 z-10 flex h-16 items-center gap-3 border-b border-line bg-surface/90 px-4 backdrop-blur md:px-6">
      <MobileNav />
      <span className="flex size-8 shrink-0 items-center justify-center rounded-lg bg-brand text-brand-fg md:hidden">
        <BookOpenCheck aria-hidden="true" className="size-4" />
        <span className="sr-only">{s.appName}</span>
      </span>
      <ProjectChip />
      <Link href="/upload" className={buttonClass("primary", "ml-auto shrink-0")}>
        <Upload aria-hidden="true" className="size-4" />
        <span className="hidden sm:inline">{s.upload}</span>
        <span className="sr-only sm:hidden">{s.upload}</span>
      </Link>
    </header>
  );
}
