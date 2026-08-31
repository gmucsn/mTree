from pathlib import Path  # noqa: D100
from typing import Any

import yaml
from pydantic import BaseModel, field_serializer


class AgentConfiguration(BaseModel):  # noqa: D101
    agent_name: str
    number: int
    class_name: str = ""
    properties: dict[str, Any] | None = {}


class InstitutionConfiguration(BaseModel):
    institution_name: str
    class_name: str = ""
    properties: dict[str, Any] | None = {}


class EnvironmentConfiguration(BaseModel):
    name: str
    mes_class: str = ""
    properties: dict[str, Any] | None = {}


class Configuration(BaseModel):
    mtree_type: str
    name: str
    id: str
    environment: EnvironmentConfiguration
    institutions: list[InstitutionConfiguration]
    agents: list[AgentConfiguration]
    properties: dict[str, Any] | None = {}
    file_source: Path = None
    data_logging: str = "json"
    debug: bool | None = True
    number_of_iterations: int = 1
    log_level: int = 2
    source_hash: str = ""
    simulation_run_id: str = ""
    mes_directory: Path = None

    @field_serializer("mes_directory")
    def serialize_path(self, file_path: Path) -> str:
        return str(
            file_path.as_posix()
        )  # Or file_path.as_posix() for uniform forward slashes

    @field_serializer("file_source")
    def serialize_file_source_path(self, file_path: Path) -> str:
        return str(
            file_path.as_posix()
        )  # Or file_path.as_posix() for uniform forward slashes

    @classmethod
    def load_from_file(cls, config_file_path: Path):
        """_summary_.

        Args:
            config_file_path (Path): _description_

        Raises:
            Exception: _description_

        Returns:
            _type_: _description_

        """
        experiment_configuration = None
        if config_file_path.suffix == ".json":
            with open(config_file_path) as f:
                json_content = f.read()
                experiment_configuration = cls.model_validate_json(json_content)
                experiment_configuration.file_source = config_file_path
                experiment_configuration.mes_directory = config_file_path.parent.parent
        elif config_file_path.suffix == ".yaml":
            with open(config_file_path) as f:
                yaml_content = yaml.safe_load(f)
                experiment_configuration = cls.model_validate(yaml_content)
                experiment_configuration.file_source = config_file_path
                experiment_configuration.mes_directory = config_file_path.parent.parent
        else:
            raise Exception("Invalid Configuration file type")

        return experiment_configuration
