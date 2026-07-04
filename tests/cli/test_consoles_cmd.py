from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

from pa_cli.cli.consoles_cmd import app
from pa_cli.exceptions import APIError, AuthError, NetworkError

runner = CliRunner()


# --- list ---


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


# --- activate ---


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
        mock_crawler.login.side_effect = AuthError("Login failed")
        mock_cls.return_value = mock_crawler

        result = runner.invoke(app, ["activate", "42"])

    assert result.exit_code == 1
    assert "Login failed" in result.output


# --- create ---


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


# --- kill ---


def test_console_kill():
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_cls.return_value = mock_client

        result = runner.invoke(app, ["kill", "42"])

    assert result.exit_code == 0


# --- get-or-create ---


def test_console_get_or_create_no_password():
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}

        result = runner.invoke(app, ["get-or-create"])

    assert result.exit_code == 1
    assert "Password not found" in result.output


def test_console_get_or_create_success():
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.crawler.console_crawler.ConsoleCrawler") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h", "password": "p"}
        mock_crawler = MagicMock()
        mock_crawler.get_or_create.return_value = 42
        mock_cls.return_value = mock_crawler

        result = runner.invoke(app, ["get-or-create"])

    assert result.exit_code == 0
    assert "Console ready: 42" in result.output
    mock_crawler.login.assert_called_once_with("u", "p")
    mock_crawler.get_or_create.assert_called_once_with("u", executable="bash")


def test_console_get_or_create_custom_executable():
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.crawler.console_crawler.ConsoleCrawler") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h", "password": "p"}
        mock_crawler = MagicMock()
        mock_crawler.get_or_create.return_value = 7
        mock_cls.return_value = mock_crawler

        result = runner.invoke(app, ["get-or-create", "-e", "python3.10"])

    assert result.exit_code == 0
    assert "Console ready: 7" in result.output
    mock_crawler.get_or_create.assert_called_once_with("u", executable="python3.10")


def test_console_get_or_create_error():
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.crawler.console_crawler.ConsoleCrawler") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h", "password": "p"}
        mock_crawler = MagicMock()
        mock_crawler.login.side_effect = AuthError("Login failed")
        mock_cls.return_value = mock_crawler

        result = runner.invoke(app, ["get-or-create"])

    assert result.exit_code == 1
    assert "Login failed" in result.output


# --- send with explicit console_id ---


def test_console_send_no_wait():
    """send with --no-wait sends input and returns immediately."""
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_cls.return_value = mock_client

        result = runner.invoke(app, ["send", "ls", "42", "--no-wait"])

    assert result.exit_code == 0
    assert "Sent to console 42: ls" in result.output
    mock_client.send_input.assert_called_once_with("u", 42, "ls\n")


def test_console_send_wait_default():
    """console send waits for output by default."""
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls, \
         patch("pa_cli.cli.consoles_cmd.time.sleep"), \
         patch("pa_cli.cli.consoles_cmd.uuid.uuid4") as mock_uuid, \
         patch("pa_cli.cli.consoles_cmd.time.time", return_value=1234567890):
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_cls.return_value = mock_client
        mock_uuid.return_value = MagicMock(hex="abc123456789")

        marker = "__PA_CLI_DONE_1234567890_abc123456789__"
        mock_client.get_output.side_effect = [
            {"output": ""},  # baseline
            {"output": f"$ echo hello\nhello\n{marker}\n$ "},  # result
        ]

        result = runner.invoke(app, ["send", "echo hello", "42"])

    assert result.exit_code == 0
    assert "hello" in result.output


def test_console_send_timeout():
    """send exits with error when timeout reached without marker."""
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls, \
         patch("pa_cli.cli.consoles_cmd.time.sleep"):
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_cls.return_value = mock_client
        mock_client.get_output.return_value = {"output": "$ still running...\n"}

        result = runner.invoke(app, ["send", "sleep 10", "42", "--timeout", "2"])

    assert result.exit_code == 1
    assert "Timeout" in result.output


# --- send auto-detect: use existing console ---


def test_console_send_auto_detect_existing():
    """send without console_id picks first existing console."""
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_cls.return_value = mock_client
        mock_client.list.return_value = [{"id": 7, "name": "bash"}]

        result = runner.invoke(app, ["send", "ls", "--no-wait"])

    assert result.exit_code == 0
    assert "Sent to console 7: ls" in result.output
    mock_client.send_input.assert_called_once_with("u", 7, "ls\n")


# --- send auto-create: no existing console ---


