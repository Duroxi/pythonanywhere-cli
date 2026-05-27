from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

from pa_cli.cli.init_cmd import app

runner = CliRunner()


def test_init_saves_config(tmp_path):
    config_path = tmp_path / "config.json"
    with patch("pa_cli.cli.init_cmd.Config.save") as mock_save:
        result = runner.invoke(app, input="testuser\nabc123\n\n")

    assert result.exit_code == 0
    mock_save.assert_called_once_with(username="testuser", token="abc123", host="www.pythonanywhere.com")
