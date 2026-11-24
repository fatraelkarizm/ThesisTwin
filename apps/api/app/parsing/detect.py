"""Deteksi tipe file dari isi (magic bytes), bukan dari nama file atau header klien."""

from typing import Literal

Kind = Literal["pdf", "docx"]

PDF_MEDIA = "application/pdf"
DOCX_MEDIA = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def detect(data: bytes) -> Kind | None:
    if data.startswith(b"%PDF-"):
        return "pdf"
    # DOCX = ZIP berisi word/document.xml; cek ZIP di sini, isi divalidasi parser DOCX.
    if data.startswith(b"PK\x03\x04") and b"word/" in data[:4096]:
        return "docx"
    return None
