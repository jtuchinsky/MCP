from mcp.server.fastmcp import FastMCP
import yfinance as yf
import time
from typing import Dict, Tuple, Optional

# Create an MCP server with a custom name
mcp = FastMCP("Stock Price Server")

CACHE_TTL_SECONDS = 60  # Cache stock prices for 60 seconds
_price_cache: Dict[str, Tuple[float, float]] = {}  # symbol -> (price, timestamp)


def _get_cached_price(symbol: str) -> Optional[float]:
    """Get cached price if valid, otherwise return None."""
    if symbol in _price_cache:
        price, timestamp = _price_cache[symbol]
        if time.time() - timestamp < CACHE_TTL_SECONDS:
            return price
        else:
            del _price_cache[symbol]
    return None


def _cache_price(symbol: str, price: float) -> None:
    """Cache a stock price with current timestamp."""
    _price_cache[symbol] = (price, time.time())


def _clear_cache() -> None:
    """Clear all cached prices. Useful for testing."""
    _price_cache.clear()


@mcp.tool()
def get_stock_price(symbol: str) -> float:
    """
    Retrieve the current stock price for the given ticker symbol.
    Returns the latest closing price as a float.
    """
    cached_price = _get_cached_price(symbol)
    if cached_price is not None:
        return cached_price
    
    try:
        ticker = yf.Ticker(symbol)
        # Get today's historical data; may return empty if market is closed or symbol is invalid.
        data = ticker.history(period="1d")
        if not data.empty:
            # Use the last closing price from today's data
            price = data['Close'].iloc[-1]
            price_float = float(price)
            _cache_price(symbol, price_float)
            return price_float
        else:
            # As a fallback, try using the regular market price from the ticker info
            info = ticker.info
            price = info.get("regularMarketPrice", None)
            if price is not None:
                price_float = float(price)
                _cache_price(symbol, price_float)
                return price_float
            else:
                return -1.0  # Indicate failure
    except Exception:
        # Return -1.0 to indicate an error occurred when fetching the stock price
        return -1.0


@mcp.resource("stock://{symbol}")
def stock_resource(symbol: str) -> str:
    """
    Expose stock price data as a resource.
    Returns a formatted string with the current stock price for the given symbol.
    """
    price = get_stock_price(symbol)
    if price < 0:
        return f"Error: Could not retrieve price for symbol '{symbol}'."
    return f"The current price of '{symbol}' is ${price:.2f}."


@mcp.tool()
def get_stock_history(symbol: str, period: str = "1mo") -> str:
    """
    Retrieve historical data for a stock given a ticker symbol and a period.
    Returns the historical data as a CSV formatted string.

    Parameters:
        symbol: The stock ticker symbol.
        period: The period over which to retrieve historical data (e.g., '1mo', '3mo', '1y').
    """
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period)
        if data.empty:
            return f"No historical data found for symbol '{symbol}' with period '{period}'."
        # Convert the DataFrame to a CSV formatted string
        csv_data = data.to_csv()
        return csv_data
    except Exception as e:
        return f"Error fetching historical data: {str(e)}"


@mcp.tool()
def compare_stocks(symbol1: str, symbol2: str) -> str:
    """
    Compare the current stock prices of two ticker symbols.
    Returns a formatted message comparing the two stock prices.

    Parameters:
        symbol1: The first stock ticker symbol.
        symbol2: The second stock ticker symbol.
    """
    price1 = get_stock_price(symbol1)
    price2 = get_stock_price(symbol2)
    if price1 < 0 or price2 < 0:
        return f"Error: Could not retrieve data for comparison of '{symbol1}' and '{symbol2}'."
    if price1 > price2:
        result = f"{symbol1} (${price1:.2f}) is higher than {symbol2} (${price2:.2f})."
    elif price1 < price2:
        result = f"{symbol1} (${price1:.2f}) is lower than {symbol2} (${price2:.2f})."
    else:
        result = f"Both {symbol1} and {symbol2} have the same price (${price1:.2f})."
    return result


if __name__ == "__main__":
    mcp.run()
