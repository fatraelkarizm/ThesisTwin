from typing import Protocol


class LLMClient(Protocol):
    """Satu-satunya antarmuka ke LLM. Provider nyata ditambahkan setelah ADR-003."""

    def complete_json(self, prompt: str) -> str:
        """Kembalikan string JSON mentah; validasi dilakukan pemanggil."""
        ...
