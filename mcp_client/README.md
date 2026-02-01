# MCP Client

A Python client for communicating with the MCP Server.

## Features

The client provides convenient methods for:

### Mathematical Tools
- `add_numbers(a, b)` - Add two numbers
- `multiply_numbers(a, b)` - Multiply two numbers
- `calculate_statistics(numbers)` - Calculate statistics

### User Management Tools
- `get_user(user_id)` - Retrieve a user
- `list_users()` - List all users

### Task Management Tools
- `get_tasks(filter_status)` - Get tasks with optional filtering
- `create_task(title, assigned_to)` - Create a new task

### Resource Access
- `read_user_resource(user_id)` - Read user as a resource
- `read_config_resource()` - Read configuration
- `read_summary_resource()` - Read data summary

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### As a Context Manager

```python
from client import MCPClient

with MCPClient() as client:
    # Call tools
    result = client.add_numbers(5, 3)
    
    # Manage users
    users = client.list_users()
    
    # Manage tasks
    tasks = client.get_tasks()
```

### Manual Management

```python
from client import MCPClient

client = MCPClient()
try:
    result = client.add_numbers(10, 20)
    print(result)
finally:
    client.close()
```

## Running the Demo

```bash
# First, make sure the server is running
# Then run:
python client.py
```

## Error Handling

The client raises `MCPClientError` for any communication issues. Always wrap calls in try-except blocks.

## Architecture

- Built with httpx for HTTP communication
- Type hints for better IDE support
- Context manager support for proper resource cleanup
- Comprehensive error handling
