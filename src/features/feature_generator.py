import pandas as pd
import numpy as np
from typing import Dict
from .technical_patterns import TechnicalPatterns
from .feature_constants import PREDICTION_FEATURES

def add_technical_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add technical indicators to the dataset"""
    df = df.copy()
    
    # Basic price features
    df['Returns'] = df['Close'].pct_change()
    df['Log_Returns'] = np.log(df['Close'] / df['Close'].shift(1))
    
    # Moving averages and trends
    df['SMA20'] = df['Close'].rolling(window=20).mean()
    df['SMA50'] = df['Close'].rolling(window=50).mean()
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
    
    # Volatility
    df['Volatility'] = df['Returns'].rolling(window=20).std()
    df['ATR'] = df['High'] - df['Low']
    
    # Trend indicators
    df['Price_Momentum'] = df['Close'].pct_change(periods=5)
    df['Trend'] = np.where(df['SMA20'] > df['SMA50'], 1, -1)
    
    # Volume analysis
    df['Volume_Change'] = df['Volume'].pct_change()
    df['Volume_MA20'] = df['Volume'].rolling(window=20).mean()
    df['Volume_Trend'] = np.where(df['Volume'] > df['Volume_MA20'], 1, -1)
    
    # Add technical patterns
    patterns = TechnicalPatterns.detect_candlestick_patterns(df)
    support_resistance = TechnicalPatterns.detect_support_resistance(df)
    momentum = TechnicalPatterns.calculate_momentum_indicators(df)
    
    # Add all new features to dataframe
    for name, values in {**patterns, **support_resistance, **momentum}.items():
        df[name] = values
    
    return df.dropna()

def generate_future_features(df: pd.DataFrame, last_known: pd.Series, n_days: int = 15) -> pd.DataFrame:
    """Generate dynamic features for future predictions"""
    features_list = []
    
    # Historical statistics
    hist_volatility = df['Volatility'].mean()
    hist_returns_std = df['Returns'].std()
    
    # Current state
    current_sma20 = last_known['SMA20']
    current_sma50 = last_known['SMA50']
    current_returns = last_known['Returns']
    current_volatility = last_known['Volatility']
    current_momentum = last_known['Price_Momentum']
    current_trend = 1 if current_sma20 > current_sma50 else -1
    current_volume_trend = last_known['Volume_Trend']
    current_rsi = last_known['RSI']
    
    for i in range(n_days):
        # Generate returns considering market conditions
        base_return = np.random.normal(0, hist_returns_std)
        
        # Adjust returns based on RSI
        if current_rsi > 70:  # Overbought
            base_return *= 0.8
        elif current_rsi < 30:  # Oversold
            base_return *= 1.2
            
        # Update features
        current_returns = base_return
        current_volatility = hist_volatility * (1 + np.random.normal(0, 0.1))
        current_momentum = current_momentum * 0.95 + base_return
        current_rsi += (base_return * 2) * (-1 if current_rsi > 50 else 1)
        current_rsi = max(0, min(100, current_rsi))
        
        features_dict = {
            'SMA20': current_sma20,
            'SMA50': current_sma50,
            'Returns': current_returns,
            'Volatility': current_volatility,
            'Price_Momentum': current_momentum,
            'Trend': current_trend,
            'Volume_Trend': current_volume_trend,
            'RSI': current_rsi
        }
        
        features_list.append(features_dict)
        
        # Update moving averages
        current_sma20 = current_sma20 * 0.95 + current_returns * 0.05
        current_sma50 = current_sma50 * 0.98 + current_returns * 0.02
    
    return pd.DataFrame(features_list)