from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from bookfactory_studio import app as studio_app


ROOT = Path(__file__).resolve().parents[1]

VALID_MANIFEST = {
    "book": {
        "title": "Studio Smoke Kitabı",
        "author": "BookFactory",
        "year": "2026",
    },
    "language": {
        "primary_language": "tr",
        "output_languages": ["tr"],
    },
    "structure": {
        "chapters": [
            {
                "id": "chapter_01",
                "title": "Giriş",
                "file": "chapter_01_giris.md",
                "status": "planned",
            }
        ]
    },
}


def test_studio_health_endpoint_contract() -> None:
    assert studio_app.health() == {
        "ok": True,
        "service": "BookFactory Studio",
    }


def test_studio_index_serves_static_shell() -> None:
    response = studio_app.index()
    html = response.body.decode("utf-8")

    assert response.status_code == 200
    assert "BookFactory Studio" in html
    assert '<script src="/static/app.js"></script>' in html
    assert '<link rel="stylesheet" href="/static/styles.css" />' in html


def test_studio_project_snapshot_for_framework_root_warns() -> None:
    snapshot = studio_app.get_project(str(ROOT))

    assert snapshot["root"] == str(ROOT)
    assert snapshot["framework_root"] == str(ROOT)
    assert snapshot["is_framework_root"] is True
    assert snapshot["validation"]["valid"] is False
    assert "framework klasörünü değil" in snapshot["validation"]["errors"][0]


def test_studio_manifest_validation_accepts_minimal_manifest() -> None:
    request = studio_app.ManifestRequest(root=str(ROOT), manifest=VALID_MANIFEST)

    validation = studio_app.validate_manifest_api(request)

    assert validation["valid"] is True
    assert validation["errors"] == []


def test_studio_normalizes_enterprise_manifest_policy_blocks() -> None:
    request = studio_app.ManifestRequest(root=str(ROOT), manifest=VALID_MANIFEST)

    rendered = studio_app.render_manifest_yaml(request)
    manifest = rendered["manifest"]

    assert manifest["schema"] == {
        "manifest_version": "1.0",
        "bookfactory_min_version": "3.4.0",
        "studio_min_version": "3.4.0",
    }

    assert manifest["quality_gates"]["require_code_meta"] is True
    assert manifest["quality_gates"]["require_code_tests_passed"] is True
    assert manifest["outputs"] == {
        "docx": True,
        "pdf": True,
        "epub": True,
        "html_site": True,
    }
    assert manifest["ci"] == {
        "enabled": True,
        "fail_on_code_error": True,
        "fail_on_missing_screenshot": False,
    }
    assert "quality_gates:" in rendered["yaml"]
    assert "outputs:" in rendered["yaml"]
    assert "ci:" in rendered["yaml"]


def test_studio_manifest_validation_rejects_invalid_policy_types() -> None:
    manifest = {
        **VALID_MANIFEST,
        "quality_gates": {"require_code_meta": "yes"},
        "outputs": {"docx": "true"},
        "ci": {"enabled": "true"},
    }
    request = studio_app.ManifestRequest(root=str(ROOT), manifest=manifest)

    validation = studio_app.validate_manifest_api(request)

    assert validation["valid"] is False
    assert "quality_gates.require_code_meta boolean olmalıdır." in validation["errors"]
    assert "outputs.docx boolean olmalıdır." in validation["errors"]
    assert "ci.enabled boolean olmalıdır." in validation["errors"]


def test_studio_yaml_parse_and_render_round_trip() -> None:
    yaml_text = """
book:
  title: Studio Smoke Kitabı
  author: BookFactory
  year: "2026"
language:
  primary_language: tr
  output_languages:
    - tr
structure:
  chapters:
    - id: chapter_01
      title: Giriş
      file: chapter_01_giris.md
      status: planned
"""
    parse_request = studio_app.ManifestYamlRequest(
        root=str(ROOT),
        yaml_text=yaml_text,
    )

    parsed = studio_app.parse_manifest_yaml_api(parse_request)
    render_request = studio_app.ManifestRequest(
        root=str(ROOT),
        manifest=parsed["manifest"],
    )
    rendered = studio_app.render_manifest_yaml(render_request)

    assert parsed["validation"]["valid"] is True
    assert rendered["validation"]["valid"] is True
    assert "Studio Smoke Kitabı" in rendered["yaml"]
    assert "chapter_01_giris.md" in rendered["yaml"]


def test_studio_pipeline_steps_include_core_actions() -> None:
    step_ids = {step["id"] for step in studio_app.steps()["steps"]}

    assert {
        "validate_manifest",
        "generate_chapter_prompts",
        "test_code",
        "export",
        "full_production",
    } <= step_ids


