"""Post-process pandoc-generated .tex:
Wrap bare non-ASCII characters that sit directly in math segments (outside any
\\text{...}/\\mathrm{...} group) in \\text{...}, so xeCJK renders them with the
CJK font (Latin Modern Math has no glyphs for 、稳倾 etc).

Usage: fixtex.py <in.tex> [<out.tex>]   (in-place when no out given)
"""
import re, sys

PROTECTED = r'(?:text|textnormal|mathrm|textbf|textit|mbox|textsf|ensuremath)'

def find_text_groups(s):
    """Return list of (start,end) indexes of \\<cmd>{...} protected groups."""
    spans = []
    for m in re.finditer(r'\\' + PROTECTED + r'\s*\{', s):
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
        spans.append((m.start(), j + 1))
    return spans

def process_segment(seg):
    spans = find_text_groups(seg)
    out = []
    for idx, ch in enumerate(seg):
        protected = any(a <= idx < b for a, b in spans)
        if ord(ch) > 127 and not protected:
            out.append('\\text{%s}' % ch)
        else:
            out.append(ch)
    return ''.join(out)

def fix(src):
    # inline math \( ... \) ; display math \[ ... \]
    src = re.sub(r'\\\((.*?)\\\)',
                 lambda m: '\\(' + process_segment(m.group(1)) + '\\)',
                 src, flags=re.S)
    src = re.sub(r'\\\[(.*?)\\\]',
                 lambda m: '\\[' + process_segment(m.group(1)) + '\\]',
                 src, flags=re.S)
    return src

def main():
    src = open(sys.argv[1], encoding='utf-8').read()
    out = fix(src)
    if len(sys.argv) > 2:
        open(sys.argv[2], 'w', encoding='utf-8').write(out)
    else:
        open(sys.argv[1], 'w', encoding='utf-8').write(out)

if __name__ == '__main__':
    main()
