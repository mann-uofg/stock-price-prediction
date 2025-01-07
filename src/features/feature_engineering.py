import pandas as pd
import numpy as np
from typing import List, Tuple

class FeatureEngineer:
    @staticmethod
    def create_features(df: pd.DataFrame, target_col: str = 'Close', 
                       lookback_periods: List[int] = [1, 5, 10]) -> Tuple[pd.DataFrame, str]:
        """
        Create features for the model including lagged returns and rolling statistics.
        """
        df = df.copy()
        
        # Calculate returns
        df['Returns'] = df[target_col].pct_change()
        
        # Create lagged returns
        for period in lookback_periods:
            df[f'Lag_Return_{period}'] = df['Returns'].shift(period)
            
        # Rolling statistics
        df['Rolling_Mean_5'] = df[target_col].rolling(window=5).mean()
        df['Rolling_Std_5'] = df[target_col].rolling(window=5).std()
        
        # Price momentum
        df['Price_Momentum'] = df[target_col] / df[target_col].shift(5) - 1
        
        # Target variable (next day return)
        target = 'Next_Day_Return'
        df[target] = df['Returns'].shift(-1)
        
        # Remove rows with NaN values
        df = df.dropna()
        
        return df, target