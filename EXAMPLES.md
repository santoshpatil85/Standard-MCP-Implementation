# Usage Examples

Comprehensive examples of using the Standard MCP Implementation.

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [MCP Client Examples](#mcp-client-examples)
3. [User Application Examples](#user-application-examples)
4. [Advanced Usage](#advanced-usage)
5. [Error Handling](#error-handling)

## Basic Usage

### Starting the Server

```python
# mcp_server/server.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(mcp.app, host="127.0.0.1", port=8000)
```

Run:
```bash
cd mcp_server
python server.py
```

### Using the Client

```python
from mcp_client.client import MCPClient

# Create client
client = MCPClient("http://127.0.0.1:8000")

# Use as context manager (recommended)
with MCPClient() as client:
    result = client.add_numbers(10, 20)
    print(result)  # {"operation": "addition", "a": 10, "b": 20, "result": 30}
```

## MCP Client Examples

### Mathematical Operations

```python
from mcp_client.client import MCPClient

with MCPClient() as client:
    # Addition
    result = client.add_numbers(5, 3)
    print(f"5 + 3 = {result['result']}")
    
    # Multiplication
    result = client.multiply_numbers(4, 7)
    print(f"4 * 7 = {result['result']}")
    
    # Statistics
    numbers = [10, 20, 30, 40, 50]
    result = client.calculate_statistics(numbers)
    print(f"Mean: {result['mean']}")
    print(f"Sum: {result['sum']}")
    print(f"Min: {result['min']}")
    print(f"Max: {result['max']}")
```

Output:
```
5 + 3 = 8
4 * 7 = 28
Mean: 30.0
Sum: 150
Min: 10
Max: 50
```

### User Management

```python
from mcp_client.client import MCPClient
import json

with MCPClient() as client:
    # List all users
    result = client.list_users()
    print(f"Total users: {result['count']}")
    for user in result['users']:
        print(f"  - {user['name']} ({user['role']})")
    
    # Get specific user
    result = client.get_user(1)
    if result['success']:
        user = result['user']
        print(f"\nUser: {user['name']}")
        print(f"Email: {user['email']}")
        print(f"Role: {user['role']}")
    
    # Read user as resource
    result = client.read_user_resource(2)
    print("\nUser 2 (as resource):")
    print(json.dumps(result, indent=2))
```

Output:
```
Total users: 3
  - Alice (admin)
  - Bob (user)
  - Charlie (user)

User: Alice
Email: alice@example.com
Role: admin

User 2 (as resource):
{
  "id": 2,
  "name": "Bob",
  "email": "bob@example.com",
  "role": "user"
}
```

### Task Management

```python
from mcp_client.client import MCPClient

with MCPClient() as client:
    # Get all tasks
    result = client.get_tasks()
    print(f"Total tasks: {result['count']}")
    
    # Get tasks by status
    for status in ["completed", "in_progress", "pending"]:
        result = client.get_tasks(filter_status=status)
        print(f"\n{status.upper()}: {result['count']} tasks")
        for task in result['tasks']:
            print(f"  - {task['title']}")
    
    # Create new task
    result = client.create_task("Review code", assigned_to=1)
    if result['success']:
        task = result['task']
        print(f"\nTask created: {task['title']} (ID: {task['id']})")
```

Output:
```
Total tasks: 3

COMPLETED: 1 tasks
  - Implement MCP

IN_PROGRESS: 1 tasks
  - Create client

PENDING: 1 tasks
  - Write tests

Task created: Review code (ID: 4)
```

### Resource Access

```python
from mcp_client.client import MCPClient
import json

with MCPClient() as client:
    # Read config
    config = client.read_config_resource()
    print("Configuration:")
    print(json.dumps(config, indent=2))
    
    # Read summary
    summary = client.read_summary_resource()
    print("\nData Summary:")
    print(f"  Users: {summary['users_count']}")
    print(f"  Total Tasks: {summary['tasks_count']}")
    print(f"  Completed: {summary['completed_tasks']}")
    print(f"  In Progress: {summary['in_progress_tasks']}")
    print(f"  Pending: {summary['pending_tasks']}")
```

Output:
```
Configuration:
{
  "app_name": "MCP Sample Application",
  "version": "1.0.0",
  "debug": true
}

Data Summary:
  Users: 3
  Total Tasks: 3
  Completed: 1
  In Progress: 1
  Pending: 1
```

## User Application Examples

### Running Complete Workflow

```bash
cd user_app
python app.py
```

Displays:
- Calculator operations
- User management
- Task management
- Data summary and configuration

### Running Specific Actions

```bash
# Calculations only
python app.py --action calc

# Users only
python app.py --action users

# Tasks only
python app.py --action tasks

# Summary only
python app.py --action summary
```

### Custom Server URL

```bash
# Connect to different server
python app.py --server-url http://localhost:8001 --action all
```

### Using Application Programmatically

```python
from user_app.app import UserApplication

# Create application instance
app = UserApplication("http://127.0.0.1:8000")

try:
    # Perform calculations
    app.perform_calculations()
    
    # Manage users
    app.manage_users()
    
    # Manage tasks
    app.manage_tasks()
    
    # View summary
    app.display_summary_and_config()

finally:
    app.close()
```

Or with context manager:

```python
from user_app.app import UserApplication

with UserApplication() as app:
    app.run_complete_workflow()
```

## Advanced Usage

### Error Handling

```python
from mcp_client.client import MCPClient, MCPClientError

with MCPClient() as client:
    try:
        # Try to get non-existent user
        result = client.get_user(999)
        if not result['success']:
            print(f"Error: {result['error']}")
    
    except MCPClientError as e:
        print(f"Client error: {e}")
    
    except Exception as e:
        print(f"Unexpected error: {e}")
```

### Batch Operations

```python
from mcp_client.client import MCPClient

with MCPClient() as client:
    # Perform batch calculations
    test_cases = [
        (1, 2),
        (5, 10),
        (100, 50),
    ]
    
    results = []
    for a, b in test_cases:
        try:
            result = client.add_numbers(a, b)
            results.append({
                "inputs": (a, b),
                "result": result['result']
            })
        except Exception as e:
            print(f"Failed for {a}, {b}: {e}")
    
    # Display results
    for r in results:
        a, b = r['inputs']
        print(f"{a} + {b} = {r['result']}")
```

### Custom Application Logic

```python
from mcp_client.client import MCPClient
from tabulate import tabulate

class ReportGenerator:
    def __init__(self, client):
        self.client = client
    
    def generate_user_task_report(self):
        """Generate report of users and their tasks."""
        users = self.client.list_users()['users']
        tasks = self.client.get_tasks()['tasks']
        
        report_data = []
        for user in users:
            user_tasks = [t for t in tasks if t['assigned_to'] == user['id']]
            pending = sum(1 for t in user_tasks if t['status'] == 'pending')
            completed = sum(1 for t in user_tasks if t['status'] == 'completed')
            
            report_data.append([
                user['name'],
                len(user_tasks),
                pending,
                completed
            ])
        
        headers = ["User", "Total Tasks", "Pending", "Completed"]
        print(tabulate(report_data, headers=headers, tablefmt="grid"))

# Usage
with MCPClient() as client:
    gen = ReportGenerator(client)
    gen.generate_user_task_report()
```

Output:
```
┌─────────┬──────────────┬─────────┬───────────┐
│ User    │ Total Tasks  │ Pending │ Completed │
├─────────┼──────────────┼─────────┼───────────┤
│ Alice   │ 1            │ 0       │ 1         │
│ Bob     │ 1            │ 0       │ 1         │
│ Charlie │ 1            │ 1       │ 0         │
└─────────┴──────────────┴─────────┴───────────┘
```

### Data Analysis

```python
from mcp_client.client import MCPClient

def analyze_task_load(client):
    """Analyze task distribution and statistics."""
    users = client.list_users()['users']
    tasks = client.get_tasks()['tasks']
    
    task_counts = {}
    for user in users:
        count = sum(1 for t in tasks if t['assigned_to'] == user['id'])
        task_counts[user['name']] = count
    
    # Statistics
    counts = list(task_counts.values())
    avg = sum(counts) / len(counts)
    
    print(f"Task Load Analysis:")
    print(f"  Average tasks per user: {avg:.2f}")
    print(f"  Most loaded: {max(task_counts, key=task_counts.get)}")
    print(f"  Least loaded: {min(task_counts, key=task_counts.get)}")
    
    # Distribution
    for user, count in sorted(task_counts.items()):
        bar = '█' * count
        print(f"  {user}: {bar} ({count})")

with MCPClient() as client:
    analyze_task_load(client)
```

## API Response Examples

### Tool Responses

**Addition**:
```json
{
  "operation": "addition",
  "a": 5,
  "b": 3,
  "result": 8
}
```

**Statistics**:
```json
{
  "count": 5,
  "sum": 150,
  "mean": 30.0,
  "min": 10,
  "max": 50
}
```

**User List**:
```json
{
  "success": true,
  "count": 3,
  "users": [
    {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "admin"},
    {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "user"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com", "role": "user"}
  ]
}
```

**Task Creation**:
```json
{
  "success": true,
  "message": "Task created successfully",
  "task": {
    "id": 4,
    "title": "Review code",
    "status": "pending",
    "assigned_to": 1
  }
}
```

## Performance Examples

### Measuring Response Time

```python
import time
from mcp_client.client import MCPClient

with MCPClient() as client:
    start = time.time()
    result = client.list_users()
    elapsed = time.time() - start
    
    print(f"list_users() took {elapsed*1000:.2f}ms")
```

### Batch Processing Performance

```python
import time
from mcp_client.client import MCPClient

with MCPClient() as client:
    numbers_list = [
        [1, 2, 3, 4, 5],
        [10, 20, 30, 40, 50],
        [100, 200, 300, 400, 500]
    ]
    
    start = time.time()
    for numbers in numbers_list:
        client.calculate_statistics(numbers)
    elapsed = time.time() - start
    
    print(f"3 calls to calculate_statistics took {elapsed*1000:.2f}ms")
```

---

**Last Updated**: February 2026
**Examples Version**: 1.0.0
