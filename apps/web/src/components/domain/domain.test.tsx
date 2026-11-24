import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { copy } from "@/lib/copy";
import type { Finding, Status } from "@/types/domain";
import { EvidenceChip } from "./EvidenceChip";
import { FindingCard } from "./FindingCard";
import { StatusBadge } from "./StatusBadge";

const statuses = Object.keys(copy.status) as Status[];

const finding: Finding = {
  id: "F-1",
  ruleId: "R-CAUSAL-01",
  priority: "high",
  title: "Pertanyaan kausal vs desain",
  whyFlagged: "w",
  suggestedClarification: "s",
  evidence: [{ element: "RQ1", document: "proposal_v2", page: 5 }],
  confidence: 0.8,
  status: "ai_suggested",
  aiGenerated: true,
};

describe("StatusBadge", () => {
  it.each(statuses)("menampilkan teks untuk %s (status tidak hanya lewat warna)", (status) => {
    render(<StatusBadge status={status} />);
    expect(screen.getByText(copy.status[status])).toBeInTheDocument();
  });
});

describe("EvidenceChip", () => {
  it("menampilkan elemen, dokumen, dan halaman", () => {
    render(<EvidenceChip evidence={{ element: "RQ1", document: "proposal_v2", page: 5 }} />);
    expect(screen.getByText("RQ1")).toBeInTheDocument();
    expect(screen.getByText(/proposal_v2, hal\. 5/)).toBeInTheDocument();
  });
});

describe("FindingCard", () => {
  it("selalu memberi label AI", () => {
    render(<FindingCard finding={finding} />);
    expect(screen.getByText(copy.aiLabel)).toBeInTheDocument();
  });

  it("temuan aturan tanpa AI tidak diberi label AI dan angkanya bukan 'perkiraan AI'", () => {
    render(<FindingCard finding={{ ...finding, aiGenerated: false }} />);
    expect(screen.queryByText(copy.aiLabel)).not.toBeInTheDocument();
    expect(screen.queryByText(new RegExp(copy.confidence))).not.toBeInTheDocument();
    expect(screen.getByText(new RegExp(copy.evidenceVerified))).toBeInTheDocument();
  });

  it("menampilkan dasar metodologi aturan bila ada", () => {
    render(<FindingCard finding={{ ...finding, basis: "Klaim kausal butuh kelompok pembanding." }} />);
    expect(screen.getByText(/Klaim kausal butuh kelompok pembanding/)).toBeInTheDocument();
  });

  it("tanpa evidence: status dipaksa 'perlu konfirmasi' dan sumber dinyatakan kosong", () => {
    render(<FindingCard finding={{ ...finding, evidence: [] }} />);
    expect(screen.getByText(copy.status.needs_user_confirmation)).toBeInTheDocument();
    expect(screen.queryByText(copy.status.ai_suggested)).not.toBeInTheDocument();
    expect(screen.getByText(copy.noEvidence)).toBeInTheDocument();
  });
});

describe("FindingCard evidence", () => {
  it("elemen setipe di halaman yang sama tidak memicu key ganda", () => {
    const errors: unknown[] = [];
    const orig = console.error;
    console.error = (...args: unknown[]) => errors.push(args);
    render(
      <FindingCard
        finding={{
          ...finding,
          evidence: [
            { element: "Rumusan masalah", document: "v1", page: 6 },
            { element: "Rumusan masalah", document: "v1", page: 6 },
          ],
        }}
      />,
    );
    console.error = orig;
    expect(errors.filter((e) => String(e).includes("same key"))).toHaveLength(0);
  });
});
