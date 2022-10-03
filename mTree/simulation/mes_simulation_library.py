import glob
import sys
import os
import json
from mTree.microeconomic_system.mes_exceptions import *

# from mTree.development.development_endpoints import simulation_library

from mTree.simulation.mes_simulation_description import MESSimulationDescription

class MESSimulationLibrary():
    def __init__(self):
        self.simulations = []

    def list_simulation_files(self):
        for filename in glob.iglob('./config/*.json', recursive=True):
            description = None
            # try:
            description = MESSimulationDescription(filename=filename)
            # except Exception as e:
            #     print("EXCEPTED OUT...")
            #     print(e)
            #     pass

            if description is not None:
                self.simulations.append({"name":description.name,
                                         "json":description.to_json(),
                                         "description": description})

    def list_human_subject_files_directory(self, mes_directory):
        for filename in glob.iglob(mes_directory + '/config/*.json', recursive=True):
            description = None
            # try:
            description = MESSimulationDescription(filename=filename)
            # except Exception as e:
            #     pass
            if description is not None:
                if description.mtree_type == "mes_subject_experiment":
                    simulation_information = {
                                            "source": os.path.basename(filename),
                                            "source_file": filename,
                                            "name":description.name,
                                            "json": description.to_json(),
                                            "description": description}
                    self.simulations.append(simulation_information)

    def list_simulation_files_directory(self, mes_directory):
        for filename in glob.iglob(mes_directory + '/config/*.json', recursive=True):
            description = None
            try:
                description = MESSimulationDescription(filename=filename)
            except Exception as e:
                print(f"ERROR: Configuration file {filename} has a problem!")
                print("\t", e)
                raise BadSimulationConfigurationFile(e)
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