from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.domain.brief import Brief, render_text
from app.domain.comments import CommentStatus
from app.domain.status import Role, Status
from app.schemas.review import (
    AnswerIn,
    CommentReviewIn,
    ElementIn,
    ElementOut,
    FindingOut,
    GraphEdge,
    GraphGap,
    GraphOut,
    ShareOut,
    StatusIn,
    StressQuestionOut,
)
from app.services import review as svc
from app.services import share
from app.services import stress as stress_svc
from app.services.findings import change_status
from app.services.rules import rule_meta

router = APIRouter(tags=["review"])


def _finding_out(row) -> FindingOut:
    out = FindingOut.model_validate(row)
    rule = rule_meta().get(out.rule_id)
    if rule:
        out.basis, out.references = rule.basis, rule.references
        out.source_types, out.directions = list(rule.source_types), rule.directions
    return out


SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/versions/{version_id}/elements", status_code=status.HTTP_201_CREATED)
def add_element(version_id: str, body: ElementIn, session: SessionDep) -> ElementOut:
    row = svc.add_element(session, version_id, body.type, body.content, body.quote, body.page)
    return ElementOut.model_validate(row)


@router.get("/versions/{version_id}/elements")
def list_elements(version_id: str, session: SessionDep) -> list[ElementOut]:
    return [ElementOut.model_validate(r) for r in svc.list_elements(session, version_id)]


@router.get("/versions/{version_id}/graph")
def graph(version_id: str, session: SessionDep) -> GraphOut:
    g, rows = svc.version_graph(session, version_id)
    by_id = {r.id: r for r in rows}
    return GraphOut(
        nodes=[ElementOut.model_validate(by_id[n.id]) for n in g.nodes],
        edges=[GraphEdge(src=e.src, dst=e.dst, type=e.type) for e in g.edges],
        gaps=[
            GraphGap(from_type=x.from_type, to_type=x.to_type, relation=x.relation) for x in g.gaps
        ],
    )


@router.post("/versions/{version_id}/check")
def run_check(version_id: str, session: SessionDep) -> list[FindingOut]:
    return [_finding_out(f) for f in svc.run_check(session, version_id)]


@router.get("/versions/{version_id}/findings")
def list_findings(version_id: str, session: SessionDep) -> list[FindingOut]:
    svc.get_version(session, version_id)
    return [_finding_out(f) for f in svc.list_findings(session, version_id)]


@router.post("/findings/{finding_id}/status")
def student_status(finding_id: str, body: StatusIn, session: SessionDep) -> FindingOut:
    row = change_status(session, finding_id, Status(body.target), "mahasiswa", Role.STUDENT)
    return _finding_out(row)


@router.post("/versions/{version_id}/comments/{comment_id}")
def review_comment(
    version_id: str, comment_id: str, body: CommentReviewIn, session: SessionDep
) -> dict[str, bool]:
    svc.review_comment(session, version_id, comment_id, body.addressed)
    return {"addressed": body.addressed}


@router.get("/projects/{project_id}/comments")
def comments(project_id: str, session: SessionDep) -> list[CommentStatus]:
    return svc.latest_comments(session, project_id)


@router.get("/projects/{project_id}/brief")
def brief(project_id: str, session: SessionDep) -> Brief:
    return svc.build_brief(session, project_id)


@router.get("/projects/{project_id}/brief.txt", response_class=PlainTextResponse)
def brief_text(project_id: str, session: SessionDep) -> str:
    return render_text(svc.build_brief(session, project_id))


@router.post("/projects/{project_id}/share", status_code=status.HTTP_201_CREATED)
def create_share(project_id: str, session: SessionDep) -> ShareOut:
    link, token = share.create_link(session, project_id)
    return ShareOut(token=token, path=f"/dosen/{token}", expires_at=link.expires_at)


@router.post("/versions/{version_id}/stress-test")
def stress_test(
    version_id: str, session: SessionDep, regenerate: bool = False
) -> list[StressQuestionOut]:
    rows = stress_svc.generate(session, version_id, regenerate)
    return [StressQuestionOut.model_validate(q) for q in rows]


@router.get("/versions/{version_id}/stress-test")
def get_stress_test(version_id: str, session: SessionDep) -> list[StressQuestionOut]:
    return [
        StressQuestionOut.model_validate(q) for q in stress_svc.list_questions(session, version_id)
    ]


@router.post("/stress-questions/{question_id}/answer")
def answer(question_id: str, body: AnswerIn, session: SessionDep) -> StressQuestionOut:
    return StressQuestionOut.model_validate(stress_svc.answer(session, question_id, body.answer))
