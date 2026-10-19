# Morph: start implementation

Work in E:/Winter/Morph. Read AGENTS.md first, then docs/ARTIFACT_INDEX.md and docs/PRODUCT_PLAN.md. This directory is the sole project root even if your Codex task is attached to the parent E:/ project.

Use all copied artifacts according to their precedence. Use the verified local ECC guidance selectively. The owner requests no new paid resources: honor the exact cost constraints in AGENTS.md. Maintain docs/STATUS.md so progress is easy to inspect.

Execute the lead assignment below. The specialist prompts and shared contract in docs/artifacts are available when useful. Continue into implementation after establishing the interfaces; do not stop after writing another plan. Record access blockers without pretending live gates passed.

## Lead assignment

Build MORPH for the Nebius x NVIDIA hackathon: a simulation-first workbench that investigates a repeatable robot-task failure, selects bounded recovery experiments, runs them on Nebius GPU compute and produces a reproducible evidence package. Implement it; do not stop at a dashboard mockup or architecture document.

Read the specification:
E:/Winter/Morph/docs/artifacts/morph-simulation-and-hardware-plan.pdf
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
