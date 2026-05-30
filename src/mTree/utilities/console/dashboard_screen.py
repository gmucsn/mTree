import pyfiglet
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import (
    Footer,
    Placeholder,
)
# from textual.widgets.option_list import Option, Separator

title = pyfiglet.figlet_format("mTree Console", font="slant")


class DashboardScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Placeholder(title)
        yield Footer()
