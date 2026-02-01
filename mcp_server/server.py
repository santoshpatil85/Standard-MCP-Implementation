"""
MCP Server Implementation using FastMCP

This server provides:
- Tools: Mathematical operations and data processing
- Resources: File-like resources with text content
- Data: Structured data endpoints
"""

import json
from typing import Any
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("sample_mcp_server")

# In-memory data store
data_store = {
    "users": [
        {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "admin"},
        {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "user"},
        {"id": 3, "name": "Charlie", "email": "charlie@example.com", "role": "user"},
    ],
    "tasks": [
        {"id": 1, "title": "Implement MCP", "status": "completed", "assigned_to": 1},
        {"id": 2, "title": "Create client", "status": "in_progress", "assigned_to": 2},
        {"id": 3, "title": "Write tests", "status": "pending", "assigned_to": 3},
    ],
    "config": {
        "app_name": "MCP Sample Application",
        "version": "1.0.0",
        "debug": True
    }
}


# ========================
# TOOLS: Callable functions
# ========================

@mcp.tool()
def add_numbers(a: float, b: float) -> dict:
    """Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Dictionary with result and operation details
    """
    result = a + b
    return {
        "operation": "addition",
        "a": a,
        "b": b,
        "result": result
    }


@mcp.tool()
def multiply_numbers(a: float, b: float) -> dict:
    """Multiply two numbers.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Dictionary with result and operation details
    """
    result = a * b
    return {
        "operation": "multiplication",
        "a": a,
        "b": b,
        "result": result
    }


@mcp.tool()
def calculate_statistics(numbers: list) -> dict:
    """Calculate statistics for a list of numbers.
    
    Args:
        numbers: List of numbers
        
    Returns:
        Dictionary with statistical measures
    """
    if not numbers:
        return {"error": "Empty list provided"}
    
    total = sum(numbers)
    count = len(numbers)
    mean = total / count
    min_val = min(numbers)
    max_val = max(numbers)
    
    return {
        "count": count,
        "sum": total,
        "mean": mean,
        "min": min_val,
        "max": max_val
    }


@mcp.tool()
def get_user(user_id: int) -> dict:
    """Retrieve a user by ID.
    
    Args:
        user_id: The ID of the user
        
    Returns:
        User dictionary or error message
    """
    for user in data_store["users"]:
        if user["id"] == user_id:
            return {"success": True, "user": user}
    
    return {"success": False, "error": f"User {user_id} not found"}


@mcp.tool()
def list_users() -> dict:
    """List all users.
    
    Returns:
        Dictionary with list of all users
    """
    return {
        "success": True,
        "count": len(data_store["users"]),
        "users": data_store["users"]
    }


@mcp.tool()
def get_tasks(filter_status: str = None) -> dict:
    """Get tasks, optionally filtered by status.
    
    Args:
        filter_status: Optional status filter (completed, in_progress, pending)
        
    Returns:
        Dictionary with filtered tasks
    """
    tasks = data_store["tasks"]
    
    if filter_status:
        tasks = [t for t in tasks if t["status"] == filter_status]
    
    return {
        "success": True,
        "count": len(tasks),
        "tasks": tasks
    }


@mcp.tool()
def create_task(title: str, assigned_to: int) -> dict:
    """Create a new task.
    
    Args:
        title: Task title
        assigned_to: User ID to assign the task to
        
    Returns:
        Created task or error message
    """
    # Check if user exists
    user_exists = any(u["id"] == assigned_to for u in data_store["users"])
    if not user_exists:
        return {"success": False, "error": f"User {assigned_to} not found"}
    
    new_id = max(t["id"] for t in data_store["tasks"]) + 1
    new_task = {
        "id": new_id,
        "title": title,
        "status": "pending",
        "assigned_to": assigned_to
    }
    
    data_store["tasks"].append(new_task)
    
    return {
        "success": True,
        "message": "Task created successfully",
        "task": new_task
    }


# ========================
# RESOURCES: File-like content
# ========================

@mcp.resource("data://users/list")
def read_users_resource() -> str:
    """Read all users as a resource.
    
    Returns:
        JSON formatted users list
    """
    return json.dumps({
        "count": len(data_store["users"]),
        "users": data_store["users"]
    }, indent=2)


@mcp.resource("data://config")
def read_config_resource() -> str:
    """Read application configuration as a resource.
    
    Returns:
        JSON formatted configuration
    """
    return json.dumps(data_store["config"], indent=2)


