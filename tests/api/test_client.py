import requests
from unittest.mock import patch, MagicMock

from pa_cli.api.client import BaseClient


def test_base_client_sets_auth_header():
    client = BaseClient(token="test-token", host="www.pythonanywhere.com")
    assert client.session.headers["Authorization"] == "Token test-token"


def test_base_client_builds_url():
    client = BaseClient(token="t", host="www.pythonanywhere.com")
    url = client._build_url("/api/v0/user/{username}/files/", username="testuser")
    assert url == "https://www.pythonanywhere.com/api/v0/user/testuser/files/"


def test_base_client_raises_on_api_error():
    client = BaseClient(token="t", host="www.pythonanywhere.com")

    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_response.json.return_value = {"detail": "Forbidden"}
    mock_response.raise_for_status.side_effect = requests.HTTPError(response=mock_response)

    with patch.object(client.session, "request", return_value=mock_response):
        try:
            client._request("GET", "/api/v0/user/{username}/cpu/", username="testuser")
            assert False, "Should have raised"
        except Exception as e:
            assert "403" in str(e) or "Forbidden" in str(e)
