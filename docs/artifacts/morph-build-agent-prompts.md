# Morph: copy-ready build prompts

Use the shared specialist contract in `agent-prompts-start-here.md`. The task is a measured recovery tool, not unrestricted robotic control.

## Lead agent prompt

```text
Build MORPH for the Nebius x NVIDIA hackathon: a simulation-first workbench that investigates a repeatable robot-task failure, selects bounded recovery experiments, runs them on Nebius GPU compute and produces a reproducible evidence package. Implement it; do not stop at a dashboard mockup or architecture document.

Read the specification:
C:/Users/asus/Documents/Codex/2026-10-03/https-nebiusglobalaihackathon-devpost-com-ref-content/outputs/morph-simulation-and-hardware-plan.pdf
If on another machine, use the attached PDF or request it. Do not assume inaccessible contents.

Use a fresh project workspace. Read applicable instructions and selected ECC skills at D:/Leave/EL/AIML/third_party/ECC: eval-harness, python-testing, api-design and verification-loop. Read each complete skill when applying it. Use agent-security-hardening at tool boundaries. Follow the prompt-pack guide's compatibility cautions; do not install global ECC hooks or change the host's model automatically.

Begin with the current official supported Isaac Lab SO-101 task and its actual compatible backend. Verify official docs and pin a reproducible commit/dependency set. Do not mix legacy Isaac Sim instructions with a tutorial using a different backend. Confirm driver, CUDA, container and headless rendering requirements on available Nebius GPU compute. A stable VM is acceptable before Serverless Jobs. Record exact environment and licensing/provenance.

Use an actually available NVIDIA Nemotron model through Nebius Token Factory for hypothesis generation and constrained experiment selection. Verify model ID and capabilities. Isaac Lab alone is not the required NVIDIA open-model integration. GR00T is optional only if a supported policy/embodiment/checkpoint works; Cosmos is unnecessary unless an evaluated visual-domain use case needs it.

First 48-hour gate: reproduce a baseline rollout; produce a meaningful, repeatable failure under a feasible perturbation; run one bounded candidate experiment; complete a real Nebius execution and Nemotron call. If the supported environment or recovery space cannot be made functional, report the precise evidence and recommend stopping before building more UI. Do not fake a trajectory or alter success criteria to create a recovery story.

Use Python for the simulation/experiment backend, a small typed web API and React/TypeScript for the workbench unless the actual environment justifies another choice. Create docs/BUILD_CONTRACT.md, docs/INTERFACES.md, docs/STATUS.md and docs/EVIDENCE.md. Define immutable TaskConfig, Perturbation, Candidate, RunManifest, EpisodeResult, EvaluationReport and RecoveryPackage schemas. The lead owns shared schemas, dependency locks, migrations and integration. Give each specialist an exclusive component boundary before parallel edits.

Limit the first product to one embodiment, one task and a small verified parameter space. Parameters must actually affect the controller. Keep injected fault labels hidden from the planner. Nemotron receives allowed observations and historical results, proposes typed experiments and explains uncertainty. Deterministic validators enforce action bounds and budgets. No arbitrary model-generated Python/shell execution, evaluator edits or raw hardware commands.

Implement baseline, matched-budget simple search and Morph methods. Freeze development/held-out splits and evaluator before final evaluation. Track seed-level results, success denominator, failures, aborts, wall-clock time, GPU-hours and inference cost. Include overhead when comparing methods. Build a refusal/escalation path when no eligible recovery is found. The agent cannot approve its own physical deployment.

Workbench: select a failing run -> inspect replay/telemetry -> investigate -> see real experiment queue -> inspect candidate results -> compare held-out results -> export a versioned evidence package. Use real job states. Clearly distinguish Simulation, Recorded replay and Physical trial. Do not label a prerecorded run live.

Optional hardware must be gated by a compatible robot, calibration, bounded actions, supervised operation and explicit operator approval. No hardware motion should occur merely from launching the app or asking the model a question. If hardware is unavailable, complete the eligible simulation-first product and accurately document the limitation. User studies are workflow evidence, not robot robustness evidence.

Deliver locked setup, container/compute configuration, budget caps and cancellation, dataset/checkpoint provenance, restartable jobs, artifact storage, CI, meaningful tests, reproducible experiment commands, browser evidence and a truthful demo runbook. Prepare but do not fabricate three-engineer usability sessions and two-buyer interviews. Never upload participant data or contact partners without actual authorization.

Use current official hackathon rules for packaging. Prepare a sub-three-minute video with at least a minute of operating modules for the simulation-only path. Do not claim superiority unless the comparison supports it. If Morph loses to simple search, report that and measure whether operator effort provides genuine value instead. Continue independent work around precise external blockers; do not mark blocked live or hardware gates passed.
```

## M1 — Simulation and task infrastructure

