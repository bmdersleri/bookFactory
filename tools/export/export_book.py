#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Export pipeline for Parametric Computer Book Factory.

Supported outputs:
- merged Markdown copy
- single-page HTML via Pandoc
- EPUB via Pandoc
- split chapter website under dist/site

The tool is intentionally conservative: it does not replace the DOCX/PDF
post-production pipeline. It adds publishing-oriented outputs after chapter
merge, Mermaid preparation and asset resolution have already been handled.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import signal
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from tools.utils.yaml_utils import load_yaml


FRONT_MATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.DOTALL)
HEADER_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
MERMAID_RE = re.compile(r"```mermaid\s*\n.*?\n```", re.DOTALL)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def dump_json(data: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def profile_base(profile_path: Path, profile: dict[str, Any]) -> Path:
    project_root = profile.get("project_root") or profile.get("post_production", {}).get("project_root")
    if project_root:
        p = Path(project_root)
        return p.resolve() if p.is_absolute() else (Path.cwd() / p).resolve()
    return Path.cwd()


def resolve(base: Path, value: str | None) -> Path | None:
    if not value:
        return None
    p = Path(value)
    return p if p.is_absolute() else (base / p).resolve()


def rel_for_report(base: Path, path: Path | None) -> str:
    if path is None:
        return ""
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except Exception:
        return path.as_posix()


def strip_front_matter(text: str) -> str:
    return FRONT_MATTER_RE.sub("", text, count=1).strip()


def slug(value: str) -> str:
    trans = str.maketrans({
        "ı": "i", "ğ": "g", "ü": "u", "ş": "s", "ö": "o", "ç": "c",
        "İ": "i", "Ğ": "g", "Ü": "u", "Ş": "s", "Ö": "o", "Ç": "c",
    })
    value = value.translate(trans).lower().strip()
    out = []
    for ch in value:
        out.append(ch if ch.isalnum() else "-")
    text = "".join(out)
    while "--" in text:
        text = text.replace("--", "-")
    return text.strip("-") or "item"


def chapter_title(path: Path, fallback: str) -> str:
    text = path.read_text(encoding="utf-8")
    no_fm = strip_front_matter(text)
    match = re.search(r"^#\s+(.+?)\s*$", no_fm, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return fallback


def chapter_entries(profile: dict[str, Any], base: Path) -> list[dict[str, Any]]:
    chapters = profile.get("chapters") or profile.get("post_production", {}).get("chapters") or []
    entries: list[dict[str, Any]] = []
    for idx, ch in enumerate(chapters, start=1):
        src = ch.get("source") or ch.get("path")
        if not src:
            continue
        p = resolve(base, str(src))
        if not p:
            continue
        cid = str(ch.get("chapter_id") or ch.get("id") or f"chapter_{idx:02d}")
        title = str(ch.get("title") or chapter_title(p, cid) if p.exists() else cid)
        entries.append({"order": ch.get("order", idx), "chapter_id": cid, "title": title, "path": p})
    entries.sort(key=lambda item: int(item.get("order") or 0))
    return entries


def ensure_merged_markdown(profile_path: Path, profile: dict[str, Any], base: Path, merged_md: Path, dry_run: bool) -> int:
    if merged_md.exists():
        return 0
    print(f"[INFO] Merged Markdown not found: {merged_md}")
    print("[INFO] Creating merged Markdown with built-in export merge fallback.")
    entries = chapter_entries(profile, base)
    if not entries:
        print("[ERROR] No chapters available for merge.", file=sys.stderr)
        return 1
    if dry_run:
        print(f"[DRY-RUN] merge {len(entries)} chapters -> {merged_md}")
        return 0

    book = profile.get("book", {})
    title = book.get("title", {})
    if isinstance(title, dict):
        title_text = title.get("tr") or title.get("en") or next(iter(title.values()), "BookFactory Book")
    else:
        title_text = title or "BookFactory Book"
    front_matter = [
        "---",
        f'title: "{str(title_text)}"',
        f'author: "{str(book.get("author", ""))}"',
        f'date: "{str(book.get("year", ""))}"',
        "lang: tr-TR",
        "toc: true",
        "toc-depth: 2",
        "---",
        "",
    ]
    parts = ["\n".join(front_matter)]
    for idx, entry in enumerate(entries, start=1):
        path = entry["path"]
        if not path.exists():
            print(f"[ERROR] Chapter source not found: {path}", file=sys.stderr)
            return 1
        parts.append(f"\n<!-- SOURCE_FILE: {rel_for_report(base, path)} -->\n\n")
        parts.append(strip_front_matter(path.read_text(encoding="utf-8")))
        if idx != len(entries):
            parts.append("\n\n\\newpage\n\n")
    merged_md.parent.mkdir(parents=True, exist_ok=True)
    merged_md.write_text("".join(parts).strip() + "\n", encoding="utf-8")
    return 0


def pandoc_available() -> bool:
    return shutil.which("pandoc") is not None


def run_pandoc(cmd: list[str], cwd: Path, dry_run: bool, extra_env: dict[str, str] | None = None) -> int:
    print("$ " + " ".join(str(x) for x in cmd), flush=True)
    if dry_run:
        return 0
    timeout = int(os.environ.get("BOOKFACTORY_PANDOC_TIMEOUT_SEC", "120"))
    merged_env = os.environ.copy()
    if extra_env:
        merged_env.update(extra_env)
    popen_kwargs: dict[str, Any] = {
        "cwd": str(cwd),
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "text": True,
        "env": merged_env,
    }
    if os.name == "nt":
        popen_kwargs["creationflags"] = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    else:
        popen_kwargs["start_new_session"] = True
    proc = subprocess.Popen(cmd, **popen_kwargs)
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        try:
            if os.name == "nt":
                proc.kill()
            else:
                os.killpg(proc.pid, signal.SIGKILL)
        except Exception:
            proc.kill()
        stdout, stderr = proc.communicate()
        if stdout.strip():
            print(stdout.strip())
        if stderr.strip():
            print(stderr.strip(), file=sys.stderr)
        print(f"[ERROR] Pandoc timed out after {timeout} seconds.", file=sys.stderr)
        return 124
    if stdout.strip():
        print(stdout.strip())
    if stderr.strip():
        print(stderr.strip(), file=sys.stderr)
    return int(proc.returncode or 0)


def pandoc_common_args(profile: dict[str, Any], base: Path) -> list[str]:
    pp = profile.get("post_production", {})
    pandoc_cfg = pp.get("pandoc", {})
    args = ["-f", pandoc_cfg.get("from", "markdown+tex_math_single_backslash")]
    if pandoc_cfg.get("toc", True):
        args.append("--toc")
    args.append(f"--toc-depth={pandoc_cfg.get('toc_depth', 2)}")
    for meta_key, meta_value in (pandoc_cfg.get("metadata") or {}).items():
        args.append(f"--metadata={meta_key}:{meta_value}")
    return args


def export_markdown(merged_md: Path, output: Path, dry_run: bool) -> dict[str, Any]:
    print(f"[EXPORT] Markdown -> {output}")
    if not dry_run:
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(merged_md, output)
    return {"format": "markdown", "output": str(output), "status": "DRY_RUN" if dry_run else "OK"}


def export_html(merged_md: Path, output: Path, profile: dict[str, Any], base: Path, css: Path | None, dry_run: bool) -> dict[str, Any]:
    print(f"[EXPORT] HTML -> {output}")
    if not dry_run:
        output.parent.mkdir(parents=True, exist_ok=True)
        body = fallback_markdown_to_html(merged_md.read_text(encoding="utf-8"))
        css_text = css.read_text(encoding="utf-8") if css and css.exists() else DEFAULT_SITE_CSS
        page = wrap_site_page("BookFactory HTML Export", body, "")
        page = page.replace('<link rel="stylesheet" href="">', f'<style>\n{css_text}\n</style>')
        output.write_text(page, encoding="utf-8")
    return {"format": "html", "output": str(output), "status": "DRY_RUN" if dry_run else "OK"}


def export_epub(merged_md: Path, output: Path, profile: dict[str, Any], base: Path, css: Path | None, cover: Path | None, dry_run: bool) -> dict[str, Any]:
    print(f"[EXPORT] EPUB -> {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["pandoc", *pandoc_common_args(profile, base), str(merged_md), "-o", str(output)]
    if css and css.exists():
        cmd.append(f"--css={css}")
    if cover and cover.exists():
        cmd.append(f"--epub-cover-image={cover}")
    rc = run_pandoc(cmd, cwd=merged_md.parent if merged_md.parent.exists() else base, dry_run=dry_run)
    return {"format": "epub", "output": str(output), "status": "OK" if rc == 0 else "ERROR", "returncode": rc}


def _run_tool(script: Path, args: list[str], cwd: Path, dry_run: bool) -> int:
    cmd = [sys.executable, str(script), *args]
    print("$ " + " ".join(str(x) for x in cmd), flush=True)
    if dry_run:
        return 0
    return subprocess.run(cmd, cwd=str(cwd)).returncode


def postprocess_docx(output: Path, profile: dict[str, Any], base: Path, dry_run: bool) -> list[str]:
    """Run fix-docx and optimize-tables on the produced DOCX. Returns warning messages."""
    tools_dir = repo_root() / "tools" / "postproduction"
    pp = profile.get("post_production", {})
    docx_cfg = pp.get("docx_postprocess", {})
    warnings: list[str] = []

    if docx_cfg.get("enabled", True) is False:
        print("[DOCX-POST] Devre dışı (docx_postprocess.enabled: false)", flush=True)
        return warnings

    # fix-docx
    fix_tool = docx_cfg.get("format_fix_tool", "fix_docx_format_ooxml.py")
    fix_args = [str(output), "--in-place"]
    if not docx_cfg.get("fix_table_headers", True):
        fix_args.append("--no-table-header-fix")
    rc = _run_tool(tools_dir / fix_tool, fix_args, base, dry_run)
    if rc:
        warnings.append(f"fix-docx returned {rc}")

    # optimize-tables
    if docx_cfg.get("optimize_tables", True):
        opt_args = [str(output), "--in-place", "--mode", docx_cfg.get("table_mode", "proportional")]
        rc = _run_tool(tools_dir / "optimize_docx_tables.py", opt_args, base, dry_run)
        if rc:
            warnings.append(f"optimize-tables returned {rc}")

    return warnings


def export_docx(merged_md: Path, output: Path, profile: dict[str, Any], base: Path, dry_run: bool) -> dict[str, Any]:
    print(f"[EXPORT] DOCX -> {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    pp = profile.get("post_production", {})
    pandoc_cfg = pp.get("pandoc", {})
    mermaid_cfg = pp.get("mermaid", {})
    exports_cfg = pp.get("exports", {}) or profile.get("exports", {}) or {}
    docx_cfg = exports_cfg.get("docx", {})

    reference_docx = resolve(base, docx_cfg.get("reference_docx") or pandoc_cfg.get("reference_docx"))
    lua_filter = resolve(base, docx_cfg.get("lua_filter") or pandoc_cfg.get("lua_filter"))
    mermaid_dir = resolve(base, mermaid_cfg.get("output_dir") or "assets/auto/diagrams")

    cmd = ["pandoc", *pandoc_common_args(profile, base), str(merged_md), "-o", str(output)]
    if reference_docx and reference_docx.exists():
        cmd.append(f"--reference-doc={reference_docx}")
    if lua_filter and lua_filter.exists():
        cmd.append(f"--lua-filter={lua_filter}")

    extra_env: dict[str, str] = {}
    if mermaid_dir and mermaid_dir.exists():
        extra_env["MERMAID_IMAGE_WIDTH"] = str(mermaid_cfg.get("docx_width", "4.90in"))
        extra_env["MERMAID_IMAGE_DIR"] = mermaid_dir.as_posix()

    rc = run_pandoc(cmd, cwd=merged_md.parent if merged_md.parent.exists() else base, dry_run=dry_run, extra_env=extra_env)
    if rc:
        return {"format": "docx", "output": str(output), "status": "ERROR", "returncode": rc}

    print("[DOCX-POST] fix-docx + optimize-tables başlıyor...", flush=True)
    warnings = postprocess_docx(output, profile, base, dry_run)
    status = "OK" if not warnings else "WARN"
    result: dict[str, Any] = {"format": "docx", "output": str(output), "status": status, "returncode": 0}
    if warnings:
        result["warnings"] = warnings
    return result


def _detect_pdf_engine() -> str:
    for engine in ("xelatex", "lualatex", "pdflatex", "wkhtmltopdf", "weasyprint"):
        if shutil.which(engine):
            return engine
    return "xelatex"


def export_pdf(merged_md: Path, output: Path, profile: dict[str, Any], base: Path, dry_run: bool) -> dict[str, Any]:
    print(f"[EXPORT] PDF -> {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    pp = profile.get("post_production", {})
    exports_cfg = pp.get("exports", {}) or profile.get("exports", {}) or {}
    pdf_cfg = exports_cfg.get("pdf", {})

    engine = pdf_cfg.get("engine") or _detect_pdf_engine()
    if not shutil.which(engine):
        return {"format": "pdf", "output": str(output), "status": "ERROR",
                "note": f"PDF engine not found: {engine}. Install xelatex (MiKTeX/TeX Live) or wkhtmltopdf."}

    cmd = ["pandoc", *pandoc_common_args(profile, base), str(merged_md), "-o", str(output),
           f"--pdf-engine={engine}",
           "-M", "numbersections=false"]

    lua_filter = resolve(base, pdf_cfg.get("lua_filter") or pp.get("pandoc", {}).get("lua_filter"))
    if lua_filter and lua_filter.exists():
        cmd.append(f"--lua-filter={lua_filter}")

    for k, v in (pdf_cfg.get("variables") or {}).items():
        cmd.extend(["-V", f"{k}={v}"])

    rc = run_pandoc(cmd, cwd=merged_md.parent if merged_md.parent.exists() else base, dry_run=dry_run)
    return {"format": "pdf", "output": str(output), "status": "OK" if rc == 0 else "ERROR", "returncode": rc}


def fallback_markdown_to_html(text: str) -> str:
    """Small fallback renderer used only if Pandoc is unavailable for site pages."""
    text = strip_front_matter(text)
    text = MERMAID_RE.sub("<pre class=\"mermaid-placeholder\">Mermaid diagram placeholder</pre>", text)
    lines: list[str] = []
    in_code = False
    code_lines: list[str] = []
    para: list[str] = []

    def flush_para() -> None:
        if para:
            lines.append("<p>" + html.escape(" ".join(para)) + "</p>")
            para.clear()

    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            if not in_code:
                flush_para()
                in_code = True
                code_lines = []
            else:
                lines.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                in_code = False
            continue
        if in_code:
            code_lines.append(line)
            continue
        m = re.match(r"^(#{1,6})\s+(.+)$", line)
        if m:
            flush_para()
            level = len(m.group(1))
            lines.append(f"<h{level}>" + html.escape(m.group(2).strip()) + f"</h{level}>")
        elif not line.strip():
            flush_para()
        elif line.startswith("- "):
            flush_para()
            lines.append("<ul><li>" + html.escape(line[2:].strip()) + "</li></ul>")
        else:
            para.append(line.strip())
    flush_para()
    return "\n".join(lines)


def chapter_to_html_with_pandoc(chapter: Path, out: Path, css_name: str | None, dry_run: bool) -> int:
    cmd = ["pandoc", "-f", "markdown+tex_math_single_backslash", str(chapter), "-o", str(out), "--standalone"]
    if css_name:
        cmd.append(f"--css={css_name}")
    return run_pandoc(cmd, cwd=chapter.parent, dry_run=dry_run)


def export_site(profile_path: Path, profile: dict[str, Any], base: Path, site_dir: Path, css: Path | None, dry_run: bool) -> dict[str, Any]:
    print(f"[EXPORT] split HTML site -> {site_dir}")
    entries = chapter_entries(profile, base)
    pages_dir = site_dir / "chapters"
    css_rel = "../assets/bookfactory.css"
    outputs: list[dict[str, str]] = []

    if not dry_run:
        pages_dir.mkdir(parents=True, exist_ok=True)
        (site_dir / "assets").mkdir(parents=True, exist_ok=True)
        if css and css.exists():
            shutil.copyfile(css, site_dir / "assets" / "bookfactory.css")
        else:
            (site_dir / "assets" / "bookfactory.css").write_text(DEFAULT_SITE_CSS, encoding="utf-8")

    for idx, entry in enumerate(entries, start=1):
        chapter_path = entry["path"]
        page_name = f"{idx:02d}-{slug(entry['chapter_id'])}.html"
        out = pages_dir / page_name
        if not chapter_path.exists():
            outputs.append({"chapter_id": entry["chapter_id"], "status": "MISSING", "output": str(out)})
            continue

        if dry_run:
            status = "DRY_RUN"
        else:
            body = fallback_markdown_to_html(chapter_path.read_text(encoding="utf-8"))
            out.write_text(wrap_site_page(str(entry["title"]), body, css_rel), encoding="utf-8")
            status = "OK"
        outputs.append({"chapter_id": entry["chapter_id"], "title": str(entry["title"]), "status": status, "output": str(out)})

    if not dry_run:
        index_body = ["<h1>BookFactory HTML Site</h1>", "<ol>"]
        for item in outputs:
            if item.get("status") == "OK":
                href = "chapters/" + Path(item["output"]).name
                index_body.append(f'<li><a href="{html.escape(href)}">{html.escape(item.get("title") or item["chapter_id"])}</a></li>')
            else:
                index_body.append(f'<li>{html.escape(item["chapter_id"])} — {html.escape(item.get("status", "UNKNOWN"))}</li>')
        index_body.append("</ol>")
        (site_dir / "index.html").write_text(wrap_site_page("BookFactory HTML Site", "\n".join(index_body), "assets/bookfactory.css"), encoding="utf-8")

    return {"format": "site", "output": str(site_dir), "status": "DRY_RUN" if dry_run else "OK", "pages": outputs}


def wrap_site_page(title: str, body: str, css_href: str) -> str:
    return f"""<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" href="{html.escape(css_href)}">
</head>
<body>
<main class="bookfactory-page">
{body}
</main>
</body>
</html>
"""


DEFAULT_SITE_CSS = """
:root { font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
body { margin: 0; background: #f7f7f8; color: #202124; }
.bookfactory-page { max-width: 920px; margin: 0 auto; padding: 2.5rem 1.4rem; background: #fff; min-height: 100vh; }
pre { overflow-x: auto; padding: 1rem; border-radius: 0.6rem; background: #f0f0f0; }
code { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; }
table { border-collapse: collapse; width: 100%; margin: 1rem 0; }
th, td { border: 1px solid #d5d7da; padding: 0.5rem; vertical-align: top; }
blockquote { border-left: 4px solid #b7b7b7; margin-left: 0; padding-left: 1rem; color: #444; }
a { color: #0b57d0; }
""".strip() + "\n"


def write_report(results: list[dict[str, Any]], report_json: Path, report_md: Path, base: Path, dry_run: bool) -> None:
    data = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "dry_run": dry_run,
        "results": results,
    }
    dump_json(data, report_json)
    lines = ["# Export Pipeline Report", "", f"Generated at: {data['generated_at']}", f"Dry run: {dry_run}", ""]
    lines.append("| Format | Status | Output |")
    lines.append("|---|---:|---|")
    for result in results:
        lines.append(f"| {result.get('format')} | {result.get('status')} | `{rel_for_report(base, Path(result.get('output', '')))}` |")
    report_md.parent.mkdir(parents=True, exist_ok=True)
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Export BookFactory content to EPUB, HTML and split website outputs.")
    ap.add_argument("--profile", required=True, help="Post-production profile YAML")
    ap.add_argument("--format", dest="formats", action="append", choices=["all", "markdown", "html", "epub", "docx", "pdf", "site"], default=[])
    ap.add_argument("--merged-md", help="Merged Markdown path. Defaults to post_production.build.merged_markdown")
    ap.add_argument("--output-dir", help="Export output directory. Defaults to profile exports.output_dir or dist")
    ap.add_argument("--merge-if-missing", action="store_true", help="Run merge_chapters.py if merged Markdown is missing")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--require-pandoc", action="store_true", help="Fail if Pandoc is missing for Pandoc-based exports")
    args = ap.parse_args(argv)

    profile_path = Path(args.profile).resolve()
    profile = load_yaml(profile_path)
    base = profile_base(profile_path, profile)
    pp = profile.get("post_production", {})
    build = pp.get("build", {})
    exports_cfg = pp.get("exports", {}) or profile.get("exports", {}) or {}

    merged_md = resolve(base, args.merged_md or build.get("merged_markdown") or exports_cfg.get("merged_markdown") or "build/book_merged.md")
    if merged_md is None:
        print("[ERROR] Unable to resolve merged Markdown path.", file=sys.stderr)
        return 1

    output_dir = resolve(base, args.output_dir or exports_cfg.get("output_dir") or "dist")
    assert output_dir is not None

    requested = args.formats or exports_cfg.get("formats") or ["html"]
    if "all" in requested:
        requested = ["markdown", "html", "epub", "docx", "pdf", "site"]

    if args.merge_if_missing:
        rc = ensure_merged_markdown(profile_path, profile, base, merged_md, args.dry_run)
        if rc:
            return rc

    if not merged_md.exists() and any(fmt in {"markdown", "html", "epub"} for fmt in requested) and not args.dry_run:
        print(f"[ERROR] Merged Markdown not found: {merged_md}", file=sys.stderr)
        print("Hint: run post-production merge first or pass --merge-if-missing.", file=sys.stderr)
        return 1

    pandoc_needed = any(fmt in {"epub", "docx", "pdf"} for fmt in requested)
    if pandoc_needed and not pandoc_available():
        message = "Pandoc is required for single HTML/EPUB export."
        if args.require_pandoc:
            print(f"[ERROR] {message}", file=sys.stderr)
            return 1
        print(f"[WARN] {message} Split site export can still use fallback rendering.")

    css_html = resolve(base, exports_cfg.get("html", {}).get("css") or "templates/export/html/bookfactory.css")
    css_epub = resolve(base, exports_cfg.get("epub", {}).get("css") or "templates/export/epub/epub.css")
    cover = resolve(base, exports_cfg.get("epub", {}).get("cover_image"))

    results: list[dict[str, Any]] = []
    for fmt in requested:
        if fmt == "markdown":
            output = resolve(base, exports_cfg.get("markdown", {}).get("output") or str(output_dir / "book_merged.md"))
            assert output is not None
            results.append(export_markdown(merged_md, output, args.dry_run))
        elif fmt == "html":
            output = resolve(base, exports_cfg.get("html", {}).get("output") or str(output_dir / "book.html"))
            assert output is not None
            results.append(export_html(merged_md, output, profile, base, css_html, args.dry_run))
        elif fmt == "epub":
            output = resolve(base, exports_cfg.get("epub", {}).get("output") or str(output_dir / "book.epub"))
            assert output is not None
            results.append(export_epub(merged_md, output, profile, base, css_epub, cover, args.dry_run))
        elif fmt == "docx":
            output = resolve(base, exports_cfg.get("docx", {}).get("output") or str(output_dir / "book.docx"))
            assert output is not None
            results.append(export_docx(merged_md, output, profile, base, args.dry_run))
        elif fmt == "pdf":
            output = resolve(base, exports_cfg.get("pdf", {}).get("output") or str(output_dir / "book.pdf"))
            assert output is not None
            results.append(export_pdf(merged_md, output, profile, base, args.dry_run))
        elif fmt == "site":
            site_dir = resolve(base, exports_cfg.get("site", {}).get("output_dir") or str(output_dir / "site"))
            assert site_dir is not None
            results.append(export_site(profile_path, profile, base, site_dir, css_html, args.dry_run))

    report_json = resolve(base, exports_cfg.get("report_json") or "build/reports/export_report.json")
    report_md = resolve(base, exports_cfg.get("report_md") or "build/reports/export_report.md")
    assert report_json is not None and report_md is not None
    if not args.dry_run:
        write_report(results, report_json, report_md, base, args.dry_run)
        print(f"Report: {report_md}")

    failed = [r for r in results if r.get("status") == "ERROR"]
    return 1 if failed else 0


if __name__ == "__main__":
    _code = main()
    sys.stdout.flush()
    sys.stderr.flush()
    print("[OK] Export pipeline finished.", flush=True)
    os._exit(int(_code))
