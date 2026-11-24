"""Tautan untuk dosen tanpa akun (Langkah 21; abstrak: "supervisors never need an account").

Token acak 256-bit hanya ditampilkan sekali; database menyimpan SHA-256-nya. Tautan kedaluwarsa
dan bisa dicabut. Keputusan dosen lewat tautan dicatat di audit log dengan id tautan.
"""

import hashlib
import secrets
import uuid
from collections.abc import Callable
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import FindingRow, Project, ShareLink
from app.domain.status import Role, Status
from app.services import audit
from app.services.documents import ProjectNotFound
from app.services.findings import FindingNotFound, change_status

DEFAULT_DAYS = 14


class LinkInvalid(LookupError):
    """Token salah, kedaluwarsa, atau dicabut. Sengaja satu jenis error agar tidak bocor info."""


def _now() -> datetime:
    return datetime.now(UTC)


def _hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def _aware(dt: datetime) -> datetime:
    return dt if dt.tzinfo else dt.replace(tzinfo=UTC)  # SQLite membuang zona waktu


def create_link(
    session: Session,
    project_id: str,
    days: int = DEFAULT_DAYS,
    now: Callable[[], datetime] = _now,
) -> tuple[ShareLink, str]:
    if session.get(Project, project_id) is None:
        raise ProjectNotFound(project_id)
    token = secrets.token_urlsafe(32)
    created = now()
    link = ShareLink(
        id=str(uuid.uuid4()),
        project_id=project_id,
        token_sha256=_hash(token),
        created_at=created,
        expires_at=created + timedelta(days=days),
    )
    session.add(link)
    audit.record(session, "mahasiswa", "share_created", "share_link", link.id, at=created)
    session.commit()
    return link, token


def resolve(session: Session, token: str, now: Callable[[], datetime] = _now) -> ShareLink:
    link = session.scalars(select(ShareLink).where(ShareLink.token_sha256 == _hash(token))).first()
    if link is None or link.revoked or _aware(link.expires_at) <= now():
        raise LinkInvalid()
    return link


def revoke(session: Session, token: str) -> None:
    link = resolve(session, token)
    link.revoked = True
    session.commit()


def supervisor_decide(
    session: Session,
    token: str,
    finding_id: str,
    confirm: bool,
    now: Callable[[], datetime] = _now,
) -> FindingRow:
    link = resolve(session, token, now)
    finding = session.get(FindingRow, finding_id)
    if finding is None or finding.project_id != link.project_id:
        raise FindingNotFound(finding_id)  # tautan proyek A tidak boleh menyentuh proyek B
    target = Status.SUPERVISOR_CONFIRMED if confirm else Status.REJECTED
    return change_status(session, finding_id, target, f"dosen-link:{link.id}", Role.SUPERVISOR, now)
