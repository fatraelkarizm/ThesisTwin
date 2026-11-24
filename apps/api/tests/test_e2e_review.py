"""Alur end-to-end tanpa LLM: unggah v1 (DOCX + komentar) -> elemen -> cek -> konfirmasi
mahasiswa -> unggah v2 -> diff + status komentar -> brief -> tautan dosen -> keputusan dosen."""

from datetime import UTC, datetime, timedelta

from app.db.models import AuditLog
from app.services import share
from tests.test_docx import _p, make_docx
from tests.test_projects_api import client  # noqa: F401  (fixture)

RQ_OLD = "Bagaimana pengaruh model PBL terhadap kemampuan pemecahan masalah siswa?"
RQ_NEW = "Bagaimana perubahan kemampuan pemecahan masalah siswa setelah model PBL?"
METHOD = "Penelitian ini memakai desain one-group pre-test/post-test."
COMMENT = (
    '<w:comment w:id="7" w:author="Pembimbing 1" w:date="2026-11-20T10:00:00Z">'
    + _p("Kata pengaruh terlalu kuat untuk desain ini.")
    + "</w:comment>"
)

V1 = make_docx(
    _p("Rumusan Masalah", "Heading1")
    + _p(RQ_OLD, comment="7")
    + _p("Metode", "Heading1")
    + _p(METHOD),
    comments=COMMENT,
)
V2 = make_docx(
    _p("Rumusan Masalah", "Heading1") + _p(RQ_NEW) + _p("Metode", "Heading1") + _p(METHOD)
)


def _upload(client, pid, data):  # noqa: F811
    r = client.post(f"/projects/{pid}/documents", files={"file": ("p.docx", data)})
    assert r.status_code == 201, r.text
    return r.json()["version"]["id"]


def _element(client, vid, type_, text, section):  # noqa: F811
    r = client.post(
        f"/versions/{vid}/elements",
        json={"type": type_, "content": text, "quote": text, "page": section},
    )
    assert r.status_code == 201, r.text
    return r.json()


def test_full_flow_without_llm(client):  # noqa: F811
    pid = client.post("/projects", json={"title": "Skripsi PBL", "program": "matematika"}).json()[
        "id"
    ]
    client.post(f"/projects/{pid}/consent")

    # v1: elemen dimasukkan mahasiswa; kutipan diverifikasi terhadap bagian dokumen.
    v1 = _upload(client, pid, V1)
    rq = _element(client, v1, "research_question", RQ_OLD, 1)
    assert rq["verified"] and rq["status"] == "student_confirmed"
    fake = _element(client, v1, "objective", "Kalimat yang tidak ada di dokumen.", 1)
    assert not fake["verified"] and fake["status"] == "needs_user_confirmation"
    _element(client, v1, "method", METHOD, 2)

    findings = client.post(f"/versions/{v1}/check").json()
    causal = next(f for f in findings if f["rule_id"] == "R-CAUSAL-01")
    assert causal["status"] == "ai_suggested"  # semua evidence terverifikasi
    assert {(e["element"], e["page"]) for e in causal["evidence"]} == {
        ("Rumusan masalah", 1),
        ("Metode/desain", 2),
    }
    r = client.post(f"/findings/{causal['id']}/status", json={"target": "student_confirmed"})
    assert r.json()["status"] == "student_confirmed"

    # Cek ulang tidak menduplikasi temuan yang sudah ditinjau.
    again = client.post(f"/versions/{v1}/check").json()
    assert sum(f["rule_id"] == "R-CAUSAL-01" for f in again) == 1

    # v2: RQ dirumuskan ulang; komentar dosen di paragraf itu kemungkinan sudah ditangani.
    v2 = _upload(client, pid, V2)
    _element(client, v2, "research_question", RQ_NEW, 1)
    _element(client, v2, "method", METHOD, 2)
    client.post(f"/versions/{v2}/check")

    [c] = client.get(f"/projects/{pid}/comments").json()
    assert (c["comment_id"], c["state"]) == ("7", "possibly_addressed")
    client.post(f"/versions/{v1}/comments/7", json={"addressed": True})

    brief = client.get(f"/projects/{pid}/brief").json()
    assert (brief["from_version"], brief["to_version"]) == (1, 2)
    assert any(line.startswith("Diubah — Rumusan masalah") for line in brief["changes"])
    assert brief["comments"][0]["confirmed"] is True
    text = client.get(f"/projects/{pid}/brief.txt").text
    assert "Kata pengaruh terlalu kuat" in text and "Bukan penilaian" in text

    # Dosen tanpa akun: tautan bertoken.
    link = client.post(f"/projects/{pid}/share").json()
    token = link["token"]
    assert link["path"] == f"/dosen/{token}"
    assert client.get(f"/share/{token}").json()["to_version"] == 2

    decided = client.post(f"/share/{token}/findings/{causal['id']}", json={"confirm": True})
    assert decided.json()["status"] == "supervisor_confirmed"
    assert client.get("/share/token-salah").status_code == 404


