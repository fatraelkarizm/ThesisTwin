from datetime import UTC, datetime

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


def _utcnow() -> datetime:
    return datetime.now(UTC)


class FindingRow(Base):
    __tablename__ = "findings"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    # Nullable: temuan lama (sebelum per-versi) tidak punya proyek/versi.
    project_id: Mapped[str | None] = mapped_column(String, default=None, index=True)
    version_id: Mapped[str | None] = mapped_column(String, default=None, index=True)
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


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    program: Mapped[str] = mapped_column(String)  # rule set prodi, mis. "matematika"
    consent_at: Mapped[datetime | None] = mapped_column(default=None)
    created_at: Mapped[datetime] = mapped_column(default=_utcnow)

    documents: Mapped[list["Document"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    kind: Mapped[str] = mapped_column(String, default="proposal")
    created_at: Mapped[datetime] = mapped_column(default=_utcnow)

    project: Mapped[Project] = relationship(back_populates="documents")
    versions: Mapped[list["DocumentVersion"]] = relationship(
        back_populates="document",
        cascade="all, delete-orphan",
        order_by="DocumentVersion.version_no",
    )


class DocumentVersion(Base):
    """Append-only (AGENTS.md §3.7): tidak ditimpa; dihapus hanya lewat hapus permanen."""

    __tablename__ = "document_versions"
    __table_args__ = (UniqueConstraint("document_id", "version_no"),)

    id: Mapped[str] = mapped_column(String, primary_key=True)
    document_id: Mapped[str] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"))
    version_no: Mapped[int]
    filename: Mapped[str] = mapped_column(String)
    media_type: Mapped[str] = mapped_column(String)
    sha256: Mapped[str] = mapped_column(String(64))
    storage_key: Mapped[str] = mapped_column(String)
    parsed_json: Mapped[str] = mapped_column(Text, default="{}")
    uploaded_at: Mapped[datetime]

    document: Mapped[Document] = relationship(back_populates="versions")


class ElementRow(Base):
    """Elemen penelitian per versi (RQ, tujuan, metode, ...). Sumber: AI atau mahasiswa."""

    __tablename__ = "elements"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    version_id: Mapped[str] = mapped_column(
        ForeignKey("document_versions.id", ondelete="CASCADE"), index=True
    )
    type: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(Text)
    quote: Mapped[str] = mapped_column(Text)
    page: Mapped[int]
    verified: Mapped[bool]  # kutipan cocok dengan teks halaman/bagian
    source: Mapped[str] = mapped_column(String)  # ai | student
    status: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(default=_utcnow)


class CommentReview(Base):
    """Konfirmasi mahasiswa: apakah komentar dosen di versi lama sudah ditindaklanjuti."""

    __tablename__ = "comment_reviews"
    __table_args__ = (UniqueConstraint("version_id", "comment_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    version_id: Mapped[str] = mapped_column(ForeignKey("document_versions.id", ondelete="CASCADE"))
    comment_id: Mapped[str] = mapped_column(String)
    addressed: Mapped[bool]
    at: Mapped[datetime]


class ShareLink(Base):
    """Tautan untuk dosen tanpa akun (abstrak §2). Hanya hash token yang disimpan."""

    __tablename__ = "share_links"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    token_sha256: Mapped[str] = mapped_column(String(64), unique=True)
    created_at: Mapped[datetime]
    expires_at: Mapped[datetime]
    revoked: Mapped[bool] = mapped_column(default=False)


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
