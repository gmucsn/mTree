
from mTree.simulation.iteration import Iteration
from pydantic import BaseModel


class ComponentInitialization(BaseModel):
    component_type: str
    iteration: Iteration
    log_actor: object
    mes_container: object
    initialization: object  # todo eventually this will come from the original configuration on an MES component
    environment: object = None
    properties: dict = (
        {}
    )  # todo eventually this will come from the original configuration on an MES component
