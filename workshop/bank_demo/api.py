"""Trader dashboard consumes the same financial-health calculation as reports."""
from .health import calculate_financial_health
from .registry import deployed_mechanism

def get_trader_dashboard():
    version = deployed_mechanism()
    return {'client': 'DEMO-001', 'health': calculate_financial_health(version['weights']), 'version': version['id']}