def test_console_send_auto_create():
    """send without console_id creates via crawler when no console exists."""
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls, \
         patch("pa_cli.crawler.console_crawler.ConsoleCrawler") as mock_crawler_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h", "password": "p"}
        mock_client = MagicMock()
        mock_cls.return_value = mock_client
        mock_client.list.return_value = []  # no existing consoles

        mock_crawler = MagicMock()
        mock_crawler.get_or_create.return_value = 99
        mock_crawler_cls.return_value = mock_crawler

        result = runner.invoke(app, ["send", "ls", "--no-wait"])

    assert result.exit_code == 0
    assert "Sent to console 99: ls" in result.output
    mock_crawler.login.assert_called_once_with("u", "p")
    mock_crawler.get_or_create.assert_called_once_with("u", executable="bash")


def test_console_send_auto_create_no_password():
    """send auto-create fails when password is missing."""
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_cls.return_value = mock_client
        mock_client.list.return_value = []

        result = runner.invoke(app, ["send", "ls", "--no-wait"])

    assert result.exit_code == 1
    assert "Password not found" in result.output


# --- send auto-activate: 412 from send_input ---


def test_console_send_auto_activate_on_412():
    """send auto-activates console when send_input returns 412."""
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls, \
         patch("pa_cli.crawler.console_crawler.ConsoleCrawler") as mock_crawler_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h", "password": "p"}
        mock_client = MagicMock()
        mock_cls.return_value = mock_client

        # send_input fails first (412), succeeds after activate
        mock_client.send_input.side_effect = [
            APIError("API error 412: "),
            None,  # success after activate
        ]

        mock_crawler = MagicMock()
        mock_crawler_cls.return_value = mock_crawler

        result = runner.invoke(app, ["send", "ls", "42", "--no-wait"])

    assert result.exit_code == 0
    assert "Sent to console 42: ls" in result.output
    mock_crawler.login.assert_called_once_with("u", "p")
    mock_crawler.activate.assert_called_once_with("u", 42)
    assert mock_client.send_input.call_count == 2


def test_console_send_auto_activate_no_password():
    """send auto-activate fails when password is missing."""
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_cls.return_value = mock_client
        mock_client.send_input.side_effect = APIError("API error 412: ")

        result = runner.invoke(app, ["send", "ls", "42", "--no-wait"])

    assert result.exit_code == 1
    assert "Password not found" in result.output


# --- send auto-activate: 412 from get_output (wait mode) ---


def test_console_send_auto_activate_on_get_output_412():
    """send auto-activates when get_output returns 412 (wait mode)."""
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls, \
         patch("pa_cli.crawler.console_crawler.ConsoleCrawler") as mock_crawler_cls, \
         patch("pa_cli.cli.consoles_cmd.time.sleep"), \
         patch("pa_cli.cli.consoles_cmd.uuid.uuid4") as mock_uuid, \
         patch("pa_cli.cli.consoles_cmd.time.time", return_value=1234567890):
        mock_load.return_value = {"username": "u", "token": "t", "host": "h", "password": "p"}
        mock_client = MagicMock()
        mock_cls.return_value = mock_client
        mock_uuid.return_value = MagicMock(hex="abc123456789")

        marker = "__PA_CLI_DONE_1234567890_abc123456789__"

        # get_output fails first (412), then succeeds
        mock_client.get_output.side_effect = [
            APIError("API error 412: "),  # baseline fails
            {"output": ""},  # baseline after activate
            {"output": f"$ ls\nfile1\n{marker}\n$ "},  # result
        ]

        mock_crawler = MagicMock()
        mock_crawler_cls.return_value = mock_crawler

        result = runner.invoke(app, ["send", "ls", "42"])

    assert result.exit_code == 0
    assert "file1" in result.output
    mock_crawler.activate.assert_called_once_with("u", 42)


# --- send full auto: no console_id, create + activate ---


def test_console_send_full_auto():
    """send with no console_id, no existing console: create + activate + send."""
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls, \
         patch("pa_cli.crawler.console_crawler.ConsoleCrawler") as mock_crawler_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h", "password": "p"}
        mock_client = MagicMock()
        mock_cls.return_value = mock_client

        # No existing consoles
        mock_client.list.return_value = []
        # send_input fails (412), then succeeds
        mock_client.send_input.side_effect = [
            APIError("API error 412: "),
            None,
        ]

        mock_crawler = MagicMock()
        mock_crawler.get_or_create.return_value = 55
        mock_crawler_cls.return_value = mock_crawler

        result = runner.invoke(app, ["send", "ls", "--no-wait"])

    assert result.exit_code == 0
    assert "Sent to console 55: ls" in result.output
    mock_crawler.get_or_create.assert_called_once()
    mock_crawler.activate.assert_called_once_with("u", 55)


