from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

ElementType = Literal[
    "research_question",
    "objective",
    "variable",
    "population",
    "method",
    "instrument",
    "analysis",
    "claim",
    "limitation",
]


class ElementIn(BaseModel):
    type: ElementType
    content: str = Field(min_length=1, max_length=2000)
    quote: str = Field(min_length=1, max_length=2000)
    page: int = Field(ge=1)


class ElementOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    type: str
    content: str
    quote: str
    page: int
    verified: bool
    source: str
    status: str


class EvidenceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    element: str
    document: str
    page: int


class FindingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    rule_id: str
    priority: str
    title: str
    why_flagged: str
    suggested_clarification: str
    confidence: float
    status: str
    ai_generated: bool
    evidence: list[EvidenceOut]


class StatusIn(BaseModel):
    target: Literal["student_confirmed", "rejected", "resolved"]


class CommentReviewIn(BaseModel):
    addressed: bool


class DecisionIn(BaseModel):
    confirm: bool


class ShareOut(BaseModel):
    token: str
    path: str
    expires_at: datetime

    @field_validator("expires_at")
    @classmethod
    def _utc(cls, v: datetime) -> datetime:
        return v if v.tzinfo else v.replace(tzinfo=UTC)


class GraphEdge(BaseModel):
    src: str
    dst: str
    type: str


class GraphGap(BaseModel):
    from_type: str
    to_type: str
    relation: str


class GraphOut(BaseModel):
    nodes: list[ElementOut]
    edges: list[GraphEdge]
    gaps: list[GraphGap]


class StressQuestionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    position: int
    kind: str
    text: str
    reason: str
    answer: str | None
    rating: int | None


class AnswerIn(BaseModel):
    answer: str = Field(min_length=1, max_length=4000)


class RatingIn(BaseModel):
    score: int = Field(ge=1, le=5)
