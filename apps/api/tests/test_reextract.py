"""Baca ulang dokumen versi lama dengan kosakata ekstraksi terbaru (config/extraction.yaml)."""

from tests.test_docx import _p, make_docx
from tests.test_e2e_review import _element, _upload
from tests.test_projects_api import client  # noqa: F401  (fixture)

RQ = "Bagaimana kemampuan representasi matematis siswa kelas VIII?"
OBJ = "Mendeskripsikan kemampuan representasi matematis siswa kelas VIII."
DOC = make_docx(_p("Rumusan Masalah", "Heading1") + _p(RQ) + _p("Tujuan", "Heading1") + _p(OBJ))


def test_reextract_adds_only_missing_elements_and_is_idempotent(client):  # noqa: F811
    pid = client.post("/projects", json={"title": "S", "program": "matematika"}).json()["id"]
    client.post(f"/projects/{pid}/consent")
    vid = _upload(client, pid, DOC)
    before = client.get(f"/versions/{vid}/elements").json()
    assert {e["type"] for e in before} == {"research_question", "objective"}

    # Mahasiswa sudah menulis elemen yang sama secara manual: tidak boleh jadi ganda.
    _element(client, vid, "method", "Survei deskriptif.", 1)
    first = client.post(f"/versions/{vid}/reextract")
    assert first.status_code == 200, first.text
    assert first.json()["added"] == 0
    assert len(client.get(f"/versions/{vid}/elements").json()) == len(before) + 1

    assert client.post(f"/versions/{vid}/reextract").json()["added"] == 0


def test_reextract_unknown_version_is_404(client):  # noqa: F811
    assert client.post("/versions/tidak-ada/reextract").status_code == 404
