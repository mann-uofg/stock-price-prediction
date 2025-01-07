import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from src.models.base_model import BaseModel
from typing import Dict

class RandomForestModel(BaseModel):
    def __init__(self, config):
        self.config = config
        self.model = RandomForestRegressor(
            n_estimators=config.rf_n_estimators,
            random_state=config.random_state,
            n_jobs=-1
        )
    
    def train(self, X_train, y_train, X_val, y_val) -> Dict:
        self.model.fit(X_train, y_train)
        train_score = self.model.score(X_train, y_train)
        val_score = self.model.score(X_val, y_val)
        
        return {
            'train_score': train_score,
            'val_score': val_score
        }
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)
    
    def save(self, path: str) -> None:
        joblib.dump(self.model, path)
    
    def load(self, path: str) -> None:
        self.model = joblib.load(path)