# Console 命令

控制台管理相关的命令，用于在 PythonAnywhere 上创建、操作和管理远程控制台。

---

## pa console list

列出当前账户的所有控制台。

### 语法

```bash
pa console list
```

### 说明

通过 REST API 获取所有控制台列表，显示每个控制台的 ID 和名称。

### 示例

```bash
$ pa console list
ID: 12345, Name: Bash
ID: 12346, Name: Python 3.10
```

**无控制台时：**

```bash
$ pa console list
No consoles found.
```

### 错误场景

**API 认证失败：**

```bash
Error: API error 401: Invalid token.
```

### 前置条件

- 需先运行 `pa init` 完成账户配置

---

## pa console create

创建一个新的控制台。

### 语法

```bash
pa console create [--executable <executable>]
```

### 选项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `--executable` | `bash` | 控制台可执行程序，如 `bash`、`python3.10` |

### 示例

**创建默认 Bash 控制台：**

```bash
$ pa console create
Console created: id=12347, executable=bash
```

**创建 Python 控制台：**

```bash
$ pa console create --executable python3.10
Console created: id=12348, executable=python3.10
```

### 错误场景

**超出控制台数量限制：**

```bash
Error: API error 400: You have too many consoles.
```

### 前置条件

- 需先运行 `pa init` 完成账户配置

---

## pa console send

向控制台发送命令并获取输出。

### 语法

```bash
pa console send <console_id> <command> [--wait/--no-wait]
```

### 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `console_id` | 是 | 控制台 ID（可通过 `pa console list` 获取） |
| `command` | 是 | 要发送的命令 |

### 选项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `--wait`, `-w` | 启用 | 等待命令输出（等待约 1 秒后获取输出） |
| `--no-wait`, `-W` | - | 发送后立即返回，不等待输出 |

### 说明

- 命令发送后自动追加换行符 `\n`
- `--wait` 模式下，发送命令后等待约 1 秒获取输出
- `send_input` 端点的 API 频率限制为 120 次/分钟（高于标准端点的 40 次/分钟）

### 示例

**发送命令并等待输出：**

```bash
$ pa console send 12345 "ls -la"
total 32
drwxr-xr-x 5 user user 4096 May 30 10:00 .
drwxr-xr-x 3 user user 4096 May 30 09:00 ..
-rw-r--r-- 1 user user  220 May 30 10:00 app.py
```

**发送命令不等待输出：**

```bash
$ pa console send 12345 "pip install flask" --no-wait
Sent to console 12345: pip install flask
```

**执行 Python 代码：**

```bash
$ pa console send 12346 "print(2 + 3)"
5
```

### 错误场景

**控制台不存在：**

```bash
Error: API error 404: Console not found.
```

**无输出时：**

```bash
(no output)
```

### 前置条件

- 需先运行 `pa init` 完成账户配置
- 需要一个已存在的控制台（通过 `pa console create` 或 `pa console get-or-create` 创建）

---

## pa console kill

终止一个控制台。

### 语法

```bash
pa console kill <console_id>
```

### 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `console_id` | 是 | 控制台 ID |

### 示例

```bash
$ pa console kill 12345
Console 12345 killed.
```

### 错误场景

**控制台不存在：**

```bash
Error: API error 404: Console not found.
```

### 前置条件

- 需先运行 `pa init` 完成账户配置

---

## pa console activate

通过 WebSocket 激活控制台。

### 语法

```bash
pa console activate <console_id>
```

### 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `console_id` | 是 | 控制台 ID |

### 说明

此命令通过爬虫模拟浏览器操作，获取控制台的 WebSocket 连接信息并建立连接以激活控制台。激活操作包括：
1. 访问控制台 frame 页面
2. 解析页面中的 WebSocket 参数
3. 建立 WebSocket 连接并发送初始化消息

此命令需要存储密码（Session 认证），因为需要模拟浏览器登录。

### 示例

```bash
$ pa console activate 12345
Console 12345 activated successfully.
```

### 错误场景

**密码未存储：**

```bash
$ pa console activate 12345
Password not found. Run 'pa account login' first.
```

**登录失败：**

```bash
Error: Login failed
```

**页面结构变更导致解析失败：**

```bash
Error: Could not parse WebSocket info from frame page
```

**WebSocket 连接失败：**

```bash
Error: WebSocket connection failed: Connection refused
```

### 前置条件

- 需先运行 `pa init` 完成账户配置
- 需先运行 `pa account login` 存储密码

---

## pa console get-or-create

获取一个现有的控制台，如果没有可用的则创建新控制台。

### 语法

```bash
pa console get-or-create [-e <executable> | --executable <executable>]
```

### 选项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `-e`, `--executable` | `bash` | 控制台可执行程序 |

### 说明

此命令自动管理控制台生命周期：
1. 列出现有控制台
2. 如果已有控制台，返回第一个控制台的 ID
3. 如果已有 2 个或更多控制台，删除最早的控制台后创建新控制台
4. 如果没有控制台，创建一个新的

此命令需要存储密码（Session 认证），因为需要通过爬虫进行操作。

### 示例

**获取或创建默认控制台：**

```bash
$ pa console get-or-create
Console ready: 12345
```

**指定可执行程序：**

```bash
$ pa console get-or-create -e python3.10
Console ready: 12346
```

### 错误场景

**密码未存储：**

```bash
$ pa console get-or-create
Password not found. Run 'pa account login' first.
```

### 前置条件

- 需先运行 `pa init` 完成账户配置
- 需先运行 `pa account login` 存储密码

---

## 典型工作流

### 执行远程命令

```bash
# 创建或获取控制台
pa console get-or-create

# 查看控制台列表获取 ID
pa console list

# 发送命令
pa console send 12345 "cd /home/myuser && ls"

# 用完后终止
pa console kill 12345
```

### 安装 Python 依赖

```bash
pa console create --executable python3.10
pa console send 12346 "import pip; pip.main(['install', 'flask', 'requests'])"
pa console kill 12346
```
