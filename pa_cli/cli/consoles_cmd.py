import time
import uuid

import typer

from pa_cli.api.consoles import ConsolesClient
from pa_cli.cli.utils import get_client
from pa_cli.config import Config
from pa_cli.exceptions import APIError, AuthError, NetworkError

app = typer.Typer(help="Manage consoles on PythonAnywhere.")


@app.command("list")
def list_consoles():
    """List all consoles."""
    try:
        account, client = get_client(ConsolesClient)
        consoles = client.list(account["username"])
        if not consoles:
            typer.echo("No consoles found.")
            return
        for console in consoles:
            typer.echo(f"ID: {console['id']}, Name: {console['name']}")
    except NetworkError as e:
        typer.echo(f"Network error: {e}", err=True)
        raise typer.Exit(code=1)
    except APIError as e:
        typer.echo(f"API error: {e}", err=True)
        raise typer.Exit(code=1)


@app.command()
def activate(
    console_id: int = typer.Argument(..., help="Console ID"),
):
    """Activate a console via WebSocket (requires login)."""
    try:
        from pa_cli.crawler.console_crawler import ConsoleCrawler

        account = Config.load(verbose=True)

        if "password" not in account:
            typer.echo("Password not found. Run 'pa account login' first.", err=True)
            raise typer.Exit(code=1)

        crawler = ConsoleCrawler(host=account.get("host", "www.pythonanywhere.com"))
        crawler.login(account["username"], account["password"])
        crawler.activate(account["username"], console_id)
        typer.echo(f"Console {console_id} activated successfully.")
    except AuthError as e:
        typer.echo(f"Auth error: {e}", err=True)
        raise typer.Exit(code=1)
    except NetworkError as e:
        typer.echo(f"Network error: {e}", err=True)
        raise typer.Exit(code=1)


@app.command()
def create(
    executable: str = typer.Option("bash", help="Console executable"),
):
    """Create a new console."""
    try:
        account, client = get_client(ConsolesClient)
        result = client.create(account["username"], executable)
        typer.echo(f"Console created: id={result['id']}, executable={result['executable']}")
    except NetworkError as e:
        typer.echo(f"Network error: {e}", err=True)
        raise typer.Exit(code=1)
    except APIError as e:
        typer.echo(f"API error: {e}", err=True)
        raise typer.Exit(code=1)


def _ensure_console(account: dict, client: ConsolesClient, executable: str = "bash") -> int:
    """Get an existing console or create a new one via crawler. Returns console_id."""
    from pa_cli.crawler.console_crawler import ConsoleCrawler

    # Try to find an existing console via API
    consoles = client.list(account["username"])
    if consoles:
        return consoles[0]["id"]

    # No console exists, create via crawler
    if "password" not in account:
        raise AuthError("Password not found. Run 'pa account login' first.")

    crawler = ConsoleCrawler(host=account.get("host", "www.pythonanywhere.com"))
    crawler.login(account["username"], account["password"])
    return crawler.get_or_create(account["username"], executable=executable)


def _ensure_activated(account: dict, console_id: int) -> None:
    """Activate a console via crawler WebSocket. Raises AuthError if password missing."""
    from pa_cli.crawler.console_crawler import ConsoleCrawler

    if "password" not in account:
        raise AuthError("Password not found. Run 'pa account login' first.")

    crawler = ConsoleCrawler(host=account.get("host", "www.pythonanywhere.com"))
    crawler.login(account["username"], account["password"])
    crawler.activate(account["username"], console_id)


