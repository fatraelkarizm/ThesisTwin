import string
from pathlib import Path

import pytest

from app.services.config import (
    CONFIG_DIR,
    ConfigFileError,
    load_extraction,
    load_ontology,
)
from app.services.rules import load_rules


def _copy_config(tmp_path: Path, **override: str) -> Path:
    for name in ("ontology.yaml", "extraction.yaml"):
        text = override.get(name) or (CONFIG_DIR / name).read_text(encoding="utf-8")
        (tmp_path / name).write_text(text, encoding="utf-8")
    return tmp_path


def test_shipped_config_loads():
    ont = load_ontology()
    assert ont.label("research_question") == "Rumusan masalah"
    assert ont.gap_question("variable", "instrument")
    assert load_extraction().sections


def test_relation_to_unknown_type_is_rejected_with_filename(tmp_path):
    bad = """
element_types: [{id: objective, label: Tujuan, layer: 1}]
relations: [{source: objective, target: hasil, type: requires}]
"""
    with pytest.raises(ConfigFileError, match=r"(?s)ontology\.yaml.*hasil"):
        load_ontology(_copy_config(tmp_path, **{"ontology.yaml": bad}))


def test_extraction_section_must_use_known_type(tmp_path):
    bad = "sections: [{type: abstrak, headings: [Abstrak]}]\n"
    with pytest.raises(ConfigFileError, match=r"(?s)extraction\.yaml.*abstrak"):
        load_extraction(_copy_config(tmp_path, **{"extraction.yaml": bad}))


def test_new_heading_is_picked_up_from_config_without_code_change(tmp_path):
    from app.domain.structure import extract_by_structure

    custom = (CONFIG_DIR / "extraction.yaml").read_text(encoding="utf-8").replace(
        "headings: [Tujuan Penelitian, Research Objectives]",
        "headings: [Tujuan Penelitian, Research Objectives, Maksud Penelitian]",
    )
    vocab = load_extraction(_copy_config(tmp_path, **{"extraction.yaml": custom}))
    pages = {
        3: "Pendahuluan singkat. \n1.3 Maksud Penelitian \n"
        "1. Mengukur kemampuan representasi matematis siswa kelas VIII."
    }
    assert [e.type for e in extract_by_structure(pages, vocab)] == ["objective"]


WITH_QUESTION = [r for r in load_rules() if r.defense_question]


@pytest.mark.parametrize("rule", WITH_QUESTION, ids=lambda r: r.id)
def test_defense_question_placeholders_are_element_types(rule):
    assert rule.defense_question is not None
    fields = {f for _, f, _, _ in string.Formatter().parse(rule.defense_question) if f}
    assert fields <= set(load_ontology().type_ids)
    assert rule.defense_question.rstrip().endswith("?")
