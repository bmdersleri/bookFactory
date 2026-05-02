# Git ve GitHub ile Modern Versiyon Kontrolü

**Framework:** Parametric Computer Book Factory v3.4.0  
**Dil:** TR  
**Yazar:** Prof. Dr. İsmail KIRBAŞ  
**Başlangıç tarihi:** 2026-05-02

---

## Proje yapısı

```
github-kitabi/
├── chapters/          ← Bölüm Markdown dosyaları
├── chapter_inputs/    ← Bölüm girdi promptları
├── manifests/         ← book_manifest.yaml
├── configs/           ← Post-production profilleri
├── assets/            ← Görseller (auto/manual/locked/final)
├── build/             ← Üretilen kod ve test raporları
├── screenshots/       ← Bölüm ekran görüntüleri
└── dist/              ← Final çıktılar (DOCX, EPUB, PDF)
```

## Kurulum

```powershell
# BookFactory framework'ü klonla (eğer yoksa)
git clone https://github.com/bmdersleri/bookFactory ../bookFactory

# Bu projeyi klonla
git clone <bu-repo-url> github-kitabi
cd github-kitabi

# Python bağımlılıklarını kur
pip install -r ../bookFactory/requirements.txt
```

## Kullanım

```powershell
# Ortam kontrolü
python ../bookFactory/tools/check_environment.py --soft

# Bölüm kod doğrulama
python -m tools.code.extract_code_blocks `
  --package-root ../bookFactory `
  --out-dir ./build/code `
  --manifest ./build/code_manifest.json `
  --chapters-dir ./chapters

# Markdown kalite kontrolü
python -m tools.quality.check_chapter_markdown `
  --chapter ./chapters/chapter_01.md `
  --chapter-id chapter_01 --chapter-no 1
```

## Framework bağlantısı

Bu proje `.bookfactory` dosyasında tanımlı framework sürümünü kullanır.  
Framework reposu: `../bookFactory`
