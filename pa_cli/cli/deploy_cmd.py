import typer

from pa_cli.config import Config
from pa_cli.workflows.deploy import deploy as deploy_workflow

app = typer.Typer(help="Deploy a local project to PythonAnywhere.")


@app.command()
def deploy(
    local_dir: str = typer.Argument(..., help="Local project directory"),
    domain: str = typer.Option(None, "--domain", "-d", help="Domain name (default: {username}.pythonanywhere.com)"),
    python_version: str = typer.Option("python310", "--python", "-p", help="Python version"),
):
    """Deploy a local project to PythonAnywhere."""
    account = Config.load()

    if domain is None:
        domain = f"{account['username']}.pythonanywhere.com"

    url = deploy_workflow(
        local_dir=local_dir,
        username=account["username"],
        token=account["token"],
        host=account["host"],
        domain=domain,
        python_version=python_version,
    )

    typer.echo(f"\nDeployed! Visit: {url}")
