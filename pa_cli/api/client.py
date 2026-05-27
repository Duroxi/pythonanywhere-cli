import requests


class BaseClient:
    def __init__(self, token: str, host: str = "www.pythonanywhere.com"):
        self.host = host
        self.base_url = f"https://{host}"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Token {token}"})

    def _build_url(self, path: str, **kwargs) -> str:
        return f"{self.base_url}{path.format(**kwargs)}"

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = self._build_url(path, **kwargs)

        # Extract path params from kwargs (used in URL formatting)
        path_params = {k for k in kwargs if "{" + k + "}" in path}
        request_kwargs = {k: v for k, v in kwargs.items() if k not in path_params}

        response = self.session.request(method, url, **request_kwargs)

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            detail = ""
            try:
                detail = response.json().get("detail", "")
            except Exception:
                detail = response.text
            raise Exception(f"API error {response.status_code}: {detail}") from e

        return response
