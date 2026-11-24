"""Uji asap semua fitur pada API yang sedang berjalan (bukan TestClient).

Jalankan dari apps/api:  python -m scripts.smoke [http://localhost:8000]
Data sintetis berlabel; proyek uji dihapus di akhir. Keluar dengan kode 1 bila ada yang gagal.
"""

import json
import sys
import urllib.error
import urllib.request
import uuid

from tests.test_docx import _p, make_docx
from tests.test_pdf import _pdf

API = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
results: list[tuple[str, bool, str]] = []


def call(method: str, path: str, body=None, file: tuple[str, bytes] | None = None, raw=False):
    headers, data = {}, None
    if file:
        b = uuid.uuid4().hex
        data = (
            (
                f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="{file[0]}"\r\n'
                "Content-Type: application/octet-stream\r\n\r\n"
            ).encode()
            + file[1]
            + f"\r\n--{b}--\r\n".encode()
        )
        headers["Content-Type"] = f"multipart/form-data; boundary={b}"
    elif body is not None:
        data, headers["Content-Type"] = json.dumps(body).encode(), "application/json"
    req = urllib.request.Request(API + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            text = r.read().decode()
            return r.status, (text if raw else (json.loads(text) if text else None))
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, bool(ok), detail))


RQ1 = "Bagaimana pengaruh model PBL terhadap kemampuan pemecahan masalah siswa?"
RQ2 = "Bagaimana perubahan kemampuan pemecahan masalah siswa setelah model PBL?"
METHOD = "Penelitian ini memakai desain one-group pre-test/post-test pada satu kelas."
ANALYSIS = "Analisis membandingkan rata-rata skor sebelum dan sesudah perlakuan."
COMMENT = (
    '<w:comment w:id="1" w:author="Pembimbing (contoh)" w:date="2026-11-20T10:00:00Z">'
    + _p("Kata pengaruh terlalu kuat untuk desain ini.")
    + "</w:comment>"
)


def doc(rq: str, comment: bool) -> bytes:
    body = (
        _p("Rumusan Masalah", "Heading1")
        + _p(f"1. {rq}", comment="1" if comment else None)
        + _p("2. Bagaimana respons siswa terhadap model PBL?")
        + _p("Tujuan Penelitian", "Heading1")
        + _p("1. Mengukur kemampuan pemecahan masalah siswa sebelum dan sesudah PBL.")
        + _p("Desain Penelitian", "Heading1")
        + _p(METHOD)
        + _p("Teknik Analisis Data", "Heading1")
        + _p(ANALYSIS)
    )
    return make_docx(body, COMMENT if comment else None)


