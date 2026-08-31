from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent / "example_data"

CONFIGURATIONS_PATH = DATA_PATH / "configurations"

YAML_CONFIGURATIONS_PATH = CONFIGURATIONS_PATH / "yaml"
JSON_CONFIGURATIONS_PATH = CONFIGURATIONS_PATH / "json"
INVALID_CONFIGURATIONS_PATH = CONFIGURATIONS_PATH / "invalid"


def pytest_generate_tests(metafunc):
    """A fixture to generate lists of files or other things to simplify testing."""
    if "yaml_configuration" in metafunc.fixturenames:
        yaml_files = [f for f in YAML_CONFIGURATIONS_PATH.iterdir() if f.is_file()]
        metafunc.parametrize(
            "yaml_configuration", yaml_files, ids=[f.name for f in yaml_files]
        )
    elif "json_configuration" in metafunc.fixturenames:
        json_files = [f for f in JSON_CONFIGURATIONS_PATH.iterdir() if f.is_file()]
        metafunc.parametrize(
            "json_configuration", json_files, ids=[f.name for f in json_files]
        )
    elif "invalid_configuration" in metafunc.fixturenames:
        invalid_files = [
            f for f in INVALID_CONFIGURATIONS_PATH.iterdir() if f.is_file()
        ]
        metafunc.parametrize(
            "invalid_configuration", invalid_files, ids=[f.name for f in invalid_files]
        )
