#requires -Version 7.0
<#
.SYNOPSIS
  BookFactory yerel Git deposunu güvenli biçimde sıfırlar ve yeni Git deposu başlatır.

.DESCRIPTION
  - Çalışan Git süreçlerini durdurur.
  - Eski .git klasörünü varsayılan olarak silmez; .git_disabled_<timestamp> olarak yeniden adlandırır.
  - İstenirse -DeleteOldGit ile eski .git klasörünü kalıcı silmeye çalışır.
  - .gitignore içine yerel Git yedeklerini dışlama kuralları ekler.
  - Yeni main branch ile git init yapar.
  - origin remote adresini ekler.
  - Dosyaları otomatik commit/push etmez; önce kullanıcıya kontrol komutlarını verir.

.USAGE
  pwsh -NoProfile -ExecutionPolicy Bypass -File .\reset_bookfactory_git_pwsh7.ps1
  pwsh -NoProfile -ExecutionPolicy Bypass -File .\reset_bookfactory_git_pwsh7.ps1 -DeleteOldGit
#>

[CmdletBinding(SupportsShouldProcess=$true)]
param(
    [string]$ProjectRoot = "C:\OneDrive\OneDrive - mehmetakif.edu.tr\BookFactory",
    [string]$RemoteUrl = "https://github.com/bmdersleri/bookFactory.git",
    [string]$Branch = "main",
    [switch]$DeleteOldGit,
    [switch]$NoInit,
    [switch]$SkipProcessStop
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Info([string]$Message) { Write-Host "[INFO] $Message" -ForegroundColor Cyan }
function Write-Ok([string]$Message) { Write-Host "[OK]   $Message" -ForegroundColor Green }
function Write-Warn([string]$Message) { Write-Host "[WARN] $Message" -ForegroundColor Yellow }
function Write-Err([string]$Message) { Write-Host "[ERR]  $Message" -ForegroundColor Red }

try {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $OutputEncoding = [System.Text.Encoding]::UTF8
} catch { }

if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) {
    throw "Proje klasörü bulunamadı: $ProjectRoot"
}

Set-Location -LiteralPath $ProjectRoot
Write-Info "Proje kökü: $ProjectRoot"
Write-Info "PowerShell sürümü: $($PSVersionTable.PSVersion)"

# 1) Çalışan Git süreçlerini durdur
if (-not $SkipProcessStop) {
    Write-Info "Git ile ilişkili süreçler kontrol ediliyor..."
    $processNames = @(
        "git",
        "git-remote-https",
        "git-remote-http",
        "git-credential-manager",
        "git-lfs"
    )

    foreach ($name in $processNames) {
        $procs = @(Get-Process -Name $name -ErrorAction SilentlyContinue)
        foreach ($p in $procs) {
            try {
                Write-Warn "Durduruluyor: $($p.ProcessName) / PID=$($p.Id)"
                Stop-Process -Id $p.Id -Force -ErrorAction Stop
            } catch {
                Write-Warn "Durdurulamadı: $($p.ProcessName) / PID=$($p.Id) / $($_.Exception.Message)"
            }
        }
    }
    Start-Sleep -Milliseconds 700
}

# 2) .gitignore içine yerel Git yedeklerini ekle
$gitignorePath = Join-Path $ProjectRoot ".gitignore"
if (-not (Test-Path -LiteralPath $gitignorePath)) {
    New-Item -ItemType File -Path $gitignorePath -Force | Out-Null
}

$gitignoreText = Get-Content -LiteralPath $gitignorePath -Raw -ErrorAction SilentlyContinue
if ($null -eq $gitignoreText) { $gitignoreText = "" }

$rulesToEnsure = @(
    "# Local Git backups",
    ".git_backup*/",
    ".git_disabled*/"
)

$rulesAdded = $false
foreach ($rule in $rulesToEnsure) {
    if ($gitignoreText -notmatch [regex]::Escape($rule)) {
        Add-Content -LiteralPath $gitignorePath -Value $rule -Encoding utf8
        $rulesAdded = $true
    }
}
if ($rulesAdded) { Write-Ok ".gitignore içine yerel Git yedek kuralları eklendi." }
else { Write-Ok ".gitignore yerel Git yedek kuralları zaten mevcut." }

