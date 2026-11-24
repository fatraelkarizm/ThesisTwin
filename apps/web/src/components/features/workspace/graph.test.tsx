import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import type { ElementOut, GraphOut } from "@/lib/api";
import { copy } from "@/lib/copy";
import { GraphView } from "./GraphView";

const el = (id: string, type: ElementOut["type"], content: string): ElementOut => ({
  id,
  type,
  content,
  quote: `kutipan ${id}`,
  page: 2,
  verified: true,
  source: "student",
  status: "student_confirmed",
});

const graph: GraphOut = {
  nodes: [el("rq", "research_question", "Apa hubungan X dan Y?"), el("o", "objective", "Mendeskripsikan X")],
  edges: [{ src: "rq", dst: "o", type: "addresses" }],
  gaps: [{ from_type: "objective", to_type: "analysis", relation: "analyzed_with" }],
};

describe("GraphView", () => {
  it("setiap elemen adalah tombol yang bisa difokus, celah ditampilkan", () => {
    render(<GraphView graph={graph} unit="section" />);
    expect(screen.getAllByRole("button")).toHaveLength(2);
    expect(screen.getByText(copy.workspace.graphGap("Tujuan", "Analisis"))).toBeInTheDocument();
  });

  it("klik elemen menampilkan kutipan dan lokasinya (bagian untuk DOCX)", async () => {
    render(<GraphView graph={graph} unit="section" />);
    await userEvent.click(screen.getByRole("button", { name: /Apa hubungan X dan Y/ }));
    expect(screen.getByText(/kutipan rq/)).toBeInTheDocument();
    expect(screen.getByText(/Rumusan masalah · Bagian 2/)).toBeInTheDocument();
    expect(screen.getByText(/menjawab Tujuan/)).toBeInTheDocument();
  });

  it("tanpa elemen: pesan kosong, bukan graph", () => {
    render(<GraphView graph={{ nodes: [], edges: [], gaps: [] }} unit="page" />);
    expect(screen.getByText(copy.workspace.graphEmpty)).toBeInTheDocument();
  });
});
