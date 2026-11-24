"""Elemen per versi, cek aturan, diff antarversi, status komentar, dan Supervision Brief."""

import json
import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

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
)
from app.domain import brief as brief_mod
from app.domain.comments import CommentStatus, comment_statuses
from app.domain.diff import ElementDiff, diff_elements
from app.domain.graph import Graph, build_graph
from app.domain.impact import change_impact
from app.domain.rules import Element, Rule, run
from app.domain.status import Status
from app.domain.verification import verify_quote
from app.services import audit
from app.services.documents import ProjectNotFound
from app.services.rules import load_rules

UNREVIEWED = {Status.AI_SUGGESTED.value, Status.NEEDS_USER_CONFIRMATION.value}


class VersionNotFound(LookupError):
    pass


def _now() -> datetime:
    return datetime.now(UTC)


def get_version(session: Session, version_id: str) -> DocumentVersion:
    v = session.get(DocumentVersion, version_id)
    if v is None:
        raise VersionNotFound(version_id)
    return v


def parsed(version: DocumentVersion) -> dict[str, Any]:
    return json.loads(version.parsed_json)


def pages(version: DocumentVersion) -> dict[int, str]:
    return {int(k): v for k, v in parsed(version).get("pages", {}).items()}


# ---- Elemen ----------------------------------------------------------------------------------


def add_element(
    session: Session,
    version_id: str,
    type_: str,
    content: str,
    quote: str,
    page: int,
    source: str = "student",
) -> ElementRow:
    """Elemen masuk (dari mahasiswa atau ekstraksi) selalu diverifikasi terhadap halaman sumber."""
    version = get_version(session, version_id)
    check = verify_quote(quote, page, pages(version))
    if source == "student":
        status = Status.STUDENT_CONFIRMED if check.ok else Status.NEEDS_USER_CONFIRMATION
    else:
        status = check.status()
    row = ElementRow(
        id=str(uuid.uuid4()),
        version_id=version.id,
        type=type_,
        content=content,
        quote=quote,
        page=page,
        verified=check.ok,
        source=source,
        status=status.value,
    )
    session.add(row)
    audit.record(session, source, "element_added", "element", row.id, {"verified": check.ok})
    session.commit()
    return row


def list_elements(session: Session, version_id: str) -> list[ElementRow]:
    get_version(session, version_id)
    return list(
        session.scalars(
            select(ElementRow)
            .where(ElementRow.version_id == version_id)
            .order_by(ElementRow.created_at)
        )
    )


def _domain_elements(rows: list[ElementRow]) -> list[Element]:
    return [
        Element(id=r.id, type=r.type, content=r.content, page=r.page, verified=r.verified)
        for r in rows
        if r.status != Status.REJECTED.value
    ]


# ---- Cek aturan ------------------------------------------------------------------------------


def run_check(
    session: Session, version_id: str, rules: list[Rule] | None = None
) -> list[FindingRow]:
    """Jalankan aturan pada elemen versi ini. Temuan yang sudah ditinjau manusia dipertahankan."""
    version = get_version(session, version_id)
    project = version.document.project
    rows = list_elements(session, version_id)
    by_id = {r.id: r for r in rows}

    # Hapus evidence dulu secara eksplisit: bulk delete tidak memicu cascade ORM, dan cascade FK
    # SQLite hanya aktif bila PRAGMA foreign_keys menyala. Tanpa ini evidence tertinggal yatim.
    stale = select(FindingRow.id).where(
        FindingRow.version_id == version_id, FindingRow.status.in_(UNREVIEWED)
    )
    session.execute(delete(EvidenceRow).where(EvidenceRow.finding_id.in_(stale)))
    session.execute(
        delete(FindingRow).where(
            FindingRow.version_id == version_id, FindingRow.status.in_(UNREVIEWED)
        )
    )
    # Satu aturan bisa menghasilkan beberapa temuan (mis. tiap bagian wajib yang hilang),
    # jadi kunci "sudah ditinjau" = aturan + alasan, bukan aturan saja.
    reviewed = {
        (f.rule_id, f.why_flagged)
        for f in session.scalars(select(FindingRow).where(FindingRow.version_id == version_id))
    }
    page_texts = pages(version)
    text = "\n".join(page_texts.values())
    elements = _domain_elements(rows)
    for rf in run(rules or load_rules(), elements, project.program, text, page_texts):
        if (rf.rule_id, rf.why_flagged) in reviewed:
            continue
        evidence = [by_id[e.element] for e in rf.evidence if e.element in by_id]
        # Evidence bagian dokumen (mis. "section:Hasil dan Pembahasan"): teks bagian itu sendiri.
        sections = [e for e in rf.evidence if e.element.startswith("section:")]
        verified = sum(e.verified for e in evidence) + len(sections)
        total = len(evidence) + len(sections)
        session.add(
            FindingRow(
                id=f"F-{uuid.uuid4().hex[:8]}",
                project_id=project.id,
                version_id=version.id,
                rule_id=rf.rule_id,
                priority=rf.priority,
                title=rf.title,
                why_flagged=rf.why_flagged,
                suggested_clarification=rf.suggested_clarification,
                # Bukan "keyakinan AI": proporsi evidence yang kutipannya terverifikasi.
                confidence=verified / total if total else 0.0,
                status=rf.status.value,
                ai_generated=any(e.source == "ai" for e in evidence),
                evidence=[
                    EvidenceRow(
                        element_id=e.id,
                        element=brief_mod.TYPE_LABEL.get(e.type, e.type),
                        document=f"v{version.version_no}",
                        page=e.page,
                    )
                    for e in evidence
                ]
                + [
                    EvidenceRow(
                        element=e.element.removeprefix("section:"),
                        document=f"v{version.version_no}",
                        page=e.page,
                    )
                    for e in sections
                ],
            )
        )
    session.commit()
    return list_findings(session, version_id)


