-- merge_pdf.lua: 把「总册」markdown 转为带正式封面 + 带页码目录的 LaTeX。
-- 1) 封面 H1 + 两行署名 → 居中、独占一页的封面（不进目录）；
-- 2) 手工「目录」清单 → LaTeX \tableofcontents（自动按页码生成，tocdepth=1 只列章）；
-- 其余章节原样保留，\newpage 分页标记来自 markdown 原文。
local cover_done = false
local drop_next = 0      -- 封面标题后待删除的段落数（2 行署名）
local drop_list = false  -- 「目录」后待删除的手工清单

function Header(el)
  local text = pandoc.utils.stringify(el.content)
  if el.level ~= 1 then return nil end
  if not cover_done then
    cover_done = true
    drop_next = 2
    return pandoc.RawBlock('latex',
      '\\thispagestyle{plain}\n' ..
      '\\begin{center}\n' ..
      '\\vspace*{1.5cm}\n' ..
      '{\\fontsize{14pt}{20pt}\\selectfont 成都锦城学院}\n' ..
      '\n' ..
      '\\vspace{0.5cm}\n' ..
      '\\rule{10cm}{0.4pt}\n' ..
      '\n' ..
      '\\vspace{6.5cm}\n' ..
      '{\\fontsize{32pt}{44pt}\\selectfont\\heiti ' .. text .. '}\n' ..
      '\n' ..
      '\\vspace{0.9cm}\n' ..
      '{\\fontsize{16pt}{22pt}\\selectfont 期末考试 / 考研 通用版}\n' ..
      '\n' ..
      '\\vspace{1.1cm}\n' ..
      '\\rule{6cm}{0.5pt}\n' ..
      '\n' ..
      '\\vspace{4.5cm}\n' ..
      '{\\fontsize{14pt}{20pt}\\selectfont\\kaishu 整理：李尚儒　·　成都锦城学院}\n' ..
      '\\end{center}\n')
  end
  if text == '目录' then
    drop_list = true
    return pandoc.RawBlock('latex',
      '\\setcounter{tocdepth}{1}\n' ..
      '\\begin{center}\n{\\fontsize{18pt}{24pt}\\selectfont\\heiti 目录}\n\\end{center}\n' ..
      '\\tableofcontents\n')
  end
  return nil
end

function Para(el)
  if drop_next > 0 then
    drop_next = drop_next - 1
    return {}
  end
  return nil
end

function BulletList(el)
  if drop_list then
    drop_list = false
    return {}
  end
  return nil
end
