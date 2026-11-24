from sqlalchemy import create_engine, inspect, text

from app.db.session import init_db
from app.domain.graph import build_graph
from app.domain.rules import Element


def E(id_, type_):
    return Element(id_, type_, id_, 1)


def test_edges_follow_ontology():
    g = build_graph([E("RQ1", "research_question"), E("O1", "objective"), E("M1", "method")])
    assert {(e.src, e.dst, e.type) for e in g.edges} == {
        ("RQ1", "O1", "addresses"),
        ("O1", "M1", "requires"),
    }


def test_gaps_when_expected_type_missing():
    g = build_graph([E("V1", "variable"), E("O1", "objective")])
    gaps = {(x.from_type, x.to_type) for x in g.gaps}
    assert ("variable", "instrument") in gaps and ("objective", "analysis") in gaps
    assert ("research_question", "objective") not in gaps  # tidak ada RQ -> bukan celah


def test_nodes_ordered_by_dependency_chain():
    g = build_graph([E("A", "analysis"), E("RQ", "research_question"), E("O", "objective")])
    assert [n.id for n in g.nodes] == ["RQ", "O", "A"]


def test_init_db_adds_new_nullable_column_to_old_table(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'old.db'}")
    with engine.begin() as c:  # skema lama tanpa kolom element_id
        c.execute(
            text(
                "CREATE TABLE finding_evidence (id INTEGER PRIMARY KEY, finding_id VARCHAR, "
                "element VARCHAR, document VARCHAR, page INTEGER)"
            )
        )
        c.execute(text("INSERT INTO finding_evidence VALUES (1, 'F', 'RQ', 'v1', 5)"))
    init_db(engine)
    cols = {c["name"] for c in inspect(engine).get_columns("finding_evidence")}
    assert "element_id" in cols
    with engine.connect() as c:  # data lama tetap ada
        assert c.execute(text("SELECT page FROM finding_evidence")).scalar() == 5
