from fastapi import APIRouter

from app.schemas.ontology import ElementTypeOut, OntologyOut, RelationOut
from app.services import config

router = APIRouter()


@router.get("/ontology")
def get_ontology() -> OntologyOut:
    """Tipe elemen, label, dan relasi dari config/ontology.yaml, agar UI tidak menyalinnya."""
    ont = config.ontology()
    types = [
        ElementTypeOut(
            id=t.id, label=t.label, short=t.short or t.label, code=t.code, layer=t.layer
        )
        for t in ont.element_types
    ]
    relations = [RelationOut(source=r.source, target=r.target, type=r.type) for r in ont.relations]
    return OntologyOut(element_types=types, relations=relations, map=ont.map)
