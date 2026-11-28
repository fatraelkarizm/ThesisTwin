from pydantic import BaseModel


class ElementTypeOut(BaseModel):
    id: str
    label: str
    short: str
    code: str
    layer: int


class RelationOut(BaseModel):
    source: str
    target: str
    type: str


class OntologyOut(BaseModel):
    """Bagian ontologi yang dibutuhkan UI. Pertanyaan & tabel dampak tetap di server."""

    element_types: list[ElementTypeOut]
    relations: list[RelationOut]
    map: list[str]
