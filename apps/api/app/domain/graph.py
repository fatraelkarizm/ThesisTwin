"""Research dependency graph (proposal §5.2) diturunkan dari elemen, deterministik.

Graph tidak disimpan: dihitung ulang dari elemen versi, sehingga tidak pernah basi.
Edge mengikuti ontologi di docs/data-model.md; celah = tipe yang diharapkan tidak ada sama sekali.
"""

from dataclasses import dataclass, field

from app.domain.rules import Element

# (dari, ke, jenis edge). Urutan = rantai dependency utama proposal.
RELATIONS: list[tuple[str, str, str]] = [
    ("research_question", "objective", "addresses"),
    ("objective", "variable", "requires"),
    ("objective", "method", "requires"),
    ("population", "method", "requires"),
    ("variable", "instrument", "measured_by"),
    ("method", "analysis", "analyzed_with"),
    ("objective", "analysis", "analyzed_with"),
    ("analysis", "claim", "supports"),
]

LAYER = {
    "research_question": 0,
    "objective": 1,
    "variable": 2,
    "population": 2,
    "method": 3,
    "instrument": 3,
    "analysis": 4,
    "claim": 5,
    "limitation": 5,
}


@dataclass(frozen=True)
class Edge:
    src: str
    dst: str
    type: str


@dataclass(frozen=True)
class Gap:
    from_type: str
    to_type: str
    relation: str


@dataclass
class Graph:
    nodes: list[Element] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)
    gaps: list[Gap] = field(default_factory=list)


def build_graph(elements: list[Element]) -> Graph:
    by_type: dict[str, list[Element]] = {}
    for e in elements:
        by_type.setdefault(e.type, []).append(e)
    g = Graph(nodes=sorted(elements, key=lambda e: (LAYER.get(e.type, 9), e.page)))
    for src_t, dst_t, rel in RELATIONS:
        sources, targets = by_type.get(src_t, []), by_type.get(dst_t, [])
        if sources and not targets:
            g.gaps.append(Gap(src_t, dst_t, rel))
        g.edges += [Edge(s.id, t.id, rel) for s in sources for t in targets]
    return g
