"""Load and validate metadata-driven ingestion configuration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class ConfigurationError(ValueError):
    """Raised when an ingestion configuration is invalid."""


def load_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML configuration file and validate its entity declarations."""
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)

    if not isinstance(config, dict):
        raise ConfigurationError("Configuration root must be a YAML mapping.")

    entities = config.get("entities")
    if not isinstance(entities, dict) or not entities:
        raise ConfigurationError("'entities' must be a non-empty mapping.")

    for name, entity in entities.items():
        if not isinstance(entity, dict):
            raise ConfigurationError(f"Entity '{name}' must be a mapping.")
        required = {"source_format", "source_path", "bronze_table", "primary_key", "expected_columns"}
        missing = required - entity.keys()
        if missing:
            raise ConfigurationError(f"Entity '{name}' is missing: {', '.join(sorted(missing))}.")
        if entity["source_format"] not in {"csv", "json", "parquet"}:
            raise ConfigurationError(f"Entity '{name}' has unsupported source_format.")
        if not isinstance(entity["expected_columns"], list) or not entity["expected_columns"]:
            raise ConfigurationError(f"Entity '{name}' expected_columns must be a non-empty list.")
        if entity["primary_key"] not in entity["expected_columns"]:
            raise ConfigurationError(f"Entity '{name}' primary_key must be in expected_columns.")

    return config
