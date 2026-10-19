# Morph status — 20 October 2026

Implementation started in E:/Winter/Morph only. This is a working, locally tested core;
the full recovery product and first live gate are not complete.

| Capability | State | Evidence |
|---|---|---|
| Tutorial source/dependency pin | PASS: lock resolves; local zero-action smoke passed | environments/simulator-pin.json |
| Source/asset provenance | PASS: required workshop LFS assets fetched; hashes recorded | environments/source-provenance.json |
| Core immutable schemas | IMPLEMENTED / LOCALLY TESTED | src/morph/contracts.py |
| Durable budget/queue/artifact store | IMPLEMENTED / LOCALLY TESTED | src/morph/store.py |
| Nemotron HTTP adapter | LIVE VERIFIED: strict Super-model proposal validated; failures retained | docs/verification/nebius-live-planner.json |
| Paired comparison/development selection | IMPLEMENTED / UNIT TESTED | src/morph/evaluation.py, protocol.py |
| Authenticated API | IMPLEMENTED / LOCALLY TESTED: real evidence endpoints and frozen-stack development job admission | src/morph/api.py |
| Restartable experiment worker | LIVE LOCAL VERIFIED: authenticated API accepted a frozen-stack job; durable worker ran the real simulator, validated and stored one successful safe episode plus content-addressed artifact in 106.97s | docs/verification/worker-e2e.json |
| Package verification | PASS: 43 tests; mypy and Ruff pass; scoped deterministic-core coverage 91.74% | docs/verification/ |
| GitHub CI | PASS: Python core, coverage gate, package build, and React production build on commit ed8b89d | https://github.com/hash066/Morph/actions |
| Local simulator installation | PASS: 157 packages installed; 100-step smoke passed | docs/verification/simulator-install-local-temp.log |
| Baseline/recovery simulation | PASS: official 800-iteration seed-42 PPO training completed; final model-799 nominal audit passed 8/8 with no aborts, timeouts, or unsafe rack contacts | docs/verification/baseline-model799-audit.json |
| Perturbation and development recovery | PASS: 1.5x actuator drift reproduced 3/8 failure; controller compensation, Nemotron balanced-75, and matched random candidate each passed 8/8 development starts | docs/verification/frozen-protocol.json |
| Frozen held-out pilot | COMPLETE / INCONCLUSIVE: baseline 4/8; Morph 8/8 with 0 unsafe; random 8/8 with 1 unsafe. Point gain +50 pp; n=8 interval crosses zero | docs/verification/heldout-summary.json |
| Independent confirmation | PASS: preregistered new starts 80..119; baseline 15/40 with 13 unsafe; Morph 39/40 with 1 unsafe; paired gain +60 pp, conservative 95% interval [0.171, 1.0] | docs/verification/confirmation-summary.json |
| Evidence export | PASS: deterministic 106,147-byte confirmation bundle with content-addressed episode artifacts and checksums | dist/morph-confirmation-evidence-v1.zip |
| Auditable simulator runner | IMPLEMENTED / LOCALLY TESTED: fixed command, bounded starts, checkpoint/condition/action readback | src/morph/isaac_runner.py |
| Nebius compute | BLOCKED: no verified project credits/quota/rates | environments/COMPUTE_GATE.md |
| Live Nemotron inference | PASS: operator authorized $30 maximum; internal ledger capped at $1; 6 measured calls cost $0.00288942 total; real evidence-driven experiment selected | docs/verification/nebius-live-summary.json |
| React workbench/browser evidence | IMPLEMENTED / BROWSER TESTED: authenticated investigation, experiment comparison, and evidence views load real API evidence; responsive navigation verified | web/, docs/verification/heldout-summary.json |
| Hardware | DISABLED: no supervised approved setup | no motion adapter exists |
| Usability/buyer evidence | NOT PERFORMED; blank protocol ready | docs/STUDY_PROTOCOL.md |

Terminal opened for hidden key entry and Windows-account-encrypted local storage. No key was
received in chat or printed. The user then authorized up to $30 of existing Token
Factory credits. This does not establish Nebius AI Cloud GPU quota.

Still required: final video recording/upload and Devpost submission by the authorized entrant.
Nebius AI Cloud execution remains
unavailable without a cloud project; real Token Factory inference is verified.

No simulated performance numbers, fake trajectories, cloud completion or participant outcomes.
Proposed controller multipliers remain exploratory limits, not validated recovery bounds.




