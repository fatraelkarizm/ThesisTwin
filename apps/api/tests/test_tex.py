from app.parsing.detect import detect
from app.parsing.tex import parse_tex

DOC = rb"""
\documentclass{article}
\newcommand{\R}{\mathbb{R}}
\begin{document}
Pembuka singkat.
\section{Pendahuluan}
Rumusan masalah: apakah $f:\R\to\R$ kontinu? % komentar penulis \ref{tidakdihitung}
\section{Kajian Teori}
\begin{definisi}[Kontinu]\label{def:kontinu}
Fungsi $f$ kontinu di $a$ jika $\lim_{x\to a} f(x) = f(a)$.
\end{definisi}
\begin{theorem}\label{thm:utama}
Menurut Definisi~\ref{def:kontinu} dan Lemma~\ref{lem:hilang}, ...
\end{theorem}
\label{def:kontinu}
\end{document}
"""


def test_detected_as_tex():
    assert detect(DOC) == "tex"
    assert detect(b"teks biasa tanpa latex") is None


def test_sections_and_headings():
    out = parse_tex(DOC)
    assert out["unit"] == "section"
    assert "Pembuka" in out["pages"]["1"]
    assert [h["title"] for h in out["headings"]] == ["Pendahuluan", "Kajian Teori"]
    assert out["headings"][0]["section"] == 2


def test_environments_keep_math_verbatim():
    envs = parse_tex(DOC)["environments"]
    assert [(e["kind"], e["label"]) for e in envs] == [
        ("definisi", "def:kontinu"),
        ("theorem", "thm:utama"),
    ]
    assert r"\lim_{x\to a} f(x) = f(a)" in envs[0]["text"]


def test_broken_and_duplicate_labels():
    out = parse_tex(DOC)
    assert out["broken_refs"] == ["lem:hilang"]  # ref di komentar % tidak dihitung
    assert out["duplicate_labels"] == ["def:kontinu"]
    assert out["macros"] == ["R"]


def test_no_headings_is_one_section():
    out = parse_tex(b"\\documentclass{x} isi tanpa bagian")
    assert list(out["pages"]) == ["1"]
