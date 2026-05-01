-- styles_revised_v14.lua
-- Java’nın Temelleri için Pandoc DOCX dönüşümü geliştirilmiş filtre:
-- 1) Callout kutularını geniş etiket kümesiyle özel Word stillerine bağlar.
-- 2) Bölüm/Ek başlıklarından önce “Bölüm Sekmesi” paragrafı üretir.
-- 3) Çoktan seçmeli soruları hem iç içe hem de ayrı A/B/C listesi biçiminde dönüştürür.
-- 4) Bilinen LaTeX denklem yazım hatalarını DOCX dönüşümünden önce onarır; Bölüm 11 ReLU cases satır kırımı için emniyet sağlar.
-- 5) Mermaid blokları için önceden üretilmiş görselleri kullanır; görsel yoksa ham kod bırakmak yerine uyarı kutusu üretir.
-- 6) Markdown içindeki \newpage / \pagebreak ifadelerini DOCX için gerçek Word sayfa sonuna çevirir.
-- 7) Tablo başlıklarını beyaz/koyu zemin için karakter stiliyle zorlar; tablo stilinin merkezlenmesini destekler.
-- 8) Tablo sonrasında metinle tablo arasında güvenli boşluk üretir.
-- 9) Bölüm sonu sekmesini yeni bölümden önceki sayfada tutmak için bölüm sonu + sayfa sonu sıralamasını düzeltir.
-- 10) Bölüm başlangıç sekmesini sağa dayalı, bölüm sonu sekmesini solda tutar.
-- 11) Kaynak Markdown içindeki elle yazılmış BÖLÜM SONU satırlarını yutar; kapanış sekmesini tek kez otomatik üretir.
-- 12) Java kitabı üstbilgisi referenceV14_java_temelleri.docx içinde tek varsayılan üst bilgi olarak sadeleştirilmiştir.
-- 13) Mermaid PNG genişliği varsayılan 4.90in olarak sınırlandı; MERMAID_IMAGE_WIDTH ile değiştirilebilir.

local stringify = pandoc.utils.stringify
local icon_base = 'callout_icons/'

local function has_visible_inlines(inlines)
  return stringify(inlines):match('%S') ~= nil
end

local function file_exists(path)
  local f = io.open(path, 'rb')
  if f then f:close(); return true end
  return false
end

local function icon_inline(src, alt)
  if not src or src == '' or not file_exists(src) then return nil end
  local attr = pandoc.Attr('', {}, {width = '0.17in', height = '0.17in'})
  return pandoc.Image({pandoc.Str(alt)}, src, '', attr)
end

local function clean_inlines(inlines)
  local out = {}
  for _, inline in ipairs(inlines) do
    if inline.t ~= 'LineBreak' and inline.t ~= 'SoftBreak' then
      table.insert(out, inline)
    end
  end
  while #out > 0 and out[1].t == 'Space' do table.remove(out, 1) end
  while #out > 0 and out[#out].t == 'Space' do table.remove(out, #out) end
  return out
end

