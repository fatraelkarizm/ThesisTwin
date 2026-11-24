import { Workspace } from "@/components/features/workspace/Workspace";
import { copy } from "@/lib/copy";

export default function ProjectPage() {
  return (
    <main className="flex flex-1 flex-col">
      <header className="border-b border-line bg-surface px-4 pt-6 pb-4 md:px-6">
        <h1 className="text-2xl font-semibold tracking-tight">{copy.workspace.title}</h1>
        <p className="text-sm text-muted">{copy.workspace.subtitle}</p>
      </header>
      <Workspace />
    </main>
  );
}
