"""Execute and verify the synthetic banking examples; no API or private data."""
import json
from bank_demo.report import generate_weekly_report
from bank_demo.api import get_trader_dashboard
from bank_demo.registry import deployed_mechanism
from bank_demo.health import calculate_margin_buffer

def run():
    report = generate_weekly_report()
    assert report['weekly_pnl'] == 460.0
    assert report['financial_health']['score'] == 54.67
    assert report['mechanism_version'] == 'health-v2'
    assert get_trader_dashboard()['health']['score'] == report['financial_health']['score']
    assert deployed_mechanism('2026-09-30')['id'] == 'health-v1'
    assert deployed_mechanism('2026-10-01')['id'] == 'health-v2'
    assert deployed_mechanism('2026-11-02')['id'] != 'health-v3-draft'
    assert calculate_margin_buffer(100000,80000) < calculate_margin_buffer(100000,50000)
    for equity in [0,-1]:
        try: calculate_margin_buffer(equity,50000)
        except ValueError: pass
        else: raise AssertionError('invalid equity accepted')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return report
if __name__ == '__main__': run()
