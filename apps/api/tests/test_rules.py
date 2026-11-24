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


VERDICT_TERMS = ["bagus", "jelek", "buruk", "salah", "benar", "keliru", "gagal", "tidak valid"]
# Arah = pilihan yang bisa dieksplorasi, bukan perintah. Kalimat perintah di awal opsi ditolak.
IMPERATIVE_START = [
    "hapus", "ganti", "tambahkan", "pilih", "tulis", "buat", "tentukan", "pindahkan",
    "batasi", "cocokkan", "sebutkan", "tetapkan", "ubah", "perbaiki", "gunakan",
]


def _rule_texts(rule: Rule) -> list[str]:
    texts = [rule.title, rule.why_flagged, rule.suggested_clarification]
    return texts + [t for d in rule.directions for t in (d.option, d.implication)]


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.id)
def test_rule_texts_carry_no_verdict(rule: Rule):
    for text in _rule_texts(rule):
        assert not has_term(text, VERDICT_TERMS), text


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.id)
def test_directions_are_options_not_orders(rule: Rule):
    assert len(rule.directions) >= 2, "navigasi butuh minimal dua arah untuk dibandingkan"
    for d in rule.directions:
        first = normalize(d.option).split()[0]
        assert first not in IMPERATIVE_START, d.option


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.id)
def test_rule_declares_where_its_basis_comes_from(rule: Rule):
    assert rule.source_types
    if rule.references:
        assert rule.basis


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


def _rule(rule_id: str) -> Rule:
    return next(r for r in RULES if r.id == rule_id)


def test_mixed_citation_styles_cite_first_page_of_each_style():
    pages = {
        1: "DAFTAR ISI ... [1] ... (Sugiyono, 2019)",
        3: "Penelitian sebelumnya [1], [2] menunjukkan hal serupa [3].",
        7: "Menurut Creswell (2018) dan (Campbell & Stanley, 1963), juga (Wohlin et al., 2012).",
    }
    text = "\n".join(pages.values())
    [f] = evaluate(_rule("R-CITE-STYLE-MIX"), [], text, pages)
    assert sorted(e.page for e in f.evidence) == [3, 7]
    assert f.status is Status.AI_SUGGESTED


def test_single_citation_style_is_quiet():
    text = "Hal ini [1] didukung [2] dan [3, 4]. Interval [0, 1] dipakai."
    assert evaluate(_rule("R-CITE-STYLE-MIX"), [], text) == []


def test_mixed_decimal_markers():
    rule = _rule("R-DECIMAL-MIX")
    assert evaluate(rule, [], "taraf 0,05 dan rata-rata 0,73; output: p = 0.012, r = 0.45")
    # Nomor subbab (3.1) dan ribuan (10.000) bukan desimal berawalan nol.
    assert not evaluate(rule, [], "Subbab 3.1, 3.2, Rp10.000; taraf 0,05 dan 0,01")


def test_invalid_regex_rejected():
    from app.domain.rules import MixedPatternsCheck

    with pytest.raises(ValueError):
        MixedPatternsCheck.model_validate(
            {
                "kind": "mixed_patterns",
                "patterns": [{"name": "a", "regex": "("}, {"name": "b", "regex": "x"}],
            }
        )
