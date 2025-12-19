import typer
import atexit
import os
from datetime import timedelta

from mTree.system.actor_system_controller import ActorSystemController
from mTree.utilities.console.mtree_console_app import MTreeConsoleApp
from thespian.actors import *
import questionary

app = typer.Typer()

@atexit.register
def shutdown_actor_system():
    ActorSystemController.shutdown()
    print("Goodbye!")


def main():
    print("mTree Console")
    actor_system = ActorSystemController.startup()

    mtree_console_app = MTreeConsoleApp()
    mtree_console_app.run()

    # capabilities = dict([("Admin Port", 19000)])
    # asys = ActorSystem(systemBase ="multiprocTCPBase", capabilities=capabilities)
    # try:
    # hello = actor_system.createActor(Hello)
    # goodbye = actor_system.createActor(Goodbye)
    # greeting = actor_system.ask(hello, 'are you there?', timedelta(seconds=1.5))
    # print(greeting + '\n' + actor_system.ask(goodbye, None,
    #                                             timedelta(milliseconds=100)))
    # except  Exception as e:
    #     print(e)

    # actor_system = ActorSystemController(True)
    # capabilities = dict([("Admin Port", 19020)])
    # asys = ActorSystem(systemBase ="multiprocTCPBase", capabilities =capabilities) #@, logDefs=logcfg)
    # asys = ActorSystem('multiprocTCPBase')systemBase = None,
    #    capabilities = None,


def find_mes_directories():
    starting_directory = os.getcwd()
    mes_directories = []
    for root, dirs, files in os.walk(starting_directory, topdown=True):
        if "mes" in dirs and "config" in dirs:
            # assume it is a real MES
            mes_directories.append((root, dirs, files))
    return mes_directories

@app.command()
def basic_simulation_run():
    print("mTree Console")
    mes_list = find_mes_directories()
    mes_simple_list = [mes[0] for mes in mes_list]
    mes_directory = questionary.select(
        "Which MES would you like to run?",
        choices=mes_simple_list,
    ).ask()

    config_directory = os.path.join(mes_directory, "config")    
    config_files = [
            file for file in os.listdir(config_directory) if file.endswith(".json")
        ]
    config_selections = questionary.checkbox(
        "Which configurations would you like to run?",
        choices=config_files,
    ).ask()
    print("Starting to run...")

# @app.command()
# def goodbye(name: str, formal: bool = False):
#     if formal:
#         print(f"Goodbye Ms. {name}. Have a good day.")
#     else:
#         print(f"Bye {name}!")


if __name__ == "__main__":
    app()