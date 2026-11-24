import json
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_storage
from app.core.config import settings
from app.db.session import get_session
from app.schemas.project import ProjectIn, ProjectOut, ShareLinkOut, UploadOut, VersionOut
from app.services import documents as svc
from app.services import pipeline, privacy
from app.storage import LocalStorage

router = APIRouter(prefix="/projects", tags=["projects"])

SessionDep = Annotated[Session, Depends(get_session)]
StorageDep = Annotated[LocalStorage, Depends(get_storage)]


@router.post("", status_code=status.HTTP_201_CREATED)
def create_project(body: ProjectIn, session: SessionDep) -> ProjectOut:
    return ProjectOut.model_validate(svc.create_project(session, body.title, body.program))


@router.post("/{project_id}/consent")
def give_consent(project_id: str, session: SessionDep) -> ProjectOut:
    return ProjectOut.model_validate(svc.give_consent(session, project_id))


@router.post("/{project_id}/documents", status_code=status.HTTP_201_CREATED)
async def upload(
    project_id: str, file: UploadFile, session: SessionDep, storage: StorageDep
) -> UploadOut:
    limit = settings.max_upload_mb * 1024 * 1024
    data = await file.read(limit + 1)
    if len(data) > limit:
        raise HTTPException(
            status.HTTP_413_CONTENT_TOO_LARGE, f"Maksimal {settings.max_upload_mb} MB."
        )
    result = pipeline.process_upload(session, storage, project_id, file.filename or "dokumen", data)
    pages = len(json.loads(result.added.version.parsed_json).get("pages", {}))
    return UploadOut(
        version=VersionOut.model_validate(result.added.version),
        created=result.added.created,
        pages=pages,
        auto_elements=result.auto_elements,
        findings=result.findings,
    )


@router.get("/{project_id}")
def get_project(project_id: str, session: SessionDep) -> ProjectOut:
    return ProjectOut.model_validate(svc.get_project(session, project_id))


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: str, session: SessionDep, storage: StorageDep) -> None:
    privacy.delete_project(session, storage, project_id)


@router.get("/{project_id}/share-links")
def list_links(project_id: str, session: SessionDep) -> list[ShareLinkOut]:
    return [ShareLinkOut.model_validate(x) for x in privacy.list_links(session, project_id)]


@router.post("/{project_id}/share-links/{link_id}/revoke")
def revoke_link(project_id: str, link_id: str, session: SessionDep) -> ShareLinkOut:
    return ShareLinkOut.model_validate(privacy.revoke_link(session, project_id, link_id))


@router.get("/{project_id}/versions")
def list_versions(project_id: str, session: SessionDep) -> list[VersionOut]:
    return [VersionOut.model_validate(v) for v in svc.list_versions(session, project_id)]
