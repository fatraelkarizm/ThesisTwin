import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { useState } from "react";
import { describe, expect, it } from "vitest";
import type { ElementOut, ElementType, OntologyOut } from "@/lib/api";
import { copy } from "@/lib/copy";
import { numberElements, ResearchMap, splitTitle, TypePanel } from "./ResearchMap";

const ontology: OntologyOut = {
  element_types: [
    { id: "research_question", label: "Rumusan masalah", short: "Rumusan masalah", code: "R", layer: 0 },
    { id: "objective", label: "Tujuan", short: "Tujuan", code: "T", layer: 1 },
    { id: "method", label: "Metode/desain", short: "Desain", code: "D", layer: 3 },
    { id: "analysis", label: "Analisis", short: "Analisis", code: "A", layer: 4 },
  ],
  relations: [],
  map: ["research_question", "objective", "method", "analysis"],
};

const el = (id: string, type: ElementType, content: string, page: number): ElementOut => ({
  id,
  type,
  content,
  quote: `kutipan ${id}`,
  page,
  verified: true,
  source: "auto",
  status: "ai_suggested",
});

const elements = [
  el("r2", "research_question", "Struktur Grup Gerak: Bagaimana orbit keping?", 6),
  el("r1", "research_question", "Representasi Geometris: Bagaimana modelnya?", 5),
  el("a1", "analysis", "Data yang dianalisis berupa struktur aljabar.", 14),
];

function Harness() {
  const [selected, setSelected] = useState<ElementType>("research_question");
  const numbered = numberElements(elements, ontology);
  return (
    <>
      <ResearchMap ontology={ontology} numbered={numbered} gaps={[]} selected={selected} onSelect={setSelected} />
      <TypePanel
        info={ontology.element_types.find((t) => t.id === selected)}
        items={numbered.filter((n) => n.el.type === selected)}
        where="Hal."
      />
    </>
  );
}

describe("ResearchMap", () => {
  it("menomori elemen per tipe menurut urutan halaman, kode dari ontologi", () => {
    const codes = numberElements(elements, ontology).map((n) => `${n.code}:${n.el.id}`);
    expect(codes).toEqual(["R1:r1", "R2:r2", "A1:a1"]);
  });

  it("judul hanya diambil dari label yang ditulis mahasiswa sebelum titik dua", () => {
    expect(splitTitle("Struktur Grup Gerak: Bagaimana orbit?")).toEqual({
      title: "Struktur Grup Gerak",
      body: "Bagaimana orbit?",
    });
    expect(splitTitle("Bagaimana rasio: a dan b?").title).toBeNull();
    expect(splitTitle("Data berupa struktur aljabar.").title).toBeNull();
  });

  it("kotak tanpa elemen ditandai belum terbaca; klik kotak mengganti isi panel", async () => {
    render(<Harness />);
    expect(screen.getByRole("button", { name: /Rumusan masalah.*R1 · R2/ })).toHaveAttribute("aria-pressed", "true");
    expect(screen.getByRole("button", { name: new RegExp(`Tujuan.*${copy.workspace.mapUnread}`) })).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: /Tujuan/ }));
    expect(screen.getByText(copy.workspace.panelEmpty)).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: /Analisis/ }));
    expect(screen.getByText(copy.workspace.panelCount(1))).toBeInTheDocument();
    expect(screen.getByText("A1")).toBeInTheDocument();
  });
});
