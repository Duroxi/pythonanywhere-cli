# pythonanywhere-cli

CLI tool for automating PythonAnywhere deployments.

## Installation

```bash
pip install -e .
```

## Quick Start

```bash
# Configure your account
pa init

# Deploy a project
pa deploy ./my-site

# Or step by step:
pa files upload ./index.html /home/youruser/mysite/index.html
pa console create
pa webapp create youruser.pythonanywhere.com
pa webapp config youruser.pythonanywhere.com --source-dir /home/youruser/mysite
pa webapp reload youruser.pythonanywhere.com
```

## Commands

| Command | Description |
|---------|-------------|
| `pa init` | Configure API token and username |
| `pa files upload <local> <remote> [-r]` | Upload file or directory |
| `pa console create` | Create a Bash console |
| `pa console send <id> <cmd>` | Send input to console |
| `pa console output <id>` | Get console output |
| `pa console kill <id>` | Kill a console |
| `pa webapp create <domain>` | Create a web app |
| `pa webapp config <domain> --source-dir <path>` | Configure web app |
| `pa webapp static <domain> --url <url> --path <path>` | Add static file mapping |
| `pa webapp reload <domain>` | Reload web app |
| `pa deploy <dir> [--domain <domain>]` | One-click deploy |
