"""Diff antarversi di level elemen penelitian (Langkah 18), bukan diff teks.

Murni & deterministik. Elemen dipasangkan per tipe berdasarkan kemiripan isi.
"""

from dataclasses import dataclass, field
from difflib import SequenceMatcher

from app.domain.rules import Element, normalize

SAME = 0.9  # >= dianggap tidak berubah (beda spasi/tanda baca kecil)
RELATED = 0.5  # >= dianggap elemen yang sama tetapi isinya berubah


@dataclass(frozen=True)
class Changed:
    old: Element
    new: Element
    similarity: float


@dataclass
class ElementDiff:
    unchanged: list[tuple[Element, Element]] = field(default_factory=list)
    changed: list[Changed] = field(default_factory=list)
    added: list[Element] = field(default_factory=list)
    removed: list[Element] = field(default_factory=list)

    @property
    def has_changes(self) -> bool:
        return bool(self.changed or self.added or self.removed)


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, normalize(a), normalize(b), autojunk=False).ratio()


def diff_elements(old: list[Element], new: list[Element]) -> ElementDiff:
    result = ElementDiff()
    remaining = list(new)
    unmatched: list[Element] = []
    for o in old:
        candidates = [(similarity(o.content, n.content), n) for n in remaining if n.type == o.type]
        best = max(candidates, key=lambda c: c[0], default=None)
        if best is None or best[0] < RELATED:
            unmatched.append(o)
            continue
        score, match = best
        remaining.remove(match)
        if score >= SAME:
            result.unchanged.append((o, match))
        else:
            result.changed.append(Changed(o, match, round(score, 2)))
    # Sisa bertipe sama dipasangkan sesuai urutan: RQ yang dirumuskan ulang total tetap "diubah",
    # bukan "dihapus + baru". Sisa tanpa pasangan tipe tetap dihapus/baru.
    for o in unmatched:
        slot = next((n for n in remaining if n.type == o.type), None)
        if slot is None:
            result.removed.append(o)
            continue
        remaining.remove(slot)
        result.changed.append(Changed(o, slot, round(similarity(o.content, slot.content), 2)))
    result.added.extend(remaining)
    return result
