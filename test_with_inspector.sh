#!/bin/bash

echo "🚀 Starting MCP Inspector for Stock Price Server..."
echo "📊 Server: stock-price-server"
echo "🌐 Inspector will be available at: http://127.0.0.1:6274"
echo ""
echo "Available tools to test:"
echo "  • get_stock_price(symbol: str) -> float"
echo "  • get_stock_history(symbol: str, period: str = '1mo') -> str"
echo "  • compare_stocks(symbol1: str, symbol2: str) -> str"
echo ""
echo "Example test calls:"
echo "  • get_stock_price('AAPL')"
echo "  • get_stock_history('TSLA', '1w')"
echo "  • compare_stocks('AAPL', 'MSFT')"
echo ""
echo "Press Ctrl+C to stop the inspector"
echo "=============================================="

cd "$(dirname "$0")"
npx @modelcontextprotocol/inspector --config mcp_inspector_config.json --server stock-price-server