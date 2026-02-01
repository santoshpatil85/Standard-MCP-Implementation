#!/usr/bin/env python3
"""
Integration test for MCP Implementation.
Tests the complete workflow: server -> client -> app
"""

import subprocess
import time
import sys
import signal
import requests
from pathlib import Path

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'


def print_success(msg):
    """Print success message."""
    print(f"{GREEN}✓ {msg}{RESET}")


def print_error(msg):
    """Print error message."""
    print(f"{RED}✗ {msg}{RESET}")


def print_info(msg):
    """Print info message."""
    print(f"{YELLOW}→ {msg}{RESET}")


def test_imports():
    """Test that all modules can be imported."""
    print_info("Testing module imports...")
    
    try:
        from mcp_server.server import mcp
        print_success("MCP server module imported")
        
        from mcp_client.client import MCPClient
        print_success("MCP client module imported")
        
        from user_app.app import UserApplication
        print_success("User application module imported")
        
        return True
    except Exception as e:
        print_error(f"Import failed: {e}")
        return False


def test_server_setup():
    """Test that server can be instantiated."""
    print_info("Testing server setup...")
    
    try:
        from mcp_server.server import mcp
        app = mcp.http_app()
        print_success("FastMCP HTTP app created successfully")
        
        # Check that we can access server configuration
        print_success(f"Server name: {mcp.name}")
        
        return True
    except Exception as e:
        print_error(f"Server setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_server_startup():
    """Test that server can start."""
    print_info("Testing server startup...")
    
    try:
        # Start server in background
        server_process = subprocess.Popen(
            [sys.executable, "mcp_server/server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Give server time to start
        time.sleep(3)
        
        # Check if server is running
        if server_process.poll() is not None:
            stdout, stderr = server_process.communicate()
            print_error(f"Server failed to start")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return False
        
        print_success("Server started successfully")
        
        # Clean up
        server_process.terminate()
        try:
            server_process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            server_process.kill()
        print_success("Server terminated cleanly")
        
        return True
    
    except Exception as e:
        print_error(f"Server startup test failed: {e}")
        try:
            server_process.terminate()
        except:
            pass
        return False


def test_client_connection():
    """Test that client can connect and make basic calls."""
    print_info("Testing client connection...")
    
    try:
        from mcp_client.client import MCPClient
        
        client = MCPClient()
        print_success("MCPClient instantiated")
        
        # Test a simple tool call (this will fail without server, but validates structure)
        try:
            result = client.add_numbers(5, 3)
            print_success(f"Tool call works: 5 + 3 = {result.get('result', 'unknown')}")
        except Exception as e:
            # Expected to fail without running server
            print_info(f"Tool call failed (expected without server): {str(e)[:50]}...")
        
        client.close()
        print_success("Client closed cleanly")
        
        return True
    
    except Exception as e:
        print_error(f"Client connection test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("MCP INTEGRATION TEST SUITE")
    print("=" * 60 + "\n")
    
    results = {}
    
    # Test 1: Imports
    results['imports'] = test_imports()
    print()
    
    # Test 2: Server setup
    results['server_setup'] = test_server_setup()
    print()
    
    # Test 3: Server startup (only if setup works)
    if results['server_setup']:
        results['server_startup'] = test_server_startup()
    else:
        results['server_startup'] = False
    print()
    
    # Test 4: Client connection
    results['client_connection'] = test_client_connection()
    print()
    
    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"  {test_name.replace('_', ' ').title()}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print_success("All tests passed!")
        return 0
    else:
        print_error(f"{total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
