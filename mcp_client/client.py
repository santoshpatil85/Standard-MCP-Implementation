"""
MCP Client Implementation

This client communicates with the MCP Server to:
- Call tools (mathematical operations, user management, task management)
- Read resources (user data, configuration, summaries)
- Handle responses and error cases
"""

import httpx
import json
from typing import Any, Optional, Dict, List
from enum import Enum


class MCPClientError(Exception):
    """Custom exception for MCP Client errors."""
    pass


class MCPClient:
    """Client for communicating with MCP Server."""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        """
        Initialize the MCP Client.
        
        Args:
            base_url: Base URL of the MCP Server
        """
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(base_url=self.base_url)
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
    
    def close(self):
        """Close the HTTP client."""
        self.client.close()
    
    # ========================
    # MATHEMATICAL TOOLS
    # ========================
    
    def add_numbers(self, a: float, b: float) -> Dict[str, Any]:
        """
        Call the add_numbers tool.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Tool response with result
            
        Raises:
            MCPClientError: If the tool call fails
        """
        return self._call_tool("add_numbers", {"a": a, "b": b})
    
    def multiply_numbers(self, a: float, b: float) -> Dict[str, Any]:
        """
        Call the multiply_numbers tool.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Tool response with result
            
        Raises:
            MCPClientError: If the tool call fails
        """
        return self._call_tool("multiply_numbers", {"a": a, "b": b})
    
    def calculate_statistics(self, numbers: List[float]) -> Dict[str, Any]:
        """
        Call the calculate_statistics tool.
        
        Args:
            numbers: List of numbers for statistical analysis
            
        Returns:
            Tool response with statistics
            
        Raises:
            MCPClientError: If the tool call fails
        """
        return self._call_tool("calculate_statistics", {"numbers": numbers})
    
    # ========================
    # USER MANAGEMENT TOOLS
    # ========================
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        """
        Retrieve a user by ID.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            Tool response with user data
            
        Raises:
            MCPClientError: If the tool call fails
        """
        return self._call_tool("get_user", {"user_id": user_id})
    
    def list_users(self) -> Dict[str, Any]:
        """
        List all users.
        
        Returns:
            Tool response with list of users
            
        Raises:
            MCPClientError: If the tool call fails
        """
        return self._call_tool("list_users", {})
    
    # ========================
    # TASK MANAGEMENT TOOLS
    # ========================
    
    def get_tasks(self, filter_status: Optional[str] = None) -> Dict[str, Any]:
        """
        Get tasks with optional status filter.
        
        Args:
            filter_status: Optional status filter (completed, in_progress, pending)
            
        Returns:
            Tool response with tasks
            
        Raises:
            MCPClientError: If the tool call fails
        """
        params = {}
        if filter_status:
            params["filter_status"] = filter_status
        
        return self._call_tool("get_tasks", params)
    
    def create_task(self, title: str, assigned_to: int) -> Dict[str, Any]:
        """
        Create a new task.
        
        Args:
            title: Task title
            assigned_to: User ID to assign the task to
            
        Returns:
            Tool response with created task
            
        Raises:
            MCPClientError: If the tool call fails
        """
        return self._call_tool("create_task", {"title": title, "assigned_to": assigned_to})
    
    # ========================
    # RESOURCE ACCESS
    # ========================
    
    def read_users_resource(self) -> Dict[str, Any]:
        """
        Read all users data as a resource.
        
        Returns:
            Users data as JSON
            
        Raises:
            MCPClientError: If reading the resource fails
        """
        uri = "data://users/list"
        return self._read_resource(uri)
    
    def read_config_resource(self) -> Dict[str, Any]:
        """
        Read application configuration as a resource.
        
        Returns:
            Configuration data as JSON
            
        Raises:
            MCPClientError: If reading the resource fails
        """
        uri = "data://config"
        return self._read_resource(uri)
    
    def read_summary_resource(self) -> Dict[str, Any]:
        """
        Read a summary of all data as a resource.
        
        Returns:
            Summary data as JSON
            
        Raises:
            MCPClientError: If reading the resource fails
        """
        uri = "data://summary"
        return self._read_resource(uri)
    
    # ========================
    # INTERNAL METHODS
    # ========================
    
    def _call_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a tool on the MCP Server.
        
        Args:
            tool_name: Name of the tool to call
            params: Parameters for the tool
            
        Returns:
            Tool response
            
        Raises:
            MCPClientError: If the tool call fails
        """
        try:
            response = self.client.post(
                f"/api/tools/{tool_name}/execute",
                json=params
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise MCPClientError(f"Failed to call tool '{tool_name}': {str(e)}")
        except Exception as e:
            raise MCPClientError(f"Unexpected error calling tool '{tool_name}': {str(e)}")
    
    def _read_resource(self, uri: str) -> Dict[str, Any]:
        """
        Read a resource from the MCP Server.
        
        Args:
            uri: Resource URI
            
        Returns:
            Resource content as JSON
            
        Raises:
            MCPClientError: If reading the resource fails
        """
        try:
            # Extract the resource path from the URI (e.g., "data://users/list" -> "users/list")
            resource_path = uri.replace("data://", "")
            response = self.client.get(
                f"/api/resources/{resource_path}",
            )
            response.raise_for_status()
            # Try to parse as JSON
            try:
                return response.json()
            except json.JSONDecodeError:
                # If not valid JSON, return as text in a wrapper
                return {"content": response.text}
        except httpx.HTTPError as e:
            raise MCPClientError(f"Failed to read resource '{uri}': {str(e)}")
        except Exception as e:
            raise MCPClientError(f"Unexpected error reading resource '{uri}': {str(e)}")


def demo():
    """Demonstrate client usage."""
    print("=" * 60)
    print("MCP Client Demo")
    print("=" * 60)
    
    try:
        with MCPClient() as client:
            # Mathematical operations
            print("\n--- Mathematical Tools ---")
            print("Adding 5 + 3:")
            result = client.add_numbers(5, 3)
            print(f"Result: {json.dumps(result, indent=2)}")
            
            print("\nMultiplying 4 * 7:")
            result = client.multiply_numbers(4, 7)
            print(f"Result: {json.dumps(result, indent=2)}")
            
            print("\nCalculating statistics for [1, 2, 3, 4, 5]:")
            result = client.calculate_statistics([1, 2, 3, 4, 5])
            print(f"Result: {json.dumps(result, indent=2)}")
            
            # User management
            print("\n--- User Management ---")
            print("Listing all users:")
            result = client.list_users()
            print(f"Result: {json.dumps(result, indent=2)}")
            
            print("\nGetting user 1:")
            result = client.get_user(1)
            print(f"Result: {json.dumps(result, indent=2)}")
            
            # Task management
            print("\n--- Task Management ---")
            print("Getting all tasks:")
            result = client.get_tasks()
            print(f"Result: {json.dumps(result, indent=2)}")
            
            print("\nGetting pending tasks:")
            result = client.get_tasks(filter_status="pending")
            print(f"Result: {json.dumps(result, indent=2)}")
            
            print("\nCreating new task:")
            result = client.create_task("Setup testing environment", assigned_to=1)
            print(f"Result: {json.dumps(result, indent=2)}")
            
            # Resource access
            print("\n--- Resource Access ---")
            print("Reading config resource:")
            result = client.read_config_resource()
            print(f"Result: {json.dumps(result, indent=2)}")
            
            print("\nReading summary resource:")
            result = client.read_summary_resource()
            print(f"Result: {json.dumps(result, indent=2)}")
            
    except MCPClientError as e:
        print(f"Client error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    demo()
