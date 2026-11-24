"""Ekstraksi elemen penelitian dari **struktur bab** proposal (tanpa LLM).

Proposal skripsi di Indonesia umumnya mengikuti struktur baku: BAB I (Rumusan Masalah, Tujuan),
BAB III (Desain, Variabel, Populasi/Data, Instrumen, Analisis). Elemen diambil dari isi bagian
dengan judul tersebut; kutipannya selalu salinan persis teks halaman, sehingga lolos verifikasi
secara jujur. Hasilnya tetap **saran** yang harus dikonfirmasi mahasiswa. Bagian yang judulnya
tidak baku tidak akan terdeteksi; di situlah LLM (nanti) atau input manual mengisi.
"""

import re
from dataclasses import dataclass

# Urutan kata kunci = prioritas. Pencocokan peka huruf (judul ditulis Title Case/UPPERCASE),
# agar penyebutan dalam kalimat ("rumusan masalah dalam penelitian ini") tidak dianggap judul.
SECTIONS: list[tuple[str, list[str]]] = [
    ("research_question", ["Rumusan Masalah", "Pertanyaan Penelitian", "Research Questions"]),
    ("objective", ["Tujuan Penelitian", "Research Objectives"]),
    (
        "method",
        ["Desain Penelitian", "Rancangan Penelitian", "Jenis Penelitian", "Metode Penelitian"],
    ),
    ("variable", ["Variabel Penelitian", "Definisi Operasional Variabel", "Definisi Operasional"]),
    (
        "population",
        [
            "Populasi dan Sampel",
            "Subjek Penelitian",
            "Objek Penelitian",
            "Sumber Data",
            "Karakteristik Dataset",
            "Dataset Penelitian",
        ],
    ),
    ("instrument", ["Instrumen Penelitian", "Teknik Pengumpulan Data"]),
    ("analysis", ["Teknik Analisis Data", "Analisis Data", "Metode Analisis Data"]),
    ("claim", ["Hipotesis Penelitian", "Hipotesis"]),
]

MAX_CHARS = 350
SKIP_PAGE = re.compile(r"\bDAFTAR (ISI|TABEL|GAMBAR|LAMPIRAN)\b")
NUMBERED = re.compile(r"(?:^|(?<=\s))(\d{1,2})[.)]\s+(?=[A-Z])")
SENTENCE_END = re.compile(r"(?<=[.?!])\s+(?=[A-Z0-9“\"(])")
NEXT_HEADING = re.compile(r"(?<=\s)(?:\d+(?:\.\d+)+\.?\s+[A-Z]|BAB\s+[IVX]+\b)")
CAPTION = re.compile(r"(Tabel|Gambar|Table|Figure)\s*$")
VARIABLE_KINDS = [
    "bebas",
    "terikat",
    "kontrol",
    "independen",
    "dependen",
    "moderator",
    "intervening",
]
DEFINING = re.compile(r"\b(adalah|yaitu|meliputi|mencakup|berupa)\b")


@dataclass(frozen=True)
class Extracted:
    type: str
    content: str
    quote: str  # bagian kutipan yang berada di halaman `page` (verifikasi per halaman)
    page: int


def _document(pages: dict[int, str]) -> tuple[str, list[tuple[int, int, int]]]:
    """Gabungkan halaman; kembalikan teks dan rentang (awal, akhir, halaman). Halaman daftar isi
    dikosongkan agar judul di daftar isi tidak dianggap bagian."""
    text, spans = "", []
    for n in sorted(pages):
        body = "" if SKIP_PAGE.search(pages[n]) else pages[n]
        start = len(text)
        text += body + "\n"
        spans.append((start, start + len(body), n))
    return text, spans


def _page_at(spans: list[tuple[int, int, int]], pos: int) -> tuple[int, int]:
    for start, end, n in spans:
        if start <= pos <= end:
            return n, end
    return spans[-1][2], spans[-1][1]


def _section(text: str, keywords: list[str]) -> tuple[int, int] | None:
    """Judul harus bernomor ("3.2.2 Variabel Penelitian") atau di awal baris/bagian (DOCX),
    bukan sel tabel di tengah teks. Judul induk yang isinya langsung subjudul dilewati."""
    for kw in keywords:
        name = rf"(?:{re.escape(kw)}|{re.escape(kw.upper())})\b"
        pattern = rf"(?:(?<=\s)\d+(?:\.\d+)*\.?\s+{name}|(?:^|(?<=\n))\s*{name})"
        for m in re.finditer(pattern, text):
            end = len(text)
            for nxt in NEXT_HEADING.finditer(text, m.end()):
                if not CAPTION.search(text[max(0, nxt.start() - 8) : nxt.start()]):
                    end = nxt.start()
                    break
            if len(text[m.end() : end].strip()) >= 40:
                return m.end(), min(end, m.end() + 4000)
    return None


def _items(body: str) -> list[tuple[int, int]]:
    """Rentang item daftar bernomor 1., 2., ... (harus dimulai dari 1)."""
    marks = [m for m in NUMBERED.finditer(body)]
    seq, expected = [], 1
    for m in marks:
        if int(m.group(1)) == expected:
            seq.append(m)
            expected += 1
    if len(seq) < 2:
        return []
    return [
        (m.end(), seq[i + 1].start() if i + 1 < len(seq) else len(body)) for i, m in enumerate(seq)
    ]


def _sentences(body: str) -> list[tuple[int, int]]:
    out, pos = [], 0
    for m in SENTENCE_END.finditer(body):
        out.append((pos, m.start()))
        pos = m.end()
    out.append((pos, len(body)))
    return [(a, b) for a, b in out if body[a:b].strip()]


def _clip(text: str) -> str:
    text = " ".join(text.split()).strip(" ;,")
    return text if len(text) <= MAX_CHARS else text[: MAX_CHARS - 1].rstrip() + "…"


def _pick(type_: str, body: str) -> list[tuple[int, int]]:
    if type_ == "research_question":
        items = _items(body)
        if items:  # potong tiap item sampai tanda tanya pertama
            return [
                (a, a + body[a:b].index("?") + 1) if "?" in body[a:b] else (a, b) for a, b in items
            ]
        return [s for s in _sentences(body) if body[s[0] : s[1]].rstrip().endswith("?")][:5]
    if type_ in {"objective", "claim"}:
        items = _items(body)
        if items:
            return [(a, a + (_sentences(body[a:b]) or [(0, b - a)])[0][1]) for a, b in items][:6]
        return _sentences(body)[:1]
    if type_ == "variable":
        picked, seen = [], set()
        for a, b in _sentences(body):
            s = body[a:b].lower()
            kind = next((k for k in VARIABLE_KINDS if f"variabel {k}" in s), None)
            if kind and kind not in seen and DEFINING.search(s):
                seen.add(kind)
                picked.append((a, b))
        return picked or _sentences(body)[:1]
    return _sentences(body)[:1]  # metode, populasi, instrumen, analisis: kalimat pembuka


def extract_by_structure(pages: dict[int, str]) -> list[Extracted]:
    text, spans = _document(pages)
    out: list[Extracted] = []
    for type_, keywords in SECTIONS:
        found = _section(text, keywords)
        if not found:
            continue
        start, end = found
        body = text[start:end]
        for a, b in _pick(type_, body):
            raw = body[a:b].strip()
            if len(raw) < 12:
                continue
            abs_a = start + a + (len(body[a:b]) - len(body[a:b].lstrip()))
            page, page_end = _page_at(spans, abs_a)
            quote = text[abs_a : min(abs_a + len(raw), page_end)]
            out.append(Extracted(type_, _clip(raw), _clip(quote), page))
    return out
