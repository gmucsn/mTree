
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import (
    Header,
    Footer,
    Tab,
    Tabs,
    Static,
    Button,
    TabbedContent,
    TabPane,
    OptionList,
    Placeholder,
    ListItem,
    ListView,
    Label,
)
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


import pyfiglet
from rich import print

title = pyfiglet.figlet_format("mTree Console", font="slant")


class DashboardScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Placeholder(title)
        yield Footer()
