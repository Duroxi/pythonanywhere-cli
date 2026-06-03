# Getting Started Guide

Welcome to pythonanywhere-cli (`pa`)! This guide will help you get started from scratch and deploy your local Python project to PythonAnywhere.

## Table of Contents

- [What is pythonanywhere-cli](#what-is-pythonanywhere-cli)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Account Configuration](#account-configuration)
- [Deploying Your First Project](#deploying-your-first-project)
- [Quick Command Reference](#quick-command-reference)
- [FAQ](#faq)

---

## What is pythonanywhere-cli

pythonanywhere-cli is a command-line tool for automating the management of resources on PythonAnywhere. Its core value lies in:

- **One-command deployment** - `pa deploy ./my-site` handles the entire workflow: upload, environment setup, web app creation, and reload
- **No browser required** - All operations are performed via the command line, suitable for scripts and AI agents
- **Free-tier friendly** - Designed specifically for PythonAnywhere free-tier users

## System Requirements

| Requirement | Version |
|-------------|---------|
| Python | 3.10 or higher |
| Operating System | Windows / macOS / Linux |
| Network | Must be able to access pythonanywhere.com |

## Installation

### Method 1: Install from Source (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-username/pythonanywhere-cli.git
cd pythonanywhere-cli

# Install in development mode
pip install -e .
```

### Method 2: Install Dependencies Directly

```bash
pip install typer requests beautifulsoup4 websocket-client
```

### Verify Installation

```bash
pa --version
```

Expected output:

```
pa, version 0.1.0
```

---

## Account Configuration

### Step 1: Register a PythonAnywhere Account (if you don't have one)

If you don't have a PythonAnywhere account yet, you can register via the command line:

```bash
pa register
```

Follow the prompts to enter:
- Email address
- Username
- Password

After successful registration, you will receive a confirmation email.

> **Tip**: If you already have an account, skip this step.

### Step 2: Initialize Configuration

```bash
pa init
```

Interactive configuration process:

```
请输入 PythonAnywhere 用户名: yourusername
正在获取 API Token...
配置已保存到 ~/.pa-cli/config.json
```

`pa init` automatically performs the following operations:
1. Saves your username
2. Automatically fetches the API Token from PythonAnywhere
3. Writes the configuration to `~/.pa-cli/config.json`

### Configuration File

The configuration is saved at `~/.pa-cli/config.json`:

```json
{
  "accounts": [
    {
      "username": "yourusername",
      "token": "your-api-token",
      "host": "www.pythonanywhere.com"
    }
  ],
  "default_account": "yourusername"
}
```

---

## Deploying Your First Project

Suppose you have a simple Flask project with the following directory structure:

```
my-site/
├── app.py
└── requirements.txt
```

**app.py:**

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from PythonAnywhere!"

if __name__ == "__main__":
    app.run()
```

**requirements.txt:**

```
flask
```

### One-Command Deployment

```bash
pa deploy ./my-site
```

Deployment output:

```
[1/5] 上传文件到 /home/yourusername/my-site...
  上传 app.py
  上传 requirements.txt
  上传完成

[2/5] 创建虚拟环境...
  python3.10 -m venv /home/yourusername/my-site/.venv
  安装依赖...
  成功

[3/5] 创建 Web 应用...
  域名: yourusername.pythonanywhere.com
  Python 版本: python3.10
  成功

[4/5] 配置 Web 应用...
  源码目录: /home/yourusername/my-site
  虚拟环境: /home/yourusername/my-site/.venv
  成功

[5/5] 重载 Web 应用...
  成功

========================================
部署成功！
访问地址: https://yourusername.pythonanywhere.com
========================================
```

### Verify the Deployment

Open `https://yourusername.pythonanywhere.com` in your browser. You should see:

```
Hello from PythonAnywhere!
```

### Specify a Custom Domain

```bash
pa deploy ./my-site --domain mysite.pythonanywhere.com
```

---

## Quick Command Reference

### Account Management

| Command | Description |
|---------|-------------|
| `pa init` | Initialize/update account configuration |
| `pa register` | Register a new account |
| `pa account login` | Save password (for crawler operations) |
| `pa account extend` | Extend free account expiry |

### Deployment

| Command | Description |
|---------|-------------|
| `pa deploy <directory>` | One-command deploy to default domain |
| `pa deploy <directory> --domain <domain>` | Deploy to a specific domain |

### File Management

| Command | Description |
|---------|-------------|
| `pa files upload <local_path> <remote_path>` | Upload a single file |
| `pa files upload <local_path> <remote_path> -r` | Upload a directory recursively |

### Web App Management

| Command | Description |
|---------|-------------|
| `pa webapp reload <domain>` | Reload web app |
| `pa webapp hits <domain>` | View traffic statistics |
| `pa webapp config <domain> --source-dir <path>` | Set source directory |
| `pa webapp config <domain> --virtualenv <path>` | Set virtualenv path |

### Console Management

| Command | Description |
|---------|-------------|
| `pa console list` | List all consoles |
| `pa console create` | Create a new console |
| `pa console send <id> <command>` | Send a command and get output |
| `pa console kill <id>` | Terminate a console |

---

## FAQ

### Q: `pa init` reports "Failed to fetch API Token"

**Cause**: This may be a network issue or an expired PythonAnywhere session.

**Solution**:
1. Verify you can access pythonanywhere.com
2. Manually obtain a Token: Log in to PythonAnywhere -> Account -> API Token -> Generate new token
3. Manually edit the configuration file `~/.pa-cli/config.json`

### Q: Website shows 500 error after deployment

**Cause**: Usually an application code error or improperly installed dependencies.

**Solution**:
```bash
# View error logs
pa webapp logs yourusername.pythonanywhere.com

# Check if virtualenv is correctly configured
pa webapp config yourusername.pythonanywhere.com --virtualenv /home/yourusername/my-site/.venv
```

### Q: What are the limitations of a free account?

- Limited CPU time (a few seconds per day)
- No SSH access (this is exactly why this tool exists)
- Can only create one web app
- Auto-expires (needs renewal every 3 months)

Renewal command:
```bash
pa account extend
```

### Q: How do I update a deployed project?

Simply run the deploy command again:

```bash
pa deploy ./my-site
```

This will re-upload the files and reload the application.

### Q: Which Python versions are supported?

PythonAnywhere supports Python 3.10, 3.11, and 3.12. The default is 3.10, which can be specified when creating a web app.

---

## Next Steps

- Read the [README.md](../README.md) for the complete command list
- Check the [PRD document](../docs/prd-mvp.md) for technical details
- Submit an Issue or PR to participate in project development
