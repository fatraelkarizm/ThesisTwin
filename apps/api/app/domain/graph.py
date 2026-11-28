"""Research dependency graph (proposal §5.2) diturunkan dari elemen, deterministik.

Graph tidak disimpan: dihitung ulang dari elemen versi, sehingga tidak pernah basi.
Edge mengikuti relasi di config/ontology.yaml; celah = tipe yang diharapkan tidak ada sama sekali.
"""

from dataclasses import dataclass, field

from app.domain.ontology import Ontology
from app.domain.rules import Element


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


def build_graph(elements: list[Element], ontology: Ontology) -> Graph:
    by_type: dict[str, list[Element]] = {}
    for e in elements:
        by_type.setdefault(e.type, []).append(e)
    g = Graph(nodes=sorted(elements, key=lambda e: (ontology.layer(e.type), e.page)))
    for r in ontology.relations:
        sources, targets = by_type.get(r.source, []), by_type.get(r.target, [])
        if sources and not targets:
            g.gaps.append(Gap(r.source, r.target, r.type))
        g.edges += [Edge(s.id, t.id, r.type) for s in sources for t in targets]
    return g
