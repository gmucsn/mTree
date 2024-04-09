from dataclasses import dataclass, field
from typing import Dict

@dataclass
class ActorProcessDescriptor:
    environment_basis: str = None
    actor_address: str = None
    actor_name: str = None
    status: str = None
    pid: str = None
    cpu_usage: str = None
    memory_usage: str = None
    started: str = None
    child_process: str = None

    def human_readable_memory(self):
        suffix="B"
        num = self.memory_usage
        for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
            if abs(num) < 1024.0:
                return f"{num:3.1f}{unit}{suffix}"
            num /= 1024.0
        return f"{num:.1f}Yi{suffix}"
