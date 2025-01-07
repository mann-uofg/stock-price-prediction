import pandas as pd
import numpy as np
from typing import Dict

class TechnicalPatterns:
    @staticmethod
    def detect_candlestick_patterns(df: pd.DataFrame) -> Dict[str, np.ndarray]:
        """Detect various candlestick patterns"""
        df = df.copy()
        
        # Calculate candlestick properties
        df['Body'] = df['Close'] - df['Open']
        df['Upper_Shadow'] = df['High'] - df[['Open', 'Close']].max(axis=1)
        df['Lower_Shadow'] = df[['Open', 'Close']].min(axis=1) - df['Low']
        df['Body_Size'] = abs(df['Body'])
        
        patterns = {}
        
        # Doji pattern (small body, longer shadows)
        body_percentile = df['Body_Size'].quantile(0.2)
        shadow_percentile = df['Upper_Shadow'].quantile(0.8)
        patterns['Doji'] = (
            (df['Body_Size'] <= body_percentile) & 
            ((df['Upper_Shadow'] >= shadow_percentile) | 
             (df['Lower_Shadow'] >= shadow_percentile))
        ).astype(int)
        
        # Hammer pattern
        patterns['Hammer'] = (
            (df['Body_Size'] > 0) &  # Positive body
            (df['Lower_Shadow'] > 2 * df['Body_Size']) &  # Long lower shadow
            (df['Upper_Shadow'] < df['Body_Size'])  # Short upper shadow
        ).astype(int)
        
        # Shooting Star pattern
        patterns['Shooting_Star'] = (
            (df['Body_Size'] > 0) &  # Positive body
            (df['Upper_Shadow'] > 2 * df['Body_Size']) &  # Long upper shadow
            (df['Lower_Shadow'] < df['Body_Size'])  # Short lower shadow
        ).astype(int)
        
        return patterns

    @staticmethod
    def detect_support_resistance(df: pd.DataFrame, window: int = 20) -> Dict[str, np.ndarray]:
        """Detect support and resistance levels"""
        df = df.copy()
        levels = {}
        
        # Rolling min/max for support/resistance
        levels['Support'] = df['Low'].rolling(window=window).min()
        levels['Resistance'] = df['High'].rolling(window=window).max()
        
        # Distance from current price to support/resistance
        for level_type in ['Support', 'Resistance']:
            levels[f'{level_type}_Distance'] = (
                (df['Close'] - levels[level_type]) / df['Close']
            )
        
        return levels

    @staticmethod
    def calculate_momentum_indicators(df: pd.DataFrame) -> Dict[str, np.ndarray]:
        """Calculate momentum-based indicators"""
        indicators = {}
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        indicators['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        indicators['MACD'] = exp1 - exp2
        indicators['MACD_Signal'] = indicators['MACD'].ewm(span=9, adjust=False).mean()
        
        return indicators