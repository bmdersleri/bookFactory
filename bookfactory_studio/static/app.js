let project = null;
let manifestData = {};
let activeJobId = null;
let jobTimer = null;

const $ = (id) => document.getElementById(id);
const root = () => $('projectRoot').value || '.';

function setStatus(msg, cls='') {
  const el = $('status');
  el.className = 'status ' + cls;
  el.textContent = msg;
}

async function api(path, opts={}) {
  const res = await fetch(path, {
    headers: {'Content-Type': 'application/json'},
    ...opts,
  });
  if (!res.ok) {
    let detail = await res.text();
    try {
      const parsed = JSON.parse(detail);
      detail = parsed.detail || parsed;
      if (typeof detail === 'object') detail = JSON.stringify(detail, null, 2);
    } catch {}
    throw new Error(detail);
  }
  return res.json();
}

function showTab(name) {
  document.querySelectorAll('.tab').forEach(b => b.classList.toggle('active', b.dataset.tab === name));
  document.querySelectorAll('.panel').forEach(p => p.classList.toggle('visible', p.id === name));
}

document.querySelectorAll('.tab').forEach(b => b.addEventListener('click', () => showTab(b.dataset.tab)));
document.querySelectorAll('.manifest-tab').forEach(b => b.addEventListener('click', () => showManifestTab(b.dataset.mtab)));

function showManifestTab(name) {
  document.querySelectorAll('.manifest-tab').forEach(b => b.classList.toggle('active', b.dataset.mtab === name));
  document.querySelectorAll('.manifest-panel').forEach(p => p.classList.toggle('visible', p.id === name));
}

function get(obj, path, fallback='') {
  return path.split('.').reduce((o, k) => (o && o[k] !== undefined ? o[k] : undefined), obj) ?? fallback;
}

function set(obj, path, value) {
  const parts = path.split('.');
  let cur = obj;
  parts.slice(0, -1).forEach(k => {
    if (!cur[k] || typeof cur[k] !== 'object' || Array.isArray(cur[k])) cur[k] = {};
    cur = cur[k];
  });
  cur[parts[parts.length - 1]] = value;
}

function lines(text) {
  return String(text || '').split('\n').map(x => x.trim()).filter(Boolean);
}

function commaList(text) {
  return String(text || '').split(',').map(x => x.trim()).filter(Boolean);
}

function escapeHtml(s) {
  return String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
}

function safeSlug(text) {
  const tr = {'ç':'c','Ç':'c','ğ':'g','Ğ':'g','ı':'i','I':'i','İ':'i','ö':'o','Ö':'o','ş':'s','Ş':'s','ü':'u','Ü':'u'};
  return String(text || 'bolum')
    .replace(/[çÇğĞıIİöÖşŞüÜ]/g, c => tr[c] || c)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/_+/g, '_')
    .replace(/^_|_$/g, '') || 'bolum';
}

function normalizeChapterId(n) {
  return `chapter_${String(n).padStart(2, '0')}`;
}

function renderRecentBooks(books) {
  const sel = $('recentBooksSelect');
  sel.innerHTML = '<option value="">Son kitaplar…</option>';
  (books || []).forEach(b => {
    const opt = document.createElement('option');
    opt.value = b;
    const name = b.replace(/\\/g, '/').split('/').pop();
    opt.textContent = name + '  —  ' + b;
    sel.appendChild(opt);
  });
}

async function initStudio() {
  try {
    const config = await api('/api/studio/config');
    $('frameworkRoot').textContent = config.framework_root || '-';
    if (config.active_book) {
      $('projectRoot').value = config.active_book;
    }
    renderRecentBooks(config.recent_books || []);
  } catch (e) {
    $('frameworkRoot').textContent = '(config okunamadı)';
  }
  await loadProject();
}

