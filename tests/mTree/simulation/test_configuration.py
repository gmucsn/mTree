from pathlib import Path

import pytest
from pydantic import ValidationError
from yaml.scanner import ScannerError

from mTree.simulation.configuration import Configuration
from mTree.simulation.library import Library

EXAMPLES_PATH = Path(__file__).resolve().parent / "example_configurations"

YAML_CONFIGURATIONS_PATH = EXAMPLES_PATH / "yaml_configurations"
JSON_CONFIGURATIONS_PATH = EXAMPLES_PATH / "json_configurations"
INVALID_CONFIGURATIONS_PATH = EXAMPLES_PATH / "invalid_configurations"

# TODO ensure that the class names match the specified names


@pytest.mark.parametrize("configuration_file", ["1.yaml", "2.yaml", "3.yaml"])
def test_yaml_configurations(configuration_file):
    configuration = Configuration.load_from_file(YAML_CONFIGURATIONS_PATH / configuration_file)
    assert configuration.id is not None

@pytest.mark.parametrize("configuration_file", ["1.json", "2.json", "3.json"])
def test_json_configurations(configuration_file):
    configuration = Configuration.load_from_file(JSON_CONFIGURATIONS_PATH / configuration_file)
    assert configuration.id is not None

@pytest.mark.parametrize("configuration_file", ["bad_json.json", "bad_yaml.yaml"])
def test_invalid_configurations(configuration_file):
    with pytest.raises((ValidationError, ScannerError)):
        configuration = Configuration.load_from_file(INVALID_CONFIGURATIONS_PATH / configuration_file)
    