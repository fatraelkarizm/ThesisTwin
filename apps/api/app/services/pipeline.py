"""Alur setelah unggah: simpan versi -> ekstraksi otomatis berbasis struktur bab -> cek aturan.

Dengan ini Tools (cek konsistensi, graph, brief, stress-test) langsung berisi hasil setelah
unggah, tanpa LLM. Elemen otomatis bersumber "auto" dan tetap harus dikonfirmasi mahasiswa.
"""

import json
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.db.models import DocumentVersion
from app.domain.rules import normalize
from app.domain.structure import extract_by_structure
from app.services import config, review
from app.services.documents import AddedVersion, ingest_upload
from app.storage import LocalStorage


@dataclass(frozen=True)
class UploadResult:
    added: AddedVersion
    auto_elements: int
    findings: int


def process_upload(
    session: Session, storage: LocalStorage, project_id: str, filename: str, data: bytes
) -> UploadResult:
    added = ingest_upload(session, storage, project_id, filename, data)
    version = added.version
    if not added.created:  # isi sama dengan versi terakhir: tidak ada yang perlu diproses ulang
        return UploadResult(added, 0, len(review.list_findings(session, version.id)))

    count = _extract_missing(session, version)
    findings = review.run_check(session, version.id) if count else []
    return UploadResult(added, count, len(findings))


@dataclass(frozen=True)
class ReextractResult:
    added: int
    findings: int


def reextract(session: Session, version_id: str) -> ReextractResult:
    """Baca ulang versi yang sudah ada dengan kosakata ekstraksi terbaru. Hanya menambah elemen
    yang belum ada; elemen lama (termasuk yang sudah dikonfirmasi) tidak diubah atau dihapus."""
    version = review.get_version(session, version_id)
    added = _extract_missing(session, version)
    if added:
        findings = len(review.run_check(session, version.id))
    else:
        findings = len(review.list_findings(session, version.id))
    return ReextractResult(added, findings)


def _extract_missing(session: Session, version: DocumentVersion) -> int:
    pages = {int(k): v for k, v in json.loads(version.parsed_json).get("pages", {}).items()}
    seen = {(e.type, normalize(e.quote)) for e in review.list_elements(session, version.id)}
    added = 0
    for e in extract_by_structure(pages, config.extraction()):
        key = (e.type, normalize(e.quote))
        if key in seen:
            continue
        seen.add(key)
        review.add_element(session, version.id, e.type, e.content, e.quote, e.page, source="auto")
        added += 1
    return added
