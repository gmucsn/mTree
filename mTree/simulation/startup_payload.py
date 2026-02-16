import hashlib
import random
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from mTree.simulation.description import SimulationDescription
from mTree.simulation.simulation_run import SimulationRun
from pydantic import BaseModel, Field, ValidationError, computed_field, field_validator
from pydantic.types import constr


class StartupPayload(BaseModel):
    configuration: SimulationDescription
    properties: dict
    dispatcher: object
    simulation_id: str
    simulation_run_id: str
    short_name: str
    run_code: str
    debug: bool
    log_level: int
    status: str
    data_logging: bool = False
    run_number: int = None
    simulation_run: SimulationRun = None
