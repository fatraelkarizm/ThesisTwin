"""DOCX -> blok (heading/paragraf/tabel), bagian, dan komentar pembimbing.

DOCX tidak punya nomor halaman tetap (bergantung renderer). Karena itu lokasi sumber DOCX
memakai **nomor bagian** (dipotong per heading), bukan halaman. UI harus menyebut "bagian",
bukan "hal.", untuk dokumen DOCX.
"""

import zipfile
from dataclasses import asdict, dataclass
from io import BytesIO
from typing import Any
from xml.etree.ElementTree import Element

from defusedxml import DefusedXmlException, ElementTree

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
_MAX_XML_BYTES = 50 * 1024 * 1024  # tolak zip bomb


class DocxError(ValueError):
    pass


@dataclass
class Block:
    index: int
    type: str  # heading | paragraph | table
    text: str
    level: int | None = None


@dataclass
class Comment:
    id: str
    author: str
    date: str | None
    text: str
    anchor_block: int | None  # blok tempat komentar menempel


def _text(el: Element) -> str:
    return "".join(t.text or "" for t in el.iter(f"{W}t")).strip()


def _heading_level(p: Element) -> int | None:
    style = p.find(f"{W}pPr/{W}pStyle")
    if style is None:
        return None
    val = (style.get(f"{W}val") or "").lower()
    for prefix in ("heading", "judul"):
        if val.startswith(prefix):
            digits = val[len(prefix) :]
            return int(digits) if digits.isdigit() else 1
    return None


def _read_xml(z: zipfile.ZipFile, name: str) -> Element | None:
    try:
        info = z.getinfo(name)
    except KeyError:
        return None
    if info.file_size > _MAX_XML_BYTES:
        raise DocxError(f"{name} terlalu besar")
    return ElementTree.fromstring(z.read(name))


def parse_docx(data: bytes) -> dict[str, Any]:
    try:
        z = zipfile.ZipFile(BytesIO(data))
        doc = _read_xml(z, "word/document.xml")
        comments_xml = _read_xml(z, "word/comments.xml")
    except (zipfile.BadZipFile, ElementTree.ParseError, DefusedXmlException) as exc:
        raise DocxError(str(exc)) from exc
    if doc is None:
        raise DocxError("word/document.xml tidak ada")
    body = doc.find(f"{W}body")
    if body is None:
        raise DocxError("dokumen kosong")

    blocks: list[Block] = []
    anchors: dict[str, int] = {}
    for el in body:
        idx = len(blocks)
        if el.tag == f"{W}p":
            for start in el.iter(f"{W}commentRangeStart"):
                anchors.setdefault(start.get(f"{W}id") or "", idx)
            text = _text(el)
            if not text:
                continue
            level = _heading_level(el)
            blocks.append(Block(idx, "heading" if level else "paragraph", text, level))
        elif el.tag == f"{W}tbl":
            for start in el.iter(f"{W}commentRangeStart"):
                anchors.setdefault(start.get(f"{W}id") or "", idx)
            rows = [
                " | ".join(_text(cell) for cell in row.findall(f"{W}tc"))
                for row in el.findall(f"{W}tr")
            ]
            blocks.append(Block(idx, "table", "\n".join(rows)))

    comments = [
        Comment(
            id=c.get(f"{W}id") or "",
            author=c.get(f"{W}author") or "",
            date=c.get(f"{W}date"),
            text=_text(c),
            anchor_block=anchors.get(c.get(f"{W}id") or ""),
        )
        for c in (comments_xml.findall(f"{W}comment") if comments_xml is not None else [])
    ]

    # Bagian = potongan per heading. Teks sebelum heading pertama = bagian 1.
    sections: dict[str, str] = {}
    current = 1 if blocks and blocks[0].type != "heading" else 0
    for b in blocks:
        if b.type == "heading":
            current += 1
        key = str(max(current, 1))
        sections[key] = f"{sections.get(key, '')}\n{b.text}".strip()

    return {
        "kind": "docx",
        "unit": "section",
        "pages": sections,
        "blocks": [asdict(b) for b in blocks],
        "comments": [asdict(c) for c in comments],
    }
