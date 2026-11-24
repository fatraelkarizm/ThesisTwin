"""Deteksi tipe file dari isi (magic bytes), bukan dari nama file atau header klien."""

import zipfile
from io import BytesIO
from typing import Literal

from app.parsing.tex import looks_like_tex

Kind = Literal["pdf", "docx", "tex"]

PDF_MEDIA = "application/pdf"
DOCX_MEDIA = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
TEX_MEDIA = "application/x-tex"


def detect(data: bytes) -> Kind | None:
    if data.startswith(b"%PDF-"):
        return "pdf"
    if data.startswith(b"PK\x03\x04"):
        # Urutan isi ZIP berbeda per aplikasi (Word, Google Docs, LibreOffice): cek daftar isinya.
        try:
            names = zipfile.ZipFile(BytesIO(data)).namelist()
        except zipfile.BadZipFile:
            return "docx" if b"word/" in data else None  # biar parser yang melaporkan rusak
        return "docx" if "word/document.xml" in names else None
    if looks_like_tex(data):
        return "tex"
    return None
