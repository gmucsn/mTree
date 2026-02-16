import atexit
import os
import time

import questionary
import typer
from mTree.generator import Generate
from mTree.simulation import Library
from mTree.system.actor_system_connector import ActorSystemConnector
from mTree.system.actor_system_controller import ActorSystemController
from mTree.system.mes_simulation_library import MESSimulationLibrary
from mTree.utilities.console.simulation_viewer import SimulationViewer
from thespian.actors import *

"""
Basic mTree CLI

This file invokes other methods to provide particular services.
"""

app = typer.Typer()


def run_simulation_from_configurations(config_dir, configurations):
    for configuration in configurations:
        working_dir = config_dir
        # actor_system.send_message()
        configuration_good = True
        # try:
        simulation_library = MESSimulationLibrary()
        simulation_library.list_simulation_files_directory(working_dir)
        list_simulations = simulation_library.simulations
        # configuration_name = os.path.basename(configuration)

        # simulation = simulation_library.get_simulation_by_filename(
        #     configuration.file_source
        # )
        # t = simulation_library.get_simulations()
        # t = os.path.join(config_dir, configuration_name)
        # except Exception as e:
        #     configuration_good = False

        if configuration_good:
            actor_system = ActorSystemConnector()
            working_dir = config_dir
            # actor_system.send_message()
            actor_system.run_simulation_configuration(configuration)
            # actor_system.run_simulation_configuration(
            #     working_dir,
            #     str(configuration.file_source),
            #     configuration.dict(exclude={"file_source"}),
            # )
            simulation_viewer = SimulationViewer()
            simulation_viewer.run()


# simulation["description"].to_hash()
# self.examine_directory()
# if self.multi_simulation is False:
#     self.launch_multi_simulations()
# else:
#     self.launch_multi_simulations()


@app.command()
def generate():
    Generate()


@app.command()
def simulation():
    library = Library()
    mes = questionary.select(
        "Which MES would you like to run?",
        choices=library.mes_list,
    ).ask()
    configurations = library.configuration_dict(mes)
    config_selections = questionary.checkbox(
        "Which configurations would you like to run?",
        choices=configurations,
    ).ask()
    print("Starting to run...")
    final_configs = [
        configurations[config_selection] for config_selection in config_selections
    ]

    @atexit.register
    def shutdown_actor_system():
        ActorSystemController.shutdown()
        print("Goodbye!")

    actor_system = ActorSystemController.startup()
    run_simulation_from_configurations(mes, final_configs)

    # @atexit.register
    # def shutdown_actor_system():
    #     ActorSystemController.shutdown()
    #     print("Goodbye!")


if __name__ == "__main__":
    app()
