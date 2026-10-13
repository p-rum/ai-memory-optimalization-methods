"""Named data sources used by the synthetic trading-support platform."""
def source(name):
    def decorator(fn):
        fn.source_name = name
        return fn
    return decorator

@source('portfolio_positions')
def load_positions():
    return {'symbol': 'AAPL', 'quantity': 100, 'largest_position_share': 0.60}

@source('market_closing_prices')
def load_closing_prices():
    return {'AAPL': {'week_start': 150.0, 'week_end': 155.0}}

@source('reference_fx_rates')
def load_fx_rates():
    return {'USD_EUR': 0.92}

@source('client_cashflows')
def load_cashflows():
    return {'available_cash': 20000.0, 'next_week_outflows': 30000.0}

@source('margin_snapshots')
def load_margin_snapshot():
    return {'equity': 100000.0, 'initial_margin': 50000.0}

@source('client_profiles')
def load_client_profile():
    return {'client_id': 'DEMO-001', 'report_currency': 'EUR'}
