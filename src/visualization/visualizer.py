import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List

class Visualizer:
    @staticmethod
    def plot_predictions(y_true: List, y_pred: List, title: str) -> None:
        plt.figure(figsize=(12, 6))
        plt.plot(y_true, label='Actual')
        plt.plot(y_pred, label='Predicted')
        plt.title(title)
        plt.legend()
        plt.show()
    
    @staticmethod
    def plot_feature_importance(feature_names: List, importance: List) -> None:
        plt.figure(figsize=(10, 6))
        sns.barplot(x=importance, y=feature_names)
        plt.title('Feature Importance')
        plt.show()
    
    @staticmethod
    def plot_metrics_history(history: Dict) -> None:
        plt.figure(figsize=(12, 4))
        plt.plot(history['loss'], label='Training Loss')
        plt.plot(history['val_loss'], label='Validation Loss')
        plt.title('Model Loss Over Time')
        plt.legend()
        plt.show()