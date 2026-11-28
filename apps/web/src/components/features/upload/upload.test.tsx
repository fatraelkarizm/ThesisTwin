import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { copy } from "@/lib/copy";
import { UploadForm } from "./UploadForm";

const u = copy.upload;

function respond(body: unknown, status = 200) {
  return Promise.resolve(new Response(JSON.stringify(body), { status }));
}

const version = {
  id: "v1",
  version_no: 1,
  filename: "proposal.pdf",
  media_type: "application/pdf",
  sha256: "a".repeat(64),
  uploaded_at: "2026-11-24T00:00:00Z",
};

beforeEach(() => window.localStorage.clear());
afterEach(() => vi.unstubAllGlobals());

describe("UploadForm", () => {
  it("tombol unggah nonaktif sampai consent dicentang", async () => {
    vi.stubGlobal("fetch", vi.fn());
    render(<UploadForm />);
    const submit = screen.getByRole("button", { name: u.submit });
    expect(submit).toBeDisabled();
    await userEvent.click(screen.getByRole("checkbox"));
    expect(submit).toBeEnabled();
  });

  it("alur sukses: buat proyek, consent, unggah, tampilkan versi", async () => {
    const fetchMock = vi.fn((url: string) => {
      if (url.endsWith("/projects")) return respond({ id: "p1", title: "t", program: "matematika", consent_at: null });
      if (url.endsWith("/consent")) return respond({ id: "p1", title: "t", program: "matematika", consent_at: "x" });
      if (url.endsWith("/documents")) return respond({ version, created: true, pages: 3, auto_elements: 5, findings: 2 }, 201);
      return respond([version]);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<UploadForm />);
    await userEvent.upload(screen.getByLabelText(u.file), new File(["%PDF-"], "proposal.pdf"));
    await userEvent.click(screen.getByRole("checkbox"));
    await userEvent.click(screen.getByRole("button", { name: u.submit }));
    expect(await screen.findByText(new RegExp(u.created))).toBeInTheDocument();
    expect(screen.getByText(new RegExp(`3 ${u.pagesPdf}`))).toBeInTheDocument();
    expect(screen.getByText(u.autoResult(5, 2))).toBeInTheDocument();
    expect(screen.getByRole("link", { name: u.reviewFindings(2) })).toHaveAttribute("href", "/temuan");
    expect(window.localStorage.getItem("thesistwin.projectId")).toBe("p1");
  });

  it("pesan error API ditampilkan apa adanya", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn((url: string) =>
        url.endsWith("/documents")
          ? respond({ detail: "Format belum didukung. Unggah PDF atau DOCX." }, 415)
          : respond({ id: "p1", title: "t", program: "matematika", consent_at: "x" }),
      ),
    );
    render(<UploadForm />);
    // Nama .pdf lolos filter `accept`; isinya bukan PDF sehingga server yang menolak.
    await userEvent.upload(screen.getByLabelText(u.file), new File(["x"], "palsu.pdf"));
    await userEvent.click(screen.getByRole("checkbox"));
    await userEvent.click(screen.getByRole("button", { name: u.submit }));
    expect(await screen.findByRole("alert")).toHaveTextContent("Format belum didukung");
  });

  it("server mati: pesan jelas, bukan error mentah", async () => {
    vi.stubGlobal("fetch", vi.fn(() => Promise.reject(new TypeError("Failed to fetch"))));
    render(<UploadForm />);
    await userEvent.upload(screen.getByLabelText(u.file), new File(["%PDF-"], "p.pdf"));
    await userEvent.click(screen.getByRole("checkbox"));
    await userEvent.click(screen.getByRole("button", { name: u.submit }));
    expect(await screen.findByRole("alert")).toHaveTextContent("Server tidak bisa dihubungi");
  });
});
