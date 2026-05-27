import typer

from pa_cli.api.consoles import ConsolesClient
from pa_cli.config import Config

app = typer.Typer(help="Manage consoles on PythonAnywhere.")


def _get_client() -> tuple:
    account = Config.load()
    client = ConsolesClient(token=account["token"], host=account["host"])
    return account, client


@app.command()
def create(
    executable: str = typer.Option("bash", help="Console executable"),
):
    """Create a new console."""
    account, client = _get_client()
    result = client.create(account["username"], executable)
    typer.echo(f"Console created: id={result['id']}, executable={result['executable']}")


@app.command()
def send(
    console_id: int = typer.Argument(..., help="Console ID"),
    command: str = typer.Argument(..., help="Command to send"),
):
    """Send input to a console."""
    account, client = _get_client()
    client.send_input(account["username"], console_id, command + "\n")
    typer.echo(f"Sent to console {console_id}: {command}")


@app.command()
def output(
    console_id: int = typer.Argument(..., help="Console ID"),
):
    """Get latest output from a console."""
    account, client = _get_client()
    result = client.get_output(account["username"], console_id)
    typer.echo(result.get("output", "(no output)"))


@app.command()
def kill(
    console_id: int = typer.Argument(..., help="Console ID"),
):
    """Kill a console."""
    account, client = _get_client()
    client.kill(account["username"], console_id)
    typer.echo(f"Console {console_id} killed.")
