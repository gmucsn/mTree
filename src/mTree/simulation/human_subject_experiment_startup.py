from pydantic import BaseModel, Field

from mTree.simulation.configuration import Configuration


class HumanSubjectExperimentStartup(BaseModel):
    configuration: Configuration
    subject_ids: list[str] = Field(min_length=1)
    source_hash: str = ""
