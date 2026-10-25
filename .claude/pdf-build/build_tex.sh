#!/bin/bash
# 为全部 Markdown 文档生成 LaTeX 版本（内嵌 header.tex 模板），输出到 /LaTeX版本
# 每个 .tex 独立自包含，用 xelatex 直接编译即可得到与 PDF导出 相同版式的 PDF。
# 总册额外套用 merge_pdf.lua（封面居中 + 带页码目录）。
set -u
cd "$(dirname "$0")/../.." || exit 1
SRC="$(pwd)"
BUILD="$SRC/.claude/pdf-build"
MDDIR="$SRC/markdown版本"
OUT="$SRC/LaTeX版本"
LOG="$SRC/latex_log"
mkdir -p "$OUT" "$LOG"

COMMON=(
  -H "$BUILD/header.tex"
  --lua-filter "$BUILD/fix.lua"
  -V geometry="a4paper, hmargin=2.2cm, vmargin=2.4cm, headheight=14.5pt, footskip=0.9cm, includehead, includefoot"
  -V colorlinks=true -V linkcolor=black -V urlcolor=black -V citecolor=black
)

fail=0
for f in "$MDDIR"/*.md; do
  name="$(basename "$f" .md)"
  tex="$OUT/$name.tex"
  filters=("${COMMON[@]}")
  [ "$name" = "土力学速查手册-总册" ] && filters+=("--lua-filter" "$BUILD/merge_pdf.lua")
  if ! pandoc -s "$f" -t latex -o "$tex" "${filters[@]}" 2>"$LOG/$name.err"; then
    echo "✗ $name  pandoc 失败"; cat "$LOG/$name.err"; fail=1; continue
  fi
  if ! python -I "$BUILD/fixtex.py" "$tex" 2>>"$LOG/$name.err"; then
    echo "✗ $name  fixtex 失败"; cat "$LOG/$name.err"; fail=1; continue
  fi
  rm -f "$LOG/$name.err"
  echo "✓ $name.tex"
done

[ "$fail" -eq 0 ] && echo "全部 LaTeX 版本已生成：$OUT/" || echo "存在失败，请查看日志"
exit "$fail"
