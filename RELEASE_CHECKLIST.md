# Release Checklist

Bu liste, yeni bir Parametric Computer Book Factory paketi yayımlamadan önce çalıştırılmalıdır.

## Zorunlu kontroller

- [ ] `python tools/check_package_integrity.py .` başarılı mı?
- [ ] `python tools/check_environment.py --soft` çalışıyor mu?
- [ ] `package_manifest.json` güncel mi?
- [ ] `core/` dosyalarında numara çakışması yok mu?
- [ ] `__pycache__`, `.bak`, `.tmp`, `.DS_Store`, `Thumbs.db` yok mu?
- [ ] Örnek manifest YAML parse edilebiliyor mu?
- [ ] Python dosyaları syntax kontrolünden geçiyor mu?
- [ ] ZIP içinde gereksiz build çıktıları yok mu?

## Önerilen kontroller

- [ ] `resolve_assets.py` kuru çalışma testi yapıldı mı?
- [ ] Post-production profile path çözümlemesi doğru mu?
- [ ] Reference DOCX ve Lua filter profildeki yollarla bulunabiliyor mu?
- [ ] LLM yükleme sırası dokümante edilmiş mi?

## v2.4.1 bakım sürümü ek kontrolleri

- [ ] Minimal demo dry-run başarılı mı?
- [ ] `MERMAID_IMAGE_DIR` ile Pandoc/Lua görsel çözümleme testi başarılı mı?
- [ ] Windows batch dosyası proje kökünden referans DOCX ve Lua filter bulabiliyor mu?
- [ ] `manifests/java_fundamentals_manifest.yaml` 33 ana bölüm + 3 ek içeriyor mu?
- [ ] `package_manifest.json` ve `checksums.sha256` yeniden üretildi mi?

## v2.5.0 code validation ek kontrolleri

- [ ] `python -m bookfactory version` çalışıyor mu?
- [ ] `python -m bookfactory test-minimal --fail-on-error` başarılı mı?
- [ ] `tools/code/extract_code_blocks.py` CODE_META bloklarını çıkarabiliyor mu?
- [ ] `tools/code/validate_code_meta.py` kod manifestini doğruluyor mu?
- [ ] `tools/code/run_code_tests.py` Java kodlarını derleyip çalıştırıyor mu?
- [ ] Hatalı test varsa `tools/code/generate_llm_repair_prompt.py` repair prompt üretiyor mu?
- [ ] `schemas/code_meta_schema.json` pakete dahil mi?
- [ ] `docs/code_validation.md` ve `docs/cli_usage.md` güncel mi?

## v2.6.0 GitHub/QR release checks

- [ ] `python -m bookfactory test-code ... --fail-on-error` passes.
- [ ] `python -m bookfactory sync-github ... --require-tests-passed --clean` stages only passed code.
- [ ] `code_manifest_github.json` contains `github_source_url` and `github_page_url` for QR-enabled code.
- [ ] `python -m bookfactory qr-from-code ... --strict-url --fail-on-empty` succeeds.
- [ ] Real `git push` is used only after manual review of staging output.

## v2.7.0 Export Pipeline Checklist

- [x] `bookfactory export` CLI komutu eklendi.
- [x] Markdown export testi yapıldı.
- [x] HTML export testi yapıldı.
- [x] EPUB export testi yapıldı.
- [x] Split site export testi yapıldı.
- [x] Export profil alanları minimal demo dosyasına eklendi.
- [x] Export politika ve kullanım dokümanları eklendi.


## Codespaces release gate

- [ ] `.devcontainer/` dosyaları `templates/codespaces/` şablonlarıyla senkron mu?
- [ ] `python -m bookfactory codespaces-check --fail-on-error` başarılı mı?
- [ ] `python -m bookfactory doctor --soft` sürüm kontrollerini çalıştırıyor mu?
- [ ] Mermaid smoke test için Puppeteer config üretilebiliyor mu?
- [ ] `configs/post_production_profile*.yaml` içinde `mermaid.puppeteer_config` alanı var mı?

## v2.11.0 Release Gates

- [ ] `python -m bookfactory version` returns `2.11.0`.
- [ ] `python -m bookfactory doctor --soft` completes.
- [ ] `python -m bookfactory codespaces-check --fail-on-error` completes.
- [ ] `python -m bookfactory test-minimal --fail-on-error` completes.
- [ ] Multilingual regression tests pass for Java, Python and JavaScript.
- [ ] `python -m bookfactory sync-github ... --require-tests-passed` stages code successfully.
- [ ] `python -m bookfactory render-code-pages ... --clean` creates rich code pages.
- [ ] `python -m bookfactory dashboard --check` confirms Streamlit availability or prints installation guidance.
- [ ] `.github/workflows/bookfactory-ci.yml` is present.
- [ ] `CHANGELOG.md` contains a v2.11.0 entry.
- [ ] `RELEASE_NOTES_v2_11_0.md` is present.
- [ ] `docs/v2_11_0_test_report.md` is present.
