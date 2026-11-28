import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { copy } from "@/lib/copy";
import { Dashboard, Home, type Live } from "./Dashboard";
import { journey, type JourneyInput } from "./journey";

const fresh: JourneyInput = {
  elements: 8,
  verified: 8,
  findingsTotal: 5,
  findingsOpen: 5,
  questions: 0,
  answered: 0,
  versions: 1,
  commentsPending: 0,
  linksCreated: 0,
};

describe("journey", () => {
  it("draf baru: langkah berikutnya meninjau temuan, dengan jumlahnya", () => {
    const j = journey(fresh);
    expect(j.next.href).toBe("/temuan");
    expect(j.next.title).toBe(copy.home.journey.next.findings(5).title);
    expect(j.steps.map((s) => s.state)).toEqual(["done", "next", "todo", "later", "todo"]);
  });

  it("tanpa elemen terbaca: mulai dari isi proposal, cek konsistensi belum dianggap selesai", () => {
    const j = journey({ ...fresh, elements: 0, verified: 0, findingsTotal: 0, findingsOpen: 0 });
    expect(j.next.href).toBe("/proyek");
    expect(j.steps[1].state).not.toBe("done");
  });

  it("satu versi: perbandingan versi dilewati, langsung ke kirim brief", () => {
    const j = journey({ ...fresh, findingsOpen: 0, questions: 3, answered: 3 });
    expect(j.next.href).toBe("/brief");
    expect(j.steps[3].state).toBe("later");
  });

  it("revisi dengan komentar dosen belum ditandai: ke perubahan versi", () => {
    const j = journey({ ...fresh, findingsOpen: 0, questions: 3, answered: 3, versions: 2, commentsPending: 2 });
    expect(j.next.href).toBe("/versi");
  });

  it("semua selesai: arahkan ke unggah revisi", () => {
    const j = journey({ ...fresh, findingsOpen: 0, questions: 3, answered: 3, versions: 2, linksCreated: 1 });
    expect(j.done).toBe(5);
    expect(j.next.href).toBe("/upload");
  });
});

const live: Live = {
  project: { id: "p1", title: "Skripsi PBL", program: "matematika", consent_at: "x" },
  latest: {
    id: "v1",
    version_no: 1,
    filename: "proposal.docx",
    media_type: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    sha256: "a",
    uploaded_at: "2026-11-24T00:00:00Z",
  },
  journey: journey(fresh),
  open: [1, 2, 3, 4].map((n) => ({
    id: `F${n}`,
    ruleId: "R-X",
    priority: "high",
    title: `Temuan ${n}`,
    whyFlagged: "w",
    suggestedClarification: "s?",
    evidence: [{ element: "Rumusan masalah", document: "v1", page: n, unit: "section" }],
    confidence: 1,
    status: "ai_suggested",
    aiGenerated: false,
  })),
};

afterEach(() => {
  window.localStorage.clear();
  vi.unstubAllGlobals();
});

describe("Beranda", () => {
  it("satu kartu langkah berikutnya, hanya 3 temuan teratas, dan tautan ke semua temuan", () => {
    render(<Home live={live} />);
    expect(screen.getByRole("heading", { name: copy.home.journey.next.findings(5).title })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Tinjau temuan/ })).toHaveAttribute("href", "/temuan");
    expect(screen.getByText("Temuan 3")).toBeInTheDocument();
    expect(screen.queryByText("Temuan 4")).not.toBeInTheDocument();
    expect(screen.getByRole("link", { name: copy.home.seeAll(4) })).toHaveAttribute("href", "/temuan");
  });

  it("tanpa proyek: onboarding, bukan data contoh", async () => {
    vi.stubGlobal("fetch", vi.fn());
    render(<Dashboard />);
    expect(await screen.findByRole("heading", { name: copy.home.onboarding.title })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: new RegExp(copy.home.onboarding.cta) })).toHaveAttribute("href", "/upload");
    expect(screen.queryByText(/simulasi/i)).not.toBeInTheDocument();
  });
});
