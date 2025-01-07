import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from src.models.base_model import BaseModel
from typing import Dict

class LSTMModel(BaseModel):
    def __init__(self, config):
        self.config = config
        self.model = self._build_model()
    
    def _build_model(self) -> Sequential:
        model = Sequential([
            LSTM(units=self.config.lstm_units, 
                 return_sequences=True, 
                 input_shape=(None, self.config.n_features)),
            Dropout(0.2),
            LSTM(units=self.config.lstm_units//2),
            Dropout(0.2),
            Dense(1)
        ])
        
        model.compile(
            optimizer=Adam(learning_rate=self.config.learning_rate),
            loss='mse'
        )
        return model
    
    def train(self, X_train, y_train, X_val, y_val) -> Dict:
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=self.config.lstm_epochs,
            batch_size=self.config.batch_size,
            verbose=1
        )
        return history.history
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)
    
    def save(self, path: str) -> None:
        self.model.save(path)
    
    def load(self, path: str) -> None:
        self.model = load_model(path)