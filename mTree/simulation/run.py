from pathlib import Path
from typing import Any, Dict, List

from mTree.simulation.configuration import Configuration
from pydantic import BaseModel, Field, ValidationError, field_validator
from pydantic.types import constr


class Run(BaseModel):
    simulation_run_id: str
    configuration: Configuration
