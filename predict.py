from src.data.stock_data import fetch_stock_data
from src.features.feature_generator import add_technical_features
from src.models.stock_predictor import StockPredictor
from src.visualization.plotter import plot_predictions

def main():
    # Get stock symbol from user
    symbol = input("Enter stock symbol (e.g., AAPL): ").upper()
    
    # Fetch and process data
    df = fetch_stock_data(symbol)
    df = add_technical_features(df)
    
    # Initialize and train model
    predictor = StockPredictor()
    X_scaled, y, features = predictor.prepare_data(df)
    
    print("\nTraining model...")
    predictor.train(X_scaled, y)
    
    # Generate predictions
    print("\nGenerating future predictions...")
    future_predictions = predictor.predict_future(df)
    
    # Plot results
    plot_predictions(df, future_predictions)
    
    # Print predicted returns
    print("\nPredicted returns for the next 15 trading days:")
    for date, pred in future_predictions.items():
        print(f"{date.strftime('%Y-%m-%d')}: {pred:+.2%}")

if __name__ == "__main__":
    main()