# 3) Eski .git klasörünü kaldır veya devre dışı bırak
$gitPath = Join-Path $ProjectRoot ".git"
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$disabledGitPath = Join-Path $ProjectRoot ".git_disabled_$stamp"

if (Test-Path -LiteralPath $gitPath -PathType Container) {
    if ($DeleteOldGit) {
        Write-Warn "Eski .git klasörü kalıcı olarak silinmeye çalışılacak."
        try {
            Remove-Item -LiteralPath $gitPath -Recurse -Force -ErrorAction Stop
            Write-Ok "Eski .git klasörü silindi."
        } catch {
            Write-Warn "PowerShell ile silinemedi: $($_.Exception.Message)"
            Write-Warn "cmd rmdir yöntemi deneniyor..."
            & cmd.exe /c "rmdir /s /q `"$gitPath`""
            Start-Sleep -Milliseconds 700
            if (Test-Path -LiteralPath $gitPath) {
                throw ".git klasörü hâlâ silinemedi. VS Code'u tamamen kapatın, OneDrive eşitlemesini duraklatın ve scripti ayrı bir PowerShell 7 penceresinden tekrar çalıştırın."
            }
            Write-Ok "Eski .git klasörü cmd rmdir ile silindi."
        }
    } else {
        Write-Info "Eski .git klasörü silinmeyecek; devre dışı bırakılacak."
        try {
            Rename-Item -LiteralPath $gitPath -NewName (Split-Path -Leaf $disabledGitPath) -ErrorAction Stop
            Write-Ok "Eski .git klasörü yeniden adlandırıldı: $disabledGitPath"
        } catch {
            Write-Warn "Rename-Item başarısız: $($_.Exception.Message)"
            Write-Warn "Move-Item yöntemi deneniyor..."
            Move-Item -LiteralPath $gitPath -Destination $disabledGitPath -Force -ErrorAction Stop
            Write-Ok "Eski .git klasörü taşındı: $disabledGitPath"
        }
    }
} else {
    Write-Ok ".git klasörü zaten yok."
}

if ($NoInit) {
    Write-Warn "-NoInit seçildi; yeni Git deposu başlatılmadı."
    exit 0
}

# 4) Yeni Git deposunu başlat
Write-Info "Yeni Git deposu başlatılıyor..."
& git init -b $Branch
if ($LASTEXITCODE -ne 0) {
    Write-Warn "git init -b başarısız olabilir. Alternatif yöntem deneniyor..."
    & git init
    if ($LASTEXITCODE -ne 0) { throw "git init başarısız oldu." }
    & git branch -M $Branch
    if ($LASTEXITCODE -ne 0) { throw "git branch -M $Branch başarısız oldu." }
}
Write-Ok "Git deposu başlatıldı: $Branch"

# 5) Remote ekle
Write-Info "origin remote ekleniyor: $RemoteUrl"
& git remote add origin $RemoteUrl
if ($LASTEXITCODE -ne 0) {
    Write-Warn "origin zaten var olabilir; URL güncelleniyor."
    & git remote set-url origin $RemoteUrl
    if ($LASTEXITCODE -ne 0) { throw "origin remote ayarlanamadı." }
}
Write-Ok "origin remote hazır."

Write-Host ""
Write-Host "Sonraki güvenli kontrol komutları:" -ForegroundColor White
Write-Host "  git remote -v" -ForegroundColor Gray
Write-Host "  git status --short --ignored" -ForegroundColor Gray
Write-Host "  git add ." -ForegroundColor Gray
Write-Host "  git status --short" -ForegroundColor Gray
Write-Host "  git commit -m \"Initial BookFactory project upload\"" -ForegroundColor Gray
Write-Host "  git push -u origin $Branch" -ForegroundColor Gray
Write-Host ""
Write-Warn "Commit öncesinde .git_disabled_*, .cleanup_quarantine, arsiv, docs/archive, build, workspace/**/build gibi klasörlerin stage edilmediğini kontrol edin."
