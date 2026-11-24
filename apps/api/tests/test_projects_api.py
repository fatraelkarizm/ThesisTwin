import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.deps import get_storage
from app.db.session import get_session, init_db
from app.main import app
from app.storage import LocalStorage
from tests.test_docx import SAMPLE
from tests.test_pdf import _pdf


@pytest.fixture
def client(tmp_path):
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    init_db(engine)
    make = sessionmaker(bind=engine, expire_on_commit=False)

    def _session():
        with make() as s:
            yield s

    app.dependency_overrides[get_session] = _session
    app.dependency_overrides[get_storage] = lambda: LocalStorage(tmp_path)
    yield TestClient(app)
    app.dependency_overrides.clear()


def _project(client) -> str:
    r = client.post("/projects", json={"title": "Skripsi", "program": "matematika"})
    assert r.status_code == 201
    return r.json()["id"]


def _upload(client, pid, data: bytes, name="proposal.pdf"):
    return client.post(f"/projects/{pid}/documents", files={"file": (name, data)})


def test_upload_requires_consent(client):
    pid = _project(client)
    r = _upload(client, pid, _pdf(["RQ1"]))
    assert r.status_code == 403


def test_pdf_upload_creates_version_with_pages(client):
    pid = _project(client)
    assert client.post(f"/projects/{pid}/consent").json()["consent_at"]
    r = _upload(client, pid, _pdf(["Halaman satu", "Halaman dua"]))
    assert r.status_code == 201
    body = r.json()
    assert (body["created"], body["pages"], body["version"]["version_no"]) == (True, 2, 1)


def test_reupload_same_file_does_not_create_version(client):
    pid = _project(client)
    client.post(f"/projects/{pid}/consent")
    data = _pdf(["sama"])
    _upload(client, pid, data)
    again = _upload(client, pid, data).json()
    assert again["created"] is False
    listed = client.get(f"/projects/{pid}/versions").json()
    assert len(listed) == 1
    assert listed[0]["uploaded_at"].endswith("Z")  # UTC konsisten walau SQLite membuang tz


def test_type_detected_from_content_not_filename(client):
    pid = _project(client)
    client.post(f"/projects/{pid}/consent")
    r = _upload(client, pid, b"bukan pdf sama sekali", name="palsu.pdf")
    assert r.status_code == 415


def test_corrupt_pdf_is_422(client):
    pid = _project(client)
    client.post(f"/projects/{pid}/consent")
    r = _upload(client, pid, b"%PDF-1.4\nrusak")
    assert r.status_code == 422


def test_docx_upload_keeps_comments(client):
    pid = _project(client)
    client.post(f"/projects/{pid}/consent")
    r = _upload(client, pid, SAMPLE, name="proposal.docx")
    assert r.status_code == 201
    assert r.json()["version"]["media_type"].endswith("wordprocessingml.document")
    assert r.json()["pages"] == 2  # 2 bagian (per heading), bukan halaman


def test_unknown_project_is_404(client):
    assert client.post("/projects/nope/consent").status_code == 404
    assert client.get("/projects/nope/versions").status_code == 404
