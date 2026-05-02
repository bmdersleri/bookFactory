/**
 * BookFactory Studio Frontend Orchestrator v4.0
 * Technical Verticalization Edition
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
  if (options.body && !options.headers) {
    options.headers = { 'Content-Type': 'application/json' };
  }
  const res = await fetch(path, options);
  if (!res.ok) {
    let msg = res.statusText;
    try {
      const err = await res.json();
      if (err.detail) {
        if (typeof err.detail === 'string') msg = err.detail;
        else if (Array.isArray(err.detail)) msg = err.detail.map(d => `${d.loc.join('.')}: ${d.msg}`).join(', ');
        else msg = JSON.stringify(err.detail);
      }
    } catch (e) {}
    throw new Error(msg);
  }
  return res.json();
}

function setStatus(msg, type = '') {
  const el = $('status');
  el.textContent = msg;
  el.className = 'status ' + type;
  if (type === 'good' || type === 'bad' || type === 'warn') {
    showToast(msg, type === 'good' ? 'success' : (type === 'bad' ? 'error' : 'warning'));
  }
}

function showToast(msg, type = 'success') {
  const container = $('toastContainer');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<div class="toast-msg">${msg}</div><div class="toast-close">&times;</div>`;
  container.appendChild(toast);
  setTimeout(() => toast.classList.add('visible'), 10);
  const close = () => { toast.classList.remove('visible'); setTimeout(() => toast.remove(), 400); };
  toast.onclick = close;
  setTimeout(close, 5000);
}

// Tooltip Logic
document.addEventListener('mouseover', (e) => {
  const help = e.target.closest('.help-icon');
  if (help) {
    const tt = $('tooltip');
    tt.textContent = help.dataset.help;
    tt.classList.add('visible');
    const rect = help.getBoundingClientRect();
    tt.style.top = (rect.top - tt.offsetHeight - 10) + 'px';
    tt.style.left = (rect.left + (rect.width/2) - (tt.offsetWidth/2)) + 'px';
  }
});
document.addEventListener('mouseout', (e) => { if (e.target.closest('.help-icon')) $('tooltip').classList.remove('visible'); });

function showTab(name, updateHash = true) {
  document.querySelectorAll('.tab').forEach(b => b.classList.toggle('active', b.dataset.tab === name));
  document.querySelectorAll('.panel').forEach(p => p.classList.toggle('visible', p.id === name));
  if (updateHash) history.replaceState(null, '', '#' + name);
  if (name === 'dashboard') renderDashboard();
  if (name === 'control') renderControlPanel();
  if (name === 'media') refreshMedia();
  if (name === 'cloud') refreshCloudStatus();
  updateStepper(name);
}

function showManifestTab(name) {
  document.querySelectorAll('.manifest-tab').forEach(b => b.classList.toggle('active', b.dataset.mtab === name));
  document.querySelectorAll('.manifest-panel').forEach(p => p.classList.toggle('visible', p.id === name));
}

function get(obj, path, fallback = '') { return path.split('.').reduce((o, k) => (o && o[k] !== undefined ? o[k] : undefined), obj) ?? fallback; }
function set(obj, path, value) {
  const parts = path.split('.');
  const last = parts.pop();
  const target = parts.reduce((o, k) => (o[k] = o[k] || {}), obj);
  target[last] = value;
}

async function loadProject() {
  try {
    const r = $('projectRoot').value.trim() || '.';
    project = await api('/api/project?root=' + encodeURIComponent(r));
    $('emptyState').classList.add('hidden');
    document.querySelectorAll('.panel:not(#emptyState)').forEach(p => p.classList.remove('hidden'));
    controlPanel = await api('/api/control-panel?root=' + encodeURIComponent(r));
    manifestData = structuredClone(project.manifest || {});
    renderDashboard(); renderControlPanel(); renderChapters(); renderManifestForm();
    await loadPipelineSteps();
    await refreshManifest(false);
    setStatus('Kitap yüklendi: ' + project.root, 'good');
  } catch (e) {
    if (e.message.includes('bulunamadı')) {
      $('emptyState').classList.remove('hidden');
      document.querySelectorAll('.panel:not(#emptyState)').forEach(p => p.classList.add('hidden'));
    } else setStatus('Hata: ' + e.message, 'bad');
  }
}

// Markdown Toolbar Logic
function insertMD(type) {
  const area = $('chapterContent');
  const start = area.selectionStart, end = area.selectionEnd, text = area.value;
  const selection = text.substring(start, end);
  let insert = "";
  switch(type) {
    case 'bold': insert = `**${selection || 'kalın'}**`; break;
    case 'italic': insert = `*${selection || 'eğik'}*`; break;
    case 'code': insert = `\`${selection || 'kod'}\``; break;
    case 'block': insert = `\n\`\`\`python\n${selection || '# kod'}\n\`\`\`\n`; break;
    case 'table': insert = `\n| B1 | B2 |\n|---|---|\n| H1 | H2 |\n`; break;
    case 'link': insert = `[${selection || 'link'}](https://)`; break;
  }
  area.value = text.substring(0, start) + insert + text.substring(end);
  area.focus(); updateMarkdownPreview();
}

function updateMarkdownPreview() { if (window.marked) $('markdownPreview').innerHTML = marked.parse($('chapterContent').value); }
function openMetaWizard() { $('metaWizardModal').classList.remove('hidden'); }

let progressChart = null;
function renderCharts(matrix) {
  const counts = { final: 0, total: matrix.length || 1 };
  const heatmap = $('healthHeatmap'); heatmap.innerHTML = '';
  matrix.forEach(r => {
    if (r.status === 'final') counts.final++;
    const box = document.createElement('div');
    box.className = `heatmap-box status-${r.status}${r.code_tests?.failed > 0 ? ' status-error' : ''}`;
    box.textContent = r.order;
    box.onclick = () => { $('importChapterId').value = r.id; showTab('chapters'); };
    heatmap.appendChild(box);
  });
  const percent = Math.round((counts.final / counts.total) * 100);
  if (progressChart) progressChart.destroy();
  const ctx = $('progressChart').getContext('2d');
  progressChart = new Chart(ctx, { type: 'doughnut', data: { datasets: [{ data: [counts.final, counts.total - counts.final], backgroundColor: ['#126b3f', '#e9ecef'], borderWidth: 0 }] }, options: { cutout: '80%', plugins: { tooltip: { enabled: false } } } });
  document.querySelector('.chart-label').textContent = `%${percent}`;
}

function renderDashboard() {
  const m = project?.manifest || {};
  $('bookTitle').textContent = m.book?.title || '-';
  $('bookAuthor').textContent = m.book?.author || '-';
  $('chapterCount').textContent = (project?.chapters || []).length;
  if (controlPanel?.chapter_matrix) renderCharts(controlPanel.chapter_matrix);
  updateSmartGuide();
}

function updateSmartGuide() {
  if (!project) return;
  const m = project.manifest || {}, matrix = controlPanel?.chapter_matrix || [];
  const missing = matrix.filter(r => !r.full_text).length;
  let next = { text: "Hazırsınız!", btn: "Üretim", tab: "production" };
  if (!m.book?.title) next = { text: "Kitap bilgileri eksik.", btn: "Düzenle", tab: "manifest" };
  else if (missing > 0) next = { text: `${missing} bölüm yazılmamış.`, btn: "Yaz", tab: "chapters" };
  $('guideText').textContent = next.text;
  $('guideActionBtn').textContent = next.btn;
  $('guideActionBtn').onclick = () => showTab(next.tab);
  $('smartGuide').classList.remove('hidden');
  updateStepper(next.tab);
}

function updateStepper(activeTab) {
  const tabToStep = { 'wizard': 1, 'manifest': 1, 'chapters': 2, 'control': 3, 'production': 5, 'dashboard': 1 };
  const currentStep = tabToStep[activeTab] || 1;
  document.querySelectorAll('.step').forEach(s => {
    const stepNum = parseInt(s.dataset.step);
    s.classList.toggle('active', stepNum === currentStep);
    s.classList.toggle('done', stepNum < currentStep);
  });
}

function renderControlPanel() {
  const data = controlPanel || {}, matrix = data.chapter_matrix || [];
  $('chapterMatrixTable').querySelector('tbody').innerHTML = matrix.map(r => (
    `<tr><td>${r.order}</td><td><code>${r.id}</code></td><td>${r.status}</td><td>${r.full_text ? `✅ <button class="smallbtn" onclick="startConsistencyAudit('${r.id}')">Audit</button> <button class="smallbtn secondary" onclick="startEditorReview('${r.id}')">Editör</button>` : `<button class="smallbtn warn" onclick="generateSingleChapterPrompt('${r.id}')">Prompt</button>`}</td><td>${r.quality_report?'✅':'❌'}</td><td>${r.code_tests?.failed>0?'❌':'✅'}</td><td>${r.screenshots?.missing_files?.length>0?'❌':'✅'}</td></tr>`
  )).join('');
  const failed = data.code_tests?.failed || [];
  $('repairPanel').innerHTML = failed.map(item => `<div class="item"><strong>${item.id}</strong> <button class="smallbtn" onclick="openDebugger('${item.chapter_id}', '${item.id}')">Hata Ayıkla</button></div>`).join('') || '<div class="item">Hata yok.</div>';
}

async function startConsistencyAudit(cid) { const job = await api(`/api/chapters/consistency-audit/${cid}?root=${encodeURIComponent($('projectRoot').value)}`, { method: 'POST' }); pollJob(job.id); }
async function startEditorReview(cid) { const job = await api(`/api/chapters/editor-review/${cid}?root=${encodeURIComponent($('projectRoot').value)}`, { method: 'POST' }); pollJob(job.id); }
async function generateSingleChapterPrompt(cid) { const job = await api('/api/jobs', { method: 'POST', body: JSON.stringify({ root: $('projectRoot').value, step: 'generate_chapter_prompts', options: { chapter_id: cid } }) }); pollJob(job.id); }

async function openDebugger(chapterId, codeId) {
  const res = await api(`/api/code/block/${chapterId}/${codeId}?root=${encodeURIComponent($('projectRoot').value)}`);
  $('debugCodeId').textContent = codeId; $('debugCodeEditor').value = res.code; $('debugModal').classList.remove('hidden');
  $('saveAndTestCode').dataset.chapterId = chapterId; $('saveAndTestCode').dataset.codeId = codeId;
}

async function saveAndTestCode() {
  const btn = $('saveAndTestCode');
  await api('/api/code/update', { method: 'POST', body: JSON.stringify({ root: $('projectRoot').value, chapter_id: btn.dataset.chapterId, code_id: btn.dataset.codeId, code: $('debugCodeEditor').value }) });
  const job = await api('/api/jobs', { method: 'POST', body: JSON.stringify({ root: $('projectRoot').value, step: 'test_code', options: {} }) });
  $('debugModal').classList.add('hidden'); pollJob(job.id);
}

async function pollJob(jobId) {
  const poll = async () => {
    try {
      const job = await api('/api/jobs/' + jobId);
      const log = await api(`/api/jobs/${jobId}/log?root=${encodeURIComponent($('projectRoot').value)}`);
      $('jobLog').textContent = log;
      if (job.status === 'running' || job.status === 'queued') setTimeout(poll, 1500);
      else { setStatus('İş tamamlandı: ' + job.status, 'good'); await loadProject(); }
    } catch (e) { console.error(e); }
  };
  poll();
}

async function refreshManifest(updateForm = true) {
  const data = await api('/api/manifest?root=' + encodeURIComponent($('projectRoot').value));
  manifestData = data.manifest; $('manifestYaml').value = data.yaml;
  if (updateForm) renderManifestForm();
}

function renderManifestForm() {
  const m = manifestData; if (!m) return;
  $('mBookTitle').value = get(m, 'book.title');
  $('mBookAuthor').value = get(m, 'book.author');
  $('mCourseCode').value = get(m, 'academic.course_code');
  $('mCourseName').value = get(m, 'academic.course_name');
  $('mStyleProfile').value = get(m, 'language.style_profile', 'Academic');
  $('mPedagogicalModel').value = get(m, 'language.pedagogical_model', 'Bloom');
  
  $('mComplexity').value = get(m, 'authoring.complexity_level', 'Intermediate');
  $('mContext').value = get(m, 'authoring.industrial_context', 'Academic');
  $('mNaming').value = get(m, 'authoring.coding_conventions.variable_naming', 'snake_case');
  $('mHinting').value = get(m, 'authoring.coding_conventions.type_hinting', 'optional');
  $('mMath').value = get(m, 'authoring.math_rigor', 'Minimal');

  renderGlossaryRows(); renderManifestChapterRows(); renderResourceRows();
}

function renderChapters() {
  const chapters = manifestData?.structure?.chapters || [];
  const tbody = $('chapterTable').querySelector('tbody');
  if (tbody) {
    tbody.innerHTML = chapters.map((ch, idx) => `<tr><td>${idx+1}</td><td><code>${ch.id}</code></td><td>${ch.title}</td><td>${ch.status}</td><td><button class="smallbtn" onclick="loadChapter('${ch.id}')">Düzenle</button></td></tr>`).join('');
  }
}

async function loadChapter(cid) {
  try {
    const res = await api(`/api/chapters/read/${cid}?root=${encodeURIComponent($('projectRoot').value)}`);
    $('importChapterId').value = cid;
    $('chapterContent').value = res.content;
    updateMarkdownPreview();
    showTab('chapters');
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}

async function saveChapter() {
  try {
    const cid = $('importChapterId').value.trim();
    if (!cid) return setStatus('Bölüm ID eksik.', 'bad');
    await api('/api/chapters/save', {
      method: 'POST',
      body: JSON.stringify({ root: $('projectRoot').value, chapter_id: cid, content: $('chapterContent').value })
    });
    setStatus('Bölüm kaydedildi.', 'good');
    await loadProject();
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}

function renderManifestChapterRows() {
  const chapters = manifestData.structure?.chapters || [];
  const tbody = $('manifestChapterRows'); if (!tbody) return;
  tbody.innerHTML = chapters.map((ch, idx) => `<tr data-idx="${idx}"><td class="drag-handle">☰</td><td>${idx+1}</td><td><input class="c-id" value="${escapeHtml(ch.id)}" /></td><td><input class="c-title" value="${escapeHtml(ch.title)}" /></td><td><input class="c-file" value="${escapeHtml(ch.file || '')}" /></td><td><select class="c-status"><option ${ch.status==='planned'?'selected':''}>planned</option><option ${ch.status==='draft'?'selected':''}>draft</option><option ${ch.status==='final'?'selected':''}>final</option></select></td><td><button class="smallbtn danger" onclick="removeChapterRow(${idx})">Sil</button></td></tr>`).join('');
  if (!window.manifestSortable) window.manifestSortable = new Sortable(tbody, { handle: '.drag-handle', onEnd: () => {
    const news = []; tbody.querySelectorAll('tr').forEach(tr => news.push(manifestData.structure.chapters[parseInt(tr.dataset.idx)]));
    manifestData.structure.chapters = news; renderManifestChapterRows();
  }});
}

function renderResourceRows() {
  const resources = get(manifestData, 'resources', []);
  const tbody = $('manifestResourceRows'); if (!tbody) return;
  tbody.innerHTML = resources.map((r, idx) => `<tr><td><input class="r-id" value="${escapeHtml(r.id)}" /></td><td><input class="r-title" value="${escapeHtml(r.title)}" /></td><td><input class="r-path" value="${escapeHtml(r.path)}" /></td><td><select class="r-type"><option ${r.type==='dataset'?'selected':''} value="dataset">dataset</option><option ${r.type==='documentation'?'selected':''} value="documentation">documentation</option><option ${r.type==='external_link'?'selected':''} value="external_link">link</option></select></td><td><button class="smallbtn danger" onclick="removeResourceRow(${idx})">Sil</button></td></tr>`).join('');
}
function addResourceRow() { if (!manifestData.resources) manifestData.resources = []; manifestData.resources.push({id: 'data_01', title: 'Veri', path: '', type: 'dataset'}); renderResourceRows(); }
function removeResourceRow(idx) { manifestData.resources.splice(idx, 1); renderResourceRows(); }

function renderGlossaryRows() {
  const terms = get(manifestData, 'glossary', []);
  const tbody = $('manifestGlossaryRows'); if (!tbody) return;
  tbody.innerHTML = terms.map((t, idx) => `<tr><td><input class="g-term" value="${escapeHtml(t.term)}" /></td><td><input class="g-def" value="${escapeHtml(t.definition)}" /></td><td><button class="smallbtn danger" onclick="removeGlossaryRow(${idx})">Sil</button></td></tr>`).join('');
}

function addGlossaryRow() { if (!manifestData.glossary) manifestData.glossary = []; manifestData.glossary.push({term: 'Yeni', definition: ''}); renderGlossaryRows(); }
function removeGlossaryRow(idx) { manifestData.glossary.splice(idx, 1); renderGlossaryRows(); }
function addChapterRow() { 
  if (!manifestData.structure) manifestData.structure = { chapters: [] };
  if (!manifestData.structure.chapters) manifestData.structure.chapters = [];
  const n = manifestData.structure.chapters.length + 1;
  const id = `chapter_${n.toString().padStart(2, '0')}`;
  manifestData.structure.chapters.push({id, title: 'Yeni Bölüm', file: `${id}.md`, status: 'planned'}); 
  renderManifestChapterRows(); 
}
function removeChapterRow(idx) { manifestData.structure.chapters.splice(idx, 1); renderManifestChapterRows(); }

function renumberChapters() {
  if (!manifestData.structure?.chapters) return;
  manifestData.structure.chapters.forEach((ch, idx) => {
    const n = idx + 1;
    const id = `chapter_${n.toString().padStart(2, '0')}`;
    ch.id = id;
    ch.file = `${id}.md`;
  });
  renderManifestChapterRows();
  showToast('Bölümler yeniden numaralandırıldı.');
}

async function matchChapterFiles() {
  try {
    const res = await api('/api/manifest/match-chapter-files', {
      method: 'POST',
      body: JSON.stringify({ root: $('projectRoot').value, manifest: manifestData })
    });
    manifestData = res.manifest;
    renderManifestChapterRows();
    showToast('Dosyalar eşleştirildi.');
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}

async function saveManifestForm() {
  const m = structuredClone(manifestData);
  m.book = {
    title: $('mBookTitle').value,
    subtitle: $('mBookSubtitle').value,
    author: $('mBookAuthor').value,
    edition: $('mBookEdition').value,
    year: parseInt($('mBookYear').value) || new Date().getFullYear(),
    framework_version: $('mFrameworkVersion').value
  };
  
  m.language = {
    primary: $('mPrimaryLanguage').value,
    output_languages: $('mOutputLanguages').value.split(',').map(s => s.trim()).filter(s => s),
    style_profile: $('mStyleProfile').value,
    pedagogical_model: $('mPedagogicalModel').value
  };

  m.cumulative_app = {
    name: $('mAppName').value,
    description: $('mAppDescription').value
  };

  m.academic = { 
    course_code: $('mCourseCode').value, 
    course_name: $('mCourseName').value,
    ects: parseInt($('mEcts').value) || 5,
    learning_outcomes: lines($('mLearningOutcomes').value)
  };

  m.authoring = { 
    complexity_level: $('mComplexity').value, 
    industrial_context: $('mContext').value, 
    math_rigor: $('mMath').value,
    coding_conventions: { 
      variable_naming: $('mNaming').value, 
      type_hinting: $('mHinting').value 
    }
  };

  m.automation = {
    project_status: $('mProjectStatus').value,
    code_extract: $('mCodeExtract').checked,
    code_test: $('mCodeTest').checked,
    github_sync: $('mGithubSync').checked,
    qr_generation: $('mQrGeneration').checked,
    screenshot_automation: $('mScreenshotAutomation').checked,
    mermaid_generation: $('mMermaidGeneration').checked,
    manual_asset_override: $('mManualOverride').checked,
    qr_threshold: parseInt($('mQrThreshold').value) || 15
  };

  m.paths = {
    chapters: $('mPathChapters').value,
    chapter_prompts: $('mPathChapterPrompts').value,
    chapter_backups: $('mPathChapterBackups').value,
    build: $('mPathBuild').value,
    assets: $('mPathAssets').value,
    exports: $('mPathExports').value
  };

  m.scope = {
    stack: lines($('mScopeStack').value),
    out_of_scope: lines($('mOutOfScope').value)
  };
  
  // Sync chapters from table
  if (!m.structure) m.structure = { chapters: [] };
  m.structure.chapters = [];
  document.querySelectorAll('#manifestChapterRows tr').forEach(tr => {
    const id = tr.querySelector('.c-id').value.trim();
    if (id) m.structure.chapters.push({ 
      id, 
      title: tr.querySelector('.c-title').value.trim(), 
      file: tr.querySelector('.c-file').value.trim(), 
      status: tr.querySelector('.c-status').value 
    });
  });

  // Sync resources from table
  m.resources = [];
  document.querySelectorAll('#manifestResourceRows tr').forEach(tr => {
    const id = tr.querySelector('.r-id').value.trim();
    if (id) m.resources.push({ id, title: tr.querySelector('.r-title').value.trim(), path: tr.querySelector('.r-path').value.trim(), type: tr.querySelector('.r-type').value });
  });

  // Sync glossary from table
  m.glossary = [];
  document.querySelectorAll('#manifestGlossaryRows tr').forEach(tr => {
    const termInput = tr.querySelector('.g-term');
    const defInput = tr.querySelector('.g-def');
    if (termInput && termInput.value.trim()) {
      m.glossary.push({ term: termInput.value.trim(), definition: defInput ? defInput.value.trim() : '' });
    }
  });

  await api('/api/manifest/save', { method: 'POST', body: JSON.stringify({ root: $('projectRoot').value, manifest: m }) });
  setStatus('Kaydedildi.', 'good'); await loadProject();
}

async function refreshMedia() {
  const data = await api('/api/assets?root=' + encodeURIComponent($('projectRoot').value));
  $('mediaGrid').innerHTML = data.assets.map(a => `<div class="media-item"><div class="media-thumb"><img src="/api/project/file?path=${encodeURIComponent(a.rel_path)}&root=${encodeURIComponent($('projectRoot').value)}"></div><div class="media-info"><div class="media-name">${escapeHtml(a.name)}</div><button class="smallbtn" onclick="copyMarkdownLink('${a.rel_path}', '${a.name}')">Link</button></div></div>`).join('');
}

async function refreshCloudStatus() {
  try {
    const status = await api('/api/cloud/status?root=' + encodeURIComponent($('projectRoot').value));
    const setInd = (id, val) => {
      const el = $(id);
      el.textContent = val ? 'YÜKLÜ' : 'EKSİK';
      el.className = 'status-indicator ' + (val ? 'good' : 'bad');
    };
    setInd('statusCodespace', status.codespace);
    setInd('statusActions', status.github_actions);
    setInd('statusDigitalTwin', status.digital_twin);
  } catch (e) { console.error(e); }
}

async function provisionCloud() {
  try {
    setStatus('GitHub yapılandırmaları oluşturuluyor...', 'warn');
    const res = await api('/api/cloud/provision?root=' + encodeURIComponent($('projectRoot').value), { method: 'POST' });
    setStatus(`${res.provisioned_files.length} dosya oluşturuldu.`, 'good');
    await refreshCloudStatus();
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}

async function copyMarkdownLink(path, name) { await navigator.clipboard.writeText(`![${name.split('.')[0]}](../${path})`); showToast('Link kopyalandı.'); }

async function saveManifestYaml() {
  try {
    const yaml_text = $('manifestYaml').value;
    await api('/api/manifest/save-yaml', { method: 'POST', body: JSON.stringify({ root: $('projectRoot').value, yaml_text }) });
    setStatus('YAML kaydedildi.', 'good');
    await loadProject();
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}

async function refreshControlPanel() {
  try {
    controlPanel = await api('/api/control-panel?root=' + encodeURIComponent($('projectRoot').value));
    renderControlPanel();
    setStatus('Panel yenilendi.', 'good');
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}

async function refreshReports() {
  try {
    const data = await api('/api/reports?root=' + encodeURIComponent($('projectRoot').value));
    $('reportList').innerHTML = data.reports.map(r => `<div class="item" onclick="loadReport('${r.path}')">${r.name} <small>${r.date}</small></div>`).join('');
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}

async function loadReport(path) {
  const res = await api(`/api/project/file?path=${encodeURIComponent(path)}&root=${encodeURIComponent($('projectRoot').value)}`);
  $('reportContent').textContent = typeof res === 'string' ? res : JSON.stringify(res, null, 2);
}

async function initProject() {
  try {
    const data = {
      title: $('wTitle').value,
      subtitle: $('wSubtitle').value,
      author: $('wAuthor').value,
      year: $('wYear').value,
      subject: $('wSubject').value,
      audience: $('wAudience').value,
      prerequisites: $('wPrereq').value,
      chapter_count: parseInt($('wChapterCount').value),
      app_name: $('wAppName').value,
      app_description: $('wAppDesc').value,
      stack: $('wStack').value
    };
    setStatus('Proje başlatılıyor...', 'warn');
    const res = await api('/api/wizard/init-project', {
      method: 'POST',
      body: JSON.stringify({ root: $('projectRoot').value, data })
    });
    setStatus('Proje başarıyla oluşturuldu: ' + res.path, 'good');
    await loadProject();
    showTab('dashboard');
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}

async function makeArchitecturePrompt() {
  try {
    const data = {
      book: {
        title: $('wTitle').value,
        subtitle: $('wSubtitle').value,
        author: $('wAuthor').value,
        year: $('wYear').value
      },
      subject: $('wSubject').value,
      audience: $('wAudience').value,
      prerequisites: $('wPrereq').value,
      chapter_count: parseInt($('wChapterCount').value),
      cumulative_app: {
        name: $('wAppName').value,
        description: $('wAppDesc').value
      },
      scope: {
        stack: lines($('wStack').value),
        out_of_scope: lines($('wOutScope').value)
      }
    };
    const res = await api('/api/wizard/architecture-prompt', {
      method: 'POST',
      body: JSON.stringify({
        root: $('projectRoot').value,
        data: data,
        save: false,
        use_rag: $('useRagToggle').checked,
        rag_query: $('ragQueryInput').value
      })
    });
    $('architecturePrompt').value = res.prompt;
    showToast('Mimari prompt üretildi.');
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}


async function validateManifest() {
  try {
    const res = await api('/api/manifest/validate', {
      method: 'POST',
      body: JSON.stringify({ root: $('projectRoot').value, manifest: manifestData })
    });
    const box = $('manifestValidationBox');
    box.className = 'validation-box ' + (res.valid ? 'good' : 'bad');
    box.innerHTML = res.valid ? '✅ Manifest geçerli.' : `❌ Hatalar: <br>${res.errors.join('<br>')}`;
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}

let currentWizardStep = 1;

function showWizardStep(n) {
  currentWizardStep = n;
  document.querySelectorAll('.wizard-panel').forEach((p, i) => p.classList.toggle('visible', i === n - 1));
  document.querySelectorAll('.wizard-step-indicator').forEach((s, i) => s.classList.toggle('active', i === n - 1));
  $('prevStep').classList.toggle('hidden', n === 1);
  $('nextStep').classList.toggle('hidden', n === 3);
  $('finishWizard').classList.toggle('hidden', n !== 3);
  if (n === 3) {
    $('wizardSummary').innerHTML = `
      <div class="item"><strong>Proje:</strong> ${$('iwName').value}</div>
      <div class="item"><strong>Başlık:</strong> ${$('iwTitle').value}</div>
      <div class="item"><strong>Yazar:</strong> ${$('iwAuthor').value}</div>
      <div class="item"><strong>Dil:</strong> ${$('iwLang').value}</div>
    `;
  }
}

async function finishWizard() {
  try {
    const data = {
      name: $('iwName').value,
      title: $('iwTitle').value,
      author: $('iwAuthor').value,
      lang: $('iwLang').value,
      options: { docx: $('iwOutDocx').checked, pdf: $('iwOutPdf').checked }
    };
    const res = await api('/api/project/init', { method: 'POST', body: JSON.stringify({ root: $('projectRoot').value, manifest: data }) });
    setStatus('Proje oluşturuldu: ' + res.path, 'good');
    $('initWizardModal').classList.add('hidden');
    await loadProject();
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}

async function uploadFiles(files) {
  const formData = new FormData();
  for (let f of files) formData.append('files', f);
  try {
    setStatus('Yükleniyor...', 'warn');
    await fetch('/api/assets/upload?root=' + encodeURIComponent($('projectRoot').value), { method: 'POST', body: formData });
    setStatus('Yüklendi.', 'good');
    await refreshMedia();
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}

function initDropZone() {
  const dz = $('dropZone'); if (!dz) return;
  dz.onclick = () => $('mediaUploadInput').click();
  dz.ondragover = (e) => { e.preventDefault(); dz.classList.add('dragover'); };
  dz.ondragleave = () => dz.classList.remove('dragover');
  dz.ondrop = (e) => { e.preventDefault(); dz.classList.remove('dragover'); uploadFiles(e.dataTransfer.files); };
  $('mediaUploadInput').onchange = (e) => uploadFiles(e.target.files);
}

async function loadConfig() {
  try {
    const cfg = await api('/api/studio/config');
    $('frameworkRoot').textContent = cfg.framework_root;
    if (cfg.active_book) $('projectRoot').value = cfg.active_book;
    $('recentBooksSelect').innerHTML = '<option value="">Son kitaplar...</option>' + cfg.recent_books.map(b => `<option value="${b}">${b.split(/[\\/]/).pop()} (${b})</option>`).join('');
  } catch (e) { console.error(e); }
}

// Global Init & Event Listeners
function initApp() {
  loadConfig();
  initDropZone();
  
  // 1. Sidebar Tabs (High Priority)
  document.querySelectorAll('.tab').forEach(b => {
    b.addEventListener('click', () => showTab(b.dataset.tab));
  });
  document.querySelectorAll('.manifest-tab').forEach(b => {
    b.addEventListener('click', () => showManifestTab(b.dataset.mtab));
  });

  // 2. Keyboard Shortcuts
  window.addEventListener('keydown', (e) => {
    if (e.altKey && e.key >= '1' && e.key <= '9') {
      const tabs = ['dashboard', 'control', 'wizard', 'manifest', 'chapters', 'production', 'reports', 'cloud', 'media'];
      const target = tabs[parseInt(e.key) - 1];
      if (target) showTab(target);
    }
  });

  // 3. Project Loading
  const loadBtn = $('loadProject');
  if (loadBtn) loadBtn.addEventListener('click', loadProject);
  
  const recentSelect = $('recentBooksSelect');
  if (recentSelect) {
    recentSelect.addEventListener('change', (e) => {
      if (e.target.value) {
        $('projectRoot').value = e.target.value;
        loadProject();
      }
    });
  }

  // 4. Wizard & Manifest
  const bind = (id, fn, event = 'click') => { const el = $(id); if (el) el.addEventListener(event, fn); };
  
  bind('toggleDarkMode', () => { localStorage.setItem('darkMode', document.body.classList.toggle('dark-mode')); });
  bind('chapterContent', updateMarkdownPreview, 'input');
  bind('addGlossaryTerm', addGlossaryRow);
  bind('addResource', addResourceRow);
  bind('addChapter', addChapterRow);
  bind('renumberChapters', renumberChapters);
  bind('matchChapterFiles', matchChapterFiles);
  bind('saveManifestForm', saveManifestForm);
  bind('validateManifest', validateManifest);
  bind('initProject', initProject);
  bind('openInitWizard', () => { currentWizardStep = 1; showWizardStep(1); $('initWizardModal').classList.remove('hidden'); });
  bind('emptyOpenWizard', () => { currentWizardStep = 1; showWizardStep(1); $('initWizardModal').classList.remove('hidden'); });
  bind('closeInitWizard', () => $('initWizardModal').classList.add('hidden'));
  bind('prevStep', () => showWizardStep(currentWizardStep - 1));
  bind('nextStep', () => showWizardStep(currentWizardStep + 1));
  bind('finishWizard', finishWizard);
  
  bind('emptySelectFolder', () => $('projectRoot').focus());
  bind('makeArchitecturePrompt', makeArchitecturePrompt);
  bind('copyArchitecturePrompt', () => {
    const val = $('architecturePrompt').value;
    if (val) {
      navigator.clipboard.writeText(val);
      showToast('Prompt kopyalandı.');
    }
  });
  
  // 5. Cloud & Media
  bind('refreshCloudStatus', refreshCloudStatus);
  bind('provisionCloud', provisionCloud);
  bind('closeDebug', () => $('debugModal').classList.add('hidden'));
  bind('saveAndTestCode', saveAndTestCode);
  
  // 6. Chapter & Metadata
  bind('insertMetaBlock', () => {
    const id = $('mwId').value.trim() || 'code_01', lang = $('mwLang').value, file = $('mwFile').value.trim(), test = $('mwTest').value;
    const shot = $('mwScreenshot').checked ? `\ncaptures_screenshot: "${$('mwScreenshotId').value.trim() || id}"` : '';
    const sandbox = $('mwSandbox').checked ? `\nsandbox_link: true` : '';
    const group = $('mwGroupId').value.trim() ? `\ngroup_id: "${$('mwGroupId').value.trim()}"` : '';
    const compare = $('mwCompare').value.trim() ? `\ncompare_with: "${$('mwCompare').value.trim()}"` : '';
    const block = `\n<!-- CODE_META\nid: ${id}\nchapter_id: ${$('importChapterId').value || 'chapter_XX'}\nlanguage: ${lang}\nfile: ${file}\ntest: ${test}${shot}${sandbox}${group}${compare}\n-->\n\n\`\`\`${lang}\n\n\`\`\`\n`;
    $('chapterContent').value += block; $('metaWizardModal').classList.add('hidden'); updateMarkdownPreview();
  });
  bind('closeMetaWizard', () => $('metaWizardModal').classList.add('hidden'));
  bind('mwScreenshot', (e) => $('mwScreenshotIdBox').classList.toggle('hidden', !e.target.checked), 'change');
  bind('useRagToggle', (e) => $('ragQueryContainer').classList.toggle('hidden', !e.target.checked), 'change');
  
  // 7. Production & Reports
  bind('runStep', () => { api('/api/jobs', { method: 'POST', body: JSON.stringify({ root: $('projectRoot').value, step: $('pipelineStep').value, options: JSON.parse($('jobOptions').value || '{}') }) }).then(j => pollJob(j.id)); });
  bind('runFull', () => { api('/api/jobs', { method: 'POST', body: JSON.stringify({ root: $('projectRoot').value, step: 'full_production', options: {}}) }).then(j => pollJob(j.id)); });
  bind('runWebSite', () => { api('/api/jobs', { method: 'POST', body: JSON.stringify({root: $('projectRoot').value, step: 'generate-web-site', options: {}}) }).then(j => pollJob(j.id)); });
  bind('importChapter', saveChapter);
  bind('refreshChapters', renderChapters);
  bind('generatePrompts', generateChapterPrompts);
  bind('refreshControlPanel', refreshControlPanel);
  bind('refreshReports', refreshReports);
  bind('saveManifestYaml', saveManifestYaml);
  bind('refreshManifest', () => refreshManifest(true));

  // 8. Initial States
  if (localStorage.getItem('darkMode') === 'true') document.body.classList.add('dark-mode');
  if (location.hash) showTab(location.hash.substring(1));
  
  loadProject();
  loadPipelineSteps();
}

// Start
initApp();
