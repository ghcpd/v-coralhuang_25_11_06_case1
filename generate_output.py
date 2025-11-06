import json
import sys

# Simple converter from pytest-json-report to output.json summary
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: generate_output.py raw_results.json output.json')
        sys.exit(2)
    raw_path = sys.argv[1]
    out_path = sys.argv[2]

    with open(raw_path, 'r') as f:
        data = json.load(f)

    summary = {
        'summary': data.get('summary', {}),
        'tests': data.get('tests', []),
    }

    with open(out_path, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f'Wrote {out_path}')
