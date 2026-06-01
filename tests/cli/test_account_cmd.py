from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

from pa_cli.cli.account_cmd import app

runner = CliRunner()


def test_login_prompts_for_password():
    with patch("pa_cli.cli.account_cmd.Config.save") as mock_save:
        result = runner.invoke(app, input="secret\n")

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
