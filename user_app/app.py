"""
User Application

A high-level application that uses the MCP Client to:
- Perform business logic operations
- Display formatted results
- Interact with the MCP Server through the client
"""

import sys
from pathlib import Path
from typing import List, Dict, Any
from tabulate import tabulate
import json

# Add parent directory to path to import mcp_client
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_client.client import MCPClient, MCPClientError


class UserApplication:
    """High-level application using MCP Client."""
    
    def __init__(self, server_url: str = "http://127.0.0.1:8000"):
        """
        Initialize the User Application.
        
        Args:
            server_url: URL of the MCP Server
        """
        self.client = MCPClient(base_url=server_url)
    
    def close(self):
        """Close the client connection."""
        self.client.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
    
    # ========================
    # CALCULATOR OPERATIONS
    # ========================
    
    def perform_calculations(self):
        """Perform and display various mathematical calculations."""
        print("\n" + "=" * 60)
        print("CALCULATOR OPERATIONS")
        print("=" * 60)
        
        try:
            # Simple addition
            print("\n[Addition]")
            print("Computing: 15 + 27")
            result = self.client.add_numbers(15, 27)
            print(f"Result: {result['result']}")
            
            # Multiple multiplications
            print("\n[Multiplications]")
            operations = [(5, 4), (12, 3), (100, 2.5)]
            for a, b in operations:
                result = self.client.multiply_numbers(a, b)
                print(f"  {a} × {b} = {result['result']}")
            
            # Statistical analysis
            print("\n[Statistical Analysis]")
            numbers = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
            result = self.client.calculate_statistics(numbers)
            stats_data = [
                ["Metric", "Value"],
                ["Count", result["count"]],
                ["Sum", result["sum"]],
                ["Mean", result["mean"]],
                ["Min", result["min"]],
                ["Max", result["max"]],
            ]
            print(tabulate(stats_data, headers="firstrow", tablefmt="grid"))
            
        except MCPClientError as e:
            print(f"Error: {e}")
    
    # ========================
    # USER MANAGEMENT
    # ========================
    
    def manage_users(self):
        """Retrieve and display user information."""
        print("\n" + "=" * 60)
        print("USER MANAGEMENT")
        print("=" * 60)
        
        try:
            # List all users
            print("\n[All Users]")
            result = self.client.list_users()
            
            users_data = [["ID", "Name", "Email", "Role"]]
            for user in result["users"]:
                users_data.append([
                    user["id"],
                    user["name"],
                    user["email"],
                    user["role"]
                ])
            
            print(tabulate(users_data, headers="firstrow", tablefmt="grid"))
            
            # List all users and read as resource
            print("\n[Users (via Resource)]")
            result = self.client.read_users_resource()
            print("Users Resource:")
            print(json.dumps(result, indent=2))
            
        except MCPClientError as e:
            print(f"Error: {e}")
    
    # ========================
    # TASK MANAGEMENT
    # ========================
    
    def manage_tasks(self):
        """Manage and display task information."""
        print("\n" + "=" * 60)
        print("TASK MANAGEMENT")
        print("=" * 60)
        
        try:
            # Get all tasks
            print("\n[All Tasks]")
            result = self.client.get_tasks()
            
            tasks_data = [["ID", "Title", "Status", "Assigned To"]]
            for task in result["tasks"]:
                tasks_data.append([
                    task["id"],
                    task["title"],
                    task["status"],
                    task["assigned_to"]
                ])
            
            print(tabulate(tasks_data, headers="firstrow", tablefmt="grid"))
            
            # Get tasks by status
            print("\n[Tasks by Status]")
            statuses = ["completed", "in_progress", "pending"]
            
            for status in statuses:
                result = self.client.get_tasks(filter_status=status)
                print(f"\n  {status.upper()}: {result['count']} task(s)")
                for task in result["tasks"]:
                    print(f"    - {task['title']}")
            
            # Create a new task
            print("\n[Create New Task]")
            new_task = self.client.create_task(
                title="Integrate MCP into production",
                assigned_to=2
            )
            if new_task["success"]:
                task = new_task["task"]
                print(f"✓ Task created successfully")
                print(f"  ID: {task['id']}")
                print(f"  Title: {task['title']}")
                print(f"  Status: {task['status']}")
                print(f"  Assigned to user: {task['assigned_to']}")
            
        except MCPClientError as e:
            print(f"Error: {e}")
    
    # ========================
    # DATA SUMMARY & CONFIG
    # ========================
    
    def display_summary_and_config(self):
        """Display data summary and configuration."""
        print("\n" + "=" * 60)
        print("DATA SUMMARY & CONFIGURATION")
        print("=" * 60)
        
        try:
            # Read configuration
            print("\n[Application Configuration]")
            config = self.client.read_config_resource()
            config_data = [["Setting", "Value"]]
            for key, value in config.items():
                config_data.append([key, str(value)])
            print(tabulate(config_data, headers="firstrow", tablefmt="grid"))
            
            # Read summary
            print("\n[Data Summary]")
            summary = self.client.read_summary_resource()
            summary_data = [["Metric", "Value"]]
            for key, value in summary.items():
                summary_data.append([key, str(value)])
            print(tabulate(summary_data, headers="firstrow", tablefmt="grid"))
            
        except MCPClientError as e:
            print(f"Error: {e}")
    
    # ========================
    # COMPLETE WORKFLOW
    # ========================
    
    def run_complete_workflow(self):
        """Run a complete workflow demonstrating all features."""
        print("\n" + "=" * 70)
        print(" " * 15 + "MCP USER APPLICATION - COMPLETE WORKFLOW")
        print("=" * 70)
        
        try:
            self.perform_calculations()
            self.manage_users()
            self.manage_tasks()
            self.display_summary_and_config()
            
            print("\n" + "=" * 70)
            print("✓ Workflow completed successfully!")
            print("=" * 70)
            
        except MCPClientError as e:
            print(f"Application error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="MCP User Application")
    parser.add_argument(
        "--server-url",
        default="http://127.0.0.1:8000",
        help="MCP Server URL (default: http://127.0.0.1:8000)"
    )
    parser.add_argument(
        "--action",
        choices=["all", "calc", "users", "tasks", "summary"],
        default="all",
        help="Action to perform (default: all)"
    )
    
    args = parser.parse_args()
    
    try:
        with UserApplication(server_url=args.server_url) as app:
            if args.action == "all":
                app.run_complete_workflow()
            elif args.action == "calc":
                app.perform_calculations()
            elif args.action == "users":
                app.manage_users()
            elif args.action == "tasks":
                app.manage_tasks()
            elif args.action == "summary":
                app.display_summary_and_config()
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
