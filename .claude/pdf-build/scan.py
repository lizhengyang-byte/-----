import subprocess, json, glob, sys, re
sys.stdout.reconfigure(encoding='utf-8')

def walk(n):
    """Robust AST walker: recurse into lists AND dicts."""
    if isinstance(n, list):
        for x in n:
            yield from walk(x)
    elif isinstance(n, dict):
        if n.get('t') in ('Math', 'Str'):
            yield n
        c = n.get('c')
        if isinstance(c, (list, dict)):
            yield from walk(c)

def direct_nonascii(latex_src):
    """Return chars that are non-ASCII and NOT inside a \\text{...} / \\mathrm{...}
    group in the math source."""
    direct = []
    in_text = []
    i = 0
    n = len(latex_src)
    # stack of depths: when we see \text{ or similar, push
    while i < n:
        ch = latex_src[i]
        if ch == '\\':
            m = re.match(r'\\([A-Za-z]+)', latex_src[i:])
            if m:
                cmd = m.group(1)
                i += len(m.group(0))
                # check for following brace group
                if i < n and latex_src[i] == '{':
                    # find matching close brace (simple depth count)
                    j = i
                    depth = 0
                    while j < n:
                        if latex_src[j] == '{':
                            depth += 1
                        elif latex_src[j] == '}':
                            depth -= 1
                            if depth == 0:
                                break
                        j += 1
                    inner = latex_src[i+1:j]
                    if cmd in ('text', 'textnormal', 'mathrm', 'textbf', 'textit', 'mbox', 'ensuremath'):
                        # treat whole inner as text context; only chars in inner:
                        in_text.extend(inner)
                    else:
                        # recurse into inner (e.g. \frac{...}{...}) — track separately
                        direct.extend(direct_nonascii(inner)[0])
                    i = j + 1
                else:
                    i += 1
            else:
                i += 1
        elif ord(ch) > 127:
            direct.append(ch)
            i += 1
        else:
            i += 1
    return direct, in_text

math_direct = {}
math_text = {}
text_chars = {}

for f in sorted(glob.glob('*.md')):
    p = subprocess.run(['pandoc', '-f', 'markdown', '-t', 'json', f],
                       capture_output=True, encoding='utf-8')
    doc = json.loads(p.stdout)
    for n in walk({'t': 'ROOT', 'c': doc['blocks']}):
        if n['t'] == 'Math':
            src = n['c'][1]
            d, t = direct_nonascii(src)
            for ch in d:
                math_direct.setdefault(ch, set()).add(f)
            for ch in t:
                math_text.setdefault(ch, set()).add(f)
        else:
            for ch in n['c']:
                if ord(ch) > 127:
                    text_chars.setdefault(ch, set()).add(f)

print('== 数学中【直接出现】的非ASCII（需处理）==')
for ch, fs in sorted(math_direct.items(), key=lambda x: ord(x[0])):
    print('  %r U+%04X  in %s' % (ch, ord(ch), sorted(fs)))
print('== 数学中【在 \\text{} 内】的非ASCII（xeCJK已处理）==')
for ch, fs in sorted(math_text.items(), key=lambda x: ord(x[0])):
    print('  %r U+%04X  in %s' % (ch, ord(ch), sorted(fs)))
print('== 正文Str中的非ASCII（非CJK、非拉丁-1的需关注）==')
def cjk(o):
    return (0x4E00 <= o <= 0x9FFF) or (0x3000 <= o <= 0x30FF) \
        or (0x2000 <= o <= 0x2FFF) or (0x3400 <= o <= 0x4DBF) \
        or (0xF900 <= o <= 0xFAFF)
for ch, fs in sorted(text_chars.items(), key=lambda x: ord(x[0])):
    o = ord(ch)
    if not (cjk(o) or (0xA0 <= o <= 0x24F)):
        print('  %r U+%04X  in %s' % (ch, o, sorted(fs)))