# --- send with explicit console_id skips auto-detect ---


def test_console_send_explicit_id_skips_list():
    """send with explicit console_id does not call list."""
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_cls.return_value = mock_client

        result = runner.invoke(app, ["send", "ls", "42", "--no-wait"])

    assert result.exit_code == 0
    mock_client.list.assert_not_called()
    mock_client.send_input.assert_called_once_with("u", 42, "ls\n")


# --- error handling ---


def test_console_list_network_error():
    """list exits with error on network failure."""
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_client.list.side_effect = NetworkError("Connection failed")
        mock_cls.return_value = mock_client

        result = runner.invoke(app, ["list"])

    assert result.exit_code == 1
    assert "Network error" in result.output


def test_console_create_network_error():
    """create exits with error on network failure."""
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_client.create.side_effect = NetworkError("Connection failed")
        mock_cls.return_value = mock_client

        result = runner.invoke(app, ["create"])

    assert result.exit_code == 1
    assert "Network error" in result.output


def test_console_create_api_error():
    """create exits with error on API failure."""
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_client.create.side_effect = APIError("API error 500")
        mock_cls.return_value = mock_client

        result = runner.invoke(app, ["create"])

    assert result.exit_code == 1
    assert "API error" in result.output


def test_console_kill_network_error():
    """kill exits with error on network failure."""
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_client.kill.side_effect = NetworkError("Connection failed")
        mock_cls.return_value = mock_client

        result = runner.invoke(app, ["kill", "42"])

    assert result.exit_code == 1
    assert "Network error" in result.output


def test_console_send_ensure_console_network_error():
    """send exits with error when _ensure_console fails with NetworkError."""
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_client.list.side_effect = NetworkError("Connection failed")
        mock_cls.return_value = mock_client

        result = runner.invoke(app, ["send", "ls", "--no-wait"])

    assert result.exit_code == 1
    assert "Network error" in result.output


def test_console_send_polling_survives_transient_error():
    """send continues polling when get_output raises transient error."""
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls, \
         patch("pa_cli.cli.consoles_cmd.time.sleep"), \
         patch("pa_cli.cli.consoles_cmd.uuid.uuid4") as mock_uuid, \
         patch("pa_cli.cli.consoles_cmd.time.time", return_value=1234567890):
        mock_load.return_value = {"username": "u", "token": "t", "host": "h"}
        mock_client = MagicMock()
        mock_cls.return_value = mock_client
        mock_uuid.return_value = MagicMock(hex="abc123456789")

        marker = "__PA_CLI_DONE_1234567890_abc123456789__"
        mock_client.get_output.side_effect = [
            {"output": ""},  # baseline
            NetworkError("Connection reset"),  # transient error
            {"output": f"$ ls\nfile1\n{marker}\n$ "},  # success
        ]

        result = runner.invoke(app, ["send", "ls", "42"])

    assert result.exit_code == 0
    assert "file1" in result.output


def test_console_send_no_wait_activate_retry_api_error():
    """send --no-wait exits with error when retry send_input also fails."""
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls, \
         patch("pa_cli.crawler.console_crawler.ConsoleCrawler") as mock_crawler_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h", "password": "p"}
        mock_client = MagicMock()
        mock_cls.return_value = mock_client
        # Both attempts fail
        mock_client.send_input.side_effect = [
            APIError("API error 412: "),
            APIError("API error 500: "),
        ]
        mock_crawler = MagicMock()
        mock_crawler_cls.return_value = mock_crawler

        result = runner.invoke(app, ["send", "ls", "42", "--no-wait"])

    assert result.exit_code == 1
    assert "API error" in result.output


def test_console_send_wait_activate_retry_api_error():
    """send wait mode exits when retry get_output also fails."""
    with patch("pa_cli.cli.consoles_cmd.Config.load") as mock_load, \
         patch("pa_cli.cli.consoles_cmd.ConsolesClient") as mock_cls, \
         patch("pa_cli.crawler.console_crawler.ConsoleCrawler") as mock_crawler_cls:
        mock_load.return_value = {"username": "u", "token": "t", "host": "h", "password": "p"}
        mock_client = MagicMock()
        mock_cls.return_value = mock_client
        # Both get_output attempts fail
        mock_client.get_output.side_effect = [
            APIError("API error 412: "),
            APIError("API error 500: "),
        ]
        mock_crawler = MagicMock()
        mock_crawler_cls.return_value = mock_crawler

        result = runner.invoke(app, ["send", "ls", "42"])

    assert result.exit_code == 1
    assert "API error" in result.output
