"""PDF -> {nomor_halaman: teks}. Nomor halaman berasal dari parser, bukan dari LLM."""

from io import BytesIO
from pathlib import Path

from pypdf import PdfReader


def read_pages(source: str | Path | bytes) -> dict[int, str]:
    reader = PdfReader(BytesIO(source) if isinstance(source, bytes) else source)
    return {i: (page.extract_text() or "") for i, page in enumerate(reader.pages, start=1)}
