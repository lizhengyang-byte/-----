"""合并土力学各章为总册 Markdown：封面 + 目录 + 章节（不含 README）。
章节之间插入 pandoc 的 \newpage 原语，供 PDF 分页；预览时以代码块显示。
"""
import io, os, sys

sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(BASE))

CHAPTERS = [
    ('00-全书公式速查总表.md',      '全书公式速查总表'),
    ('01-土的物理性质与分类.md',     '第一章 土的物理性质与工程分类'),
    ('02-土的渗透性与渗流.md',       '第二章 土的渗透性与渗流'),
    ('03-土中应力计算.md',           '第三章 土中应力计算'),
    ('04-土的压缩性与地基沉降计算.md','第四章 土的压缩性与地基沉降计算'),
    ('05-土的抗剪强度.md',           '第五章 土的抗剪强度'),
    ('06-土压力与挡土墙.md',         '第六章 土压力与挡土墙'),
    ('07-土坡稳定分析.md',           '第七章 土坡稳定分析'),
    ('08-地基承载力.md',             '第八章 地基承载力'),
]

NEWPAGE = '```{=latex}\n\\newpage\n```'

def anchor(title):
    # pandoc 自动标识符：空格 → 连字符，保留 CJK/字母数字
    return title.replace(' ', '-')

parts = []

# ---------- 封面 ----------
parts.append('''# 土力学速查手册

**期末考试 / 考研 通用版**

**整理：李尚儒　·　成都锦城学院**
''')
parts.append(NEWPAGE)

# ---------- 目录 ----------
toc_lines = ['# 目录', '']
for fn, title in CHAPTERS:
    toc_lines.append('- [%s](#%s)' % (title, anchor(title)))
toc_lines.append('')
parts.append('\n'.join(toc_lines))
parts.append(NEWPAGE)

# ---------- 章节正文 ----------
for fn, title in CHAPTERS:
    path = os.path.join(ROOT, 'markdown版本', fn)
    with io.open(path, encoding='utf-8') as f:
        body = f.read().strip()
    parts.append('<!-- ================ %s ================ -->' % title)
    parts.append('')
    parts.append(body)
    parts.append('')
    parts.append(NEWPAGE)

out = '\n\n'.join(parts).rstrip() + '\n'

dest = os.path.join(ROOT, 'markdown版本', '土力学速查手册-总册.md')
with io.open(dest, 'w', encoding='utf-8') as f:
    f.write(out)
print('已生成：', dest)
print('总行数：', out.count('\n') + 1, '，章节数：', len(CHAPTERS))
