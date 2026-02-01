# User Application

A high-level application demonstrating how to use the MCP Client for business operations.

## Features

The application provides:

### Calculator Operations
- Perform arithmetic calculations (addition, multiplication)
- Analyze statistical data
- Display formatted results

### User Management
- List all users
- Access user resources
- Display user information in tables

### Task Management
- View all tasks
- Filter tasks by status
- Create new tasks
- Assign tasks to users

### Data Summary & Configuration
- View application configuration
- Display data summary with counts
- Monitor task completion metrics

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Run Complete Workflow

```bash
python app.py
```

### Run Specific Action

```bash
# Perform calculations
python app.py --action calc

# Manage users
python app.py --action users

# Manage tasks
python app.py --action tasks

# View summary and config
python app.py --action summary
```

### Custom Server URL

```bash
python app.py --server-url http://localhost:8000 --action all
```

## Architecture

The application follows a clean, layered architecture:

1. **Presentation Layer**: Formatted output using tables
2. **Business Logic Layer**: `UserApplication` class with methods for each domain
3. **Client Layer**: Uses `MCPClient` for server communication
4. **Data Layer**: MCP Server provides all data

## Prerequisites

- MCP Server must be running before starting this application
- Server should be accessible at the specified URL

## Example Output

The application displays:
- Mathematical calculations with results
- User information in formatted tables
- Task lists with status and assignments
- Application configuration and data metrics

## Error Handling

- Graceful error handling for server communication issues
- Informative error messages
- Proper resource cleanup with context managers
