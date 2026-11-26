import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { copy } from "@/lib/copy";
import { SupervisorBrief } from "./SupervisorBrief";

function respond(body: unknown) {
  return Promise.resolve(new Response(JSON.stringify(body), { status: 200 }));
}

const awaiting = {
  id: "F1",
  rule_id: "R-CAUSAL-01",
  title: "Pertanyaan kausal, desain mungkin belum mendukung inferensi kausal",
  priority: "high",
  status: "student_confirmed",
  why_flagged: "Pertanyaan memakai bahasa sebab-akibat.",
  evidence: [
    { element: "Rumusan masalah", page: 5 },
    { element: "Metode/desain", page: 21 },
  ],
  basis: "Klaim sebab-akibat butuh desain yang mengendalikan penjelasan alternatif.",
  source_types: ["methodology"],
};

const brief = {
  project_title: "Skripsi PBL",
  program: "matematika",
  from_version: null,
  to_version: 1,
  generated_at: "2026-11-26T00:00:00Z",
  unit: "page",
  changes: [],
  comments: [],
  open_findings: [],
  awaiting_supervisor: [awaiting],
  resolved_rules: [],
  impacts: [],
};

afterEach(() => vi.unstubAllGlobals());

describe("SupervisorBrief", () => {
  it("kartu keputusan memuat alasan, bukti halaman, dan landasan", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn((url: string) => respond(url.endsWith("/stress-test") ? [] : brief)),
    );
    render(<SupervisorBrief token="t" />);
    expect(await screen.findByText(awaiting.why_flagged)).toBeInTheDocument();
    expect(screen.getByText("Rumusan masalah")).toBeInTheDocument();
    expect(screen.getByText(/v1, hal\. 21/)).toBeInTheDocument();
    expect(screen.getByText(/mengendalikan penjelasan alternatif/)).toBeInTheDocument();
    expect(screen.getByText(new RegExp(copy.sourceType.methodology))).toBeInTheDocument();
  });
});
