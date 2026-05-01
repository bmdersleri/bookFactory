#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate LLM repair prompts from failed code test results."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def resolve_path(path_value: str, root: Path) -> Path:
    path = Path(path_value)
    return path if path.is_absolute() else root / path


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def find_manifest_item(manifest: dict[str, Any], item_id: str) -> dict[str, Any] | None:
    for item in manifest.get("items", []):
        if str(item.get("id")) == item_id:
            return item
    return None


def step_text(step: dict[str, Any]) -> str:
    parts = [
        f"Step: {step.get('name')}",
        "Command: " + " ".join(step.get("command", [])),
        f"Return code: {step.get('returncode')}",
    ]
    if step.get("stdout"):
        parts.append("STDOUT:\n" + str(step.get("stdout")))
    if step.get("stderr"):
        parts.append("STDERR:\n" + str(step.get("stderr")))
    return "\n".join(parts)


def build_prompt(result: dict[str, Any], manifest_item: dict[str, Any] | None, package_root: Path) -> str:
    code_text = ""
    code_path = None
    if manifest_item and manifest_item.get("code_path"):
        code_path = resolve_path(str(manifest_item["code_path"]), package_root)
        if code_path.exists():
            code_text = code_path.read_text(encoding="utf-8")
    steps = "\n\n".join(step_text(step) for step in result.get("steps", []))
    meta_lines = []
    if manifest_item:
        for key in ["id", "chapter_id", "language", "kind", "title_key", "file", "test", "main_class"]:
            if key in manifest_item:
                meta_lines.append(f"- {key}: `{manifest_item[key]}`")
    else:
        meta_lines.append(f"- id: `{result.get('id')}`")
    return f"""# CODE_REPAIR_PROMPT — {result.get('id')}

Aşağıdaki kod BookFactory v2.5.0 kod doğrulama hattında hata verdi. Görevin, kodu yalnızca hatayı giderecek şekilde düzeltmektir.

## CODE_META özeti

{chr(10).join(meta_lines)}

## Hata özeti

- Durum: `{result.get('status')}`
- Hata nedeni: `{result.get('failure_reason', '')}`

```text
{steps}
```

## Mevcut kod

```{(manifest_item or {}).get('language', result.get('language', 'text'))}
{code_text.rstrip()}
```

## Düzeltme kuralları

1. Dosya adını ve public class adını uyumlu tut.
2. Başlangıç düzeyi kitap kapsamını aşma.
3. Gereksiz yeni kütüphane ekleme.
4. Çıktı beklentisi varsa bunu koru.
5. Yalnızca düzeltilmiş kodu ve kısa hata açıklamasını ver.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate repair prompts for failed code tests.")
    parser.add_argument("--test-report", type=Path, default=Path("build/test_reports/code_test_report.json"))
    parser.add_argument("--manifest", type=Path, default=Path("build/code_manifest.json"))
    parser.add_argument("--out-dir", type=Path, default=Path("build/repair_prompts"))
    parser.add_argument("--package-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)

    package_root = args.package_root.resolve()
    report = load_json(resolve_path(str(args.test_report), package_root))
    manifest = load_json(resolve_path(str(args.manifest), package_root))
    out_dir = resolve_path(str(args.out_dir), package_root)
    out_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for result in report.get("results", []):
        if result.get("status") != "failed":
            continue
        item_id = str(result.get("id"))
        manifest_item = find_manifest_item(manifest, item_id)
        prompt = build_prompt(result, manifest_item, package_root)
        (out_dir / f"{item_id}_repair_prompt.md").write_text(prompt, encoding="utf-8")
        count += 1
    print(f"Repair prompts generated: {count}")
    print(f"Output directory: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
