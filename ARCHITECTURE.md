# Architecture

Detailed architecture documentation for the Standard MCP Implementation.

## System Design

### Three-Tier Architecture

```
┌─────────────────────────────────────────────────────────┐
│               PRESENTATION TIER                         │
│         User Application (user_app/app.py)              │
│                                                         │
│  - UserApplication class                                │
│  - Business logic methods                               │
│  - Formatted output (tables, JSON)                       │
│  - Action-based workflow                                │
└────────────────┬────────────────────────────────────────┘
                 │ HTTP over Network
                 │
┌─────────────────────────────────────────────────────────┐
│               CLIENT TIER                               │
│          MCP Client (mcp_client/client.py)              │
│                                                         │
│  - MCPClient class                                      │
│  - Tool methods (add_numbers, list_users, etc.)         │
│  - Resource methods (read_config, read_summary)         │
│  - Error handling                                       │
│  - Connection management                                │
└────────────────┬────────────────────────────────────────┘
                 │ HTTP/REST API
                 │
┌─────────────────────────────────────────────────────────┐
│               SERVER TIER                               │
│         MCP Server (mcp_server/server.py)               │
│                                                         │
│  - FastMCP framework                                    │
│  - Tool decorators (@mcp.tool())                        │
│  - Resource decorators (@mcp.resource())                │
│  - Prompt definitions                                   │
│  - Data store                                           │
└─────────────────────────────────────────────────────────┘
```

## Component Details

### 1. MCP Server

**File**: `mcp_server/server.py`

**Responsibilities**:
- Provide callable tools
- Serve resources
- Manage data store
- Handle requests

**Tools Implementation**:
```python
@mcp.tool()
def add_numbers(a: float, b: float) -> dict:
    """Tool definition with automatic registration"""
```

**Resources Implementation**:
```python
@mcp.resource(uri_template="data://users/{user_id}")
def read_user_resource(user_id: str) -> str:
    """Resource handler with URI templates"""
```

**Data Store**:
```python
data_store = {
    "users": [...],
    "tasks": [...],
    "config": {...}
}
```

### 2. MCP Client

**File**: `mcp_client/client.py`

**Responsibilities**:
- Communicate with server
- Provide convenient API
- Handle errors
- Manage connections

**Architecture**:
- `MCPClient` class wraps HTTP client
- Methods for each tool and resource
- Context manager support
- Error handling with `MCPClientError`

**Internal Methods**:
- `_call_tool()` - Execute server tools
- `_read_resource()` - Read server resources

### 3. User Application

**File**: `user_app/app.py`

**Responsibilities**:
- Implement business logic
- Format output
- Coordinate user interactions
- Provide command-line interface

**Architecture**:
- `UserApplication` class
- Logical action methods
- Table formatting with tabulate
- CLI argument parsing

## Communication Flow

### Tool Call Flow

```
User App → Client.add_numbers(5, 3)
           ↓
         client._call_tool("add_numbers", {"a": 5, "b": 3})
           ↓
         HTTP POST /tools/add_numbers/execute
           ↓
         Server receives request
           ↓
         Server.add_numbers(5, 3) executed
           ↓
         Returns: {"operation": "addition", "a": 5, "b": 3, "result": 8}
           ↓
         Client receives JSON
           ↓
User App receives result
```

### Resource Read Flow

```
User App → Client.read_config_resource()
           ↓
         client._read_resource("data://config")
           ↓
         HTTP GET /resources/data://config
           ↓
         Server receives request
           ↓
         Server.read_config_resource() executed
           ↓
         Returns: {"app_name": "...", "version": "...", ...}
           ↓
         Client receives JSON
           ↓
User App receives result
```

## Data Flow Diagram

```
┌──────────────────┐
│ User Triggers    │
│ Action (e.g.,    │
│ "calc")          │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────┐
│ UserApplication.              │
│ perform_calculations()        │
└────────┬─────────────────────┘
         │
         ├─→ client.add_numbers(15, 27)
         │   ├─→ HTTP POST
         │   └─→ Returns {"result": 42}
         │
         ├─→ client.multiply_numbers(5, 4)
         │   ├─→ HTTP POST
         │   └─→ Returns {"result": 20}
         │
         └─→ client.calculate_statistics([...])
             ├─→ HTTP POST
             └─→ Returns {"mean": ..., "sum": ...}
                           │
                           ▼
                    ┌──────────────────┐
                    │ Format results   │
                    │ using tabulate   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Display to user  │
                    └──────────────────┘
```

