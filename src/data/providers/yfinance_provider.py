import yfinance as yf
import pandas as pd
from typing import Optional
from .base_provider import BaseDataProvider

class YFinanceProvider(BaseDataProvider):
    def fetch_data(self, symbol: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        try:
            df = yf.download(symbol, start=start_date, end=end_date)
            return df
        except Exception as e:
            raise Exception(f"Error fetching data for {symbol}: {str(e)}")