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
from textual.coordinate import Coordinate
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

ROWS = [
    ("lane", "swimmer", "country", "time"),
    (4, "Joseph Schooling", "Singapore", 50.39),
    (2, "Michael Phelps", "United States", 51.14),
    (5, "Chad le Clos", "South Africa", 51.14),
    (6, "László Cseh", "Hungary", 51.14),
    (3, "Li Zhuhao", "China", 51.26),
    (8, "Mehdy Metella", "France", 51.58),
    (7, "Tom Shields", "United States", 51.73),
    (1, "Aleksandr Sadovnikov", "Russia", 51.84),
    (10, "Darren Burns", "Scotland", 51.84),
]


from mTree.server.actor_system_connector import ActorSystemConnector

# table_data = [
#             ['Run Code', 'Configuration', 'Run Number', 'Status', 'Total Time'],
#         ]
#         actor_system = ActorSystemConnector()
#         statuses = actor_system.get_status()
#         print("STATUS REPORTING")
#         print(statuses)
#         if statuses is None:
#             table_data.append(["No Simulations Runnings"])
#         else:
#             table_data.extend(statuses)
#         table = AsciiTable(table_data)
#         print(table.table)


class MTreeSystemStatusScreen(Screen):
    _refresh_timer: Timer | None

    def compose(self) -> ComposeResult:
        yield Static("Status Information", classes="label")
        yield Static("System Last Checked: ", id="last-status-check", classes="label")
        yield DataTable(id="system-status-table")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns('Run Code', 'Configuration', 'Run Number', 'Status', 'Total Time')
        self._refresh_timer = self.set_interval(2, self.update_status)

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


    def update_status(self) -> None:
        actor_system = ActorSystemConnector()
        statuses = actor_system.get_status()
        
        status_table = self.query_one("#system-status-table")

        for run_status in statuses:
            try: 
                row_index = status_table.get_row_index(run_status[0])
                for index, i in enumerate(run_status):
                    status_table.update_cell_at(Coordinate(row_index, index), i)
            except:
                status_table.add_row(run_status[0], run_status[1], run_status[2], run_status[3], run_status[4], key=run_status[0])

        last_status_check = self.query_one("#last-status-check")
        last_status_check.update(f"System Last Checked: {datetime.now().isoformat()}")
        
        # if statuses is None:
        #     table_data.append(["No Simulations Runnings"])
        # else:
        #     table_data.extend(statuses)
        # table = AsciiTable(table_data)
        # print(table.table)

