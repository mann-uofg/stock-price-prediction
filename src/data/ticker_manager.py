import json
import os
from typing import List, Dict
from datetime import datetime

class TickerManager:
    def __init__(self, storage_path: str = 'data/tickers'):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        self.tickers_file = os.path.join(storage_path, 'tickers.json')
        self.tickers = self._load_tickers()
    
    def _load_tickers(self) -> Dict:
        if os.path.exists(self.tickers_file):
            with open(self.tickers_file, 'r') as f:
                return json.load(f)
        return {'watchlist': [], 'last_updated': None}
    
    def add_ticker(self, ticker: str) -> None:
        if ticker not in self.tickers['watchlist']:
            self.tickers['watchlist'].append(ticker)
            self.tickers['last_updated'] = datetime.now().isoformat()
            self._save_tickers()
    
    def remove_ticker(self, ticker: str) -> None:
        if ticker in self.tickers['watchlist']:
            self.tickers['watchlist'].remove(ticker)
            self.tickers['last_updated'] = datetime.now().isoformat()
            self._save_tickers()
    
    def get_tickers(self) -> List[str]:
        return self.tickers['watchlist']
    
    def _save_tickers(self) -> None:
        with open(self.tickers_file, 'w') as f:
            json.dump(self.tickers, f, indent=2)