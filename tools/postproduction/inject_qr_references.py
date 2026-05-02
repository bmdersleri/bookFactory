#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inject QR code image references into a merged Markdown file.

For each CODE_META block with qr != none, inserts QR PNG image references
immediately after the closing code fence so pandoc/DOCX includes them.

Usage:
  python inject_qr_references.py \
    --merged-md build/merged/book_merged.md \
    --qr-manifest build/qr_manifest.yaml \
    --base-dir . \
    --output build/merged/book_merged.md
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from tools.utils.yaml_utils import load_data


# Matches full <!-- CODE_META ... --> blocks (multi-line)
_META_RE = re.compile(r'(<!--\s*CODE_META\s*\n)(.*?)(\n-->)', re.DOTALL)
# Matches a fenced code block (opening ``` to closing ```)
_FENCE_RE = re.compile(r'(```[^\n]*\n)(.*?)(```)', re.DOTALL)


def _extract_field(meta_text: str, field: str) -> str:
    for line in meta_text.splitlines():
        stripped = line.strip()
        if stripped.startswith(field + ':'):
            return stripped[len(field) + 1:].strip().strip('"\'')
    return ''


def _build_qr_lookup(qr_manifest: Path, qr_final_dir: Path) -> dict[str, dict[str, Path]]:
    """Return {code_id: {kind: abs_path}} from the QR manifest."""
    data = load_data(qr_manifest)
    section = data.get('qr', data)
    lookup: dict[str, dict[str, Path]] = {}
    for entry in section.get('entries', []):
        if not isinstance(entry, dict):
            continue
        code_id = str(entry.get('code_id', '')).strip()
        kind = str(entry.get('kind', '')).strip()      # 'source' or 'page'
        out_val = str(entry.get('output', '')).strip()
        if not (code_id and kind and out_val):
            continue
        filename = Path(out_val).name
        abs_path = (qr_final_dir / filename).resolve()
        lookup.setdefault(code_id, {})[kind] = abs_path
    return lookup


def _qr_snippet(code_id: str, qr_policy: str, lookup: dict[str, dict[str, Path]], width: str) -> str:
    """Build the markdown image lines to inject after the code block."""
    if qr_policy in ('none', 'false', 'no', 'skip'):
        return ''
    entry = lookup.get(code_id, {})
    parts: list[str] = []
    if qr_policy in ('dual', 'source') and 'source' in entry:
        p = entry['source'].as_posix()
        parts.append(f'![QR Kaynak]({p}){{width={width}}}')
    if qr_policy in ('dual', 'page') and 'page' in entry:
        p = entry['page'].as_posix()
        parts.append(f'![QR Sayfa]({p}){{width={width}}}')
    if not parts:
        return ''
    return '\n\n' + '&nbsp;&nbsp;'.join(parts) + '\n'


def inject(text: str, lookup: dict[str, dict[str, Path]], width: str, min_lines: int = 15) -> tuple[str, int]:
    """Scan merged markdown and inject QR images after each code fence."""
    out: list[str] = []
    pos = 0
    injected = 0

    for meta_m in _META_RE.finditer(text):
        meta_body = meta_m.group(2)
        code_id = _extract_field(meta_body, 'id')
        qr_policy = (_extract_field(meta_body, 'qr') or 'dual').lower()

        # Copy everything up to end of CODE_META comment
        out.append(text[pos:meta_m.end()])
        pos = meta_m.end()

        if not code_id or qr_policy in ('none', 'false', 'no', 'skip'):
            continue

        # Find the following fence
        next_meta = _META_RE.search(text, pos)
        fence_m = _FENCE_RE.search(text, pos)
        if fence_m is None:
            continue
        if next_meta and next_meta.start() < fence_m.start():
            continue  # another meta block precedes the fence — skip

        # Extract code and count lines
        code_content = fence_m.group(2)
        line_count = len(code_content.splitlines())

        # Logic: Inject if 'force' OR (not 'none' AND lines >= threshold)
        should_inject = False
        if qr_policy == 'force':
            should_inject = True
        elif qr_policy != 'none' and line_count >= min_lines:
            should_inject = True

        # Copy up to and including the closing ```
        out.append(text[pos:fence_m.end()])
        pos = fence_m.end()

        if should_inject:
            snippet = _qr_snippet(code_id, qr_policy, lookup, width)
            if snippet:
                out.append(snippet)
                injected += 1

    out.append(text[pos:])
    return ''.join(out), injected


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description='Inject QR image references into merged Markdown.')
    ap.add_argument('--merged-md', required=True, type=Path, help='Input merged Markdown file')
    ap.add_argument('--qr-manifest', required=True, type=Path, help='QR manifest YAML/JSON')
    ap.add_argument('--base-dir', type=Path, default=Path('.'), help='Project root (for resolving paths)')
    ap.add_argument('--qr-final-dir', type=Path, default=None,
                    help='Directory containing final QR PNGs (default: <base-dir>/assets/final/qr)')
    ap.add_argument('--output', type=Path, default=None,
                    help='Output Markdown path (default: overwrite --merged-md)')
    ap.add_argument('--width', default='0.8in', help='QR image width in DOCX (default: 0.8in)')
    ap.add_argument('--min-lines', type=int, default=15, help='Minimum code lines to trigger QR (default: 15)')
    args = ap.parse_args(argv)

    base_dir = args.base_dir.resolve()
    qr_final_dir = (args.qr_final_dir or (base_dir / 'assets/final/qr')).resolve()
    merged_path = args.merged_md if args.merged_md.is_absolute() else (base_dir / args.merged_md)
    merged_path = merged_path.resolve()
    output_path = (args.output or merged_path).resolve()

    if not merged_path.exists():
        print(f'[ERROR] Merged markdown not found: {merged_path}', file=sys.stderr)
        return 1

    qr_manifest_path = args.qr_manifest if args.qr_manifest.is_absolute() else (base_dir / args.qr_manifest)
    if not qr_manifest_path.exists():
        print(f'[ERROR] QR manifest not found: {qr_manifest_path}', file=sys.stderr)
        return 1

    if not qr_final_dir.exists():
        print(f'[ERROR] QR final dir not found: {qr_final_dir}', file=sys.stderr)
        print('Run resolve-assets stage first.', file=sys.stderr)
        return 1

    lookup = _build_qr_lookup(qr_manifest_path, qr_final_dir)
    if not lookup:
        print('[WARN] No QR entries found in manifest — nothing to inject.')
        return 0

    text = merged_path.read_text(encoding='utf-8')
    new_text, count = inject(text, lookup, args.width, min_lines=args.min_lines)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(new_text, encoding='utf-8')

    print(f'[OK] Injected QR references: {count}')
    print(f'[OK] Output: {output_path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
