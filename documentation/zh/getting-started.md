# 快速开始指南

欢迎使用 pythonanywhere-cli (`pa`)！本指南将帮助你从零开始，将本地 Python 项目部署到 PythonAnywhere。

## 目录

- [什么是 pythonanywhere-cli](#什么是-pythonanywhere-cli)
- [环境要求](#环境要求)
- [安装](#安装)
- [账号配置](#账号配置)
- [第一个项目部署](#第一个项目部署)
- [常用命令速查](#常用命令速查)
- [常见问题](#常见问题)

---

## 什么是 pythonanywhere-cli

pythonanywhere-cli 是一个命令行工具，用于自动化管理 PythonAnywhere 上的资源。它的核心价值是：

- **一行命令部署** - `pa deploy ./my-site` 完成上传、环境配置、网站创建、重载全流程
- **无需浏览器** - 所有操作通过命令行完成，适合脚本和 AI Agent 调用
- **免费套餐友好** - 专为 PythonAnywhere 免费用户设计

## 环境要求

| 要求 | 版本 |
|------|------|
| Python | 3.10 或更高 |
| 操作系统 | Windows / macOS / Linux |
| 网络 | 需要能访问 pythonanywhere.com |

## 安装

### 方式一：从源码安装（推荐）

```bash
# 克隆仓库
git clone https://github.com/your-username/pythonanywhere-cli.git
cd pythonanywhere-cli

# 安装（开发模式）
pip install -e .
```

### 方式二：直接安装依赖

```bash
pip install typer requests beautifulsoup4 websocket-client
```

### 验证安装

```bash
pa --version
```

预期输出：

```
pa, version 0.1.0
```

---

## 账号配置

### 第一步：注册 PythonAnywhere 账号（如果没有）

如果你还没有 PythonAnywhere 账号，可以通过命令行注册：

```bash
pa register
```

按照提示输入：
- 邮箱地址
- 用户名
- 密码

注册成功后，你会收到一封确认邮件。

> **提示**：如果你已有账号，跳过此步。

### 第二步：初始化配置

```bash
pa init
```

交互式配置过程：

```
请输入 PythonAnywhere 用户名: yourusername
正在获取 API Token...
配置已保存到 ~/.pa-cli/config.json
```

`pa init` 会自动完成以下操作：
1. 保存你的用户名
2. 自动从 PythonAnywhere 获取 API Token
3. 将配置写入 `~/.pa-cli/config.json`

### 配置文件说明

配置保存在 `~/.pa-cli/config.json`：

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

## 第一个项目部署

假设你有一个简单的 Flask 项目，目录结构如下：

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

### 一键部署

```bash
pa deploy ./my-site
```

部署过程输出：

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

### 验证部署

在浏览器中打开 `https://yourusername.pythonanywhere.com`，应该看到：

```
Hello from PythonAnywhere!
```

### 指定自定义域名

```bash
pa deploy ./my-site --domain mysite.pythonanywhere.com
```

---

## 常用命令速查

### 账号管理

| 命令 | 说明 |
|------|------|
| `pa init` | 初始化/更新账号配置 |
| `pa register` | 注册新账号 |
| `pa account login` | 保存密码（用于爬虫操作） |
| `pa account extend` | 延长免费账号有效期 |

### 部署

| 命令 | 说明 |
|------|------|
| `pa deploy <目录>` | 一键部署到默认域名 |
| `pa deploy <目录> --domain <域名>` | 部署到指定域名 |

### 文件管理

| 命令 | 说明 |
|------|------|
| `pa files upload <本地路径> <远程路径>` | 上传单个文件 |
| `pa files upload <本地路径> <远程路径> -r` | 递归上传目录 |

### Web 应用管理

| 命令 | 说明 |
|------|------|
| `pa webapp reload <域名>` | 重载 Web 应用 |
| `pa webapp hits <域名>` | 查看访问统计 |
| `pa webapp config <域名> --source-dir <路径>` | 设置源码目录 |
| `pa webapp config <域名> --virtualenv <路径>` | 设置虚拟环境路径 |

### 控制台管理

| 命令 | 说明 |
|------|------|
| `pa console list` | 列出所有控制台 |
| `pa console create` | 创建新控制台 |
| `pa console send <id> <命令>` | 发送命令并获取输出 |
| `pa console kill <id>` | 终止控制台 |

---

## 常见问题

### Q: `pa init` 报错 "无法获取 API Token"

**原因**：可能是网络问题或 PythonAnywhere 会话过期。

**解决**：
1. 确认能访问 pythonanywhere.com
2. 手动获取 Token：登录 PythonAnywhere → Account → API Token → 生成新 Token
3. 手动编辑配置文件 `~/.pa-cli/config.json`

### Q: 部署后访问网站显示 500 错误

**原因**：通常是应用代码错误或依赖未正确安装。

**解决**：
```bash
# 查看错误日志
pa webapp logs yourusername.pythonanywhere.com

# 检查虚拟环境是否正确配置
pa webapp config yourusername.pythonanywhere.com --virtualenv /home/yourusername/my-site/.venv
```

### Q: 免费账号有什么限制？

- CPU 时间有限（每天几秒）
- 没有 SSH 访问（这正是本工具存在的意义）
- 只能创建一个 Web 应用
- 自动过期（每 3 个月需要续期）

续期命令：
```bash
pa account extend
```

### Q: 如何更新已部署的项目？

再次运行部署命令即可：

```bash
pa deploy ./my-site
```

这会重新上传文件并重载应用。

### Q: 支持哪些 Python 版本？

PythonAnywhere 支持 Python 3.10、3.11、3.12。默认使用 3.10，可在创建 Web 应用时指定。

---

## 下一步

- 阅读 [README.md](../README.md) 了解完整命令列表
- 查看 [PRD 文档](../docs/prd-mvp.md) 了解技术细节
- 提交 Issue 或 PR 参与项目开发
