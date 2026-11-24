"""Orkestrasi ekstraksi: redact -> LLM -> validasi skema (+retry) -> verifikasi evidence."""

import json
from dataclasses import dataclass, field

from pydantic import ValidationError

from app.domain.redaction import redact
from app.domain.status import Status
from app.domain.verification import Verdict, verify_quote
from app.llm.base import LLMClient
from app.schemas.extraction import ExtractedElementIn, ExtractionPayload

_PROMPT = (
    "Ekstrak elemen riset dari teks berikut sebagai JSON "
    '{{"elements":[{{"element_type","content","quote","page","confidence"}}]}}. '
    "`quote` harus salinan persis dari teks. Jangan mengarang.\n\n{body}"
)


@dataclass(frozen=True)
class VerifiedElement:
    element: ExtractedElementIn
    status: Status
    verdict: Verdict
    score: float


@dataclass
class ExtractionReport:
    elements: list[VerifiedElement] = field(default_factory=list)
    attempts: int = 0
    schema_failed: bool = False  # semua percobaan invalid -> serahkan ke konfirmasi manual

    @property
    def verified_ratio(self) -> float:
        if not self.elements:
            return 0.0
        return sum(e.verdict is Verdict.VERIFIED for e in self.elements) / len(self.elements)


def extract_elements(
    llm: LLMClient, pages: dict[int, str], max_attempts: int = 3
) -> ExtractionReport:
    # LLM hanya melihat teks yang sudah diredaksi; verifikasi juga terhadap teks itu.
    safe_pages = {n: redact(t) for n, t in pages.items()}
    body = "\n\n".join(f"[halaman {n}]\n{t}" for n, t in sorted(safe_pages.items()))
    report = ExtractionReport()

    payload: ExtractionPayload | None = None
    for _ in range(max_attempts):
        report.attempts += 1
        try:
            payload = ExtractionPayload.model_validate(
                json.loads(llm.complete_json(_PROMPT.format(body=body)))
            )
            break
        except (json.JSONDecodeError, ValidationError):
            continue

    if payload is None:
        report.schema_failed = True
        return report

    for el in payload.elements:
        v = verify_quote(el.quote, el.page, safe_pages)
        report.elements.append(VerifiedElement(el, v.status(), v.verdict, v.score))
    return report
