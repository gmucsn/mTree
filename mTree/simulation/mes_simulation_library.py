import glob
import sys

from mTree.simulation.mes_simulation_description import MESSimulationDescription

class MESSimulationLibrary():
    def __init__(self):
        self.simulations = []

    def list_simulation_files(self):
        for filename in glob.iglob('./config/*.json', recursive=True):
            description = None
            try:
                description = MESSimulationDescription(filename=filename)
            except Exception as e:
                print("EXCEPTED OUT...")
                print(e)

                pass
            if description is not None:
                self.simulations.append({"name":description.name,
                                         "json":description.to_json(),
                                         "description": description})

    def get_simulations(self):
        return self.simulations