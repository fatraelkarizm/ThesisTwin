"""Invarian evidence: finding/node wajib punya sumber, atau berstatus needs_user_confirmation."""

from dataclasses import dataclass

from app.domain.status import Status


@dataclass(frozen=True)
class EvidenceRef:
    element: str
    document: str
    page: int


class MissingEvidence(ValueError):
    pass


def require_evidence(evidence: list[EvidenceRef], status: Status) -> None:
    if not evidence and status is not Status.NEEDS_USER_CONFIRMATION:
        raise MissingEvidence("Tanpa evidence, status harus needs_user_confirmation")
