from mTree.utilities.console.dashboard_screen import DashboardScreen
from mTree.utilities.console.mes_library import MESLibrary
from mTree.utilities.console.system_status_screen import SystemStatusScreen
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
from textual.screen import Screen
from textual.widgets import (
    Button,
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

# from textual.widgets.option_list import Option, Separator


class SimulationViewer(App):
    """A Textual app to manage stopwatches."""

    CSS_PATH = "option_list.tcss"
    BINDINGS = [
        ("ctrl+d", "quit", "Quit"),
    ]

    MODES = {
        "system_status": SystemStatusScreen,
    }

    def on_mount(self) -> None:
        self.switch_mode("system_status")

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
