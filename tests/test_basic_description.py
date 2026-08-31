import json

import pytest
from pydantic import ValidationError

from mTree.simulation.description import SimulationDescription


@pytest.fixture(scope="function")
def basic_description():
    return {
        "mtree_type": "mes_simulation_description",
        "name": "Basic Simulation Run",
        "id": "1",
        "environment": "ENVIRONMENTNAME",
        "institution": "INSTITUTIONNAME",
        "number_of_runs": 1,
        "agents": [{"agent_name": "AGENTNAME", "number": 5}],
        "properties": {"agent_endowment": 10},
    }


def test_basic_description(basic_description):
    sd = SimulationDescription.model_validate_json(json.dumps(basic_description))
    assert sd


def test_bad_basic_description(basic_description):
    temp_description = basic_description
    del temp_description["environment"]
    with pytest.raises(ValidationError):
        sd = SimulationDescription.model_validate_json(json.dumps(temp_description))
