"""Constraint engine deterministik (technical-design §2; abstrak §6: "each flag cites a rule").

Murni: tanpa IO. Aturan datang sebagai data (rules/*.yaml) yang divalidasi model di bawah.
Menambah aturan = menambah data + contoh, bukan mengubah engine.
LLM tidak memutuskan apa pun di sini.
"""

import re
from dataclasses import dataclass, field, replace
from typing import Annotated, Literal

from pydantic import BaseModel, Field

from app.domain.status import Status

_NON_WORD = re.compile(r"[^\w]+", re.UNICODE)


def normalize(text: str) -> str:
    """Huruf kecil; tanda baca/tanda hubung jadi spasi: 'Pre-Test' -> 'pre test'."""
    return " ".join(_NON_WORD.sub(" ", text.lower()).split())


def has_term(text: str, terms: list[str]) -> bool:
    padded = f" {normalize(text)} "
    return any(f" {normalize(t)} " in padded for t in terms)


# ---- Elemen masukan (hasil ekstraksi yang sudah diverifikasi) -------------------------------


@dataclass(frozen=True)
class Element:
    id: str
    type: str  # research_question | objective | variable | method | instrument | analysis | ...
    content: str
    page: int
    verified: bool = True  # kutipan cocok dengan halaman (domain/verification.py)


@dataclass(frozen=True)
class Evidence:
    element: str
    page: int


@dataclass(frozen=True)
class RuleFinding:
    rule_id: str
    priority: str
    title: str
    why_flagged: str
    suggested_clarification: str
    evidence: list[Evidence] = field(default_factory=list)
    status: Status = Status.AI_SUGGESTED


# ---- Skema aturan -------------------------------------------------------------------------


class Match(BaseModel):
    types: list[str] = Field(min_length=1)
    any_terms: list[str] = Field(default_factory=list)  # kosong = semua elemen bertipe itu
    label: str | None = None  # nama yang ditampilkan di temuan, mis. "rumusan masalah"

    def select(self, elements: list[Element]) -> list[Element]:
        return [
            e
            for e in elements
            if e.type in self.types and (not self.any_terms or has_term(e.content, self.any_terms))
        ]


class ConflictCheck(BaseModel):
    """Terpicu bila elemen yang cocok dengan `a` DAN elemen yang cocok dengan `b` sama-sama ada."""

    kind: Literal["conflict"]
    a: Match
    b: Match


class RequiresCheck(BaseModel):
    """Terpicu bila ada elemen `source` tetapi tidak ada satu pun elemen `target`."""

    kind: Literal["requires"]
    source: Match
    target: Match


class Section(BaseModel):
    name: str
    any_terms: list[str] = Field(min_length=1)


class RequiredSectionsCheck(BaseModel):
    """Terpicu per bagian wajib panduan yang istilahnya tidak muncul di teks dokumen."""

    kind: Literal["required_sections"]
    sections: list[Section] = Field(min_length=1)


class CountMatchCheck(BaseModel):
    """Terpicu bila jumlah elemen `a` dan `b` sama-sama > 0 tetapi berbeda."""

    kind: Literal["count_match"]
    a: Match
    b: Match


class MissingTermsCheck(BaseModel):
    """Terpicu bila elemen `when` ada, tetapi dokumen tidak memuat satu pun istilah `absent`
    (mis. desain eksperimen tanpa pembahasan ancaman validitas)."""

    kind: Literal["missing_terms"]
    when: Match
    absent: list[str] = Field(min_length=1)


class ForbiddenSectionsCheck(BaseModel):
    """Terpicu per bagian yang **tidak seharusnya** ada di dokumen (mis. Bab Hasil di proposal)."""

    kind: Literal["forbidden_sections"]
    sections: list[Section] = Field(min_length=1)


Check = Annotated[
    ConflictCheck
    | RequiresCheck
    | RequiredSectionsCheck
    | CountMatchCheck
    | MissingTermsCheck
    | ForbiddenSectionsCheck,
    Field(discriminator="kind"),
]


class Example(BaseModel):
    elements: list[dict[str, str | int]] = Field(default_factory=list)
    document_text: str = ""


