import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict


@dataclass
class AdminMessage:
    timestamp = time.time()
    directive: str = None
    payload: object = None
    short_name_base: str = None
    source_class: str = None
    source_hash: str = None
    local_properties: dict = field(default_factory=dict)
    global_properties: dict = field(default_factory=dict)
    number: int = 1

    def __str__(self):
        return "<AdminMessage Request: {}, Response: {}, Payload: {}>".format(
            self.directive, self.response, self.payload
        )

    def __repr__(self):
        return "<AdminMessage Request: {}, Response: {}, Payload: {}>".format(
            self.directive, "", ""
        )
