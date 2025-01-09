import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_stock_data(symbol: str) -> pd.DataFrame:
    """Fetch stock data from Yahoo Finance"""
    print(f"Fetching data for {symbol}...")
    
    # Calculate start date (2 years ago from today)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)  # 730 days = 2 years
    
    df = yf.download(symbol, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
    df.columns = df.columns.map(lambda x: x if isinstance(x, str) else x[0])
    return df