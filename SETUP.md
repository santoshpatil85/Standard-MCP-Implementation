# Setup & Installation Guide

Complete guide for setting up and running the Standard MCP Implementation.

## Prerequisites

### System Requirements

- **OS**: Linux, macOS, or Windows (with WSL)
- **Python**: 3.8 or higher
- **pip**: Latest version recommended
- **RAM**: 512MB minimum
- **Disk**: 500MB free space

### Check Your Python Installation

```bash
python --version
pip --version
```

Expected output:
```
Python 3.8.0 (or higher)
pip 21.0 (or higher)
```

## Installation Steps

### 1. Clone/Download the Repository

```bash
cd /workspaces/Standard-MCP-Implementation
```

### 2. Create Virtual Environments (Recommended)

Create separate virtual environments for each project:

```bash
# For MCP Server
cd mcp_server
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# For MCP Client
cd ../mcp_client
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# For User App
cd ../user_app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

**For MCP Server:**
```bash
cd mcp_server
source venv/bin/activate
pip install -r requirements.txt
```

**For MCP Client:**
```bash
cd mcp_client
source venv/bin/activate
pip install -r requirements.txt
```

**For User App:**
```bash
cd user_app
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Verify Installation

Test that dependencies are installed:

```bash
# Test Server
cd mcp_server
python -c "import fastmcp; print('FastMCP OK')"

# Test Client
cd ../mcp_client
python -c "import httpx; print('httpx OK')"

# Test App
cd ../user_app
python -c "from tabulate import tabulate; print('tabulate OK')"
```

## Running the System

### Terminal Setup

Open 3 terminal windows:
1. **Terminal 1**: MCP Server
2. **Terminal 2**: User Application
3. **Terminal 3**: Monitoring (optional)

### Starting the MCP Server

**Terminal 1:**
```bash
cd /workspaces/Standard-MCP-Implementation/mcp_server
source venv/bin/activate
python server.py
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Starting the User Application

**Terminal 2:**
```bash
cd /workspaces/Standard-MCP-Implementation/user_app
source venv/bin/activate
python app.py
```

This will run the complete workflow and display results.

### Using Custom Server URL

```bash
python app.py --server-url http://127.0.0.1:8000 --action all
```

### Running Specific Actions

```bash
# Just calculations
python app.py --action calc

# Just user management
python app.py --action users

# Just task management
python app.py --action tasks

# Just summary
python app.py --action summary
```

## Testing the MCP Client Directly

### Test Client Against Running Server

**Terminal 2:**
```bash
cd /workspaces/Standard-MCP-Implementation/mcp_client
source venv/bin/activate
python client.py
```

This runs the demo function showing all client capabilities.

## Troubleshooting

### Issue: "Module not found" errors

**Solution**: Make sure you're in the activated virtual environment:
```bash
which python  # Should show path to venv python
```

### Issue: Connection refused to server

**Solution**: Ensure server is running on the correct URL:
```bash
# Check if port 8000 is in use
lsof -i :8000

# If needed, use different port
python server.py --port 8001
```

### Issue: "No module named 'fastmcp'"

**Solution**: Reinstall dependencies:
```bash
pip install --upgrade -r requirements.txt
```

### Issue: httpx SSL errors

**Solution**: Update certifi:
```bash
pip install --upgrade certifi
```

## Project Configuration

### Environment Variables

Create `.env` file in each project root (optional):

```bash
# .env for each project
SERVER_URL=http://127.0.0.1:8000
DEBUG=True
LOG_LEVEL=INFO
```

Load in Python:
```python
from dotenv import load_dotenv
import os

load_dotenv()
server_url = os.getenv("SERVER_URL", "http://127.0.0.1:8000")
```

## Advanced Setup

### Using Different Python Versions

If you have multiple Python versions:

```bash
# Use Python 3.10
python3.10 -m venv venv

# Or specify in virtual environment
python3.9 -m venv venv_py39
```

### Using Poetry (Alternative)

If you prefer Poetry over pip:

```bash
# Install Poetry
pip install poetry

# Initialize in each project
poetry init

# Install dependencies
poetry install

# Run with poetry
poetry run python server.py
```

### Docker Setup (Advanced)

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY mcp_server /app/mcp_server
COPY requirements.txt /app/

RUN pip install -r mcp_server/requirements.txt

EXPOSE 8000

CMD ["python", "mcp_server/server.py"]
```

Build and run:
```bash
docker build -t mcp-server .
docker run -p 8000:8000 mcp-server
```

## Performance Tuning

### For Development

```python
# server.py configuration
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        mcp.app,
        host="127.0.0.1",
        port=8000,
        reload=True,  # Auto-reload on changes
        log_level="debug"
    )
```

### For Production

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        mcp.app,
        host="0.0.0.0",
        port=8000,
        workers=4,  # Multiple workers
        log_level="info"
    )
```

## Uninstalling

To remove all installations:

```bash
# Remove virtual environments
rm -rf mcp_server/venv
rm -rf mcp_client/venv
rm -rf user_app/venv

# Or deactivate and remove
deactivate
rm -rf venv
```

## Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] Created virtual environments (optional but recommended)
- [ ] Installed all dependencies from requirements.txt
- [ ] Started MCP Server successfully
- [ ] Ran User Application successfully
- [ ] Verified all tools work
- [ ] Verified all resources accessible

## Next Steps

1. Read [EXAMPLES.md](EXAMPLES.md) for usage examples
2. Read [ARCHITECTURE.md](ARCHITECTURE.md) for system design
3. Explore the source code
4. Modify and extend components
5. Add your own tools and resources

## Getting Help

### Common Issues

1. **Port already in use**: Change port in server.py
2. **Slow performance**: Reduce logging level
3. **Memory issues**: Check data store size

### Resource Links

- [FastMCP Documentation](https://fastmcp.readthedocs.io/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

---

**Last Updated**: February 2026
**Setup Guide Version**: 1.0.0
