# pythonanywhere-cli Architecture Documentation

This document describes the overall architecture design, module responsibilities, and extension patterns of the pythonanywhere-cli (`pa`) project.

---

## 1. Project Structure

```
pythonanywhere-cli/
├── pa_cli/                    # Main source directory
│   ├── __init__.py
│   ├── config.py              # Configuration management (read/write ~/.pa-cli/config.json)
│   │
│   ├── api/                   # REST API client module (Token authentication)
│   │   ├── __init__.py
│   │   ├── client.py          # BaseClient base class, wraps HTTP requests
│   │   ├── consoles.py        # ConsolesClient - Console API
│   │   ├── files.py           # FilesClient - File upload API
│   │   └── webapps.py         # WebappsClient - Web app API
│   │
│   ├── cli/                   # CLI command layer (Typer framework)
│   │   ├── __init__.py
│   │   ├── main.py            # Entry point: registers all subcommands
│   │   ├── init_cmd.py        # pa init - Initialize configuration
│   │   ├── files_cmd.py       # pa files - File operations
│   │   ├── consoles_cmd.py    # pa console - Console operations
│   │   ├── webapps_cmd.py     # pa webapp - Web app operations
│   │   ├── deploy_cmd.py      # pa deploy - Deploy project
│   │   ├── account_cmd.py     # pa account - Account management
│   │   └── register_cmd.py    # pa register - Register new account
│   │
│   ├── crawler/               # Browser simulation module (Session authentication)
│   │   ├── __init__.py
│   │   ├── account_crawler.py # AccountCrawler - Account operation crawler
│   │   └── console_crawler.py # ConsoleCrawler - Console operation crawler
│   │
│   └── workflows/             # Workflow orchestration
│       ├── __init__.py
│       └── deploy.py          # Deploy workflow (upload -> environment -> config -> reload)
│
├── tests/                     # Test directory
├── docs/                      # Supplementary documentation
├── documentation/             # Detailed documentation (this document's location)
├── pyproject.toml             # Project metadata and dependencies
└── README.md                  # Project overview
```

### Module Responsibilities

| Module | Responsibility | Dependencies |
|--------|---------------|--------------|
| `config.py` | Manage configuration file read/write, support multiple accounts | Standard library |
| `api/` | Wrap PythonAnywhere REST API, provide type-safe clients | requests |
| `cli/` | Parse command-line arguments, call api or crawler modules | typer, api, crawler |
| `crawler/` | Simulate browser operations, handle functionality without APIs | requests, bs4, websocket |
| `workflows/` | Orchestrate multi-step operations (e.g., full deployment flow) | api |

---

## 2. Authentication Model

PythonAnywhere provides two access methods, both supported by this project.

### 2.1 Token Authentication (API Module)

```
┌─────────┐    Token: xxxxx    ┌──────────────────┐
│  pa CLI  │ ─────────────────→│  PA REST API     │
│          │ ←─────────────────│  (api/v0/...)    │
└─────────┘    JSON Response   └──────────────────┘
```

**Characteristics:**
- Uses API Token for authentication, passed via `Authorization: Token xxxxx` header
- Applies to standard REST API endpoints
- Rate limit: 40 requests/minute (standard endpoints), 120 requests/minute (`send_input` endpoint)
- Token is configured during `pa init` and stored in `~/.pa-cli/config.json`

**Implementation location:** `pa_cli/api/client.py` `BaseClient`

```python
# Authentication method
self.session.headers.update({"Authorization": f"Token {token}"})
```

### 2.2 Session Authentication (Crawler Module)

```
┌─────────┐   POST /login/    ┌──────────────────┐
│  pa CLI  │ ────────────────→│  PA Web UI       │
│          │ ←────────────────│  (HTML pages)    │
│          │   Session Cookie  │                  │
│          │ ────────────────→│  Perform ops...  │
└─────────┘                   └──────────────────┘
```

**Characteristics:**
- Uses username + password login to obtain Session Cookie
- Simulates browser behavior (parses HTML, handles CSRF Tokens)
- No official rate limit (but request frequency should be self-controlled)
- Applies to functionality without REST APIs (e.g., account registration, extending expiry)

**Implementation location:** `pa_cli/crawler/` directory

```python
# Login flow
data = {
    "csrfmiddlewaretoken": csrf_input["value"],
    "auth-username": username,
    "auth-password": password,
    "login_view-current_step": "auth",
}
login_resp = self.session.post(login_url, data=data)
```

### 2.3 Authentication Method Comparison

| Feature | Token Authentication | Session Authentication |
|---------|---------------------|----------------------|
| Credentials | API Token | Username + Password |
| Auth Header | `Authorization: Token xxx` | Session Cookie |
| Rate Limit | 40 req/min | No official limit |
| Use Case | Standard API operations | Browser-exclusive features |
| Implementation Complexity | Low | High (requires CSRF handling) |
| Stability | High (official API) | Medium (depends on page structure) |