async function loadProject() {
  try {
    setStatus('Kitap projesi yükleniyor...');
    project = await api('/api/project?root=' + encodeURIComponent(root()));
    manifestData = structuredClone(project.manifest || {});
    renderDashboard();
    renderChapters();
    renderManifestForm();
    renderReports(project.reports || []);
    await loadPipelineSteps();
    await refreshManifest(false);
    const valid = project.validation?.valid;
    setStatus('Kitap projesi yüklendi: ' + project.root, valid ? 'good' : 'warn');
    // Seçili kitabı config'e kaydet
    const r = root();
    if (r && r !== '.') {
      try {
        const cfg = await api('/api/studio/config', {method: 'POST', body: JSON.stringify({active_book: r})});
        renderRecentBooks(cfg.recent_books || []);
      } catch {}
    }
  } catch (e) {
    setStatus('Hata: ' + e.message, 'bad');
  }
}

function renderDashboard() {
  const m = project?.manifest || {};
  $('bookTitle').textContent = m.book?.title || '-';
  $('bookAuthor').textContent = m.book?.author || '-';
  $('chapterCount').textContent = (project?.chapters || []).length;
  $('manifestState').textContent = project?.validation?.valid ? 'Geçerli' : 'Sorun var';
  const warn = $('bookRootWarning');
  if (project?.is_framework_root) {
    warn.classList.remove('hidden');
    warn.innerHTML = '<strong>Yanlış kök seçilmiş olabilir.</strong> BookFactory framework klasörü yerine doğrudan kitap klasörünü seçin. Örnek: <code>...\\react-web</code> veya <code>...\\BookFactory\\workspace\\react</code>.';
  } else if ((project?.discovered_book_roots || []).length && !project?.manifest_path) {
    warn.classList.remove('hidden');
    warn.innerHTML = '<strong>Alt klasörlerde kitap manifestleri bulundu.</strong> Aktif kök olarak ilgili kitap klasörünü yazın: ' + project.discovered_book_roots.map(x => `<code>${escapeHtml(x.root)}</code>`).join(', ');
  } else {
    warn.classList.add('hidden');
  }
  const counts = project?.chapter_status_counts || {};
  $('statusCounts').innerHTML = Object.keys(counts).length ? Object.entries(counts).map(([k,v]) => `<span class="pill">${escapeHtml(k)}: ${v}</span>`).join('') : '<span class="pill">Henüz bölüm yok</span>';
  const reports = (project?.reports || []).slice(-6).reverse();
  $('recentReports').innerHTML = reports.length ? reports.map(r => `<div class="item">${escapeHtml(r.path)}<br><small>${r.size} bayt</small></div>`).join('') : '<div class="item">Rapor yok.</div>';
}

async function refreshManifest(updateForm=true) {
  try {
    const data = await api('/api/manifest?root=' + encodeURIComponent(root()));
    manifestData = structuredClone(data.manifest || {});
    $('manifestYaml').value = data.yaml;
    renderValidation(data.validation);
    if (updateForm) renderManifestForm();
  } catch (e) {
    $('manifestYaml').value = '# Manifest bulunamadı veya okunamadı.\n# Kitap Sihirbazı veya mevcut YAML dosyasını kullanın.\n';
    renderValidation({valid:false, errors:[e.message], warnings:[]});
  }
}

function renderValidation(validation) {
  const box = $('manifestValidationBox');
  const errors = validation?.errors || [];
  const warnings = validation?.warnings || [];
  if (validation?.valid && warnings.length === 0) {
    box.className = 'validation-box valid';
    box.innerHTML = '<strong>Manifest geçerli.</strong> Kayıt ve production için temel alanlar uygun görünüyor.';
    return;
  }
  if (errors.length) {
    box.className = 'validation-box invalid';
    box.innerHTML = `<h4>Kaydı engelleyen hatalar</h4><ul>${errors.map(e => `<li>${escapeHtml(e)}</li>`).join('')}</ul>` +
      (warnings.length ? `<h4>Uyarılar</h4><ul>${warnings.map(w => `<li>${escapeHtml(w)}</li>`).join('')}</ul>` : '');
    return;
  }
  if (warnings.length) {
    box.className = 'validation-box warning';
    box.innerHTML = `<strong>Manifest kaydedilebilir; ancak uyarılar var.</strong><ul>${warnings.map(w => `<li>${escapeHtml(w)}</li>`).join('')}</ul>`;
    return;
  }
  box.className = 'validation-box muted';
  box.textContent = 'Manifest henüz kontrol edilmedi.';
}

