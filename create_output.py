import json
p = json.load(open('raw_results.json'))
summary = {
    'tests_run': p.get('summary', {}).get('total', 0),
    'tests_failed': p.get('summary', {}).get('failed', 0),
    'tests_passed': p.get('summary', {}).get('passed', 0),
    'tests_skipped': p.get('summary', {}).get('skipped', 0),
}
open('output.json','w').write(json.dumps(summary, indent=2))
print('Generated output.json')
