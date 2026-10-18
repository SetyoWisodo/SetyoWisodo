-- Pandoc Lua filter: custom book structures for Typst (print) and EPUB (ebook).
--   # Title {.part number="I"}          -> part page
--   # Title {.unnumbered}                -> unnumbered chapter-level heading
--   ::: {.box title="..." kind="note|action|local"} ... :::   -> callout box
--   ::: lead ... :::                     -> chapter lead paragraph
-- For Indonesian Typst output, soft hyphens are inserted following Indonesian
-- syllabification rules (Typst ships no Indonesian hyphenation patterns).

local fmt = FORMAT
local is_typst = fmt:match("typst") ~= nil
local lang = "en"

local function tesc(s)
  s = s:gsub("\\", "\\\\"):gsub('"', '\\"')
  return s
end

local function cesc(s) -- escape for typst content brackets
  return (s:gsub("([\\%[%]#%*_@<>`%$])", "\\%1"))
end

-- ---------------- Indonesian syllabification ----------------
local V = { a = true, e = true, i = true, o = true, u = true }
local DIGRAPH = { ng = true, ny = true, kh = true, sy = true }

local function units(w)
  local u, i = {}, 1
  while i <= #w do
    local two = w:sub(i, i + 1)
    if DIGRAPH[two] then
      table.insert(u, two); i = i + 2
    else
      table.insert(u, w:sub(i, i)); i = i + 1
    end
  end
  return u
end

local function syllabify(word)
  if #word < 7 or word:match("[^a-z]") then return nil end
  local u = units(word)
  local isv = {}
  for k, x in ipairs(u) do isv[k] = V[x] or false end
  local breaks = {}
  local k = 1
  -- find vowel positions
  local vpos = {}
  for j = 1, #u do if isv[j] then table.insert(vpos, j) end end
  for n = 1, #vpos - 1 do
    local a, b = vpos[n], vpos[n + 1]
    local nc = b - a - 1
    if nc == 1 then breaks[a] = true          -- V-CV
    elseif nc == 2 then breaks[a + 1] = true  -- VC-CV
    elseif nc >= 3 then breaks[a + 1] = true  -- VC-CCV
    end -- nc == 0 (VV): no break
  end
  local out, len = {}, 0
  local total = #word
  for j = 1, #u do
    table.insert(out, u[j]); len = len + #u[j]
    if breaks[j] and len >= 3 and (total - len) >= 3 then table.insert(out, "\u{00AD}") end
  end
  return table.concat(out)
end

local function hyph_id(s)
  return (s:gsub("(%a+)", function(w)
    if w:match("^%l+$") then return syllabify(w) or w end
    return w
  end))
end

-- ---------------- filters ----------------
function Meta(m)
  if m.lang then lang = pandoc.utils.stringify(m.lang) end
  return m
end

local function Header(h)
  if h.level ~= 1 then return nil end
  local title = pandoc.utils.stringify(h.content)
  if h.classes:includes("part") then
    if is_typst then
      local num = h.attributes["number"] or ""
      return pandoc.RawBlock("typst", string.format('#part-page(number: "%s", title: "%s", lang: "%s")', tesc(num), tesc(title), lang))
    else
      local num = h.attributes["number"] or ""
      local label = (lang == "id") and "Bagian " or "Part "
      h.content = { pandoc.Str(label .. num .. ": " .. title) }
      h.classes:insert("unnumbered")
      return h
    end
  end
  if is_typst and h.classes:includes("unnumbered") then
    local outlined = h.classes:includes("unlisted") and "false" or "true"
    return pandoc.RawBlock("typst", string.format('#heading(level: 1, numbering: none, outlined: %s)[%s]', outlined, cesc(title)))
  end
  return nil
end

local function Div(d)
  if d.classes:includes("box") then
    local title = d.attributes["title"] or ""
    local kind = d.attributes["kind"] or "note"
    if is_typst then
      local blocks = { pandoc.RawBlock("typst", string.format('#callout(title: "%s", kind: "%s")[', tesc(title), kind)) }
      for _, b in ipairs(d.content) do table.insert(blocks, b) end
      table.insert(blocks, pandoc.RawBlock("typst", "]"))
      return blocks
    else
      local c = { pandoc.Div({ pandoc.Para({ pandoc.Strong({ pandoc.Str(title) }) }) }, pandoc.Attr("", { "box-title" })) }
      for _, b in ipairs(d.content) do table.insert(c, b) end
      return pandoc.Div(c, pandoc.Attr("", { "box", "box-" .. kind }))
    end
  end
  if d.classes:includes("lead") then
    if is_typst then
      local blocks = { pandoc.RawBlock("typst", "#lead[") }
      for _, b in ipairs(d.content) do table.insert(blocks, b) end
      table.insert(blocks, pandoc.RawBlock("typst", "]"))
      return blocks
    end
  end
  if is_typst and (d.classes:includes("hanging") or d.classes:includes("plain")) then
    local rule = d.classes:includes("hanging")
      and "#set par(hanging-indent: 1.6em, first-line-indent: 0pt, justify: false, spacing: 0.75em)\n#set text(size: 8.9pt)"
      or "#set par(first-line-indent: 0pt, spacing: 0.85em)\n#set text(size: 9.6pt)"
    local blocks = { pandoc.RawBlock("typst", "#[\n" .. rule) }
    for _, b in ipairs(d.content) do table.insert(blocks, b) end
    table.insert(blocks, pandoc.RawBlock("typst", "]"))
    return blocks
  end
  if d.classes:includes("pagebreak") and is_typst then
    return pandoc.RawBlock("typst", "#pagebreak()")
  end
  return nil
end

local function Table(t)
  -- full-width tables with column widths proportional to content length, left-aligned
  local n = #t.colspecs
  local lens = {}
  for i = 1, n do lens[i] = 4 end
  local function scan(rows)
    for _, row in ipairs(rows) do
      for i, cell in ipairs(row.cells) do
        if i <= n then
          local l = #pandoc.utils.stringify(cell.contents)
          if l > lens[i] then lens[i] = l end
        end
      end
    end
  end
  scan(t.head.rows)
  for _, b in ipairs(t.bodies) do scan(b.body) end
  local total = 0
  for i = 1, n do lens[i] = math.min(math.max(lens[i], 8), 60); total = total + lens[i] end
  for i = 1, n do
    local al = t.colspecs[i][1]
    if al == "AlignDefault" or al == pandoc.AlignDefault then al = pandoc.AlignLeft end
    t.colspecs[i] = { al, lens[i] / total }
  end
  return t
end

local function Str(s)
  if is_typst and lang == "id" then
    s.text = hyph_id(s.text)
    return s
  end
end

local function Code() return nil end

return {
  { Meta = Meta },
  { Header = Header, Div = Div, Table = Table },
  { Str = Str, Code = Code, Link = function(l) return l end },
}
