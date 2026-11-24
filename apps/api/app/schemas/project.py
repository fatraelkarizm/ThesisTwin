from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProjectIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    program: str = Field(min_length=1, max_length=80)


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    program: str
    consent_at: datetime | None


class VersionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    version_no: int
    filename: str
    media_type: str
    sha256: str
    uploaded_at: datetime

    @field_validator("uploaded_at")
    @classmethod
    def _as_utc(cls, v: datetime) -> datetime:
        # SQLite membuang zona waktu; semua waktu disimpan dalam UTC.
        return v if v.tzinfo else v.replace(tzinfo=UTC)


class UploadOut(BaseModel):
    version: VersionOut
    created: bool
    pages: int
    auto_elements: int = 0  # elemen terdeteksi dari struktur bab
    findings: int = 0


class ShareLinkOut(BaseModel):
    """Tanpa token: token hanya ditampilkan sekali saat dibuat."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    expires_at: datetime
    revoked: bool

    @field_validator("created_at", "expires_at")
    @classmethod
    def _as_utc(cls, v: datetime) -> datetime:
        return v if v.tzinfo else v.replace(tzinfo=UTC)
