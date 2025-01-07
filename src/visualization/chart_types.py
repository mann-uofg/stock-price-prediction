"""Different chart type implementations"""
import mplfinance as mpf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_candlestick(ax1, data):
    """Plot candlestick chart"""
    # Prepare data for mplfinance
    df = data.copy()
    
    # Ensure OHLCV columns are present and in correct order
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    
    # Create mplfinance style
    style = mpf.make_mpf_style(
        marketcolors=mpf.make_marketcolors(
            up='green',
            down='red',
            edge='inherit',
            wick='inherit',
            volume='gray'
        ),
        gridstyle='--',
        gridcolor='gray',
        gridaxis='both',
        rc={'axes.grid': True}
    )
    
    # Plot candlesticks
    mpf.plot(
        df,
        type='candle',
        style=style,
        ax=ax1,
        volume=False,
        warn_too_much_data=10000,
        update_width_config=dict(
            candle_linewidth=0.8,
            candle_width=0.6
        )
    )

def plot_line(ax1, data):
    """Plot line chart"""
    line = ax1.plot(data.index, data['Close'], 
                   label='Historical', 
                   color='blue', 
                   linewidth=1.5)
    return line

def plot_prediction_line(ax1, dates, prices, color='red'):
    """Plot prediction line"""
    line = ax1.plot(dates, prices, 
                   label='Predicted', 
                   color=color, 
                   linestyle='--', 
                   linewidth=1.5)
    return line