from src.data.data_loader import DataLoader
from src.features.technical_indicators import TechnicalFeatures
from src.features.feature_engineering import FeatureEngineer
from src.data.data_splitter import DataSplitter
from src.models.lstm_model import LSTMModel
from src.models.random_forest_model import RandomForestModel
from src.evaluation.metrics import EvaluationMetrics
from src.visualization.visualizer import Visualizer
from src.utils.config import ModelConfig

def main():
    # Initialize configuration
    config = ModelConfig()
    
    # Create data loader
    data_loader = DataLoader(
        symbol=config.symbol,
        start_date='2020-01-01',
        end_date='2023-12-31'
    )
    
    try:
        # Load and process data
        df = data_loader.fetch_data()
        print(f"Successfully loaded data for {config.symbol}")
        
        # Add technical indicators
        df = TechnicalFeatures.add_technical_indicators(df)
        print("Added technical indicators")
        
        # Create features
        df, target = FeatureEngineer.create_features(
            df, 
            target_col=config.target_col,
            lookback_periods=config.lookback_periods
        )
        
        # Split data
        X_train, X_val, X_test, y_train, y_val, y_test, scaler = DataSplitter.train_val_test_split(
            df, target, config
        )
        
        # Train models
        models = {
            'lstm': LSTMModel(config),
            'rf': RandomForestModel(config)
        }
        
        results = {}
        for name, model in models.items():
            print(f"\nTraining {name.upper()} model...")
            history = model.train(X_train, y_train, X_val, y_val)
            
            # Make predictions
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            metrics = EvaluationMetrics.calculate_metrics(y_test, y_pred)
            results[name] = metrics
            
            # Visualize results
            Visualizer.plot_predictions(y_test, y_pred, f"{name.upper()} Predictions")
            print(f"{name.upper()} Metrics:", metrics)
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()