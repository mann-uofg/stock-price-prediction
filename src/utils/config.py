from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

@dataclass
class ModelConfig:
    # Data parameters
    symbol: str = 'AAPL'
    train_size: float = 0.7
    val_size: float = 0.15
    test_size: float = 0.15
    
    # Data provider settings
    data_provider: str = 'yfinance'  # 'yfinance' or 'finnhub'
    finnhub_api_key: str = ''  # Required if using Finnhub
    
    # Auto-update settings
    auto_update: bool = True
    update_frequency: str = 'daily'  # 'daily' or 'weekly'
    
    # Feature parameters
    lookback_periods: List[int] = (1, 5, 10)
    target_col: str = 'Close'
    
    # Model parameters
    random_state: int = 42
    lstm_units: int = 50
    lstm_epochs: int = 100
    rf_n_estimators: int = 100
    
    # Training parameters
    batch_size: int = 32
    learning_rate: float = 0.001