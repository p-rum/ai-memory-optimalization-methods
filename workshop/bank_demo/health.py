"""Illustrative score, NOT an actual bank scoring rule or credit decision."""
from .sources import load_cashflows, load_margin_snapshot, load_positions

def calculate_liquidity_component(cash, outflows):
    if outflows <= 0:
        raise ValueError('outflows must be positive')
    return max(0.0, min(1.0, cash / outflows / 2.0))

def calculate_margin_buffer(equity, initial_margin):
    if equity <= 0:
        raise ValueError('equity must be positive')
    return max(0.0, min(1.0, ((equity - initial_margin) / equity) / 0.5))

def calculate_diversification(largest_position_share):
    if not 0.0 <= largest_position_share <= 1.0:
        raise ValueError('share must be between 0 and 1')
    return 1.0 - largest_position_share

def calculate_financial_health(weights):
    cashflows = load_cashflows()
    margins = load_margin_snapshot()
    position = load_positions()
    liquidity = calculate_liquidity_component(cashflows['available_cash'], cashflows['next_week_outflows'])
    margin = calculate_margin_buffer(margins['equity'], margins['initial_margin'])
    diversification = calculate_diversification(position['largest_position_share'])
    score = 100.0 * (weights['liquidity'] * liquidity + weights['margin'] * margin + weights['diversification'] * diversification)
    return {'score': round(score, 2), 'components': {'liquidity': liquidity, 'margin': margin, 'diversification': diversification}}
