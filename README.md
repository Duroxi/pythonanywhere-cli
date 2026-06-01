# pythonanywhere-cli

CLI tool for automating PythonAnywhere deployments.

## Installation

```bash
pip install -e .
```

## Quick Start

```bash
# 1. Configure your account
pa init

# 2. Store password for crawler operations (optional)
pa account login

# 3. Deploy a project
pa deploy ./my-site
```

## Commands

### Account Management

| Command | Description |
|---------|-------------|
| `pa init` | Configure API token and username (interactive) |
| `pa account login` | Store password for crawler operations (interactive, hidden input) |

### File Management

| Command | Description |
|---------|-------------|
| `pa files upload <local> <remote>` | Upload a single file |
| `pa files upload <local> <remote> -r` | Upload directory recursively |

### Console Management

| Command | Description |
|---------|-------------|
| `pa console create` | Create a Bash console |
| `pa console send <id> <cmd>` | Send input to console |
| `pa console output <id>` | Get console output |
| `pa console kill <id>` | Kill a console |

### Web App Management

| Command | Description |
|---------|-------------|
| `pa webapp create <domain>` | Create a web app |
| `pa webapp config <domain> --source-dir <path>` | Configure source directory |
| `pa webapp config <domain> --virtualenv <path>` | Configure virtualenv path |
| `pa webapp static <domain> --url <url> --path <path>` | Add static file mapping |
| `pa webapp reload <domain>` | Reload web app |

### Deployment

| Command | Description |
|---------|-------------|
| `pa deploy <dir>` | One-click deploy to default domain |
| `pa deploy <dir> --domain <domain>` | One-click deploy to custom domain |

## Crawler Module

The crawler module provides browser-simulation capabilities for operations not available via REST API.

### AccountCrawler

```python
from pa_cli.crawler.account_crawler import AccountCrawler

# Initialize (reads username from config)
crawler = AccountCrawler()

# Login (reads password from config)
crawler.login()

# Get API token
token = crawler.get_token()

# Extend account expiry (free tier)
crawler.extend_expiry()

# Reload web app
crawler.reload_webapp("youruser.pythonanywhere.com")

# Get web app hit statistics
hits = crawler.get_hits("youruser.pythonanywhere.com")
# Returns: {"hits_current_hour": 0, "hits_previous_hour": 2, ...}
```

### ConsoleCrawler

```python
from pa_cli.crawler.console_crawler import ConsoleCrawler

# Initialize
crawler = ConsoleCrawler()

# Login
crawler.login("username", "password")

# Get or create console (max 2 for free tier)
console_id = crawler.get_or_create("username")

# Activate console (starts the process via WebSocket)
crawler.activate("username", console_id)

# Now use REST API for commands
from pa_cli.api.consoles import ConsolesClient
client = ConsolesClient(token="your-api-token")
client.send_input("username", console_id, "echo hello\n")
output = client.get_output("username", console_id)
```

## Configuration

Configuration is stored at `~/.pa-cli/config.json`:

```json
{
  "accounts": [
    {
      "username": "yourusername",
      "token": "your-api-token",
      "host": "www.pythonanywhere.com",
      "password": "your-password"
    }
  ],
  "default_account": "yourusername"
}
```

## Architecture

```
pa_cli/
├── api/           # REST API clients (Token auth)
├── cli/           # CLI commands (Typer)
├── crawler/       # Browser simulation (Session auth)
├── workflows/     # Deployment orchestration
└── config.py      # Configuration management
```

## Dependencies

- `typer` - CLI framework
- `requests` - HTTP client
- `beautifulsoup4` - HTML parsing
- `websocket-client` - WebSocket connections

## Testing

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_account_crawler.py
```

## License

MIT