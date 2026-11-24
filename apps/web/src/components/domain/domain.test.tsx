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

  it("tanpa evidence: status dipaksa 'perlu konfirmasi' dan sumber dinyatakan kosong", () => {
    render(<FindingCard finding={{ ...finding, evidence: [] }} />);
    expect(screen.getByText(copy.status.needs_user_confirmation)).toBeInTheDocument();
    expect(screen.queryByText(copy.status.ai_suggested)).not.toBeInTheDocument();
    expect(screen.getByText(copy.noEvidence)).toBeInTheDocument();
  });
});