class Rule(BaseModel):
    id: str = Field(pattern=r"^R-[A-Z0-9]+(-[A-Z0-9]+)*$")
    enabled: bool = True
    programs: list[str] = Field(default_factory=lambda: ["*"])
    priority: Literal["high", "medium", "low"]
    title: str
    why_flagged: str
    suggested_clarification: str
    check: Check
    # Wajib: contoh yang harus memicu dan yang tidak boleh memicu (docs/alignment-rules.md).
    examples: dict[Literal["fires", "quiet"], Example]
    reviewed_by_supervisor: bool = False
    # Dasar metodologis aturan (prinsip/rujukan), agar temuan bisa diperiksa dosen.
    basis: str | None = None
    # Rujukan akademik (APA). Tanpa nomor halaman: tim memverifikasi halaman sebelum dipakai.
    references: list[str] = Field(default_factory=list)
    # Langkah perbaikan yang bisa dikerjakan mahasiswa. Tindakan, bukan teks skripsi.
    suggestions: list[str] = Field(default_factory=list)

    def applies_to(self, program: str) -> bool:
        return self.enabled and ("*" in self.programs or program in self.programs)


# ---- Engine -------------------------------------------------------------------------------


def _status(evidence: list[Element]) -> Status:
    # Temuan hanya "saran AI" bila semua evidence-nya terverifikasi; selain itu perlu konfirmasi.
    if evidence and all(e.verified for e in evidence):
        return Status.AI_SUGGESTED
    return Status.NEEDS_USER_CONFIRMATION


def _finding(
    rule: Rule, evidence: list[Element], why: str | None = None, detail: str | None = None
) -> RuleFinding:
    return RuleFinding(
        rule_id=rule.id,
        priority=rule.priority,
        # Satu aturan bisa menghasilkan beberapa temuan: detail membuat judulnya bisa dibedakan.
        title=f"{rule.title}: {detail}" if detail else rule.title,
        why_flagged=why or rule.why_flagged,
        suggested_clarification=rule.suggested_clarification,
        evidence=[Evidence(e.id, e.page) for e in evidence],
        status=_status(evidence),
    )


TOC_PAGE = re.compile(r"\bDAFTAR (ISI|TABEL|GAMBAR|LAMPIRAN)\b")


def locate(pages: dict[int, str], terms: list[str]) -> int | None:
    """Halaman pertama (di luar daftar isi) yang memuat salah satu istilah."""
    for n in sorted(pages):
        if not TOC_PAGE.search(pages[n]) and has_term(pages[n], terms):
            return n
    return None


def evaluate(
    rule: Rule,
    elements: list[Element],
    document_text: str = "",
    pages: dict[int, str] | None = None,
) -> list[RuleFinding]:
    check = rule.check
    if isinstance(check, ConflictCheck):
        a, b = check.a.select(elements), check.b.select(elements)
        return [_finding(rule, a + b)] if a and b else []
    if isinstance(check, RequiresCheck):
        source = check.source.select(elements)
        return [_finding(rule, source)] if source and not check.target.select(elements) else []
    if isinstance(check, CountMatchCheck):
        a, b = check.a.select(elements), check.b.select(elements)
        if a and b and len(a) != len(b):
            counts = (
                f"{len(a)} {check.a.label or check.a.types[0]}, "
                f"{len(b)} {check.b.label or check.b.types[0]}"
            )
            return [_finding(rule, a + b, f"{rule.why_flagged} ({counts})", counts)]
        return []
    if isinstance(check, MissingTermsCheck):
        when = check.when.select(elements)
        return [_finding(rule, when)] if when and not has_term(document_text, check.absent) else []
    if isinstance(check, ForbiddenSectionsCheck):
        out = []
        for s in check.sections:
            if not has_term(document_text, s.any_terms):
                continue
            page = locate(pages or {}, s.any_terms)
            f = _finding(rule, [], f"{rule.why_flagged} ({s.name})", s.name)
            if page is not None:  # teks bagian itu sendiri adalah bukti, dan halamannya diketahui
                f = replace(
                    f, evidence=[Evidence(f"section:{s.name}", page)], status=Status.AI_SUGGESTED
                )
            out.append(f)
        return out
    missing = [s for s in check.sections if not has_term(document_text, s.any_terms)]
    return [_finding(rule, [], f"{rule.why_flagged} ({s.name})", s.name) for s in missing]


def run(
    rules: list[Rule],
    elements: list[Element],
    program: str,
    document_text: str = "",
    pages: dict[int, str] | None = None,
) -> list[RuleFinding]:
    return [
        f
        for r in rules
        if r.applies_to(program)
        for f in evaluate(r, elements, document_text, pages)
    ]


def example_elements(example: Example) -> list[Element]:
    return [
        Element(
            id=str(raw.get("id", f"E{i}")),
            type=str(raw["type"]),
            content=str(raw["content"]),
            page=int(raw.get("page", 1)),
        )
        for i, raw in enumerate(example.elements, start=1)
    ]
