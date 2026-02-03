import typer
from mTree.generator import Generate

"""
Basic mTree CLI

This file invokes other methods to provide particular services.
"""

app = typer.Typer()


@app.command()
def generate():
    Generate()


if __name__ == "__main__":
    app()