## Class Hierarchies

### MCPClient

```
MCPClient
├── __init__(base_url)
├── __enter__() / __exit__()
├── close()
├── Mathematical Tools
│   ├── add_numbers(a, b)
│   ├── multiply_numbers(a, b)
│   └── calculate_statistics(numbers)
├── User Management
│   ├── get_user(user_id)
│   └── list_users()
├── Task Management
│   ├── get_tasks(filter_status)
│   └── create_task(title, assigned_to)
├── Resource Access
│   ├── read_user_resource(user_id)
│   ├── read_config_resource()
│   └── read_summary_resource()
└── Internal Methods
    ├── _call_tool(tool_name, params)
    └── _read_resource(uri)
```

### UserApplication

```
UserApplication
├── __init__(server_url)
├── __enter__() / __exit__()
├── close()
├── perform_calculations()
├── manage_users()
├── manage_tasks()
├── display_summary_and_config()
└── run_complete_workflow()
```

## Error Handling Architecture

```
┌─────────────────────────────────────────────┐
│         Error Flow                          │
└─────────────────────────────────────────────┘

HTTP Error in Client
    │
    ├─→ httpx.HTTPError
    │   └─→ Converted to MCPClientError
    │
    └─→ Propagated to Application
        └─→ Caught and handled gracefully
```

## Data Persistence

### Current Implementation (Demo)

- **Type**: In-memory dictionary
- **Persistence**: Session-only
- **Suitable for**: Development, testing, demos

```python
data_store = {
    "users": [...],
    "tasks": [...],
    "config": {...}
}
```

### Production Recommendations

- **Replace with**: Database (PostgreSQL, MongoDB, etc.)
- **ORM**: SQLAlchemy, Tortoise ORM
- **Caching**: Redis for frequently accessed data
- **Backup**: Regular database backups

## Security Architecture

### Current State
- No authentication
- No authorization
- HTTP only
- No rate limiting

### Recommended Enhancements

```python
# Authentication (use API keys or JWT)
@app.post("/auth/token")
async def login(credentials: Credentials) -> Token:
    # Validate credentials
    # Return JWT token

# Authorization (middleware)
@app.middleware("http")
async def verify_token(request: Request) -> Response:
    # Verify JWT token
    # Check permissions

# HTTPS/TLS
# Use SSL certificates in production

# Rate Limiting
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
```

## Scalability Considerations

### Horizontal Scaling

```
Multiple Clients ──┐
                   ├──→ Load Balancer ──→ Multiple Server Instances
Multiple Clients ──┘                        with shared database
```

### Vertical Scaling

- Async I/O for better concurrency
- Database optimization (indexing)
- Caching layer
- Connection pooling

## Testing Architecture

### Unit Tests

```
test_client.py
├── test_add_numbers()
├── test_multiply_numbers()
├── test_list_users()
└── test_get_tasks()

test_server.py
├── test_tool_add_numbers()
├── test_resource_user()
└── test_data_store()

test_app.py
├── test_perform_calculations()
├── test_manage_users()
└── test_manage_tasks()
```

### Integration Tests

```
test_integration.py
├── test_client_server_communication()
├── test_app_complete_workflow()
└── test_error_handling()
```

## Deployment Architecture

### Development

```
Developer Machine
├── mcp_server (port 8000)
├── mcp_client
└── user_app
```

### Production

```
Docker Network
├── nginx (reverse proxy, port 80/443)
├── FastAPI Server (port 8000, internal)
├── PostgreSQL Database
├── Redis Cache
└── Monitoring (Prometheus, Grafana)
```

## API Versioning

Current: v1 (implicit in URLs)

```
/tools/{tool_name}/execute
/resources/{resource_uri}
```

Future versioning:
```
/v1/tools/{tool_name}/execute
/v2/tools/{tool_name}/execute
```

## Logging Architecture

### Components

1. **Server Logging**
   - Request/response logging
   - Error logging
   - Tool execution logging

2. **Client Logging**
   - HTTP requests
   - Retries
   - Errors

3. **Application Logging**
   - User actions
   - Workflow progress
   - Errors

### Log Levels

- **DEBUG**: Development and detailed diagnostics
- **INFO**: General information
- **WARNING**: Warning messages
- **ERROR**: Error conditions
- **CRITICAL**: Critical failures

---

**Last Updated**: February 2026
**Architecture Version**: 1.0.0
