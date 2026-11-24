from typing import Literal

from pydantic import BaseModel, Field, model_validator

from app.domain.status import Status


class EvidenceOut(BaseModel):
    element: str
    document: str
    page: int = Field(ge=1)


class FindingOut(BaseModel):
    id: str
    rule_id: str
    priority: Literal["high", "medium", "low"]
    title: str
    why_flagged: str
    suggested_clarification: str
    evidence: list[EvidenceOut]
    confidence: float = Field(ge=0, le=1)
    status: Status
    ai_generated: Literal[True] = True

    @model_validator(mode="after")
    def _evidence_or_needs_confirmation(self) -> "FindingOut":
        if not self.evidence and self.status is not Status.NEEDS_USER_CONFIRMATION:
            raise ValueError("finding tanpa evidence harus needs_user_confirmation")
        return self
