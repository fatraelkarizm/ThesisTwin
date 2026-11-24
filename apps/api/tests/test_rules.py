import pytest

from app.domain.rules import (
    Element,
    Rule,
    evaluate,
    example_elements,
    has_term,
    normalize,
    run,
)
from app.domain.status import Status
from app.services.rules import RuleFileError, load_rules

RULES = load_rules()


def test_rules_directory_loads():
    assert RULES, "rules/*.yaml kosong"


# Tes generik: setiap aturan membawa contoh yang harus memicu dan yang tidak boleh memicu.
@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.id)
def test_rule_examples(rule: Rule):
    fires, quiet = rule.examples["fires"], rule.examples["quiet"]
    assert evaluate(rule, example_elements(fires), fires.document_text), (
        "contoh 'fires' tidak memicu"
    )
    assert not evaluate(rule, example_elements(quiet), quiet.document_text), "contoh 'quiet' memicu"


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.id)
def test_findings_are_questions_not_verdicts(rule: Rule):
    assert rule.suggested_clarification.rstrip().endswith("?")
    # Per kata utuh: "masalah" bukan "salah".
    assert not has_term(rule.title, ["salah", "keliru", "gagal", "tidak valid"])


def test_normalize_and_terms():
    assert normalize("One-Group  Pre-Test/Post-Test") == "one group pre test post test"
    assert has_term("Desain one-group pre-test", ["pre test"])
    assert not has_term("pengaruhnya", ["pengaruh"])  # utuh per kata, bukan potongan


def _causal() -> Rule:
    return next(r for r in RULES if r.id == "R-CAUSAL-01")


def test_finding_cites_rule_and_evidence_pages():
    els = [
        Element("RQ1", "research_question", "Apa pengaruh X terhadap Y?", 5),
        Element("M1", "method", "Desain one-group pre-test/post-test", 21),
    ]
    [f] = evaluate(_causal(), els)
    assert f.rule_id == "R-CAUSAL-01"
    assert [(e.element, e.page) for e in f.evidence] == [("RQ1", 5), ("M1", 21)]
    assert f.status is Status.AI_SUGGESTED


def test_unverified_evidence_downgrades_status():
    els = [
        Element("RQ1", "research_question", "Apa pengaruh X?", 5, verified=False),
        Element("M1", "method", "one-group pre-test", 21),
    ]
    [f] = evaluate(_causal(), els)
    assert f.status is Status.NEEDS_USER_CONFIRMATION


def test_program_filter_and_disabled():
    rule = _causal().model_copy(update={"programs": ["fisika"]})
    els = example_elements(rule.examples["fires"])
    assert run([rule], els, "matematika") == []
    off = _causal().model_copy(update={"enabled": False})
    assert run([off], els, "matematika") == []


def test_invalid_rule_file_reports_filename(tmp_path):
    (tmp_path / "R-BAD.yaml").write_text("id: R-BAD\npriority: urgent\n", encoding="utf-8")
    with pytest.raises(RuleFileError, match="R-BAD.yaml"):
        load_rules(tmp_path)
