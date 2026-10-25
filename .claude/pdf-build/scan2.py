import subprocess, json, sys
sys.stdout.reconfigure(encoding='utf-8')
p = subprocess.run(['pandoc', '-f', 'markdown', '-t', 'json', '01-土的物理性质与分类.md'],
                   capture_output=True, encoding='utf-8')
doc = json.loads(p.stdout)

def walk(n):
    if n.get('t') == 'Math':
        yield n
    c = n.get('c')
    if isinstance(c, list):
        for x in c:
            if isinstance(x, dict):
                yield from walk(x)

for m in walk({'t': 'ROOT', 'c': doc['blocks']}):
    t = m['c'][1]
    if '60' in t or '、' in t or '12289' in t:
        print('MATH:', repr(t))
        for ch in t:
            if ord(ch) > 127:
                print('   non-ascii char:', repr(ch), hex(ord(ch)))
