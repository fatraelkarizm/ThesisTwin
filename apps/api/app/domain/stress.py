"""Defense Stress-Test (abstrak §4 langkah 4; Langkah 22).

Tautan terlemah graph -> 3–5 pertanyaan penguji. Deterministik: pemilihan dengan skor yang bisa
dijelaskan, pertanyaan dari templat. Pertanyaan tidak pernah berisi jawabannya.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field

from app.domain.graph import Graph
from app.domain.ontology import Ontology
from app.domain.rules import Element

MIN_Q, MAX_Q = 3, 5
PRIORITY = {"high": 2, "medium": 1, "low": 0}
PRIORITY_LABEL = {"high": "tinggi", "medium": "sedang", "low": "rendah"}
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


def _fill(template: str, els: list[Element], types: list[str]) -> str:
    """Isi {<tipe elemen>} dengan elemen pertama bertipe itu; yang tidak ada -> "bagian ini"."""
    values = {t: _short(e.content) for t in types if (e := _first(els, t))}
    for t in types:
        values.setdefault(t, "bagian ini")
    return template.format(**values)


def stress_questions(
    graph: Graph,
    findings: list[FindingRef],
    ontology: Ontology,
    rule_questions: Mapping[str, str],
) -> list[Question]:
    """`rule_questions`: id aturan -> templat pertanyaan sidang (field `defense_question` di
    rules/*.yaml). Templat celah & dasar datang dari ontologi."""
    els = graph.nodes
    by_id = {e.id: e for e in els}
    out: list[Question] = []

    for f in findings:
        if f.status in CLOSED or f.rule_id not in rule_questions:
            continue
        involved = [by_id[i] for i in f.element_ids if i in by_id] or els
        out.append(
            Question(
                key=f"finding:{f.rule_id}",
                kind="finding",
                text=_fill(rule_questions[f.rule_id], involved, ontology.type_ids),
                reason=(
                    f"Temuan {f.rule_id} masih terbuka "
                    f"(prioritas {PRIORITY_LABEL.get(f.priority, f.priority)})."
                ),
                element_ids=tuple(f.element_ids),
                score=3 + PRIORITY.get(f.priority, 0),
            )
        )
    for g in graph.gaps:
        template = ontology.gap_question(g.from_type, g.to_type)
        if template:
            src = [e.id for e in els if e.type == g.from_type]
            out.append(
                Question(
                    key=f"gap:{g.from_type}:{g.to_type}",
                    kind="gap",
                    text=template,
                    reason=(
                        f"Rantai terputus: ada {ontology.label(g.from_type).lower()} "
                        f"tanpa {ontology.label(g.to_type).lower()}."
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
            template = ontology.baseline_question(e.type)
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
