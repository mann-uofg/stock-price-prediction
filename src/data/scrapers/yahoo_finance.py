import yfinance as yf
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
from typing import Dict, Any

class YahooFinanceScraper:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.ticker = yf.Ticker(symbol)
    
    def get_analyst_data(self) -> Dict[str, Any]:
        """Get analyst recommendations and price targets"""
        try:
            # Get analyst recommendations
            recommendations = self.ticker.recommendations
            if recommendations is not None:
                recommendations = recommendations.tail()
            
            # Get analyst price targets
            target_data = self.ticker.info
            return {
                'recommendations': recommendations,
                'current_price': target_data.get('currentPrice'),
                'target_mean_price': target_data.get('targetMeanPrice'),
                'target_high_price': target_data.get('targetHighPrice'),
                'target_low_price': target_data.get('targetLowPrice'),
                'number_of_analysts': target_data.get('numberOfAnalystOpinions')
            }
        except Exception as e:
            print(f"Error fetching analyst data: {str(e)}")
            return {}
    
    def get_earnings_data(self) -> Dict[str, Any]:
        """Get earnings data and next earnings date"""
        try:
            # Get earnings data
            earnings = self.ticker.earnings
            next_earnings = self.ticker.calendar
            
            return {
                'historical_earnings': earnings,
                'next_earnings_date': next_earnings.get('Earnings Date', [None])[0] if next_earnings is not None else None
            }
        except Exception as e:
            print(f"Error fetching earnings data: {str(e)}")
            return {}
    
    def get_financials(self) -> Dict[str, Any]:
        """Get key financial metrics"""
        try:
            info = self.ticker.info
            return {
                'market_cap': info.get('marketCap'),
                'pe_ratio': info.get('forwardPE'),
                'eps': info.get('trailingEps'),
                'revenue': info.get('totalRevenue'),
                'profit_margins': info.get('profitMargins'),
                'beta': info.get('beta'),
                'dividend_yield': info.get('dividendYield')
            }
        except Exception as e:
            print(f"Error fetching financial data: {str(e)}")
            return {}
        