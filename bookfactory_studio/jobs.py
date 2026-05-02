from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from .core import (
    chapter_id,
    chapter_markdown_path,
    chapters_from_manifest,
    ensure_workspace,
    find_manifest,
    framework_root,
    generate_chapter_prompts,
    load_yaml,
    project_snapshot,
    safe_relative,
    validate_manifest,
)

@dataclass
class Job:
    id: str
    step: str
    root: str
    status: str = "queued"
    started_at: str | None = None
    finished_at: str | None = None
    returncode: int | None = None
    title: str = ""
    log_path: str = ""
    summary: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

JOBS: dict[str, Job] = {}
LOCK = threading.Lock()

def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")

def _python() -> str:
    return sys.executable or "python"

def _framework() -> Path:
    return framework_root()

def _tool(*parts: str) -> str:
    return str(_framework().joinpath(*parts))

def _job_file(root: Path, job_id: str) -> Path:
    return root / "build" / "studio_jobs" / f"{job_id}.json"

def _log_file(root: Path, job_id: str) -> Path:
    return root / "build" / "studio_jobs" / f"{job_id}.log"

def _save_job(root: Path, job: Job) -> None:
    path = _job_file(root, job.id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(job), ensure_ascii=False, indent=2), encoding="utf-8")

def create_job(root: Path, step: str, options: dict[str, Any] | None = None) -> Job:
    ensure_workspace(root)
    jid = uuid.uuid4().hex[:12]
    log_path = _log_file(root, jid)
    job = Job(id=jid, step=step, root=str(root), title=step, log_path=safe_relative(log_path, root))
    with LOCK:
        JOBS[jid] = job
    _save_job(root, job)
    thread = threading.Thread(target=_run_job, args=(job, root, options or {}), daemon=True)
    thread.start()
    return job

def get_job(job_id: str) -> Job | None:
    with LOCK:
        return JOBS.get(job_id)

def read_job_log(root: Path, job_id: str) -> str:
    path = _log_file(root, job_id)
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""

def _append(log_path: Path, text: str) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8", errors="replace") as f:
        f.write(text)
        if not text.endswith("\n"):
            f.write("\n")

def _studio_env() -> dict[str, str]:
    env = os.environ.copy()
    fw = str(_framework())
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = fw + (os.pathsep + existing if existing else "")

    # Windows / Turkish locale fix: child Python processes may select cp1254
    # for stdout when running under a pipe. Force UTF-8 so quality reports can
    # print Turkish characters and status icons without UnicodeEncodeError.
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    return env

def _run_subprocess(cmd: list[str], cwd: Path, log_path: Path, env: dict[str, str] | None = None) -> int:
    _append(log_path, "\n$ " + " ".join(cmd) + "\n")
    process = subprocess.Popen(
        cmd,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env or _studio_env(),
    )
    assert process.stdout is not None
    for line in process.stdout:
        _append(log_path, line.rstrip("\n"))
    return process.wait()

def _run_job(job: Job, root: Path, options: dict[str, Any]) -> None:
    log_path = _log_file(root, job.id)
    job.status = "running"
    job.started_at = _now()
    _save_job(root, job)
    _append(log_path, f"BookFactory Studio job started: {job.step} @ {job.started_at}")
    _append(log_path, f"Book root: {root}")
    _append(log_path, f"Framework root: {_framework()}")
    try:
        rc = _execute_step(job.step, root, log_path, options)
        job.returncode = rc
        job.status = "success" if rc == 0 else "failed"
    except Exception as exc:
        job.returncode = 1
        job.status = "failed"
        job.error = str(exc)
        _append(log_path, f"[ERROR] {exc}")
    job.finished_at = _now()
    try:
        job.summary = project_snapshot(root).get("validation", {})
    except Exception:
        job.summary = {}
    _append(log_path, f"BookFactory Studio job finished: {job.status} @ {job.finished_at}")
    with LOCK:
        JOBS[job.id] = job
    _save_job(root, job)

