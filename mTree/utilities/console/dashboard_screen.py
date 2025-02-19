import pyfiglet
from rich import box, print
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
from textual.widgets.option_list import Option, Separator

title = pyfiglet.figlet_format("mTree Console", font="slant")


class DashboardScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Placeholder(title)
        yield Footer()
