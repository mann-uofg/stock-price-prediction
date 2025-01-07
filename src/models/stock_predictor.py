import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta
from src.features.feature_constants import TRAINING_FEATURES, PREDICTION_FEATURES

class StockPredictor:
    def __init__(self, n_estimators: int = 200, random_state: int = 42):
        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            random_state=random_state,
            max_depth=8,
            min_samples_split=5,
            min_samples_leaf=2,
            max_features='sqrt'
        )
        self.scaler = StandardScaler()
        
    def prepare_data(self, df: pd.DataFrame) -> tuple:
        """Prepare data for training"""
        X = df[TRAINING_FEATURES]
        y = df['Returns'].shift(-1)  # Predict next day's returns
        
        # Remove last row since we don't have next day's return
        X = X[:-1]
        y = y[:-1]
        
        X_scaled = self.scaler.fit_transform(X)
        return X_scaled, y, TRAINING_FEATURES
    
    def train(self, X: np.ndarray, y: np.ndarray):
        """Train the model"""
        self.model.fit(X, y)
    
    def predict_future(self, df: pd.DataFrame, n_days: int = 15) -> pd.Series:
        """Predict future stock returns"""
        from src.features.feature_generator import generate_future_features
        
        last_date = df.index[-1]
        future_dates = []
        current_date = last_date
        
        while len(future_dates) < n_days:
            current_date += timedelta(days=1)
            if current_date.weekday() < 5:  # Monday = 0, Friday = 4
                future_dates.append(current_date)
        
        last_known = df.iloc[-1]
        future_features = generate_future_features(df, last_known, n_days)
        
        # Ensure we use the same features for prediction as training
        future_features_scaled = self.scaler.transform(
            future_features[PREDICTION_FEATURES]
        )
        
        predicted_returns = self.model.predict(future_features_scaled)
        
        # Apply smoothing to avoid extreme predictions
        predicted_returns = np.clip(
            predicted_returns,
            df['Returns'].quantile(0.05),  # Lower bound
            df['Returns'].quantile(0.95)   # Upper bound
        )
        
        return pd.Series(predicted_returns, index=future_dates)