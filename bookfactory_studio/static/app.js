/**
 * BookFactory Studio Frontend Orchestrator v3.7
 * User Experience & Authoring Excellence
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
    setStatus('Kitap projesi yükleniyor...');
    const r = $('projectRoot').value.trim() || '.';
    project = await api('/api/project?root=' + encodeURIComponent(r));
    $('emptyState').classList.add('hidden');
    document.querySelectorAll('.panel:not(#emptyState)').forEach(p => p.classList.remove('hidden'));
    controlPanel = await api('/api/control-panel?root=' + encodeURIComponent(r));
    manifestData = structuredClone(project.manifest || {});
    renderDashboard();
    renderControlPanel();
    renderManifestForm();
    await loadPipelineSteps();
    await refreshManifest(false);
    setStatus('Kitap projesi yüklendi: ' + project.root, 'good');
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

function updateMarkdownPreview() {
  if (window.marked) $('markdownPreview').innerHTML = marked.parse($('chapterContent').value);
}

let progressChart = null;
function renderCharts(matrix) {
  const counts = { final: 0, total: matrix.length || 1 };
  const heatmap = $('healthHeatmap');
  heatmap.innerHTML = '';
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
  const matrix = controlPanel?.chapter_matrix || [];
  if (matrix.length) renderCharts(matrix);
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
  renderGlossaryRows(); renderManifestChapterRows();
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

function renderGlossaryRows() {
  const terms = get(manifestData, 'glossary', []);
  const tbody = $('manifestGlossaryRows'); if (!tbody) return;
  tbody.innerHTML = terms.map((t, idx) => `<tr><td><input class="g-term" value="${escapeHtml(t.term)}" /></td><td><input class="g-def" value="${escapeHtml(t.definition)}" /></td><td><button class="smallbtn danger" onclick="removeGlossaryRow(${idx})">Sil</button></td></tr>`).join('');
}

function addGlossaryRow() { if (!manifestData.glossary) manifestData.glossary = []; manifestData.glossary.push({term: 'Yeni', definition: ''}); renderGlossaryRows(); }
function removeGlossaryRow(idx) { manifestData.glossary.splice(idx, 1); renderGlossaryRows(); }
function removeChapterRow(idx) { manifestData.structure.chapters.splice(idx, 1); renderManifestChapterRows(); }

async function saveManifestForm() {
  const m = structuredClone(manifestData);
  m.book.title = $('mBookTitle').value; m.book.author = $('mBookAuthor').value;
  m.academic = m.academic || {}; m.academic.course_code = $('mCourseCode').value; m.academic.course_name = $('mCourseName').value;
  m.language.style_profile = $('mStyleProfile').value; m.language.pedagogical_model = $('mPedagogicalModel').value;
  await api('/api/manifest/save', { method: 'POST', body: JSON.stringify({ root: $('projectRoot').value, manifest: m }) });
  setStatus('Kaydedildi.', 'good'); await loadProject();
}

async function refreshMedia() {
  const data = await api('/api/assets?root=' + encodeURIComponent($('projectRoot').value));
  $('mediaGrid').innerHTML = data.assets.map(a => `<div class="media-item"><div class="media-thumb"><img src="/api/project/file?path=${encodeURIComponent(a.rel_path)}&root=${encodeURIComponent($('projectRoot').value)}"></div><div class="media-info"><div class="media-name">${escapeHtml(a.name)}</div><button class="smallbtn" onclick="copyMarkdownLink('${a.rel_path}', '${a.name}')">Link</button></div></div>`).join('');
}

async function copyMarkdownLink(path, name) {
  await navigator.clipboard.writeText(`![${name.split('.')[0]}](../${path})`);
  showToast('Link kopyalandı.');
}

// Global Init
$('loadProject').addEventListener('click', loadProject);
$('toggleDarkMode').addEventListener('click', () => { localStorage.setItem('darkMode', document.body.classList.toggle('dark-mode')); });
if (localStorage.getItem('darkMode') === 'true') document.body.classList.add('dark-mode');
$('chapterContent').addEventListener('input', updateMarkdownPreview);
$('addGlossaryTerm').addEventListener('click', addGlossaryRow);
$('saveManifestForm').addEventListener('click', saveManifestForm);
$('closeDebug').addEventListener('click', () => $('debugModal').classList.add('hidden'));
$('saveAndTestCode').addEventListener('click', saveAndTestCode);
$('runStep').addEventListener('click', () => { api('/api/jobs', { method: 'POST', body: JSON.stringify({ root: $('projectRoot').value, step: $('pipelineStep').value, options: JSON.parse($('jobOptions').value || '{}') }) }).then(j => pollJob(j.id)); });
$('runWebSite').addEventListener('click', () => { api('/api/jobs', { method: 'POST', body: JSON.stringify({root: $('projectRoot').value, step: 'generate-web-site', options: {}}) }).then(j => pollJob(j.id)); });
window.addEventListener('keydown', (e) => { if (e.altKey && e.key >= '1' && e.key <= '8') showTab(['dashboard', 'control', 'wizard', 'manifest', 'chapters', 'production', 'reports', 'media'][parseInt(e.key)-1]); });
async function loadPipelineSteps() { const data = await api('/api/pipeline/steps'); $('pipelineStep').innerHTML = data.steps.map(s => `<option value="${s.id}">${s.title}</option>`).join(''); }

loadProject();
loadPipelineSteps();