local function callout_match(label)
  -- Pandoc stringify() emoji ve Türkçe karakterleri korur; bu nedenle exact eşleşme yerine içerik tabanlı yakalama kullanıyoruz.
  if label:find('Matematiksel Sezgi ve Form') or label:find('Matematiksel Sezgi ve Formülasyon') then
    return {style = 'Matematiksel Sezgi Kutusu', icon = nil, text = 'Matematiksel Sezgi ve Formülasyon:'}
  end
  if label:find('Matematiksel Sezgi') or label:find('Matematiksel sezgi') then
    return {style = 'Matematiksel Sezgi Kutusu', icon = nil, text = 'Matematiksel Sezgi:'}
  end
  if label:find('Laboratuvar İpucu') or label:find('Laboratuvar Ipucu') then
    return {style = 'Laboratuvar Ipucu Kutusu', icon = nil, text = 'Laboratuvar İpucu:'}
  end
  if label:find('Ek Bölüm Hedefi') or label:find('Ek Bolum Hedefi') then
    return {style = 'Bolum Hedefi Kutusu', icon = nil, text = 'Ek Bölüm Hedefi:'}
  end
  if label:find('Bölüm Hedefi') or label:find('Bolum Hedefi') then
    return {style = 'Bolum Hedefi Kutusu', icon = nil, text = 'Bölüm Hedefi:'}
  end
  if label:find('Sınav Notu') or label:find('Sinav Notu') then
    return {style = 'Sinav Notu Kutusu', icon = icon_base .. 'target2.png', text = 'Sınav Notu:'}
  end
  if label:find('Alıştırma Molası') or label:find('Alistirma Molasi') then
    return {style = 'Alistirma Molasi Kutusu', icon = icon_base .. 'pencil.png', text = 'Alıştırma Molası:'}
  end
  if label:find('Derinlemesine') then
    return {style = 'Derinlemesine Kutusu', icon = icon_base .. 'search.png', text = 'Derinlemesine:'}
  end
  if label:find('Dikkat') then
    return {style = 'Dikkat Kutusu', icon = icon_base .. 'warning.png', text = 'Dikkat:'}
  end
  if label:find('İpucu') or label:find('Ipucu') then
    return {style = 'Ipucu Kutusu', icon = icon_base .. 'bulb.png', text = 'İpucu:'}
  end
  if label:find('Mini özet') or label:find('Mini Ozet') then
    return {style = 'Mini Ozet Kutusu', icon = icon_base .. 'target.png', text = 'Mini özet:'}
  end
  if label:find('Bir sonraki bölüme geçiş cümlesi') then
    return {style = 'Derinlemesine Kutusu', icon = nil, text = 'Bir sonraki bölüme geçiş cümlesi:'}
  end
  return nil
end

local function split_para_segments(para)
  if para.t ~= 'Para' then return nil end

  local segments = {}
  local current_style = nil
  local current_inlines = {}

  local function flush()
    if current_style and has_visible_inlines(current_inlines) then
      table.insert(segments, {style = current_style, para = pandoc.Para(clean_inlines(current_inlines))})
    end
    current_inlines = {}
  end

  local skip_next_space = false

  for _, inline in ipairs(para.content) do
    local matched = nil
    if inline.t == 'Strong' then
      matched = callout_match(stringify(inline))
    end

    if matched then
      flush()
      current_style = matched.style
      local ic = icon_inline(matched.icon, matched.text)
      if ic then
        table.insert(current_inlines, ic)
        table.insert(current_inlines, pandoc.Space())
      end
      table.insert(current_inlines, pandoc.Strong({pandoc.Str(matched.text)}))
      table.insert(current_inlines, pandoc.Space())
      skip_next_space = true
    else
      if current_style then
        if skip_next_space and inline.t == 'Space' then
          skip_next_space = false
        else
          skip_next_space = false
          table.insert(current_inlines, inline)
        end
      end
    end
  end

  flush()
  if #segments > 0 then return segments end
  return nil
end

local function make_styled_para(inlines, style_name)
  return pandoc.Div({pandoc.Para(inlines)}, pandoc.Attr('', {}, {['custom-style'] = style_name}))
end


