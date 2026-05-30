from pathlib import Path
from typing import List

from mTree.simulation.configuration import Configuration
from pydantic import BaseModel


class MESDescription(BaseModel):
    mes_directory: Path
    configurations: List[Configuration]
