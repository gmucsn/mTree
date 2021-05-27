import glob
import sys
import os

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

    def list_simulation_files_directory(self, mes_directory):
        for filename in glob.iglob(mes_directory + '/config/*.json', recursive=True):
            description = None
            try:
                description = MESSimulationDescription(filename=filename)
            except Exception as e:
                pass
            if description is not None:
                self.simulations.append({
                                        "source": os.path.basename(filename),
                                        "source_file": filename,
                                        "name":description.name,
                                         "json":description.to_json(),
                                         "description": description})

    def get_simulations(self):
        return self.simulations

    def get_simulation_by_filename(self, filename):
        for simulation in self.simulations:
            if simulation["source"] == filename:
                return simulation
        return None