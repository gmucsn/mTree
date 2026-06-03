import os
from pathlib import Path

import pytest

from mTree.simulation.library import Library

YAML_CONFIGURATIONS = Path(__file__).resolve().parent / "yaml_configurations"
JSON_CONFIGURATIONS = Path(__file__).resolve().parent / "json_configurations"

EXAMPLE_MES_DIRECTORY = Path(__file__).resolve().parent / "example_mes_directory" 
EMPTY_EXAMPLE_MES_DIRECTORY = Path(__file__).resolve().parent / "empty_example_mes_directory" 


INVALID_CONFIGURATIONS = Path(__file__).resolve().parent / "invalid_configurations"


@pytest.fixture(autouse=True)
def change_test_dir(request):
    old_cwd = os.getcwd()    
    new_cwd = EXAMPLE_MES_DIRECTORY
    os.chdir(new_cwd)
    yield
    os.chdir(old_cwd)

def test_target_directory_with_mes():
    library = Library(target_directory=EXAMPLE_MES_DIRECTORY)
    assert len(library.mes_list) > 0

def test_target_directory_without_mes():
    library = Library(target_directory=EMPTY_EXAMPLE_MES_DIRECTORY)
    assert len(library.mes_list) == 0

def test_library_cwd(change_test_dir):
    library = Library()
    assert len(library.mes_list) > 0
    assert len(library.mes_library.values()) > 0
    print(library.mes_library)
    assert len(library.configuration_dict(library.mes_list[0]).values()) > 0