```text
Own sim/ and environments/. Use ECC python-testing and verification-loop; use official pinned simulator/task docs for robotics specifics.

Reproduce the supported SO-101 task and baseline on compatible NVIDIA GPU compute. Save full versions, seed, policy/checkpoint provenance, configuration, video and evaluator result. Add mild feasible perturbations without changing embodiment, reward and observations simultaneously. Separate recoverable and intentionally unrecoverable conditions.

Define a small controller parameter space with verified numerical bounds and units. Demonstrate that candidate settings actually influence the task. Preserve the environment-owned success definition; object proximity alone must not substitute for correct placement/release. Export telemetry sufficient to diagnose timing, error and slip where available. Keep ground-truth fault labels out of planner-visible records.

Provide headless worker entrypoints, deterministic configuration serialization, seed handling, timeouts, cancellation and artifact output. Test job interruption and resumption. State any nondeterminism rather than promising identical GPU trajectories. Hand off a real baseline and repeatable failure, not a hardcoded animation.
```

## M2 — Recovery agent and experiment orchestration

```text
Own planner/ and orchestration/. Use ECC api-design, cost-aware-llm-pipeline and agent-security-hardening.

Implement a real Nemotron adapter through Nebius Token Factory. Accept only bounded typed tools: inspect allowed telemetry, propose candidate, request evaluation, compare results and propose a recovery package. Reject arbitrary executable code, invalid ranges, evaluator changes, attempts to access hidden fault labels and attempts to command physical hardware.

Use durable job/manifests and immutable result history. Make repeated submissions idempotent and recover from worker/provider failure. Enforce iteration, rollout, time and spending caps. Expose actual task progress and errors to the UI. Record all planner calls and candidate lineage without leaking secrets or held-out data.

Implement stop conditions, insufficient-evidence responses and No validated recovery. Choose candidates on development data only. Final evaluation is invoked through a separate evaluator boundary. Test malformed model JSON, tool injection, out-of-range parameters, repeated candidates, missing artifacts and exhausted budgets. Model confidence must not become an unearned probability or deployment approval.
```

## M3 — Independent benchmark and evidence

```text
Own evaluation/ and evidence/. Use ECC eval-harness and python-testing. Read ECC agents/mle-reviewer.md for reproducibility and leakage review; treat it as guidance, not an automatic model or tool configuration.

Before results are known, define baseline, matched-budget random/CEM search and Morph comparison. Use the same parameter space and feasible conditions. Freeze development and held-out seed manifests. Proposed target: five development seeds per condition and twenty held-out seeds for each of three conditions per method. Record any reduction and its reason; never imply unperformed episodes occurred.

Keep the evaluator inaccessible to planner mutation. Report seed-level successes, counts/denominators, completion times, aborts, total simulation budget, GPU time and model cost. Include uncertainty and paired comparisons where appropriate. Prevent tuning on held-out outcomes. Include failure replays and a separately labeled unrecoverable case. Add one meaningful ablation of diagnosis-driven selection.

Export a machine-readable report and human-readable result page with exact reproduction commands and artifact hashes. Separate simulation performance, physical trials, workflow usability and buyer interviews. Provide blank study templates, not invented participant findings. If the method does not outperform the baseline, say so clearly.
```

## M4 — Workbench, integration and optional hardware

```text
Own apps/workbench and the hardware adapter only if the lead assigns it. Use ECC frontend-design-direction, e2e-testing and security-review. Keep hardware disabled by default.

Build the actual investigation workflow: failing-run selection, telemetry/replay, hypotheses, candidate queue, real progress, comparison and evidence export. Show units, provenance, run IDs, status, failures and resource budget. Use an accessible technical interface with clear hierarchy; avoid a decorative robot animation as the main product. Verify loading, disconnected, empty, partial-result and failed-job states with browser tests and screenshots.

For hardware, first verify exact embodiment, calibration, sensing and action conventions with the qualified operator. Implement a separate armed execution boundary with joint/action limits, watchdog, stop mechanism, explicit configuration approval and audited trial records. Test validation without motion first. Do not transmit movement commands without scoped authorization and supervised setup. Unsupported hardware stays blocked rather than silently mapped.

Prepare baseline/after trial logging that counts all attempts and interventions. If no compatible robot is available, ship the complete simulation workflow with accurate labels. A participant opening the workbench is a usability test, not a physical trial. Hand off real browser traces and evidence paths.
```

## Final acceptance prompt

```text
Independently audit Morph from a clean environment against the build contract. Reproduce one baseline, one perturbed failure, one recovery candidate and the comparison report. Verify real Nebius compute and Nemotron traces. Inspect candidate bounds, job restart behavior, budget enforcement, hidden fault labels, seed split integrity and evaluator ownership.

Attempt to falsify the core claim: can simple search achieve the same result at equal budget, does the candidate actually affect control, and does reported success mean task completion? Report inconclusive or negative results honestly. Check that UI labels distinguish simulation, replay and physical operation. Confirm no hardware command can execute by default.

Fix authorized implementation defects and rerun affected tests. Produce PASS/FAIL/BLOCKED with commands, results and artifact links. Distinguish a reproducible simulator result from physical validation and user-study evidence. Prepare a truthful demo and an exact list of remaining external requirements. Do not manufacture performance gains to finish the project.
```
