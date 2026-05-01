# BookFactory — Geliştirme Ortamı Rehberi

**Modül:** `brief_environment.md`  
**Yükleme önceliği:** İsteğe bağlı — Ortam kurulumu veya Windows/Codespaces sorunu varsa yükle  
**İlgili modüller:** [`brief_structure.md`](brief_structure.md)

---

## 1. PowerShell 7 ve VS Code standardı

Windows ortamında önerilen terminal: **PowerShell 7.x / pwsh**

VS Code terminalinde komutlar mümkünse doğrudan `pwsh` profili üzerinden çalıştırılmalıdır. `powershell` komutu çoğu sistemde Windows PowerShell 5.1'i açabilir.

**Betik çalıştırma örneği:**

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\archive_legacy_bookfactory_md_pwsh7.ps1 -Apply
```

**PowerShell profilinde UTF-8 ayarı:**

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
```

---

## 2. VS Code proje ayarları

`.vscode/settings.json` için önerilen temel ayarlar:

```json
{
  "terminal.integrated.defaultProfile.windows": "PowerShell 7",
  "terminal.integrated.cwd": "${workspaceFolder}",
  "files.encoding": "utf8",
  "files.autoGuessEncoding": true,
  "files.eol": "\r\n"
}
```

---

## 3. Dev Container ve GitHub Codespaces politikası

BookFactory içinde `.devcontainer/` klasörü varsa VS Code şu uyarıyı gösterebilir:

```
Folder contains a Dev Container configuration file.
Reopen folder to develop in a container.
```

Bu uyarı normaldir. Yerel Windows + PowerShell 7 ortamı çalışıyorsa container'a geçmek **zorunlu değildir**.

### Hangi ortamı seçmeli?

| Durum | Öneri |
|---|---|
| Yerel Python/Node/Pandoc kurulumu sorunsuz | Yerel ortamla devam et |
| Her kullanıcıda aynı ortam isteniyor | Dev Container veya Codespaces kullan |
| Windows path/UTF-8 sorunları sık yaşanıyor | Dev Container değerlendirilebilir |
| GitHub üzerinden tarayıcıda çalışma isteniyor | GitHub Codespaces uygundur |

**LLM, container geçişini zorunlu gibi sunmamalıdır.**

---

## 4. Codespaces kontrol komutları

```powershell
python -m bookfactory codespaces-check
python -m bookfactory doctor --soft
python -m bookfactory test-minimal --fail-on-error
```

Yeni veya harici bir BookFactory projesine Codespaces dosyalarını eklemek için:

```powershell
python -m bookfactory codespaces-init
```

Ayrıntılar için `docs/codespaces_integration.md` dosyasına bakınız.

---

## 5. Ortam doğrulama komutları

```powershell
python tools/check_package_integrity.py .
python tools/check_environment.py --soft
```

```powershell
python -m bookfactory doctor --soft
python -m bookfactory test-minimal --fail-on-error
```

---

## 6. Sık karşılaşılan sorunlar

| Sorun | Olası neden | Çözüm |
|---|---|---|
| UTF-8 karakter bozulması | PowerShell 5.1 veya eksik encoding ayarı | `$OutputEncoding = [System.Text.Encoding]::UTF8` ekle, `pwsh` kullan |
| `python` bulunamadı | PATH sorunu veya sanal ortam aktif değil | `python --version` ile kontrol et, venv aktive et |
| Mermaid PNG üretilemedi | `MERMAID_IMAGE_DIR` ortam değişkeni eksik | `configs/puppeteer_config.json` oluştur, `doctor --soft` çalıştır |
| Pandoc/DOCX hatası | Pandoc kurulu değil veya PATH'te yok | `pandoc --version` ile kontrol et, `docs/windows_setup.md` oku |
| Node bulunamadı | Node.js kurulu değil | `node --version` ile kontrol et |
