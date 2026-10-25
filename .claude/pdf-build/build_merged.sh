#!/bin/bash
# 构建「总册」PDF：封面 + 带页码目录 + 各章（每章新起一页）
# 流程同 build.sh，但额外套用 merge_pdf.lua（封面居中、目录换成 \tableofcontents）
set -u
cd "$(dirname "$0")/../.." || exit 1
SRC="$(pwd)"
BUILD="$SRC/.claude/pdf-build"
TEX="$BUILD/tex"
OUT="$SRC/PDF导出"
LOG="$SRC/latex_log"
mkdir -p "$OUT" "$LOG"

NAME="土力学速查手册-总册"
MD="$SRC/markdown版本/$NAME.md"

echo "pandoc → tex …"
pandoc -s "$MD" -t latex -o "$TEX/$NAME.tex" \
  -H "$BUILD/header.tex" \
  --lua-filter "$BUILD/fix.lua" \
  --lua-filter "$BUILD/merge_pdf.lua" \
  -V geometry="a4paper, hmargin=2.2cm, vmargin=2.4cm, headheight=14.5pt, footskip=0.9cm, includehead, includefoot" \
  -V colorlinks=true -V linkcolor=black -V urlcolor=black -V citecolor=black \
  || { echo "pandoc 失败"; exit 1; }

echo "fixtex …"
python -I "$BUILD/fixtex.py" "$TEX/$NAME.tex" || { echo "fixtex 失败"; exit 1; }

echo "xelatex（第 1 遍）…"
xelatex -interaction=nonstopmode -halt-on-error -jobname "$NAME" \
  -aux-directory="$LOG" -output-directory="$OUT" "$TEX/$NAME.tex" >/dev/null 2>&1 \
  || { echo "xelatex 失败"; tail -15 "$LOG/$NAME.log"; exit 1; }
echo "xelatex（第 2 遍，生成目录页码）…"
xelatex -interaction=nonstopmode -halt-on-error -jobname "$NAME" \
  -aux-directory="$LOG" -output-directory="$OUT" "$TEX/$NAME.tex" >/dev/null 2>&1 \
  || { echo "xelatex 第 2 遍失败"; tail -15 "$LOG/$NAME.log"; exit 1; }

echo "检查缺字 …"
if grep -q "Missing character" "$LOG/$NAME.log"; then
  echo "!!! 日志含 Missing character 警告，需人工查看：$LOG/$NAME.log"
else
  echo "无缺字警告 ✓"
fi

echo "完成：$OUT/$NAME.pdf"
