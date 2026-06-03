# Console Commands

Console management commands for creating, operating, and managing remote consoles on PythonAnywhere.

---

## pa console list

List all consoles for the current account.

### Syntax

```bash
pa console list
```

### Description

Retrieves all consoles via the REST API, displaying each console's ID and name.

### Examples

```bash
$ pa console list
ID: 12345, Name: Bash
ID: 12346, Name: Python 3.10
```

**When no consoles exist:**

```bash
$ pa console list
No consoles found.
```

### Error Scenarios

**API authentication failed:**

```bash
Error: API error 401: Invalid token.
```

### Prerequisites

- Must run `pa init` first to complete account configuration

---

## pa console create

Create a new console.

### Syntax

```bash
pa console create [--executable <executable>]
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--executable` | `bash` | Console executable, e.g., `bash`, `python3.10` |

### Examples

**Create a default Bash console:**

```bash
$ pa console create
Console created: id=12347, executable=bash
```

**Create a Python console:**

```bash
$ pa console create --executable python3.10
Console created: id=12348, executable=python3.10
```

### Error Scenarios

**Console limit exceeded:**

```bash
Error: API error 400: You have too many consoles.
```

### Prerequisites

- Must run `pa init` first to complete account configuration

---

## pa console send

Send a command to a console and retrieve the output.

### Syntax

```bash
pa console send <console_id> <command> [--wait/--no-wait]
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `console_id` | Yes | Console ID (obtainable via `pa console list`) |
| `command` | Yes | The command to send |

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--wait`, `-w` | Enabled | Wait for command output (waits approximately 1 second before retrieving output) |
| `--no-wait`, `-W` | - | Return immediately after sending, without waiting for output |

### Description

- A newline character `\n` is automatically appended to the command
- In `--wait` mode, the command waits approximately 1 second after sending before retrieving output
- The `send_input` endpoint has an API rate limit of 120 requests/minute (higher than the standard 40 requests/minute)

### Examples

**Send a command and wait for output:**

```bash
$ pa console send 12345 "ls -la"
total 32
drwxr-xr-x 5 user user 4096 May 30 10:00 .
drwxr-xr-x 3 user user 4096 May 30 09:00 ..
-rw-r--r-- 1 user user  220 May 30 10:00 app.py
```

**Send a command without waiting for output:**

```bash
$ pa console send 12345 "pip install flask" --no-wait
Sent to console 12345: pip install flask
```

**Execute Python code:**

```bash
$ pa console send 12346 "print(2 + 3)"
5
```

### Error Scenarios

**Console does not exist:**

```bash
Error: API error 404: Console not found.
```

**No output:**

```bash
(no output)
```

### Prerequisites

- Must run `pa init` first to complete account configuration
- Requires an existing console (created via `pa console create` or `pa console get-or-create`)

---

## pa console kill

Terminate a console.

### Syntax

```bash
pa console kill <console_id>
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `console_id` | Yes | Console ID |

### Examples

```bash
$ pa console kill 12345
Console 12345 killed.
```

### Error Scenarios

**Console does not exist:**

```bash
Error: API error 404: Console not found.
```

### Prerequisites

- Must run `pa init` first to complete account configuration

---

## pa console activate

Activate a console via WebSocket.

### Syntax

```bash
pa console activate <console_id>
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `console_id` | Yes | Console ID |

### Description

This command activates a console by simulating browser operations via the crawler. It retrieves the console's WebSocket connection information from the frame page and establishes a connection. The activation process includes:
1. Accessing the console frame page
2. Parsing WebSocket parameters from the page
3. Establishing a WebSocket connection and sending initialization messages

This command requires a stored password (Session authentication) because it simulates browser login.

### Examples

```bash
$ pa console activate 12345
Console 12345 activated successfully.
```

### Error Scenarios

**Password not stored:**

```bash
$ pa console activate 12345
Password not found. Run 'pa account login' first.
```

**Login failed:**

```bash
Error: Login failed
```

**Page structure change causing parse failure:**

```bash
Error: Could not parse WebSocket info from frame page
```

**WebSocket connection failed:**

```bash
Error: WebSocket connection failed: Connection refused
```

### Prerequisites

- Must run `pa init` first to complete account configuration
- Must run `pa account login` first to store the password

---

## pa console get-or-create

Get an existing console, or create a new one if none are available.

### Syntax

```bash
pa console get-or-create [-e <executable> | --executable <executable>]
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `-e`, `--executable` | `bash` | Console executable |

### Description

This command automatically manages the console lifecycle:
1. Lists existing consoles
2. If consoles exist, returns the ID of the first one
3. If 2 or more consoles exist, deletes the oldest one and creates a new one
4. If no consoles exist, creates a new one

This command requires a stored password (Session authentication) because it performs operations via the crawler.

### Examples

**Get or create a default console:**

```bash
$ pa console get-or-create
Console ready: 12345
```

**Specify an executable:**

```bash
$ pa console get-or-create -e python3.10
Console ready: 12346
```

### Error Scenarios

**Password not stored:**

```bash
$ pa console get-or-create
Password not found. Run 'pa account login' first.
```

### Prerequisites

- Must run `pa init` first to complete account configuration
- Must run `pa account login` first to store the password

---

## Typical Workflows

### Execute Remote Commands

```bash
# Create or get a console
pa console get-or-create

# List consoles to get the ID
pa console list

# Send commands
pa console send 12345 "cd /home/myuser && ls"

# Terminate when done
pa console kill 12345
```

### Install Python Dependencies

```bash
pa console create --executable python3.10
pa console send 12346 "import pip; pip.main(['install', 'flask', 'requests'])"
pa console kill 12346
```
