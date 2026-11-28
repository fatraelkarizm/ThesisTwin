"""Defense Stress-Test: buat pertanyaan per versi, simpan justifikasi mahasiswa, rating dosen."""

import json
import uuid
from collections.abc import Callable
from datetime import UTC, datetime

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db.models import AuditLog, StressQuestionRow
from app.domain.stress import FindingRef, stress_questions
from app.services import config, review
from app.services.rules import rule_meta


class QuestionNotFound(LookupError):
    pass


class InvalidRating(ValueError):
    pass


def _now() -> datetime:
    return datetime.now(UTC)


def list_questions(session: Session, version_id: str) -> list[StressQuestionRow]:
    review.get_version(session, version_id)
    return list(
        session.scalars(
            select(StressQuestionRow)
            .where(StressQuestionRow.version_id == version_id)
            .order_by(StressQuestionRow.position)
        )
    )


def generate(
    session: Session, version_id: str, regenerate: bool = False
) -> list[StressQuestionRow]:
    """Idempoten: bila sudah ada, kembalikan yang ada. `regenerate` hanya membuang pertanyaan yang
    belum dijawab dan belum dinilai, sehingga jawaban dan rating tidak pernah hilang."""
    existing = list_questions(session, version_id)
    if existing and not regenerate:
        return existing
    session.execute(
        delete(StressQuestionRow).where(
            StressQuestionRow.version_id == version_id,
            StressQuestionRow.answer.is_(None),
            StressQuestionRow.rating.is_(None),
        )
    )
    kept = {q.key for q in list_questions(session, version_id)}
    graph, _ = review.version_graph(session, version_id)
    refs = [
        FindingRef(
            f.rule_id, f.priority, f.status, [e.element_id for e in f.evidence if e.element_id]
        )
        for f in review.list_findings(session, version_id)
    ]
    position = len(kept)
    questions = {r.id: r.defense_question for r in rule_meta().values() if r.defense_question}
    for q in stress_questions(graph, refs, config.ontology(), questions):
        if q.key in kept:
            continue
        session.add(
            StressQuestionRow(
                id=str(uuid.uuid4()),
                version_id=version_id,
                position=position,
                key=q.key,
                kind=q.kind,
                text=q.text,
                reason=q.reason,
                element_ids_json=json.dumps(list(q.element_ids)),
            )
        )
        position += 1
    session.commit()
    return list_questions(session, version_id)


def answer(
    session: Session, question_id: str, text: str, now: Callable[[], datetime] = _now
) -> StressQuestionRow:
    q = session.get(StressQuestionRow, question_id)
    if q is None:
        raise QuestionNotFound(question_id)
    q.answer, q.answered_at = text, now()
    session.add(_audit("mahasiswa", "stress_answer", q.id, {}, now))
    session.commit()
    return q


def rate(
    session: Session,
    question_id: str,
    score: int,
    project_id: str,
    actor: str,
    now: Callable[[], datetime] = _now,
) -> StressQuestionRow:
    if not 1 <= score <= 5:
        raise InvalidRating(score)
    q = session.get(StressQuestionRow, question_id)
    if q is None or review.get_version(session, q.version_id).document.project_id != project_id:
        raise QuestionNotFound(question_id)  # tautan proyek A tidak boleh menilai proyek B
    q.rating, q.rated_at = score, now()
    session.add(_audit(actor, "stress_rating", q.id, {"score": score}, now))
    session.commit()
    return q


def latest_for_project(session: Session, project_id: str) -> list[StressQuestionRow]:
    _, versions = review.project_versions(session, project_id)
    return list_questions(session, versions[-1].id)


def _audit(actor: str, action: str, entity_id: str, meta: dict, now) -> AuditLog:
    return AuditLog(
        actor_id=actor,
        action=action,
        entity="stress_question",
        entity_id=entity_id,
        at=now(),
        meta_json=json.dumps(meta),
    )
