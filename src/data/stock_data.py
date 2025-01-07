import yfinance as yf
import pandas as pd

def fetch_stock_data(symbol: str, start_date: str = '2020-01-01') -> pd.DataFrame:
    """Fetch stock data from Yahoo Finance"""
    print(f"Fetching data for {symbol}...")
    df = yf.download(symbol, start=start_date)
    df.columns = df.columns.map(lambda x: x if isinstance(x, str) else x[0])
    return df