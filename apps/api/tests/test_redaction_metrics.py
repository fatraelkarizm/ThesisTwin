from app.domain.metrics import evidence_correctness, score_extraction
from app.domain.redaction import redact


def test_redacts_email_phone_nim():
    out = redact("NIM 13520012345, hp 081234567890 / +628123456789, a.b@mail.itb.ac.id")
    assert "13520012345" not in out and "0812" not in out and "@" not in out
    assert "[NIM]" in out and "[TELEPON]" in out and "[EMAIL]" in out


def test_phone_not_misread_as_nim():
    assert redact("081234567890") == "[TELEPON]"


def test_plain_numbers_kept():
    assert redact("sampel 120 responden, tahun 2026") == "sampel 120 responden, tahun 2026"


def test_score_extraction_per_type():
    gold = {("research_question", "rq1"), ("research_question", "rq2"), ("method", "survei")}
    pred = {("research_question", "rq1"), ("method", "survei"), ("method", "eksperimen")}
    s = score_extraction(pred, gold)
    assert (s["research_question"].precision, s["research_question"].recall) == (1.0, 0.5)
    assert (s["method"].precision, s["method"].recall) == (0.5, 1.0)
    assert (s["ALL"].tp, s["ALL"].fp, s["ALL"].fn) == (2, 1, 1)


def test_score_empty_is_zero_not_crash():
    assert score_extraction(set(), set())["ALL"].f1 == 0.0
    assert evidence_correctness([]) == 0.0
    assert evidence_correctness([True, True, False, True]) == 0.75
