import hashlib
import random
from datetime import datetime

from mTree.simulation.configuration import Configuration
from pydantic import BaseModel, computed_field


class Iteration(BaseModel):
    simulation_run_id: str
    configuration: Configuration
    iteration_number: int
    status: str = "Registered"
    mes_base_address: object = None
    start_time: datetime = None
    end_time: datetime = None
    dispatcher: object = None

    @computed_field
    @property
    def iteration_id(self) -> str:
        return self.simulation_run_id + "-" + str(self.iteration_number)

    @computed_field
    @property
    def run_code(self) -> float:  # TODO Change to iteration code
        hash_basis = (
            str(self.configuration.name)
            + "-"
            + str(self.configuration.id)
            + "-"
            + str(self.iteration_number)
            + str(random.uniform(0, 100))
        )
        hash_object = hashlib.sha1(hash_basis.encode("utf-8"))
        return hash_object.hexdigest()[0:6]

    def set_mes_base_address(self, base_address):
        self.mes_base_address = base_address

    def mark_running(self):
        self.status = "Running"
        self.start_time = datetime.now()

    def mark_finished(self):
        self.status = "Finished"
        self.end_time = datetime.now()

    def mark_killed(self):
        self.status = "Killed"
        self.end_time = datetime.now()

    def mark_excepted(self):
        self.status = "Exception!"
        self.end_time = datetime.now()

    def to_data_row(self):
        total_time = "Not running"
        if self.start_time is not None:
            if self.end_time is not None:
                total_time = self.end_time - self.start_time
            else:
                total_time = datetime.now() - self.start_time
        return [self.run_code, self.name, self.run_number, self.status, str(total_time)]

    # def __str__(self):
    #     output_string = f"<SimulationRunStatus run_code: {self.run_code} id: {self.id} run_number: {self.run_number} status: {self.status} start_time: {self.start_time} end_time: {self.start_time}  >"
    #     return output_string

    # def __repr__(self):
    #     return self.__str__()
