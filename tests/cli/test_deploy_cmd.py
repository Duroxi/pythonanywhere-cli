from unittest.mock import patch
from typer.testing import CliRunner

from pa_cli.cli.deploy_cmd import app

runner = CliRunner()


def test_deploy_command():
    with patch("pa_cli.cli.deploy_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.deploy_cmd.deploy_workflow") as mock_deploy:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}
        mock_deploy.return_value = "https://u.pythonanywhere.com"

        result = runner.invoke(app, ["./mysite"])

    assert result.exit_code == 0
    assert "u.pythonanywhere.com" in result.output
