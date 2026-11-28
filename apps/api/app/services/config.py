"""Memuat config/*.yaml (IO di sini; skema murni di domain/ontology.py)."""

from functools import cache
from pathlib import Path
from typing import TypeVar

import yaml
from pydantic import BaseModel

from app.domain.ontology import Extraction, Ontology

M = TypeVar("M", bound=BaseModel)

CONFIG_DIR = Path(__file__).resolve().parents[2] / "config"


class ConfigFileError(ValueError):
    pass


def _load(path: Path, model: type[M]) -> M:
    try:
        return model.model_validate(yaml.safe_load(path.read_text(encoding="utf-8")))
    except Exception as exc:  # pesan jelas: file mana yang rusak
        raise ConfigFileError(f"{path.name}: {exc}") from exc


def load_ontology(directory: Path = CONFIG_DIR) -> Ontology:
    return _load(directory / "ontology.yaml", Ontology)


def load_extraction(directory: Path = CONFIG_DIR) -> Extraction:
    extraction = _load(directory / "extraction.yaml", Extraction)
    try:
        extraction.check_types(load_ontology(directory))
    except ValueError as exc:
        raise ConfigFileError(f"extraction.yaml: {exc}") from exc
    return extraction


@cache
def ontology() -> Ontology:
    """Dimuat sekali per proses."""
    return load_ontology()


@cache
def extraction() -> Extraction:
    return load_extraction()
