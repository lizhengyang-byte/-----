"""Scan generated .tex for non-ASCII chars that sit bare inside math segments
(i.e. not inside a \\text{...}/\\mathrm{...} group). These would render as
missing glyphs in Latin Modern Math."""
import re, glob, sys
sys.stdout.reconfigure(encoding='utf-8')

def find_text_groups(s):
    """Return list of (start,end) byte indexes of \\text{...}-style protected groups."""
    spans = []
    for m in re.finditer(r'\\(?:text|textnormal|mathrm|textbf|textit|mbox|textsf|ensuremath)\s*\{', s):
        start = m.start()
        i = s.index('{', m.start())
        j = i
        depth = 0
        while j < len(s):
            if s[j] == '{':
                depth += 1
            elif s[j] == '}':
                depth -= 1
                if depth == 0:
                    break
            j += 1
        spans.append((start, j + 1))
    return spans

def is_inside(i, spans):
    return any(a <= i < b for a, b in spans)

for f in sorted(glob.glob('.claude/pdf-build/tex/*.tex')):
    src = open(f, encoding='utf-8').read()
    issues = []
    # inline math \( ... \)  and display math \[ ... \]
    for m in re.finditer(r'\\\((.*?)\\\)|\\\[(.*?)\\\]', src, re.S):
        seg = m.group(1) if m.group(1) is not None else m.group(2)
        base = m.start(1) if m.group(1) is not None else m.start(2)
        spans = find_text_groups(seg)
        for idx, ch in enumerate(seg):
            if ord(ch) > 127 and not is_inside(idx, spans):
                issues.append((base + idx, ch))
    if issues:
        print('###', f)
        for pos, ch in issues:
            line = src.count('\n', 0, pos) + 1
            ctx = src[max(0, pos - 40):pos + 40].replace('\n', ' ')
            print('  L%-4d %r U+%04X  ctx: …%s…' % (line, ch, ord(ch), ctx))
    else:
        print('###', f, '(clean)')
