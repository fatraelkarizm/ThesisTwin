import json

from sqlalchemy import func, select

from app.db import models as m
from app.db.session import get_session
from app.main import app
from tests.test_e2e_review import METHOD, RQ_OLD, V1, _element, _upload
from tests.test_projects_api import client  # noqa: F401


def _session():
    return next(app.dependency_overrides[get_session]())


def _seed(client):  # noqa: F811
    pid = client.post("/projects", json={"title": "Hapus", "program": "matematika"}).json()["id"]
    client.post(f"/projects/{pid}/consent")
    vid = _upload(client, pid, V1)
    _element(client, vid, "research_question", RQ_OLD, 1)
    _element(client, vid, "method", METHOD, 2)
    client.post(f"/versions/{vid}/check")
    client.post(f"/versions/{vid}/stress-test")
    token = client.post(f"/projects/{pid}/share").json()["token"]
    return pid, vid, token


def test_delete_removes_everything_and_files(client, tmp_path):  # noqa: F811
    pid, vid, token = _seed(client)
    assert any(tmp_path.rglob("*"))  # file unggahan ada
    assert client.get(f"/projects/{pid}").json()["title"] == "Hapus"
    assert client.delete(f"/projects/{pid}").status_code == 204
    assert client.get(f"/projects/{pid}").status_code == 404

    s = _session()
    for table in (
        m.Project,
        m.Document,
        m.DocumentVersion,
        m.ElementRow,
        m.FindingRow,
        m.EvidenceRow,
        m.StressQuestionRow,
        m.ShareLink,
    ):
        assert s.scalar(select(func.count()).select_from(table)) == 0, table.__tablename__
    assert not any(p.is_file() for p in tmp_path.rglob("*"))  # file ikut terhapus
    assert client.get(f"/share/{token}").status_code == 404
    last = s.scalars(select(m.AuditLog).order_by(m.AuditLog.id.desc())).first()
    assert (last.action, last.entity_id, json.loads(last.meta_json)) == ("project_deleted", pid, {})


def test_revoked_link_stops_working(client):  # noqa: F811
    pid, _, token = _seed(client)
    [link] = client.get(f"/projects/{pid}/share-links").json()
    assert "token" not in link and link["revoked"] is False
    assert client.post(f"/projects/{pid}/share-links/{link['id']}/revoke").json()["revoked"]
    assert client.get(f"/share/{token}").status_code == 404


def test_cannot_revoke_link_of_other_project(client):  # noqa: F811
    a, _, _ = _seed(client)
    b, _, _ = _seed(client)
    [link_b] = client.get(f"/projects/{b}/share-links").json()
    assert client.post(f"/projects/{a}/share-links/{link_b['id']}/revoke").status_code == 404


def test_actions_are_audited_without_content(client):  # noqa: F811
    _seed(client)
    s = _session()
    actions = {a.action for a in s.scalars(select(m.AuditLog))}
    assert {"version_uploaded", "element_added", "share_created"} <= actions
    for a in s.scalars(select(m.AuditLog)):
        assert RQ_OLD not in a.meta_json  # isi penelitian tidak masuk audit
