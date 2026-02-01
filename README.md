# Standard MCP Implementation

A comprehensive, production-ready implementation of the Model Context Protocol (MCP) in Python using FastMCP.

## Overview

This workspace contains three separate projects demonstrating a complete MCP ecosystem:

1. **MCP Server** - Provides tools, resources, and data
2. **MCP Client** - Communicates with the server
3. **User Application** - High-level application using the client

## Project Structure

```
Standard-MCP-Implementation/
├── mcp_server/              # MCP Server implementation
│   ├── server.py           # Main server with tools, resources, prompts
│   ├── requirements.txt     # Python dependencies
│   └── README.md           # Server documentation
│
├── mcp_client/              # MCP Client implementation
│   ├── client.py           # Client class for server communication
│   ├── requirements.txt     # Python dependencies
│   └── README.md           # Client documentation
│
├── user_app/                # User-facing application
│   ├── app.py              # Application using the client
│   ├── requirements.txt     # Python dependencies
│   └── README.md           # Application documentation
│
├── README.md               # This file
├── ARCHITECTURE.md         # Detailed architecture documentation
├── SETUP.md                # Setup and installation guide
└── EXAMPLES.md             # Usage examples and code samples
```

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation & Running

1. **Start the MCP Server**

```bash
cd mcp_server
pip install -r requirements.txt
python server.py
```

The server will be available at `http://127.0.0.1:8000`

2. **Run the User Application** (in a new terminal)

```bash
cd user_app
pip install -r requirements.txt
python app.py
```

The application will interact with the server and display results.

## Features

### MCP Server Features

**Tools** (8 callable functions):
- `add_numbers(a, b)` - Mathematical addition
- `multiply_numbers(a, b)` - Mathematical multiplication
- `calculate_statistics(numbers)` - Statistical analysis
- `get_user(user_id)` - Retrieve user by ID
- `list_users()` - Get all users
- `get_tasks(filter_status)` - Get tasks with optional filtering
- `create_task(title, assigned_to)` - Create new task

**Resources** (3 readable resources):
- `data://users/{user_id}` - User data as resource
- `data://config` - Application configuration
- `data://summary` - Data summary and metrics

**Data**:
- 3 sample users with roles
- 3 sample tasks with various statuses
- Application configuration

### MCP Client Features

Convenient wrapper around server API:
- Context manager support
- Type hints for IDE support
- Comprehensive error handling
- All server tools and resources accessible

### User Application Features

High-level business operations:
- Calculator operations with formatted output
- User management and viewing
- Task management (view, create, filter)
- Data summary and configuration display
- Multiple action modes

## Documentation

- **[SETUP.md](SETUP.md)** - Installation and setup instructions
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Detailed system architecture
- **[EXAMPLES.md](EXAMPLES.md)** - Code examples and usage patterns

## Component READMEs

- **[mcp_server/README.md](mcp_server/README.md)** - Server documentation
- **[mcp_client/README.md](mcp_client/README.md)** - Client documentation
- **[user_app/README.md](user_app/README.md)** - Application documentation

## Architecture Overview

```
┌─────────────────────────────────────┐
│      User Application               │
│  (Business Logic & Presentation)    │
└──────────────┬──────────────────────┘
               │
               │ HTTP (httpx)
               ▼
┌─────────────────────────────────────┐
│       MCP Client                    │
│  (Communication & Interface)        │
└──────────────┬──────────────────────┘
               │
               │ HTTP/REST
               ▼
┌─────────────────────────────────────┐
│       MCP Server                    │
│  (Tools, Resources, Data)           │
│                                     │
│  - Mathematical tools               │
│  - User management tools            │
│  - Task management tools            │
│  - Data resources                   │
│  - In-memory data store             │
└─────────────────────────────────────┘
```

## Technologies Used

- **FastMCP**: MCP server framework
- **httpx**: HTTP client library
- **Pydantic**: Data validation
- **Tabulate**: Formatted table output
- **Python 3.8+**: Core language

## Data Model

### User
```json
{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com",
  "role": "admin"
}
```

### Task
```json
{
  "id": 1,
  "title": "Implement MCP",
  "status": "completed",
  "assigned_to": 1
}
```

## Usage Example

### Using the Client Directly

```python
from mcp_client.client import MCPClient

with MCPClient() as client:
    # Call a tool
    result = client.add_numbers(5, 3)
    print(result)  # {"operation": "addition", "a": 5, "b": 3, "result": 8}
    
    # List users
    users = client.list_users()
    print(users)
    
    # Create a task
    task = client.create_task("New task", assigned_to=1)
    print(task)
```

### Running the User Application

```bash
# Run complete workflow
python app.py

# Run specific action
python app.py --action calc   # Just calculations
python app.py --action users  # Just users
python app.py --action tasks  # Just tasks
python app.py --action summary # Just summary
```

## Performance Considerations

- Server uses in-memory storage (suitable for demos)
- HTTP communication adds latency
- Consider caching in client for repeated requests
- For production, replace in-memory storage with database

## Security Considerations

Currently demonstrates:
- ❌ No authentication/authorization
- ❌ No input validation (beyond types)
- ❌ No rate limiting
- ❌ No HTTPS

For production, add:
- ✓ API key authentication
- ✓ Input validation and sanitization
- ✓ Rate limiting
- ✓ HTTPS/TLS
- ✓ CORS configuration
- ✓ Request logging and monitoring

## Next Steps

1. Read [SETUP.md](SETUP.md) for detailed installation
2. Read [EXAMPLES.md](EXAMPLES.md) for usage patterns
3. Read [ARCHITECTURE.md](ARCHITECTURE.md) for system design
4. Explore the source code
5. Modify and extend components
6. Add your own tools and resources

## License

This is a sample implementation for educational purposes.

## Contributing

This is a reference implementation. Feel free to use it as a template for your own MCP implementations.

## Support

For questions about MCP:
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://fastmcp.readthedocs.io/)

---

**Last Updated**: February 2026
**Version**: 1.0.0
