let project = null;
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
    try { detail = JSON.parse(detail).detail || detail; } catch {}
    throw new Error(detail);
  }
  return res.json();
}

function showTab(name) {
  document.querySelectorAll('.tab').forEach(b => b.classList.toggle('active', b.dataset.tab === name));
  document.querySelectorAll('.panel').forEach(p => p.classList.toggle('visible', p.id === name));
}

document.querySelectorAll('.tab').forEach(b => b.addEventListener('click', () => showTab(b.dataset.tab)));

async function loadProject() {
  try {
    setStatus('Proje yükleniyor...');
    project = await api('/api/project?root=' + encodeURIComponent(root()));
    renderDashboard();
    renderChapters();
    renderReports(project.reports || []);
    await loadPipelineSteps();
    await refreshManifest();
    setStatus('Proje yüklendi: ' + project.root, project.validation?.valid ? 'good' : 'warn');
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
  const counts = project?.chapter_status_counts || {};
  $('statusCounts').innerHTML = Object.keys(counts).length ? Object.entries(counts).map(([k,v]) => `<span class="pill">${k}: ${v}</span>`).join('') : '<span class="pill">Henüz bölüm yok</span>';
  $('pathInfo').innerHTML = `<div class="item"><strong>Kitap kökü:</strong><br><code>${project?.root || '-'}</code><br><small>Framework kökü: ${project?.framework_root || '-'}</small></div>` +
    (project?.is_framework_root ? '<div class="item warn">Seçilen yol BookFactory framework kökü gibi görünüyor. Lütfen doğrudan kitap klasörünü seçin.</div>' : '');
  const discovered = project?.discovered_book_roots || [];
  $('discoveredProjects').innerHTML = discovered.length ? discovered.map(d => `<button class="projectPick" data-root="${d.root}"><strong>${d.title || d.path}</strong><br><small>${d.root}<br>${d.chapters || 0} bölüm · manifest: ${d.manifest}</small></button>`).join('') : '<div class="item">Bu kök altında kitap çalışması bulunamadı.</div>';
  document.querySelectorAll('.projectPick').forEach(b => b.addEventListener('click', async () => { $('projectRoot').value = b.dataset.root; await loadProject(); }));
  const reports = (project?.reports || []).slice(-6).reverse();
  $('recentReports').innerHTML = reports.length ? reports.map(r => `<div class="item">${r.path}<br><small>${r.size} bayt</small></div>`).join('') : '<div class="item">Rapor yok.</div>';
}

async function refreshManifest() {
  try {
    const data = await api('/api/manifest?root=' + encodeURIComponent(root()));
    $('manifestYaml').value = data.yaml;
  } catch (e) {
    $('manifestYaml').value = '# Manifest bulunamadı veya okunamadı.\n# Kitap Sihirbazı veya mevcut YAML dosyasını kullanın.\n';
  }
}

async function saveManifest() {
  try {
    const yamlText = $('manifestYaml').value;
    const data = await api('/api/manifest/save-yaml', {method: 'POST', body: JSON.stringify({root: root(), yaml_text: yamlText})});
    project = await api('/api/project?root=' + encodeURIComponent(root()));
    renderDashboard();
    renderChapters();
    setStatus('Manifest kaydedildi: ' + data.path, data.validation?.valid ? 'good' : 'warn');
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
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
    scope: {stack: $('wStack').value.split('\n').map(x => x.trim()).filter(Boolean), out_of_scope: $('wOutScope').value.split('\n').map(x => x.trim()).filter(Boolean)}
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
  if (!project?.manifest) { setStatus('Önce mevcut manifest içeren bir proje açın veya book_manifest.yaml ekleyin.', 'warn'); return; }
  try {
    const data = await api('/api/project/init', {method: 'POST', body: JSON.stringify({root: root(), manifest: project.manifest})});
    project = data;
    renderDashboard(); renderChapters(); await refreshManifest();
    setStatus('Klasör yapısı oluşturuldu ve manifest yazıldı.', 'good');
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}

function renderChapters() {
  const tbody = document.querySelector('#chapterTable tbody');
  const rows = project?.chapters || [];
  tbody.innerHTML = rows.map(r => `<tr>
    <td>${r.order}</td><td><code>${r.id}</code></td><td>${r.title}</td><td>${r.status}</td>
    <td>${r.prompt_exists ? '✅' : '—'}<br><small>${r.prompt_path}</small></td>
    <td>${r.chapter_exists ? '✅' : '—'}<br><small>${r.chapter_path}</small></td>
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
  $('pipelineStep').innerHTML = data.steps.map(s => `<option value="${s.id}">${s.group} — ${s.title}</option>`).join('');
}

async function importChapter() {
  try {
    const data = await api('/api/chapters/import', {method: 'POST', body: JSON.stringify({root: root(), chapter_id: $('importChapterId').value, content: $('chapterContent').value})});
    setStatus('Bölüm Markdown kaydedildi: ' + data.path, 'good');
    await loadProject();
  } catch (e) { setStatus('Hata: ' + e.message, 'bad'); }
}

function renderReports(reports) {
  $('reportList').innerHTML = reports.length ? reports.map(r => `<button data-path="${r.path}">${r.path}<br><small>${r.size} bayt · ${r.modified || ''}</small></button>`).join('') : '<div class="item">Rapor yok.</div>';
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
$('refreshManifest').addEventListener('click', refreshManifest);
$('saveManifest').addEventListener('click', saveManifest);
$('initProject').addEventListener('click', initProject);
$('makeArchitecturePrompt').addEventListener('click', makeArchitecturePrompt);
$('copyArchitecturePrompt').addEventListener('click', copyArchitecturePrompt);
$('generatePrompts').addEventListener('click', () => startJob('generate_chapter_prompts'));
$('refreshChapters').addEventListener('click', loadProject);
$('importChapter').addEventListener('click', importChapter);
$('runStep').addEventListener('click', () => startJob($('pipelineStep').value));
$('runFull').addEventListener('click', () => startJob('full_production'));
$('refreshReports').addEventListener('click', refreshReports);

loadProject();
