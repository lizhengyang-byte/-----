#!/bin/bash
# 将全部 .md 导出为学术黑白 A4 PDF，输出到 /PDF导出
# 流程：pandoc -> .tex（Lua过滤器修正°等数学字符/emoji/链接）
#       -> fixtex.py（把数学中裸露的中文字符包进 \text{}）
#       -> xelatex -> PDF
set -u
cd "$(dirname "$0")/../.." || exit 1
SRC="$(pwd)"
BUILD="$SRC/.claude/pdf-build"
MDDIR="$SRC/markdown版本"
TEX="$BUILD/tex"
OUT="$SRC/PDF导出"
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
  tex="$TEX/$name.tex"
  pdf="$OUT/$name.pdf"
  printf '%-4s %s …' '' "$name"
  if ! pandoc -s "$f" -t latex -o "$tex" "${COMMON[@]}" 2>"$TEX/$name.err"; then
    echo "pandoc 失败"; cat "$TEX/$name.err"; fail=1; continue
  fi
  if ! python -I "$BUILD/fixtex.py" "$tex" 2>>"$TEX/$name.err"; then
    echo "fixtex 失败"; cat "$TEX/$name.err"; fail=1; continue
  fi
  if ! xelatex -interaction=nonstopmode -halt-on-error -jobname "$name" \
       -aux-directory="$LOG" -output-directory="$OUT" "$tex" >/dev/null 2>&1; then
    echo "xelatex 失败"; tail -15 "$LOG/$name.log"; fail=1; continue
  fi
  # 第二遍：解决 hyperref/longtable 的 rerun 警告
  xelatex -interaction=nonstopmode -halt-on-error -jobname "$name" \
       -aux-directory="$LOG" -output-directory="$OUT" "$tex" >/dev/null 2>&1
  echo "完成"
done

[ "$fail" -eq 0 ] && echo "全部导出成功" || echo "存在失败，请检查日志"
exit "$fail"
