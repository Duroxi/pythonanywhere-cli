from pathlib import Path

import typer

from pa_cli.api.files import FilesClient
from pa_cli.config import Config

app = typer.Typer(help="Manage files on PythonAnywhere.")


@app.callback()
def main():
    """Manage files on PythonAnywhere."""
    pass


@app.command()
def upload(
    local_path: str = typer.Argument(..., help="Local file or directory path"),
    remote_path: str = typer.Argument(..., help="Remote path on PythonAnywhere"),
    recursive: bool = typer.Option(False, "-r", "--recursive", help="Upload directory recursively"),
):
    """Upload a file or directory to PythonAnywhere."""
    local = Path(local_path)

    if not local.exists():
        typer.echo(f"Error: {local_path} does not exist")
        raise typer.Exit(code=1)

    if local.is_dir() and not recursive:
        typer.echo("Error: Use -r/--recursive to upload directories")
        raise typer.Exit(code=1)

    account = Config.load()
    client = FilesClient(token=account["token"], host=account["host"])

    if local.is_file():
        content = local.read_bytes()
        status = client.upload(account["username"], remote_path, content)
        typer.echo(f"Uploaded {local_path} -> {remote_path} (HTTP {status})")
    else:
        # Recursive directory upload
        count = 0
        for file in local.rglob("*"):
            if file.is_file():
                relative = file.relative_to(local)
                remote = f"{remote_path.rstrip('/')}/{relative}".replace("\\", "/")
                content = file.read_bytes()
                client.upload(account["username"], remote, content)
                count += 1
        typer.echo(f"Uploaded {count} files to {remote_path}")
