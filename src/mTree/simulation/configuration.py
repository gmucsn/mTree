import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from pydantic import BaseModel


class AgentConfiguration(BaseModel):
    agent_name: str
    number: int
    class_name: str = ""
    properties: Optional[Dict[str, Any]] = {}


class InstitutionConfiguration(BaseModel):
    institution_name: str
    class_name: str = ""
    properties: Optional[Dict[str, Any]] = {}


class EnvironmentConfiguration(BaseModel):
    name: str
    mes_class: str = ""
    properties: Optional[Dict[str, Any]] = {}


class Configuration(BaseModel):
    mtree_type: str
    name: str
    id: str
    environment: EnvironmentConfiguration
    institutions: List[InstitutionConfiguration]
    agents: List[AgentConfiguration]
    properties: Optional[Dict[str, Any]] = {}
    file_source: Path = None
    data_logging: str = "json"
    debug: Optional[bool] = True
    number_of_iterations: int = 1
    log_level: int = 2
    source_hash: str = ""
    simulation_run_id: str = ""
    mes_directory: Path = None

    @classmethod
    def load_from_file(cls, config_file_path: Path):
        experiment_configuration = None
        if config_file_path.suffix == ".json":
            with open(config_file_path, "r") as f:
                json_content = f.read()
                experiment_configuration = cls.model_validate_json(
                    json_content
                )
        elif config_file_path.suffix == ".yaml":
            with open(config_file_path, "r") as f:
                yaml_content = yaml.safe_load(f)
                experiment_configuration = cls.model_validate(yaml_content)
        else:
            raise Exception("Invalid Configuration file type")
        
        return experiment_configuration
