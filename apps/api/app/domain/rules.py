"""Constraint engine deterministik (technical-design §2; abstrak §6: "each flag cites a rule").

Murni: tanpa IO. Aturan datang sebagai data (rules/*.yaml) yang divalidasi model di bawah.
Menambah aturan = menambah data + contoh, bukan mengubah engine.
LLM tidak memutuskan apa pun di sini.
"""

import re
from dataclasses import dataclass, field
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


Check = Annotated[
    ConflictCheck | RequiresCheck | RequiredSectionsCheck, Field(discriminator="kind")
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

    def applies_to(self, program: str) -> bool:
        return self.enabled and ("*" in self.programs or program in self.programs)


# ---- Engine -------------------------------------------------------------------------------


def _status(evidence: list[Element]) -> Status:
    # Temuan hanya "saran AI" bila semua evidence-nya terverifikasi; selain itu perlu konfirmasi.
    if evidence and all(e.verified for e in evidence):
        return Status.AI_SUGGESTED
    return Status.NEEDS_USER_CONFIRMATION


def _finding(rule: Rule, evidence: list[Element], why: str | None = None) -> RuleFinding:
    return RuleFinding(
        rule_id=rule.id,
        priority=rule.priority,
        title=rule.title,
        why_flagged=why or rule.why_flagged,
        suggested_clarification=rule.suggested_clarification,
        evidence=[Evidence(e.id, e.page) for e in evidence],
        status=_status(evidence),
    )


def evaluate(rule: Rule, elements: list[Element], document_text: str = "") -> list[RuleFinding]:
    check = rule.check
    if isinstance(check, ConflictCheck):
        a, b = check.a.select(elements), check.b.select(elements)
        return [_finding(rule, a + b)] if a and b else []
    if isinstance(check, RequiresCheck):
        source = check.source.select(elements)
        return [_finding(rule, source)] if source and not check.target.select(elements) else []
    missing = [s for s in check.sections if not has_term(document_text, s.any_terms)]
    return [_finding(rule, [], f"{rule.why_flagged} ({s.name})") for s in missing]


def run(
    rules: list[Rule], elements: list[Element], program: str, document_text: str = ""
) -> list[RuleFinding]:
    return [f for r in rules if r.applies_to(program) for f in evaluate(r, elements, document_text)]


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
