import type { Metadata } from "next";
import { Suspense } from "react";
import { SupervisorBrief } from "@/components/features/supervisor/SupervisorBrief";

// Tautan berisi token rahasia: jangan diindeks dan jangan kirim URL lengkap sebagai referrer.
export const metadata: Metadata = {
  title: "Supervision Brief · ThesisTwin",
  robots: { index: false, follow: false },
  referrer: "no-referrer",
};

// cacheComponents aktif: `params` adalah data request-time, jadi aksesnya harus di dalam <Suspense>
// (node_modules/next/dist/docs/01-app/01-getting-started/08-caching.md, "Prerender validation").
async function WithToken({ params }: { params: PageProps<"/dosen/[token]">["params"] }) {
  const { token } = await params;
  return <SupervisorBrief token={token} />;
}

export default function SupervisorPage(props: PageProps<"/dosen/[token]">) {
  return (
    <Suspense fallback={<p className="p-8 text-sm text-muted">Memuat…</p>}>
      <WithToken params={props.params} />
    </Suspense>
  );
}
