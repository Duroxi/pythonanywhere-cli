import typer

from pa_cli.config import Config

app = typer.Typer(help="Configure PythonAnywhere account.")


@app.command()
def init():
    """Interactive setup for PythonAnywhere account."""
    username = typer.prompt("PythonAnywhere username")
    token = typer.prompt("API Token", hide_input=True)
    host = typer.prompt("Host", default="www.pythonanywhere.com")
    password = typer.prompt("Password (optional, press Enter to skip)", default="", hide_input=True)

    save_kwargs = dict(username=username, token=token, host=host)
    if password:
        save_kwargs["password"] = password

    Config.save(**save_kwargs)
    typer.echo(f"Account '{username}' configured successfully.")