function renderManifestForm() {
  const m = manifestData || {};
  $('mBookTitle').value = get(m, 'book.title');
  $('mBookSubtitle').value = get(m, 'book.subtitle');
  $('mBookAuthor').value = get(m, 'book.author');
  $('mBookEdition').value = get(m, 'book.edition');
  $('mBookYear').value = get(m, 'book.year');
  $('mFrameworkVersion').value = get(m, 'book.framework_version');
  $('mPrimaryLanguage').value = get(m, 'language.primary_language', 'tr');
  $('mOutputLanguages').value = (get(m, 'language.output_languages', ['tr']) || []).join(',');
  $('mAppName').value = get(m, 'cumulative_app.name');
  $('mAppDescription').value = get(m, 'cumulative_app.description');
  $('mScopeStack').value = (get(m, 'scope.stack', []) || []).join('\n');
  $('mOutOfScope').value = (get(m, 'scope.out_of_scope', []) || []).join('\n');

  $('mGateManifest').value = get(m, 'approval_gates.manifest_validation', 'required');
  $('mGateChapterInput').value = get(m, 'approval_gates.chapter_input_generation', 'optional');
  $('mGateOutline').value = get(m, 'approval_gates.outline_review', 'required');
  $('mGateFullText').value = get(m, 'approval_gates.full_text_generation', 'required');
  $('mGateCodeValidation').value = get(m, 'approval_gates.code_validation', 'required');
  $('mGateMarkdownQuality').value = get(m, 'approval_gates.markdown_quality_check', 'required');
  $('mGatePostProduction').value = get(m, 'approval_gates.post_production_build', 'optional');
  $('mProjectStatus').value = get(m, 'project.status', 'in_progress');

  $('mCodeExtract').checked = Boolean(get(m, 'code.extract', true));
  $('mCodeTest').checked = Boolean(get(m, 'code.test', true));
  $('mGithubSync').checked = Boolean(get(m, 'code.github_sync', false));
  $('mQrGeneration').checked = Boolean(get(m, 'code.qr_generation', false));
  $('mScreenshotAutomation').checked = Boolean(get(m, 'assets.screenshot_automation', false));
  $('mMermaidGeneration').checked = Boolean(get(m, 'assets.mermaid_generation', true));
  $('mManualOverride').checked = Boolean(get(m, 'assets.manual_override', true));

  $('mPathChapters').value = get(m, 'project.paths.chapters', 'chapters');
  $('mPathChapterPrompts').value = get(m, 'project.paths.chapter_prompts', 'prompts/chapter_inputs');
  $('mPathChapterBackups').value = get(m, 'project.paths.chapter_backups', 'chapter_backups');
  $('mPathBuild').value = get(m, 'project.paths.build', 'build');
  $('mPathAssets').value = get(m, 'project.paths.assets', 'assets');
  $('mPathExports').value = get(m, 'project.paths.exports', 'exports');

  renderManifestChapters();
}

function chapterFileStatus(ch, idx) {
  const rows = project?.chapters || [];
  const row = rows.find(r => r.id === ch.id) || rows[idx];
  if (!row) return '<span class="file-missing">?</span>';
  return row.chapter_exists ? `<span class="file-ok">Var</span><br><small>${escapeHtml(row.chapter_path)}</small>` : `<span class="file-missing">Yok</span><br><small>${escapeHtml(row.chapter_path || '')}</small>`;
}

