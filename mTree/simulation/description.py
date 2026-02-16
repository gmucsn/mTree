from pathlib import Path
from typing import Any, Dict, List

from pydantic import BaseModel, Field, ValidationError, field_validator
from pydantic.types import constr


class AgentDescription(BaseModel):
    agent_name: str
    number: int


class SimulationDescription(BaseModel):
    mtree_type: str
    name: str
    id: str
    environment: str
    institution: str
    agents: List[AgentDescription]
    properties: Dict[str, Any]
    file_source: Path = None
    data_logging: str = "json"
    debug: bool = True
    number_of_runs: int = 1
    log_level: int = 2
    source_hash: str = ""
    simulation_run_id: str = ""
    mes_directory: Path = None


class MESDescription(BaseModel):
    mes_directory: Path
    configurations: List[SimulationDescription]
