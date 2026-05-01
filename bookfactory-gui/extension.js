const vscode = require('vscode');
const path   = require('path');
const cp     = require('child_process');
const fs     = require('fs');

let panel = null;

function activate(context) {
  context.subscriptions.push(
    vscode.commands.registerCommand('bookfactory.openPanel', () => openPanel(context))
  );
}

function deactivate() {}

// ─── Panel ────────────────────────────────────────────────────────────────────

function openPanel(context) {
  if (panel) { panel.reveal(); return; }

  panel = vscode.window.createWebviewPanel(
    'bookfactoryGui',
    'BookFactory',
    vscode.ViewColumn.One,
    {
      enableScripts: true,
      retainContextWhenHidden: true,
      localResourceRoots: [vscode.Uri.joinPath(context.extensionUri, 'media')]
    }
  );

  panel.webview.html = getWebviewHtml(context, panel.webview);

  panel.onDidDispose(() => { panel = null; });

  panel.webview.onDidReceiveMessage(msg => handleMessage(msg, context), null, context.subscriptions);

  sendConfig();
}

// ─── Mesaj yönlendirici ───────────────────────────────────────────────────────

function handleMessage(msg, context) {
  switch (msg.type) {

    case 'getConfig':
      sendConfig();
      break;

    case 'saveConfig':
      saveConfig(msg.frameworkPath, msg.bookProjectPath, msg.pythonPath);
      break;

    case 'browseFolder':
      browseFolder(msg.key);
      break;

    case 'readManifest':
      readManifest();
      break;

    case 'readChapters':
      readChapters();
      break;

    case 'runInTerminal':
      runInTerminal(msg.label, msg.command);
      break;

    case 'runQuiet':
      runQuiet(msg.id, msg.command);
      break;

    case 'openFile':
      openFile(msg.filePath);
      break;
  }
}

// ─── Yapılandırma ─────────────────────────────────────────────────────────────

function getConfig() {
  const cfg = vscode.workspace.getConfiguration('bookfactory');
  return {
    frameworkPath:   cfg.get('frameworkPath')   || '',
    bookProjectPath: cfg.get('bookProjectPath') || '',
    pythonPath:      cfg.get('pythonPath')      || 'python',
  };
}

function sendConfig() {
  if (!panel) return;
  const cfg = getConfig();
  panel.webview.postMessage({ type: 'config', ...cfg });
}

function saveConfig(frameworkPath, bookProjectPath, pythonPath) {
  const cfg = vscode.workspace.getConfiguration('bookfactory');
  cfg.update('frameworkPath',   frameworkPath,   vscode.ConfigurationTarget.Global);
  cfg.update('bookProjectPath', bookProjectPath, vscode.ConfigurationTarget.Global);
  cfg.update('pythonPath',      pythonPath,      vscode.ConfigurationTarget.Global);
  vscode.window.showInformationMessage('BookFactory yapılandırması kaydedildi.');
  sendConfig();
}

async function browseFolder(key) {
  const uris = await vscode.window.showOpenDialog({
    canSelectFolders: true, canSelectFiles: false, canSelectMany: false,
    openLabel: 'Klasörü Seç'
  });
  if (!uris || !uris[0]) return;
  const selected = uris[0].fsPath;
  const cfg = vscode.workspace.getConfiguration('bookfactory');

  if (key === 'frameworkPath') {
    cfg.update('frameworkPath', selected, vscode.ConfigurationTarget.Global);
  } else if (key === 'bookProjectPath') {
    cfg.update('bookProjectPath', selected, vscode.ConfigurationTarget.Global);
  }
  setTimeout(sendConfig, 200);
}

// ─── Manifest okuma ───────────────────────────────────────────────────────────

function readManifest() {
  const { bookProjectPath } = getConfig();
  if (!bookProjectPath) {
    send({ type: 'manifest', error: 'Kitap projesi klasörü ayarlanmamış.' }); return;
  }
  const manifestPath = path.join(bookProjectPath, 'manifests', 'book_manifest.yaml');
  if (!fs.existsSync(manifestPath)) {
    send({ type: 'manifest', error: `Manifest bulunamadı: ${manifestPath}` }); return;
  }
  const raw = fs.readFileSync(manifestPath, 'utf8');
  send({ type: 'manifest', raw });
}

