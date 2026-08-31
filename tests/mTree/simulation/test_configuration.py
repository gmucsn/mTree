"""Tests used to evalue the Configuration objects used to setup an mTree experiment.

This will check, amongst other things, the basic ingestion of configuration files.

"""

import pytest
from pydantic import ValidationError
from yaml.scanner import ScannerError

from mTree.simulation.configuration import Configuration


def test_yaml_configurations(yaml_configuration):
    """A test for checking yaml configuration ingestion.

    Args:
        yaml_configuration: Fixture list of yaml configuration examples.

    """
    configuration = Configuration.load_from_file(yaml_configuration)
    assert configuration.id is not None


def test_json_configurations(json_configuration):
    """A test for checking json configuration ingestion.

    Args:
        json_configuration: Fixture list of json configuration example

    """
    configuration = Configuration.load_from_file(json_configuration)
    assert configuration.id is not None


def test_invalid_configurations(invalid_configuration):
    """A test for checking the handling of invalid configuration files.

    Args:
        invalid_configuration: Fixture list of invalid configuraiton files of different formats.

    """
    with pytest.raises((ValidationError, ScannerError)):
        Configuration.load_from_file(invalid_configuration)
