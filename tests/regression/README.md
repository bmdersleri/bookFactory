# BookFactory Regression Smoke Tests

This folder contains small local fixtures for v2.10.0 adapter and YAML utility checks.

## Multi-language adapter smoke test

```bash
python -m bookfactory test-code \
  --manifest tests/regression/code_manifests/multilanguage_manifest.json \
  --report-json build/test_reports/regression_multilanguage.json \
  --report-md build/test_reports/regression_multilanguage.md \
  --fail-on-error
```

Expected behavior:

- Java item compiles/runs when JDK is available.
- Python item compiles/runs with the selected Python executable.
- JavaScript item compiles/runs when Node.js is available.
- Missing runtimes are reported as skipped rather than silently treated as passed.
