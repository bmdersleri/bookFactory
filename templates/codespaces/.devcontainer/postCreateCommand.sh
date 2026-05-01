#!/usr/bin/env bash
set -euo pipefail

cd "${CODESPACE_VSCODE_FOLDER:-$(pwd)}"

python -m pip install --upgrade pip
python -m pip install -e ".[dashboard]"
python -m pip install -r requirements-dev.txt || true

# Mermaid CLI uses Puppeteer/Chrome. Dockerfile normally installs Chrome;
# this step writes a stable project-level Puppeteer config and tries a safe
# bootstrap if Chrome is missing in a rebuilt or partially restored Codespace.
if ! python tools/cloud/write_puppeteer_config.py --output configs/puppeteer_config.json --check; then
  echo "Puppeteer Chrome bulunamadı; chrome-headless-shell kurulumu deneniyor..."
  npx puppeteer browsers install chrome-headless-shell || true
  python tools/cloud/write_puppeteer_config.py --output configs/puppeteer_config.json --check || true
fi

python -m bookfactory version
python -m bookfactory doctor --soft
python -m bookfactory codespaces-check || true

cat <<'MSG'

BookFactory Codespace hazır.
Önerilen komutlar:
  python -m bookfactory doctor --soft
  python -m bookfactory test-minimal --fail-on-error
  python -m bookfactory dashboard --check
  python -m streamlit run tools/dashboard/local_dashboard.py -- --root . --profile examples/minimal_book/configs/post_production_profile_minimal.yaml
MSG
