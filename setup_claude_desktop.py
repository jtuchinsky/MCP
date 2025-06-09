#!/usr/bin/env python3
"""
Setup script to configure the Stock Price MCP Server for Claude Desktop.
"""

import json
import os
import shutil
from pathlib import Path

def get_claude_config_path():
    """Get the Claude Desktop configuration path based on the OS."""
    home = Path.home()
    
    # macOS path
    config_path = home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    
    return config_path

def backup_existing_config(config_path):
    """Create a backup of existing configuration if it exists."""
    if config_path.exists():
        backup_path = config_path.with_suffix('.json.backup')
        shutil.copy2(config_path, backup_path)
        print(f"✅ Backed up existing config to: {backup_path}")
        return True
    return False

def load_existing_config(config_path):
    """Load existing Claude Desktop configuration."""
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"⚠️  Warning: Existing config file is invalid JSON")
            return {}
    return {}

def setup_mcp_server():
    """Set up the Stock Price MCP Server for Claude Desktop."""
    print("🚀 Setting up Stock Price MCP Server for Claude Desktop...")
    
    # Get paths
    project_root = Path(__file__).parent.absolute()
    server_path = project_root / "src" / "servers" / "stock_price_server.py"
    config_path = get_claude_config_path()
    
    # Verify server file exists
    if not server_path.exists():
        print(f"❌ Error: Server file not found at {server_path}")
        return False
    
    # Create config directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Backup existing config
    backup_existing_config(config_path)
    
    # Load existing config or create new one
    config = load_existing_config(config_path)
    
    # Initialize mcpServers if it doesn't exist
    if "mcpServers" not in config:
        config["mcpServers"] = {}
    
    # Add our server configuration
    config["mcpServers"]["stock-price-server"] = {
        "command": "python",
        "args": [str(server_path)],
        "env": {
            "PYTHONPATH": str(project_root)
        }
    }
    
    # Write the updated configuration
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Successfully configured Claude Desktop!")
        print(f"📁 Config file: {config_path}")
        print(f"🔧 Server path: {server_path}")
        print("\n📋 Next steps:")
        print("1. Restart Claude Desktop")
        print("2. The Stock Price Server should now be available")
        print("3. You can test it by asking Claude about stock prices")
        
        return True
        
    except Exception as e:
        print(f"❌ Error writing config file: {e}")
        return False

def verify_dependencies():
    """Verify required dependencies are installed."""
    try:
        import yfinance
        import mcp.server.fastmcp
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📦 Install with: pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    print("🔍 Verifying dependencies...")
    if not verify_dependencies():
        exit(1)
    
    print("\n🛠️  Setting up MCP server...")
    if setup_mcp_server():
        print("\n🎉 Setup completed successfully!")
    else:
        print("\n💥 Setup failed!")
        exit(1)