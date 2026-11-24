import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import { copy } from "@/lib/copy";
import { FindingQueue } from "./FindingQueue";
import { ToolsPanel } from "./ToolsPanel";
import { findings } from "./sample";

describe("ToolsPanel", () => {
  it("hanya tool yang tersedia menjadi tautan; sisanya berlabel Segera", () => {
    render(<ToolsPanel />);
    const links = screen.getAllByRole("link");
    expect(links).toHaveLength(1);
    expect(links[0]).toHaveTextContent(copy.dashboard.tools.items.consistency.title);
    expect(screen.getAllByText(copy.soon)).toHaveLength(3);
  });
});

describe("FindingQueue", () => {
  it("konfirmasi mahasiswa mengubah status dan menghilangkan tombol aksi", async () => {
    render(<FindingQueue initial={[findings[0]]} />);
    await userEvent.click(screen.getByRole("button", { name: copy.confirm }));
    expect(screen.getByText(copy.status.student_confirmed)).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: copy.confirm })).not.toBeInTheDocument();
  });

  it("tolak mengubah status jadi Ditolak hanya pada temuan itu", async () => {
    render(<FindingQueue initial={findings} />);
    const items = screen.getAllByRole("listitem");
    await userEvent.click(within(items[1]).getByRole("button", { name: copy.reject }));
    expect(within(items[1]).getByText(copy.status.rejected)).toBeInTheDocument();
    expect(within(items[0]).getByRole("button", { name: copy.confirm })).toBeInTheDocument();
  });
});
