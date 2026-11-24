import json
from datetime import UTC, datetime

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import AuditLog, FindingRow
from app.db.session import init_db, make_engine
from app.domain.status import InvalidTransition, Role, Status
from app.schemas.finding import EvidenceOut, FindingOut
from app.services.findings import FindingNotFound, change_status, create_finding

FIXED = datetime(2026, 11, 24, tzinfo=UTC)


@pytest.fixture
def session():
    engine = make_engine("sqlite://")
    init_db(engine)
    with Session(engine) as s:
        yield s


def _finding(**over) -> FindingOut:
    base = dict(
        id="F-001",
        rule_id="R-CAUSAL-01",
        priority="high",
        title="t",
        why_flagged="w",
        suggested_clarification="s",
        confidence=0.8,
        status=Status.AI_SUGGESTED,
        evidence=[EvidenceOut(element="RQ1", document="proposal_v3", page=5)],
    )
    return FindingOut(**{**base, **over})


def test_create_and_confirm_writes_audit_log(session):
    create_finding(session, _finding())
    row = change_status(
        session, "F-001", Status.STUDENT_CONFIRMED, "u1", Role.STUDENT, now=lambda: FIXED
    )
    assert row.status == "student_confirmed"
    log = session.scalars(select(AuditLog)).one()
    assert (log.actor_id, log.entity_id, log.at) == ("u1", "F-001", FIXED.replace(tzinfo=None))
    assert json.loads(log.meta_json)["to"] == "student_confirmed"


def test_invalid_transition_leaves_status_and_log_untouched(session):
    create_finding(session, _finding())
    with pytest.raises(InvalidTransition):
        change_status(session, "F-001", Status.SUPERVISOR_CONFIRMED, "u1", Role.STUDENT)
    session.rollback()
    assert session.scalars(select(AuditLog)).all() == []


def test_unknown_finding(session):
    with pytest.raises(FindingNotFound):
        change_status(session, "nope", Status.REJECTED, "u1", Role.STUDENT)


def test_finding_without_evidence_persists_only_as_needs_confirmation(session):
    create_finding(session, _finding(status=Status.NEEDS_USER_CONFIRMATION, evidence=[]))
    assert session.get(FindingRow, "F-001").status == "needs_user_confirmation"
