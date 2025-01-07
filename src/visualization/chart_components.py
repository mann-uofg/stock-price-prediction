"""Components for chart visualization"""
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.gridspec import GridSpec
import mplfinance as mpf

def setup_chart_layout(figsize=(15, 8)):
    """Create and setup the basic chart layout"""
    fig = plt.figure(figsize=figsize)
    gs = GridSpec(2, 1, height_ratios=[3, 1], hspace=0.3)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    return fig, ax1, ax2

def format_axes(ax1, ax2):
    """Format axes with common styling"""
    # Format dates
    date_formatter = DateFormatter('%Y-%m-%d')
    ax1.xaxis.set_major_formatter(date_formatter)
    ax2.xaxis.set_major_formatter(date_formatter)
    
    # Rotate and align tick labels
    plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
    plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
    
    # Add gridlines
    ax1.grid(True, which='both', linestyle='--', alpha=0.6)
    ax2.grid(True, which='both', linestyle='--', alpha=0.6)
    
    # Enable zooming and panning
    ax1.set_zorder(1)
    ax1.patch.set_visible(False)
    ax2.set_zorder(0)

def add_volume_subplot(ax2, data):
    """Add volume subplot"""
    ax2.bar(data.index, data['Volume'], color='gray', alpha=0.5)
    ax2.set_ylabel('Volume')