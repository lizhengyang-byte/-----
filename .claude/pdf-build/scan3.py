import subprocess, json, sys
sys.stdout.reconfigure(encoding='utf-8')
p = subprocess.run(['pandoc', '-f', 'markdown', '-t', 'json', '01-土的物理性质与分类.md'],
                   capture_output=True, encoding='utf-8')
doc = json.loads(p.stdout)

def walk(n):
    if isinstance(n, dict):
        if n.get('t') == 'Math':
            yield n
        c = n.get('c')
        if isinstance(c, list):
            for x in c:
                yield from walk(x)
        elif isinstance(c, dict):
            yield from walk(c)

total = 0
for m in walk({'t': 'ROOT', 'c': doc['blocks']}):
    total += 1
    t = m['c'][1]
    if '60' in t or '12289' in t or '、' in t:
        print('FOUND MATH:', repr(t))
        for ch in t:
            o = ord(ch)
            if o > 127:
                print('   non-ascii:', repr(ch), 'U+%04X' % o)
print('total math elements in ch01:', total)
