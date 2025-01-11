import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict, Any

def format_financial_value(value: float, metric: str) -> str:
    """Format financial values with appropriate units"""
    if value is None:
        return 'N/A'
        
    if metric == 'market_cap':
        if value >= 1e12:
            return f'${value/1e12:.2f}T'
        if value >= 1e9:
            return f'${value/1e9:.2f}B'
        if value >= 1e6:
            return f'${value/1e6:.2f}M'
    elif metric == 'revenue':
        if value >= 1e9:
            return f'${value/1e9:.2f}B'
        if value >= 1e6:
            return f'${value/1e6:.2f}M'
    elif metric in ['pe_ratio', 'beta']:
        return f'{value:.2f}'
    elif metric == 'profit_margins':
        return f'{value*100:.1f}%'
    elif metric == 'dividend_yield':
        return f'{value*100:.2f}%' if value else 'No Div'
    elif metric == 'eps':
        return f'${value:.2f}'
    
    return f'${value:,.2f}'

def plot_financial_summary(symbol: str, analyst_data: Dict[str, Any], earnings_data: Dict[str, Any], financials: Dict[str, Any]):
    """Create a comprehensive financial summary plot"""
    plt.style.use('bmh')
    fig = plt.figure(figsize=(15, 10))
    
    gs = plt.GridSpec(3, 2, figure=fig)
    
    # Price Targets subplot
    ax1 = fig.add_subplot(gs[0, 0])
    if analyst_data:
        current_price = analyst_data.get('current_price', 0)
        target_prices = [
            analyst_data.get('target_low_price', current_price),
            current_price,
            analyst_data.get('target_mean_price', current_price),
            analyst_data.get('target_high_price', current_price)
        ]
        ax1.plot(['Target Low', 'Current', 'Target Mean', 'Target High'], 
                target_prices, 'bo-')
        ax1.set_title('Analyst Price Targets')
        # Add price labels above points
        for i, price in enumerate(target_prices):
            if price:
                ax1.annotate(f'${price:,.2f}', 
                           (i, price), 
                           textcoords="offset points", 
                           xytext=(0,10), 
                           ha='center')
        ax1.grid(True)
    
    # Earnings subplot
    ax2 = fig.add_subplot(gs[0, 1])
    if earnings_data and earnings_data.get('historical_earnings') is not None:
        earnings = earnings_data['historical_earnings']
        if not isinstance(earnings, str) and not earnings.empty:
            ax2.bar(earnings.index.astype(str), earnings['Earnings'])
            ax2.set_title('Historical Earnings (Quarterly)')
            # Format earnings values
            for i, v in enumerate(earnings['Earnings']):
                ax2.text(i, v, f'${v/1e9:.1f}B' if abs(v) >= 1e9 else f'${v/1e6:.1f}M',
                        ha='center', va='bottom')
            ax2.grid(True)
        else:
            ax2.text(0.5, 0.5, 'No earnings data available',
                    ha='center', va='center',
                    transform=ax2.transAxes)
            ax2.set_title('Historical Earnings (Quarterly)')
    else:
        ax2.text(0.5, 0.5, 'No earnings data available',
                ha='center', va='center',
                transform=ax2.transAxes)
        ax2.set_title('Historical Earnings (Quarterly)')
    
    # Financial Metrics
    ax3 = fig.add_subplot(gs[1, :])
    if financials:
        metrics = {k: v for k, v in financials.items() if v is not None}
        if metrics:
            # Create formatted labels
            formatted_metrics = {}
            for k, v in metrics.items():
                formatted_value = format_financial_value(v, k)
                formatted_key = k.replace('_', ' ').title()
                formatted_metrics[formatted_key] = v
            
            # Plot bars
            bars = ax3.bar(formatted_metrics.keys(), formatted_metrics.values())
            ax3.set_title('Key Financial Metrics')
            ax3.tick_params(axis='x', rotation=45)
            
            # Add value labels on top of bars
            for bar, (metric, value) in zip(bars, metrics.items()):
                formatted_value = format_financial_value(value, metric)
                ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                        formatted_value,
                        ha='center', va='bottom')
            ax3.grid(True)
    
    # Add summary text
    ax4 = fig.add_subplot(gs[2, :])
    ax4.axis('off')
    
    # Format the next earnings date
    next_earnings = earnings_data.get('next_earnings_date')
    if isinstance(next_earnings, pd.Timestamp):
        next_earnings_str = next_earnings.strftime('%Y-%m-%d')
    else:
        next_earnings_str = 'N/A'
    
    # Format current price and target
    current_price = analyst_data.get('current_price')
    mean_target = analyst_data.get('target_mean_price')
    current_price_str = f"${current_price:,.2f}" if current_price else 'N/A'
    mean_target_str = f"${mean_target:,.2f}" if mean_target else 'N/A'
    
    # Calculate potential return
    if current_price and mean_target:
        potential_return = ((mean_target - current_price) / current_price) * 100
        potential_return_str = f"{potential_return:+.1f}% potential return"
    else:
        potential_return_str = "N/A"
    
    summary_text = f"""
    {symbol} Financial Summary
    
    Next Earnings Date: {next_earnings_str}
    Number of Analysts: {analyst_data.get('number_of_analysts', 'N/A')}
    Current Price: {current_price_str}
    Mean Target: {mean_target_str}
    {potential_return_str}
    """
    ax4.text(0.1, 0.5, summary_text, fontsize=12, verticalalignment='center')
    
    plt.tight_layout()
    plt.show(block=False)
