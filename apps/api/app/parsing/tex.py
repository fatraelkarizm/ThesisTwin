"""LaTeX (.tex) -> bagian, lingkungan teorema, label/ref, notasi (Langkah 7b). Tanpa LLM.

Persamaan disimpan apa adanya; tidak dikirim ke LLM untuk "dirapikan".
Bukan parser LaTeX penuh: makro buatan sendiri yang rumit bisa lolos; ini cukup untuk
struktur proposal dan pemeriksaan rujukan silang.
"""

import re
from typing import Any

_COMMENT = re.compile(r"(?<!\\)%.*")
_SECTION = re.compile(r"\\(chapter|section|subsection|subsubsection)\*?\{([^}]*)\}")
_ENV = re.compile(
    r"\\begin\{(theorem|lemma|definition|proposition|corollary|teorema|definisi|proposisi|akibat|"
    r"conjecture|example|contoh)\}(?:\[([^\]]*)\])?(.*?)\\end\{\1\}",
    re.S,
)
_LABEL = re.compile(r"\\label\{([^}]+)\}")
_REF = re.compile(r"\\(?:eq|auto|c|C|page)?ref\{([^}]+)\}")
_NEWCOMMAND = re.compile(r"\\(?:re)?newcommand\{?\\(\w+)\}?(?:\[\d\])?\{")


class TexError(ValueError):
    pass


def looks_like_tex(data: bytes) -> bool:
    head = data[:20000]
    return any(m in head for m in (b"\\documentclass", b"\\begin{document}", b"\\section{"))


def parse_tex(data: bytes) -> dict[str, Any]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        text = data.decode("latin-1")
    text = "\n".join(_COMMENT.sub("", line) for line in text.splitlines())
    macros = sorted(set(_NEWCOMMAND.findall(text)))  # biasanya di preamble
    if "\\begin{document}" in text:
        text = text.split("\\begin{document}", 1)[1].split("\\end{document}", 1)[0]

    # Bagian = potongan per heading; teks sebelum heading pertama (bila ada) = bagian 1.
    marks = list(_SECTION.finditer(text))
    cuts = [m.start() for m in marks]
    if not marks or text[: marks[0].start()].strip():
        cuts = [0, *cuts]
    sections: dict[str, str] = {}
    for n, start in enumerate(cuts, start=1):
        end = cuts[n] if n < len(cuts) else len(text)
        sections[str(n)] = text[start:end].strip()
    offset = len(cuts) - len(marks)  # 1 bila ada pembuka tanpa heading
    headings = [
        {"section": i + 1 + offset, "level": m.group(1), "title": m.group(2).strip()}
        for i, m in enumerate(marks)
    ]

    labels = _LABEL.findall(text)
    refs = _REF.findall(text)
    dup = sorted({lb for lb in labels if labels.count(lb) > 1})
    environments = [
        {
            "kind": m.group(1),
            "title": (m.group(2) or "").strip(),
            "label": (_LABEL.search(m.group(3)) or [None, None])[1],
            "text": m.group(3).strip(),
        }
        for m in _ENV.finditer(text)
    ]
    return {
        "kind": "tex",
        "unit": "section",
        "pages": sections,
        "headings": headings,
        "environments": environments,
        "labels": sorted(set(labels)),
        "duplicate_labels": dup,
        "broken_refs": sorted({r for r in refs if r not in labels}),
        "macros": macros,
    }