---

## 3. Design Decision: Why the Crawler Module Exists

### 3.1 Background

PythonAnywhere's REST API does not cover all functionality. The following operations can only be performed through the web interface:

1. **Register a new account** - No API endpoint
2. **Extend account expiry** - No API endpoint
3. **Obtain API Token** - Requires login and extraction from the page
4. **WebSocket console activation** - Requires parsing connection parameters from the page

### 3.2 Solution

The Crawler module supplements the API's limitations by simulating browser behavior:

```
User Request
    │
    ├─ Standard operations (upload files, create consoles, etc.)
    │   └─→ Use API module (Token authentication)
    │
    └─ Browser-exclusive operations (register, extend expiry, etc.)
        └─→ Use Crawler module (Session authentication)
```

### 3.3 Design Principles

1. **Minimize usage** - Prefer API; use Crawler only when no API is available
2. **Separation of concerns** - Crawler code is independent of API code, with no mutual dependencies
3. **Defensive programming** - Handle CSRF Tokens, page structure changes, and other potential issues
4. **Replaceability** - If PythonAnywhere provides corresponding APIs in the future, migration can be seamless

---

## 4. API vs Crawler: Use Cases

### 4.1 Scenarios Using the API Module

| Operation | Client Class | Method |
|-----------|-------------|--------|
| Upload files | `FilesClient` | `upload()` |
| List consoles | `ConsolesClient` | `list()` |
| Create console | `ConsolesClient` | `create()` |
| Send command | `ConsolesClient` | `send_input()` |
| Get output | `ConsolesClient` | `get_output()` |
| Create web app | `WebappsClient` | `create()` |
| Update config | `WebappsClient` | `update()` |
| Reload app | `WebappsClient` | `reload()` |

### 4.2 Scenarios Using the Crawler Module

| Operation | Crawler Class | Method |
|-----------|--------------|--------|
| Register new account | `AccountCrawler` | `register()` |
| Login to obtain session | `AccountCrawler` | `login()` |
| Extract API Token | `AccountCrawler` | `get_token()` |
| Extend account expiry | `AccountCrawler` | `extend_expiry()` |
| Reload web app (alternative) | `AccountCrawler` | `reload_webapp()` |
| Get traffic statistics | `AccountCrawler` | `get_hits()` |
| Activate console (WebSocket) | `ConsoleCrawler` | `activate()` |

### 4.3 Decision Flowchart

```
Need to perform an operation
    │
    ▼
Does this operation have a REST API?
    │
    ├─ Yes → Use API module (api/)
    │        Benefits: stable, fast, rate-limit protection
    │
    └─ No → Use Crawler module (crawler/)
            Note: depends on page structure, may need maintenance
```

---

## 5. Configuration Management

### 5.1 Configuration File Location

```
~/.pa-cli/config.json
```

### 5.2 Configuration File Format

```json
{
  "default_account": "myusername",
  "accounts": [
    {
      "username": "myusername",
      "token": "abc123def456...",
      "host": "www.pythonanywhere.com",
      "password": "optional_for_crawler"
    },
    {
      "username": "work_account",
      "token": "xyz789...",
      "host": "www.pythonanywhere.com"
    }
  ]
}
```

### 5.3 Field Descriptions

| Field | Required | Description |
|-------|----------|-------------|
| `default_account` | Yes | Username of the default account |
| `accounts` | Yes | List of accounts |
| `accounts[].username` | Yes | PythonAnywhere username |
| `accounts[].token` | Yes | API Token (obtained via `pa init`) |
| `accounts[].host` | No | API host, defaults to `www.pythonanywhere.com` |
| `accounts[].password` | No | Password (only needed for Crawler features) |

### 5.4 Configuration Operations

```bash
# Initialize configuration (interactive)
pa init

# Specify account for operations
pa --account work_account files ls /home/work_account/
```

### 5.5 Implementation Details

Configuration management is implemented by the `Config` class in `pa_cli/config.py`:

- `Config.save()` - Save or update configuration, supports partial updates
- `Config.load()` - Load configuration, supports lookup by username

---

## 6. Extension Points

### 6.1 Adding a New API Client

When PythonAnywhere releases new API endpoints:

**Step 1:** Create a new client file in `pa_cli/api/`

```python
# pa_cli/api/databases.py
from pa_cli.api.client import BaseClient


class DatabasesClient(BaseClient):
    def list(self, username: str) -> list:
        response = self._request(
            "GET",
            "/api/v0/user/{username}/databases/",
            username=username,
        )
        return response.json()

    def create(self, username: str, name: str) -> dict:
        response = self._request(
            "POST",
            "/api/v0/user/{username}/databases/",
            username=username,
            json={"name": name},
        )
        return response.json()
```

**Step 2:** Create the corresponding command in `pa_cli/cli/`

