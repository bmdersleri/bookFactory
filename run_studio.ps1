# BookFactory Studio başlatıcı
# Kullanım: PowerShell içinde BookFactory kök klasöründe çalıştırın.

$ErrorActionPreference = "Stop"
Write-Host "BookFactory Studio başlatılıyor..." -ForegroundColor Cyan
python -m bookfactory_studio.app
