from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

from pa_cli.cli.account_cmd import app

runner = CliRunner()


def test_login_prompts_for_password():
    with patch("pa_cli.cli.account_cmd.Config.save") as mock_save:
        result = runner.invoke(app, ["login"], input="secret\n")

    assert result.exit_code == 0
    mock_save.assert_called_once_with(password="secret")
    assert "Password saved" in result.output


def test_login_uses_hidden_input():
    with patch("pa_cli.cli.account_cmd.Config.save"):
        with patch("pa_cli.cli.account_cmd.typer") as mock_typer:
            mock_typer.prompt.return_value = "secret"
            mock_typer.echo = MagicMock()
            from pa_cli.cli.account_cmd import login
            login()

    mock_typer.prompt.assert_called_once_with("Password", hide_input=True)


# --- token command tests ---


def test_token_command_logs_in_and_gets_token():
    """token command creates crawler, logs in, gets token, and saves it."""
    with patch("pa_cli.cli.account_cmd.AccountCrawler") as mock_cls:
        mock_crawler = MagicMock()
        mock_crawler.login.return_value = True
        mock_crawler.get_token.return_value = "abc123token"
        mock_cls.return_value = mock_crawler

        with patch("pa_cli.cli.account_cmd.Config.save") as mock_save:
            result = runner.invoke(app, ["token"])

    assert result.exit_code == 0
    mock_crawler.login.assert_called_once()
    mock_crawler.get_token.assert_called_once()
    mock_save.assert_called_once_with(token="abc123token")
    assert "abc123token" in result.output


def test_token_command_exits_on_login_failure():
    """token command exits with error when login returns False."""
    with patch("pa_cli.cli.account_cmd.AccountCrawler") as mock_cls:
        mock_crawler = MagicMock()
        mock_crawler.login.return_value = False
        mock_cls.return_value = mock_crawler

        result = runner.invoke(app, ["token"])

    assert result.exit_code == 1
    assert "Login failed" in result.output


def test_token_command_exits_on_login_exception():
    """token command exits with error when login raises exception."""
    with patch("pa_cli.cli.account_cmd.AccountCrawler") as mock_cls:
        mock_crawler = MagicMock()
        mock_crawler.login.side_effect = ValueError("Password not found in config")
        mock_cls.return_value = mock_crawler

        result = runner.invoke(app, ["token"])

    assert result.exit_code == 1
    assert "Password not found" in result.output


# --- extend command tests ---


def test_extend_command_logs_in_and_extends():
    """extend command creates crawler, logs in, and extends account expiry."""
    with patch("pa_cli.cli.account_cmd.AccountCrawler") as mock_cls:
        mock_crawler = MagicMock()
        mock_crawler.login.return_value = True
        mock_crawler.extend_expiry.return_value = True
        mock_cls.return_value = mock_crawler

        result = runner.invoke(app, ["extend"])

    assert result.exit_code == 0
    mock_crawler.login.assert_called_once()
    mock_crawler.extend_expiry.assert_called_once()
    assert "extended" in result.output.lower()


def test_extend_command_exits_on_login_failure():
    """extend command exits with error when login returns False."""
    with patch("pa_cli.cli.account_cmd.AccountCrawler") as mock_cls:
        mock_crawler = MagicMock()
        mock_crawler.login.return_value = False
        mock_cls.return_value = mock_crawler

        result = runner.invoke(app, ["extend"])

    assert result.exit_code == 1
    assert "Login failed" in result.output


def test_extend_command_exits_on_extend_failure():
    """extend command exits with error when extend_expiry returns False."""
    with patch("pa_cli.cli.account_cmd.AccountCrawler") as mock_cls:
        mock_crawler = MagicMock()
        mock_crawler.login.return_value = True
        mock_crawler.extend_expiry.return_value = False
        mock_cls.return_value = mock_crawler

        result = runner.invoke(app, ["extend"])

    assert result.exit_code == 1
    assert "Failed to extend" in result.output


def test_extend_command_exits_on_login_exception():
    """extend command exits with error when login raises exception."""
    with patch("pa_cli.cli.account_cmd.AccountCrawler") as mock_cls:
        mock_crawler = MagicMock()
        mock_crawler.login.side_effect = ValueError("Password not found in config")
        mock_cls.return_value = mock_crawler

        result = runner.invoke(app, ["extend"])

    assert result.exit_code == 1
    assert "Password not found" in result.output
