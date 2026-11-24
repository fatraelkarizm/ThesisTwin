"""Hapus permanen proyek (FR-122) dan kelola tautan dosen."""

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db.models import (
    CommentReview,
    Document,
    DocumentVersion,
    ElementRow,
    EvidenceRow,
    FindingRow,
    Project,
    ShareLink,
    StressQuestionRow,
)
from app.services import audit
from app.services.documents import ProjectNotFound
from app.storage import LocalStorage


class LinkNotFound(LookupError):
    pass


def delete_project(session: Session, storage: LocalStorage, project_id: str) -> None:
    """Menghapus semua data proyek: dokumen, versi, file, elemen, temuan, pertanyaan, tautan.

    Yang tersisa hanya satu baris audit "project_deleted" berisi id proyek (tanpa isi).
    """
    project = session.get(Project, project_id)
    if project is None:
        raise ProjectNotFound(project_id)
    # Hapus eksplisit, tidak bergantung pada PRAGMA foreign_keys SQLite (mudah terlewat di
    # koneksi lain): data penelitian tidak boleh tertinggal.
    version_ids = list(
        session.scalars(
            select(DocumentVersion.id).join(Document).where(Document.project_id == project_id)
        )
    )
    finding_ids = select(FindingRow.id).where(FindingRow.project_id == project_id)
    session.execute(delete(EvidenceRow).where(EvidenceRow.finding_id.in_(finding_ids)))
    session.execute(delete(FindingRow).where(FindingRow.project_id == project_id))
    for table in (ElementRow, StressQuestionRow, CommentReview):
        session.execute(delete(table).where(table.version_id.in_(version_ids)))
    session.execute(delete(ShareLink).where(ShareLink.project_id == project_id))
    session.delete(project)  # ORM cascade: documents -> versions
    audit.record(session, "mahasiswa", "project_deleted", "project", project_id)
    session.commit()
    storage.delete_prefix(project_id)


def list_links(session: Session, project_id: str) -> list[ShareLink]:
    if session.get(Project, project_id) is None:
        raise ProjectNotFound(project_id)
    return list(
        session.scalars(
            select(ShareLink)
            .where(ShareLink.project_id == project_id)
            .order_by(ShareLink.created_at.desc())
        )
    )


def revoke_link(session: Session, project_id: str, link_id: str) -> ShareLink:
    link = session.get(ShareLink, link_id)
    if link is None or link.project_id != project_id:
        raise LinkNotFound(link_id)
    link.revoked = True
    audit.record(session, "mahasiswa", "share_revoked", "share_link", link_id)
    session.commit()
    return link
