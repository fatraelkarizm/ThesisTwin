"""Ekstraksi elemen penelitian dari **struktur bab** proposal (tanpa LLM).

Proposal skripsi di Indonesia umumnya mengikuti struktur baku: BAB I (Rumusan Masalah, Tujuan),
BAB III (Desain, Variabel, Populasi/Data, Instrumen, Analisis). Elemen diambil dari isi bagian
dengan judul tersebut; kutipannya selalu salinan persis teks halaman, sehingga lolos verifikasi
secara jujur. Hasilnya tetap **saran** yang harus dikonfirmasi mahasiswa.

Kosakata judul bab adalah data (config/extraction.yaml, skema `Extraction`). Bagian yang judulnya
belum terdaftar tidak akan terdeteksi; tambahkan judulnya di config atau isi manual.
"""

import re
from dataclasses import dataclass

from app.domain.ontology import Extraction, SectionVocab

# Mekanika pemotongan teks, bukan kosakata domain.
NUMBERED = re.compile(r"(?:^|(?<=\s))(\d{1,2})[.)]\s+(?=[A-Z])")
SENTENCE_END = re.compile(r"(?<=[.?!])\s+(?=[A-Z0-9“\"(])")
NEXT_HEADING = re.compile(r"(?<=\s)(?:\d+(?:\.\d+)+\.?\s+[A-Z]|BAB\s+[IVX]+\b)")
CAPTION = re.compile(r"(Tabel|Gambar|Table|Figure)\s*$")


@dataclass(frozen=True)
class Extracted:
    type: str
    content: str
    quote: str  # bagian kutipan yang berada di halaman `page` (verifikasi per halaman)
    page: int


def _any_word(words: list[str]) -> re.Pattern[str] | None:
    return re.compile(r"\b(" + "|".join(map(re.escape, words)) + r")\b") if words else None


def _document(
    pages: dict[int, str], skip: re.Pattern[str] | None
) -> tuple[str, list[tuple[int, int, int]]]:
    """Gabungkan halaman; kembalikan teks dan rentang (awal, akhir, halaman). Halaman daftar isi
    dikosongkan agar judul di daftar isi tidak dianggap bagian."""
    text, spans = "", []
    for n in sorted(pages):
        body = "" if skip and skip.search(pages[n]) else pages[n]
        start = len(text)
        text += body + "\n"
        spans.append((start, start + len(body), n))
    return text, spans


def _page_at(spans: list[tuple[int, int, int]], pos: int) -> tuple[int, int]:
    for start, end, n in spans:
        if start <= pos <= end:
            return n, end
    return spans[-1][2], spans[-1][1]


def _section(text: str, vocab: SectionVocab) -> tuple[int, int] | None:
    """Judul harus bernomor ("3.2.2 Variabel Penelitian") atau di awal baris/bagian (DOCX),
    bukan sel tabel di tengah teks. Judul induk yang isinya langsung subjudul dilewati.
    Judul `standalone` hanya sah bila berdiri sendiri di barisnya ("1.3 Tujuan", bukan
    "2.1 Tujuan Pembelajaran")."""
    headings = [(h, r"\b") for h in vocab.headings]
    headings += [(h, r"[ \t]*(?=\n|$)") for h in vocab.standalone_headings]
    for word, tail in headings:
        name = rf"(?:{re.escape(word)}|{re.escape(word.upper())}){tail}"
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
    # Satu item pun dihitung bila bagian dibuka dengan "1." (mis. satu tujuan penelitian);
    # "1." di tengah prosa tidak.
    if not seq or (len(seq) == 1 and body[: seq[0].start()].strip()):
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


def _clip(text: str, max_chars: int) -> str:
    text = " ".join(text.split()).strip(" ;,")
    return text if len(text) <= max_chars else text[: max_chars - 1].rstrip() + "…"


def _pick(type_: str, body: str, vocab: Extraction) -> list[tuple[int, int]]:
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
        defining = _any_word(vocab.defining_words)
        picked, seen = [], set()
        for a, b in _sentences(body):
            s = body[a:b].lower()
            kind = next((k for k in vocab.variable_kinds if f"variabel {k}" in s), None)
            if kind and kind not in seen and defining and defining.search(s):
                seen.add(kind)
                picked.append((a, b))
        return picked or _sentences(body)[:1]
    return _sentences(body)[:1]  # metode, populasi, instrumen, analisis: kalimat pembuka


def extract_by_structure(pages: dict[int, str], vocab: Extraction) -> list[Extracted]:
    text, spans = _document(pages, _any_word(vocab.skip_pages))
    out: list[Extracted] = []
    for section in vocab.sections:
        found = _section(text, section)
        if not found:
            continue
        start, end = found
        body = text[start:end]
        for a, b in _pick(section.type, body, vocab):
            raw = body[a:b].strip()
            if len(raw) < 12:
                continue
            abs_a = start + a + (len(body[a:b]) - len(body[a:b].lstrip()))
            page, page_end = _page_at(spans, abs_a)
            quote = text[abs_a : min(abs_a + len(raw), page_end)]
            clip = vocab.max_chars
            out.append(Extracted(section.type, _clip(raw, clip), _clip(quote, clip), page))
    return out
