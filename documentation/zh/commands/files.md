# Files 命令

文件管理相关的命令，用于将本地文件上传到 PythonAnywhere 服务器。

---

## pa files upload

上传文件或目录到 PythonAnywhere。

### 语法

```bash
pa files upload <local_path> <remote_path> [-r | --recursive]
```

### 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `local_path` | 是 | 本地文件或目录路径 |
| `remote_path` | 是 | PythonAnywhere 上的远程路径 |

### 选项

| 选项 | 说明 |
|------|------|
| `-r`, `--recursive` | 递归上传目录及其所有内容 |

### 说明

- 使用 Token 认证，通过 REST API 上传
- 远程路径以 `/home/{username}/` 为根目录
- 单文件上传返回 HTTP 状态码
- 目录上传时自动遍历所有子文件，路径分隔符统一转换为 `/`

### 示例

**上传单个文件：**

```bash
$ pa files upload ./app.py /home/myuser/myproject/app.py
Uploaded ./app.py -> /home/myuser/myproject/app.py (HTTP 200)
```

**上传整个目录：**

```bash
$ pa files upload ./myproject /home/myuser/myproject -r
Uploaded 15 files to /home/myuser/myproject
```

**上传到用户根目录：**

```bash
$ pa files upload ./config.json /home/myuser/config.json
Uploaded ./config.json -> /home/myuser/config.json (HTTP 200)
```

### 错误场景

**本地路径不存在：**

```bash
$ pa files upload ./nonexistent /home/myuser/test
Error: ./nonexistent does not exist
```

**上传目录时未指定 `-r`：**

```bash
$ pa files upload ./myproject /home/myuser/myproject
Error: Use -r/--recursive to upload directories
```

**API 认证失败（Token 无效）：**

```bash
Error: API error 401: Invalid token.
```

**远程路径无写入权限：**

```bash
Error: API error 403: You do not have permission to write to this path.
```

**上传失败：**

```bash
Error: Upload failed: 500 Internal Server Error
```

### 前置条件

- 需先运行 `pa init` 完成账户配置（包含有效的 API Token）

### 注意事项

- 上传操作会覆盖远程同名文件
- 目录上传时保持本地目录结构，`local_path` 的最后一级目录名会作为远程目录名
- 大量文件上传时无进度显示，完成后显示总文件数
