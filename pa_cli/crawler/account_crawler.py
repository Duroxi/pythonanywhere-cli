import requests
from bs4 import BeautifulSoup


class AccountCrawler:
    def __init__(self, host: str = "www.pythonanywhere.com"):
        self.base_url = f"https://{host}"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        })

    def register(self, username: str, email: str, password: str) -> bool:
        register_url = f"{self.base_url}/registration/register/beginner/"

        try:
            register_page_resp = self.session.get(register_url)
            register_page_resp.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch registration page: {e}") from e

        soup = BeautifulSoup(register_page_resp.text, "html.parser")
        csrf_input = soup.find("input", {"name": "csrfmiddlewaretoken"})
        if csrf_input is None:
            raise Exception("CSRF token not found on registration page")

        data = {
            "csrfmiddlewaretoken": csrf_input["value"],
            "username": username,
            "email": email,
            "password1": password,
            "password2": password,
            "tos": "on",
            "recaptcha_response_token_v3": "",
        }

        try:
            register_resp = self.session.post(register_url, data=data)
            register_resp.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Registration request failed: {e}") from e

        return "/registration/register/complete/" in register_resp.url
