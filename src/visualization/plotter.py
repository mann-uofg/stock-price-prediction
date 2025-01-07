"""Main plotting functionality"""
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import mplcursors
from .hover_annotations import add_hover_annotations

def plot_predictions(df, future_predictions):
    """Plot historical prices and future predictions"""
    # Calculate future prices
    last_close = df['Close'].iloc[-1]
    future_prices = [last_close]
    for ret in future_predictions:
        next_price = future_prices[-1] * (1 + ret)
        future_prices.append(next_price)
    future_prices = future_prices[1:]
    
    # Get last 6 months of data
    days_6m = 180  # Approximately 6 months of trading days
    last_6m = df.iloc[-days_6m:] if len(df) > days_6m else df
    
    # Create figure and axes
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 8), height_ratios=[3, 1], gridspec_kw={'hspace': 0.3})
    
    # Plot historical prices
    historical_line = ax1.plot(last_6m.index, last_6m['Close'], 
                             label='Historical', color='blue', linewidth=1.5)
    
    # Plot predictions
    prediction_line = ax1.plot(future_predictions.index, future_prices,
                             label='Predicted', color='red', linestyle='--', linewidth=1.5)
    
    # Plot volume
    ax2.bar(last_6m.index, last_6m['Volume'], color='gray', alpha=0.5)
    
    # Format dates
    date_formatter = DateFormatter('%Y-%m-%d')
    ax1.xaxis.set_major_formatter(date_formatter)
    ax2.xaxis.set_major_formatter(date_formatter)
    
    # Rotate and align tick labels
    plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
    plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
    
    # Add gridlines
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax2.grid(True, linestyle='--', alpha=0.6)
    
    # Add hover annotations
    add_hover_annotations([*historical_line, *prediction_line])
    
    # Set titles and labels
    ax1.set_title('Stock Price Prediction', fontsize=14, pad=20)
    ax1.set_ylabel('Price ($)', fontsize=12)
    ax2.set_ylabel('Volume', fontsize=12)
    ax1.legend(loc='upper left')
    
    # Adjust layout and display
    plt.tight_layout()
    plt.show()