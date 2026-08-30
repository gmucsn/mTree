from typing import Any

from pydantic import BaseModel


class HumanSubjectExperimentMessage(BaseModel):
    action: str
    source: str
    destination: str
    payload: Any