function readChapters() {
  const { bookProjectPath } = getConfig();
  if (!bookProjectPath) { send({ type: 'chapters', chapters: [] }); return; }
  const chaptersDir = path.join(bookProjectPath, 'chapters');
  if (!fs.existsSync(chaptersDir)) { send({ type: 'chapters', chapters: [] }); return; }
  const files = fs.readdirSync(chaptersDir)
    .filter(f => f.endsWith('.md') && !f.startsWith('.'))
    .sort()
    .map(f => {
      const stat = fs.statSync(path.join(chaptersDir, f));
      return { name: f, size: stat.size, mtime: stat.mtime.toISOString() };
    });
  send({ type: 'chapters', chapters: files });
}

// ─── Komut çalıştırma ─────────────────────────────────────────────────────────

function buildEnv() {
  const { frameworkPath } = getConfig();
  const env = { ...process.env };
  if (frameworkPath) {
    const existing = env.PYTHONPATH || '';
    env.PYTHONPATH = existing ? `${frameworkPath};${existing}` : frameworkPath;
    env.PYTHONUTF8 = '1';
  }
  return env;
}

function runInTerminal(label, command) {
  const { bookProjectPath } = getConfig();
  const cwd = bookProjectPath || vscode.workspace.rootPath || process.cwd();

  let term = vscode.window.terminals.find(t => t.name === 'BookFactory');
  if (!term) term = vscode.window.createTerminal({ name: 'BookFactory', cwd });
  term.show();

  const { frameworkPath } = getConfig();
  if (frameworkPath) {
    term.sendText(`$env:PYTHONPATH = "${frameworkPath}"; $env:PYTHONUTF8 = "1"`);
  }
  term.sendText(`cd "${cwd}"`);
  term.sendText(command);
  send({ type: 'terminalStarted', label });
}

function runQuiet(id, command) {
  const { bookProjectPath, pythonPath } = getConfig();
  const cwd = bookProjectPath || vscode.workspace.rootPath || process.cwd();
  const fullCmd = command.replace(/^python\b/, pythonPath);

  cp.exec(fullCmd, { cwd, env: buildEnv(), encoding: 'utf8' }, (err, stdout, stderr) => {
    send({
      type: 'quietResult',
      id,
      stdout: stdout || '',
      stderr: stderr || '',
      exitCode: err ? (err.code || 1) : 0,
    });
  });
}

function openFile(filePath) {
  const uri = vscode.Uri.file(filePath);
  vscode.window.showTextDocument(uri);
}

function send(msg) {
  if (panel) panel.webview.postMessage(msg);
}

// ─── Webview HTML ─────────────────────────────────────────────────────────────

