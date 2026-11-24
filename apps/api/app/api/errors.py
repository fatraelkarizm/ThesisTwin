"""Satu tempat memetakan error domain/service ke HTTP, agar router tetap tipis."""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.domain.status import InvalidTransition
from app.services import documents as docs
from app.services import review, share
from app.services.findings import FindingNotFound

_MAP: dict[type[Exception], tuple[int, str]] = {
    docs.ProjectNotFound: (status.HTTP_404_NOT_FOUND, "Proyek tidak ditemukan."),
    FindingNotFound: (status.HTTP_404_NOT_FOUND, "Temuan tidak ditemukan."),
    review.VersionNotFound: (status.HTTP_404_NOT_FOUND, "Versi tidak ditemukan."),
    share.LinkInvalid: (
        status.HTTP_404_NOT_FOUND,
        "Tautan tidak berlaku (salah, kedaluwarsa, atau dicabut). Minta tautan baru ke mahasiswa.",
    ),
    docs.ConsentRequired: (status.HTTP_403_FORBIDDEN, "Berikan persetujuan sebelum mengunggah."),
    docs.UnsupportedFile: (
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Format belum didukung. Unggah PDF atau DOCX.",
    ),
    docs.UnreadableFile: (
        status.HTTP_422_UNPROCESSABLE_CONTENT,
        "File tidak bisa dibaca. Coba ekspor ulang.",
    ),
    InvalidTransition: (status.HTTP_409_CONFLICT, "Perubahan status ini tidak diizinkan."),
}


def register(app: FastAPI) -> None:
    for exc_type, (code, message) in _MAP.items():

        async def handler(_: Request, __: Exception, code: int = code, message: str = message):
            return JSONResponse(status_code=code, content={"detail": message})

        app.add_exception_handler(exc_type, handler)
