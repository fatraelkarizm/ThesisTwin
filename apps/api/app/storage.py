"""Penyimpanan file unggahan. Lokal untuk sekarang; S3-compatible menyusul (technical-design §3)."""

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
