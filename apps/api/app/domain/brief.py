"""Supervision Brief satu halaman (Langkah 20; abstrak §4 langkah 3).

Hanya merangkum **state** (perubahan, komentar, temuan, keputusan). Tidak menulis isi penelitian.
Murni: data masuk -> struktur brief -> teks pesan chat.
"""

from dataclasses import dataclass, field
from datetime import datetime

from app.domain.comments import CommentState, CommentStatus
from app.domain.diff import ElementDiff
from app.domain.impact import Impact

TYPE_LABEL = {
    "research_question": "Rumusan masalah",
    "objective": "Tujuan",
    "variable": "Variabel",
    "population": "Populasi",
    "method": "Metode/desain",
    "instrument": "Instrumen",
    "analysis": "Analisis",
    "claim": "Klaim",
    "limitation": "Keterbatasan",
}


@dataclass(frozen=True)
class BriefEvidence:
    element: str  # label elemen, mis. "Rumusan masalah", atau nama bagian dokumen
    page: int


@dataclass(frozen=True)
class BriefFinding:
    id: str
    rule_id: str
    title: str
    priority: str
    status: str
    # Agar dosen bisa memutuskan tanpa membuka dokumen (docs/feedback/supervisor-burden.md §2.1).
    why_flagged: str = ""
    evidence: tuple[BriefEvidence, ...] = ()
    basis: str | None = None
    source_types: tuple[str, ...] = ()


@dataclass
class Brief:
    project_title: str
    program: str
    from_version: int | None
    to_version: int
    generated_at: datetime
    unit: str = "page"  # "page" (PDF) atau "section" (Word/LaTeX): satuan nomor di evidence
    changes: list[str] = field(default_factory=list)
    comments: list[CommentStatus] = field(default_factory=list)
    open_findings: list[BriefFinding] = field(default_factory=list)
    awaiting_supervisor: list[BriefFinding] = field(default_factory=list)
    resolved_rules: list[str] = field(default_factory=list)
    impacts: list[str] = field(default_factory=list)


def _label(t: str) -> str:
    return TYPE_LABEL.get(t, t)


def describe_changes(d: ElementDiff) -> list[str]:
    lines = [f"Diubah — {_label(c.new.type)}: “{c.new.content}”" for c in d.changed]
    lines += [f"Baru — {_label(e.type)}: “{e.content}”" for e in d.added]
    lines += [f"Dihapus — {_label(e.type)}: “{e.content}”" for e in d.removed]
    return lines


def describe_impacts(impacts: list[Impact]) -> list[str]:
    lines = []
    for i in impacts:
        src, dst = _label(i.changed_type), _label(i.affected_type).lower()
        if not i.affected_elements:
            continue  # tidak ada elemen terdampak yang tercatat; celahnya sudah dilaporkan graph
        stale = " — belum berubah sejak versi lalu" if i.stale else ""
        lines.append(f"{src} berubah → cek {dst}: {i.check}{stale}")
    return lines


def build_brief(
    *,
    project_title: str,
    program: str,
    from_version: int | None,
    to_version: int,
    generated_at: datetime,
    diff: ElementDiff | None,
    comments: list[CommentStatus],
    findings: list[BriefFinding],
    previous_rules: set[str],
    impacts: list[Impact] | None = None,
    unit: str = "page",
) -> Brief:
    open_ = [f for f in findings if f.status in {"ai_suggested", "needs_user_confirmation"}]
    awaiting = [f for f in findings if f.status == "student_confirmed"]
    current_rules = {f.rule_id for f in findings if f.status != "rejected"}
    return Brief(
        project_title=project_title,
        program=program,
        from_version=from_version,
        to_version=to_version,
        generated_at=generated_at,
        unit=unit,
        changes=describe_changes(diff) if diff else [],
        comments=comments,
        open_findings=open_,
        awaiting_supervisor=awaiting,
        resolved_rules=sorted(previous_rules - current_rules),
        impacts=describe_impacts(impacts or []),
    )


_STATE_TEXT = {
    CommentState.POSSIBLY_ADDRESSED: "bagian yang dikomentari sudah berubah",
    CommentState.NOT_ADDRESSED: "bagian yang dikomentari belum berubah",
    CommentState.UNKNOWN: "tidak menempel ke paragraf tertentu",
}


def render_text(b: Brief) -> str:
    """Teks pesan chat (WhatsApp/email). Pendek, faktual, tanpa penilaian."""
    head = f"Supervision Brief — {b.project_title} ({b.program})"
    span = f"v{b.from_version} → v{b.to_version}" if b.from_version else f"v{b.to_version}"
    out = [head, f"Versi: {span}", ""]

    out.append("Yang berubah:")
    out += [f"- {c}" for c in b.changes] or ["- Tidak ada perubahan elemen yang terdeteksi."]

    if b.impacts:
        out += ["", "Perlu dicek ulang karena perubahan:"]
        out += [f"- {line}" for line in b.impacts]

    out += ["", "Komentar dosen sebelumnya:"]
    if b.comments:
        for c in b.comments:
            confirmed = (
                ""
                if c.confirmed is None
                else (" (mahasiswa: sudah)" if c.confirmed else " (mahasiswa: belum)")
            )
            out.append(f"- “{c.text}” — {_STATE_TEXT[c.state]}{confirmed}")
    else:
        out.append("- Tidak ada komentar yang terbaca.")

    out += ["", "Menunggu keputusan dosen:"]
    where = "bagian" if b.unit == "section" else "hlm."
    for f in b.awaiting_supervisor:
        pages = ", ".join(f"{e.element} {where} {e.page}" for e in f.evidence)
        out.append(f"- [{f.rule_id}] {f.title}" + (f" ({pages})" if pages else ""))
    if not b.awaiting_supervisor:
        out.append("- Tidak ada.")

    out += ["", "Temuan terbuka (belum dikonfirmasi mahasiswa):"]
    out += [f"- [{f.rule_id}] {f.title}" for f in b.open_findings] or ["- Tidak ada."]

    if b.resolved_rules:
        out += ["", "Tidak muncul lagi di versi ini: " + ", ".join(b.resolved_rules)]

    out += [
        "",
        "Dibuat otomatis oleh ThesisTwin dari catatan versi. Bukan penilaian; temuan adalah "
        "pertanyaan untuk didiskusikan.",
    ]
    return "\n".join(out)
