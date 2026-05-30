
from mTree.simulation.description import SimulationDescription
from mTree.simulation.simulation_run import SimulationRun
from pydantic import BaseModel


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
