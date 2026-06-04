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

    def list(self, username: str, remote_path: str) -> dict:
        """List files and directories at remote path. Returns dict of {name: {type, url}}."""
        url = self._build_url(
            "/api/v0/user/{username}/files/path{remote_path}",
            username=username,
            remote_path=remote_path,
        )
        response = self.session.get(url)
        try:
            response.raise_for_status()
        except Exception as e:
            raise Exception(f"List failed: {response.status_code} {response.text}") from e
        return response.json()

    def download(self, username: str, remote_path: str) -> bytes:
        """Download a file from remote path. Returns file content as bytes."""
        url = self._build_url(
            "/api/v0/user/{username}/files/path{remote_path}",
            username=username,
            remote_path=remote_path,
        )
        response = self.session.get(url)
        try:
            response.raise_for_status()
        except Exception as e:
            raise Exception(f"Download failed: {response.status_code} {response.text}") from e
        return response.content

    def delete(self, username: str, remote_path: str) -> None:
        """Delete a file or directory at remote path."""
        url = self._build_url(
            "/api/v0/user/{username}/files/path{remote_path}",
            username=username,
            remote_path=remote_path,
        )
        response = self.session.delete(url)
        try:
            response.raise_for_status()
        except Exception as e:
            raise Exception(f"Delete failed: {response.status_code} {response.text}") from e
