import hashlib
import json
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from pypdf.errors import PdfReadError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Document, DocumentVersion, Project
from app.parsing.detect import DOCX_MEDIA, PDF_MEDIA, TEX_MEDIA, detect
from app.parsing.docx import DocxError, parse_docx
from app.parsing.pdf import read_pages
from app.parsing.tex import parse_tex
from app.services import audit
from app.storage import LocalStorage


class ProjectNotFound(LookupError):
    pass


class ConsentRequired(PermissionError):
    """Unggahan ditolak sebelum mahasiswa memberi consent (FR-003)."""


@dataclass(frozen=True)
class AddedVersion:
    version: DocumentVersion
    created: bool  # False = isi sama dengan versi terakhir, tidak membuat versi baru


def _now() -> datetime:
    return datetime.now(UTC)


def create_project(session: Session, title: str, program: str) -> Project:
    project = Project(id=str(uuid.uuid4()), title=title, program=program)
    session.add(project)
    session.commit()
    return project


def give_consent(session: Session, project_id: str, now: Callable[[], datetime] = _now) -> Project:
    project = _get_project(session, project_id)
    if project.consent_at is None:
        project.consent_at = now()
        session.commit()
    return project


def add_version(
    session: Session,
    storage: LocalStorage,
    project_id: str,
    filename: str,
    media_type: str,
    data: bytes,
    parsed: dict[str, Any],
    now: Callable[[], datetime] = _now,
) -> AddedVersion:
    project = _get_project(session, project_id)
    if project.consent_at is None:
        raise ConsentRequired(project_id)

    document = next((d for d in project.documents if d.kind == "proposal"), None)
    if document is None:
        document = Document(id=str(uuid.uuid4()), project_id=project.id, kind="proposal")
        session.add(document)
        session.flush()

    digest = hashlib.sha256(data).hexdigest()
    latest = session.scalars(
        select(DocumentVersion)
        .where(DocumentVersion.document_id == document.id)
        .order_by(DocumentVersion.version_no.desc())
        .limit(1)
    ).first()
    if latest is not None and latest.sha256 == digest:
        return AddedVersion(latest, created=False)

    version_no = 1 if latest is None else latest.version_no + 1
    version_id = str(uuid.uuid4())
    key = f"{project.id}/{document.id}/v{version_no}-{digest[:12]}"
    storage.save(key, data)
    version = DocumentVersion(
        id=version_id,
        document_id=document.id,
        version_no=version_no,
        filename=filename,
        media_type=media_type,
        sha256=digest,
        storage_key=key,
        parsed_json=json.dumps(parsed, ensure_ascii=False),
        uploaded_at=now(),
    )
    session.add(version)
    audit.record(
        session,
        "mahasiswa",
        "version_uploaded",
        "document_version",
        version_id,
        {"version_no": version_no, "sha256": digest},
    )
    session.commit()
    return AddedVersion(version, created=True)


class UnsupportedFile(ValueError):
    pass


class UnreadableFile(ValueError):
    pass


def ingest_upload(
    session: Session, storage: LocalStorage, project_id: str, filename: str, data: bytes
) -> AddedVersion:
    """Deteksi tipe dari isi file, parse, lalu simpan sebagai versi baru."""
    kind = detect(data)
    try:
        if kind == "pdf":
            pages = read_pages(data)
            parsed: dict[str, Any] = {
                "kind": "pdf",
                "unit": "page",
                "pages": {str(n): t for n, t in pages.items()},
            }
            media = PDF_MEDIA
        elif kind == "docx":
            parsed, media = parse_docx(data), DOCX_MEDIA
        elif kind == "tex":
            parsed, media = parse_tex(data), TEX_MEDIA
        else:
            raise UnsupportedFile(filename)
    except (PdfReadError, DocxError) as exc:
        raise UnreadableFile(filename) from exc
    return add_version(session, storage, project_id, filename, media, data, parsed)


def list_versions(session: Session, project_id: str) -> list[DocumentVersion]:
    _get_project(session, project_id)
    return list(
        session.scalars(
            select(DocumentVersion)
            .join(Document)
            .where(Document.project_id == project_id)
            .order_by(DocumentVersion.version_no)
        )
    )


def get_project(session: Session, project_id: str) -> Project:
    return _get_project(session, project_id)


def _get_project(session: Session, project_id: str) -> Project:
    project = session.get(Project, project_id)
    if project is None:
        raise ProjectNotFound(project_id)
    return project
