from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

from pa_cli.cli.consoles_cmd import app

runner = CliRunner()


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
