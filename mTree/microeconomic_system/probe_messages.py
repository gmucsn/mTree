from dataclasses import dataclass


@dataclass
class ProbeMessage:
    state_request: dict = None
    state_response: dict = None