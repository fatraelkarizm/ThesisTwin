from app.domain.graph import build_graph
from app.domain.rules import Element
from app.domain.stress import MAX_Q, MIN_Q, FindingRef, stress_questions
from tests.test_e2e_review import METHOD, RQ_OLD, V1, _element, _upload
from tests.test_projects_api import client  # noqa: F401


def E(id_, type_, content, verified=True):
    return Element(id_, type_, content, 1, verified)


ELS = [
    E("rq", "research_question", "Bagaimana pengaruh PBL terhadap hasil belajar?"),
    E("o", "objective", "Mengetahui pengaruh PBL."),
    E("m", "method", "Desain one-group pre-test/post-test."),
    E("v", "variable", "Motivasi belajar", verified=False),
]


def test_open_finding_ranks_first_and_names_the_design():
    qs = stress_questions(
        build_graph(ELS), [FindingRef("R-CAUSAL-01", "high", "student_confirmed", ["rq", "m"])]
    )
    assert MIN_Q <= len(qs) <= MAX_Q
    assert qs[0].key == "finding:R-CAUSAL-01" and "one-group" in qs[0].text
    assert all(q.text.rstrip().endswith("?") for q in qs)  # pertanyaan, bukan jawaban


def test_gaps_and_unverified_elements_become_questions():
    keys = {q.key for q in stress_questions(build_graph(ELS), [])}
    assert "gap:variable:instrument" in keys and "unverified:v" in keys


def test_rejected_findings_are_ignored():
    qs = stress_questions(build_graph(ELS), [FindingRef("R-CAUSAL-01", "high", "rejected", ["rq"])])
    assert "finding:R-CAUSAL-01" not in {q.key for q in qs}


def test_baseline_fills_up_to_minimum():
    qs = stress_questions(
        build_graph([E("m", "method", "Studi kasus."), E("a", "analysis", "Analisis tematik.")]), []
    )
    assert len(qs) >= 2 and all(q.kind in {"gap", "baseline"} for q in qs)


def test_api_flow_answer_and_supervisor_rating(client):  # noqa: F811
    pid = client.post("/projects", json={"title": "S", "program": "matematika"}).json()["id"]
    client.post(f"/projects/{pid}/consent")
    vid = _upload(client, pid, V1)
    _element(client, vid, "research_question", RQ_OLD, 1)
    _element(client, vid, "method", METHOD, 2)
    client.post(f"/versions/{vid}/check")

    qs = client.post(f"/versions/{vid}/stress-test").json()
    assert qs[0]["text"].startswith("Pertanyaan Anda bersifat sebab-akibat")
    assert client.post(f"/versions/{vid}/stress-test").json() == qs  # idempoten

    a = client.post(f"/stress-questions/{qs[0]['id']}/answer", json={"answer": "Karena ..."})
    assert a.json()["answer"] == "Karena ..."
    regenerated = client.post(f"/versions/{vid}/stress-test?regenerate=true").json()
    assert any(q["answer"] == "Karena ..." for q in regenerated)  # jawaban tidak hilang

    token = client.post(f"/projects/{pid}/share").json()["token"]
    assert len(client.get(f"/share/{token}/stress-test").json()) == len(regenerated)
    r = client.post(f"/share/{token}/stress-questions/{qs[0]['id']}/rating", json={"score": 4})
    assert r.json()["rating"] == 4
    bad = client.post(f"/share/{token}/stress-questions/{qs[0]['id']}/rating", json={"score": 9})
    assert bad.status_code == 422


def test_link_cannot_rate_other_project(client):  # noqa: F811
    ids = []
    for t in ("A", "B"):
        pid = client.post("/projects", json={"title": t, "program": "matematika"}).json()["id"]
        client.post(f"/projects/{pid}/consent")
        ids.append(pid)
    vb = _upload(client, ids[1], V1)
    _element(client, vb, "method", METHOD, 2)
    qb = client.post(f"/versions/{vb}/stress-test").json()[0]["id"]
    token_a = client.post(f"/projects/{ids[0]}/share").json()["token"]
    r = client.post(f"/share/{token_a}/stress-questions/{qb}/rating", json={"score": 5})
    assert r.status_code == 404


def test_reasons_use_indonesian_labels_not_internal_ids():
    qs = stress_questions(build_graph([E("v", "variable", "Motivasi")]), [])
    gap = next(q for q in qs if q.kind == "gap")
    assert "variabel tanpa instrumen" in gap.reason and "variable" not in gap.reason


def test_new_rules_have_examiner_questions():
    qs = stress_questions(
        build_graph(ELS),
        [
            FindingRef("R-PROPOSAL-RESULTS", "high", "ai_suggested", []),
            FindingRef("R-RQ-OBJ-COUNT", "medium", "ai_suggested", ["rq", "o"]),
        ],
    )
    keys = [q.key for q in qs]
    assert keys[:2] == ["finding:R-PROPOSAL-RESULTS", "finding:R-RQ-OBJ-COUNT"]
    assert "angka hasil" in qs[0].text
