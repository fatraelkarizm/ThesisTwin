import { Settings } from "@/components/features/settings/Settings";
import { copy } from "@/lib/copy";

export default function SettingsPage() {
  return (
    <main className="flex flex-1 flex-col bg-surface">
      <header className="border-b border-line px-4 pt-6 pb-4 md:px-6">
        <h1 className="text-2xl font-semibold tracking-tight">{copy.settings.title}</h1>
        <p className="text-sm text-muted">{copy.settings.subtitle}</p>
      </header>
      <Settings />
    </main>
  );
}
