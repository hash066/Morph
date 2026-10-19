# Interfaces v1

Immutable Pydantic contracts live in src/morph/contracts.py. Unknown fields and nonfinite
numbers are rejected. Collections are tuples, not mutable lists/dicts. JSON manifests are
content-addressed; SHA-256 identifies exact bytes of canonical sorted JSON.

RunManifest binds task/provenance, candidate, opaque condition, seed allocation, split,
method, evaluator hash and budget. Perturbation is evaluator-private. Planner receives only
Observation records; it never receives manifests, perturbations, held-out IDs or raw text logs.
Candidates select a prevalidated registry ID; no arbitrary code, paths or controller keys.

SQLite transactions own job state and resource reservations. States: queued, running,
succeeded, failed, cancelled, interrupted. Leases expire into interrupted, never automatic
retry: an interrupted GPU job may still consume credit. Manual new submissions require a new
reservation. Result completion is compare-and-swap against the active lease.

API is localhost-only, bearer protected using MORPH_API_TOKEN (minimum 32 characters).
GET /api/v1/status, GET /api/v1/runs, POST /api/v1/runs,
GET /api/v1/runs/{id}, POST /api/v1/runs/{id}/cancel, GET /api/v1/runs/{id}/package.
Submission stores blocked work as an explicit error until the simulator gate is verified.
OpenAPI documents schemas. No upload, shell, provisioning or motion endpoint exists.

Evaluation includes all scheduled cases, treats absent results as incomplete, rejects duplicate
or unpaired case IDs and mixed provenance. Candidate selection is development-only.
Held-out comparisons require exact paired coverage and identical evaluator/task/checkpoint.
A package is evidence, never physical deployment approval.
