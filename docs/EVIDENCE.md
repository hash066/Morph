# Evidence ledger — 19 October 2026

## Observed environment
- Project root verified by git rev-parse: E:/Winter/Morph.
- GPU: NVIDIA GeForce RTX 3050 Laptop GPU, 4096 MiB, driver 581.80.
- Python 3.11.9 for Morph; Python 3.12.8 discovered for tutorial; uv 0.11.8.
- Only CUDA_PATH/CUDA_PATH_V13_0 among relevant environment variable names. No Nebius/Nemotron key exposed. Values were not printed and unrelated credential stores were not read.
- Nebius CLI not found on PATH. No authenticated credit/quota check is possible from available access. No provisioning or purchases performed.

## Upstream source
Official tutorial: https://isaac-sim.github.io/IsaacLab/develop/source/setup/tutorial.html
Repository: https://github.com/isaac-sim/IsaacLabTutorial
Checked-out commit: 9a4286b4bc8a5720ac97f87e5e0140f7542c22d9.
Lock copied verbatim and SHA-256 recorded in environments/simulator-pin.json.
`uv sync --project vendor/IsaacLabTutorial --locked --dry-run --python 3.12 --no-python-downloads`
passed: 201 packages resolved, 157 planned installs. Dry resolution is not runtime success.
Full locked installation attempted; outcome to be recorded below.
Source license Apache-2.0. Git LFS smudge disabled during clone; assets require explicit LFS retrieval
before baseline acceptance. Reset dataset is an ordinary Git blob per upstream .gitattributes.
No trained policy checkpoint supplied or downloaded. No checkpoint provenance can be claimed.

Source inspection: arm_action scale 0.033 rad, gripper_action scale 0.02 rad in nominal preset.
play_mode resets nominal mass to 0.020 kg and friction to 0.7, so naive pre-play perturbation
overrides may be erased. Do not assert a perturbation took effect until resolved config confirms it.
The external evaluator outputs SO101_EVAL_RESULT and per-episode reset rows/poses when
SO101_EVALUATION_OUTPUT is set. Default audit repeats 128 canonical starts eight times.
Seeds alone do not establish independent initial conditions. Morph's protocol disallows repeated
condition/start pairs and split overlap. Exact split application to the runtime is still unimplemented.
Upstream per-episode records lack all Morph abort/safety/time fields; raw summary import alone
must not be promoted into a complete Morph EpisodeResult.

Requirements: https://isaac-sim.github.io/IsaacLab/develop/source/setup/installation/index.html
CUDA 13 build minimum driver is 580.88 Windows / 580.65.06 Linux. Local driver clears minimum.
Full Isaac Sim 16 GiB VRAM guidance must not be misapplied as a Newton requirement; 4 GiB Newton
feasibility is untested. Nebius GPU, Linux driver, toolkit and headless rendering remain unverified.

## Provider interface
https://docs.tokenfactory.nebius.com/quickstart
https://github.com/nebius/token-factory-cookbook/blob/main/models/nemotron/nemotron3-nano-30b.md
Official cookbook documents nvidia/nvidia-nemotron-3-nano-30b-a3b and structured output/function
calling. This is a documented candidate, NOT verified account availability. Runtime adapter
requires an explicit model and verifies /models before inference. It allows only official regional
HTTPS endpoints, forbids redirects, bounds output and persists worst-case reservation before POST.
Rates/credit proof and expiry come from operator account evidence; no assumed free tier.
Mock transport tests are not live-provider evidence.

## Rules checked
https://nebiusglobalaihackathon.devpost.com/rules
Submission deadline 30 October 2026 10:00 PDT / 22:30 IST. Video should be under three minutes;
Physical AI includes at least one minute of hardware operating or application modules if no hardware.
Current code is not yet eligible evidence of an operating complete simulation product.

## Verification
Pending final local test/build/type/lint report in docs/verification/core.txt.
No tests or fixtures constitute measured simulation performance.

## Local core verification completed
32 tests passed, 86.75% line coverage. Mypy checked eight source files with no issues.
Ruff check passed; wheel and source distribution built. Exact output is in docs/verification/.
Tests exercise fixtures and mock HTTP; they do not establish simulator or live-provider success.

## Simulator installation attempt
Initial locked installation failed while extracting Torch 2.11.0+cu130 because the default
uv cache on C: ran out of disk space (Windows error 112). C: had 0.68 GiB free at inspection.
E: had 207.29 GiB free. Retried with UV_CACHE_DIR=E:/Winter/Morph/data/uv-cache and
UV_LINK_MODE=copy; output captured in docs/verification/simulator-install.log.
Required workshop assets were fetched using a scoped Git LFS include (media excluded).
Source, evaluator, reset dataset and asset hashes recorded in environments/source-provenance.json.

