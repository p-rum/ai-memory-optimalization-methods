"""Select deployed mechanism by validity date, not by document similarity."""
import json
from pathlib import Path

def deployed_mechanism(as_of='2026-10-13'):
    versions = json.loads(Path(__file__).with_name('mechanisms.json').read_text())
    matches = [v for v in versions if v['status'] == 'deployed' and v['valid_from'] <= as_of and (v['valid_to'] is None or as_of < v['valid_to'])]
    if len(matches) != 1:
        raise ValueError('no unique deployed version')
    return matches[0]
