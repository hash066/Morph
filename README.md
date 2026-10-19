# Morph

Simulation-first recovery investigation for the SO-101 vial-placement task.
Current delivery is a tested orchestration/evidence core and a pinned feasibility spike.
**No recovery performance or live Nebius execution has been demonstrated.** See docs/STATUS.md.

## Local setup

Use Python 3.11 and uv 0.11.8. Run from E:/Winter/Morph (or a fresh checkout root):

```powershell
uv sync --locked --python 3.11
uv run python -m morph status
uv run pytest --cov=morph --cov-report=term-missing
uv run ruff check src tests
uv run mypy
uv build
```

Run the authenticated local API after setting a random MORPH_API_TOKEN of at least 32 characters:

```powershell
uv run uvicorn morph.api:create_app --factory --host 127.0.0.1 --port 8091
```

API requests require `Authorization: Bearer <MORPH_API_TOKEN>`. OpenAPI is at /docs.
Default storage is data/morph.sqlite; no secrets or runtime data are tracked. Jobs submitted
through the API currently receive a truthful 409 until simulation feasibility is verified.
No automatic GPU provisioning, training, model call or hardware motion occurs on startup.
React UI is deferred under the lead assignment's explicit feasibility gate.

## Simulator spike

Pinned source and exact transitive lock are in environments/. The tutorial is independently
licensed; fetch its pinned commit rather than tracking main. From this project root:

```powershell
$env:GIT_LFS_SKIP_SMUDGE='1'
git clone https://github.com/isaac-sim/IsaacLabTutorial.git vendor/IsaacLabTutorial
git -C vendor/IsaacLabTutorial checkout 9a4286b4bc8a5720ac97f87e5e0140f7542c22d9
pwsh -NoProfile -File scripts/setup_simulator.ps1
uv run python scripts/simulator_smoke.py
```

The smoke runner uses one environment, zero actions, 100 steps and a 180-second timeout.
It records return code, command, duration and lock hash. A zero-action test is NOT a trained
baseline, repeated failure, recovery or Nebius execution. Check LFS asset availability before
interpreting a failure; fetch only the pinned repository's required assets. Training is not launched
automatically. No checkpoint is included.

## Nemotron

The actual HTTP adapter is src/morph/planner.py. It uses Nebius Token Factory, checks the account
catalog, accepts only a typed candidate ID, and never evaluates model code. To check an existing
account without inference:

```powershell
uv run python -m morph provider-check --authorization data/credit-authorization.json
```

Set NEBIUS_API_KEY through the process environment. Authorization fields are documented by
CreditAuthorization: account reference, hashed operator authorization, expiry, approved credits,
inference cap, verified token rates, exact NVIDIA Nemotron model ID and official endpoint region.
Do not invent balances/rates or paste keys into JSON. A bounded live Nemotron 3 Super
planner call is verified in docs/verification/nebius-live-planner.json; it correctly
returned insufficient evidence when no simulation observations were supplied.
The documented cookbook model is only a candidate; /models must confirm account availability.

The caller invokes Nemotron.propose with development-only Observation records, a bounded
candidate registry and attempted IDs. Worst-case inference cost is reserved durably before POST;
failed/uncertain calls retain reservations and are not retried automatically. Live model output
must pass the same validators as mock-transport tests.

## Evidence boundaries

Contracts reject unknown fields and nonfinite numbers. Frozen protocol cases prevent canonical
start overlap across splits. Evaluation compares exact paired coverage with an unchanged
checkpoint/evaluator, records missing episodes, and refuses fixture-derived recovery claims.
Inference overhead belongs in RunResult wall time/cost. Per-condition reports avoid pooling an
unrecoverable case. The confidence bound assumes independent cases; canonical repeats are rejected.

SQLite queue leases, cancellation, explicit failure and interrupted states survive restarts.
Reservations are intentionally not refunded automatically. Artifact bytes are content-addressed.
This is a single-user local core; it is not a hosted multi-tenant service or an OS sandbox.

Remaining implementation after runtime access: actual per-seed worker, controller sensitivity,
perturbation readback, trained baseline, Nebius job integration, full investigate/evaluate loop,
React replay workbench, real browser evidence, held-out benchmark and complete artifact bundle.
See docs/BUILD_CONTRACT.md, docs/INTERFACES.md, docs/EVIDENCE.md and docs/DEMO_RUNBOOK.md.

## Key entry helper

`scripts/configure_nebius_key.ps1` prompts using Read-Host -AsSecureString and writes only
Windows DPAPI ciphertext to ignored data/nebius-key.dpapi. It never prints or stores plaintext.
`scripts/check_nebius_models.ps1` decrypts only in process memory for a read-only model catalog
request; it prints only matching model IDs and redacted status. This does not verify credits or
perform inference. Do not paste the key into chat, shell commands, authorization JSON or logs.


