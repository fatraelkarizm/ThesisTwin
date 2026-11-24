"""PDF -> {nomor_halaman: teks}. Nomor halaman berasal dari parser, bukan dari LLM."""

import re
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader

_WORD_PER_LINE = re.compile(r"[ \t]*\n[ \t]*\n[ \t]*")  # "Kata\n \nKata" (ekspor Google Docs)
_SPACES = re.compile(r"[ \t]+")


def normalize(text: str) -> str:
    """Beberapa PDF (mis. ekspor Google Docs) terekstrak satu kata per baris, dipisah baris
    berisi spasi. Satukan kembali agar kalimat dan judul bagian utuh; baris biasa dipertahankan."""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if lines and sum(len(ln.split()) <= 2 for ln in lines) / len(lines) > 0.7:
        text = _WORD_PER_LINE.sub(" ", text)
    return _SPACES.sub(" ", text).strip()


def read_pages(source: str | Path | bytes) -> dict[int, str]:
    reader = PdfReader(BytesIO(source) if isinstance(source, bytes) else source)
    return {i: normalize(page.extract_text() or "") for i, page in enumerate(reader.pages, start=1)}
