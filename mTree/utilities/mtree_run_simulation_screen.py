import sys
import os
import sys
import pyfiglet

# from mTree.runner.runner import Runner
from mTree.server.actor_system_startup import ActorSystemStartup
from mTree.server.actor_system_connector import ActorSystemConnector
# from thespian.actors import *
import time

import atexit
from subprocess import Popen, PIPE
# import subprocess


from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Header, Footer, Tab, Tabs, Static, Button, TabbedContent, TabPane, OptionList, Placeholder, ListItem, ListView, Label
from textual.widgets.option_list import Option, Separator
from rich import box
from rich.console import RenderableType
from rich.json import JSON
from rich.markdown import Markdown
from rich.markup import escape
from rich.pretty import Pretty
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from datetime import datetime


import atexit


from textual.app import App, ComposeResult
from textual.widgets import DataTable
from textual.timer import Timer
from textual.widgets import Tree, SelectionList
from mTree.server.actor_system_connector import ActorSystemConnector
from mTree.simulation.mes_simulation_library import MESSimulationLibrary





def run_simulation_from_configurations(config_dir, configurations):
    for configuration in configurations:
        working_dir = config_dir
        #actor_system.send_message()
        configuration_good = True
        try:
            simulation_library = MESSimulationLibrary()
            simulation_library.list_simulation_files_directory(working_dir)
            list_simulations = simulation_library.simulations
            configuration_name = os.path.basename(configuration)
            simulation = simulation_library.get_simulation_by_filename(configuration_name)
            
        except Exception as e:
            configuration_good = False    
            
        if configuration_good:
            actor_system = ActorSystemConnector()
            working_dir = config_dir
            #actor_system.send_message()
            actor_system.run_simulation(working_dir, configuration, simulation["description"].to_hash())

            # self.examine_directory()
            # if self.multi_simulation is False:
            #     self.launch_multi_simulations()
            # else:
            #     self.launch_multi_simulations()


def find_mes_directories():
    starting_directory = os.getcwd()
    mes_directories = []
    for (root,dirs,files) in os.walk(starting_directory, topdown=True): 
        if "mes" in dirs and "config" in dirs:
            # assume it is a real MES
            mes_directories.append((root, dirs, files))
    return mes_directories

class MTreeRunSimulationSetupScreen(Screen):
    _refresh_timer: Timer | None

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        mes_location: str = None
    ) -> None:
        super().__init__(name=name, id=id, classes=classes)
        self.mes_location = mes_location._label.plain
        
    def compose(self) -> ComposeResult:
        yield Static("MES Setup a Simulation", classes="label")
        yield Static("MES Location: ", id="mes-location", classes="label")
        yield SelectionList(id="config-select")
        yield Button("Run Simulation Configuration", id="run-simulation-configurations")
        yield Footer()

    def on_mount(self) -> None:
        mes_location = self.query_one("#mes-location")
        config_select = self.query_one("#config-select")
        mes_location.update(f"MES Location: {self.mes_location}")
        working_dir = self.mes_location
        config_directory = os.path.join(working_dir, "config")
        # #actor_system.send_message()
        # simulation_library = MESSimulationLibrary()
        # simulation_library.list_simulation_files_directory(working_dir)
        
        # simulation = simulation_library.get_simulation_by_filename(os.path.basename(self.configuration))
        # actor_system = ActorSystemConnector()
        # working_dir = os.getcwd()
        # #actor_system.send_message()
        # actor_system.run_simulation(working_dir, simulation["description"].to_hash())



        config_files = [file for file in os.listdir(config_directory) if file.endswith('.json')]
        self.config_selections = []
        for config_index, config in enumerate(config_files):
            config_select.add_option(item=(config, config_index))
            self.config_selections.append(config)
        # terminal_menu = TerminalMenu(
        #     config_files,
        #     multi_select=True,
        #     show_multi_select_hint=True,
        # )
        # menu_entry_indices = terminal_menu.show()

        # if len(menu_entry_indices) == 0:
        #     print("Make sure to select a configuration")

        # selected_configs = [config_files[selected] for selected in menu_entry_indices]

        # self.run_simulation_from_configurations(selected_configs)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        config_select = self.query_one("#config-select")
        tester = config_select.selected
        selections = [self.config_selections[config] for config in config_select.selected]
        run_simulation_from_configurations(self.mes_location, selections)
        
        self.app.pop_screen()
        self.app.switch_mode("system_status") 
        # self.app.push_screen(MTreeRunSimulationSetupScreen(mes_location=self._selected_location))
    


class MTreeRunSimulationScreen(Screen):
    _refresh_timer: Timer | None
    _selected_location: str | None

    def compose(self) -> ComposeResult:
        yield Static("MES Library", classes="label")
        tree: Tree[dict] = Tree("MES Library", id="mes-library")
        tree.root.expand()
        yield tree
        yield Button("Load Selected Simulation", id="load-selected-simulation")
        yield Footer()

    def on_mount(self) -> None:
        mes_tree = self.query_one("#mes-library")

        mes_list = find_mes_directories()
        for mes in mes_list:            
            new_mes = mes_tree.root.add(mes[0], expand=True)
            new_mes.add_leaf(mes[0])
        
    def on_tree_node_selected(self, event):
        event.stop()
        self._selected_location = event.node


    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.push_screen(MTreeRunSimulationSetupScreen(mes_location=self._selected_location))
        #str(event.button)

        # self.name = configuration["name"]
        # self.id = configuration["id"]
        # self.run_number = run_number
        
        # hash_basis = str(self.name) + "-" + str(self.id) + "-" + str(self.run_number) + str(random.uniform(0,100))
        # hash_object = hashlib.sha1(hash_basis.encode("utf-8"))
        # self.run_code = hash_object.hexdigest()[0:6]

        # self.status = "Registered"
        # self.mes_base_address = None
        # self.start_time = None
        # self.end_time = None


