# BookFactory GUI — VS Code Extension

BookFactory işlemlerini VS Code panelinden çalıştırmanızı sağlar.

## Özellikler

- **Proje** — manifest okuma, bölüm özeti, hızlı işlemler
- **Bölümler** — bölüm listesi, yeni bölüm oluşturma, dosya açma
- **Kod Testi** — CODE_META çıkarma → doğrulama → test zinciri
- **Mermaid / QR** — PNG üretimi, QR manifest, GitHub sync
- **Post-production** — pipeline aşamaları, terim dizini, dashboard
- **Export** — DOCX, HTML, EPUB, PDF

## Kurulum

```powershell
# Extension klasörüne git
cd bookfactory-gui

# VS Code extensions klasörüne kopyala
$dest = "$env:USERPROFILE\.vscode\extensions\bookfactory-gui-0.1.0"
Copy-Item . $dest -Recurse -Force

# VS Code'u yeniden başlat
code --relaunch
```

## Kullanım

1. `Ctrl+Shift+P` → **BookFactory: Paneli Aç**
2. Sol menüden **Ayarlar** → framework ve kitap projesi klasörlerini seçin
3. **Kaydet**'e tıklayın
4. Tüm işlemler artık panelden çalışır

## Kısayol

`Ctrl+Shift+B` — Paneli aç/kapat

## Yapılandırma (settings.json)

```json
{
  "bookfactory.frameworkPath": "C:\\OneDrive\\BookFactory",
  "bookfactory.bookProjectPath": "C:\\OneDrive\\react-web",
  "bookfactory.pythonPath": "python"
}
```

## Notlar

- Uzun süren komutlar VS Code entegre terminalinde çalışır, çıktıyı orada izleyebilirsiniz
- Manifest JSON Schema doğrulaması panelden tek tıkla çalıştırılabilir
- GitHub push işlemi her zaman terminalde onay ister
