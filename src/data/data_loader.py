import yfinance as yf
import pandas as pd
from typing import Optional, Tuple

class DataLoader:
    def __init__(self, symbol: str, start_date: str, end_date: str):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        
    def fetch_data(self) -> pd.DataFrame:
        """Fetch historical data from Yahoo Finance."""
        try:
            df = yf.download(self.symbol, start=self.start_date, end=self.end_date)
            return self._validate_data(df)
        except Exception as e:
            raise Exception(f"Error fetching data for {self.symbol}: {str(e)}")
    
    def _validate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate and clean the downloaded data."""
        if df.empty:
            raise ValueError(f"No data found for {self.symbol}")
        
        # Remove any missing values
        df = df.dropna()
        
        # Ensure all required columns are present
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Missing required columns in data")
            
        return df