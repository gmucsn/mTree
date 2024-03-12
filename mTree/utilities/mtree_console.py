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

import atexit

@atexit.register
def goodbye():
    actor_system = ActorSystemStartup()
    actor_system.shutdown()
    print("mTree finished shutting down")


mtree_runner = None

JSON_EXAMPLE = """{
    "glossary": {
        "title": "example glossary",
		"GlossDiv": {
            "title": "S",
			"GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
					"SortAs": "SGML",
					"GlossTerm": "Standard Generalized Markup Language",
					"Acronym": "SGML",
					"Abbrev": "ISO 8879:1986",
					"GlossDef": {
                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
						"GlossSeeAlso": ["GML", "XML"]
                    },
					"GlossSee": "markup"
                }
            }
        }
    }
}
"""


def configuration_files():
    config_directory = os.path.join(os.getcwd(), "config")
    config_files = [file for file in os.listdir(config_directory) if file.endswith('.json')]
    return config_files
    
def load_config_file(config_file):
    config_directory = os.path.join(os.getcwd(), "config")
    read_file = ""
    with open(os.path.join(config_directory, config_file), "r") as i:
        read_file = i.read()

    return read_file

class Runner():
    def __init__(self, running_directory): #, multi_simulation=False):
        self.container = None
        self.running_directory = running_directory
        self.config_directory = os.path.join(running_directory, "config")
        if not os.path.isdir(self.config_directory):
            print("!!! Config directory doesn't exist !!!")
            print("!!! Make sure you are running inside an MES !!!")
            exit()
            
        self.actor_system = ActorSystemConnector()
        # self.component_registry = registry.Registry()
        
        # self.component_registry.register_server(self)
        # self.multi_simulation = multi_simulation
        # self.container = None
        #self.configuration = config_file
        # if self.multi_simulation is not True:
        #     self.configuration = self.load_mtree_config(config_file)
        # else:
        #     self.configuration = self.load_multiple_mtree_config(config_file)
        #print("Current Configuration: ", json.dumps(self.configuration, indent=4, sort_keys=True))
        # self.actor_system = ActorSystemConnector()


    def show_configuration_menu(self):
        config_files = [file for file in os.listdir(self.config_directory) if file.endswith('.json')]
        return config_files
    
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


    # def show_configuration_menu(self):
    #     config_files = [file for file in os.listdir(self.config_directory) if file.endswith('.json')]

    #     terminal_menu = TerminalMenu(
    #         config_files,
    #         multi_select=True,
    #         show_multi_select_hint=True,
    #     )
    #     menu_entry_indices = terminal_menu.show()

    #     if len(menu_entry_indices) == 0:
    #         print("Make sure to select a configuration")

    #     selected_configs = [config_files[selected] for selected in menu_entry_indices]

    #     self.run_simulation_from_configurations(selected_configs)


class Simulations(Static):
    def compose(self) -> ComposeResult:
        with VerticalScroll(id="left-pane"):
            for number in range(15):
                yield Static(f"Vertical layout, child {number}")
        with Horizontal(id="top-right"):
            yield Static("Horizontally")
            yield Static("Positioned")
        # yield OptionList(
        #     Option("Aerilon", id="aer"),
        #     Option("Aquaria", id="aqu"),
        #     Separator(),
        #     Option("Canceron", id="can"),
        #     Option("Caprica", id="cap", disabled=True),
        #     Separator(),
        #     Option("Gemenon", id="gem"),
        #     Separator(),
        #     Option("Leonis", id="leo"),
        #     Option("Libran", id="lib"),
        #     Separator(),
        #     Option("Picon", id="pic"),
        #     Separator(),
        #     Option("Sagittaron", id="sag"),
        #     Option("Scorpia", id="sco"),
        #     Separator(),
        #     Option("Tauron", id="tau"),
        #     Separator(),
        #     Option("Virgon", id="vir"),
        # )

import pyfiglet
from rich import print

title = pyfiglet.figlet_format('mTree Console', font='slant')
# print(f'[magenta]{title}[/magenta]')

class DashboardScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Placeholder(title)
        yield Footer()


class Window(Container):
    pass

class LabelItem(ListItem):

    def __init__(self, label: str) -> None:
        super().__init__()
        self.label = label

    def compose( self ) -> ComposeResult:
        yield Label(self.label)

class SimulationsScreen(Screen):
    
    def compose(self) -> ComposeResult:
        with Container(id="app-grid"):
            with VerticalScroll(id="left-pane"):
                with ListView():
                    for configuration in configuration_files():
                        yield LabelItem(f"{configuration}")
                
            with Horizontal(id="top-right"):
                yield Window(Static(JSON(JSON_EXAMPLE), id='json-view', expand=True),  classes="pad")
            with Horizontal(id="bottom-right"):
                yield Button("Run Simulation", variant="primary")
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected):
        new_json = JSON(load_config_file(event.item.label))
        self.query_one("#json-view",Static).update(new_json)


####
# check_status    force_shutdown  hello           help            kill_run        quit            run_simulation
####

class HelpScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Placeholder("Help Screen")
        yield Footer()

from mTree.utilities.mtree_system_status_screen import MTreeSystemStatusScreen
from mTree.utilities.mtree_run_simulation_screen import MTreeRunSimulationScreen

class MTreeConsole(App):
    """A Textual app to manage stopwatches."""
    CSS_PATH = "option_list.tcss"
    BINDINGS = [("ctrl+q", "quit", "Quit"),
                ("ctrl+s", "switch_mode('system_status')", "System Status"),
                ("ctrl+d", "switch_mode('dashboard')", "Dashboard"),  
                ("ctrl+l", "switch_mode('library')", "MES Library"),
                ("ctrl+h", "switch_mode('help')", "Help"),]

    MODES = {
        "dashboard": DashboardScreen,  
        "library": MTreeRunSimulationScreen,
        "help": HelpScreen,
        "system_status": MTreeSystemStatusScreen
    }

    def on_mount(self) -> None:
        self.switch_mode("dashboard") 

    # def compose(self) -> ComposeResult:
    #     """Create child widgets for the app."""
    #     yield Header()
    #     with TabbedContent(initial="simulations"):
    #         with TabPane("Simulations", id="simulations"):  # First tab
    #             yield Simulations()
    #         with TabPane("Server Status", id="status"):
    #             yield Simulations()
            
    #     yield Footer()

    def action_quit(self) -> None:
        exit()



def main():
    # Set Thespian log file location so we can track issues...
    os.environ['THESPLOG_FILE'] =  os.path.join(os.getcwd(), "thespian.log")
    # TODO Fix and make this selectable from the command line
    os.environ['THESPLOG_THRESHOLD'] =  "DEBUG"

    background_actor_py = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "server", "background_actor_system.py")
    import subprocess
    process = Popen([sys.executable, background_actor_py], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) #, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) #, stdout=PIPE, stderr=PIPE)
    
    #with open(os.devnull, 'w') as DEVNULL:
    # creationflags=subprocess.CREATE_NO_WINDOW|subprocess.DETACHED_PROCESS|subprocess.HIGH_PRIORITY_CLASS
    # process = subprocess.run([sys.executable, background_actor_py], stdout=DEVNULL, stderr=DEVNULL) #, stdout=PIPE, stderr=PIPE)
    # time.sleep(3)
    # mtree_runner = Runner(os.getcwd())
    

    app = MTreeConsole()
    app.run()

if __name__ == "__main__":
    
    main()