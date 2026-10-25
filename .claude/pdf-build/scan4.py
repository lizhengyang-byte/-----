import subprocess, json, sys
sys.stdout.reconfigure(encoding='utf-8')
p = subprocess.run(['pandoc', '-f', 'markdown', '-t', 'json', '01-土的物理性质与分类.md'],
                   capture_output=True, encoding='utf-8')
raw = p.stdout
print('contains literal ideographic comma in raw JSON:', '、' in raw)
print('contains \\\\12289 (backslash digits) in raw JSON:', '12289' in raw)

doc = json.loads(raw)
# Dump every Math element text
def walk(n):
    if isinstance(n, dict):
        if n.get('t') == 'Math':
            yield n['c'][1]
        c = n.get('c')
        if isinstance(c, list):
            for x in c:
                yield from walk(x)
        elif isinstance(c, dict):
            yield from walk(c)
maths = list(walk({'t': 'ROOT', 'c': doc['blocks']}))
print('n math:', len(maths))
for t in maths:
    print('  MATH:', repr(t))