function renderManifestChapters() {
  const chapters = get(manifestData, 'structure.chapters', []);
  const tbody = $('manifestChapterRows');
  tbody.innerHTML = chapters.map((ch, idx) => {
    const id = ch.id || normalizeChapterId(idx + 1);
    return `<tr data-idx="${idx}">
      <td>${idx + 1}</td>
      <td><input class="ch-id mono" value="${escapeHtml(id)}" /></td>
      <td><input class="ch-title" value="${escapeHtml(ch.title || '')}" /></td>
      <td><input class="ch-file mono" value="${escapeHtml(ch.file || `${id}_${safeSlug(ch.title || id)}.md`)}" /></td>
      <td><select class="ch-status">
        ${['planned','prompt_ready','in_progress','draft','review','done','skipped','archived'].map(s => `<option ${s === (ch.status || 'planned') ? 'selected' : ''}>${s}</option>`).join('')}
      </select></td>
      <td>${chapterFileStatus(ch, idx)}</td>
      <td class="toolbar compact">
        <button class="smallbtn secondary" data-act="slug" title="Başlıktan dosya adı üret">Adlandır</button>
        <button class="smallbtn secondary" data-act="up">↑</button>
        <button class="smallbtn secondary" data-act="down">↓</button>
        <button class="smallbtn danger" data-act="delete">Sil</button>
      </td>
    </tr>`;
  }).join('');
  tbody.querySelectorAll('input,select').forEach(el => el.addEventListener('input', syncChaptersFromTable));
  tbody.querySelectorAll('button').forEach(btn => btn.addEventListener('click', chapterAction));
}

function syncChaptersFromTable() {
  const rows = [...document.querySelectorAll('#manifestChapterRows tr')];
  const chapters = rows.map((tr) => ({
    id: tr.querySelector('.ch-id').value.trim(),
    title: tr.querySelector('.ch-title').value.trim(),
    file: tr.querySelector('.ch-file').value.trim(),
    status: tr.querySelector('.ch-status').value,
  }));
  set(manifestData, 'structure.chapters', chapters);
  markInvalidInputs();
}

function chapterAction(e) {
  e.preventDefault();
  syncChaptersFromTable();
  const tr = e.target.closest('tr');
  const idx = Number(tr.dataset.idx);
  const act = e.target.dataset.act;
  const chapters = get(manifestData, 'structure.chapters', []);
  if (act === 'delete') chapters.splice(idx, 1);
  if (act === 'up' && idx > 0) [chapters[idx - 1], chapters[idx]] = [chapters[idx], chapters[idx - 1]];
  if (act === 'down' && idx < chapters.length - 1) [chapters[idx + 1], chapters[idx]] = [chapters[idx], chapters[idx + 1]];
  if (act === 'slug') {
    const id = chapters[idx].id || normalizeChapterId(idx + 1);
    chapters[idx].file = `${id}_${safeSlug(chapters[idx].title || id)}.md`;
  }
  renderManifestChapters();
}

