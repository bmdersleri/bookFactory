# Changelog

All notable changes to BookFactory are documented in this file.

## [2.11.0] - 2026-04-30

### Added

- Real read-only Streamlit dashboard panels for code tests, exports, glossary/index outputs, GitHub sync artifacts, code pages and Codespaces reports.
- GitHub Actions workflow at `.github/workflows/bookfactory-ci.yml`.
- `bookfactory render-code-pages` CLI command.
- Rich static code pages containing metadata, run commands, source code and test-result details.
- v2.11.0 release notes and test report.

### Changed

- `tools/github/render_code_pages.py` now renders usable documentation pages instead of minimal placeholder pages.
- `tools/github/sync_code_repository.py` now embeds source code in generated explanation pages and uses the shared YAML/JSON loader correctly.
- Dashboard caption and documentation now reflect v2.11.0.
- Release and checklist documentation now include CI, dashboard and code-page gates.

### Fixed

- Fixed the recursive `load_data()` shadowing bug in GitHub sync/code page tooling.
- Improved the reliability of generated code-page metadata and links.

## [2.10.0] - 2026-04-30

### Added

- Shared YAML/JSON helper module under `tools/utils/yaml_utils.py`.
- Shared process helper module under `tools/utils/process_utils.py`.
- Adapter-based code test architecture.
- Java, Python and JavaScript smoke test adapters.
- `dev` optional dependency group in `pyproject.toml`.
- Multilingual regression sample tests.

### Changed

- `run_code_tests.py` now dispatches through language adapters.
- Repeated YAML fallback readers were consolidated around shared helpers.

## [2.9.1] - 2026-04-30

### Fixed

- Added Puppeteer/Chrome-headless support for Mermaid rendering in Codespaces.
- Added Puppeteer config generation.
- Improved Codespaces checks and `doctor --soft` behavior.
- Reworked Codespaces init to use templates as source of truth.

## [2.9.0] - 2026-04-30

### Added

- GitHub Codespaces integration.
- `.devcontainer` files and Codespaces validation tooling.
- Cloud IDE policy documentation.

## [2.8.1] - 2026-04-29

### Added

- Dashboard/index follow-up improvements.

## [2.8.0] - 2026-04-29

### Added

- Initial local dashboard and index/glossary reporting layer.

## [2.7.0] - 2026-04-29

### Added

- Glossary and back-index generation.

## [2.6.0] - 2026-04-29

### Added

- Export pipeline for Markdown, HTML, EPUB and site outputs.

## [2.5.0] - 2026-04-29

### Added

- Code validation, GitHub sync and QR manifest workflow.

## [2.4.1] - 2026-04-29

### Added

- Post-production and Mermaid rendering improvements.

## v3.1.0-studio-mvp

- BookFactory Studio FastAPI tabanlı yerel web arayüzü eklendi.
- Kitap mimarisi LLM prompt üretimi, manifest görüntüleme, bölüm prompt üretimi ve Markdown içe aktarma akışı eklendi.
- Production pipeline adımları için job/log izleme katmanı eklendi.
- Rapor görüntüleme, Codespaces/GitHub/QR/Mermaid/export orkestrasyon uçları eklendi.
