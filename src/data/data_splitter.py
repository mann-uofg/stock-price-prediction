import numpy as np
import pandas as pd
from typing import Tuple
from sklearn.preprocessing import StandardScaler

class DataSplitter:
    @staticmethod
    def train_val_test_split(df: pd.DataFrame, target: str, config) -> Tuple:
        """Split data into train, validation, and test sets."""
        n = len(df)
        train_idx = int(n * config.train_size)
        val_idx = int(n * (config.train_size + config.val_size))
        
        # Split data
        train_data = df[:train_idx]
        val_data = df[train_idx:val_idx]
        test_data = df[val_idx:]
        
        # Prepare features and targets
        feature_cols = [col for col in df.columns if col != target]
        
        # Scale features
        scaler = StandardScaler()
        X_train = scaler.fit_transform(train_data[feature_cols])
        X_val = scaler.transform(val_data[feature_cols])
        X_test = scaler.transform(test_data[feature_cols])
        
        y_train = train_data[target].values
        y_val = val_data[target].values
        y_test = test_data[target].values
        
        return (X_train, X_val, X_test, y_train, y_val, y_test, scaler)