function collectManifestFromForm() {
  syncChaptersFromTable();
  const m = structuredClone(manifestData || {});
  set(m, 'book.title', $('mBookTitle').value.trim());
  set(m, 'book.subtitle', $('mBookSubtitle').value.trim());
  set(m, 'book.author', $('mBookAuthor').value.trim());
  set(m, 'book.edition', $('mBookEdition').value.trim());
  set(m, 'book.year', $('mBookYear').value.trim());
  set(m, 'book.framework_version', $('mFrameworkVersion').value.trim());
  set(m, 'language.primary_language', $('mPrimaryLanguage').value.trim() || 'tr');
  set(m, 'language.output_languages', commaList($('mOutputLanguages').value));
  set(m, 'language.file_naming_language', get(m, 'language.file_naming_language', 'en'));
  set(m, 'language.manifest_language', get(m, 'language.manifest_language', 'en'));
  set(m, 'language.automation_language', get(m, 'language.automation_language', 'en'));
  set(m, 'cumulative_app.name', $('mAppName').value.trim());
  set(m, 'cumulative_app.description', $('mAppDescription').value.trim());
  set(m, 'scope.stack', lines($('mScopeStack').value));
  set(m, 'scope.out_of_scope', lines($('mOutOfScope').value));

  set(m, 'approval_gates.manifest_validation', $('mGateManifest').value);
  set(m, 'approval_gates.chapter_input_generation', $('mGateChapterInput').value);
  set(m, 'approval_gates.outline_review', $('mGateOutline').value);
  set(m, 'approval_gates.full_text_generation', $('mGateFullText').value);
  set(m, 'approval_gates.code_validation', $('mGateCodeValidation').value);
  set(m, 'approval_gates.markdown_quality_check', $('mGateMarkdownQuality').value);
  set(m, 'approval_gates.post_production_build', $('mGatePostProduction').value);
  set(m, 'project.status', $('mProjectStatus').value);

  set(m, 'code.extract', $('mCodeExtract').checked);
  set(m, 'code.test', $('mCodeTest').checked);
  set(m, 'code.github_sync', $('mGithubSync').checked);
  set(m, 'code.qr_generation', $('mQrGeneration').checked);
  set(m, 'assets.screenshot_automation', $('mScreenshotAutomation').checked);
  set(m, 'assets.mermaid_generation', $('mMermaidGeneration').checked);
  set(m, 'assets.manual_override', $('mManualOverride').checked);

  set(m, 'project.paths.chapters', $('mPathChapters').value.trim() || 'chapters');
  set(m, 'project.paths.chapter_prompts', $('mPathChapterPrompts').value.trim() || 'prompts/chapter_inputs');
  set(m, 'project.paths.chapter_backups', $('mPathChapterBackups').value.trim() || 'chapter_backups');
  set(m, 'project.paths.build', $('mPathBuild').value.trim() || 'build');
  set(m, 'project.paths.assets', $('mPathAssets').value.trim() || 'assets');
  set(m, 'project.paths.exports', $('mPathExports').value.trim() || 'exports');
  manifestData = m;
  return m;
}

function markInvalidInputs() {
  const must = ['mBookTitle', 'mBookAuthor', 'mPrimaryLanguage'];
  must.forEach(id => $(id).classList.toggle('invalid', !$(id).value.trim()));
  $('mBookYear').classList.toggle('invalid', Boolean($('mBookYear').value.trim()) && !/^[0-9]{4}$/.test($('mBookYear').value.trim()));
  document.querySelectorAll('.ch-id').forEach(inp => inp.classList.toggle('invalid', !/^chapter_[0-9]{2}$/.test(inp.value.trim())));
  document.querySelectorAll('.ch-file').forEach(inp => inp.classList.toggle('invalid', !/^[A-Za-z0-9_./-]+\.md$/.test(inp.value.trim()) || inp.value.includes('..') || inp.value.includes(' ')));
}

async function validateManifestFromForm() {
  try {
    const manifest = collectManifestFromForm();
    const validation = await api('/api/manifest/validate', {method: 'POST', body: JSON.stringify({root: root(), manifest})});
    renderValidation(validation);
    markInvalidInputs();
    setStatus(validation.valid ? 'Manifest geçerli.' : 'Manifestte kaydı engelleyen hatalar var.', validation.valid ? 'good' : 'bad');
    return validation;
  } catch (e) {
    setStatus('Manifest kontrol hatası: ' + e.message, 'bad');
    return {valid:false, errors:[e.message], warnings:[]};
  }
}

async function saveManifestFromForm() {
  try {
    const manifest = collectManifestFromForm();
    const data = await api('/api/manifest/save', {method: 'POST', body: JSON.stringify({root: root(), manifest})});
    manifestData = structuredClone(data.manifest || manifest);
    $('manifestYaml').value = data.yaml || $('manifestYaml').value;
    renderValidation(data.validation);
    project = await api('/api/project?root=' + encodeURIComponent(root()));
    renderDashboard(); renderChapters(); renderManifestForm();
    setStatus('Manifest formdan güvenli biçimde kaydedildi: ' + data.path, 'good');
  } catch (e) {
    setStatus('Kaydedilmedi: ' + e.message, 'bad');
  }
}

