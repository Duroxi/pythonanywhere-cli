import typer

from pa_cli.config import Config

app = typer.Typer(help="Account management commands.")


@app.command()
def login():
    """Store password for the current account."""
    password = typer.prompt("Password", hide_input=True)
    Config.save(password=password)
    typer.echo("Password saved successfully.")

