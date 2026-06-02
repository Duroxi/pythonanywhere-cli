from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

from pa_cli.cli.consoles_cmd import app

runner = CliRunner()


def test_console_list():
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_client.list.return_value = [
            {"id": 1, "name": "bash"},
            {"id": 2, "name": "python3.10"},
        ]
        mock_cls.return_value = mock_client

        result = runner.invoke(app, ["list"])

    assert result.exit_code == 0
    assert "ID: 1, Name: bash" in result.output
    assert "ID: 2, Name: python3.10" in result.output


def test_console_list_empty():
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_client.list.return_value = []
        mock_cls.return_value = mock_client

        result = runner.invoke(app, ["list"])

    assert result.exit_code == 0
    assert "No consoles found." in result.output


def test_console_activate_no_password():
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}

        result = runner.invoke(app, ["activate", "42"])

    assert result.exit_code == 1
    assert "Password not found" in result.output


def test_console_activate_success():
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.crawler.console_crawler.ConsoleCrawler") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h", "password": "p"}
        mock_crawler = MagicMock()
        mock_cls.return_value = mock_crawler

        result = runner.invoke(app, ["activate", "42"])

    assert result.exit_code == 0
    assert "Console 42 activated successfully." in result.output
    mock_crawler.login.assert_called_once_with("u", "p")
    mock_crawler.activate.assert_called_once_with("u", 42)


def test_console_activate_error():
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.crawler.console_crawler.ConsoleCrawler") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h", "password": "p"}
        mock_crawler = MagicMock()
        mock_crawler.login.side_effect = Exception("Login failed")
        mock_cls.return_value = mock_crawler

        result = runner.invoke(app, ["activate", "42"])

    assert result.exit_code == 1
    assert "Login failed" in result.output


def test_console_create():
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_client.create.return_value = {"id": 42, "executable": "bash"}
        mock_cls.return_value = mock_client

        result = runner.invoke(app, ["create"])

    assert result.exit_code == 0
    assert "42" in result.output


def test_console_send():
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_cls.return_value = mock_client

        result = runner.invoke(app, ["send", "42", "ls"])

    assert result.exit_code == 0


def test_console_output():
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_client.get_output.return_value = {"output": "file1.txt\n"}
        mock_cls.return_value = mock_client

        result = runner.invoke(app, ["output", "42"])

    assert result.exit_code == 0
    assert "file1.txt" in result.output


def test_console_kill():
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_cls.return_value = mock_client

        result = runner.invoke(app, ["kill", "42"])

    assert result.exit_code == 0
