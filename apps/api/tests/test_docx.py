import zipfile
from io import BytesIO

import pytest

from app.parsing.detect import detect
from app.parsing.docx import DocxError, parse_docx

NS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'


def _p(text: str, style: str | None = None, comment: str | None = None) -> str:
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
    start = f'<w:commentRangeStart w:id="{comment}"/>' if comment else ""
    return f"<w:p>{ppr}{start}<w:r><w:t>{text}</w:t></w:r></w:p>"


def make_docx(body: str, comments: str | None = None) -> bytes:
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("[Content_Types].xml", "<Types/>")
        z.writestr("word/document.xml", f"<w:document {NS}><w:body>{body}</w:body></w:document>")
        if comments is not None:
            z.writestr("word/comments.xml", f"<w:comments {NS}>{comments}</w:comments>")
    return buf.getvalue()


SAMPLE = make_docx(
    _p("BAB I PENDAHULUAN", "Heading1")
    + _p("Bagaimana pengaruh metode X terhadap hasil belajar?", comment="0")
    + _p("BAB III METODE", "Heading1")
    + _p("Desain one-group pre-test/post-test.")
    + "<w:tbl><w:tr><w:tc>"
    + _p("Variabel")
    + "</w:tc><w:tc>"
    + _p("Instrumen")
    + "</w:tc></w:tr></w:tbl>",
    comments=(
        '<w:comment w:id="0" w:author="Pembimbing 1" w:date="2026-11-20T10:00:00Z">'
        + _p("Metodenya coba diperjelas.")
        + "</w:comment>"
    ),
)


def test_detected_as_docx():
    assert detect(SAMPLE) == "docx"


def test_detected_even_when_word_entries_come_late():
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("docProps/padding.bin", bytes(8000))  # dorong word/ jauh ke belakang
        z.writestr("word/document.xml", f"<w:document {NS}><w:body/></w:document>")
    assert detect(buf.getvalue()) == "docx"


def test_other_zip_is_not_docx():
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("xl/workbook.xml", "<x/>")
    assert detect(buf.getvalue()) is None


def test_blocks_headings_and_tables():
    out = parse_docx(SAMPLE)
    types = [b["type"] for b in out["blocks"]]
    assert types == ["heading", "paragraph", "heading", "paragraph", "table"]
    assert out["blocks"][0]["level"] == 1
    assert out["blocks"][-1]["text"] == "Variabel | Instrumen"


def test_sections_split_by_heading_not_pages():
    out = parse_docx(SAMPLE)
    assert out["unit"] == "section"
    assert "pengaruh metode X" in out["pages"]["1"]
    assert "one-group" in out["pages"]["2"] and "Variabel" in out["pages"]["2"]


def test_comment_with_author_and_anchor():
    [c] = parse_docx(SAMPLE)["comments"]
    assert (c["author"], c["text"], c["anchor_block"]) == (
        "Pembimbing 1",
        "Metodenya coba diperjelas.",
        1,
    )


def test_docx_without_comments():
    assert parse_docx(make_docx(_p("Isi")))["comments"] == []


def test_indonesian_heading_style_is_recognised():
    out = parse_docx(make_docx(_p("BAB I", "Judul1") + _p("isi")))
    assert out["blocks"][0]["type"] == "heading"


@pytest.mark.parametrize("data", [b"PK\x03\x04 rusak word/", make_docx("<w:p>")])
def test_broken_docx_raises(data):
    with pytest.raises(DocxError):
        parse_docx(data)


def test_entity_expansion_is_refused():
    evil = (
        '<?xml version="1.0"?><!DOCTYPE d [<!ENTITY a "aaaa">]>'
        f"<w:document {NS}><w:body>{_p('&a;')}</w:body></w:document>"
    )
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("word/document.xml", evil)
    with pytest.raises(DocxError):  # defusedxml menolak entitas -> 422, bukan 500
        parse_docx(buf.getvalue())
