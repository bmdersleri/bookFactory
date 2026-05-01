$ErrorActionPreference = "Stop"

Write-Host "React BookFactory temiz derleme başlıyor..."

$root = (Get-Location).Path
$chapters = Join-Path $root "workspace\react\chapters"
$build = Join-Path $root "workspace\react\build"
$codeDir = Join-Path $build "code"
$reportDir = Join-Path $build "test_reports"

Write-Host "1) Chapter dosyaları kontrol ediliyor..."
Get-ChildItem $chapters -Filter "chapter_01*.md" | Format-Table Name, Length, LastWriteTime

Write-Host "2) Eski build çıktıları temizleniyor..."
Remove-Item $codeDir -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item $reportDir -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item (Join-Path $build "code_manifest.json") -Force -ErrorAction SilentlyContinue
Remove-Item (Join-Path $build "code_manifest.yaml") -Force -ErrorAction SilentlyContinue

New-Item -ItemType Directory -Force -Path $codeDir | Out-Null
New-Item -ItemType Directory -Force -Path $reportDir | Out-Null

Write-Host "3) CODE_META blokları çıkarılıyor..."
python -m tools.code.extract_code_blocks `
  --package-root . `
  --out-dir .\workspace\react\build\code `
  --manifest .\workspace\react\build\code_manifest.json `
  --yaml-manifest .\workspace\react\build\code_manifest.yaml `
  --chapters-dir .\workspace\react\chapters

Write-Host "4) CODE_META doğrulanıyor..."
python -m tools.code.validate_code_meta `
  .\workspace\react\build\code_manifest.json `
  --package-root .

Write-Host "5) Kod testleri çalıştırılıyor..."
python -m tools.code.run_code_tests `
  --manifest .\workspace\react\build\code_manifest.json `
  --package-root . `
  --report-json .\workspace\react\build\test_reports\code_test_report.json `
  --report-md .\workspace\react\build\test_reports\code_test_report.md `
  --node node `
  --fail-on-error

Write-Host "Temiz derleme tamamlandı."