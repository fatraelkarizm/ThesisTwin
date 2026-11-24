"""Verifikasi evidence hasil ekstraksi (menutup gap G3 di docs/feedback/gap.md).

Murni & deterministik. Tiga hal diperiksa untuk tiap elemen:
1. halaman yang dirujuk memang ada di dokumen;
2. kutipan (`quote`) benar-benar muncul di halaman itu (fuzzy, toleran spasi/tanda baca/OCR ringan);
3. kalau gagal, elemen tidak ditolak diam-diam: status diturunkan ke needs_user_confirmation.
"""

import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from enum import StrEnum

from app.domain.status import Status

_WORD = re.compile(r"\w+", re.UNICODE)


class Verdict(StrEnum):
    VERIFIED = "verified"
    PAGE_MISSING = "page_missing"
    QUOTE_NOT_FOUND = "quote_not_found"
    QUOTE_EMPTY = "quote_empty"


@dataclass(frozen=True)
class Verification:
    verdict: Verdict
    score: float  # kemiripan terbaik 0..1 (1.0 = persis)

    @property
    def ok(self) -> bool:
        return self.verdict is Verdict.VERIFIED

    def status(self, proposed: Status = Status.AI_SUGGESTED) -> Status:
        return proposed if self.ok else Status.NEEDS_USER_CONFIRMATION


def _words(text: str) -> list[str]:
    return [w.lower() for w in _WORD.findall(text)]


def best_match_score(quote: str, page_text: str) -> float:
    """Kemiripan terbaik (0..1) antara kutipan dan jendela teks halaman, level karakter.

    Level karakter (bukan kata) agar salah-OCR satu huruf tidak menggugurkan seluruh kata.
    """
    q, p = " ".join(_words(quote)), " ".join(_words(page_text))
    if not q or not p:
        return 0.0
    if q in p:
        return 1.0
    if len(q) >= len(p):
        return SequenceMatcher(None, q, p, autojunk=False).ratio()
    starts = [0] + [i + 1 for i, c in enumerate(p) if c == " "]
    best = 0.0
    for i in starts:
        window = p[i : i + len(q)]
        best = max(best, SequenceMatcher(None, q, window, autojunk=False).ratio())
    return best


def verify_quote(
    quote: str, page: int, pages: dict[int, str], threshold: float = 0.9
) -> Verification:
    if page not in pages:
        return Verification(Verdict.PAGE_MISSING, 0.0)
    if not _words(quote):
        return Verification(Verdict.QUOTE_EMPTY, 0.0)
    score = best_match_score(quote, pages[page])
    verdict = Verdict.VERIFIED if score >= threshold else Verdict.QUOTE_NOT_FOUND
    return Verification(verdict, score)
