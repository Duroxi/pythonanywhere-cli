from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

from pa_cli.cli.webapps_cmd import app

runner = CliRunner()


def test_webapp_create():
    with patch("pa_cli.cli.webapps_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.webapps_cmd.WebappsClient") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_cls.return_value = mock_client

        result = runner.invoke(app, ["create", "u.pythonanywhere.com", "--python", "python310"])

    assert result.exit_code == 0
    assert "created" in result.output.lower()


def test_webapp_config():
    with patch("pa_cli.cli.webapps_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.webapps_cmd.WebappsClient") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_cls.return_value = mock_client

        result = runner.invoke(app, [
            "config", "u.pythonanywhere.com",
            "--source-dir", "/home/u/mysite",
            "--virtualenv", "/home/u/.virtualenvs/mysite",
        ])

    assert result.exit_code == 0


def test_webapp_static():
    with patch("pa_cli.cli.webapps_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.webapps_cmd.WebappsClient") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_cls.return_value = mock_client

        result = runner.invoke(app, [
            "static", "u.pythonanywhere.com",
            "--url", "/static/",
            "--path", "/home/u/mysite/static",
        ])

    assert result.exit_code == 0


def test_webapp_reload():
    with patch("pa_cli.cli.webapps_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.webapps_cmd.WebappsClient") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_cls.return_value = mock_client

        result = runner.invoke(app, ["reload", "u.pythonanywhere.com"])

    assert result.exit_code == 0
