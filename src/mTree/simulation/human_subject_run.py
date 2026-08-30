
from mTree.simulation.configuration import Configuration
from pydantic import BaseModel


class HumanSubjectRun(BaseModel):
    simulation_run_id: str
    configuration: Configuration
    subject_ids: list[str]
