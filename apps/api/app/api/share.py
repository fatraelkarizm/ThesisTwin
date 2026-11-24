"""Akses dosen tanpa akun. Semua endpoint di sini hanya butuh token tautan."""

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.domain.brief import Brief, render_text
from app.schemas.review import DecisionIn, FindingOut, RatingIn, StressQuestionOut
from app.services import review as svc
from app.services import share
from app.services import stress as stress_svc

router = APIRouter(prefix="/share", tags=["dosen"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/{token}")
def shared_brief(token: str, session: SessionDep) -> Brief:
    link = share.resolve(session, token)
    return svc.build_brief(session, link.project_id)


@router.get("/{token}/brief.txt", response_class=PlainTextResponse)
def shared_brief_text(token: str, session: SessionDep) -> str:
    link = share.resolve(session, token)
    return render_text(svc.build_brief(session, link.project_id))


@router.post("/{token}/findings/{finding_id}")
def decide(token: str, finding_id: str, body: DecisionIn, session: SessionDep) -> FindingOut:
    return FindingOut.model_validate(
        share.supervisor_decide(session, token, finding_id, body.confirm)
    )


@router.get("/{token}/stress-test")
def shared_stress(token: str, session: SessionDep) -> list[StressQuestionOut]:
    link = share.resolve(session, token)
    rows = stress_svc.latest_for_project(session, link.project_id)
    return [StressQuestionOut.model_validate(q) for q in rows]


@router.post("/{token}/stress-questions/{question_id}/rating")
def rate(token: str, question_id: str, body: RatingIn, session: SessionDep) -> StressQuestionOut:
    link = share.resolve(session, token)
    row = stress_svc.rate(
        session, question_id, body.score, link.project_id, f"dosen-link:{link.id}"
    )
    return StressQuestionOut.model_validate(row)