-- DOCX için gerçek sayfa sonu üretir.
-- Markdown içindeki \newpage LaTeX/PDF çıktıda çalışabilir; DOCX çıktısında WordprocessingML'e çevrilmelidir.
local function word_pagebreak()
  return pandoc.RawBlock('openxml', '<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
end

local function is_latex_pagebreak_text(txt)
  if not txt then return false end
  txt = txt:gsub('\r', ''):gsub('^%s+', ''):gsub('%s+$', '')
  return txt == '\\newpage' or txt == '\\pagebreak' or txt == '\\clearpage'
end

local function is_pagebreak_block(blk)
  if blk.t == 'RawBlock' and blk.format == 'openxml' and blk.text and blk.text:find('w:br') and blk.text:find('page') then
    return true
  end
  if blk.t == 'RawBlock' and (blk.format == 'tex' or blk.format == 'latex') then
    return is_latex_pagebreak_text(blk.text)
  end
  if blk.t == 'Para' or blk.t == 'Plain' then
    local txt = stringify(blk.content)
    if is_latex_pagebreak_text(txt) then return true end
    if #blk.content == 1 and blk.content[1].t == 'RawInline' then
      local inline = blk.content[1]
      if (inline.format == 'tex' or inline.format == 'latex') and is_latex_pagebreak_text(inline.text) then
        return true
      end
    end
  end
  if blk.t == 'Div' then
    for _, cls in ipairs(blk.classes or {}) do
      if cls == 'pagebreak' or cls == 'newpage' then return true end
    end
  end
  return false
end


-- Kaynak Markdown sonunda elle yazılmış BÖLÜM SONU/BOLUM SONU satırları
-- şablon tarafından otomatik üretildiği için yutulur. Bu, final DOCX/PDF çıktısında
-- bölüm sonu etiketinin iki kez görünmesini engeller.
local function is_manual_chapter_end_block(blk)
  if blk.t ~= 'Para' and blk.t ~= 'Plain' then return false end
  local txt = stringify(blk.content)
  txt = txt:gsub('\r', ''):gsub('^%s+', ''):gsub('%s+$', '')
  return txt == 'BÖLÜM SONU' or txt == 'BOLUM SONU'
end

function RawBlock(el)
  if (el.format == 'tex' or el.format == 'latex') and is_latex_pagebreak_text(el.text) then
    return word_pagebreak()
  end
  return nil
end

function Div(el)
  for _, cls in ipairs(el.classes or {}) do
    if cls == 'pagebreak' or cls == 'newpage' then
      return word_pagebreak()
    end
  end
  return nil
end

local function alpha_label(i)
  local letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  if i <= #letters then return letters:sub(i, i) .. ')' end
  return tostring(i) .. ')'
end

local function get_first_inlines(blocks)
  for _, blk in ipairs(blocks) do
    if blk.t == 'Plain' or blk.t == 'Para' then
      return clean_inlines(blk.content)
    end
  end
  return {}
end

local function find_upperalpha_list(blocks)
  for _, blk in ipairs(blocks) do
    if blk.t == 'OrderedList' and blk.listAttributes and blk.listAttributes.style == 'UpperAlpha' then
      return blk
    end
  end
  return nil
end

local function transform_mcq_list(el)
  local out = {}
  local start = 1
  if el.listAttributes and el.listAttributes.start then start = el.listAttributes.start end

  for idx, item in ipairs(el.content) do
    local qno = start + idx - 1
    local q_inlines = get_first_inlines(item)
    local qline = {pandoc.Strong({pandoc.Str(tostring(qno) .. '.')})}
    if #q_inlines > 0 then
      table.insert(qline, pandoc.Space())
      for _, x in ipairs(q_inlines) do table.insert(qline, x) end
    end
    table.insert(out, make_styled_para(qline, 'Soru Metni'))

    local opts = find_upperalpha_list(item)
    if opts then
      for j, opt_item in ipairs(opts.content) do
        local opt_inlines = get_first_inlines(opt_item)
        local line = {pandoc.Strong({pandoc.Str(alpha_label(j))})}
        if #opt_inlines > 0 then
          table.insert(line, pandoc.Space())
          for _, x in ipairs(opt_inlines) do table.insert(line, x) end
        end
        table.insert(out, make_styled_para(line, 'Soru Secenegi'))
      end
    end
  end
  return out
end



local function transform_upperalpha_list(el)
  local out = {}
  for j, opt_item in ipairs(el.content) do
    local opt_inlines = get_first_inlines(opt_item)
    local line = {pandoc.Strong({pandoc.Str(alpha_label(j))})}
    if #opt_inlines > 0 then
      table.insert(line, pandoc.Space())
      for _, x in ipairs(opt_inlines) do table.insert(line, x) end
    end
    table.insert(out, make_styled_para(line, 'Soru Secenegi'))
  end
  return out
end

local function is_answer_key_para(blk)
  if blk.t ~= 'Para' and blk.t ~= 'Plain' then return false end
  local txt = stringify(blk.content)
  return txt:match('^%s*Doğru%s+cevap%s*:') or txt:match('^%s*Doğru%s+Cevap%s*:') or txt:match('^%s*Cevap%s*:')
end

local function transform_answer_key_para(blk)
  return make_styled_para(clean_inlines(blk.content), 'Cevap Anahtarı')
end

local function chapter_tab_text(header_text)
  local n = header_text:match('^Bölüm%s+(%d+)%s*:')
  if n then return 'BÖLÜM ' .. n end

  local ek1 = header_text:match('^Ek%s+Bölüm%s+([A-ZÇĞİÖŞÜ])')
  if ek1 then return 'EK ' .. ek1 end

  local ek2 = header_text:match('^Ek%s+([A-ZÇĞİÖŞÜ])%s*:')
  if ek2 then return 'EK ' .. ek2 end

  return nil
end



-- Tablo başlıklarında table-style rPr bazı Word/LibreOffice dönüşümlerinde uygulanmayabilir.
-- Bu nedenle başlık hücrelerindeki metin, referenceV10.docx içindeki "Tablo Baslik Yazisi"
-- karakter stiliyle ayrıca işaretlenir. Tablo merkezleme ise referenceV10.docx içindeki Table stilinden gelir.
local function style_table_header_block(block)
  if block.t == 'Para' or block.t == 'Plain' then
    if has_visible_inlines(block.content) then
      block.content = {pandoc.Span(block.content, pandoc.Attr('', {}, {['custom-style'] = 'Tablo Baslik Yazisi'}))}
    end
    return block
  elseif block.t == 'Div' then
    for i, b in ipairs(block.content) do
      block.content[i] = style_table_header_block(b)
    end
    return block
  else
    return block
  end
end


-- Tablo sonrasında metnin tabloya yapışmasını önlemek için küçük ama kontrollü bir boşluk üretir.
-- Raw OpenXML kullanmak, boş paragrafın Pandoc/Word tarafından yutulmasını engeller.
local function table_after_spacing()
  return pandoc.RawBlock('openxml', '<w:p><w:pPr><w:spacing w:before="120" w:after="120" w:line="240" w:lineRule="auto"/></w:pPr></w:p>')
end

local function style_table_header_cell(cell)
  if cell and cell.contents then
    for i, b in ipairs(cell.contents) do
      cell.contents[i] = style_table_header_block(b)
    end
  end
  return cell
end

function Table(el)
  -- Pandoc 3.x table object: el.head.rows[].cells[]
  if el.head and el.head.rows then
    for _, row in ipairs(el.head.rows) do
      if row.cells then
        for i, cell in ipairs(row.cells) do
          row.cells[i] = style_table_header_cell(cell)
        end
      end
    end
  end
  -- Tabloyu izleyen normal metinle tablo arasında kontrollü boşluk bırak.
  return {el, table_after_spacing()}
end

function Math(el)
  if el.mathtype == 'DisplayMath' then
    local txt = el.text
    -- Bölüm 11'de ReLU türevi cases ortamında tek backslash kalmışsa Word denklem dönüşümü bozulur.
    txt = txt:gsub([[z>0 \
0,]], [[z>0 \\
0,]])
    txt = txt:gsub([[z>0 
0,]], [[z>0 \\
0,]])
    -- Word denklemlerinde fonksiyon adlarının italikleşmesini azaltmak için ReLU'yu operatorname yap.
    txt = txt:gsub('ReLU%(', '\\operatorname{ReLU}(')
    txt = txt:gsub("ReLU%'%(", "\\operatorname{ReLU}'(")
    el.text = txt
  end
  return el
end

function BlockQuote(el)
  local out = {}
  local current_style = nil
  local current_blocks = {}

  local function flush_current()
    if current_style and #current_blocks > 0 then
      table.insert(out, pandoc.Div(current_blocks, pandoc.Attr('', {}, {['custom-style'] = current_style})))
    elseif #current_blocks > 0 then
      table.insert(out, pandoc.BlockQuote(current_blocks))
    end
    current_style = nil
    current_blocks = {}
  end

  for _, blk in ipairs(el.content) do
    local segments = split_para_segments(blk)
    if segments then
      for _, seg in ipairs(segments) do
        flush_current()
        current_style = seg.style
        table.insert(current_blocks, seg.para)
      end
    else
      table.insert(current_blocks, blk)
    end
  end

  flush_current()
  if #out > 0 then return out end
  return nil
end



local mermaid_counter = 0

-- v2.4.1: Mermaid görsel genişliği ve görsel dizini ortam değişkeniyle yönetilebilir.
-- Örnek:
--   MERMAID_IMAGE_WIDTH=5.20in MERMAID_IMAGE_DIR=build/mermaid_images pandoc ...
local mermaid_image_width = os.getenv('MERMAID_IMAGE_WIDTH') or '4.90in'
local mermaid_image_dir = os.getenv('MERMAID_IMAGE_DIR') or 'mermaid_images'

local function join_path(dir, file)
  if not dir or dir == '' then return file end
  local last = dir:sub(-1)
  if last == '/' or last == '\\' then
    return dir .. file
  end
  return dir .. '/' .. file
end

local function mermaid_image_candidates(n)
  local names = {
    string.format('diagram_%03d.png', n),
    string.format('diagram_%03d.svg', n),
    string.format('diyagram_%03d.png', n),
    string.format('diyagram_%03d.svg', n)
  }
  local candidates = {}
  for _, name in ipairs(names) do
    table.insert(candidates, join_path(mermaid_image_dir, name))
  end
  if mermaid_image_dir ~= 'mermaid_images' then
    for _, name in ipairs(names) do
      table.insert(candidates, join_path('mermaid_images', name))
    end
  end
  return candidates
end

local function missing_mermaid_block(n)
  local expected = join_path(mermaid_image_dir, string.format('diagram_%03d.png', n))
  local msg = string.format(
    'Mermaid diyagram görseli bulunamadı. Beklenen dosya: %s. DOCX/PDF final çıktıdan önce Mermaid bloklarını PNG/SVG görsele dönüştürünüz.',
    expected
  )
  return pandoc.Div({
    pandoc.Para({
      pandoc.Strong({pandoc.Str('Diyagram görseli eksik:')}),
      pandoc.Space(),
      pandoc.Str(msg)
    })
  }, pandoc.Attr('', {}, {['custom-style']='Dikkat Kutusu'}))
end

function CodeBlock(el)
  local is_mermaid = false
  if el.classes then
    for _, cls in ipairs(el.classes) do
      if cls == 'mermaid' then is_mermaid = true end
    end
  end
  if is_mermaid then
    mermaid_counter = mermaid_counter + 1
    for _, img in ipairs(mermaid_image_candidates(mermaid_counter)) do
      if file_exists(img) then
        local attr = pandoc.Attr('', {}, {width = mermaid_image_width})
        return pandoc.Para({pandoc.Image({pandoc.Str('Diyagram')}, img, '', attr)})
      end
    end
    -- Ham Mermaid kodunu final belgeye bırakma: görünür uyarı üret.
    return missing_mermaid_block(mermaid_counter)
  end
  return nil
end

function Pandoc(doc)
  local blocks = {}
  local in_mcq = false
  local active_chapter_tab = nil
  local last_was_pagebreak = false

  local function is_chapter_header_block(blk)
    if blk and blk.t == 'Header' and blk.level == 1 then
      local htxt = stringify(blk.content)
      return chapter_tab_text(htxt) ~= nil
    end
    return false
  end

  local function next_significant_block(blocks_in, start_index)
    for j = start_index + 1, #blocks_in do
      local b = blocks_in[j]
      if not is_pagebreak_block(b) then
        if b.t ~= 'Null' then
          return b
        end
      end
    end
    return nil
  end

  local function insert_chapter_end_tab()
    if active_chapter_tab then
      table.insert(blocks, make_styled_para({pandoc.Str('BÖLÜM SONU')}, 'Bolum Sekmesi'))
      active_chapter_tab = nil
      last_was_pagebreak = false
      return true
    end
    return false
  end

  for i, blk in ipairs(doc.blocks) do
    if is_manual_chapter_end_block(blk) then
      -- Kaynaktaki elle yazılmış kapanış etiketi atlanır; kapanış sekmesi dosya sonunda veya yeni bölümden önce tek kez otomatik eklenir.
      last_was_pagebreak = false

    elseif is_pagebreak_block(blk) then
      -- Eğer bu sayfa sonundan sonra yeni bölüm/ek geliyorsa, kapanış sekmesini
      -- sayfa sonundan ÖNCE ekle. Böylece “BÖLÜM SONU” yeni bölüm sekmesiyle aynı
      -- sayfada ve aynı mavi blok içinde birleşmez.
      local nxt = next_significant_block(doc.blocks, i)
      if active_chapter_tab and is_chapter_header_block(nxt) then
        insert_chapter_end_tab()
      end
      table.insert(blocks, word_pagebreak())
      last_was_pagebreak = true

    elseif blk.t == 'Header' then
      local htxt = stringify(blk.content)
      if in_mcq and blk.level <= 3 and not htxt:match('Çoktan seçmeli sorular') then
        in_mcq = false
      end
      if htxt:match('Çoktan seçmeli sorular') then
        in_mcq = true
      end

      if blk.level == 1 then
        local tab = chapter_tab_text(htxt)
        if tab then
          -- Yeni bir bölüm/ek başlığı başlamadan önce önceki bölümün kapanış sekmesini ekle.
          -- Eğer kaynak Markdown'da sayfa sonu yoksa burada otomatik sayfa sonu üret.
          if active_chapter_tab then
            insert_chapter_end_tab()
            if not last_was_pagebreak then
              table.insert(blocks, word_pagebreak())
              last_was_pagebreak = true
            end
          end
          table.insert(blocks, make_styled_para({pandoc.Str(tab)}, 'Bolum Baslangic Sekmesi'))
          active_chapter_tab = tab
          last_was_pagebreak = false
        end
      end
      table.insert(blocks, blk)
      last_was_pagebreak = false

    elseif in_mcq and blk.t == 'OrderedList' and blk.listAttributes and blk.listAttributes.style == 'Decimal' then
      -- İki biçimi de destekler: seçeneklerin soru içine gömülü olduğu yapı ve seçeneklerin ayrı UpperAlpha listesi olarak geldiği yapı.
      local converted = transform_mcq_list(blk)
      for _, b in ipairs(converted) do table.insert(blocks, b) end
      last_was_pagebreak = false

    elseif in_mcq and blk.t == 'OrderedList' and blk.listAttributes and blk.listAttributes.style == 'UpperAlpha' then
      local converted = transform_upperalpha_list(blk)
      for _, b in ipairs(converted) do table.insert(blocks, b) end
      last_was_pagebreak = false

    elseif in_mcq and is_answer_key_para(blk) then
      table.insert(blocks, transform_answer_key_para(blk))
      last_was_pagebreak = false

    else
      table.insert(blocks, blk)
      last_was_pagebreak = false
    end
  end

  -- Belgenin son bölüm/ek kapanış sekmesi.
  insert_chapter_end_tab()

  doc.blocks = blocks
  return doc
end
