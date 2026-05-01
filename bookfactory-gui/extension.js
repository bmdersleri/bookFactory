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

  // HTML ayrı dosyadan yükleniyor — template literal çakışması yok
  const htmlPath = path.join(context.extensionPath, 'media', 'panel.html');
  panel.webview.html = fs.readFileSync(htmlPath, 'utf8');

  panel.onDidDispose(() => { panel = null; });
  panel.webview.onDidReceiveMessage(msg => handleMessage(msg, context), null, context.subscriptions);
  sendConfig();
}

function handleMessage(msg, context) {
  switch (msg.type) {
    case 'getConfig':    sendConfig(); break;
    case 'saveConfig':   saveConfig(msg.frameworkPath, msg.bookProjectPath, msg.pythonPath); break;
    case 'browseFolder': browseFolder(msg.key); break;
    case 'readManifest': readManifest(); break;
    case 'readChapters': readChapters(); break;
    case 'runInTerminal': runInTerminal(msg.label, msg.command); break;
    case 'runQuiet':     runQuiet(msg.id, msg.command); break;
    case 'openFile':     openFile(msg.filePath); break;
  }
}

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
  panel.webview.postMessage({ type: 'config', ...getConfig() });
}

async function saveConfig(frameworkPath, bookProjectPath, pythonPath) {
  const cfg = vscode.workspace.getConfiguration('bookfactory');

  // await ile sıralı kaydet — hepsi bitmeden sendConfig çalışmasın
  await cfg.update('frameworkPath',   frameworkPath,        vscode.ConfigurationTarget.Global);
  await cfg.update('bookProjectPath', bookProjectPath,      vscode.ConfigurationTarget.Global);
  await cfg.update('pythonPath',      pythonPath || 'python', vscode.ConfigurationTarget.Global);

  // Klasörlerin gerçekten var olup olmadığını kontrol et
  const fwOk   = !!frameworkPath   && fs.existsSync(frameworkPath);
  const bookOk = !!bookProjectPath && fs.existsSync(bookProjectPath);

  const warnings = [];
  if (frameworkPath   && !fwOk)   warnings.push('Framework klasörü bulunamadı: ' + frameworkPath);
  if (bookProjectPath && !bookOk) warnings.push('Kitap klasörü bulunamadı: '     + bookProjectPath);

  if (warnings.length) {
    vscode.window.showWarningMessage(warnings.join(' | '));
  } else {
    vscode.window.showInformationMessage('BookFactory yapılandırması kaydedildi.');
  }

  // Panel'e kayıt sonucunu bildir (yeşil/kırmızı gösterge için)
  send({ type: 'saveResult', fwOk, bookOk, warnings });

  sendConfig(); // await bitti, değerler artık kesinleşti
}

async function browseFolder(key) {
  const uris = await vscode.window.showOpenDialog({
    canSelectFolders: true, canSelectFiles: false, canSelectMany: false,
    openLabel: 'Klasörü Seç'
  });
  if (!uris || !uris[0]) return;
  const cfg = vscode.workspace.getConfiguration('bookfactory');
  cfg.update(key, uris[0].fsPath, vscode.ConfigurationTarget.Global);
  setTimeout(() => sendConfig(), 300);
}

function readManifest() {
  const { bookProjectPath } = getConfig();
  if (!bookProjectPath) { send({ type: 'manifest', error: 'Kitap projesi klasörü ayarlanmamış.' }); return; }
  const manifestPath = path.join(bookProjectPath, 'manifests', 'book_manifest.yaml');
  if (!fs.existsSync(manifestPath)) { send({ type: 'manifest', error: 'Manifest bulunamadı: ' + manifestPath }); return; }
  send({ type: 'manifest', raw: fs.readFileSync(manifestPath, 'utf8') });
}

function readChapters() {
  const { bookProjectPath } = getConfig();
  if (!bookProjectPath) { send({ type: 'chapters', chapters: [] }); return; }
  const dir = path.join(bookProjectPath, 'chapters');
  if (!fs.existsSync(dir)) { send({ type: 'chapters', chapters: [] }); return; }
  const files = fs.readdirSync(dir)
    .filter(f => f.endsWith('.md') && !f.startsWith('.'))
    .sort()
    .map(f => {
      const stat = fs.statSync(path.join(dir, f));
      return { name: f, size: stat.size, mtime: stat.mtime.toISOString() };
    });
  send({ type: 'chapters', chapters: files });
}

function buildEnv() {
  const { frameworkPath } = getConfig();
  const env = { ...process.env };
  if (frameworkPath) {
    env.PYTHONPATH = frameworkPath + (env.PYTHONPATH ? ';' + env.PYTHONPATH : '');
    env.PYTHONUTF8 = '1';
  }
  return env;
}

function runInTerminal(label, command) {
  const { bookProjectPath, frameworkPath } = getConfig();
  const cwd = bookProjectPath || vscode.workspace.rootPath || process.cwd();
  let term = vscode.window.terminals.find(t => t.name === 'BookFactory');
  if (!term) term = vscode.window.createTerminal({ name: 'BookFactory', cwd });
  term.show();
  if (frameworkPath) {
    term.sendText('$env:PYTHONPATH = "' + frameworkPath + '"; $env:PYTHONUTF8 = "1"');
  }
  term.sendText('cd "' + cwd + '"');
  term.sendText(command);
  send({ type: 'terminalStarted', label });
}

function runQuiet(id, command) {
  const { bookProjectPath, pythonPath } = getConfig();
  const cwd = bookProjectPath || vscode.workspace.rootPath || process.cwd();
  const fullCmd = command.replace(/^python\b/, pythonPath || 'python');
  cp.exec(fullCmd, { cwd, env: buildEnv(), encoding: 'utf8' }, (err, stdout, stderr) => {
    send({ type: 'quietResult', id, stdout: stdout || '', stderr: stderr || '', exitCode: err ? (err.code || 1) : 0 });
  });
}

function openFile(filePath) {
  vscode.window.showTextDocument(vscode.Uri.file(filePath));
}

function send(msg) {
  if (panel) panel.webview.postMessage(msg);
}

module.exports = { activate, deactivate };