def test_recheck_keeps_sibling_findings_of_the_same_rule(client):  # noqa: F811
    pid = client.post("/projects", json={"title": "S", "program": "matematika"}).json()["id"]
    client.post(f"/projects/{pid}/consent")
    vid = _upload(client, pid, V1)
    _element(client, vid, "research_question", RQ_OLD, 1)
    sections = [
        f for f in client.post(f"/versions/{vid}/check").json() if f["rule_id"] == "R-SECTIONS-UMUM"
    ]
    assert len(sections) > 1  # satu temuan per bagian wajib yang hilang
    assert len({f["title"] for f in sections}) == len(sections)  # judulnya bisa dibedakan
    client.post(f"/findings/{sections[0]['id']}/status", json={"target": "student_confirmed"})
    again = [
        f for f in client.post(f"/versions/{vid}/check").json() if f["rule_id"] == "R-SECTIONS-UMUM"
    ]
    assert len(again) == len(sections)  # yang lain tidak hilang setelah satu dikonfirmasi


def test_link_cannot_touch_other_project_and_expires(client):  # noqa: F811
    a = client.post("/projects", json={"title": "A", "program": "matematika"}).json()["id"]
    b = client.post("/projects", json={"title": "B", "program": "matematika"}).json()["id"]
    for pid in (a, b):
        client.post(f"/projects/{pid}/consent")
    vb = _upload(client, b, V1)
    _element(client, vb, "research_question", RQ_OLD, 1)
    _element(client, vb, "method", METHOD, 2)
    finding_b = client.post(f"/versions/{vb}/check").json()[0]["id"]

    token_a = client.post(f"/projects/{a}/share").json()["token"]
    r = client.post(f"/share/{token_a}/findings/{finding_b}", json={"confirm": True})
    assert r.status_code == 404  # tautan proyek A tidak bisa memutuskan temuan proyek B


def test_expired_link_is_rejected():
    from sqlalchemy.orm import Session

    from app.db.session import init_db, make_engine
    from app.services.documents import create_project

    engine = make_engine("sqlite://")
    init_db(engine)
    with Session(engine) as s:
        p = create_project(s, "X", "matematika")
        t0 = datetime(2026, 11, 1, tzinfo=UTC)
        _, token = share.create_link(s, p.id, days=14, now=lambda: t0)
        share.resolve(s, token, now=lambda: t0 + timedelta(days=13))
        try:
            share.resolve(s, token, now=lambda: t0 + timedelta(days=14, seconds=1))
            raise AssertionError("tautan kedaluwarsa masih diterima")
        except share.LinkInvalid:
            pass
        assert [a.action for a in s.query(AuditLog)] == ["share_created"]  # hanya pembuatan tautan


def test_style_finding_keeps_page_evidence(client):  # noqa: F811
    pid = client.post("/projects", json={"title": "S", "program": "matematika"}).json()["id"]
    client.post(f"/projects/{pid}/consent")
    doc = make_docx(
        _p("Metode", "Heading1")
        + _p("Taraf signifikansi 0,05 dan rata-rata 0,73.")
        + _p("Hasil Uji Coba", "Heading1")
        + _p("Output: p = 0.012, r = 0.45.")
    )
    vid = _upload(client, pid, doc)
    found = client.post(f"/versions/{vid}/check").json()
    [f] = [f for f in found if f["rule_id"] == "R-DECIMAL-MIX"]
    assert {e["element"] for e in f["evidence"]} == {"koma desimal", "titik desimal"}
    assert all(e["page"] for e in f["evidence"])
    assert f["source_types"] == ["math_writing"] and len(f["directions"]) == 3
