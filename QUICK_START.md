# Quick Start Guide

This guide will get the MCP Implementation up and running in minutes.

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Terminal access

## Installation

### 1. Install Dependencies

Install the required packages for all three projects:

```bash
# Install server dependencies
pip install -r mcp_server/requirements.txt

# Install client dependencies  
pip install -r mcp_client/requirements.txt

# Install application dependencies
pip install -r user_app/requirements.txt
```

Or install all at once:

```bash
pip install -r mcp_server/requirements.txt -r mcp_client/requirements.txt -r user_app/requirements.txt
```

## Running the System

### Step 1: Start the MCP Server

In terminal 1:

```bash
cd mcp_server
python server.py
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

The server is now running and accepting MCP requests.

### Step 2: Run the User Application

In terminal 2:

```bash
cd user_app
python app.py
```

This will run the complete workflow, demonstrating:
- ✓ Mathematical calculations (addition, multiplication, statistics)
- ✓ User management (list users, read user resources)
- ✓ Task management (list tasks, create tasks, filter by status)
- ✓ Configuration and summary retrieval

You'll see formatted tables with results for each operation.

### Step 3: Test Client Directly (Optional)

In terminal 2 (if not running app.py):

```bash
cd mcp_client
python -c "
from client import MCPClient

client = MCPClient()
result = client.add_numbers(10, 5)
print(f'10 + 5 = {result[\"result\"]}')
client.close()
"
```

## Available Tools (Server)

The MCP Server provides these tools:

| Tool | Description | Example |
|------|-------------|---------|
| `add_numbers` | Add two numbers | add_numbers(5, 3) → 8 |
| `multiply_numbers` | Multiply two numbers | multiply_numbers(4, 7) → 28 |
| `calculate_statistics` | Calculate stats for a list | calculate_statistics([1,2,3]) |
| `get_user` | Get a user by ID | get_user(1) |
| `list_users` | Get all users | list_users() |
| `get_tasks` | Get tasks by status | get_tasks("completed") |
| `create_task` | Create a new task | create_task("Title", 1) |

## Available Resources (Server)

The MCP Server provides these file-like resources:

| Resource | URI | Description |
|----------|-----|-------------|
| Users List | `data://users/list` | Returns all users in JSON format |
| Configuration | `data://config` | Returns application configuration |
| Summary | `data://summary` | Returns summary statistics |

Access via client:
```python
client = MCPClient()
users = client.read_users_resource()
config = client.read_config_resource()
summary = client.read_summary_resource()
```

## Running Tests

To verify everything is working:

```bash
python test_integration.py
```

Output should show:
```
✓ All tests passed!
```

## Application Options

Run the app with specific actions:

```bash
# Run everything (default)
python app.py

# Run only calculations
python app.py --action calc

# Run only user management
python app.py --action users

# Run only task management
python app.py --action tasks

# Run only configuration/summary
python app.py --action summary

# Connect to different server
python app.py --server-url http://localhost:8000
```

## Troubleshooting

### Server won't start

**Error**: `Address already in use`
- Another process is using port 8000
- **Solution**: Kill the process using port 8000 or use a different port:
  ```bash
  # Edit mcp_server/server.py and change port 8000 to another port
  ```

### Client connection refused

**Error**: `[Errno 111] Connection refused`
- Server is not running
- **Solution**: Make sure server.py is running in another terminal

### Missing dependencies

**Error**: `ModuleNotFoundError: No module named 'fastmcp'`
- Dependencies not installed
- **Solution**: Run `pip install -r requirements.txt` in the appropriate project directory

### Python version issues

**Error**: `Syntax error` or `Type hints not supported`
- Python version is too old (< 3.8)
- **Solution**: Upgrade Python to 3.8+ or use a virtual environment

## Architecture

```
┌─────────────────────────────────────────────────────┐
│         USER APPLICATION (user_app/)                │
│  ├─ app.py          - High-level business logic    │
│  ├─ requirements.txt - Dependencies                │
│  └─ README.md       - Documentation                │
│           ↓ uses
├─────────────────────────────────────────────────────┤
│         MCP CLIENT (mcp_client/)                    │
│  ├─ client.py       - HTTP wrapper for MCP         │
│  ├─ requirements.txt - Dependencies                │
│  └─ README.md       - Documentation                │
│           ↓ HTTP requests/responses
├─────────────────────────────────────────────────────┤
│         MCP SERVER (mcp_server/)                    │
│  ├─ server.py       - FastMCP server               │
│  ├─ requirements.txt - Dependencies                │
│  └─ README.md       - Documentation                │
│           ↑ Serves on port 8000
└─────────────────────────────────────────────────────┘
```

## Project Structure

```
Standard-MCP-Implementation/
├── mcp_server/              # FastMCP server
│   ├── server.py           # Server implementation (259 lines)
│   ├── requirements.txt     # Dependencies
│   └── README.md          # Server documentation
│
├── mcp_client/              # MCP client wrapper
│   ├── client.py           # Client implementation (337 lines)
│   ├── requirements.txt     # Dependencies
│   └── README.md          # Client documentation
│
├── user_app/                # User-facing application
│   ├── app.py              # Application implementation
│   ├── requirements.txt     # Dependencies
│   └── README.md          # Application documentation
│
├── test_integration.py      # Integration test suite
├── API_COMPATIBILITY_FIX.md # FastMCP 2.14.4 compatibility notes
├── README.md               # This file
└── OTHER DOCUMENTATION/    # Additional guides and references
```

## Performance

- **Server startup time**: < 1 second
- **Tool call latency**: < 100ms
- **Resource read latency**: < 50ms
- **Concurrent requests**: Limited by uvicorn workers

## Next Steps

1. **Explore the code**: Each component has detailed inline documentation
2. **Modify the data**: Edit `data_store` in server.py to add/modify users and tasks
3. **Add new tools**: Follow the pattern in server.py to create new tools
4. **Add new resources**: Follow the resource definition pattern for new data sources
5. **Deploy**: The server can be deployed to any cloud platform supporting Python/FastAPI

## Documentation Files

- [README.md](README.md) - Project overview
- [mcp_server/README.md](mcp_server/README.md) - Server documentation
- [mcp_client/README.md](mcp_client/README.md) - Client documentation
- [user_app/README.md](user_app/README.md) - Application documentation
- [API_COMPATIBILITY_FIX.md](API_COMPATIBILITY_FIX.md) - API migration guide
- [DEPENDENCY_FIX.md](DEPENDENCY_FIX.md) - Dependency resolution details

## Support

For issues or questions, refer to the detailed README files in each project directory.
