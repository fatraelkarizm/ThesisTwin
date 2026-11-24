"""Redaction deterministik sebelum teks dikirim ke LLM (FR-014, NFR-02).

Regex-based dan sengaja konservatif: lebih baik menyamarkan berlebih daripada membocorkan.
Bukan jaminan penuh; nama orang dan data peserta bebas-teks butuh tinjauan manusia.
"""

import re

_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
_PHONE = re.compile(r"(?<!\d)(?:\+62|62|0)8\d{7,11}(?!\d)")
_NIM = re.compile(r"(?<!\d)\d{8,14}(?!\d)")


def redact(text: str) -> str:
    text = _EMAIL.sub("[EMAIL]", text)
    text = _PHONE.sub("[TELEPON]", text)  # sebelum NIM: nomor telepon juga deret digit panjang
    return _NIM.sub("[NIM]", text)
