from pathlib import Path
from typing import Any, Dict, List

from mTree.simulation.configuration import Configuration
from pydantic import BaseModel, Field, ValidationError, field_validator
from pydantic.types import constr


class MESDescription(BaseModel):
    mes_directory: Path
    configurations: List[Configuration]
