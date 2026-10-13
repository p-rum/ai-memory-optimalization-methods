"""Weekly report for traders on the synthetic support platform."""
from .sources import load_client_profile
from .pnl import calculate_weekly_pnl
from .health import calculate_financial_health
from .registry import deployed_mechanism

def generate_weekly_report():
    profile = load_client_profile()
    mechanism = deployed_mechanism()
    return {'client': profile['client_id'], 'currency': profile['report_currency'], 'weekly_pnl': calculate_weekly_pnl(), 'financial_health': calculate_financial_health(mechanism['weights']), 'mechanism_version': mechanism['id']}
