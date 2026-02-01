# Integration & Extension Guide

Guide for integrating and extending the MCP system.

## Table of Contents

1. [Adding New Tools](#adding-new-tools)
2. [Adding New Resources](#adding-new-resources)
3. [Integrating with External Services](#integrating-with-external-services)
4. [Custom Data Models](#custom-data-models)
5. [Production Deployment](#production-deployment)

## Adding New Tools

### Step 1: Define Tool in Server

Add to `mcp_server/server.py`:

```python
@mcp.tool()
def process_text(text: str, operation: str) -> dict:
    """Process text with specified operation.
    
    Args:
        text: Text to process
        operation: "uppercase", "lowercase", or "reverse"
        
    Returns:
        Processed text result
    """
    if operation == "uppercase":
        result = text.upper()
    elif operation == "lowercase":
        result = text.lower()
    elif operation == "reverse":
        result = text[::-1]
    else:
        return {"error": f"Unknown operation: {operation}"}
    
    return {
        "success": True,
        "original": text,
        "operation": operation,
        "result": result
    }
```

### Step 2: Add Method to Client

Add to `mcp_client/client.py`:

```python
def process_text(self, text: str, operation: str) -> Dict[str, Any]:
    """Process text with specified operation.
    
    Args:
        text: Text to process
        operation: Operation type
        
    Returns:
        Processed result
        
    Raises:
        MCPClientError: If the tool call fails
    """
    return self._call_tool("process_text", {
        "text": text,
        "operation": operation
    })
```

### Step 3: Use in Application

Add to `user_app/app.py`:

```python
def process_text_demo(self):
    """Demonstrate text processing."""
    print("\n--- Text Processing ---")
    operations = ["uppercase", "lowercase", "reverse"]
    text = "Hello World"
    
    for op in operations:
        result = self.client.process_text(text, op)
        if result['success']:
            print(f"{op}: {result['result']}")
```

## Adding New Resources

### Step 1: Define Resource in Server

Add to `mcp_server/server.py`:

```python
@mcp.resource(uri_template="data://stats")
def read_stats_resource() -> str:
    """Read application statistics as a resource.
    
    Returns:
        JSON formatted statistics
    """
    stats = {
        "total_requests": 1000,
        "successful_requests": 950,
        "failed_requests": 50,
        "average_response_time": 45.2,
        "uptime_hours": 168
    }
    return json.dumps(stats, indent=2)
```

### Step 2: Add Method to Client

Add to `mcp_client/client.py`:

```python
def read_stats_resource(self) -> Dict[str, Any]:
    """Read application statistics as a resource.
    
    Returns:
        Statistics data as JSON
        
    Raises:
        MCPClientError: If reading the resource fails
    """
    uri = "data://stats"
    return self._read_resource(uri)
```

### Step 3: Use in Application

Add to `user_app/app.py`:

```python
def display_stats(self):
    """Display application statistics."""
    print("\n--- Application Statistics ---")
    stats = self.client.read_stats_resource()
    stats_data = [["Metric", "Value"]]
    for key, value in stats.items():
        stats_data.append([key, str(value)])
    print(tabulate(stats_data, headers="firstrow", tablefmt="grid"))
```

## Integrating with External Services

### Example: Database Integration

**Modify Server for Database:**

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker

# Create database connection
engine = create_engine("postgresql://user:pass@localhost/mcp_db")
Session = sessionmaker(bind=engine)

@mcp.tool()
def save_task(title: str, assigned_to: int) -> dict:
    """Save task to database."""
    session = Session()
    try:
        # Instead of data_store
        new_task = TaskModel(title=title, assigned_to=assigned_to, status="pending")
        session.add(new_task)
        session.commit()
        
        return {
            "success": True,
            "task_id": new_task.id
        }
    except Exception as e:
        session.rollback()
        return {"success": False, "error": str(e)}
    finally:
        session.close()
```

### Example: REST API Integration

```python
import httpx

@mcp.tool()
def fetch_weather(city: str) -> dict:
    """Fetch weather from external API."""
    try:
        response = httpx.get(
            "https://api.weather.example.com/current",
            params={"city": city}
        )
        response.raise_for_status()
        data = response.json()
        
        return {
            "success": True,
            "city": city,
            "temperature": data["temp"],
            "condition": data["condition"]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
```

### Example: Authentication Integration

```python
import jwt

def verify_token(token: str) -> bool:
    """Verify JWT token."""
    try:
        jwt.decode(token, "secret_key", algorithms=["HS256"])
        return True
    except:
        return False

@mcp.tool()
def protected_operation(token: str, data: str) -> dict:
    """Operation requiring authentication."""
    if not verify_token(token):
        return {"success": False, "error": "Invalid token"}
    
    # Perform operation
    return {"success": True, "result": "Operation completed"}
```

## Custom Data Models

### Using Pydantic Models

```python
from pydantic import BaseModel, validator
from typing import List

class User(BaseModel):
    """User model with validation."""
    id: int
    name: str
    email: str
    role: str
    
    @validator("email")
    def email_valid(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email")
        return v
    
    @validator("role")
    def role_valid(cls, v):
        if v not in ["admin", "user"]:
            raise ValueError("Invalid role")
        return v

class Task(BaseModel):
    """Task model with validation."""
    id: int
    title: str
    status: str
    assigned_to: int
    
    @validator("status")
    def status_valid(cls, v):
        if v not in ["pending", "in_progress", "completed"]:
            raise ValueError("Invalid status")
        return v

# Use in server tools
@mcp.tool()
def create_user(name: str, email: str, role: str) -> dict:
    """Create user with validation."""
    try:
        user = User(id=4, name=name, email=email, role=role)
        # Save user...
        return {"success": True, "user": user.dict()}
    except ValueError as e:
        return {"success": False, "error": str(e)}
```

## Async/Concurrent Operations

### Async Tool Implementation

```python
import asyncio

@mcp.tool()
async def batch_calculate(operations: List[tuple]) -> dict:
    """Calculate multiple operations concurrently."""
    
    async def calculate_one(a, b, op):
        await asyncio.sleep(0.1)  # Simulate work
        if op == "add":
            return a + b
        elif op == "multiply":
            return a * b
    
    tasks = [
        calculate_one(a, b, op) 
        for a, b, op in operations
    ]
    
    results = await asyncio.gather(*tasks)
    return {"results": results}
```

## Caching Strategy

### Client-Side Caching

```python
from functools import lru_cache
import time

class CachingMCPClient(MCPClient):
    """Client with caching support."""
    
    def __init__(self, base_url: str, cache_ttl: int = 300):
        super().__init__(base_url)
        self.cache_ttl = cache_ttl
        self._cache = {}
        self._cache_times = {}
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        """Get user with caching."""
        cache_key = f"user_{user_id}"
        
        # Check cache
        if cache_key in self._cache:
            if time.time() - self._cache_times[cache_key] < self.cache_ttl:
                return self._cache[cache_key]
        
        # Fetch from server
        result = super().get_user(user_id)
        
        # Update cache
        self._cache[cache_key] = result
        self._cache_times[cache_key] = time.time()
        
        return result
```

## Error Handling Enhancements

### Custom Exception Hierarchy

```python
class MCPException(Exception):
    """Base MCP exception."""
    pass

class MCPConnectionError(MCPException):
    """Connection error."""
    pass

class MCPAuthenticationError(MCPException):
    """Authentication failed."""
    pass

class MCPValidationError(MCPException):
    """Data validation failed."""
    pass

# Use in client
def _call_tool(self, tool_name: str, params: Dict) -> Dict:
    try:
        response = self.client.post(f"/tools/{tool_name}/execute", json=params)
        response.raise_for_status()
        return response.json()
    except httpx.ConnectError:
        raise MCPConnectionError(f"Cannot connect to server")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise MCPAuthenticationError("Invalid credentials")
        raise MCPValidationError(f"Validation error: {e}")
```

## Logging Configuration

### Server Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('server.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@mcp.tool()
def logged_operation(data: str) -> dict:
    """Operation with logging."""
    logger.info(f"Starting operation with data: {data}")
    try:
        result = process(data)
        logger.info(f"Operation successful, result: {result}")
        return {"success": True, "result": result}
    except Exception as e:
        logger.error(f"Operation failed: {e}")
        return {"success": False, "error": str(e)}
```

## Testing Integration

### Unit Tests for Tools

```python
import pytest
from mcp_server.server import add_numbers, create_task

def test_add_numbers():
    result = add_numbers(5, 3)
    assert result["result"] == 8
    assert result["operation"] == "addition"

def test_create_task():
    result = create_task("Test", 1)
    assert result["success"] is True
    assert result["task"]["title"] == "Test"

def test_create_task_invalid_user():
    result = create_task("Test", 999)
    assert result["success"] is False
```

### Integration Tests

```python
def test_client_server_integration():
    from mcp_client.client import MCPClient
    
    with MCPClient() as client:
        result = client.add_numbers(10, 20)
        assert result["result"] == 30
        
        users = client.list_users()
        assert users["count"] > 0
```

## Production Deployment

### Docker Deployment

**Dockerfile**:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY mcp_server /app/mcp_server
COPY requirements.txt /app/mcp_server/

RUN pip install -r mcp_server/requirements.txt

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "mcp_server.server:mcp.app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml**:
```yaml
version: '3.8'
services:
  mcp-server:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - LOG_LEVEL=info
    volumes:
      - ./logs:/app/logs

  postgres:
    image: postgres:14
    environment:
      - POSTGRES_DB=mcp_db
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"
```

### Environment Configuration

**.env**:
```
# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=False
LOG_LEVEL=info

# Database
DATABASE_URL=postgresql://user:pass@localhost/mcp_db

# Authentication
JWT_SECRET=your-secret-key

# External Services
WEATHER_API_KEY=your-api-key
```

### Health Check

```python
@mcp.tool()
def health_check() -> dict:
    """Check server health."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
```

## Performance Optimization

### Batch Operations

```python
@mcp.tool()
def batch_add(pairs: List[tuple]) -> dict:
    """Perform multiple additions."""
    results = [a + b for a, b in pairs]
    return {
        "count": len(results),
        "results": results
    }
```

### Pagination

```python
@mcp.tool()
def list_users_paginated(page: int = 1, limit: int = 10) -> dict:
    """List users with pagination."""
    users = data_store["users"]
    start = (page - 1) * limit
    end = start + limit
    
    return {
        "page": page,
        "limit": limit,
        "total": len(users),
        "users": users[start:end]
    }
```

---

**Version**: 1.0.0
**Last Updated**: February 2026
