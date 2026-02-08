import questionary
import typer
from mTree.generator import Generate
from mTree.simulation import Library

"""
Basic mTree CLI

This file invokes other methods to provide particular services.
"""

app = typer.Typer()


@app.command()
def generate():
    Generate()


@app.command()
def simulation():
    library = Library()
    mes = questionary.select(
        "Which MES would you like to run?",
        choices=library.mes_list,
    ).ask()
    config_selections = questionary.checkbox(
        "Which configurations would you like to run?",
        choices=library.configuration_list(mes),
    ).ask()
    print("Starting to run...")


if __name__ == "__main__":
    app()