function getWebviewHtml(context, webview) {
  return `<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline';">
<title>BookFactory</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--vscode-font-family);font-size:13px;color:var(--vscode-foreground);background:var(--vscode-editor-background);display:flex;height:100vh;overflow:hidden}

/* Sidebar */
#sidebar{width:180px;flex-shrink:0;background:var(--vscode-sideBar-background);border-right:1px solid var(--vscode-panel-border);display:flex;flex-direction:column;overflow-y:auto}
#sidebar h2{font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--vscode-sideBarSectionHeader-foreground);padding:16px 12px 8px;border-bottom:1px solid var(--vscode-panel-border)}
.nav-item{padding:8px 14px;cursor:pointer;border-left:3px solid transparent;font-size:13px;color:var(--vscode-sideBar-foreground);transition:background .1s}
.nav-item:hover{background:var(--vscode-list-hoverBackground)}
.nav-item.active{border-left-color:var(--vscode-focusBorder);background:var(--vscode-list-activeSelectionBackground);color:var(--vscode-list-activeSelectionForeground)}
.nav-sep{height:1px;background:var(--vscode-panel-border);margin:6px 0}

/* Main */
#main{flex:1;display:flex;flex-direction:column;overflow:hidden}
#toolbar{padding:8px 16px;border-bottom:1px solid var(--vscode-panel-border);display:flex;align-items:center;gap:8px;background:var(--vscode-editor-background)}
#toolbar span{font-size:12px;color:var(--vscode-descriptionForeground)}
.tab-panel{display:none;flex:1;overflow-y:auto;padding:16px}
.tab-panel.active{display:block}

/* Log */
#log-wrap{height:160px;flex-shrink:0;border-top:1px solid var(--vscode-panel-border)}
#log-bar{padding:4px 12px;font-size:11px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--vscode-descriptionForeground);background:var(--vscode-editor-background);display:flex;justify-content:space-between;align-items:center;cursor:pointer;border-bottom:1px solid var(--vscode-panel-border)}
#log{height:130px;overflow-y:auto;padding:6px 12px;font-family:var(--vscode-editor-font-family,'monospace');font-size:12px;line-height:1.5;background:var(--vscode-terminal-background,#1e1e1e);color:var(--vscode-terminal-foreground,#ccc)}
.log-ok{color:#4ec9b0}.log-err{color:#f44}.log-info{color:#569cd6}.log-warn{color:#ce9178}

/* Form */
label{display:block;font-size:12px;color:var(--vscode-descriptionForeground);margin-bottom:4px;margin-top:12px}
input[type=text]{width:100%;padding:5px 8px;background:var(--vscode-input-background);color:var(--vscode-input-foreground);border:1px solid var(--vscode-input-border);border-radius:2px;font-size:13px;outline:none}
input[type=text]:focus{border-color:var(--vscode-focusBorder)}
.row{display:flex;gap:6px;align-items:flex-end}
.row input{flex:1}

/* Buttons */
button{padding:5px 12px;background:var(--vscode-button-background);color:var(--vscode-button-foreground);border:none;border-radius:2px;cursor:pointer;font-size:12px}
button:hover{background:var(--vscode-button-hoverBackground)}
button.sec{background:var(--vscode-button-secondaryBackground);color:var(--vscode-button-secondaryForeground)}
button.sec:hover{background:var(--vscode-button-secondaryHoverBackground)}
button.danger{background:#a1260d;color:#fff}

/* Cards */
.card{background:var(--vscode-editor-inactiveSelectionBackground);border:1px solid var(--vscode-panel-border);border-radius:4px;padding:12px;margin-bottom:10px}
.card h3{font-size:13px;font-weight:600;margin-bottom:8px}
.card-desc{font-size:12px;color:var(--vscode-descriptionForeground);margin-bottom:10px;line-height:1.5}
.badge{display:inline-block;font-size:11px;padding:2px 7px;border-radius:10px;margin-left:6px}
.badge-ok{background:#0e7a0d22;color:#4ec9b0}
.badge-warn{background:#ce917822;color:#ce9178}
.badge-err{background:#f4444422;color:#f44}

/* Chapter list */
table{width:100%;border-collapse:collapse;font-size:12px}
th{text-align:left;padding:6px 8px;border-bottom:1px solid var(--vscode-panel-border);color:var(--vscode-descriptionForeground);font-weight:600}
td{padding:5px 8px;border-bottom:1px solid var(--vscode-panel-border)}
tr:hover td{background:var(--vscode-list-hoverBackground)}
.status-done{color:#4ec9b0}.status-progress{color:#dcdcaa}.status-planned{color:#858585}

/* Progress */
.progress-bar{height:6px;background:var(--vscode-panel-border);border-radius:3px;margin:6px 0}
.progress-fill{height:100%;border-radius:3px;background:var(--vscode-progressBar-background)}

/* Grid */
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:10px}
@media(max-width:600px){.grid-2{grid-template-columns:1fr}}
</style>
</head>
<body>

<div id="sidebar">
  <h2>BookFactory</h2>
  <div class="nav-item active" onclick="showTab('proje')">Proje</div>
  <div class="nav-item" onclick="showTab('bolumler')">Bölümler</div>
  <div class="nav-sep"></div>
  <div class="nav-item" onclick="showTab('kod')">Kod Testi</div>
  <div class="nav-item" onclick="showTab('uretim')">Mermaid / QR</div>
  <div class="nav-item" onclick="showTab('postprod')">Post-production</div>
  <div class="nav-item" onclick="showTab('export')">Export</div>
  <div class="nav-sep"></div>
  <div class="nav-item" onclick="showTab('ayarlar')">Ayarlar</div>
</div>

<div id="main">
  <div id="toolbar">
    <span id="toolbar-project">Proje seçilmedi</span>
  </div>

  <!-- TAB: Proje -->
  <div class="tab-panel active" id="tab-proje">
    <div id="proje-alert" class="card" style="border-color:#ce9178;display:none">
      <p style="color:#ce9178">Yapılandırma eksik. <a href="#" onclick="showTab('ayarlar')">Ayarlar</a> sekmesinden framework ve kitap yollarını girin.</p>
    </div>
    <div class="grid-2">
      <div class="card">
        <h3>Kitap bilgileri</h3>
        <div id="book-info" class="card-desc">Manifest okunuyor...</div>
      </div>
      <div class="card">
        <h3>Bölüm durumu</h3>
        <div id="chapter-summary">Yükleniyor...</div>
      </div>
    </div>
    <div class="card">
      <h3>Hızlı işlemler</h3>
      <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:8px">
        <button onclick="runTerminal('Ortam Kontrolü', 'python -m bookfactory doctor --soft')">Ortam kontrolü</button>
        <button onclick="runTerminal('Manifest Doğrulama', buildValidateCmd())" class="sec">Manifest doğrula</button>
        <button onclick="runTerminal('Paket Bütünlük', 'python tools/check_package_integrity.py .')" class="sec">Paket bütünlüğü</button>
      </div>
    </div>
  </div>

  <!-- TAB: Bölümler -->
  <div class="tab-panel" id="tab-bolumler">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
      <div style="font-size:13px;font-weight:600">Bölümler</div>
      <button onclick="loadChapters()">Yenile</button>
    </div>
    <table>
      <thead><tr><th>Dosya</th><th>Boyut</th><th>Son güncelleme</th><th></th></tr></thead>
      <tbody id="chapter-list"><tr><td colspan="4" style="color:var(--vscode-descriptionForeground)">Yükleniyor...</td></tr></tbody>
    </table>
    <div class="card" style="margin-top:12px">
      <h3>Yeni bölüm oluştur</h3>
      <div class="card-desc">Bölüm numarası ve slug girerek boş bölüm dosyası oluşturur.</div>
      <div class="row" style="margin-top:8px">
        <input type="text" id="new-ch-num" placeholder="01" style="width:60px">
        <input type="text" id="new-ch-slug" placeholder="giris_ve_kurulum">
        <button onclick="createChapter()">Oluştur</button>
      </div>
    </div>
  </div>

  <!-- TAB: Kod Testi -->
  <div class="tab-panel" id="tab-kod">
    <div class="card">
      <h3>Kod bloğu çıkarma ve test</h3>
      <div class="card-desc">chapters/ klasöründeki CODE_META bloklarını çıkarır, doğrular ve test eder.</div>
      <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:8px">
        <button onclick="runTerminal('Kod Çıkarma', buildExtractCmd())">1. Çıkar</button>
        <button onclick="runTerminal('Kod Doğrulama', buildValidateCodeCmd())" class="sec">2. Doğrula</button>
        <button onclick="runTerminal('Kod Testi', buildTestCmd())">3. Test et</button>
        <button onclick="runTerminal('Tam Zincir', buildFullChainCmd())" style="background:#0e639c">Tam zincir (1+2+3)</button>
      </div>
    </div>
    <div class="card">
      <h3>Markdown kalite kontrolü</h3>
      <div class="card-desc">Bölüm başlık yapısı, CODE_META yerleşimi, screenshot marker kontrolü.</div>
      <div class="row" style="margin-top:8px">
        <input type="text" id="quality-chapter" placeholder="chapters/chapter_01_giris.md">
        <button onclick="runTerminal('Kalite Kontrol', buildQualityCmd())">Kontrol et</button>
      </div>
    </div>
    <div class="card">
      <h3>Manifest doğrulama (JSON Schema)</h3>
      <div style="margin-top:8px">
        <button onclick="runQuiet('validate', buildValidateCmd())">Doğrula</button>
        <span id="validate-result" style="margin-left:10px;font-size:12px"></span>
      </div>
    </div>
  </div>

  <!-- TAB: Mermaid / QR -->
  <div class="tab-panel" id="tab-uretim">
    <div class="card">
      <h3>Mermaid diyagram → PNG</h3>
      <div class="card-desc">chapters/ içindeki Mermaid bloklarını çıkarır ve PNG görsellerine dönüştürür.</div>
      <div style="display:flex;gap:8px;margin-top:8px">
        <button onclick="runTerminal('Mermaid Çıkar', buildMermaidExtractCmd())">Mermaid çıkar</button>
        <button onclick="runTerminal('PNG Üret', buildMermaidRenderCmd())" class="sec">PNG üret (mmdc)</button>
      </div>
    </div>
    <div class="card">
      <h3>QR kod üretimi</h3>
      <div class="card-desc">CODE_META bloklarından QR manifest üretir ve QR görsellerini oluşturur.</div>
      <div style="display:flex;gap:8px;margin-top:8px">
        <button onclick="runTerminal('QR Manifest', buildQrManifestCmd())">QR manifest üret</button>
        <button onclick="runTerminal('QR Üret', buildQrCmd())" class="sec">QR görselleri üret</button>
      </div>
    </div>
    <div class="card">
      <h3>GitHub sync</h3>
      <div class="card-desc">Test geçen kod dosyalarını GitHub'a senkronize eder. <strong>push</strong> için ayrı onay gerekir.</div>
      <div style="display:flex;gap:8px;margin-top:8px">
        <button onclick="runTerminal('GitHub Sync (dry)', buildGithubSyncCmd(false))">Dry-run</button>
        <button onclick="confirmGithubPush()" class="danger">Push (onaylı)</button>
      </div>
    </div>
  </div>

  <!-- TAB: Post-production -->
  <div class="tab-panel" id="tab-postprod">
    <div class="card">
      <h3>Post-production pipeline</h3>
      <div class="card-desc">Bölümleri birleştirir, Mermaid/PNG üretir, DOCX ve diğer çıktıları hazırlar.</div>
      <label>Post-production profil dosyası</label>
      <div class="row">
        <input type="text" id="pp-profile" value="configs/post_production_profile.yaml">
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:10px">
        <button onclick="runStage('merge_chapters')">Bölümleri birleştir</button>
        <button onclick="runStage('extract_mermaid')" class="sec">Mermaid çıkar</button>
        <button onclick="runStage('render_mermaid')" class="sec">PNG üret</button>
        <button onclick="runStage('build_docx')" class="sec">DOCX üret</button>
        <button onclick="runStage('all')" style="background:#0e639c">Tümünü çalıştır</button>
      </div>
    </div>
    <div class="card">
      <h3>Terim dizini ve dashboard</h3>
      <div style="display:flex;gap:8px;margin-top:8px">
        <button onclick="runTerminal('Terim Dizini', buildIndexCmd())">Dizin üret</button>
        <button onclick="runTerminal('Dashboard', 'python -m bookfactory dashboard --check')" class="sec">Dashboard kontrol</button>
      </div>
    </div>
  </div>

  <!-- TAB: Export -->
  <div class="tab-panel" id="tab-export">
    <div class="card">
      <h3>Çıktı formatları</h3>
      <div class="card-desc">Post-production profilinden çıktı üretir. Önce post-production aşamasını tamamlayın.</div>
      <label>Post-production profil</label>
      <input type="text" id="export-profile" value="configs/post_production_profile.yaml">
      <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:10px">
        <button onclick="runExport('docx')">DOCX</button>
        <button onclick="runExport('html')" class="sec">HTML</button>
        <button onclick="runExport('epub')" class="sec">EPUB</button>
        <button onclick="runExport('pdf')" class="sec">PDF</button>
        <button onclick="runExport('all')" style="background:#0e639c">Tümü</button>
      </div>
    </div>
    <div class="card">
      <h3>dist/ klasörü</h3>
      <div id="dist-list" style="font-size:12px;color:var(--vscode-descriptionForeground)">Yükleniyor...</div>
    </div>
  </div>

  <!-- TAB: Ayarlar -->
  <div class="tab-panel" id="tab-ayarlar">
    <div class="card">
      <h3>Klasör yapılandırması</h3>
      <div class="card-desc">Repolar farklı konumlarda olduğu için her birini ayrıca seçin.</div>

      <label>BookFactory framework klasörü (bookfactory/ içeren dizin)</label>
      <div class="row">
        <input type="text" id="cfg-framework" placeholder="C:\Users\...\BookFactory">
        <button class="sec" onclick="browse('frameworkPath')">Gözat</button>
      </div>

      <label>Kitap projesi klasörü (.bookfactory dosyasının bulunduğu dizin)</label>
      <div class="row">
        <input type="text" id="cfg-book" placeholder="C:\Users\...\react-web">
        <button class="sec" onclick="browse('bookProjectPath')">Gözat</button>
      </div>

      <label>Python yolu</label>
      <input type="text" id="cfg-python" value="python" placeholder="python veya C:\\Python314\\python.exe">

      <div style="margin-top:14px;display:flex;gap:8px">
        <button onclick="saveConfig()">Kaydet</button>
        <button class="sec" onclick="vscodeApi.postMessage({type:'getConfig'})">Yenile</button>
      </div>
    </div>
  </div>

  <!-- Log -->
  <div id="log-wrap">
    <div id="log-bar" onclick="toggleLog()">
      <span>Terminal çıktısı</span>
      <span id="log-toggle">▼</span>
    </div>
    <div id="log"></div>
  </div>
</div>

<script>
const vscodeApi = acquireVsCodeApi();
let cfg = {};

// ─── Navigation ──────────────────────────────────────────────────────────────
function showTab(name) {
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  document.getElementById('tab-' + name).classList.add('active');
  const items = document.querySelectorAll('.nav-item');
  items.forEach(n => { if (n.textContent.trim().toLowerCase().startsWith(name.slice(0,3))) n.classList.add('active'); });
  if (name === 'bolumler') loadChapters();
  if (name === 'export') loadDist();
}

// ─── VS Code mesaj alıcısı ───────────────────────────────────────────────────
window.addEventListener('message', e => {
  const msg = e.data;
  switch (msg.type) {

    case 'config':
      cfg = msg;
      document.getElementById('cfg-framework').value = msg.frameworkPath || '';
      document.getElementById('cfg-book').value      = msg.bookProjectPath || '';
      document.getElementById('cfg-python').value    = msg.pythonPath || 'python';
      updateToolbar();
      vscodeApi.postMessage({ type: 'readManifest' });
      vscodeApi.postMessage({ type: 'readChapters' });
      break;

    case 'manifest':
      renderManifest(msg);
      break;

    case 'chapters':
      renderChapters(msg.chapters);
      break;

    case 'terminalStarted':
      logInfo('Terminal\'de başlatıldı: ' + msg.label);
      break;

    case 'quietResult':
      handleQuietResult(msg);
      break;
  }
});

// ─── Toolbar ─────────────────────────────────────────────────────────────────
function updateToolbar() {
  const el = document.getElementById('toolbar-project');
  if (cfg.bookProjectPath) {
    const parts = cfg.bookProjectPath.replace(/\\/g, '/').split('/');
    el.textContent = parts[parts.length - 1] || cfg.bookProjectPath;
  } else {
    el.textContent = 'Proje seçilmedi';
    document.getElementById('proje-alert').style.display = 'block';
  }
}

// ─── Manifest render ─────────────────────────────────────────────────────────
function renderManifest(msg) {
  const el = document.getElementById('book-info');
  if (msg.error) { el.textContent = msg.error; return; }
  const lines = msg.raw.split('\n');
  const get = (key) => {
    const line = lines.find(l => l.trim().startsWith(key + ':'));
    return line ? line.split(':').slice(1).join(':').trim().replace(/['"]/g,'') : '—';
  };
  el.innerHTML = [
    '<b>' + get('title') + '</b>',
    'Yazar: ' + get('author'),
    'Baskı: ' + get('edition') + ' (' + get('year') + ')',
    'Framework: ' + get('framework_version'),
  ].join('<br>');
}

// ─── Chapter render ───────────────────────────────────────────────────────────
function loadChapters() {
  vscodeApi.postMessage({ type: 'readChapters' });
}

function renderChapters(chapters) {
  const tbody = document.getElementById('chapter-list');
  const summary = document.getElementById('chapter-summary');

  if (!chapters.length) {
    tbody.innerHTML = '<tr><td colspan="4" style="color:var(--vscode-descriptionForeground)">chapters/ klasörü boş</td></tr>';
    summary.textContent = 'Bölüm bulunamadı.';
    return;
  }

  tbody.innerHTML = chapters.map(c => {
    const kb = (c.size / 1024).toFixed(1);
    const date = new Date(c.mtime).toLocaleDateString('tr-TR');
    return \`<tr>
      <td>\${c.name}</td>
      <td>\${kb} KB</td>
      <td>\${date}</td>
      <td><button class="sec" style="padding:2px 8px;font-size:11px" onclick="openChapter('\${c.name}')">Aç</button></td>
    </tr>\`;
  }).join('');

  const total = chapters.length;
  const totalKb = (chapters.reduce((s,c) => s + c.size, 0) / 1024).toFixed(0);
  summary.innerHTML = \`<b>\${total} bölüm</b> · \${totalKb} KB<br><div class="progress-bar"><div class="progress-fill" style="width:\${Math.min(total/16*100,100)}%"></div></div><span style="font-size:11px;color:var(--vscode-descriptionForeground)">\${total}/16 bölüm tamamlandı</span>\`;
}

function openChapter(name) {
  if (!cfg.bookProjectPath) return;
  const filePath = cfg.bookProjectPath.replace(/\\\\/g, '/') + '/chapters/' + name;
  vscodeApi.postMessage({ type: 'openFile', filePath });
}

function createChapter() {
  const num  = document.getElementById('new-ch-num').value.trim().padStart(2,'0');
  const slug = document.getElementById('new-ch-slug').value.trim().replace(/\s+/g,'_').toLowerCase();
  if (!num || !slug) { logWarn('Numara ve slug zorunlu.'); return; }
  if (!cfg.bookProjectPath) { logErr('Kitap projesi klasörü ayarlanmamış.'); return; }
  const filename = \`chapter_\${num}_\${slug}.md\`;
  const cmd = \`python -c "from pathlib import Path; p=Path('chapters/\${filename}'); p.write_text('# Bölüm \${num}\\\\n\\\\nİçerik buraya gelecek.', encoding='utf-8'); print('Oluşturuldu:', p)"\`;
  runTerminal('Bölüm Oluştur', cmd);
}

// ─── Komut oluşturucular ──────────────────────────────────────────────────────
function fw() { return cfg.frameworkPath || '..\\\\bookFactory'; }
function py() { return cfg.pythonPath || 'python'; }

function buildExtractCmd() {
  return \`\${py()} -m tools.code.extract_code_blocks --package-root . --out-dir ./build/code --manifest ./build/code_manifest.json --yaml-manifest ./build/code_manifest.yaml --chapters-dir ./chapters\`;
}
function buildValidateCodeCmd() {
  return \`\${py()} -m tools.code.validate_code_meta ./build/code_manifest.json --package-root .\`;
}
function buildTestCmd() {
  return \`\${py()} -m tools.code.run_code_tests --manifest ./build/code_manifest.json --package-root . --report-json ./build/test_reports/code_test_report.json --report-md ./build/test_reports/code_test_report.md --node node --fail-on-error\`;
}
function buildFullChainCmd() {
  return buildExtractCmd() + ' && ' + buildValidateCodeCmd() + ' && ' + buildTestCmd();
}
function buildQualityCmd() {
  const ch = document.getElementById('quality-chapter').value.trim() || 'chapters/chapter_01.md';
  const id = ch.replace(/.*chapter_(\d+).*/,'chapter_$1');
  const no = ch.replace(/.*chapter_(\d+).*/,'$1');
  return \`\${py()} -m tools.quality.check_chapter_markdown --chapter ./\${ch} --chapter-id \${id} --chapter-no \${no} --report ./build/test_reports/quality_report.md\`;
}
function buildValidateCmd() {
  return \`\${py()} -c "import json,yaml,jsonschema; schema=json.load(open('\${fw()}/schemas/book_manifest_schema.json',encoding='utf-8')); manifest=yaml.safe_load(open('manifests/book_manifest.yaml',encoding='utf-8')); jsonschema.validate(manifest,schema); print('Manifest gecerli.')"\`;
}
function buildMermaidExtractCmd() {
  const profile = document.getElementById('pp-profile')?.value || 'configs/post_production_profile.yaml';
  return \`\${py()} tools/postproduction/post_production_pipeline.py --profile \${profile} --stage extract_mermaid\`;
}
function buildMermaidRenderCmd() {
  const profile = document.getElementById('pp-profile')?.value || 'configs/post_production_profile.yaml';
  return \`\${py()} tools/postproduction/post_production_pipeline.py --profile \${profile} --stage render_mermaid\`;
}
function buildQrManifestCmd() {
  return \`\${py()} tools/postproduction/build_qr_manifest_from_code_manifest.py --code-manifest ./build/code_manifest.json --output ./build/qr_manifest.yaml\`;
}
function buildQrCmd() {
  return \`\${py()} tools/postproduction/generate_qr_codes.py --manifest ./build/qr_manifest.yaml --output-dir assets/auto/qr --report ./build/reports/qr_report.md\`;
}
function buildGithubSyncCmd(push) {
  return \`\${py()} -m bookfactory sync-github --code-manifest ./build/code_manifest.json --test-report ./build/test_reports/code_test_report.json --require-tests-passed\${push ? ' --push' : ''}\`;
}
function buildIndexCmd() {
  const profile = document.getElementById('pp-profile')?.value || 'configs/post_production_profile.yaml';
  return \`\${py()} -m bookfactory build-index --profile \${profile}\`;
}

function runStage(stage) {
  const profile = document.getElementById('pp-profile').value.trim() || 'configs/post_production_profile.yaml';
  runTerminal('Post-production: ' + stage, \`\${py()} tools/postproduction/post_production_pipeline.py --profile \${profile} --stage \${stage}\`);
}

function runExport(fmt) {
  const profile = document.getElementById('export-profile').value.trim() || 'configs/post_production_profile.yaml';
  runTerminal('Export: ' + fmt, \`\${py()} -m bookfactory export --profile \${profile} --format \${fmt} --merge-if-missing\`);
}

function loadDist() {
  if (!cfg.bookProjectPath) return;
  runQuiet('dist-list', \`\${py()} -c "import os,json; d='dist'; files=[{'name':f,'size':os.path.getsize(os.path.join(d,f))} for f in os.listdir(d) if not f.startswith('.')] if os.path.isdir(d) else []; print(json.dumps(files))"\`);
}

// ─── Komut çalıştırma ─────────────────────────────────────────────────────────
function runTerminal(label, command) {
  if (!cfg.bookProjectPath) { logErr('Kitap projesi klasörü ayarlanmamış.'); showTab('ayarlar'); return; }
  vscodeApi.postMessage({ type: 'runInTerminal', label, command });
}

function runQuiet(id, command) {
  if (!cfg.bookProjectPath) return;
  vscodeApi.postMessage({ type: 'runQuiet', id, command });
}

function handleQuietResult(msg) {
  if (msg.id === 'validate') {
    const el = document.getElementById('validate-result');
    if (msg.exitCode === 0) {
      el.innerHTML = '<span style="color:#4ec9b0">✓ Manifest geçerli</span>';
      logOk('Manifest doğrulandı.');
    } else {
      el.innerHTML = '<span style="color:#f44">✗ Hata var</span>';
      logErr(msg.stderr || msg.stdout);
    }
  } else if (msg.id === 'dist-list') {
    try {
      const files = JSON.parse(msg.stdout.trim());
      const el = document.getElementById('dist-list');
      if (!files.length) { el.textContent = 'dist/ klasörü boş.'; return; }
      el.innerHTML = files.map(f => \`<div style="display:flex;justify-content:space-between;padding:3px 0;border-bottom:1px solid var(--vscode-panel-border)"><span>\${f.name}</span><span style="color:var(--vscode-descriptionForeground)">\${(f.size/1024).toFixed(0)} KB</span></div>\`).join('');
    } catch(e) { /* ignore */ }
  }
}

async function confirmGithubPush() {
  logWarn('GitHub push başlatılıyor — terminal onayı bekleniyor...');
  runTerminal('GitHub Push', buildGithubSyncCmd(true));
}

// ─── Ayarlar ──────────────────────────────────────────────────────────────────
function saveConfig() {
  vscodeApi.postMessage({
    type: 'saveConfig',
    frameworkPath:   document.getElementById('cfg-framework').value.trim(),
    bookProjectPath: document.getElementById('cfg-book').value.trim(),
    pythonPath:      document.getElementById('cfg-python').value.trim() || 'python',
  });
}

function browse(key) {
  vscodeApi.postMessage({ type: 'browseFolder', key });
}

// ─── Log ──────────────────────────────────────────────────────────────────────
function log(msg, cls) {
  const el = document.getElementById('log');
  const line = document.createElement('div');
  line.className = cls || '';
  line.textContent = '[' + new Date().toLocaleTimeString('tr-TR') + '] ' + msg;
  el.appendChild(line);
  el.scrollTop = el.scrollHeight;
}
function logOk(m)   { log(m, 'log-ok'); }
function logErr(m)  { log(m, 'log-err'); }
function logInfo(m) { log(m, 'log-info'); }
function logWarn(m) { log(m, 'log-warn'); }

function toggleLog() {
  const logEl = document.getElementById('log');
  const btn = document.getElementById('log-toggle');
  const hidden = logEl.style.display === 'none';
  logEl.style.display = hidden ? 'block' : 'none';
  btn.textContent = hidden ? '▼' : '▲';
}

// ─── Init ─────────────────────────────────────────────────────────────────────
vscodeApi.postMessage({ type: 'getConfig' });
</script>
</body>
</html>`;
}

module.exports = { activate, deactivate };
