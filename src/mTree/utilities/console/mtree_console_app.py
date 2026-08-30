from mTree.utilities.console.dashboard_screen import DashboardScreen
from mTree.utilities.console.mes_library import MESLibrary
from mTree.utilities.console.system_status_screen import SystemStatusScreen
from textual.app import App
# from textual.widgets.option_list import Option, Separator


class MTreeConsoleApp(App):
    """A Textual app to manage stopwatches."""

    CSS_PATH = "option_list.tcss"
    BINDINGS = [
        ("ctrl+d", "quit", "Quit"),
        ("ctrl+s", "switch_mode('system_status')", "System Status"),
        ("ctrl+b", "switch_mode('dashboard')", "Dashboard"),
        ("ctrl+l", "switch_mode('library')", "MES Library"),
        ("ctrl+h", "switch_mode('help')", "Help"),
    ]

    MODES = {
        "dashboard": DashboardScreen,
        "library": MESLibrary,
        # "help": HelpScreen,
        "system_status": SystemStatusScreen,
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
