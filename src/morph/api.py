from __future__ import annotations

import json
import os
import secrets
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from fastapi.responses import FileResponse, Response

from morph.contracts import Budget, RecoveryPackage, RunManifest, RunResult
from morph.evidence import export_bundle
from morph.store import Conflict, Store
from morph.worker import ExecutionRejected, validate_execution_manifest

ROOT = Path(__file__).resolve().parents[2]
VERIFICATION = ROOT / "docs" / "verification"


def create_app(store: Store | None = None, token: str | None = None) -> FastAPI:
    access_token = token or os.environ.get("MORPH_API_TOKEN", "")
    if len(access_token) < 32:
        raise RuntimeError("Set MORPH_API_TOKEN to a random secret of at least 32 characters")
    database = store or Store(
        Path("data/morph.sqlite"), Budget(rollouts=100, wall_seconds=86400, gpu_hours=24, cost_usd=0)
    )

    def authorize(authorization: Annotated[str | None, Header()] = None):
        if not secrets.compare_digest(authorization or "", "Bearer " + access_token):
            raise HTTPException(401, "Bearer authorization required")

    # Frozen evidence is public/read-only so reviewers do not handle an operator
    # secret. Queue and export operations remain authenticated.
    app = FastAPI(title="Morph", version="0.1.0")

    @app.get("/api/v1/status")
    def status():
        provider_verified = (VERIFICATION / "nebius-recovery-selection.json").is_file()
        summary_ready = (VERIFICATION / "confirmation-summary.json").is_file()
        return {
            "mode": "Simulation",
            "simulation_gate": "evaluated" if summary_ready else "blocked",
            "reason": (
                "Independent confirmation complete; simulation recovery gate passed"
                if summary_ready
                else "Held-out evidence is incomplete"
            ),
            "hardware": "disabled",
            "provider": "live_verified" if provider_verified else "not_live_verified",
        }

    @app.get("/api/v1/evidence/summary")
    def evidence_summary():
        path = VERIFICATION / "confirmation-summary.json"
        if not path.is_file():
            raise HTTPException(404, "Held-out evidence is not available")
        return json.loads(path.read_text(encoding="utf-8"))

    @app.get("/api/v1/evidence/audits/{audit_name}")
    def evidence_audit(audit_name: str):
        allowed = {
            "nominal": "baseline-model799-audit.json",
            "fault": "confirmation-fault-baseline.json",
            "morph": "confirmation-morph-balanced75.json",
            "random": "confirmation-random-arm67-jaw80.json",
        }
        filename = allowed.get(audit_name)
        if filename is None:
            raise HTTPException(404, "Unknown evidence audit")
        return json.loads((VERIFICATION / filename).read_text(encoding="utf-8"))

    @app.get("/api/v1/evidence/context")
    def evidence_context():
        # Read-only planner and pilot records the workbench narrates beside the confirmation.
        files = {
            "planner": "nebius-recovery-selection.json",
            "planner_usage": "nebius-live-summary.json",
            "pilot": "heldout-summary.json",
        }
        context = {}
        for key, filename in files.items():
            path = VERIFICATION / filename
            context[key] = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None
        return context

    @app.get("/api/v1/evidence/bundle")
    def confirmation_bundle():
        path = ROOT / "dist" / "morph-confirmation-evidence-v1.zip"
        if not path.is_file():
            raise HTTPException(404, "Confirmation evidence bundle is not available")
        return FileResponse(path, media_type="application/zip", filename=path.name)

    @app.get("/api/v1/runs")
    def runs(
        limit: Annotated[int, Query(ge=1, le=100)] = 100,
        offset: Annotated[int, Query(ge=0)] = 0,
        _: None = Depends(authorize),
    ):
        return {"data": database.list(limit, offset)}

    @app.post("/api/v1/runs", status_code=201)
    def submit(manifest: RunManifest, _: None = Depends(authorize)):
        try:
            validate_execution_manifest(manifest, ROOT)
            key = database.submit(manifest)
        except (ExecutionRejected, Conflict) as exc:
            raise HTTPException(409, str(exc)) from None
        return {"id": key, "state": database.get(key)["state"]}

    def lookup(run_id: str):
        try:
            return database.get(run_id)
        except KeyError:
            raise HTTPException(404, "Run not found") from None

    @app.get("/api/v1/runs/{run_id}")
    def run(run_id: str, _: None = Depends(authorize)):
        row = lookup(run_id)
        return {
            "id": row["id"],
            "state": row["state"],
            "error": row["error"],
            "manifest": json.loads(row["manifest"]),
            "result": json.loads(row["result"]) if row["result"] else None,
        }

    @app.post("/api/v1/runs/{run_id}/cancel")
    def cancel(run_id: str, _: None = Depends(authorize)):
        lookup(run_id)
        database.cancel(run_id)
        return {"id": run_id, "state": database.get(run_id)["state"]}

    @app.get("/api/v1/runs/{run_id}/package")
    def package(run_id: str, _: None = Depends(authorize)):
        row = lookup(run_id)
        manifest = RunManifest.model_validate_json(row["manifest"])
        results = (RunResult.model_validate_json(row["result"]),) if row["result"] else ()
        for result in results:
            for episode in result.episodes:
                try:
                    database.artifact(episode.raw_artifact_sha256)
                except (KeyError, Conflict):
                    raise HTTPException(409, "Evidence artifact missing or corrupt") from None
        package = RecoveryPackage(manifests=(manifest,), results=results)
        return Response(
            package.canonical(),
            media_type="application/json",
            headers={
                "ETag": '"' + package.digest() + '"',
                "Content-Disposition": 'attachment; filename="morph-evidence.json"',
            },
        )

    @app.get("/api/v1/runs/{run_id}/bundle")
    def bundle(run_id: str, _: None = Depends(authorize)):
        row = lookup(run_id)
        manifests = (RunManifest.model_validate_json(row["manifest"]),)
        results = (RunResult.model_validate_json(row["result"]),) if row["result"] else ()
        try:
            content = export_bundle(RecoveryPackage(manifests=manifests, results=results), database)
        except (KeyError, ValueError):
            raise HTTPException(409, "Incomplete or invalid evidence bundle") from None
        return Response(
            content,
            media_type="application/zip",
            headers={"Content-Disposition": 'attachment; filename="morph-evidence-v1.zip"'},
        )

    return app
