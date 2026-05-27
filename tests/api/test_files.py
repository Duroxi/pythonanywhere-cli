from unittest.mock import patch, MagicMock

from pa_cli.api.files import FilesClient


def test_upload_file():
    client = FilesClient(token="t", host="www.pythonanywhere.com")

    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.raise_for_status = MagicMock()

    with patch.object(client.session, "post", return_value=mock_response) as mock_post:
        result = client.upload(
            username="testuser",
            remote_path="/home/testuser/index.html",
            content=b"<h1>Hello</h1>",
        )

    mock_post.assert_called_once()
    assert result == 201


def test_upload_directory():
    client = FilesClient(token="t", host="www.pythonanywhere.com")

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status = MagicMock()

    with patch.object(client.session, "post", return_value=mock_response) as mock_post:
        result = client.upload(
            username="testuser",
            remote_path="/home/testuser/mysite/",
            content=b"<h1>Hello</h1>",
        )

    assert result == 200
