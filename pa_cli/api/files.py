from pa_cli.api.client import BaseClient


class FilesClient(BaseClient):
    def upload(self, username: str, remote_path: str, content: bytes) -> int:
        url = self._build_url(
            "/api/v0/user/{username}/files/path{remote_path}",
            username=username,
            remote_path=remote_path,
        )
        response = self.session.post(url, files={"content": content})
        try:
            response.raise_for_status()
        except Exception as e:
            raise Exception(f"Upload failed: {response.status_code} {response.text}") from e
        return response.status_code
