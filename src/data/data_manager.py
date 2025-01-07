import pandas as pd
import os
from datetime import datetime, timedelta
from typing import Optional
from .data_loader import DataLoader
from .ticker_manager import TickerManager

class DataManager:
    def __init__(self, storage_path: str = 'data/stock_data'):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        self.ticker_manager = TickerManager()
    
    def update_data(self, ticker: Optional[str] = None) -> None:
        """Update data for one ticker or all tickers in watchlist"""
        tickers = [ticker] if ticker else self.ticker_manager.get_tickers()
        
        for symbol in tickers:
            # Get latest data date
            last_date = self._get_last_date(symbol)
            start_date = last_date + timedelta(days=1) if last_date else None
            
            # Fetch new data
            loader = DataLoader(
                symbol=symbol,
                start_date=start_date.strftime('%Y-%m-%d') if start_date else None,
                end_date=datetime.now().strftime('%Y-%m-%d')
            )
            
            new_data = loader.fetch_data()
            if not new_data.empty:
                self._save_data(symbol, new_data)
    
    def get_data(self, ticker: str) -> pd.DataFrame:
        """Get stored data for a ticker"""
        file_path = os.path.join(self.storage_path, f'{ticker}.csv')
        if os.path.exists(file_path):
            return pd.read_csv(file_path, index_col=0, parse_dates=True)
        return pd.DataFrame()
    
    def _get_last_date(self, ticker: str) -> Optional[datetime]:
        data = self.get_data(ticker)
        if not data.empty:
            return pd.to_datetime(data.index[-1])
        return None
    
    def _save_data(self, ticker: str, data: pd.DataFrame) -> None:
        file_path = os.path.join(self.storage_path, f'{ticker}.csv')
        
        # Append to existing data if it exists
        existing_data = self.get_data(ticker)
        if not existing_data.empty:
            data = pd.concat([existing_data, data])
            data = data[~data.index.duplicated(keep='last')]
        
        data.sort_index().to_csv(file_path)