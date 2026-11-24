"""Defense Stress-Test (abstrak §4 langkah 4; Langkah 22).

Tautan terlemah graph -> 3–5 pertanyaan penguji. Deterministik: pemilihan dengan skor yang bisa
dijelaskan, pertanyaan dari templat. Pertanyaan tidak pernah berisi jawabannya.
"""

from dataclasses import dataclass, field

from app.domain.brief import TYPE_LABEL
from app.domain.graph import Graph
from app.domain.rules import Element

MIN_Q, MAX_Q = 3, 5
PRIORITY = {"high": 2, "medium": 1, "low": 0}
PRIORITY_LABEL = {"high": "tinggi", "medium": "sedang", "low": "rendah"}
FINDING_TYPES = ("research_question", "objective", "variable", "method", "analysis", "instrument")
CLOSED = {"rejected", "resolved"}


@dataclass(frozen=True)
class FindingRef:
    rule_id: str
    priority: str
    status: str
    element_ids: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Question:
    key: str  # dedupe: satu pertanyaan per sumber kelemahan
    kind: str  # finding | gap | unverified | baseline
    text: str
    reason: str  # mengapa pertanyaan ini dipilih (ditampilkan ke mahasiswa dan dosen)
    element_ids: tuple[str, ...]
    score: int


def _short(text: str, n: int = 90) -> str:
    text = " ".join(text.split())
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


def _first(els: list[Element], type_: str) -> Element | None:
    return next((e for e in els if e.type == type_), None)


FINDING_Q = {
    "R-CAUSAL-01": (
        "Pertanyaan Anda bersifat sebab-akibat, sedangkan desainnya “{method}”. Mengapa desain ini "
        "cukup untuk menyimpulkan pengaruh, dan ancaman validitas apa yang Anda kendalikan?"
    ),
    "R-RQ-OBJ": (
        "Tujuan penelitian mana yang menjawab “{research_question}”, dan bagaimana Anda tahu "
        "tujuan itu tercapai?"
    ),
    "R-OBJ-ANALYSIS": (
        "Dengan analisis apa tujuan “{objective}” dicapai, dan mengapa analisis itu cocok dengan "
        "jenis datanya?"
    ),
    "R-VAR-INSTR": (
        "Bagaimana “{variable}” diukur, dan apa bukti validitas serta reliabilitas instrumennya?"
    ),
    "R-PROPOSAL-RESULTS": (
        "Proposal Anda sudah memuat hasil dan kesimpulan. Dari mana angka hasil itu diperoleh, "
        "dan bagaimana Anda menjamin rencana penelitian tidak disesuaikan dengan hasil yang sudah "
        "ditulis?"
    ),
    "R-RQ-OBJ-COUNT": (
        "Jumlah rumusan masalah dan tujuan Anda berbeda. Tujuan mana menjawab rumusan masalah yang "
        "mana, dan apakah ada tujuan yang sebenarnya manfaat atau keluaran penelitian?"
    ),
    "R-CONCL-SCOPE": (
        "Sampel Anda terbatas. Sampai sejauh mana hasil boleh digeneralisasi, dan bagaimana Anda "
        "membatasi klaimnya?"
    ),
}

GAP_Q = {
    ("research_question", "objective"): "Tujuan apa yang menjawab rumusan masalah Anda?",
    ("objective", "variable"): (
        "Variabel apa yang Anda teliti untuk mencapai tujuan ini, dan bagaimana definisi "
        "operasionalnya?"
    ),
    ("objective", "method"): "Desain penelitian apa yang dipakai untuk mencapai tujuan ini?",
    ("population", "method"): "Bagaimana sampel diambil dari populasi yang Anda tetapkan?",
    ("variable", "instrument"): "Instrumen apa yang mengukur variabel Anda, dan bagaimana diuji?",
    ("method", "analysis"): "Teknik analisis apa yang sesuai dengan desain Anda, dan mengapa?",
    ("objective", "analysis"): "Bagaimana data diolah sampai tujuan penelitian terjawab?",
    ("analysis", "claim"): "Kesimpulan apa yang Anda harapkan dari analisis ini, dan apa batasnya?",
}

BASELINE_Q = {
    "method": "Mengapa memilih desain “{content}” dibanding alternatifnya?",
    "analysis": "Asumsi apa yang harus dipenuhi oleh “{content}”, dan bagaimana Anda mengujinya?",
    "research_question": "Mengapa masalah “{content}” penting dan layak diteliti sekarang?",
    "instrument": "Bagaimana “{content}” disusun, dan sudah diuji coba pada siapa?",
}


def _fill(template: str, els: list[Element], extra: dict[str, str] | None = None) -> str:
    values = {t: _short(e.content) for t in FINDING_TYPES if (e := _first(els, t))}
    values.update(extra or {})
    for t in FINDING_TYPES:
        values.setdefault(t, "bagian ini")
    return template.format(**values)


def stress_questions(graph: Graph, findings: list[FindingRef]) -> list[Question]:
    els = graph.nodes
    by_id = {e.id: e for e in els}
    out: list[Question] = []

    for f in findings:
        if f.status in CLOSED or f.rule_id not in FINDING_Q:
            continue
        involved = [by_id[i] for i in f.element_ids if i in by_id] or els
        out.append(
            Question(
                key=f"finding:{f.rule_id}",
                kind="finding",
                text=_fill(FINDING_Q[f.rule_id], involved),
                reason=(
                    f"Temuan {f.rule_id} masih terbuka "
                    f"(prioritas {PRIORITY_LABEL.get(f.priority, f.priority)})."
                ),
                element_ids=tuple(f.element_ids),
                score=3 + PRIORITY.get(f.priority, 0),
            )
        )
    for g in graph.gaps:
        template = GAP_Q.get((g.from_type, g.to_type))
        if template:
            src = [e.id for e in els if e.type == g.from_type]
            out.append(
                Question(
                    key=f"gap:{g.from_type}:{g.to_type}",
                    kind="gap",
                    text=template,
                    reason=(
                        f"Rantai terputus: ada {TYPE_LABEL.get(g.from_type, g.from_type).lower()} "
                        f"tanpa {TYPE_LABEL.get(g.to_type, g.to_type).lower()}."
                    ),
                    element_ids=tuple(src),
                    score=2,
                )
            )
    for e in els:
        if not e.verified:
            out.append(
                Question(
                    key=f"unverified:{e.id}",
                    kind="unverified",
                    text=(
                        f"Di bagian mana proposal Anda menyatakan “{_short(e.content)}”, "
                        "dan apakah konsisten dengan bagian lain?"
                    ),
                    reason="Kutipan elemen ini tidak ditemukan di dokumen.",
                    element_ids=(e.id,),
                    score=1,
                )
            )

    seen: set[str] = set()
    ranked: list[Question] = []
    for q in sorted(out, key=lambda q: -q.score):  # sorted stabil: urutan asli untuk skor sama
        if q.key not in seen:
            seen.add(q.key)
            ranked.append(q)
    if len(ranked) < MIN_Q:  # lengkapi dengan pertanyaan dasar dari elemen yang ada
        for e in els:
            if len(ranked) >= MIN_Q:
                break
            template = BASELINE_Q.get(e.type)
            key = f"baseline:{e.type}"
            if template and key not in seen:
                seen.add(key)
                ranked.append(
                    Question(
                        key=key,
                        kind="baseline",
                        text=template.format(content=_short(e.content)),
                        reason="Pertanyaan umum penguji untuk bagian ini.",
                        element_ids=(e.id,),
                        score=0,
                    )
                )
    return ranked[:MAX_Q]