def list_findings(session: Session, version_id: str) -> list[FindingRow]:
    return list(
        session.scalars(
            select(FindingRow)
            .where(FindingRow.version_id == version_id)
            .order_by(FindingRow.created_at)
        )
    )


# ---- Versi, diff, komentar, brief ------------------------------------------------------------


def project_versions(session: Session, project_id: str) -> tuple[Project, list[DocumentVersion]]:
    project = session.get(Project, project_id)
    if project is None:
        raise ProjectNotFound(project_id)
    versions = list(
        session.scalars(
            select(DocumentVersion)
            .join(Document)
            .where(Document.project_id == project_id)
            .order_by(DocumentVersion.version_no)
        )
    )
    if not versions:
        raise VersionNotFound(f"proyek {project_id} belum punya versi")
    return project, versions


def latest_diff(session: Session, project_id: str) -> tuple[int | None, int, ElementDiff | None]:
    _, versions = project_versions(session, project_id)
    if len(versions) < 2:
        return None, versions[-1].version_no, None
    prev, last = versions[-2], versions[-1]
    old = _domain_elements(list_elements(session, prev.id))
    new = _domain_elements(list_elements(session, last.id))
    return prev.version_no, last.version_no, diff_elements(old, new)


def latest_comments(session: Session, project_id: str) -> list[CommentStatus]:
    """Komentar di versi sebelumnya vs teks versi terbaru (hanya bila keduanya DOCX)."""
    _, versions = project_versions(session, project_id)
    if len(versions) < 2:
        return []
    prev, last = parsed(versions[-2]), parsed(versions[-1])
    if prev.get("kind") != "docx" or last.get("kind") != "docx":
        return []
    reviews = {
        r.comment_id: r.addressed
        for r in session.scalars(
            select(CommentReview).where(CommentReview.version_id == versions[-2].id)
        )
    }
    return comment_statuses(prev["blocks"], prev["comments"], last["blocks"], reviews)


def review_comment(
    session: Session,
    version_id: str,
    comment_id: str,
    addressed: bool,
    now: Callable[[], datetime] = _now,
) -> CommentReview:
    get_version(session, version_id)
    row = session.scalars(
        select(CommentReview).where(
            CommentReview.version_id == version_id, CommentReview.comment_id == comment_id
        )
    ).first()
    if row is None:
        row = CommentReview(
            version_id=version_id, comment_id=comment_id, addressed=addressed, at=now()
        )
        session.add(row)
    else:
        row.addressed, row.at = addressed, now()
    session.commit()
    return row


def build_brief(
    session: Session, project_id: str, now: Callable[[], datetime] = _now
) -> brief_mod.Brief:
    project, versions = project_versions(session, project_id)
    from_v, to_v, diff = latest_diff(session, project_id)
    impacts = (
        change_impact(diff, _domain_elements(list_elements(session, versions[-1].id)))
        if diff
        else []
    )
    findings = [
        brief_mod.BriefFinding(f.id, f.rule_id, f.title, f.priority, f.status)
        for f in list_findings(session, versions[-1].id)
    ]
    previous_rules = (
        {
            f.rule_id
            for f in list_findings(session, versions[-2].id)
            if f.status != Status.REJECTED.value
        }
        if len(versions) > 1
        else set()
    )
    return brief_mod.build_brief(
        project_title=project.title,
        program=project.program,
        from_version=from_v,
        to_version=to_v,
        generated_at=now(),
        diff=diff,
        comments=latest_comments(session, project_id),
        findings=findings,
        previous_rules=previous_rules,
        impacts=impacts,
    )


def version_graph(session: Session, version_id: str) -> tuple[Graph, list[ElementRow]]:
    rows = list_elements(session, version_id)
    return build_graph(_domain_elements(rows)), rows