def main() -> int:
    s, health = call("GET", "/health")
    check("API hidup", s == 200 and health == {"status": "ok"})

    s, p = call(
        "POST", "/projects", {"title": "[UJI ASAP] Proposal sintetis", "program": "matematika"}
    )
    pid = p["id"]
    s, _ = call("POST", f"/projects/{pid}/documents", file=("p.pdf", _pdf(["x"])))
    check("Unggah ditolak tanpa consent", s == 403, f"status {s}")
    call("POST", f"/projects/{pid}/consent")

    s, up1 = call("POST", f"/projects/{pid}/documents", file=("v1.docx", doc(RQ1, comment=True)))
    v1 = up1["version"]["id"]
    check(
        "Unggah DOCX v1 + ekstraksi otomatis",
        s == 201 and up1["auto_elements"] >= 4,
        f"{up1.get('auto_elements')} elemen, {up1.get('findings')} temuan",
    )
    s, again = call("POST", f"/projects/{pid}/documents", file=("v1.docx", doc(RQ1, comment=True)))
    check("Unggah ulang isi sama tidak membuat versi", again["created"] is False)

    _, els = call("GET", f"/versions/{v1}/elements")
    check(
        "Elemen otomatis terverifikasi",
        els and all(e["verified"] for e in els),
        f"{len(els)} elemen",
    )
    _, manual = call(
        "POST",
        f"/versions/{v1}/elements",
        {
            "type": "claim",
            "content": "Kalimat karangan",
            "quote": "tidak ada di dokumen",
            "page": 1,
        },
    )
    check(
        "Kutipan karangan ditolak verifikasi",
        manual["verified"] is False and manual["status"] == "needs_user_confirmation",
    )

    _, findings = call("POST", f"/versions/{v1}/check")
    rules = {f["rule_id"] for f in findings}
    check(
        "Cek konsistensi: aturan kausal & uji statistik",
        {"R-CAUSAL-01", "R-STAT-TEST"} <= rules,
        ", ".join(sorted(rules)),
    )
    causal = next(f for f in findings if f["rule_id"] == "R-CAUSAL-01")
    check(
        "Temuan membawa rujukan + arah + halaman",
        causal["references"]
        and len(causal["directions"]) >= 2
        and all(e["page"] for e in causal["evidence"]),
        f"{len(causal['references'])} rujukan",
    )

    _, graph = call("GET", f"/versions/{v1}/graph")
    check(
        "Dependency graph",
        graph["nodes"] and graph["edges"],
        f"{len(graph['nodes'])} node, {len(graph['edges'])} edge",
    )

    _, conf = call("POST", f"/findings/{causal['id']}/status", {"target": "student_confirmed"})
    check("Konfirmasi mahasiswa", conf["status"] == "student_confirmed")
    s, _ = call("POST", f"/findings/{causal['id']}/status", {"target": "resolved"})
    check("Transisi tidak sah ditolak (409)", s == 409, f"status {s}")

    _, qs = call("POST", f"/versions/{v1}/stress-test")
    check("Stress-Test 3–5 pertanyaan", 3 <= len(qs) <= 5, f"{len(qs)} pertanyaan")
    call("POST", f"/stress-questions/{qs[0]['id']}/answer", {"answer": "Jawaban uji."})
    _, regen = call("POST", f"/versions/{v1}/stress-test?regenerate=true")
    check(
        "Jawaban tetap ada setelah pertanyaan diperbarui",
        any(q["answer"] == "Jawaban uji." for q in regen),
    )

    s, up2 = call("POST", f"/projects/{pid}/documents", file=("v2.docx", doc(RQ2, comment=False)))
    check("Unggah v2", s == 201 and up2["version"]["version_no"] == 2)
    _, comments = call("GET", f"/projects/{pid}/comments")
    check(
        "Komentar dosen: kemungkinan ditangani",
        comments and comments[0]["state"] == "possibly_addressed",
    )
    call("POST", f"/versions/{v1}/comments/1", {"addressed": True})

    _, brief = call("GET", f"/projects/{pid}/brief")
    check(
        "Brief: perubahan antarversi",
        any(c.startswith("Diubah — Rumusan masalah") for c in brief["changes"]),
    )
    check("Brief: dampak perubahan", bool(brief["impacts"]), f"{len(brief['impacts'])} dampak")
    s, text = call("GET", f"/projects/{pid}/brief.txt", raw=True)
    check("Brief teks chat", s == 200 and "Bukan penilaian" in text)

    _, share = call("POST", f"/projects/{pid}/share")
    token = share["token"]
    s, shared = call("GET", f"/share/{token}")
    check("Tautan dosen tanpa akun", s == 200 and shared["to_version"] == 2)
    s, rated = call("POST", f"/share/{token}/stress-questions/{qs[0]['id']}/rating", {"score": 4})
    check("Rating dosen 1–5", s == 200 and rated["rating"] == 4)
    _, links = call("GET", f"/projects/{pid}/share-links")
    call("POST", f"/projects/{pid}/share-links/{links[0]['id']}/revoke")
    s, _ = call("GET", f"/share/{token}")
    check("Tautan dicabut tidak berlaku", s == 404)

    tex = (
        b"\\documentclass{article}\\begin{document}\\section{Pendahuluan} "
        b"Lihat Lemma~\\ref{lem:x}.\\end{document}"
    )
    s, up3 = call("POST", f"/projects/{pid}/documents", file=("p.tex", tex))
    check("Unggah .tex", s == 201 and up3["version"]["media_type"] == "application/x-tex")

    s, _ = call("DELETE", f"/projects/{pid}")
    s2, _ = call("GET", f"/projects/{pid}")
    check("Hapus permanen", s == 204 and s2 == 404)

    width = max(len(n) for n, _, _ in results)
    for name, ok, detail in results:
        print(f"{'LULUS' if ok else 'GAGAL'}  {name.ljust(width)}  {detail}")
    failed = sum(not ok for _, ok, _ in results)
    print(f"\n{len(results) - failed}/{len(results)} lulus")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
