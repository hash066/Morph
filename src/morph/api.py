from __future__ import annotations

import json
import os
import secrets
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from fastapi.responses import Response

from morph.contracts import Budget, RecoveryPackage, RunManifest, RunResult
from morph.evidence import export_bundle
from morph.store import Conflict, Store


def create_app(store: Store | None = None, token: str | None = None) -> FastAPI:
    access_token = token or os.environ.get("MORPH_API_TOKEN", "")
    if len(access_token) < 32:
        raise RuntimeError("Set MORPH_API_TOKEN to a random secret of at least 32 characters")
    database = store or Store(
        Path("data/morph.sqlite"), Budget(rollouts=100, wall_seconds=3600, gpu_hours=0, cost_usd=0)
    )

    def authorize(authorization: Annotated[str | None, Header()] = None):
        if not secrets.compare_digest(authorization or "", "Bearer " + access_token):
            raise HTTPException(401, "Bearer authorization required")

    app = FastAPI(title="Morph", version="0.1.0", dependencies=[Depends(authorize)])

    @app.get("/api/v1/status")
    def status():
        provider_verified = Path("docs/verification/nebius-live-planner.json").is_file()
        return {
            "mode": "Simulation",
            "simulation_gate": "blocked",
            "reason": "Baseline training active; recovery and controller sensitivity not yet verified",
            "hardware": "disabled",
            "provider": "live_verified" if provider_verified else "not_live_verified",
        }

    @app.get("/api/v1/runs")
    def runs(limit: Annotated[int, Query(ge=1, le=100)] = 100, offset: Annotated[int, Query(ge=0)] = 0):
        return {"data": database.list(limit, offset)}

    @app.post("/api/v1/runs", status_code=201)
    def submit(manifest: RunManifest):
        # Deliberate gate: source inspection alone cannot authorize candidate execution.
        raise HTTPException(409, "Simulator baseline and candidate sensitivity gate not verified")

    def lookup(run_id: str):
        try:
            return database.get(run_id)
        except KeyError:
            raise HTTPException(404, "Run not found") from None

    @app.get("/api/v1/runs/{run_id}")
    def run(run_id: str):
        row = lookup(run_id)
        return {
            "id": row["id"],
            "state": row["state"],
            "error": row["error"],
            "manifest": json.loads(row["manifest"]),
            "result": json.loads(row["result"]) if row["result"] else None,
        }

    @app.post("/api/v1/runs/{run_id}/cancel")
    def cancel(run_id: str):
        lookup(run_id)
        database.cancel(run_id)
        return {"id": run_id, "state": database.get(run_id)["state"]}

    @app.get("/api/v1/runs/{run_id}/package")
    def package(run_id: str):
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
    def bundle(run_id: str):
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
