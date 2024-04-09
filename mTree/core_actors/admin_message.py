from dataclasses import dataclass, field
from typing import Dict

@dataclass
class AdminMessage:
    directive: str = None
    payload: object = None
    short_name_base: str = None
    source_class: str = None
    source_hash: str = None
    local_properties: dict = field(default_factory=dict)
    global_properties: dict = field(default_factory=dict)
    number: int = 1
