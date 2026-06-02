import typer

from pa_cli.config import Config
from pa_cli.crawler.account_crawler import AccountCrawler

app = typer.Typer(help="Account management commands.")


@app.command()
def login():
    """Store password for the current account."""
    password = typer.prompt("Password", hide_input=True)
    Config.save(password=password)
    typer.echo("Password saved successfully.")


@app.command()
def token():
    """Get API token by logging in via crawler."""
    try:
        crawler = AccountCrawler()
        if not crawler.login():
            typer.echo("Login failed. Check your credentials.", err=True)
            raise typer.Exit(code=1)
        new_token = crawler.get_token()
        Config.save(token=new_token)
        typer.echo(f"API token: {new_token}")
        typer.echo("Token saved to config.")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


@app.command()
def extend():
    """Extend account expiry by logging in via crawler."""
    try:
        crawler = AccountCrawler()
        if not crawler.login():
            typer.echo("Login failed. Check your credentials.", err=True)
            raise typer.Exit(code=1)
        if crawler.extend_expiry():
            typer.echo("Account expiry extended successfully.")
        else:
            typer.echo("Failed to extend account expiry.", err=True)
            raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

