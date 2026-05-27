from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

from pa_cli.cli.files_cmd import app

runner = CliRunner()


def test_upload_single_file(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello")

    with patch("pa_cli.cli.files_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.files_cmd.FilesClient") as mock_client_cls:
        mock_load.return_value = {"username": "testuser", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_client.upload.return_value = 201
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["upload", str(test_file), "/home/testuser/test.txt"])

    assert result.exit_code == 0
    assert "uploaded" in result.output.lower() or "success" in result.output.lower()


def test_upload_directory_recursive(tmp_path):
    test_dir = tmp_path / "mysite"
    test_dir.mkdir()
    (test_dir / "index.html").write_text("<h1>Hello</h1>")

    with patch("pa_cli.cli.files_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.files_cmd.FilesClient") as mock_client_cls:
        mock_load.return_value = {"username": "testuser", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_client.upload.return_value = 201
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["upload", str(test_dir), "/home/testuser/mysite", "-r"])

    assert result.exit_code == 0
