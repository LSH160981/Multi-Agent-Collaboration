#!/usr/bin/env python3
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EXAMPLE = REPO / 'examples' / 'tests' / 'session-probe-example.json'


def main():
    obj = json.loads(EXAMPLE.read_text(encoding='utf-8'))
    required_top = ['session_count', 'stale_minutes', 'action_legend', 'sessions']
    required_actions = ['probe', 'resume', 'redispatch', 'rebuild']

    missing_top = [k for k in required_top if k not in obj]
    action_legend = obj.get('action_legend', {})
    missing_actions = [k for k in required_actions if k not in action_legend]

    sessions = obj.get('sessions', [])
    sample_ok = bool(sessions) and all(k in sessions[0] for k in ['age_minutes', 'recommended_action'])

    report = {
        'example': str(EXAMPLE),
        'missing_top': missing_top,
        'missing_actions': missing_actions,
        'sample_ok': sample_ok,
        'status': 'ok' if not missing_top and not missing_actions and sample_ok else 'fail',
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report['status'] == 'ok' else 1)


if __name__ == '__main__':
    main()
