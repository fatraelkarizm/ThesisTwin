"""Alur setelah unggah: simpan versi -> ekstraksi otomatis berbasis struktur bab -> cek aturan.

Dengan ini Tools (cek konsistensi, graph, brief, stress-test) langsung berisi hasil setelah
unggah, tanpa LLM. Elemen otomatis bersumber "auto" dan tetap harus dikonfirmasi mahasiswa.
"""

import json
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.domain.structure import extract_by_structure
from app.services import review
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

    pages = {int(k): v for k, v in json.loads(version.parsed_json).get("pages", {}).items()}
    extracted = extract_by_structure(pages)
    for e in extracted:
        review.add_element(session, version.id, e.type, e.content, e.quote, e.page, source="auto")
    findings = review.run_check(session, version.id) if extracted else []
    return UploadResult(added, len(extracted), len(findings))