async function saveManifestYaml() {
  try {
    const yamlText = $('manifestYaml').value;
    const data = await api('/api/manifest/save-yaml', {method: 'POST', body: JSON.stringify({root: root(), yaml_text: yamlText})});
    manifestData = structuredClone(data.manifest || {});
    renderValidation(data.validation);
    project = await api('/api/project?root=' + encodeURIComponent(root()));
    renderDashboard(); renderChapters(); renderManifestForm();
    setStatus('YAML güvenli biçimde kaydedildi: ' + data.path, 'good');
  } catch (e) { setStatus('Kaydedilmedi: ' + e.message, 'bad'); }
}

async function previewYaml() {
  const manifest = collectManifestFromForm();
  try {
    const data = await api('/api/manifest/render-yaml', {method: 'POST', body: JSON.stringify({root: root(), manifest})});
    $('manifestYaml').value = data.yaml || '';
    renderValidation(data.validation);
    setStatus('Formdan YAML önizleme üretildi. Dosyaya kaydedilmedi.', data.validation?.valid ? 'good' : 'warn');
  } catch (e) { setStatus('YAML önizleme hatası: ' + e.message, 'bad'); }
}

async function yamlToForm() {
  try {
    const data = await api('/api/manifest/parse-yaml', {method: 'POST', body: JSON.stringify({root: root(), yaml_text: $('manifestYaml').value})});
    manifestData = structuredClone(data.manifest || {});
    renderManifestForm();
    renderValidation(data.validation);
    setStatus('YAML forma yüklendi. Henüz dosyaya kaydedilmedi.', data.validation?.valid ? 'good' : 'warn');
  } catch (e) { setStatus('YAML forma yüklenemedi: ' + e.message, 'bad'); }
}

async function matchChapterFiles() {
  try {
    const manifest = collectManifestFromForm();
    const data = await api('/api/manifest/match-chapter-files', {method: 'POST', body: JSON.stringify({root: root(), manifest})});
    manifestData = structuredClone(data.manifest || manifest);
    renderManifestForm();
    renderValidation(data.validation);
    const fileUpdates = (data.changes || []).filter(c => c.new_file).length;
    const statUpdates = (data.changes || []).filter(c => c.status_updated).length;
    try {
      const saveData = await api('/api/manifest/save', {method: 'POST', body: JSON.stringify({root: root(), manifest: data.manifest, force: false})});
      manifestData = structuredClone(saveData.manifest || data.manifest);
      $('manifestYaml').value = saveData.yaml || $('manifestYaml').value;
      project = await api('/api/project?root=' + encodeURIComponent(root()));
      renderDashboard(); renderChapters(); renderManifestForm();
      setStatus(
        `${data.changes?.length || 0} güncelleme: ${fileUpdates} dosya adı, ${statUpdates} durum düzeltildi. Manifest kaydedildi.` +
        (data.unmatched?.length ? ` ${data.unmatched.length} bölüm eşleşmedi.` : ''),
        data.unmatched?.length ? 'warn' : 'good'
      );
    } catch (saveErr) {
      setStatus(`Eşleştirme yapıldı (${data.changes?.length || 0} güncelleme) fakat kayıt başarısız: ${saveErr.message}`, 'warn');
    }
  } catch (e) { setStatus('Dosya eşleştirme hatası: ' + e.message, 'bad'); }
}

function addChapter() {
  syncChaptersFromTable();
  const chapters = get(manifestData, 'structure.chapters', []);
  const id = normalizeChapterId(chapters.length + 1);
  chapters.push({id, title: '', file: `${id}_yeni_bolum.md`, status: 'planned'});
  set(manifestData, 'structure.chapters', chapters);
  renderManifestChapters();
}