## Credential entry
At the user's request, opened an interactive hidden-input PowerShell prompt. The helper uses
SecureString and Windows DPAPI to save ciphertext under ignored data/, never plaintext.
No key was yet present when last checked. The read-only catalog probe does not infer credit
availability and suppresses credential-bearing response/error bodies.

## Authenticated provider catalog verified
User entered the key through hidden terminal input. Existing Windows DPAPI ciphertext was
successfully decrypted only in memory; no key printed or sent to the model context.
Read-only GET https://api.tokenfactory.nebius.com/v1/models succeeded on 19 October.
Exact account-visible IDs are in docs/verification/nebius-model-catalog.json, including
nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B (case differs from the older cookbook example).
This verifies authentication/model listing only. No completion call, credit balance, quota,
GPU execution or spend verification has occurred. Live inference remains gated.
The legacy Windows PowerShell encryption-module issue was avoided by using direct .NET DPAPI;
a round-trip test with a nonsensitive sentinel passed. Helper supports the existing ciphertext.

## Final core package checks
35 tests passed, 86.88% coverage; nine source files pass mypy. Ruff and wheel/sdist build pass.
Added deterministic ZIP evidence bundles with per-file hashes, immutable raw artifacts, and
recomputed report validation. No fabricated results included in any exported package.

Browser access check: the available Codex browser opened Token Factory's public logged-out
page, not an authenticated billing console. Closed the temporary tab. Existing credit balance
and Nebius GPU quota therefore remain unverified despite a valid inference API key.

## Build-temp disk correction and final regression check
The source wheel builder uses Python tempfile independently of UV_CACHE_DIR. Its temporary
staging filled C: further (0.08 GiB free). Terminated only this installation's uv process tree.
Verified its exact staging directory (created during this attempt, containing src/isaaclab) and
moved that task-created tree into data/interrupted-isaaclab-wheel-ov4kb3a4 to restore C: space.
No unrelated temporary directories were moved/deleted. Retried with TEMP, TMP and UV_CACHE_DIR
all scoped under E:/Winter/Morph/data; cached Torch download is reused. Reproduction helper:
scripts/setup_simulator.ps1. Latest output: simulator-install-local-temp.log.

Final regression suite: 36 passed, 86.77% coverage. Preserves environment task-success and
safety/abort flags independently; refuses selection when success increases alongside safety
violations. Mypy, Ruff, wheel/sdist build pass. Package-content audit confirms no data/, vendor/,
.venv/, .env or DPAPI credential files inside built distributions.

## Locked simulator installation succeeded
With cache and TEMP/TMP on E:, pinned Isaac Lab wheel built in 6m52s and 157 packages
installed in 2m19s. Command exited 0. Exact output: simulator-install-local-temp.log.
This establishes installation only. Started scripts/simulator_smoke.py: one environment,
100 zero-action steps, 180-second timeout, E:-scoped temp/kernel caches, provider keys removed
from simulator child environment. Runtime outcome recorded separately, never inferred from install.

## Smoke attempt 1 and corrected retry
First zero-agent attempt hit the 180-second timeout (returncode 124) during asset startup;
no completed rollout or episode result. Preserved simulator-smoke-attempt1.log/.json.
Source inspection found checkpoint-free agents default to newton_gl and do not expose a
--seed argument. Verified supported launcher value --visualizer none and Hydra env.seed override.
Retry uses --visualizer none, env.seed=42 and PYTHONUNBUFFERED=1, with the same 100-step and
180-second limits. This corrects headless/seed setup without changing the task or success criterion.

## Cold-start budget adjustment
The seeded headless attempt also timed out at 180 seconds, after creating the one-environment
scene on cuda:0 and starting kernel compilation. Preserved attempt2 log/manifest. Warp cache
contained newly generated SM86 PTX files with timestamps during that run, including articulation
ordering and Newton asset kernels. This is startup progress, not a completed rollout.
A third attempt uses an explicit 600-second cold-start allowance with the SAME task, seed 42,
headless backend and 100-step limit. Both prior failures remain counted in the evidence ledger.
The smoke runner accepts a bounded timeout (1–900 seconds) and defaults to 180.

## Saved key authentication confirmed
The saved Windows-account-encrypted key returned the model catalog. A separate GET to
the same endpoint without Authorization returned HTTP 401, confirming the catalog requires
authentication. Five Nemotron model IDs were available. No inference or cloud compute was
started; credit balance and GPU quota remain unverified. No plaintext key was logged.

## Local runtime smoke passed
Third bounded attempt exited 0 after 320.063 seconds within its 600-second allowance.
The pinned IsaacTutorial-Place-Vial-SO101 environment initialized on cuda:0 with seed 42,
headless newton_mjwarp, and completed the 100-step zero-action smoke. See
docs/verification/simulator-smoke.json and simulator-smoke.log. Prior two startup
timeouts remain preserved. This verifies local runtime only: no trained baseline,
recovery result, policy success rate, paid inference or cloud job was evaluated.

