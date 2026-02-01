# Quick Reference Guide

Fast lookup guide for the MCP implementation.

## Directory Reference

```
Standard-MCP-Implementation/
├── README.md                 ← Start here for overview
├── SETUP.md                  ← Installation steps
├── ARCHITECTURE.md           ← System design
├── EXAMPLES.md               ← Code examples
├── PROJECT_SUMMARY.md        ← This project overview
├── QUICK_REFERENCE.md        ← This file
├── mcp_server/
│   ├── server.py            # Main server (250+ lines)
│   ├── requirements.txt      # pip install
│   └── README.md             # Server docs
├── mcp_client/
│   ├── client.py            # Main client (300+ lines)
│   ├── requirements.txt      # pip install
│   └── README.md             # Client docs
└── user_app/
    ├── app.py               # Main app (300+ lines)
    ├── requirements.txt      # pip install
    └── README.md             # App docs
```

## Quick Commands

### Install & Run Server
```bash
cd mcp_server
pip install -r requirements.txt
python server.py
# Output: Uvicorn running on http://127.0.0.1:8000
```

### Install & Run Application
```bash
cd user_app
pip install -r requirements.txt
python app.py
```

### Test Client
```bash
cd mcp_client
pip install -r requirements.txt
python client.py
```

## Server Tools

| Tool | Parameters | Returns |
|------|-----------|---------|
| `add_numbers` | `a`, `b` | `{"result": sum}` |
| `multiply_numbers` | `a`, `b` | `{"result": product}` |
| `calculate_statistics` | `numbers` | `{"mean", "sum", "min", "max"}` |
| `get_user` | `user_id` | `{"success", "user"}` |
| `list_users` | (none) | `{"count", "users"}` |
| `get_tasks` | `filter_status?` | `{"count", "tasks"}` |
| `create_task` | `title`, `assigned_to` | `{"success", "task"}` |

## Server Resources

| URI | Type | Returns |
|-----|------|---------|
| `data://users/{id}` | GET | User JSON |
| `data://config` | GET | Config JSON |
| `data://summary` | GET | Summary JSON |

## Client API

### Basic Usage
```python
from mcp_client.client import MCPClient

# With context manager (recommended)
with MCPClient() as client:
    result = client.add_numbers(5, 3)

# Manual management
client = MCPClient()
try:
    result = client.add_numbers(5, 3)
finally:
    client.close()
```

### Tool Methods
```python
client.add_numbers(a, b)
client.multiply_numbers(a, b)
client.calculate_statistics(numbers)
client.get_user(user_id)
client.list_users()
client.get_tasks(filter_status=None)
client.create_task(title, assigned_to)
```

### Resource Methods
```python
client.read_user_resource(user_id)
client.read_config_resource()
client.read_summary_resource()
```

## Application Actions

```bash
python app.py                    # All workflows
python app.py --action calc      # Calculations only
python app.py --action users     # Users only
python app.py --action tasks     # Tasks only
python app.py --action summary   # Summary only
```

## Data Models

### User
```python
{
    "id": int,
    "name": str,
    "email": str,
    "role": str  # "admin" or "user"
}
```

### Task
```python
{
    "id": int,
    "title": str,
    "status": str,  # "pending", "in_progress", "completed"
    "assigned_to": int  # user_id
}
```

### Configuration
```python
{
    "app_name": str,
    "version": str,
    "debug": bool
}
```

## Error Handling

### Client Errors
```python
from mcp_client.client import MCPClientError

try:
    result = client.add_numbers(5, 3)
except MCPClientError as e:
    print(f"Error: {e}")
```

## Common Patterns

### Batch Operations
```python
with MCPClient() as client:
    for i in range(1, 11):
        result = client.add_numbers(i, i*2)
        print(result['result'])
```

### Error Recovery
```python
with MCPClient() as client:
    try:
        user = client.get_user(999)
        if not user['success']:
            print(f"User not found: {user['error']}")
    except MCPClientError as e:
        print(f"Connection error: {e}")
```

### Conditional Logic
```python
with MCPClient() as client:
    tasks = client.get_tasks()
    if tasks['count'] > 0:
        for task in tasks['tasks']:
            print(f"Task: {task['title']}")
```

## URL Reference

### Local Server
- Base URL: `http://127.0.0.1:8000`
- Tool Endpoint: `/tools/{tool_name}/execute`
- Resource Endpoint: `/resources/{resource_uri}`

## Response Format

### Success Response
```json
{
    "success": true,
    "data": {...}
}
```

### Error Response
```json
{
    "success": false,
    "error": "Description of error"
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 in use | Kill process on port: `lsof -i :8000` |
| Connection refused | Ensure server is running |
| Module not found | Install deps: `pip install -r requirements.txt` |
| Wrong Python version | Use Python 3.8+: `python --version` |
| Permission denied | Use venv or sudo |

## Development Workflow

### 1. Start Server
```bash
cd mcp_server && python server.py
```

### 2. Test in Another Terminal
```bash
cd mcp_client && python client.py
```

### 3. Run Application
```bash
cd user_app && python app.py
```

## Performance Tips

- Use context managers for connection pooling
- Batch operations when possible
- Cache frequently accessed resources
- Minimize serialization/deserialization overhead

## File Sizes

| File | Size |
|------|------|
| `server.py` | ~250 lines |
| `client.py` | ~300 lines |
| `app.py` | ~300 lines |
| Documentation | ~1500 lines |
| Total | ~2000+ lines |

## Key Technologies

- **FastMCP**: Server framework
- **httpx**: HTTP client
- **Pydantic**: Data validation
- **Tabulate**: Table formatting
- **Python 3.8+**: Runtime

## Resource Links

- [FastMCP Docs](https://fastmcp.readthedocs.io/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [httpx Documentation](https://www.python-httpx.org/)

## Common Use Cases

### 1. Add a New Tool
```python
# In server.py
@mcp.tool()
def new_tool(param: str) -> dict:
    """Tool description."""
    return {"result": param}

# In client.py, add method:
def new_tool(self, param: str) -> dict:
    return self._call_tool("new_tool", {"param": param})
```

### 2. Add a New Resource
```python
# In server.py
@mcp.resource(uri_template="data://resource")
def read_resource() -> str:
    return json.dumps(data)

# In client.py, add method:
def read_resource(self) -> dict:
    return self._read_resource("data://resource")
```

### 3. Add New Application Action
```python
# In app.py
def new_action(self):
    """Perform new action."""
    result = self.client.new_tool("param")
    print(result)

# In main():
elif args.action == "new":
    app.new_action()
```

## Best Practices

✓ Always use context managers for client  
✓ Handle exceptions explicitly  
✓ Add type hints to all functions  
✓ Document all public methods  
✓ Use meaningful variable names  
✓ Keep functions focused and small  
✓ Test error conditions  
✓ Log important operations  

## Next Steps

1. Read [SETUP.md](SETUP.md) for installation
2. Run the server and application
3. Explore [EXAMPLES.md](EXAMPLES.md) for patterns
4. Study [ARCHITECTURE.md](ARCHITECTURE.md) for design
5. Extend with your own tools and resources

---

**Version**: 1.0.0
**Last Updated**: February 2026