function renumberChapters() {
  syncChaptersFromTable();
  const chapters = get(manifestData, 'structure.chapters', []);
  chapters.forEach((ch, idx) => {
    const oldId = ch.id || normalizeChapterId(idx + 1);
    const id = normalizeChapterId(idx + 1);
    ch.id = id;
    if (!ch.file || ch.file.startsWith(oldId + '_') || /^chapter_\d{2}_/.test(ch.file)) {
      ch.file = `${id}_${safeSlug(ch.title || id)}.md`;
    }
  });
  renderManifestChapters();
  setStatus('Bölüm ID ve uygun dosya adları yeniden numaralandırıldı.', 'good');
}

function wizardData() {
  return {
    book: {title: $('wTitle').value, subtitle: $('wSubtitle').value, author: $('wAuthor').value, year: $('wYear').value, edition: '1', framework_version: 'v2.11.x'},
    language: {primary_language: 'tr', output_languages: ['tr'], file_naming_language: 'en', manifest_language: 'en', automation_language: 'en'},
    subject: $('wSubject').value,
    target_audience: $('wAudience').value,
    prerequisites: $('wPrereq').value,
    chapter_count: Number($('wChapterCount').value || 16),
    cumulative_app: {name: $('wAppName').value, description: $('wAppDesc').value},
    scope: {stack: lines($('wStack').value), out_of_scope: lines($('wOutScope').value)}
  };
}

