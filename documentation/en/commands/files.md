# Files Commands

File management commands for uploading local files to the PythonAnywhere server.

---

## pa files upload

Upload a file or directory to PythonAnywhere.

### Syntax

```bash
pa files upload <local_path> <remote_path> [-r | --recursive]
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `local_path` | Yes | Local file or directory path |
| `remote_path` | Yes | Remote path on PythonAnywhere |

### Options

| Option | Description |
|--------|-------------|
| `-r`, `--recursive` | Recursively upload a directory and all its contents |

### Description

- Uses Token authentication for upload via REST API
- Remote paths use `/home/{username}/` as the root directory
- Single file upload returns an HTTP status code
- Directory upload automatically traverses all sub-files, with path separators normalized to `/`

### Examples

**Upload a single file:**

```bash
$ pa files upload ./app.py /home/myuser/myproject/app.py
Uploaded ./app.py -> /home/myuser/myproject/app.py (HTTP 200)
```

**Upload an entire directory:**

```bash
$ pa files upload ./myproject /home/myuser/myproject -r
Uploaded 15 files to /home/myuser/myproject
```

**Upload to user root directory:**

```bash
$ pa files upload ./config.json /home/myuser/config.json
Uploaded ./config.json -> /home/myuser/config.json (HTTP 200)
```

### Error Scenarios

**Local path does not exist:**

```bash
$ pa files upload ./nonexistent /home/myuser/test
Error: ./nonexistent does not exist
```

**Uploading a directory without `-r`:**

```bash
$ pa files upload ./myproject /home/myuser/myproject
Error: Use -r/--recursive to upload directories
```

**API authentication failed (invalid token):**

```bash
Error: API error 401: Invalid token.
```

**No write permission to remote path:**

```bash
Error: API error 403: You do not have permission to write to this path.
```

**Upload failed:**

```bash
Error: Upload failed: 500 Internal Server Error
```

### Prerequisites

- Must run `pa init` first to complete account configuration (including a valid API Token)

### Notes

- Upload operations will overwrite remote files with the same name
- Directory upload preserves the local directory structure; the last directory name of `local_path` becomes the remote directory name
- No progress display for large file uploads; the total file count is shown upon completion