@mcp.resource("data://summary")
def read_summary_resource() -> str:
    """Read a summary of all data as a resource.
    
    Returns:
        JSON formatted summary
    """
    summary = {
        "users_count": len(data_store["users"]),
        "tasks_count": len(data_store["tasks"]),
        "completed_tasks": sum(1 for t in data_store["tasks"] if t["status"] == "completed"),
        "pending_tasks": sum(1 for t in data_store["tasks"] if t["status"] == "pending"),
        "in_progress_tasks": sum(1 for t in data_store["tasks"] if t["status"] == "in_progress"),
        "application": data_store["config"]["app_name"]
    }
    return json.dumps(summary, indent=2)


# ========================
# PROMPTS: Multi-turn guidance
# ========================

@mcp.prompt()
def task_summary_prompt() -> str:
    """Provide a prompt for task summary analysis."""
    return """You are a task management assistant. 
    Analyze the task list and provide insights about:
    1. Overall progress
    2. Tasks by status
    3. Workload distribution among users
    4. Recommendations for improvement"""


# ========================
# REST API ENDPOINTS (wrapper layer for client compatibility)
# ========================
# These endpoints are added after getting the HTTP app

def setup_rest_endpoints(app):
    """Setup REST endpoints for the Starlette app."""
    from starlette.routing import Route
    from starlette.requests import Request
    from starlette.responses import JSONResponse
    
    async def execute_tool(request: Request):
        """Execute a tool via REST API."""
        try:
            # Extract tool_name from path
            path_parts = request.url.path.split('/')
            tool_name = path_parts[-2] if len(path_parts) >= 3 else None
            
            if not tool_name:
                return JSONResponse({"error": "Tool name required"}, status_code=400)
            
            params = await request.json()
            
            # Get the tool from mcp's tool manager
            if tool_name not in mcp._tool_manager._tools:
                return JSONResponse({"error": f"Tool '{tool_name}' not found"}, status_code=404)
            
            tool_obj = mcp._tool_manager._tools[tool_name]
            # Call the tool using its .fn attribute
            result = tool_obj.fn(**params)
            return JSONResponse(result)
        except TypeError as e:
            return JSONResponse({"error": f"Invalid parameters: {str(e)}"}, status_code=400)
        except Exception as e:
            return JSONResponse({"error": f"Error executing tool: {str(e)}"}, status_code=500)
    
    
    async def read_resource(request: Request):
        """Read a resource via REST API."""
        try:
            # Extract resource path from URL
            path_parts = request.url.path.split('/api/resources/', 1)
            resource_path = path_parts[-1] if len(path_parts) > 1 else None
            
            if not resource_path:
                return JSONResponse({"error": "Resource path required"}, status_code=400)
            
            resource_uri = f"data://{resource_path}"
            
            # Get resource from mcp's resource manager
            if resource_uri not in mcp._resource_manager._resources:
                return JSONResponse({"error": f"Resource '{resource_uri}' not found"}, status_code=404)
            
            resource_obj = mcp._resource_manager._resources[resource_uri]
            # Call the resource using its .fn attribute
            content = resource_obj.fn()
            
            # Parse the JSON content returned from resources
            return JSONResponse(json.loads(content))
        except json.JSONDecodeError:
            return JSONResponse({"error": "Error parsing resource content"}, status_code=500)
        except Exception as e:
            return JSONResponse({"error": f"Error reading resource: {str(e)}"}, status_code=500)
    
    
    async def health_check(request: Request):
        """Health check endpoint."""
        return JSONResponse({"status": "healthy", "server": "sample_mcp_server"})
    
    # Add routes using app.router.add_route
    app.router.routes.append(
        Route("/api/tools/{tool_name}/execute", execute_tool, methods=["POST"])
    )
    app.router.routes.append(
        Route("/api/resources/{resource_path:path}", read_resource, methods=["GET"])
    )
    app.router.routes.append(
        Route("/health", health_check, methods=["GET"])
    )


if __name__ == "__main__":
    # Run the server using mcp.http_app() and uvicorn
    # This exposes tools, resources, and data over HTTP transport
    import uvicorn
    
    # Create the HTTP app from FastMCP
    # This properly sets up all MCP tools, resources, and endpoints
    app = mcp.http_app()
    
    # Add REST wrapper endpoints for backward compatibility
    setup_rest_endpoints(app)
    
    # Run with uvicorn for HTTP serving
    # The mcp.http_app() handles all MCP protocol setup
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