async function makeArchitecturePrompt() {
  try {
    const data = await api('/api/wizard/architecture-prompt', {method: 'POST', body: JSON.stringify({root: root(), data: wizardData(), save: true})});
    $('architecturePrompt').value = data.prompt;
    setStatus('LLM kitap kurgusu promptu üretildi: ' + data.path, 'good');
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}

async function copyArchitecturePrompt() {
  await navigator.clipboard.writeText($('architecturePrompt').value);
  setStatus('Prompt panoya kopyalandı.', 'good');
}

async function initProject() {
  try {
    const manifest = collectManifestFromForm();
    const data = await api('/api/project/init', {method: 'POST', body: JSON.stringify({root: root(), manifest})});
    project = data;
    manifestData = structuredClone(data.manifest || manifest);
    renderDashboard(); renderChapters(); renderManifestForm(); await refreshManifest(false);
    setStatus('Klasör yapısı oluşturuldu ve manifest yazıldı.', 'good');
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}

function renderChapters() {
  const tbody = document.querySelector('#chapterTable tbody');
  const rows = project?.chapters || [];
  tbody.innerHTML = rows.map(r => `<tr>
    <td>${r.order}</td><td><code>${escapeHtml(r.id)}</code></td><td>${escapeHtml(r.title)}</td><td>${escapeHtml(r.status)}</td>
    <td>${r.prompt_exists ? '✅' : '—'}<br><small>${escapeHtml(r.prompt_path)}</small></td>
    <td>${r.chapter_exists ? '✅' : '—'}<br><small>${escapeHtml(r.chapter_path)}</small></td>
  </tr>`).join('');
}

async function startJob(step) {
  try {
    let options = {};
    try { options = JSON.parse($('jobOptions').value || '{}'); } catch { throw new Error('Seçenekler JSON biçiminde olmalı.'); }
    const job = await api('/api/jobs', {method: 'POST', body: JSON.stringify({root: root(), step, options})});
    activeJobId = job.id;
    $('jobInfo').textContent = `${job.step} — ${job.status} — ${job.id}`;
    $('jobLog').textContent = '';
    setStatus('İş başlatıldı: ' + job.step, 'good');
    pollJob();
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}

async function pollJob() {
  if (!activeJobId) return;
  clearTimeout(jobTimer);
  try {
    const job = await api('/api/jobs/' + activeJobId);
    $('jobInfo').textContent = `${job.step} — ${job.status} — rc=${job.returncode ?? '-'} — ${job.id}`;
    const log = await fetch('/api/jobs/' + activeJobId + '/log?root=' + encodeURIComponent(root())).then(r => r.text());
    $('jobLog').textContent = log;
    $('jobLog').scrollTop = $('jobLog').scrollHeight;
    if (job.status === 'running' || job.status === 'queued') {
      jobTimer = setTimeout(pollJob, 1500);
    } else {
      setStatus('İş tamamlandı: ' + job.status, job.status === 'success' ? 'good' : 'bad');
      await loadProject();
    }
  } catch (e) { setStatus('Job izleme hatası: ' + e.message, 'bad'); }
}

async function loadPipelineSteps() {
  const data = await api('/api/pipeline/steps');
  $('pipelineStep').innerHTML = data.steps.map(s => `<option value="${escapeHtml(s.id)}">${escapeHtml(s.group)} — ${escapeHtml(s.title)}</option>`).join('');
}

async function importChapter() {
  try {
    const data = await api('/api/chapters/import', {method: 'POST', body: JSON.stringify({root: root(), chapter_id: $('importChapterId').value, content: $('chapterContent').value})});
    setStatus('Bölüm Markdown kaydedildi: ' + data.path, 'good');
    await loadProject();
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}

function renderReports(reports) {
  $('reportList').innerHTML = reports.length ? reports.map(r => `<button data-path="${escapeHtml(r.path)}">${escapeHtml(r.path)}<br><small>${r.size} bayt · ${escapeHtml(r.modified || '')}</small></button>`).join('') : '<div class="item">Rapor yok.</div>';
  document.querySelectorAll('#reportList button').forEach(b => b.addEventListener('click', () => loadReport(b.dataset.path)));
}

async function refreshReports() {
  try {
    const data = await api('/api/reports?root=' + encodeURIComponent(root()));
    renderReports(data.reports || []);
    setStatus('Raporlar yenilendi.', 'good');
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}

async function loadReport(path) {
  try {
    const data = await api('/api/report?root=' + encodeURIComponent(root()) + '&path=' + encodeURIComponent(path));
    $('reportContent').textContent = data.content;
  } catch (e) { setStatus('Rapor okuma hatası: ' + e.message, 'bad'); }
}

$('loadProject').addEventListener('click', loadProject);
$('recentBooksSelect').addEventListener('change', async () => {
  const val = $('recentBooksSelect').value;
  if (val) { $('projectRoot').value = val; $('recentBooksSelect').value = ''; await loadProject(); }
});
$('refreshManifest').addEventListener('click', () => refreshManifest(true));
$('validateManifest').addEventListener('click', validateManifestFromForm);
$('saveManifestForm').addEventListener('click', saveManifestFromForm);
$('saveManifestYaml').addEventListener('click', saveManifestYaml);
$('loadYamlToForm').addEventListener('click', yamlToForm);
$('previewYaml').addEventListener('click', previewYaml);
$('initProject').addEventListener('click', initProject);
$('matchChapterFiles').addEventListener('click', matchChapterFiles);
$('addChapter').addEventListener('click', addChapter);
$('renumberChapters').addEventListener('click', renumberChapters);
$('makeArchitecturePrompt').addEventListener('click', makeArchitecturePrompt);
$('copyArchitecturePrompt').addEventListener('click', copyArchitecturePrompt);
$('generatePrompts').addEventListener('click', () => startJob('generate_chapter_prompts'));
$('refreshChapters').addEventListener('click', loadProject);
$('importChapter').addEventListener('click', importChapter);
$('runStep').addEventListener('click', () => startJob($('pipelineStep').value));
$('runFull').addEventListener('click', () => startJob('full_production'));
$('refreshReports').addEventListener('click', refreshReports);
['mBookTitle','mBookAuthor','mBookYear','mPrimaryLanguage','mPathChapters','mPathChapterPrompts','mPathBuild','mPathAssets','mPathExports'].forEach(id => $(id).addEventListener('input', markInvalidInputs));

initStudio();
