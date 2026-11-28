from datetime import UTC, datetime

from app.domain.brief import BriefFinding, build_brief, render_text
from app.domain.comments import CommentState, comment_statuses
from app.domain.diff import diff_elements
from app.domain.rules import Element


def E(id_, type_, content):
    return Element(id_, type_, content, 1)


def test_diff_pairs_by_type_and_similarity():
    old = [
        E("a", "research_question", "Bagaimana pengaruh PBL terhadap pemecahan masalah?"),
        E("b", "method", "Desain one-group pre-test/post-test."),
        E("c", "variable", "Motivasi belajar."),
    ]
    new = [
        E("a2", "research_question", "Bagaimana perubahan skor pemecahan masalah setelah PBL?"),
        E("b2", "method", "Desain one-group pre-test / post-test."),
        E("d", "instrument", "Tes uraian 5 soal."),
    ]
    d = diff_elements(old, new)
    assert [(o.id, n.id) for o, n in d.unchanged] == [("b", "b2")]
    assert [(c.old.id, c.new.id) for c in d.changed] == [("a", "a2")]
    assert [e.id for e in d.removed] == ["c"]
    assert [e.id for e in d.added] == ["d"]


def test_fully_rewritten_element_of_same_type_counts_as_changed():
    d = diff_elements(
        [E("a", "research_question", "Apa pengaruh X terhadap Y?")],
        [E("b", "research_question", "Bagaimana hubungan antara Z dan W di kelas VIII?")],
    )
    assert [(c.old.id, c.new.id) for c in d.changed] == [("a", "b")]
    assert not d.added and not d.removed


def test_diff_never_pairs_across_types():
    d = diff_elements([E("a", "objective", "Sama persis")], [E("b", "claim", "Sama persis")])
    assert [e.id for e in d.removed] == ["a"] and [e.id for e in d.added] == ["b"]


BLOCKS_OLD = [
    {"index": 0, "text": "Bagaimana pengaruh PBL terhadap hasil belajar?"},
    {"index": 1, "text": "Desain one-group pre-test/post-test."},
]
COMMENTS = [
    {"id": "1", "author": "Dosen", "text": "Hati-hati kata pengaruh.", "anchor_block": 0},
    {"id": "2", "author": "Dosen", "text": "Desain?", "anchor_block": 1},
    {"id": "3", "author": "Dosen", "text": "Umum.", "anchor_block": None},
]


def test_comment_state_follows_anchored_text():
    new = [
        {"index": 0, "text": "Bagaimana perubahan hasil belajar setelah PBL?"},
        {"index": 1, "text": "Desain one-group pre-test/post-test."},
    ]
    states = {c.comment_id: c.state for c in comment_statuses(BLOCKS_OLD, COMMENTS, new)}
    assert states == {
        "1": CommentState.POSSIBLY_ADDRESSED,
        "2": CommentState.NOT_ADDRESSED,
        "3": CommentState.UNKNOWN,
    }


def test_student_confirmation_is_carried():
    [c, *_] = comment_statuses(BLOCKS_OLD, COMMENTS, BLOCKS_OLD, {"1": True})
    assert c.confirmed is True


def test_brief_summarises_state_only():
    d = diff_elements(
        [E("a", "research_question", "Apa pengaruh X terhadap Y?")],
        [E("a2", "research_question", "Apa hubungan X dengan Y pada kelas VIII?")],
    )
    findings = [
        BriefFinding("F1", "R-OBJ-ANALYSIS", "Tujuan belum punya analisis", "high", "ai_suggested"),
        BriefFinding(
            "F2", "R-VAR-INSTR", "Variabel tanpa instrumen", "medium", "student_confirmed"
        ),
    ]
    b = build_brief(
        project_title="Skripsi",
        program="matematika",
        from_version=1,
        to_version=2,
        generated_at=datetime(2026, 11, 24, tzinfo=UTC),
        diff=d,
        comments=comment_statuses(BLOCKS_OLD, COMMENTS, BLOCKS_OLD),
        findings=findings,
        previous_rules={"R-CAUSAL-01", "R-OBJ-ANALYSIS"},
    )
    assert [f.id for f in b.open_findings] == ["F1"]
    assert [f.id for f in b.awaiting_supervisor] == ["F2"]
    assert b.resolved_rules == ["R-CAUSAL-01"]
    text = render_text(b)
    assert "v1 → v2" in text and "Diubah — Rumusan masalah" in text
    assert "Bukan penilaian" in text


def test_brief_speaks_in_rule_titles_not_ids():
    # Dosen tidak mengenal ID aturan (supervisor-burden §2 no. 4).
    sections = [
        BriefFinding(
            f"S{i}", "R-SECTIONS-UMUM", f"Bagian wajib tidak ditemukan: {s}", "low", "ai_suggested"
        )
        for i, s in enumerate(["Latar Belakang", "Hipotesis"])
    ]
    b = build_brief(
        project_title="Skripsi",
        program="matematika",
        from_version=1,
        to_version=2,
        generated_at=datetime(2026, 11, 24, tzinfo=UTC),
        diff=None,
        comments=[],
        findings=[
            *sections,
            BriefFinding(
                "F2", "R-VAR-INSTR", "Variabel tanpa instrumen", "medium", "student_confirmed"
            ),
        ],
        previous_rules={"R-CAUSAL-01"},
        rule_titles={"R-CAUSAL-01": "Pertanyaan kausal, desain mungkin belum mendukung"},
    )
    assert b.open_summary == ["Bagian wajib tidak ditemukan: Latar Belakang, Hipotesis"]
    assert b.resolved_titles == ["Pertanyaan kausal, desain mungkin belum mendukung"]
    text = render_text(b)
    assert "R-" not in text
    assert "- Variabel tanpa instrumen" in text
    assert "Bagian wajib tidak ditemukan: Latar Belakang, Hipotesis" in text
