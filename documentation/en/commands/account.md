# Account Commands

Account management commands, including initializing configuration, registering new accounts, storing passwords, fetching API Tokens, and extending account expiry.

---

## pa init

Interactively configure a PythonAnywhere account. Automatically logs in and fetches the API Token.

### Syntax

```bash
pa init
```

### Description

This command sequentially prompts for the following information:
1. PythonAnywhere username
2. Password (hidden input)
3. Host address (default: `www.pythonanywhere.com`)

After configuration is complete, it automatically logs in via the crawler and fetches the API Token, saving it to `~/.pa-cli/config.json`.

### Example

```bash
$ pa init
PythonAnywhere username: myuser
Password: ********
Host [www.pythonanywhere.com]:
Account 'myuser' configured successfully.
API token fetched and saved.
```

### Error Scenarios

**Incorrect username or password:**

```bash
$ pa init
PythonAnywhere username: wronguser
Password: ********
Host [www.pythonanywhere.com]:
Login failed. Please check your username and password.
Don't have an account? Register with: pa register
```

**Network error:**

```bash
Error: Failed to fetch login page: Connection refused
```

### Prerequisites

- No prior configuration needed; run this when using the CLI for the first time
- Requires a valid PythonAnywhere account (run `pa register` first if you don't have one)

---

## pa register

Register a new PythonAnywhere account.

### Syntax

```bash
pa register
```

### Description

Completes the registration process by simulating browser behavior via the crawler. Sequentially prompts for:
1. Username (letters and numbers only)
2. Email address
3. Password (hidden input)
4. Confirm password (hidden input)

### Example

```bash
$ pa register
Username (letters and numbers only): newuser
Email: user@example.com
Password: ********
Confirm password: ********
Account 'newuser' registered successfully!
Please check your email to verify your account.
Then run: pa init
```

### Error Scenarios

**Passwords do not match:**

```bash
$ pa register
Username (letters and numbers only): newuser
Email: user@example.com
Password: ********
Confirm password: ********
Passwords do not match.
```

**Registration failed (e.g., username already exists):**

```bash
Registration failed. Please check your inputs.
```

**Network error:**

```bash
Error: Failed to fetch registration page: Connection refused
```

### Next Steps

After successful registration:
1. Check your email to complete verification
2. Run `pa init` to configure your account

---

## pa account login

Store the current account's password in the local configuration file.

### Syntax

```bash
pa account login
```

### Description

Some commands (such as `pa account token`, `pa account extend`, `pa console activate`, `pa console get-or-create`) require simulating login via the crawler, which necessitates storing the password locally. This command only saves the password to `~/.pa-cli/config.json` and does not perform a login operation.

The password is stored in plaintext in the configuration file.

### Example

```bash
$ pa account login
Password: ********
Password saved successfully.
```

### Prerequisites

- Must run `pa init` first to complete account configuration

---

## pa account token

Log in via the crawler and fetch the API Token.

### Syntax

```bash
pa account token
```

### Description

Uses the username and password from the configuration file to simulate a browser login to PythonAnywhere, scrapes the API Token from the account page, and saves it to the configuration file.

### Example

```bash
$ pa account token
API token: abc123def456ghi789
Token saved to config.
```

### Error Scenarios

**Password not stored:**

```bash
$ pa account token
Error: Password not found in config. Run 'pa account login' to store it.
```

**Login failed:**

```bash
Login failed. Check your credentials.
```

**Token extraction failed due to page structure change:**

```bash
Error: API token not found on account page
```

### Prerequisites

- Must run `pa init` first to complete account configuration
- Must run `pa account login` first to store the password

---

## pa account extend

Extend the expiry of a free account.

### Syntax

```bash
pa account extend
```

### Description

Free accounts have an expiration date, after which they are deleted. This command automatically extends the account expiry by simulating browser operations via the crawler. The implementation finds and submits the "extend" form on the Web Apps page.

### Example

```bash
$ pa account extend
Account expiry extended successfully.
```

### Error Scenarios

**Password not stored:**

```bash
$ pa account extend
Error: Password not found in config. Run 'pa account login' to store it.
```

**Login failed:**

```bash
Login failed. Check your credentials.
```

**Extension failed (e.g., page structure change):**

```bash
Failed to extend account expiry.
```

**Extend form not found:**

```bash
Error: Extend form not found on webapps page
```

### Prerequisites

- Must run `pa init` first to complete account configuration
- Must run `pa account login` first to store the password

---

## Authentication Methods

This CLI uses two authentication methods:

| Method | Description | Applicable Commands |
|--------|-------------|---------------------|
| Token Authentication | Calls REST API via API Token | `pa files`, `pa console list/create/send/kill`, `pa webapp create/config/static/reload`, `pa deploy` |
| Session Authentication | Simulates browser login via password | `pa account token`, `pa account extend`, `pa console activate/get-or-create`, `pa webapp reload-crawler/hits` |

Token authentication rate limit is 40 requests/minute for standard API endpoints, and 120 requests/minute for the `send_input` endpoint.
