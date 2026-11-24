"""Analisis dampak perubahan antarversi (FR-071, FR-072; aturan R-POP-CHANGE di katalog).

Bila sebuah elemen berubah, elemen yang bergantung padanya perlu dicek ulang. Bila elemen yang
bergantung itu **tidak berubah sama sekali**, tandai sebagai ketergantungan yang mungkin belum
diperbarui (contoh proposal §16: RQ sudah diubah, abstrak masih memakai kata "impact").
"""

from dataclasses import dataclass

from app.domain.diff import ElementDiff
from app.domain.rules import Element

# tipe yang berubah -> (tipe yang perlu dicek ulang, apa yang dicek)
IMPACT: dict[str, list[tuple[str, str]]] = {
    "research_question": [
        ("objective", "apakah tujuan masih menjawab rumusan masalah yang baru"),
        ("method", "apakah desain masih sesuai bentuk pertanyaan"),
        ("analysis", "apakah analisis masih menjawab pertanyaan"),
        ("claim", "apakah klaim/kesimpulan masih sesuai"),
    ],
    "objective": [
        ("method", "apakah desain masih mendukung tujuan"),
        ("instrument", "apakah instrumen masih mengukur yang dibutuhkan tujuan"),
        ("analysis", "apakah analisis masih menjawab tujuan"),
    ],
    "population": [
        ("method", "sampling frame, ukuran sampel, dan stratifikasi"),
        ("instrument", "kelayakan instrumen untuk populasi baru"),
        ("analysis", "apakah analisis masih sesuai ukuran/karakter sampel"),
        ("claim", "batas generalisasi hasil"),
    ],
    "variable": [
        ("instrument", "apakah instrumen masih mengukur variabel"),
        ("analysis", "apakah analisis sesuai skala data variabel"),
    ],
    "method": [
        ("analysis", "apakah analisis sesuai desain baru"),
        ("claim", "apakah klaim masih didukung desain"),
        ("limitation", "keterbatasan desain yang perlu ditulis"),
    ],
    "instrument": [("analysis", "apakah analisis sesuai data dari instrumen")],
    "analysis": [("claim", "apakah kesimpulan sesuai hasil analisis")],
}


@dataclass(frozen=True)
class Impact:
    changed_type: str
    change: str  # changed | added | removed
    affected_type: str
    check: str
    affected_elements: tuple[Element, ...]
    stale: bool  # elemen terdampak tidak berubah sejak versi lalu


def change_impact(d: ElementDiff, new: list[Element]) -> list[Impact]:
    unchanged_ids = {n.id for _, n in d.unchanged}
    sources = (
        [("changed", c.new.type) for c in d.changed]
        + [("added", e.type) for e in d.added]
        + [("removed", e.type) for e in d.removed]
    )
    out: list[Impact] = []
    seen: set[tuple[str, str]] = set()
    for change, src_type in sources:
        for affected_type, check in IMPACT.get(src_type, []):
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
