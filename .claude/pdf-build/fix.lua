-- fix.lua
-- 将 Markdown 源适配为学术黑白 PDF：
--  1) 数学环境内：裸 Unicode 字符替换为 LaTeX 命令（° → ^{\circ}、× → \times 等）
--  2) 正文文本：替换无法渲染的 emoji（⚠ → ◆ 等）
--  3) 链接：同库 .md 内部链接转为纯文本（PDF 中为死链）
local math_map = {
  ['°']='^{\\circ}', ['×']='\\times', ['÷']='\\div', ['−']='-',
  ['≈']='\\approx', ['≠']='\\neq',   ['≤']='\\leq',  ['≥']='\\geq',
  ['％']='\\%',     ['φ']='\\varphi', ['α']='\\alpha', ['β']='\\beta',
  ['γ']='\\gamma',  ['δ']='\\delta',  ['ε']='\\varepsilon', ['θ']='\\theta',
  ['τ']='\\tau',    ['π']='\\pi',     ['ρ']='\\rho',  ['σ']='\\sigma',
  ['ω']='\\omega',  ['μ']='\\mu',     ['λ']='\\lambda', ['Δ']='\\Delta',
  ['Φ']='\\Phi',    ['Ω']='\\Omega',  ['√']='\\sqrt{}', ['−']='-',
}

function Math(el)
  local t = el.text
  for k, v in pairs(math_map) do
    t = t:gsub(k, v)
  end
  el.text = t
  return el
end

function Str(el)
  local t = el.text
  t = t:gsub('⚠', '◆')
  t = t:gsub('✅', '■')
  t = t:gsub('❌', '□')
  t = t:gsub('☑', '□')
  el.text = t
  return el
end

function Link(el)
  -- 库内 .md 相对链接转为纯文本（避免 PDF 死链）
  if el.target:match('%.md$') then
    return el.content
  end
  return nil
end
