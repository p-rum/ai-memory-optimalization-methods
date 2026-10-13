"""Demonstration of one unchanged position; excludes intraweek trades and fees."""
from .sources import load_positions, load_closing_prices, load_fx_rates

def calculate_weekly_pnl():
    position = load_positions()
    prices = load_closing_prices()[position['symbol']]
    fx = load_fx_rates()['USD_EUR']
    return round(position['quantity'] * (prices['week_end'] - prices['week_start']) * fx, 2)
