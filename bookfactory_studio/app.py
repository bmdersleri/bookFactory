from __future__ import annotations

from dataclasses import asdict
from importlib import resources
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .core import (
    dump_yaml,
    find_manifest,
    import_chapter_markdown,
    initialize_project,
    load_yaml,
    parse_yaml_text,
    pipeline_steps,
    project_root,
    project_snapshot,
    read_text_report,
    render_architecture_prompt,
    save_architecture_prompt,
    validate_manifest,
    write_yaml,
)
from .jobs import create_job, get_job, read_job_log


class ManifestRequest(BaseModel):
    root: str = "."
    manifest: dict[str, Any]


class WizardPromptRequest(BaseModel):
    root: str = "."
    data: dict[str, Any]
    save: bool = True


class ManifestYamlRequest(BaseModel):
    root: str = "."
    yaml_text: str


class ProjectInitRequest(BaseModel):
    root: str = "."
    manifest: dict[str, Any]


class ChapterImportRequest(BaseModel):
    root: str = "."
    chapter_id: str
    content: str = Field(min_length=1)


class JobRequest(BaseModel):
    root: str = "."
    step: str
    options: dict[str, Any] = Field(default_factory=dict)


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


@app.get("/api/project")
def get_project(root: str = Query(".")) -> dict[str, Any]:
    try:
        return project_snapshot(project_root(root))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/manifest")
def get_manifest(root: str = Query(".")) -> dict[str, Any]:
    r = project_root(root)
    path = find_manifest(r)
    if not path:
        raise HTTPException(status_code=404, detail="Manifest bulunamadı.")
    manifest = load_yaml(path)
    return {"path": str(path), "manifest": manifest, "yaml": dump_yaml(manifest), "validation": validate_manifest(manifest)}


@app.post("/api/manifest/save")
def save_manifest(req: ManifestRequest) -> dict[str, Any]:
    try:
        r = project_root(req.root)
        path = find_manifest(r) or (r / "book_manifest.yaml")
        write_yaml(path, req.manifest)
        return {"ok": True, "path": str(path), "validation": validate_manifest(req.manifest)}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/manifest/save-yaml")
def save_manifest_yaml(req: ManifestYamlRequest) -> dict[str, Any]:
    try:
        r = project_root(req.root)
        manifest = parse_yaml_text(req.yaml_text)
        path = find_manifest(r) or (r / "book_manifest.yaml")
        write_yaml(path, manifest)
        return {"ok": True, "path": str(path), "validation": validate_manifest(manifest), "manifest": manifest}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/project/init")
def init_project(req: ProjectInitRequest) -> dict[str, Any]:
    try:
        return initialize_project(project_root(req.root), req.manifest)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/wizard/architecture-prompt")
def architecture_prompt(req: WizardPromptRequest) -> dict[str, Any]:
    try:
        r = project_root(req.root)
        if req.save:
            return save_architecture_prompt(r, req.data)
        return {"prompt": render_architecture_prompt(req.data), "path": None}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/chapter-prompts/generate")
def generate_chapter_prompt_files(req: JobRequest) -> dict[str, Any]:
    try:
        job = create_job(project_root(req.root), "generate_chapter_prompts", req.options)
        return asdict(job)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/chapters/import")
def import_chapter(req: ChapterImportRequest) -> dict[str, Any]:
    try:
        return import_chapter_markdown(project_root(req.root), req.chapter_id, req.content)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/pipeline/steps")
def steps() -> dict[str, Any]:
    return {"steps": pipeline_steps()}


@app.post("/api/jobs")
def start_job(req: JobRequest) -> dict[str, Any]:
    known = {s["id"] for s in pipeline_steps()}
    if req.step not in known:
        raise HTTPException(status_code=400, detail=f"Bilinmeyen step: {req.step}")
    try:
        job = create_job(project_root(req.root), req.step, req.options)
        return asdict(job)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/jobs/{job_id}")
def job_status(job_id: str) -> dict[str, Any]:
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job bulunamadı. Sunucu yeniden başlatılmış olabilir; build/studio_jobs klasöründeki logları kontrol edin.")
    return asdict(job)


@app.get("/api/jobs/{job_id}/log", response_class=PlainTextResponse)
def job_log(job_id: str, root: str = Query(".")) -> PlainTextResponse:
    return PlainTextResponse(read_job_log(project_root(root), job_id))


@app.get("/api/reports")
def reports(root: str = Query(".")) -> dict[str, Any]:
    try:
        return {"reports": project_snapshot(project_root(root)).get("reports", [])}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/report")
def report(root: str = Query("."), path: str = Query(...)) -> dict[str, Any]:
    try:
        return read_text_report(project_root(root), path)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


def main() -> None:
    import uvicorn

    uvicorn.run("bookfactory_studio.app:app", host="127.0.0.1", port=8765, reload=False)


if __name__ == "__main__":
    main()
