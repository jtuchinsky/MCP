# Stock Price Server - MCP Integration Guide

A Model Context Protocol (MCP) server that provides real-time stock price data and analysis tools using the Yahoo Finance API.

## Features

The Stock Price Server provides the following tools:

- **`get_stock_price(symbol)`**: Get current stock price for any ticker symbol
- **`get_stock_history(symbol, period)`**: Retrieve historical data in CSV format
- **`compare_stocks(symbol1, symbol2)`**: Compare prices between two stocks
- **`stock://` resources**: Access stock data as MCP resources

## Prerequisites

- Python 3.8+
- Required packages: `mcp`, `yfinance`, `pandas`
- Node.js (for MCP Inspector)

Install dependencies:
```bash
pip install -r requirements.txt
```

## Testing the Server Directly

### 1. Basic Server Test

Test if the server starts correctly:
```bash
cd /path/to/your/project
python src/servers/stock_price_server.py
```

### 2. Unit Tests

Run comprehensive unit tests:
```bash
pytest tests/servers/test_stock_price_server.py -v
```

The tests cover:
- Stock price retrieval with mocked API responses
- Error handling for invalid symbols
- Historical data processing
- Stock comparison functionality

## Integration with Claude Desktop

### Automatic Setup

Use the provided setup script for easy configuration:

```bash
python setup_claude_desktop.py
```

This script will:
- ✅ Verify all dependencies are installed
- 🔧 Configure Claude Desktop's MCP settings
- 📁 Set up proper Python paths
- 🔄 Create backup of existing configuration

### Manual Setup

If you prefer manual setup, add this to your Claude Desktop configuration file:

**Location**: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

```json
{
  "mcpServers": {
    "stock-price-server": {
      "command": "/path/to/your/python",
      "args": ["/path/to/your/project/src/servers/stock_price_server.py"],
      "env": {
        "PYTHONPATH": "/path/to/your/project"
      }
    }
  }
}
```

**Important**: Use the full path to your Python executable (e.g., `/Users/username/anaconda3/bin/python`)

### After Setup

1. **Restart Claude Desktop** completely
2. **Test the integration** by asking Claude:
   - "What's the current price of AAPL?"
   - "Compare TSLA and MSFT stock prices"
   - "Get the 1-week history for NVDA"

## Using MCP Inspector for Testing

MCP Inspector provides a web-based interface for testing and debugging MCP servers.

### Quick Start

Use the provided test script:
```bash
./test_with_inspector.sh
```

This opens the MCP Inspector at `http://127.0.0.1:6274`

### Manual Launch

```bash
npx @modelcontextprotocol/inspector --config mcp_inspector_config.json --server stock-price-server
```

### CLI Mode Testing

For command-line testing:
```bash
./test_cli.sh
```

Or manually:
```bash
npx @modelcontextprotocol/inspector --config mcp_inspector_config.json --server stock-price-server --cli
```

## Testing Examples

### Through MCP Inspector Web UI

1. **Open Inspector**: Navigate to `http://127.0.0.1:6274`
2. **View Tools**: See all available tools in the sidebar
3. **Test Tool Calls**:
   - `get_stock_price("AAPL")` → Returns current Apple stock price
   - `get_stock_history("TSLA", "1w")` → Returns Tesla's 1-week price history
   - `compare_stocks("AAPL", "MSFT")` → Compares Apple vs Microsoft prices
4. **Check Resources**: Test `stock://AAPL` resource access

### Through Claude Desktop

Once configured, you can ask Claude:

```
"What's the current price of Apple stock?"
"Show me Tesla's stock performance over the last month"
"Which is more expensive right now: Amazon or Google stock?"
"Get the historical data for Microsoft over the past 3 months"
```

## Troubleshooting

### Server Not Connecting

1. **Check Python Path**: Ensure you're using the correct Python executable
   ```bash
   which python
   /path/to/your/python --version
   ```

2. **Verify Dependencies**: 
   ```bash
   python -c "import mcp.server.fastmcp, yfinance; print('Dependencies OK')"
   ```

3. **Test Server Directly**:
   ```bash
   python src/servers/stock_price_server.py
   ```

### Claude Desktop Issues

1. **Restart Claude Desktop** completely
2. **Check Configuration Path**: Verify the config file location
3. **Use Full Paths**: Always use absolute paths in configuration
4. **Check Logs**: Look for error messages in Claude Desktop's console

### MCP Inspector Issues

1. **Port Conflicts**: If port 6274 is busy, the inspector will use a different port
2. **Node.js Required**: Ensure Node.js is installed
3. **Network Issues**: Check if `http://127.0.0.1:6274` is accessible

## API Rate Limits

The Yahoo Finance API used by this server has rate limits:
- **Recommended**: Don't make more than 2000 requests per hour
- **Best Practice**: Cache results when possible
- **Error Handling**: The server returns `-1.0` for failed requests

## Configuration Files

### Claude Desktop Config
- **File**: `claude_desktop_config.json`
- **Purpose**: Reference configuration for Claude Desktop
- **Usage**: Copy to Claude Desktop's config directory

### MCP Inspector Config
- **File**: `mcp_inspector_config.json`
- **Purpose**: Configuration for testing with MCP Inspector
- **Usage**: Used by test scripts and manual inspector launches

## Development

### Adding New Tools

1. **Define Function**: Create a new function in `stock_price_server.py`
2. **Add Decorator**: Use `@mcp.tool()` decorator
3. **Write Tests**: Add tests in `test_stock_price_server.py`
4. **Update Documentation**: Update this README

### Example New Tool

```python
@mcp.tool()
def get_stock_info(symbol: str) -> str:
    """Get detailed stock information including market cap, P/E ratio, etc."""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return f"Market Cap: {info.get('marketCap', 'N/A')}, P/E: {info.get('trailingPE', 'N/A')}"
    except Exception:
        return f"Error retrieving info for {symbol}"
```

## Security Notes

- **No Authentication**: This server doesn't implement authentication
- **Rate Limiting**: Be mindful of Yahoo Finance API limits
- **Error Handling**: Sensitive information is not exposed in error messages
- **Local Access**: Server runs locally and doesn't expose external endpoints

## Support

For issues related to:
- **MCP Protocol**: Check [MCP Documentation](https://modelcontextprotocol.io/)
- **Claude Desktop**: Refer to Claude Desktop documentation
- **Yahoo Finance Data**: Check `yfinance` library documentation
- **This Server**: Create an issue in the project repository

---

**Happy Trading! 📈**