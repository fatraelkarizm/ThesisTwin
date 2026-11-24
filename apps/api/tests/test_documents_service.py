import pytest
from sqlalchemy.orm import Session

from app.db.session import init_db, make_engine
from app.services.documents import (
    ConsentRequired,
    ProjectNotFound,
    add_version,
    create_project,
    give_consent,
)
from app.storage import LocalStorage


@pytest.fixture
def session():
    engine = make_engine("sqlite://")
    init_db(engine)
    with Session(engine) as s:
        yield s


@pytest.fixture
def storage(tmp_path):
    return LocalStorage(tmp_path)


def _add(session, storage, project_id, data: bytes):
    return add_version(
        session,
        storage,
        project_id,
        "p.pdf",
        "application/pdf",
        data,
        {"pages": {"1": data.decode()}},  # isi terbaca mengikuti data
    )


def test_upload_without_consent_is_refused(session, storage):
    p = create_project(session, "Skripsi", "matematika")
    with pytest.raises(ConsentRequired):
        _add(session, storage, p.id, b"v1")


def test_versions_are_numbered_and_appended(session, storage, tmp_path):
    p = create_project(session, "Skripsi", "matematika")
    give_consent(session, p.id)
    v1 = _add(session, storage, p.id, b"isi v1")
    v2 = _add(session, storage, p.id, b"isi v2")
    assert (v1.created, v1.version.version_no) == (True, 1)
    assert (v2.created, v2.version.version_no) == (True, 2)
    assert storage.read(v1.version.storage_key) == b"isi v1"  # v1 tidak tertimpa
    assert storage.read(v2.version.storage_key) == b"isi v2"


def test_same_content_as_latest_does_not_create_version(session, storage):
    p = create_project(session, "Skripsi", "matematika")
    give_consent(session, p.id)
    first = _add(session, storage, p.id, b"sama")
    again = _add(session, storage, p.id, b"sama")
    assert again.created is False and again.version.id == first.version.id


def test_reverting_to_older_content_is_a_new_version(session, storage):
    p = create_project(session, "Skripsi", "matematika")
    give_consent(session, p.id)
    _add(session, storage, p.id, b"A")
    _add(session, storage, p.id, b"B")
    back = _add(session, storage, p.id, b"A")
    assert back.created and back.version.version_no == 3


def test_unknown_project(session, storage):
    with pytest.raises(ProjectNotFound):
        _add(session, storage, "nope", b"x")
