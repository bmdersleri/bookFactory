# BookFactory GitHub Codespaces

Bu klasör, BookFactory projesinin GitHub Codespaces üzerinde tekrarlanabilir şekilde açılmasını destekleyen notları içerir.

Başlangıç komutları:

```bash
python -m bookfactory doctor --soft
python -m bookfactory test-minimal --fail-on-error
python -m bookfactory dashboard --check
python -m streamlit run tools/dashboard/local_dashboard.py -- \
  --root . \
  --profile examples/minimal_book/configs/post_production_profile_minimal.yaml
```

Dashboard varsayılan olarak `8501` portunu kullanır. Bu port `.devcontainer/devcontainer.json` içinde forward edilmiştir.

Mermaid diyagramları için Puppeteer/Chrome desteği v2.9.1 ile devcontainer içinde kuruludur. Project-level config dosyası `configs/puppeteer_config.json` konumunda üretilir.
