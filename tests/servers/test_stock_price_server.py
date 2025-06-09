import pytest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
from src.servers.stock_price_server import get_stock_price, stock_resource, get_stock_history, compare_stocks


class TestGetStockPrice:
    
    @patch('src.servers.stock_price_server.yf.Ticker')
    def test_get_stock_price_success_with_history(self, mock_ticker):
        # Setup mock data
        mock_data = pd.DataFrame({'Close': [150.0, 155.0]})
        mock_ticker_instance = Mock()
        mock_ticker_instance.history.return_value = mock_data
        mock_ticker.return_value = mock_ticker_instance
        
        result = get_stock_price("AAPL")
        
        assert result == 155.0
        mock_ticker.assert_called_once_with("AAPL")
        mock_ticker_instance.history.assert_called_once_with(period="1d")
    
    @patch('src.servers.stock_price_server.yf.Ticker')
    def test_get_stock_price_success_with_fallback(self, mock_ticker):
        # Setup mock data - empty history, fallback to info
        mock_data = pd.DataFrame()
        mock_ticker_instance = Mock()
        mock_ticker_instance.history.return_value = mock_data
        mock_ticker_instance.info = {"regularMarketPrice": 160.5}
        mock_ticker.return_value = mock_ticker_instance
        
        result = get_stock_price("AAPL")
        
        assert result == 160.5
        mock_ticker.assert_called_once_with("AAPL")
    
    @patch('src.servers.stock_price_server.yf.Ticker')
    def test_get_stock_price_no_data_available(self, mock_ticker):
        # Setup mock data - empty history, no regularMarketPrice
        mock_data = pd.DataFrame()
        mock_ticker_instance = Mock()
        mock_ticker_instance.history.return_value = mock_data
        mock_ticker_instance.info = {}
        mock_ticker.return_value = mock_ticker_instance
        
        result = get_stock_price("INVALID")
        
        assert result == -1.0
    
    @patch('src.servers.stock_price_server.yf.Ticker')
    def test_get_stock_price_exception_handling(self, mock_ticker):
        # Setup mock to raise exception
        mock_ticker.side_effect = Exception("Network error")
        
        result = get_stock_price("AAPL")
        
        assert result == -1.0


class TestStockResource:
    
    @patch('src.servers.stock_price_server.get_stock_price')
    def test_stock_resource_success(self, mock_get_price):
        mock_get_price.return_value = 150.75
        
        result = stock_resource("AAPL")
        
        assert result == "The current price of 'AAPL' is $150.75."
        mock_get_price.assert_called_once_with("AAPL")
    
    @patch('src.servers.stock_price_server.get_stock_price')
    def test_stock_resource_error(self, mock_get_price):
        mock_get_price.return_value = -1.0
        
        result = stock_resource("INVALID")
        
        assert result == "Error: Could not retrieve price for symbol 'INVALID'."
        mock_get_price.assert_called_once_with("INVALID")


class TestGetStockHistory:
    
    @patch('src.servers.stock_price_server.yf.Ticker')
    def test_get_stock_history_success(self, mock_ticker):
        # Setup mock data
        mock_data = pd.DataFrame({
            'Open': [100.0, 101.0],
            'High': [105.0, 106.0],
            'Low': [99.0, 100.0],
            'Close': [104.0, 105.0],
            'Volume': [1000000, 1100000]
        })
        mock_ticker_instance = Mock()
        mock_ticker_instance.history.return_value = mock_data
        mock_ticker.return_value = mock_ticker_instance
        
        result = get_stock_history("AAPL", "1mo")
        
        assert "Open,High,Low,Close,Volume" in result
        assert "100.0,105.0,99.0,104.0,1000000" in result
        mock_ticker.assert_called_once_with("AAPL")
        mock_ticker_instance.history.assert_called_once_with(period="1mo")
    
    @patch('src.servers.stock_price_server.yf.Ticker')
    def test_get_stock_history_default_period(self, mock_ticker):
        # Setup mock data
        mock_data = pd.DataFrame({
            'Open': [100.0],
            'High': [105.0],
            'Low': [99.0],
            'Close': [104.0],
            'Volume': [1000000]
        })
        mock_ticker_instance = Mock()
        mock_ticker_instance.history.return_value = mock_data
        mock_ticker.return_value = mock_ticker_instance
        
        result = get_stock_history("AAPL")
        
        assert isinstance(result, str)
        mock_ticker_instance.history.assert_called_once_with(period="1mo")
    
    @patch('src.servers.stock_price_server.yf.Ticker')
    def test_get_stock_history_empty_data(self, mock_ticker):
        # Setup mock data - empty DataFrame
        mock_data = pd.DataFrame()
        mock_ticker_instance = Mock()
        mock_ticker_instance.history.return_value = mock_data
        mock_ticker.return_value = mock_ticker_instance
        
        result = get_stock_history("INVALID", "1y")
        
        assert result == "No historical data found for symbol 'INVALID' with period '1y'."
    
    @patch('src.servers.stock_price_server.yf.Ticker')
    def test_get_stock_history_exception_handling(self, mock_ticker):
        # Setup mock to raise exception
        mock_ticker.side_effect = Exception("API error")
        
        result = get_stock_history("AAPL", "1mo")
        
        assert result == "Error fetching historical data: API error"


class TestCompareStocks:
    
    @patch('src.servers.stock_price_server.get_stock_price')
    def test_compare_stocks_first_higher(self, mock_get_price):
        mock_get_price.side_effect = [150.0, 120.0]
        
        result = compare_stocks("AAPL", "MSFT")
        
        assert result == "AAPL ($150.00) is higher than MSFT ($120.00)."
        assert mock_get_price.call_count == 2
    
    @patch('src.servers.stock_price_server.get_stock_price')
    def test_compare_stocks_second_higher(self, mock_get_price):
        mock_get_price.side_effect = [120.0, 150.0]
        
        result = compare_stocks("MSFT", "AAPL")
        
        assert result == "MSFT ($120.00) is lower than AAPL ($150.00)."
        assert mock_get_price.call_count == 2
    
    @patch('src.servers.stock_price_server.get_stock_price')
    def test_compare_stocks_equal_prices(self, mock_get_price):
        mock_get_price.side_effect = [150.0, 150.0]
        
        result = compare_stocks("AAPL", "MSFT")
        
        assert result == "Both AAPL and MSFT have the same price ($150.00)."
        assert mock_get_price.call_count == 2
    
    @patch('src.servers.stock_price_server.get_stock_price')
    def test_compare_stocks_first_error(self, mock_get_price):
        mock_get_price.side_effect = [-1.0, 150.0]
        
        result = compare_stocks("INVALID", "AAPL")
        
        assert result == "Error: Could not retrieve data for comparison of 'INVALID' and 'AAPL'."
        assert mock_get_price.call_count == 2
    
    @patch('src.servers.stock_price_server.get_stock_price')
    def test_compare_stocks_second_error(self, mock_get_price):
        mock_get_price.side_effect = [150.0, -1.0]
        
        result = compare_stocks("AAPL", "INVALID")
        
        assert result == "Error: Could not retrieve data for comparison of 'AAPL' and 'INVALID'."
        assert mock_get_price.call_count == 2
    
    @patch('src.servers.stock_price_server.get_stock_price')
    def test_compare_stocks_both_error(self, mock_get_price):
        mock_get_price.side_effect = [-1.0, -1.0]
        
        result = compare_stocks("INVALID1", "INVALID2")
        
        assert result == "Error: Could not retrieve data for comparison of 'INVALID1' and 'INVALID2'."
        assert mock_get_price.call_count == 2