## Tutorial validation and capacity benchmark
The exact pinned tutorial test suite passed 95 tests on 2026-10-19; two optional
deployment/export tests were skipped because cv2 and LEAPP extras are not installed.
The state-task runtime benchmark then completed with the official 4,096-environment
batch: 12,095 environment steps/s, 73.2% mean GPU utilization, and 1.60 GB peak GPU
memory on the local RTX 3050 Laptop GPU. This is a capacity result, not policy evidence.

## Baseline training started
The official state-policy PPO command is running locally with 4,096 environments,
800 iterations, seed 42, headless newton_mjwarp, and the pinned tutorial lock. The
first checkpoint is preserved at model_0.pt. Early training metrics are not baseline
evaluation and are not used as recovery evidence. The local projected runtime is much
longer than the tutorial's published RTX 6000 Ada reference, so a faster cloud run
remains gated on verified Nebius project credits, quota, rates, and an approved cap.

## Auditable condition runner
Morph now has a constrained Isaac audit adapter that fixes the task, backend and
environment-owned evaluator; scopes temp/cache paths; removes provider secrets from
the child process; selects disjoint canonical reset ranges; applies only validated mass
and controller-scale fields; and rejects checkpoint, reset-row, perturbation or action
readback mismatches. Its command construction and bounds are covered by tests. No
recovery result is claimed until the real checkpoint and audits complete.

## Live Nebius Nemotron integration
The user authorized at most USD 30 of existing Token Factory credits attached to the
saved key. Morph uses a separate USD 1 durable inference ledger. Three bounded calls
were made: Lightning exhausted its output limit and was rejected; Nano returned an
invalid proposal shape and was rejected; Super returned a schema-valid
`insufficient_evidence` refusal because no simulation observations were supplied.
Measured aggregate cost was USD 0.00099072. Failed reservations remain consumed and
were not retried automatically. No raw provider response, API key, synthetic simulator
observation, or recovery claim was stored. The validated proposal, token counts,
latency, prompt/response hashes, pricing and model ID are preserved under
docs/verification. This satisfies the real Token Factory runtime-call requirement but
does not substitute for the later observation-driven recovery experiment.

## Model-50 exploratory audit
The first scheduled intermediate checkpoint audit exercised the complete Morph callback
against eight canonical nominal starts with mass 0.020 kg, arm scale 0.033, jaw scale
0.020, seed 42 and the unchanged tutorial success criterion. It completed in 582.109
seconds with 0/8 successes, 0 aborts, 8 timeouts and 0 unsafe rack contacts. The exact
condition/action readback and per-episode rows are in
docs/verification/baseline-model50-audit.json. Morph rejects this immature checkpoint as
a baseline and keeps training. This result is not pooled with later checkpoint audits.

## Completed baseline and nominal acceptance
The pinned seed-42 PPO run completed all 800 scheduled iterations in 25,775.27 seconds.
All checkpoints and the full training log are preserved locally; model_799.pt has SHA-256
`5ec3622d81ed3f9210c3da8aa2cf1b70a661f6b13998de396fda4ccf324ec10d`.
The final fixed-evaluator audit passed 8/8 canonical nominal starts with zero aborts,
timeouts, or unsafe rack contacts. Completion times ranged from 6.87 to 8.67 seconds.
Exact runtime parameters and episode rows are in
docs/verification/baseline-model799-audit.json. Earlier failed checkpoint audits remain
preserved and are not pooled into this accepted baseline.

## Initial feasible perturbation probe
The maximum schema-allowed vial mass, 0.030 kg, was applied with unchanged controller
scales to the same eight development starts. All 8/8 episodes still passed with no
aborts, timeouts, or unsafe rack contacts. This is a robustness observation, not the
required failure and not a recovery claim. Morph will probe other validated physical
conditions or tighten the bounded perturbation definition before candidate selection.
Evidence: docs/verification/perturbation-mass030-audit.json.

## Repeatable failure and development recovery
A bounded 1.5x actuator-calibration multiplier produced a meaningful failure on the eight
development starts: 3/8 successes, five timeouts, and one unsafe rack contact. Applying a
two-thirds controller-scale compensation restored 8/8 with no unsafe contacts, validating
that the allowed controller parameters materially affect the outcome. Live Nemotron then
selected balanced_75 from the real development observations. It passed 8/8 in 6.60 seconds
mean completion time. A deterministic random-seed-42 selection, arm67_jaw80, also passed
8/8, with 7.78 seconds mean completion time. No superiority claim is made before held-out
evaluation. The evaluator hash, development starts, held-out starts 64..71, condition,
candidate selections, and one-shot policy were frozen before held-out execution in
docs/verification/frozen-protocol.json.
