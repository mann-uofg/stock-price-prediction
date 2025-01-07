"""Hover annotations for matplotlib plots"""
import mplcursors
import matplotlib.dates as mdates
import pandas as pd

def add_hover_annotations(lines):
    """Add hover annotations to the plot lines"""
    for line in lines:
        cursor = mplcursors.cursor(line, hover=True)
        
        def create_annotation(sel):
            """Create the hover annotation text"""
            x, y = sel.target
            
            # Handle both datetime and float x-values
            if isinstance(x, (pd.Timestamp, pd.DatetimeIndex)):
                date_str = x.strftime('%Y-%m-%d')
            else:
                try:
                    date = mdates.num2date(x)
                    date_str = date.strftime('%Y-%m-%d')
                except:
                    date_str = 'N/A'
            
            return f'Date: {date_str}\nPrice: ${y:.2f}'
        
        cursor.connect("add", lambda sel: sel.annotation.set_text(
            create_annotation(sel)))