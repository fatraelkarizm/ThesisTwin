import { FindingCard } from "@/components/domain/FindingCard";
import { sampleFindings } from "@/components/features/findings/sample";

export default function Home() {
  return (
    <main className="mx-auto w-full max-w-3xl space-y-6 p-6">
      <header>
        <h1 className="text-2xl font-semibold">ThesisTwin</h1>
        <p className="text-sm text-muted">
          Navigasi dan konsistensi skripsi. Data di bawah ini simulasi (bukan hasil analisis nyata).
        </p>
      </header>
      <section aria-labelledby="temuan" className="space-y-4">
        <h2 id="temuan" className="text-lg font-semibold">
          Temuan
        </h2>
        {sampleFindings.map((f) => (
          <FindingCard key={f.id} finding={f} />
        ))}
      </section>
    </main>
  );
}
