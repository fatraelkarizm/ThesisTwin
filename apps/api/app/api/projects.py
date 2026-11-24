import json
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_storage
from app.core.config import settings
from app.db.session import get_session
from app.schemas.project import ProjectIn, ProjectOut, UploadOut, VersionOut
from app.services import documents as svc
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
    added = svc.ingest_upload(session, storage, project_id, file.filename or "dokumen", data)
    pages = len(json.loads(added.version.parsed_json).get("pages", {}))
    return UploadOut(
        version=VersionOut.model_validate(added.version), created=added.created, pages=pages
    )


@router.get("/{project_id}/versions")
def list_versions(project_id: str, session: SessionDep) -> list[VersionOut]:
    return [VersionOut.model_validate(v) for v in svc.list_versions(session, project_id)]
