#!/bin/bash

echo "🔧 Testing MCP Server in CLI mode..."
echo "=============================================="

cd "$(dirname "$0")"
npx @modelcontextprotocol/inspector --config mcp_inspector_config.json --server stock-price-server --cli