"""Memuat aturan dari rules/*.yaml (IO di sini; engine murni di domain/rules.py)."""

from pathlib import Path

import yaml

from app.domain.rules import Rule

RULES_DIR = Path(__file__).resolve().parents[2] / "rules"


class RuleFileError(ValueError):
    pass


def load_rules(directory: Path = RULES_DIR) -> list[Rule]:
    rules: list[Rule] = []
    seen: set[str] = set()
    for path in sorted(directory.glob("*.yaml")):
        try:
            rule = Rule.model_validate(yaml.safe_load(path.read_text(encoding="utf-8")))
        except Exception as exc:  # pesan jelas: file mana yang rusak
            raise RuleFileError(f"{path.name}: {exc}") from exc
        if rule.id in seen:
            raise RuleFileError(f"{path.name}: id ganda {rule.id}")
        seen.add(rule.id)
        rules.append(rule)
    return rules
