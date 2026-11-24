from datetime import UTC, datetime

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


def _utcnow() -> datetime:
    return datetime.now(UTC)


class FindingRow(Base):
    __tablename__ = "findings"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    rule_id: Mapped[str] = mapped_column(String)
    priority: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String)
    why_flagged: Mapped[str] = mapped_column(Text)
    suggested_clarification: Mapped[str] = mapped_column(Text)
    confidence: Mapped[float]
    status: Mapped[str] = mapped_column(String)
    ai_generated: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=_utcnow)

    evidence: Mapped[list["EvidenceRow"]] = relationship(
        back_populates="finding", cascade="all, delete-orphan"
    )


class EvidenceRow(Base):
    __tablename__ = "finding_evidence"

    id: Mapped[int] = mapped_column(primary_key=True)
    finding_id: Mapped[str] = mapped_column(ForeignKey("findings.id", ondelete="CASCADE"))
    element: Mapped[str] = mapped_column(String)
    document: Mapped[str] = mapped_column(String)
    page: Mapped[int]

    finding: Mapped[FindingRow] = relationship(back_populates="evidence")


class AuditLog(Base):
    """Append-only: setiap perubahan status menulis satu baris (FR-121)."""

    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(primary_key=True)
    actor_id: Mapped[str] = mapped_column(String)
    action: Mapped[str] = mapped_column(String)
    entity: Mapped[str] = mapped_column(String)
    entity_id: Mapped[str] = mapped_column(String)
    at: Mapped[datetime]
    meta_json: Mapped[str] = mapped_column(Text, default="{}")
