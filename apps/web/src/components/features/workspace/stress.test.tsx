import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import type { StressQuestionOut } from "@/lib/api";
import { copy } from "@/lib/copy";
import { StressPanel } from "./StressPanel";

const q: StressQuestionOut = {
  id: "q1",
  position: 0,
  kind: "finding",
  text: "Mengapa desain ini cukup?",
  reason: "Temuan R-CAUSAL-01 masih terbuka (prioritas high).",
  answer: null,
  rating: null,
};

describe("StressPanel", () => {
  it("menampilkan alasan pemilihan dan label templat (bukan AI)", () => {
    render(<StressPanel questions={[q]} onGenerate={vi.fn()} onAnswer={vi.fn()} />);
    expect(screen.getByText(/R-CAUSAL-01 masih terbuka/)).toBeInTheDocument();
    expect(screen.getByText(copy.stress.source)).toBeInTheDocument();
    expect(screen.queryByText(copy.aiLabel)).not.toBeInTheDocument();
  });

  it("simpan jawaban hanya aktif bila ada perubahan, lalu memanggil onAnswer", async () => {
    const onAnswer = vi.fn().mockResolvedValue(undefined);
    render(<StressPanel questions={[q]} onGenerate={vi.fn()} onAnswer={onAnswer} />);
    const save = screen.getByRole("button", { name: copy.stress.save });
    expect(save).toBeDisabled();
    await userEvent.type(screen.getByLabelText(copy.stress.answerLabel), "Karena ada pembanding historis.");
    await userEvent.click(save);
    expect(onAnswer).toHaveBeenCalledWith("q1", "Karena ada pembanding historis.");
  });

  it("tanpa pertanyaan: tombol 'Buat pertanyaan'", () => {
    render(<StressPanel questions={[]} onGenerate={vi.fn()} onAnswer={vi.fn()} />);
    expect(screen.getByRole("button", { name: copy.stress.generate })).toBeInTheDocument();
  });
});
