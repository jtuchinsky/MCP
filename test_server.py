#!/usr/bin/env python3
"""
Simple test MCP server to verify connectivity
"""

from mcp.server.fastmcp import FastMCP
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Create a simple test server
mcp = FastMCP("Test Server")

@mcp.tool()
def test_tool() -> str:
    """A simple test tool that returns a greeting."""
    return "Hello from MCP Test Server!"

if __name__ == "__main__":
    print("Starting Test MCP Server...", file=sys.stderr)
    mcp.run()