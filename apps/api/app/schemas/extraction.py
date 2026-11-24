from typing import Literal

from pydantic import BaseModel, Field

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


class ExtractedElementIn(BaseModel):
    """Kontrak output LLM. `quote` wajib agar evidence bisa diverifikasi."""

    element_type: ElementType
    content: str = Field(min_length=1)
    quote: str = Field(min_length=1)
    page: int = Field(ge=1)
    confidence: float = Field(ge=0, le=1)


class ExtractionPayload(BaseModel):
    elements: list[ExtractedElementIn]
