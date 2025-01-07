import numpy as np
from typing import Dict
from sklearn.metrics import mean_squared_error, mean_absolute_error

class EvaluationMetrics:
    @staticmethod
    def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict:
        """Calculate various performance metrics."""
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mae = mean_absolute_error(y_true, y_pred)
        
        # Directional accuracy
        direction_true = np.sign(np.diff(y_true))
        direction_pred = np.sign(np.diff(y_pred))
        directional_accuracy = np.mean(direction_true == direction_pred)
        
        return {
            'rmse': rmse,
            'mae': mae,
            'directional_accuracy': directional_accuracy
        }