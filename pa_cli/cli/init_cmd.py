import typer

from pa_cli.config import Config

app = typer.Typer(help="Configure PythonAnywhere account.")


@app.command()
def init():
    """Interactive setup for PythonAnywhere account."""
    username = typer.prompt("PythonAnywhere username")
    token = typer.prompt("API Token", hide_input=True)
    host = typer.prompt("Host", default="www.pythonanywhere.com")

    Config.save(username=username, token=token, host=host)
    typer.echo(f"Account '{username}' configured successfully.")
