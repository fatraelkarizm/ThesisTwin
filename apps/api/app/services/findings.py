import json
from collections.abc import Callable
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.db.models import AuditLog, EvidenceRow, FindingRow
from app.domain.evidence import EvidenceRef, require_evidence
from app.domain.status import Role, Status, transition
from app.schemas.finding import FindingOut


class FindingNotFound(LookupError):
    pass


def _now() -> datetime:
    return datetime.now(UTC)


def create_finding(session: Session, data: FindingOut) -> FindingRow:
    require_evidence(
        [EvidenceRef(e.element, e.document, e.page) for e in data.evidence], data.status
    )
    row = FindingRow(
        id=data.id,
        rule_id=data.rule_id,
        priority=data.priority,
        title=data.title,
        why_flagged=data.why_flagged,
        suggested_clarification=data.suggested_clarification,
        confidence=data.confidence,
        status=data.status.value,
        ai_generated=True,
        evidence=[
            EvidenceRow(element=e.element, document=e.document, page=e.page) for e in data.evidence
        ],
    )
    session.add(row)
    session.commit()
    return row


def change_status(
    session: Session,
    finding_id: str,
    target: Status,
    actor_id: str,
    actor_role: Role,
    now: Callable[[], datetime] = _now,
) -> FindingRow:
    """Satu-satunya jalur mengubah status; selalu lewat state machine + audit log."""
    row = session.get(FindingRow, finding_id)
    if row is None:
        raise FindingNotFound(finding_id)
    previous = Status(row.status)
    row.status = transition(previous, target, actor_role).value
    session.add(
        AuditLog(
            actor_id=actor_id,
            action="status_change",
            entity="finding",
            entity_id=finding_id,
            at=now(),
            meta_json=json.dumps(
                {"from": previous.value, "to": target.value, "role": actor_role.value}
            ),
        )
    )
    session.commit()
    return row