```python
# pa_cli/cli/databases_cmd.py
import typer
from pa_cli.config import Config
from pa_cli.api.databases import DatabasesClient

app = typer.Typer()


@app.command("ls")
def list_databases():
    config = Config.load()
    client = DatabasesClient(token=config["token"], host=config["host"])
    databases = client.list(config["username"])
    for db in databases:
        print(db["name"])
```

**Step 3:** Register the new command in `pa_cli/cli/main.py`

```python
from pa_cli.cli.databases_cmd import app as databases_app
app.add_typer(databases_app, name="database", help="Manage databases")
```

### 6.2 Adding a New Crawler Feature

When operating on web pages without APIs:

```python
# pa_cli/crawler/new_crawler.py
import requests
from bs4 import BeautifulSoup


class NewCrawler:
    def __init__(self, host: str = "www.pythonanywhere.com"):
        self.base_url = f"https://{host}"
        self.session = requests.Session()

    def login(self, username: str, password: str) -> bool:
        # Standard login flow
        login_url = f"{self.base_url}/login/"
        resp = self.session.get(login_url)
        soup = BeautifulSoup(resp.text, "html.parser")
        csrf = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

        data = {
            "csrfmiddlewaretoken": csrf,
            "auth-username": username,
            "auth-password": password,
            "login_view-current_step": "auth",
        }
        login_resp = self.session.post(login_url, data=data)
        return "/login/" not in login_resp.url

    def new_operation(self):
        # Implement new operation
        pass
```

### 6.3 Adding a New Workflow

When orchestrating multi-step operations:

```python
# pa_cli/workflows/setup.py
from pa_cli.api.files import FilesClient
from pa_cli.api.consoles import ConsolesClient


def setup_project(username, token, host, project_name):
    """Complete project initialization workflow"""
    files = FilesClient(token=token, host=host)
    consoles = ConsolesClient(token=token, host=host)

    # Step 1: Create directory structure
    # Step 2: Upload template files
    # Step 3: Install dependencies
    # Step 4: Configure environment
    pass
```

### 6.4 Extension Checklist

When adding new functionality, confirm the following:

- [ ] Check if a REST API is available (prefer API)
- [ ] If no API, assess the stability of the Crawler implementation
- [ ] Follow existing naming conventions (English, semantically clear)
- [ ] Client class inherits from `BaseClient` (API module)
- [ ] Commands use the Typer framework (CLI module)
- [ ] Register new commands in `main.py`
- [ ] Add corresponding test cases

---

## 7. Data Flow Examples

### 7.1 Deployment Flow

```
User executes: pa deploy ./myproject myusername.pythonanywhere.com

    ┌─────────────────────────────────────────────────────────────┐
    │                      deploy workflow                        │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  1. FilesClient.upload() x N                                │
    │     Upload local files to remote directory                  │
    │                          ↓                                  │
    │  2. ConsolesClient.create()                                  │
    │     Create temporary console                                │
    │                          ↓                                  │
    │  3. ConsolesClient.send_input() x N                         │
    │     Execute mkvirtualenv, pip install, etc.                 │
    │                          ↓                                  │
    │  4. WebappsClient.create()                                   │
    │     Create/update web app configuration                     │
    │                          ↓                                  │
    │  5. WebappsClient.reload()                                   │
    │     Reload web app                                          │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
```

### 7.2 Account Registration Flow

```
User executes: pa register --username newuser --email user@example.com

    ┌─────────────────────────────────────────────────────────────┐
    │                   AccountCrawler.register()                 │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  1. GET /registration/register/beginner/                     │
    │     Fetch registration page and CSRF Token                  │
    │                          ↓                                  │
    │  2. POST /registration/register/beginner/                    │
    │     Submit registration form (username, email, password)    │
    │                          ↓                                  │
    │  3. Check if redirected to /registration/register/complete/  │
    │     Confirm registration success                            │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
```

---

## 8. Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| CLI Framework | Typer | Command-line argument parsing, help generation |
| HTTP Client | requests | API calls and page requests |
| HTML Parsing | BeautifulSoup4 | Parse web pages, extract CSRF Tokens |
| WebSocket | websocket-client | Console WebSocket connection |
| Config Storage | JSON | Local configuration file |
| Minimum Python | 3.8+ | `str | None` type syntax requires 3.10+ |

---

## 9. Important Notes

### 9.1 Rate Limits

- API module: 40 requests/minute (standard endpoints)
- API module: 120 requests/minute (`send_input` endpoint)
- Crawler module: No official limit, but frequency should be controlled

### 9.2 Crawler Stability

The Crawler depends on web page structure. If PythonAnywhere updates their pages, selectors may need adjustment. Key points:

- CSRF Token extraction method
- Form field names
- Page redirect URL patterns

### 9.3 Security Considerations

- API Tokens and passwords are stored in a local JSON file
- It is recommended to set appropriate file permissions: `chmod 600 ~/.pa-cli/config.json`
- Do not commit the configuration file to version control
