/**
 * BookFactory Studio Frontend Orchestrator v3.5
 * Author-Centric & Intelligent Quality Edition
 */

let project = null;
let manifestData = null;
let controlPanel = null;
let activeJobId = null;
let jobTimer = null;

const $ = (id) => document.getElementById(id);
const escapeHtml = (s) => (s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const lines = (s) => (s || '').split('\n').map(l => l.trim()).filter(l => l);

async function api(path, options = {}) {
  const res = await fetch(path, options);
  if (!res.ok) {
    const err = await res.json().catch(() => ({detail: res.statusText}));
    throw new Error(err.detail || res.statusText);
  }
  return res.json();
}

function setStatus(msg, type = '') {
  const el = $('status');
  el.textContent = msg;
  el.className = 'status ' + type;
}

function showTab(name, updateHash = true) {
  document.querySelectorAll('.tab').forEach(b => b.classList.toggle('active', b.dataset.tab === name));
  document.querySelectorAll('.panel').forEach(p => p.classList.toggle('visible', p.id === name));
  if (updateHash) history.replaceState(null, '', '#' + name);
  
  if (name === 'dashboard') renderDashboard();
  if (name === 'control') renderControlPanel();
  
  updateStepper(name);
}

function showManifestTab(name) {
  document.querySelectorAll('.manifest-tab').forEach(b => b.classList.toggle('active', b.dataset.mtab === name));
  document.querySelectorAll('.manifest-panel').forEach(p => p.classList.toggle('visible', p.id === name));
}

function get(obj, path, fallback = '') {
  return path.split('.').reduce((o, k) => (o && o[k] !== undefined ? o[k] : undefined), obj) ?? fallback;
}

function set(obj, path, value) {
  const parts = path.split('.');
  const last = parts.pop();
  const target = parts.reduce((o, k) => (o[k] = o[k] || {}), obj);
  target[last] = value;
}

async function loadProject() {
  try {
    setStatus('Kitap projesi yükleniyor...');
    const r = $('projectRoot').value.trim() || '.';
    project = await api('/api/project?root=' + encodeURIComponent(r));
    
    $('emptyState').classList.add('hidden');
    document.querySelectorAll('.panel:not(#emptyState)').forEach(p => p.classList.remove('hidden'));
    
    controlPanel = await api('/api/control-panel?root=' + encodeURIComponent(r));
    manifestData = structuredClone(project.manifest || {});
    renderDashboard();
    renderControlPanel();
    renderChapters();
    renderManifestForm();
    renderReports(project.reports || []);
    await loadPipelineSteps();
    await refreshManifest(false);
    const valid = project.validation?.valid;
    setStatus('Kitap projesi yüklendi: ' + project.root, valid ? 'good' : 'warn');
    
    if (r && r !== '.') {
      try {
        const cfg = await api('/api/studio/config', {method: 'POST', body: JSON.stringify({active_book: r})});
        renderRecentBooks(cfg.recent_books || []);
      } catch {}
    }
  } catch (e) {
    if (e.message.includes('manifest.yaml bulunamadı')) {
      $('emptyState').classList.remove('hidden');
      document.querySelectorAll('.panel:not(#emptyState)').forEach(p => p.classList.add('hidden'));
      setStatus('Lütfen bir kitap projesi seçin veya oluşturun.', 'warn');
    } else {
      setStatus('Hata: ' + e.message, 'bad');
    }
  }
}

function renderRecentBooks(roots) {
  const select = $('recentBooksSelect');
  if (!select) return;
  const first = select.options[0];
  select.innerHTML = '';
  select.appendChild(first);
  roots.forEach(r => {
    const opt = document.createElement('option');
    opt.value = r;
    opt.textContent = r.split(/[\\/]/).pop() || r;
    opt.title = r;
    select.appendChild(opt);
  });
}

function statusLabel(status) {
  if (status === 'ok') return '<span class="file-ok">OK</span>';
  if (status === 'fail') return '<span class="file-missing">FAIL</span>';
  return '<span class="warn">WARN</span>';
}

function updateMarkdownPreview() {
  const content = $('chapterContent').value;
  if (window.marked) {
    $('markdownPreview').innerHTML = marked.parse(content);
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
    warn.innerHTML = '<strong>Yanlış kök seçilmiş olabilir.</strong> BookFactory framework klasörü yerine doğrudan kitap klasörünü seçin.';
  } else {
    warn.classList.add('hidden');
  }
  const counts = project?.chapter_status_counts || {};
  $('statusCounts').innerHTML = Object.entries(counts).map(([k,v]) => `<span class="pill">${escapeHtml(k)}: ${v}</span>`).join('');
  const reports = (project?.reports || []).slice(0, 6);
  $('recentReports').innerHTML = reports.map(r => `<div class="item">${escapeHtml(r.path)}<br><small>${r.size} bayt</small></div>`).join('');
  updateSmartGuide();
}

function updateSmartGuide() {
  if (!project) return;
  const m = project.manifest || {};
  const matrix = controlPanel?.chapter_matrix || [];
  const missingFiles = matrix.filter(r => !r.full_text).length;
  const failedTests = controlPanel?.code_tests?.summary?.failed || 0;
  
  let nextAction = { text: "Projeniz harika görünüyor! Üretim aşamasına geçebilirsiniz.", btn: "Üretimi Başlat", tab: "production" };
  let currentStepTab = "dashboard";

  if (!m.book?.title || m.book.title === 'Yeni Kitap' || m.book.title === '-') {
    nextAction = { text: "Kitap bilgileri henüz girilmemiş. Lütfen temel bilgileri düzenleyin.", btn: "Manifesti Düzenle", tab: "manifest" };
    currentStepTab = "manifest";
  } else if (!m.structure?.chapters || m.structure.chapters.length === 0) {
    nextAction = { text: "Bölüm listesi boş. Kitap Sihirbazı ile mimariyi kurgulayabilirsiniz.", btn: "Sihirbaza Git", tab: "wizard" };
    currentStepTab = "wizard";
  } else if (missingFiles > 0) {
    nextAction = { text: `${missingFiles} bölüm dosyası henüz yazılmamış. Yazıma başlayın.`, btn: "Bölümleri Yönet", tab: "chapters" };
    currentStepTab = "chapters";
  } else if (failedTests > 0) {
    nextAction = { text: "Kod testlerinde hatalar tespit edildi. Lütfen düzeltmeleri yapın.", btn: "Kontrol Paneli", tab: "control" };
    currentStepTab = "control";
  } else {
    currentStepTab = "production";
  }

  $('guideText').textContent = nextAction.text;
  $('guideActionBtn').textContent = nextAction.btn;
  $('guideActionBtn').onclick = () => showTab(nextAction.tab);
  $('smartGuide').classList.remove('hidden');
  updateStepper(currentStepTab);
}

function updateStepper(activeTab) {
  const steps = document.querySelectorAll('.step');
  const tabToStep = { 'wizard': 1, 'manifest': 1, 'chapters': 2, 'control': 3, 'production': 5, 'dashboard': 1 };
  const currentStep = tabToStep[activeTab] || 1;
  steps.forEach(s => {
    const stepNum = parseInt(s.dataset.step);
    s.classList.toggle('active', stepNum === currentStep);
    s.classList.toggle('done', stepNum < currentStep);
  });
}

function renderControlPanel() {
  const data = controlPanel || {};
  const health = data.health || {};
  const checks = health.checks || [];
  $('healthPanel').innerHTML = checks.length ? checks.map(x => (
    `<div class="item">${statusLabel(x.status)} <strong>${escapeHtml(x.name)}</strong><br><small>${escapeHtml(x.detail || '')}</small></div>`
  )).join('') : '<div class="item">Sağlık verisi yok.</div>';

  const matrix = data.chapter_matrix || [];
  $('chapterMatrixTable').querySelector('tbody').innerHTML = matrix.length ? matrix.map(r => (
    `<tr>
      <td>${r.order}</td>
      <td><code>${escapeHtml(r.id)}</code><br><small>${escapeHtml(r.title)}</small></td>
      <td>${escapeHtml(r.status)}</td>
      <td>${r.full_text ? `✅ <button class="smallbtn" onclick="startConsistencyAudit('${r.id}')">Denetle</button>` : `<button class="smallbtn warn" onclick="generateSingleChapterPrompt('${r.id}')">Prompt Üret</button>`}</td>
      <td>${r.quality_report ? '✅' : '❌'}</td>
      <td>${r.code_tests?.failed > 0 ? '❌' : '✅'}</td>
      <td>${r.screenshots?.missing_files?.length > 0 ? '❌' : '✅'}</td>
    </tr>`
  )).join('') : '<tr><td colspan="7">Veri yok.</td></tr>';

  const failed = data.code_tests?.failed || [];
  $('repairPanel').innerHTML = failed.length ? failed.map(item => (
    `<div class="item">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <strong>${escapeHtml(item.id)}</strong>
        <button class="smallbtn" onclick="copyRepairPrompt('${item.id}')">Tamir Promptu</button>
      </div>
      <small style="color:var(--bad)">${escapeHtml(item.failure_reason)}</small>
    </div>`
  )).join('') : '<div class="item">Hata yok.</div>';
}

async function copyRepairPrompt(codeId) {
  try {
    const res = await api(`/api/jobs/repair-prompt/${codeId}?root=${encodeURIComponent($('projectRoot').value)}`);
    await navigator.clipboard.writeText(res.prompt);
    setStatus('Tamir promptu kopyalandı.', 'good');
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}

async function startConsistencyAudit(chapterId) {
  try {
    setStatus(`${chapterId} için tutarlılık denetimi başlatılıyor...`, 'warn');
    const job = await api(`/api/chapters/consistency-audit/${chapterId}?root=${encodeURIComponent($('projectRoot').value)}`, { method: 'POST' });
    pollJob(job.id);
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}

async function generateSingleChapterPrompt(chapterId) {
  try {
    setStatus(`${chapterId} için prompt üretiliyor...`, 'warn');
    const body = { root: $('projectRoot').value, step: 'generate_chapter_prompts', options: { chapter_id: chapterId } };
    const job = await api('/api/jobs', { method: 'POST', body: JSON.stringify(body) });
    pollJob(job.id);
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}

async function openDebugger(chapterId, codeId) {
  try {
    setStatus('Kod yükleniyor...', 'warn');
    const res = await api(`/api/code/block/${chapterId}/${codeId}?root=${encodeURIComponent($('projectRoot').value)}`);
    const codeTests = controlPanel.code_tests.failed || [];
    const errorItem = codeTests.find(x => x.id === codeId);
    
    let errorLog = "Hata kaydı bulunamadı.";
    if (errorItem && errorItem.steps) {
        errorLog = errorItem.steps.map(s => `--- STEP: ${s.name} ---\n${s.stderr || s.stdout || ''}`).join('\n\n');
    }

    $('debugCodeId').textContent = codeId;
    $('debugCodeEditor').value = res.code;
    $('debugOutput').textContent = errorLog;
    $('debugModal').classList.remove('hidden');
    
    // Attach current IDs to the save button
    $('saveAndTestCode').dataset.chapterId = chapterId;
    $('saveAndTestCode').dataset.codeId = codeId;
    
    setStatus('Hata ayıklama modu aktif.', 'good');
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}

async function saveAndTestCode() {
  const btn = $('saveAndTestCode');
  const chapterId = btn.dataset.chapterId;
  const codeId = btn.dataset.codeId;
  const code = $('debugCodeEditor').value;

  try {
    setStatus('Kod kaydediliyor...', 'warn');
    await api('/api/code/update', {
      method: 'POST',
      body: JSON.stringify({
        root: $('projectRoot').value,
        chapter_id: chapterId,
        code_id: codeId,
        code: code
      })
    });
    
    setStatus('Kod güncellendi. Test başlatılıyor...', 'warn');
    // Re-run code tests (minimal context)
    const job = await api('/api/jobs', {
      method: 'POST',
      body: JSON.stringify({
        root: $('projectRoot').value,
        step: 'test_code',
        options: {}
      })
    });
    
    $('debugModal').classList.add('hidden');
    pollJob(job.id);
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}

$('closeDebug').addEventListener('click', () => $('debugModal').classList.add('hidden'));
$('saveAndTestCode').addEventListener('click', saveAndTestCode);

async function pollJob(jobId) {
  const poll = async () => {
    try {
      const job = await api('/api/jobs/' + jobId);
      activeJobId = jobId;
      const log = await api(`/api/jobs/${jobId}/log?root=${encodeURIComponent($('projectRoot').value)}`);
      $('jobLog').textContent = log;
      $('jobLog').scrollTop = $('jobLog').scrollHeight;
      if (job.status === 'running' || job.status === 'queued') setTimeout(poll, 1500);
      else { setStatus('İş tamamlandı: ' + job.status, job.status === 'success' ? 'good' : 'bad'); await loadProject(); }
    } catch (e) { console.error(e); }
  };
  poll();
}

async function refreshManifest(updateForm = true) {
  try {
    const data = await api('/api/manifest?root=' + encodeURIComponent($('projectRoot').value));
    manifestData = data.manifest;
    $('manifestYaml').value = data.yaml;
    if (updateForm) renderManifestForm();
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}

function renderManifestForm() {
  const m = manifestData;
  if (!m) return;
  $('mBookTitle').value = get(m, 'book.title');
  $('mBookAuthor').value = get(m, 'book.author');
  $('mCourseCode').value = get(m, 'academic.course_code');
  $('mCourseName').value = get(m, 'academic.course_name');
  renderGlossaryRows();
}

function renderGlossaryRows() {
  const terms = get(manifestData, 'glossary', []);
  const tbody = $('manifestGlossaryRows');
  if (!tbody) return;
  tbody.innerHTML = terms.map((t, idx) => (
    `<tr>
      <td><input class="g-term" value="${escapeHtml(t.term)}" /></td>
      <td><input class="g-def" value="${escapeHtml(t.definition)}" /></td>
      <td><button class="smallbtn danger" onclick="removeGlossaryRow(${idx})">Sil</button></td>
    </tr>`
  )).join('');
}

function addGlossaryRow() {
  if (!manifestData.glossary) manifestData.glossary = [];
  manifestData.glossary.push({term: 'Yeni Terim', definition: ''});
  renderGlossaryRows();
}

function removeGlossaryRow(idx) {
  manifestData.glossary.splice(idx, 1);
  renderGlossaryRows();
}

async function startJob(step) {
  try {
    const body = { root: $('projectRoot').value, step, options: JSON.parse($('jobOptions').value || '{}') };
    const job = await api('/api/jobs', { method: 'POST', body: JSON.stringify(body) });
    pollJob(job.id);
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}

// Event Listeners
$('loadProject').addEventListener('click', loadProject);
$('toggleDarkMode').addEventListener('click', () => {
  const isDark = document.body.classList.toggle('dark-mode');
  localStorage.setItem('darkMode', isDark);
});
if (localStorage.getItem('darkMode') === 'true') document.body.classList.add('dark-mode');

$('chapterContent').addEventListener('input', updateMarkdownPreview);
$('addGlossaryTerm').addEventListener('click', addGlossaryRow);
$('runStep').addEventListener('click', () => startJob($('pipelineStep').value));
$('runFull').addEventListener('click', () => startJob('full_production'));
$('runWebSite').addEventListener('click', () => startJob('generate-web-site'));

// Keyboard Shortcuts
window.addEventListener('keydown', (e) => {
  if (e.altKey && e.key >= '1' && e.key <= '7') {
    const tabs = ['dashboard', 'control', 'wizard', 'manifest', 'chapters', 'production', 'reports'];
    showTab(tabs[parseInt(e.key) - 1]);
  }
});

async function refreshMedia() {
  try {
    const data = await api('/api/assets?root=' + encodeURIComponent($('projectRoot').value));
    renderMedia(data.assets || []);
    setStatus('Medya kütüphanesi yenilendi.', 'good');
  } catch (e) { setStatus('Medya listeleme hatası: ' + e.message, 'bad'); }
}

function renderMedia(assets) {
  const grid = $('mediaGrid');
  grid.innerHTML = assets.map(a => `
    <div class="media-item">
      <div class="media-thumb">
        <img src="/api/project/file?path=${encodeURIComponent(a.rel_path)}&root=${encodeURIComponent($('projectRoot').value)}" alt="${escapeHtml(a.name)}" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAiIGhlaWdodD0iMTAwIj48cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iI2Y4ZmFmYyIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBkb21pbmFudC1iYXNlbGluZT0ibWlkZGxlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjOTRhM2I4IiBmb250LXNpemU9IjE0Ij5Hw7Zyc2VsPC90ZXh0Pjwvc3ZnPg=='">
      </div>
      <div class="media-info">
        <div class="media-name" title="${escapeHtml(a.name)}">${escapeHtml(a.name)}</div>
        <div class="media-meta">${a.type.toUpperCase()} · ${(a.size/1024).toFixed(1)} KB</div>
        <div class="media-actions">
          <button class="smallbtn" onclick="copyMarkdownLink('${a.rel_path}', '${a.name}')">MD Link</button>
          <button class="smallbtn secondary" onclick="window.open('/api/project/file?path=${encodeURIComponent(a.rel_path)}&root=${encodeURIComponent($('projectRoot').value)}', '_blank')">Aç</button>
        </div>
      </div>
    </div>
  `).join('');
}

async function copyMarkdownLink(path, name) {
  // Use relative path from chapters/ for markdown
  const mdPath = path.replace('assets/', '../assets/');
  const link = `![${name.split('.')[0]}](${mdPath})`;
  await navigator.clipboard.writeText(link);
  setStatus('Markdown görsel linki kopyalandı.', 'good');
}

async function uploadFiles(files) {
  for (const file of files) {
    try {
      setStatus(`${file.name} yükleniyor...`, 'warn');
      const formData = new FormData();
      formData.append('file', file);
      await api(`/api/assets/upload?root=${encodeURIComponent($('projectRoot').value)}`, {
        method: 'POST',
        body: formData
      });
      setStatus(`${file.name} başarıyla yüklendi.`, 'good');
    } catch (e) { setStatus('Yükleme hatası: ' + e.message, 'bad'); }
  }
  refreshMedia();
}

// Drag & Drop Listeners
const dropZone = $('dropZone');
dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('active'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('active'));
dropZone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropZone.classList.remove('active');
  if (e.dataTransfer.files.length) uploadFiles(e.dataTransfer.files);
});
dropZone.addEventListener('click', () => $('mediaUploadInput').click());
$('mediaUploadInput').addEventListener('change', (e) => {
  if (e.target.files.length) uploadFiles(e.target.files);
});
$('refreshMedia').addEventListener('click', refreshMedia);

async function loadPipelineSteps() {
  const data = await api('/api/pipeline/steps');
  $('pipelineStep').innerHTML = data.steps.map(s => `<option value="${s.id}">${s.title}</option>`).join('');
}

function initStudio() {
  loadProject();
}

initStudio();
