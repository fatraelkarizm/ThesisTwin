import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { copy } from "@/lib/copy";
import type { Finding } from "@/types/domain";
import { FindingGroup, groupFindings } from "./FindingGroup";

const base: Finding = {
  id: "F",
  ruleId: "R-SECTIONS-UMUM",
  priority: "medium",
  title: "Bagian wajib belum ditemukan",
  whyFlagged: "Panduan meminta bagian ini.",
  suggestedClarification: "Apakah bagian ini ada dengan judul lain?",
  evidence: [],
  confidence: 1,
  status: "needs_user_confirmation",
  aiGenerated: false,
  directions: [
    { option: "Bagian ada dengan judul lain", implication: "Judulnya bisa disamakan dengan panduan." },
    { option: "Bagian belum ditulis", implication: "Perlu dibahas dengan pembimbing." },
  ],
};

const sections = ["Batasan Masalah", "Manfaat Penelitian", "Hipotesis"].map((s, i) => ({
  ...base,
  id: `S${i}`,
  title: `${base.title}: ${s}`,
  whyFlagged: `${base.whyFlagged} (${s})`,
}));

describe("groupFindings", () => {
  it("satu aturan = satu kelompok, prioritas tinggi lebih dulu", () => {
    const causal = { ...base, id: "C", ruleId: "R-CAUSAL-01", priority: "high" as const, title: "Kausal" };
    const groups = groupFindings([...sections, causal]);
    expect(groups.map((g) => [g.ruleId, g.findings.length])).toEqual([
      ["R-CAUSAL-01", 1],
      ["R-SECTIONS-UMUM", 3],
    ]);
  });
});

describe("FindingGroup", () => {
  it("judul, alasan, dan arah tampil sekali; tiap rincian tetap punya status, sumber, dan aksi sendiri", async () => {
    const onConfirm = vi.fn();
    render(<FindingGroup group={{ ruleId: base.ruleId, findings: sections }} onConfirm={onConfirm} onReject={vi.fn()} />);
    expect(screen.getAllByRole("heading", { name: base.title })).toHaveLength(1);
    expect(screen.getByText(base.whyFlagged)).toBeInTheDocument();
    expect(screen.getAllByText("Bagian ada dengan judul lain")).toHaveLength(1);
    expect(screen.getAllByText(copy.noEvidence)).toHaveLength(3);
    expect(screen.getAllByText(copy.status.needs_user_confirmation)).toHaveLength(3);
    await userEvent.click(screen.getByRole("button", { name: `${copy.confirm}: Hipotesis` }));
    expect(onConfirm).toHaveBeenCalledWith("S2");
  });

  it("rincian yang sudah ditinjau tidak menampilkan tombol aksi", () => {
    const done = sections.map((f, i) => (i === 0 ? { ...f, status: "rejected" as const } : f));
    render(<FindingGroup group={{ ruleId: base.ruleId, findings: done }} onConfirm={vi.fn()} onReject={vi.fn()} />);
    expect(screen.queryByRole("button", { name: `${copy.confirm}: Batasan Masalah` })).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: `${copy.confirm}: Hipotesis` })).toBeInTheDocument();
  });
});
