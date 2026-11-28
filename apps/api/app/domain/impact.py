"""Analisis dampak perubahan antarversi (FR-071, FR-072; aturan R-POP-CHANGE di katalog).

Bila sebuah elemen berubah, elemen yang bergantung padanya perlu dicek ulang. Bila elemen yang
bergantung itu **tidak berubah sama sekali**, tandai sebagai ketergantungan yang mungkin belum
diperbarui (contoh proposal §16: RQ sudah diubah, abstrak masih memakai kata "impact").
"""

from dataclasses import dataclass

from app.domain.diff import ElementDiff
from app.domain.ontology import Ontology
from app.domain.rules import Element


@dataclass(frozen=True)
class Impact:
    changed_type: str
    change: str  # changed | added | removed
    affected_type: str
    check: str
    affected_elements: tuple[Element, ...]
    stale: bool  # elemen terdampak tidak berubah sejak versi lalu


def change_impact(d: ElementDiff, new: list[Element], ontology: Ontology) -> list[Impact]:
    unchanged_ids = {n.id for _, n in d.unchanged}
    sources = (
        [("changed", c.new.type) for c in d.changed]
        + [("added", e.type) for e in d.added]
        + [("removed", e.type) for e in d.removed]
    )
    out: list[Impact] = []
    seen: set[tuple[str, str]] = set()
    for change, src_type in sources:
        for item in ontology.impact.get(src_type, []):
            affected_type, check = item.affected, item.check
            if (src_type, affected_type) in seen:
                continue
            seen.add((src_type, affected_type))
            affected = tuple(e for e in new if e.type == affected_type)
            out.append(
                Impact(
                    changed_type=src_type,
                    change=change,
                    affected_type=affected_type,
                    check=check,
                    affected_elements=affected,
                    stale=bool(affected) and all(e.id in unchanged_ids for e in affected),
                )
            )
    return out
