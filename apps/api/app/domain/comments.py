"""Apakah komentar dosen di versi lama sudah ditindaklanjuti di versi baru (Langkah 19).

Deterministik dan sengaja rendah hati: kode hanya bisa melihat apakah **teks yang dikomentari
berubah**. Berubah != sudah benar. Karena itu hasilnya "kemungkinan ditangani" dan selalu
butuh konfirmasi mahasiswa (lalu dosen lewat brief).
"""

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from app.domain.diff import similarity

UNCHANGED = 0.95


class CommentState(StrEnum):
    POSSIBLY_ADDRESSED = "possibly_addressed"  # bagian yang dikomentari berubah/hilang
    NOT_ADDRESSED = "not_addressed"  # bagian yang dikomentari masih sama
    UNKNOWN = "unknown"  # komentar tidak menempel ke paragraf tertentu


@dataclass(frozen=True)
class CommentStatus:
    comment_id: str
    author: str
    text: str
    anchor_text: str | None
    state: CommentState
    confirmed: bool | None = None  # jawaban mahasiswa; None = belum dikonfirmasi


def comment_statuses(
    old_blocks: list[dict[str, Any]],
    comments: list[dict[str, Any]],
    new_blocks: list[dict[str, Any]],
    confirmations: dict[str, bool] | None = None,
) -> list[CommentStatus]:
    by_index = {b["index"]: b["text"] for b in old_blocks}
    new_texts = [b["text"] for b in new_blocks]
    confirmations = confirmations or {}
    out = []
    for c in comments:
        anchor = by_index.get(c.get("anchor_block"))
        if anchor is None:
            state = CommentState.UNKNOWN
        else:
            best = max((similarity(anchor, t) for t in new_texts), default=0.0)
            state = (
                CommentState.NOT_ADDRESSED if best >= UNCHANGED else CommentState.POSSIBLY_ADDRESSED
            )
        out.append(
            CommentStatus(
                comment_id=c["id"],
                author=c.get("author", ""),
                text=c.get("text", ""),
                anchor_text=anchor,
                state=state,
                confirmed=confirmations.get(c["id"]),
            )
        )
    return out