def _execute_step(step: str, root: Path, log_path: Path, options: dict[str, Any]) -> int:
    ensure_workspace(root)
    if step == "validate_manifest":
        path = find_manifest(root)
        if not path:
            _append(log_path, "[FAIL] book_manifest.yaml bulunamadı. Kitap kökü olarak ilgili kitap klasörünü seçin.")
            return 1
        manifest = load_yaml(path)
        report = validate_manifest(manifest)
        out = root / "build" / "reports" / "manifest_validation_report.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        _append(log_path, json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report.get("valid") else 1
    if step == "generate_chapter_prompts":
        use_rag = bool(options.get("use_rag", False))
        rag_query = options.get("rag_query")
        result = generate_chapter_prompts(root, use_rag=use_rag, rag_query=rag_query)
        _append(log_path, json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    if step == "outline_check":
        return _outline_check(root, log_path, options)
    if step == "extract_code":
        return _run_subprocess([_python(), _tool("tools", "code", "extract_code_blocks.py"), "--package-root", str(root), "--out-dir", "build/code", "--manifest", "build/code_manifest.json", "--yaml-manifest", "build/code_manifest.yaml", "--chapters-dir", "chapters"], root, log_path)
    if step == "validate_code":
        return _run_subprocess([_python(), _tool("tools", "code", "validate_code_meta.py"), str(root / "build" / "code_manifest.json"), "--package-root", str(root)], root, log_path)
    if step == "test_code":
        return _run_subprocess([_python(), _tool("tools", "code", "run_code_tests.py"), "--manifest", str(root / "build" / "code_manifest.json"), "--package-root", str(root), "--report-json", str(root / "build" / "test_reports" / "code_test_report.json"), "--report-md", str(root / "build" / "test_reports" / "code_test_report.md")], root, log_path)
    if step == "mermaid_extract":
        return _mermaid_extract(root, log_path)
    if step == "mermaid_render":
        return _run_subprocess([_python(), _tool("tools", "postproduction", "render_mermaid_png.py"), str(root / "assets" / "auto" / "mermaid"), "--recursive", "--force"], root, log_path)
    if step == "qr_manifest":
        code_manifest = root / "build" / "code_manifest_github.json"
        if not code_manifest.exists():
            code_manifest = root / "build" / "code_manifest.json"
        return _run_subprocess([_python(), _tool("tools", "postproduction", "build_qr_manifest_from_code_manifest.py"), "--code-manifest", str(code_manifest), "--output", str(root / "build" / "qr_manifest.yaml"), "--output-prefix", "assets/auto/qr"], root, log_path)
    if step == "qr_generate":
        return _run_subprocess([_python(), _tool("tools", "postproduction", "generate_qr_codes.py"), "--manifest", str(root / "build" / "qr_manifest.yaml"), "--output-dir", "assets/auto/qr", "--report", "build/reports/qr_report.md", "--base-dir", str(root), "--force"], root, log_path)
    if step == "github_sync":
        return _github_sync(root, log_path, options)
    if step == "pages_setup":
        return _pages_setup(root, log_path, options)
    if step == "codespaces_check":
        return _run_subprocess([_python(), _tool("tools", "cloud", "codespaces_check.py"), "--root", str(root), "--report-json", str(root / "build" / "codespaces_check_report.json"), "--report-md", str(root / "build" / "codespaces_check_report.md")], root, log_path)
    if step == "export":
        profile = options.get("profile") or str(root / "configs" / "post_production_profile_studio.yaml")
        return _run_subprocess([_python(), _tool("tools", "export", "export_book.py"), "--profile", str(profile), "--format", options.get("format", "docx"), "--merge-if-missing"], root, log_path)
    if step == "full_production":
        sequence = ["validate_manifest", "outline_check", "extract_code", "validate_code", "test_code", "mermaid_extract", "mermaid_render", "qr_manifest", "qr_generate", "codespaces_check", "export"]
        for sub in sequence:
            _append(log_path, f"\n=== {sub} ===")
            rc = _execute_step(sub, root, log_path, options)
            if rc != 0 and options.get("stop_on_error", True):
                _append(log_path, f"[STOP] {sub} başarısız oldu. Pipeline durduruldu.")
                return rc
        return 0
    _append(log_path, f"Bilinmeyen step: {step}")
    return 1

def _outline_check(root: Path, log_path: Path, options: dict[str, Any] | None = None) -> int:
    options = options or {}
    path = find_manifest(root)
    if not path:
        _append(log_path, "Manifest bulunamadı.")
        return 1
    manifest = load_yaml(path)
    overall = 0
    missing: list[dict[str, Any]] = []
    checked = 0
    for i, ch in enumerate(chapters_from_manifest(manifest), start=1):
        cid = chapter_id(ch, i)
        cfile = chapter_markdown_path(root, ch, i)
        if not cfile.exists():
            rel = safe_relative(cfile, root)
            _append(log_path, f"[MISSING] {cid}: dosya yok: {rel}")
            missing.append({"id": cid, "chapter_no": i, "expected_path": rel, "title": ch.get("title", "")})
            continue
        checked += 1
        report = root / "build" / "quality_reports" / f"{cid}_quality_report.md"
        rc = _run_subprocess([_python(), _tool("tools", "quality", "check_chapter_markdown.py"), "--chapter", str(cfile), "--chapter-id", cid, "--chapter-no", str(i), "--report", str(report)], root, log_path)
        overall = max(overall, rc)

    report_dir = root / "build" / "quality_reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "missing_chapters_report.json").write_text(
        json.dumps({"checked": checked, "missing_count": len(missing), "missing": missing}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    md_lines = [
        "# Eksik Bölüm Dosyaları Raporu",
        "",
        f"- Kontrol edilen mevcut bölüm: {checked}",
        f"- Eksik bölüm dosyası: {len(missing)}",
        "",
    ]
    if missing:
        md_lines.extend(["| Bölüm | Beklenen dosya | Başlık |", "|---|---|---|"])
        for item in missing:
            md_lines.append(f"| {item['id']} | `{item['expected_path']}` | {item.get('title') or ''} |")
    else:
        md_lines.append("Eksik bölüm dosyası bulunmadı.")
    (report_dir / "missing_chapters_report.md").write_text("\n".join(md_lines), encoding="utf-8")

    if missing:
        _append(log_path, f"[INFO] {len(missing)} bölüm dosyası henüz yok. Ayrıntı: build/quality_reports/missing_chapters_report.md")
        if bool(options.get("fail_on_missing_chapters", False)):
            overall = max(overall, 1)
    return overall

def _mermaid_extract(root: Path, log_path: Path) -> int:
    path = find_manifest(root)
    if not path:
        _append(log_path, "Manifest bulunamadı.")
        return 1
    manifest = load_yaml(path)
    overall = 0
    for i, ch in enumerate(chapters_from_manifest(manifest), start=1):
        cid = chapter_id(ch, i)
        cfile = chapter_markdown_path(root, ch, i)
        if not cfile.exists():
            _append(log_path, f"[SKIP] {cid}: dosya yok.")
            continue
        out_dir = root / "assets" / "auto" / "mermaid" / cid
        rc = _run_subprocess([_python(), _tool("tools", "postproduction", "prepare_mermaid_images.py"), str(cfile), "--out-dir", str(out_dir), "--force", "--prefix", cid], root, log_path)
        overall = max(overall, rc)
    return overall

def _github_sync(root: Path, log_path: Path, options: dict[str, Any]) -> int:
    manifest = load_yaml(find_manifest(root)) if find_manifest(root) else {}
    gh = manifest.get("github", {}) or {}
    owner = options.get("owner") or gh.get("owner") or "bmdersleri"
    repo = options.get("repo") or gh.get("repo") or "react-web"
    branch = options.get("branch") or gh.get("branch") or "main"
    cmd = [_python(), _tool("tools", "github", "sync_code_repository.py"), "--code-manifest", str(root / "build" / "code_manifest.json"), "--test-report", str(root / "build" / "test_reports" / "code_test_report.json"), "--package-root", str(root), "--out-dir", str(root / "build" / "github_repo"), "--owner", owner, "--repo", repo, "--branch", branch, "--code-root", options.get("code_root") or gh.get("code_root") or "kodlar", "--pages-root", options.get("pages_root") or gh.get("pages_root") or "docs/kodlar", "--include-all", "--clean"]
    if bool(options.get("commit") or gh.get("commit")):
        cmd.append("--commit")
    if bool(options.get("push") or gh.get("push")):
        cmd.append("--push")
    return _run_subprocess(cmd, root, log_path)

def _pages_setup(root: Path, log_path: Path, options: dict[str, Any]) -> int:
    manifest = load_yaml(find_manifest(root)) if find_manifest(root) else {}
    gh = manifest.get("github", {}) or {}
    owner = options.get("owner") or gh.get("owner") or "bmdersleri"
    repo = options.get("repo") or gh.get("repo") or "react-web"
    docs_dir = options.get("docs_dir") or gh.get("pages", {}).get("source") or str(root / "build" / "github_repo" / "docs")
    docs_dir_path = Path(docs_dir)
    if not docs_dir_path.is_absolute():
        docs_dir_path = root / docs_dir_path
    manifest_path = root / "build" / "code_manifest_github.json"
    if not manifest_path.exists():
        manifest_path = root / "build" / "code_manifest.json"
    return _run_subprocess([_python(), _tool("tools", "github", "setup_github_pages.py"), "--docs-dir", str(docs_dir_path), "--manifest", str(manifest_path), "--owner", owner, "--repo", repo], root, log_path)
