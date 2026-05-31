from pa_cli.api.client import BaseClient


class ConsolesClient(BaseClient):
    def list(self, username: str) -> list:
        response = self._request(
            "GET",
            "/api/v0/user/{username}/consoles/",
            username=username,
        )
        return response.json()

    def create(self, username: str, executable: str = "bash") -> dict:
        response = self._request(
            "POST",
            "/api/v0/user/{username}/consoles/",
            username=username,
            json={"executable": executable},
        )
        return response.json()

    def send_input(self, username: str, console_id: int, input_text: str) -> None:
        self._request(
            "POST",
            "/api/v0/user/{username}/consoles/{id}/send_input/",
            username=username,
            id=console_id,
            data={"input": input_text},
        )

    def get_output(self, username: str, console_id: int) -> dict:
        response = self._request(
            "GET",
            "/api/v0/user/{username}/consoles/{id}/get_latest_output/",
            username=username,
            id=console_id,
        )
        return response.json()

    def kill(self, username: str, console_id: int) -> None:
        self._request(
            "DELETE",
            "/api/v0/user/{username}/consoles/{id}/",
            username=username,
            id=console_id,
        )
