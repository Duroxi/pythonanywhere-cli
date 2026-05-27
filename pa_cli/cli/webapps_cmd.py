import typer

from pa_cli.api.webapps import WebappsClient
from pa_cli.config import Config

app = typer.Typer(help="Manage web apps on PythonAnywhere.")


def _get_client() -> tuple:
    account = Config.load()
    client = WebappsClient(token=account["token"], host=account["host"])
    return account, client


@app.command()
def create(
    domain_name: str = typer.Argument(..., help="Domain name"),
    python_version: str = typer.Option("python310", "--python", "-p", help="Python version"),
):
    """Create a new web app."""
    account, client = _get_client()
    client.create(account["username"], domain_name, python_version)
    typer.echo(f"Webapp {domain_name} created with {python_version}")


@app.command()
def config(
    domain_name: str = typer.Argument(..., help="Domain name"),
    source_dir: str = typer.Option(..., "--source-dir", "-s", help="Source directory path"),
    virtualenv: str = typer.Option(None, "--virtualenv", "-v", help="Virtualenv path"),
):
    """Configure a web app."""
    account, client = _get_client()
    kwargs = {"source_directory": source_dir}
    if virtualenv:
        kwargs["virtualenv_path"] = virtualenv
    client.update(account["username"], domain_name, **kwargs)
    typer.echo(f"Webapp {domain_name} configured.")


@app.command()
def static(
    domain_name: str = typer.Argument(..., help="Domain name"),
    url: str = typer.Option(..., "--url", help="URL prefix"),
    path: str = typer.Option(..., "--path", help="Directory path"),
):
    """Add a static file mapping."""
    account, client = _get_client()
    client.add_static_file(account["username"], domain_name, url=url, path=path)
    typer.echo(f"Static mapping added: {url} -> {path}")


@app.command()
def reload(
    domain_name: str = typer.Argument(..., help="Domain name"),
):
    """Reload a web app."""
    account, client = _get_client()
    client.reload(account["username"], domain_name)
    typer.echo(f"Webapp {domain_name} reloaded.")
