import pandas as pd
import requests
from typing import Optional
from datetime import datetime
from .base_provider import BaseDataProvider

class FinnhubProvider(BaseDataProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://finnhub.io/api/v1"
    
    def fetch_data(self, symbol: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        try:
            # Convert dates to timestamps
            start_ts = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp()) if start_date else None
            end_ts = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp()) if end_date else int(datetime.now().timestamp())
            
            # Make API request
            url = f"{self.base_url}/stock/candle"
            params = {
                'symbol': symbol,
                'resolution': 'D',
                'from': start_ts,
                'to': end_ts,
                'token': self.api_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if data['s'] == 'ok':
                df = pd.DataFrame({
                    'Open': data['o'],
                    'High': data['h'],
                    'Low': data['l'],
                    'Close': data['c'],
                    'Volume': data['v']
                }, index=pd.to_datetime([datetime.fromtimestamp(t) for t in data['t']]))
                return df
            
            return pd.DataFrame()
            
        except Exception as e:
            raise Exception(f"Error fetching data from Finnhub for {symbol}: {str(e)}")