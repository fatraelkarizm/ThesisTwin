import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
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

describe("ToolsPanel (proyek nyata)", () => {
  it("tiap tool menaut ke halamannya sendiri dan berlabel Tersedia, bukan simulasi", () => {
    render(<ToolsPanel live />);
    const links = screen.getAllByRole("link");
    expect(links).toHaveLength(4);
    expect(links.map((a) => a.getAttribute("href"))).toEqual(["/temuan", "/versi", "/brief", "/stress-test"]);
    expect(screen.getAllByText(copy.dashboard.tools.available)).toHaveLength(4);
    expect(screen.queryByText(copy.simulated)).not.toBeInTheDocument();
  });
});

describe("FindingQueue (proyek nyata)", () => {
  it("keputusan dikirim lewat onDecide dan hasil API yang ditampilkan", async () => {
    const onDecide = vi.fn().mockResolvedValue({ ...findings[0], status: "student_confirmed" });
    render(<FindingQueue initial={[findings[0]]} onDecide={onDecide} />);
    await userEvent.click(screen.getByRole("button", { name: copy.confirm }));
    expect(onDecide).toHaveBeenCalledWith(findings[0].id, "student_confirmed");
    expect(await screen.findByText(copy.status.student_confirmed)).toBeInTheDocument();
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
