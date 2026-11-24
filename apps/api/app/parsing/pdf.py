"""PDF -> {nomor_halaman: teks}. Nomor halaman berasal dari parser, bukan dari LLM."""

from pathlib import Path

from pypdf import PdfReader


def read_pages(source: str | Path) -> dict[int, str]:
    reader = PdfReader(source)
    return {i: (page.extract_text() or "") for i, page in enumerate(reader.pages, start=1)}
