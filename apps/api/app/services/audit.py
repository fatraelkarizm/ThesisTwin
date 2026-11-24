"""Satu cara menulis audit log (FR-121). Meta berisi id dan angka, bukan isi penelitian."""

import json
from datetime import UTC, datetime
from typing import Any

from sqlalchemy.orm import Session

from app.db.models import AuditLog


def record(
    session: Session,
    actor: str,
    action: str,
    entity: str,
    entity_id: str,
    meta: dict[str, Any] | None = None,
    at: datetime | None = None,
) -> None:
    """Menambahkan baris audit ke sesi; commit dilakukan pemanggil bersama perubahannya."""
    session.add(
        AuditLog(
            actor_id=actor,
            action=action,
            entity=entity,
            entity_id=entity_id,
            at=at or datetime.now(UTC),
            meta_json=json.dumps(meta or {}),
        )
    )