@app.command()
def send(
    command: str = typer.Argument(..., help="Command to send"),
    console_id: int = typer.Argument(None, help="Console ID (auto-detected if omitted)"),
    wait: bool = typer.Option(True, "--wait/--no-wait", "-w/-W", help="Wait for output"),
    timeout: int = typer.Option(30, "--timeout", "-t", help="Max seconds to wait for output"),
):
    """Send input to a console and get output. Auto-creates and activates if needed."""
    try:
        account, client = get_client(ConsolesClient)
    except (AuthError, NetworkError, APIError) as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

    # Auto-detect or create console
    if console_id is None:
        try:
            console_id = _ensure_console(account, client)
        except AuthError as e:
            typer.echo(f"Auth error: {e}", err=True)
            raise typer.Exit(code=1)
        except NetworkError as e:
            typer.echo(f"Network error: {e}", err=True)
            raise typer.Exit(code=1)

    if not wait:
        try:
            client.send_input(account["username"], console_id, command + "\n")
        except APIError:
            # Likely 412: console not activated
            try:
                _ensure_activated(account, console_id)
                client.send_input(account["username"], console_id, command + "\n")
            except AuthError as e:
                typer.echo(f"Auth error: {e}", err=True)
                raise typer.Exit(code=1)
            except NetworkError as e:
                typer.echo(f"Network error: {e}", err=True)
                raise typer.Exit(code=1)
            except APIError as e:
                typer.echo(f"API error: {e}", err=True)
                raise typer.Exit(code=1)
        typer.echo(f"Sent to console {console_id}: {command}")
        return

    # Get baseline output before sending command
    try:
        baseline = client.get_output(account["username"], console_id)
    except APIError:
        # 412: console not activated, activate and retry
        try:
            _ensure_activated(account, console_id)
            baseline = client.get_output(account["username"], console_id)
        except AuthError as e:
            typer.echo(f"Auth error: {e}", err=True)
            raise typer.Exit(code=1)
        except NetworkError as e:
            typer.echo(f"Network error: {e}", err=True)
            raise typer.Exit(code=1)
        except APIError as e:
            typer.echo(f"API error: {e}", err=True)
            raise typer.Exit(code=1)

    baseline_output = baseline.get("output", "")

    # Generate unique completion marker
    marker = f"__PA_CLI_DONE_{int(time.time())}_{uuid.uuid4().hex}__"

    # Send command + marker echo
    try:
        client.send_input(
            account["username"],
            console_id,
            f"{command}\necho {marker}\n",
        )
    except APIError:
        try:
            _ensure_activated(account, console_id)
            client.send_input(
                account["username"],
                console_id,
                f"{command}\necho {marker}\n",
            )
        except AuthError as e:
            typer.echo(f"Auth error: {e}", err=True)
            raise typer.Exit(code=1)
        except NetworkError as e:
            typer.echo(f"Network error: {e}", err=True)
            raise typer.Exit(code=1)
        except APIError as e:
            typer.echo(f"API error: {e}", err=True)
            raise typer.Exit(code=1)

    # Poll for marker
    elapsed = 0.0
    poll_interval = 0.5
    while elapsed < timeout:
        time.sleep(poll_interval)
        elapsed += poll_interval
        try:
            result = client.get_output(account["username"], console_id)
        except (APIError, NetworkError):
            # Transient error during polling, keep trying
            continue
        output = result.get("output", "")

        if marker in output and output != baseline_output:
            new_output = output[len(baseline_output):]
            lines = new_output.split("\n")
            user_lines = []
            for line in lines:
                if marker in line:
                    break
                user_lines.append(line)
            typer.echo("\n".join(user_lines).strip() or "(no output)")
            return

    typer.echo("Timeout waiting for command output", err=True)
    raise typer.Exit(code=1)


@app.command("get-or-create")
def get_or_create(
    executable: str = typer.Option("bash", "--executable", "-e", help="Console executable"),
):
    """Get an existing console or create a new one. Prefer using 'send' directly."""
    try:
        from pa_cli.crawler.console_crawler import ConsoleCrawler

        account = Config.load(verbose=True)

        if "password" not in account:
            typer.echo("Password not found. Run 'pa account login' first.", err=True)
            raise typer.Exit(code=1)

        crawler = ConsoleCrawler(host=account.get("host", "www.pythonanywhere.com"))
        crawler.login(account["username"], account["password"])
        console_id = crawler.get_or_create(account["username"], executable=executable)
        typer.echo(f"Console ready: {console_id}")
    except AuthError as e:
        typer.echo(f"Auth error: {e}", err=True)
        raise typer.Exit(code=1)
    except NetworkError as e:
        typer.echo(f"Network error: {e}", err=True)
        raise typer.Exit(code=1)


@app.command()
def kill(
    console_id: int = typer.Argument(..., help="Console ID"),
):
    """Kill a console."""
    try:
        account, client = get_client(ConsolesClient)
        client.kill(account["username"], console_id)
        typer.echo(f"Console {console_id} killed.")
    except NetworkError as e:
        typer.echo(f"Network error: {e}", err=True)
        raise typer.Exit(code=1)
    except APIError as e:
        typer.echo(f"API error: {e}", err=True)
        raise typer.Exit(code=1)
