"""Penyimpanan file unggahan. Lokal untuk sekarang; S3-compatible menyusul (technical-design §3)."""

import shutil
from pathlib import Path


class LocalStorage:
    def __init__(self, base_dir: str | Path) -> None:
        self.base = Path(base_dir)

    def save(self, key: str, data: bytes) -> None:
        path = self.base / key
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def read(self, key: str) -> bytes:
        return (self.base / key).read_bytes()

    def delete_prefix(self, prefix: str) -> None:
        """Hapus semua file di bawah prefix (mis. id proyek). Aman bila tidak ada."""
        target = (self.base / prefix).resolve()
        if self.base.resolve() not in target.parents:
            raise ValueError("prefix di luar folder penyimpanan")
        shutil.rmtree(target, ignore_errors=True)
