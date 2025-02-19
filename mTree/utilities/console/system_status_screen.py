import atexit
import os
import sys
# from thespian.actors import *
import time
from datetime import datetime
from subprocess import PIPE, Popen

import pyfiglet
from mTree.system.actor_system_connector import ActorSystemConnector
from rich import box
from rich.console import RenderableType
from rich.json import JSON
from rich.markdown import Markdown
from rich.markup import escape
from rich.pretty import Pretty
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.coordinate import Coordinate
from textual.screen import Screen
from textual.timer import Timer
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Label,
    ListItem,
    ListView,
    OptionList,
    Placeholder,
    Static,
    Tab,
    TabbedContent,
    TabPane,
    Tabs,
)
from textual.widgets.option_list import Option, Separator

# from mTree.runner.runner import Runner
# from mTree.server.actor_system_startup import ActorSystemStartup
# from mTree.server.actor_system_connector import ActorSystemConnector




# import subprocess








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


# from mTree.server.actor_system_connector import ActorSystemConnector

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


class SystemStatusScreen(Screen):
    _refresh_timer: Timer | None

    def compose(self) -> ComposeResult:
        yield Static("Status Information", classes="label")
        yield Static("System Last Checked: ", id="last-status-check", classes="label")
        yield DataTable(id="system-status-table")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_column("Actor", key="actor")
        table.add_column("Status", key="status")
        table.add_column("pid", key="pid")
        table.add_column("CPU", key="cpu")
        table.add_column("Mem", key="mem")
        table.add_column("Started", key="started")

        self._refresh_timer = self.set_interval(2, self.update_status)

        statuses = ActorSystemConnector.get_status()
        for status_item in statuses:
            table.add_row(
                status_item.actor_name,
                status_item.status,
                status_item.pid,
                status_item.cpu_usage,
                status_item.human_readable_memory(),
                status_item.started,
                key=str(status_item.pid),
            )
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

        table = self.query_one(DataTable)
        statuses = ActorSystemConnector.get_status()
        for status_item in statuses:
            try:
                table.get_row(str(status_item.pid))
                table.update_cell(str(status_item.pid), "status", status_item.status)
                table.update_cell(str(status_item.pid), "cpu", status_item.cpu_usage)
                table.update_cell(
                    str(status_item.pid), "mem", status_item.human_readable_memory()
                )

                # table.update_cell_at(Coordinate(row_index, 0), status_item.actor_name)
                # table.update_cell_at(Coordinate(row_index, 1), status_item.status)
                # table.update_cell_at(Coordinate(row_index, 2), status_item.pid)
                # table.update_cell_at(Coordinate(row_index, 3), status_item.cpu_usage)
                # table.update_cell_at(Coordinate(row_index, 4), status_item.memory_usage)
                # table.update_cell_at(Coordinate(row_index, 5), status_item.started)
            except:
                table.add_row(
                    status_item.actor_name,
                    status_item.status,
                    status_item.pid,
                    status_item.cpu_usage,
                    status_item.human_readable_memory(),
                    status_item.started,
                    key=str(status_item.pid),
                )

        # for run_status in statuses:
        #     try:
        #         row_index = status_table.get_row_index(run_status[0])
        #         for index, i in enumerate(run_status):
        #             status_table.update_cell_at(Coordinate(row_index, index), i)
        #     except:
        #         status_table.add_row(
        #             run_status[0],
        #             run_status[1],
        #             run_status[2],
        #             run_status[3],
        #             run_status[4],
        #             key=run_status[0],
        #         )

        last_status_check = self.query_one("#last-status-check")
        last_status_check.update(f"System Last Checked: {datetime.now().isoformat()}")

        # if statuses is None:
        #     table_data.append(["No Simulations Runnings"])
        # else:
        #     table_data.extend(statuses)
        # table = AsciiTable(table_data)
        # print(table.table)
