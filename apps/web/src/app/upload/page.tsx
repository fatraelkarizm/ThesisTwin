import { UploadForm } from "@/components/features/upload/UploadForm";
import { copy } from "@/lib/copy";

export default function UploadPage() {
  return (
    <main className="mx-auto w-full max-w-7xl space-y-5 p-4 md:p-6">
      <header>
        <h1 className="text-2xl font-semibold">{copy.upload.title}</h1>
        <p className="text-sm text-muted">{copy.upload.subtitle}</p>
      </header>
      <UploadForm />
    </main>
  );
}
