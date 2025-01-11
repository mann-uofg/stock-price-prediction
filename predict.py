from src.data.stock_data import fetch_stock_data
from src.features.feature_generator import add_technical_features
from src.models.stock_predictor import StockPredictor
from src.visualization.plotter import plot_predictions
from src.data.scrapers.yahoo_finance import YahooFinanceScraper
from src.visualization.financial_plot import plot_financial_summary

def main():
    # Get stock symbol from user
    symbol = input("Enter stock symbol (e.g., AAPL): ").upper()
    
    # Initialize scraper and get additional data
    print("\nFetching financial data...")
    scraper = YahooFinanceScraper(symbol)
    analyst_data = scraper.get_analyst_data()
    earnings_data = scraper.get_earnings_data()
    financials = scraper.get_financials()
    
    # Show financial summary
    plot_financial_summary(symbol, analyst_data, earnings_data, financials)
    
    # Fetch and process data for price prediction
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

if __name__ == "__main__":
    main()
    