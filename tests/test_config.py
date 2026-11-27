from pathlib import Path

import pytest

from insureai.config import ConfigurationError, load_config


CONFIG = Path(__file__).parents[1] / "configs" / "sources" / "insurance_entities.yml"


def test_load_insurance_entity_config():
    config = load_config(CONFIG)
    assert config["domain"] == "property_and_casualty"
    assert {"customers", "policies", "claims"} <= set(config["entities"])


def test_rejects_missing_config_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_config(tmp_path / "missing.yml")


def test_rejects_invalid_entity_config(tmp_path):
    path = tmp_path / "bad.yml"
    path.write_text("entities:\n  claims:\n    source_format: csv\n", encoding="utf-8")
    with pytest.raises(ConfigurationError):
        load_config(path)
