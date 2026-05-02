# -*- coding: utf-8 -*-
"""FastAPI orchestrator for BookFactory Studio."""
from __future__ import annotations

from dataclasses import asdict
from importlib import resources
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

# Modular Services
from .services.manifest_service import ManifestService
from .services.path_service import PathService
from .services.health_service import HealthService
from .services.prompt_service import PromptService

# Pydantic Models
from .models import (
    ManifestRequest, ManifestYamlRequest, ProjectInitRequest, 
    WizardInitRequest, WizardPromptRequest, ChapterImportRequest, 
    JobRequest, StudioConfigRequest
)

# Core imports (temporarily keeping what isn't fully service-ized)
from .core import (
    load_studio_config, set_active_book, framework_root,
    initialize_project, initialize_project_wizard,
    render_architecture_prompt, dump_yaml, validate_manifest,
    normalize_manifest, parse_yaml_text, pipeline_steps,
    import_chapter_markdown, read_text_report, match_chapter_files,
    write_yaml
)
from .jobs import create_job, get_job, read_job_log

app = FastAPI(title="BookFactory Studio", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = resources.files("bookfactory_studio") / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    html = (Path(str(static_dir)) / "index.html").read_text(encoding="utf-8")
    return HTMLResponse(html)


@app.get("/api/health")
def health() -> dict[str, Any]:
    return {"ok": True, "service": "BookFactory Studio"}


@app.get("/api/studio/config")
def get_studio_config() -> dict[str, Any]:
    config = load_studio_config()
    return {
        "framework_root": str(framework_root()),
        "active_book": config.get("active_book"),
        "recent_books": [b for b in (config.get("recent_books") or []) if Path(b).exists()],
    }


@app.post("/api/studio/config")
def post_studio_config(req: StudioConfigRequest) -> dict[str, Any]:
    try:
        book_path = Path(req.active_book).expanduser().resolve()
        fw = framework_root()
        if book_path == fw:
            raise HTTPException(status_code=400, detail="Kitap kökü, framework kökü ile aynı olamaz.")
        config = set_active_book(str(book_path))
        return {
            "ok": True,
            "framework_root": str(fw),
            "active_book": config["active_book"],
            "recent_books": [b for b in (config.get("recent_books") or []) if Path(b).exists()],
        }
    except HTTPException: raise
    except Exception as exc: raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/project")
def get_project(root: str = Query(".")) -> dict[str, Any]:
    try:
        r = PathService.project_root(root)
        if not ManifestService.find(r):
            raise HTTPException(status_code=400, detail="Aktif dizinde book_manifest.yaml bulunamadı.")
        return HealthService.project_snapshot(r)
    except Exception as exc: raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/control-panel")
def control_panel(root: str = Query(".")) -> dict[str, Any]:
    try:
        r = PathService.project_root(root)
        if not ManifestService.find(r):
            raise HTTPException(status_code=400, detail="Aktif dizinde book_manifest.yaml bulunamadı.")
        return HealthService.control_panel_snapshot(r)
    except Exception as exc: raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/wizard/init-project")
def wizard_init_project(req: WizardInitRequest) -> dict[str, Any]:
    try:
        r = PathService.project_root(req.root)
        return initialize_project_wizard(r, req.data)
    except Exception as exc: raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/project/file")
def get_project_file(path: str = Query(...), root: str = Query(".")) -> FileResponse:
    try:
        r = PathService.project_root(root)
        full_path = (r / path).resolve()
        if not str(full_path).startswith(str(r.resolve())):
            raise HTTPException(status_code=403, detail="Erişim engellendi.")
        if not full_path.exists():
            raise HTTPException(status_code=404, detail="Dosya bulunamadı.")
        return FileResponse(full_path)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/manifest")
def get_manifest(root: str = Query(".")) -> dict[str, Any]:
    r = PathService.project_root(root)
    path = ManifestService.find(r)
    if not path: raise HTTPException(status_code=404, detail="Manifest bulunamadı.")
    manifest = ManifestService.load(path)
    return {"path": str(path), "manifest": manifest, "yaml": dump_yaml(manifest), "validation": validate_manifest(manifest, root=r)}


@app.post("/api/manifest/validate")
def validate_manifest_api(req: ManifestRequest) -> dict[str, Any]:
    try:
        r = PathService.project_root(req.root)
        manifest = normalize_manifest(req.manifest)
        return validate_manifest(manifest, root=r)
    except Exception as exc: raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/manifest/match-chapter-files")
def match_manifest_chapter_files(req: ManifestRequest) -> dict[str, Any]:
    try:
        r = PathService.project_root(req.root)
        return match_chapter_files(r, req.manifest)
    except Exception as exc: raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/manifest/render-yaml")
def render_manifest_yaml(req: ManifestRequest) -> dict[str, Any]:
    try:
        r = PathService.project_root(req.root)
        manifest = normalize_manifest(req.manifest)
        return {"manifest": manifest, "yaml": dump_yaml(manifest), "validation": validate_manifest(manifest, root=r)}
    except Exception as exc: raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/manifest/parse-yaml")
def parse_manifest_yaml_api(req: ManifestYamlRequest) -> dict[str, Any]:
    try:
        r = PathService.project_root(req.root)
        manifest = normalize_manifest(parse_yaml_text(req.yaml_text))
        return {"manifest": manifest, "yaml": dump_yaml(manifest), "validation": validate_manifest(manifest, root=r)}
    except Exception as exc: raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/manifest/save")
def save_manifest(req: ManifestRequest) -> dict[str, Any]:
    try:
        r = PathService.project_root(req.root)
        manifest = normalize_manifest(req.manifest)
        validation = validate_manifest(manifest, root=r)
        if not validation.get("valid") and not req.force:
            raise HTTPException(status_code=422, detail={"message": "Manifest hatalı olduğu için kaydedilmedi.", "validation": validation})
        path = ManifestService.find(r) or (r / "book_manifest.yaml")
        write_yaml(path, manifest)
        return {"ok": True, "path": str(path), "validation": validation, "manifest": manifest, "yaml": dump_yaml(manifest)}
    except HTTPException: raise
    except Exception as exc: raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/manifest/save-yaml")
def save_manifest_yaml(req: ManifestYamlRequest) -> dict[str, Any]:
    try:
        r = PathService.project_root(req.root)
        manifest = normalize_manifest(parse_yaml_text(req.yaml_text))
        validation = validate_manifest(manifest, root=r)
        if not validation.get("valid") and not req.force:
            raise HTTPException(status_code=422, detail={"message": "Manifest hatalı olduğu için kaydedilmedi.", "validation": validation})
        path = ManifestService.find(r) or (r / "book_manifest.yaml")
        write_yaml(path, manifest)
        return {"ok": True, "path": str(path), "validation": validation, "manifest": manifest, "yaml": dump_yaml(manifest)}
    except HTTPException: raise
    except Exception as exc: raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/project/init")
def init_project(req: ProjectInitRequest) -> dict[str, Any]:
    try:
        return initialize_project(PathService.project_root(req.root), req.manifest)
    except Exception as exc: raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/wizard/architecture-prompt")
def architecture_prompt(req: WizardPromptRequest) -> dict[str, Any]:
    try:
        r = PathService.project_root(req.root)
        prompt = render_architecture_prompt(req.data)
        if req.use_rag and req.rag_query:
            from tools.memory.rag_manager import BookContextMemory
            memory = BookContextMemory(r)
            context = memory.retrieve_context(req.rag_query)
            rag_header = "\n\nLLM İÇİN ÖNCEKİ BÖLÜMLERDEN HATIRLATMA (CONTEXT):\n--------------------------------------------------\n"
            prompt += f"{rag_header}{context}\n--------------------------------------------------\n"
        if req.save:
            return PromptService.save_architecture_prompt(r, prompt)
        return {"prompt": prompt, "path": None}
    except Exception as exc: raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/chapter-prompts/generate")
def generate_chapter_prompt_files(req: JobRequest) -> dict[str, Any]:
    try:
        job = create_job(PathService.project_root(req.root), "generate_chapter_prompts", req.options)
        return asdict(job)
    except Exception as exc: raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/chapters/import")
def import_chapter(req: ChapterImportRequest) -> dict[str, Any]:
    try:
        return import_chapter_markdown(PathService.project_root(req.root), req.chapter_id, req.content, lang=req.lang)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/chapters/consistency-audit/{chapter_id}")
def consistency_audit(chapter_id: str, root: str = Query(".")) -> dict[str, Any]:
    try:
        r = PathService.project_root(root)
        manifest_path = ManifestService.find(r)
        if not manifest_path:
            raise HTTPException(status_code=400, detail="Manifest bulunamadı.")

        manifest = ManifestService.load(manifest_path)
        # Find chapter by ID
        chapter = None
        for i, ch in enumerate(ManifestService.chapters_from_manifest(manifest), 1):
            if ManifestService.chapter_id(ch, i) == chapter_id:
                chapter = ch
                break

        if not chapter:
            raise HTTPException(status_code=404, detail="Bölüm bulunamadı.")

        job = create_job(r, "consistency_audit", {"chapter_id": chapter_id})
        return asdict(job)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/chapters/editor-review/{chapter_id}")
def editor_review(chapter_id: str, root: str = Query(".")) -> dict[str, Any]:
    try:
        r = PathService.project_root(root)
        manifest_path = ManifestService.find(r)
        if not manifest_path:
            raise HTTPException(status_code=400, detail="Manifest bulunamadı.")

        manifest = ManifestService.load(manifest_path)
        chapter = None
        for i, ch in enumerate(ManifestService.chapters_from_manifest(manifest), 1):
            if ManifestService.chapter_id(ch, i) == chapter_id:
                chapter = ch
                break

        if not chapter:
            raise HTTPException(status_code=404, detail="Bölüm bulunamadı.")

        job = create_job(r, "editor_review", {"chapter_id": chapter_id})
        return asdict(job)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


from .services.cloud_service import CloudService


@app.get("/api/cloud/status")
def cloud_status(root: str = Query(".")) -> dict[str, Any]:
    try:
        r = PathService.project_root(root)
        return CloudService.check_cloud_status(r)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/cloud/provision")
def cloud_provision(root: str = Query(".")) -> dict[str, Any]:
    try:
        r = PathService.project_root(root)
        manifest_path = ManifestService.find(r)
        if not manifest_path:
            raise HTTPException(status_code=400, detail="Manifest bulunamadı.")
        
        manifest = ManifestService.load(manifest_path)
        files = CloudService.provision_github_configs(r, manifest)
        return {"status": "success", "provisioned_files": files}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/jobs")
def start_job(req: JobRequest) -> dict[str, Any]:
    known = {s["id"] for s in pipeline_steps()}
    if req.step not in known: raise HTTPException(status_code=400, detail=f"Bilinmeyen step: {req.step}")
    try:
        job = create_job(PathService.project_root(req.root), req.step, req.options)
        return asdict(job)
    except Exception as exc: raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/jobs/{job_id}")
def job_status(job_id: str) -> dict[str, Any]:
    job = get_job(job_id)
    if not job: raise HTTPException(status_code=404, detail="Job bulunamadı.")
    return asdict(job)


@app.get("/api/jobs/{job_id}/log", response_class=PlainTextResponse)
def job_log(job_id: str, root: str = Query(".")) -> PlainTextResponse:
    return PlainTextResponse(read_job_log(PathService.project_root(root), job_id))


@app.get("/api/reports")
def reports(root: str = Query(".")) -> dict[str, Any]:
    try:
        r = PathService.project_root(root)
        return {"reports": HealthService.list_reports(r)}
    except Exception as exc: raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/report")
def report(root: str = Query("."), path: str = Query(...)) -> dict[str, Any]:
    try:
        return read_text_report(PathService.project_root(root), path)
    except Exception as exc: raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/code/block/{chapter_id}/{code_id}")
def get_code_block(chapter_id: str, code_id: str, root: str = Query(".")) -> dict[str, Any]:
    try:
        r = PathService.project_root(root)
        res = CodeService.get_code_block(r, chapter_id, code_id)
        if "error" in res:
            raise HTTPException(status_code=404, detail=res["error"])
        return res
    except HTTPException: raise
    except Exception as exc: raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/code/update")
def update_code_block(req: CodeUpdateRequest) -> dict[str, Any]:
    try:
        r = PathService.project_root(req.root)
        success = CodeService.update_code_block(r, req.chapter_id, req.code_id, req.code)
        if not success:
            raise HTTPException(status_code=400, detail="Kod bloğu güncellenemedi.")
        return {"ok": True}
    except Exception as exc: raise HTTPException(status_code=400, detail=str(exc)) from exc


def main() -> None:
    import uvicorn
    uvicorn.run("bookfactory_studio.app:app", host="127.0.0.1", port=8765, reload=False)

if __name__ == "__main__":
    main()
