from mTree.utilities.console.system_status_screen import SystemStatusScreen
from textual.app import App

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
