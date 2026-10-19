from fastapi.testclient import TestClient

from morph.api import create_app


def test_api_auth_gate_empty_and_export(store, manifest):
    client = TestClient(create_app(store, "t" * 32))
    assert client.get("/api/v1/status").status_code == 401
    client.headers["Authorization"] = "Bearer " + "t" * 32
    assert client.get("/api/v1/status").json()["simulation_gate"] == "evaluated"
    summary = client.get("/api/v1/evidence/summary")
    assert summary.json()["morph_report"]["candidate_successes"] == 39
    assert client.get("/api/v1/evidence/audits/morph").json()["summary"]["unsafe_rack_contacts"] == 1
    assert client.get("/api/v1/evidence/audits/secret").status_code == 404
    assert client.get("/api/v1/runs").json() == {"data": []}
    assert client.post("/api/v1/runs", json=manifest.model_dump(mode="json")).status_code == 409
    assert store.list() == []
    key = store.submit(manifest)
    assert client.get(f"/api/v1/runs/{key}").json()["state"] == "queued"
    export = client.get(f"/api/v1/runs/{key}/package")
    assert export.status_code == 200
    assert export.json()["results"] == []
    assert export.json()["physical_deployment_approved"] is False
    assert "etag" in export.headers
    bundle = client.get(f"/api/v1/runs/{key}/bundle")
    assert bundle.status_code == 200
    assert bundle.headers["content-type"] == "application/zip"
    assert client.post(f"/api/v1/runs/{key}/cancel").json()["state"] == "cancelled"
    assert client.get("/api/v1/runs/missing").status_code == 404
    assert client.post("/api/v1/hardware/move", json={}).status_code == 404
