# MCP Server

A comprehensive Model Context Protocol (MCP) server implementation using FastMCP.

## Features

### Tools
The server provides the following callable tools:

1. **Mathematical Tools**
   - `add_numbers(a, b)` - Add two numbers
   - `multiply_numbers(a, b)` - Multiply two numbers
   - `calculate_statistics(numbers)` - Calculate statistics for a list of numbers

2. **User Management Tools**
   - `get_user(user_id)` - Retrieve a specific user
   - `list_users()` - List all users

3. **Task Management Tools**
   - `get_tasks(filter_status)` - Get tasks with optional status filter
   - `create_task(title, assigned_to)` - Create a new task

### Resources
The server exposes the following resources:

1. `data://users/{user_id}` - User data resource
2. `data://config` - Application configuration
3. `data://summary` - Summary of all data

### Data
In-memory data store containing:
- Users with roles and contact information
- Tasks with status and assignment
- Application configuration

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python server.py
```

The server will start on `http://127.0.0.1:8000`

## Architecture

- Built with FastMCP framework
- Supports both tool calls and resource reading
- RESTful API endpoints
- In-memory data persistence (for demo purposes)

## Testing

Use the MCP client from `../mcp_client` to test this server.
