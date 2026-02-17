from pathlib import Path
from typing import Any, Dict, List

from pydantic import BaseModel, Field, ValidationError, field_validator
from pydantic.types import constr


class AgentConfiguration(BaseModel):
    agent_name: str
    number: int
    class_name: str = ""
    properties: Dict[str, Any] = {}


class InstitutionConfiguration(BaseModel):
    institution_name: str
    class_name: str = ""
    properties: Dict[str, Any] = {}


class EnvironmentConfiguration(BaseModel):
    name: str
    mes_class: str = ""
    properties: Dict[str, Any] = {}


class Configuration(BaseModel):
    mtree_type: str
    name: str
    id: str
    environment: EnvironmentConfiguration
    institutions: List[InstitutionConfiguration]
    agents: List[AgentConfiguration]
    properties: Dict[str, Any]
    file_source: Path = None
    data_logging: str = "json"
    debug: bool = True
    number_of_iterations: int = 1
    log_level: int = 2
    source_hash: str = ""
    simulation_run_id: str = ""
    mes_directory: Path = None
