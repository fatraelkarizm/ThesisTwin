"""Skema konfigurasi ontologi & kosakata ekstraksi (config/*.yaml). Murni: tanpa IO.

Tipe elemen, relasi, tabel dampak, label, dan kosakata judul bab adalah DATA (AGENTS.md §3.8).
Engine di domain/ menerima objek ini sebagai parameter; services/config.py yang membaca file.
"""

from typing import Self

from pydantic import BaseModel, Field, model_validator


class ElementType(BaseModel):
    id: str = Field(pattern=r"^[a-z_]+$")
    label: str
    # Awalan nomor elemen di UI (R1, T2); nama ringkas untuk peta.
    code: str = Field(pattern=r"^[A-Z]{1,3}$")
    short: str | None = None
    layer: int = Field(ge=0)
    # Pertanyaan sidang umum untuk tipe ini; {content} = isi elemen.
    baseline_question: str | None = None


class Relation(BaseModel):
    source: str
    target: str
    type: str
    gap_question: str | None = None


class ImpactCheck(BaseModel):
    affected: str
    check: str


class Ontology(BaseModel):
    element_types: list[ElementType] = Field(min_length=1)
    relations: list[Relation] = Field(default_factory=list)
    impact: dict[str, list[ImpactCheck]] = Field(default_factory=dict)
    # Urutan kotak di peta penelitian (UI).
    map: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _known_types(self) -> Self:
        known = {t.id for t in self.element_types}
        if len(known) != len(self.element_types):
            raise ValueError("id element_types ganda")
        codes = [t.code for t in self.element_types]
        if len(set(codes)) != len(codes):
            raise ValueError("code element_types ganda")
        used = [r.source for r in self.relations] + [r.target for r in self.relations]
        used += list(self.impact) + [c.affected for cs in self.impact.values() for c in cs]
        used += self.map
        unknown = sorted(set(used) - known)
        if unknown:
            raise ValueError(f"tipe tidak dikenal: {', '.join(unknown)}")
        return self

    @property
    def type_ids(self) -> list[str]:
        return [t.id for t in self.element_types]

    def label(self, type_id: str) -> str:
        return next((t.label for t in self.element_types if t.id == type_id), type_id)

    def layer(self, type_id: str) -> int:
        return next((t.layer for t in self.element_types if t.id == type_id), 9)

    def baseline_question(self, type_id: str) -> str | None:
        return next((t.baseline_question for t in self.element_types if t.id == type_id), None)

    def gap_question(self, source: str, target: str) -> str | None:
        return next(
            (r.gap_question for r in self.relations if (r.source, r.target) == (source, target)),
            None,
        )


class SectionVocab(BaseModel):
    type: str
    headings: list[str] = Field(min_length=1)
    standalone_headings: list[str] = Field(default_factory=list)


class Extraction(BaseModel):
    max_chars: int = Field(default=350, ge=40)
    skip_pages: list[str] = Field(default_factory=list)
    sections: list[SectionVocab] = Field(min_length=1)
    variable_kinds: list[str] = Field(default_factory=list)
    defining_words: list[str] = Field(default_factory=list)

    def check_types(self, ontology: Ontology) -> None:
        unknown = sorted({s.type for s in self.sections} - set(ontology.type_ids))
        if unknown:
            raise ValueError(f"sections memakai tipe tidak dikenal: {', '.join(unknown)}")
