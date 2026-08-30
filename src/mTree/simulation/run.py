
from mTree.simulation.configuration import Configuration
from pydantic import BaseModel


class Run(BaseModel):
    simulation_run_id: str
    configuration: Configuration