def test_studio_static_frontend_references_existing_api_routes() -> None:
    app_js = (ROOT / "bookfactory_studio" / "static" / "app.js").read_text(
        encoding="utf-8"
    )
    route_paths = {
        route.path
        for route in studio_app.app.routes
        if getattr(route, "path", "").startswith("/api/")
    }

    for path in [
        "/api/studio/config",
        "/api/project",
        "/api/control-panel",
        "/api/manifest",
        "/api/manifest/validate",
        "/api/manifest/render-yaml",
        "/api/manifest/parse-yaml",
        "/api/manifest/save",
        "/api/manifest/save-yaml",
        "/api/manifest/match-chapter-files",
        "/api/project/init",
        "/api/wizard/architecture-prompt",
        "/api/jobs",
        "/api/pipeline/steps",
        "/api/chapters/import",
        "/api/reports",
        "/api/report",
    ]:
        assert path in app_js
        assert path in route_paths


def test_studio_control_panel_snapshot_reads_production_artifacts() -> None:
    tmp_path = ROOT / "build" / "pytest-workspaces" / "studio-control-panel"
    if tmp_path.exists():
        shutil.rmtree(tmp_path)
    tmp_path.mkdir(parents=True)
    try:
        manifest = """
book:
  title: Kontrol Paneli Kitabı
  author: BookFactory
language:
  primary_language: tr
structure:
  chapters:
    - id: chapter_01
      title: Giriş
      file: chapter_01_giris.md
      status: draft
      screenshot_plan:
        - id: b01_01_home
          route: /home
quality_gates:
  require_screenshot_plan: true
"""
        (tmp_path / "book_manifest.yaml").write_text(manifest, encoding="utf-8")
        (tmp_path / "chapters").mkdir()
        (tmp_path / "chapters" / "chapter_01_giris.md").write_text(
            "# Giriş\n\n[SCREENSHOT:b01_01_home]\n",
            encoding="utf-8",
        )
        report_dir = tmp_path / "build" / "test_reports"
        report_dir.mkdir(parents=True)
        (report_dir / "code_test_report.json").write_text(
            json.dumps(
                {
                    "summary": {"total": 1, "passed": 0, "failed": 1, "skipped": 0},
                    "results": [
                        {
                            "id": "chapter_01_code01",
                            "chapter_id": "chapter_01",
                            "language": "python",
                            "file": "demo.py",
                            "status": "failed",
                            "steps": [{"returncode": 1, "stderr": "SyntaxError"}],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        code_dir = tmp_path / "build"
        (code_dir / "code_manifest.json").write_text(
            json.dumps(
                {
                    "items": [
                        {
                            "id": "chapter_01_code01",
                            "chapter_id": "chapter_01",
                            "language": "python",
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        export_dir = tmp_path / "exports" / "docx"
        export_dir.mkdir(parents=True)
        (export_dir / "book.docx").write_bytes(b"docx")

        panel = studio_app.control_panel(str(tmp_path))

        assert panel["health"]["checks"][0]["name"] == "Manifest"
        assert panel["chapter_matrix"][0]["id"] == "chapter_01"
        assert panel["chapter_matrix"][0]["code_blocks"] == 1
        assert panel["chapter_matrix"][0]["code_tests"]["failed"] == 1
        assert panel["screenshots"]["missing_count"] == 1
        assert panel["exports"]["files"][0]["format"] == "docx"
        assert "SyntaxError" in panel["repair"]["prompts"][0]["prompt"]
    finally:
        shutil.rmtree(tmp_path, ignore_errors=True)


def test_studio_frontend_has_required_dom_ids() -> None:
    html = (ROOT / "bookfactory_studio" / "static" / "index.html").read_text(
        encoding="utf-8"
    )
    app_js = (ROOT / "bookfactory_studio" / "static" / "app.js").read_text(
        encoding="utf-8"
    )
    ids = set(re.findall(r"\$\('([^']+)'\)", app_js))

    for element_id in ids:
        assert f'id="{element_id}"' in html


def test_bookfactory_studio_static_assets_are_packaged() -> None:
    metadata = json.loads(
        json.dumps(studio_app.app.openapi())
    )

    assert metadata["info"]["title"] == "BookFactory Studio"
    assert metadata["info"]["version"] == "0.1.0"
    assert (ROOT / "bookfactory_studio" / "static" / "index.html").exists()
    assert (ROOT / "bookfactory_studio" / "static" / "app.js").exists()
    assert (ROOT / "bookfactory_studio" / "static" / "styles.css").exists()


def test_book_manifest_schema_defines_enterprise_policy_blocks() -> None:
    schema = json.loads(
        (ROOT / "schemas" / "book_manifest_schema.json").read_text(
            encoding="utf-8"
        )
    )

    properties = schema["properties"]
    assert "schema" in properties
    assert "quality_gates" in properties
    assert "outputs" in properties
    assert "ci" in properties
    assert "require_code_tests_passed" in properties["quality_gates"]["properties"]
    assert "html_site" in properties["outputs"]["properties"]
    assert "fail_on_code_error" in properties["ci"]["properties"]
