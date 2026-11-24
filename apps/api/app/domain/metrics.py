"""Pengukuran akurasi ekstraksi terhadap set emas berlabel (research-validation-plan.md §11.3).

Murni. Item = (element_type, kunci_ternormalisasi). Dihitung per element_type.
"""

from collections import defaultdict
from dataclasses import dataclass

Item = tuple[str, str]


@dataclass(frozen=True)
class Score:
    precision: float
    recall: float
    f1: float
    tp: int
    fp: int
    fn: int


def _ratio(a: int, b: int) -> float:
    return a / b if b else 0.0


def _score(tp: int, fp: int, fn: int) -> Score:
    p, r = _ratio(tp, tp + fp), _ratio(tp, tp + fn)
    return Score(p, r, _ratio(2 * p * r, p + r), tp, fp, fn)


def score_extraction(predicted: set[Item], gold: set[Item]) -> dict[str, Score]:
    """Kunci hasil: tiap element_type plus "ALL"."""
    types = {t for t, _ in predicted | gold}
    out = {}
    for t in sorted(types):
        pt = {x for x in predicted if x[0] == t}
        gt = {x for x in gold if x[0] == t}
        out[t] = _score(len(pt & gt), len(pt - gt), len(gt - pt))
    out["ALL"] = _score(len(predicted & gold), len(predicted - gold), len(gold - predicted))
    return out


def evidence_correctness(rows: list[bool]) -> float:
    """Proporsi elemen yang halaman+kutipannya benar (BO-4/NFR-03)."""
    counts: dict[bool, int] = defaultdict(int)
    for ok in rows:
        counts[ok] += 1
    return _ratio(counts[True], len(rows))
