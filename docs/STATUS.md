# Morph status — 19 October 2026

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
| Authenticated API | IMPLEMENTED / LOCALLY TESTED; launch gate closed | src/morph/api.py |
| Package verification | PASS: 41 tests; mypy and Ruff pass; prior measured coverage 86.77% | docs/verification/ |
| Local simulator installation | PASS: 157 packages installed; 100-step smoke passed | docs/verification/simulator-install-local-temp.log |
| Baseline/recovery simulation | PASS: official 800-iteration seed-42 PPO training completed; final model-799 nominal audit passed 8/8 with no aborts, timeouts, or unsafe rack contacts | docs/verification/baseline-model799-audit.json |
| Perturbation and development recovery | PASS: 1.5x actuator drift reproduced 3/8 failure; controller compensation, Nemotron balanced-75, and matched random candidate each passed 8/8 development starts | docs/verification/frozen-protocol.json |
| Auditable simulator runner | IMPLEMENTED / LOCALLY TESTED: fixed command, bounded starts, checkpoint/condition/action readback | src/morph/isaac_runner.py |
| Nebius compute | BLOCKED: no verified project credits/quota/rates | environments/COMPUTE_GATE.md |
| Live Nemotron inference | PASS: operator authorized $30 maximum; internal ledger capped at $1; measured spend $0.00099072 | docs/verification/nebius-live-summary.json |
| React workbench/browser evidence | DEFERRED by explicit feasibility gate | BOOTSTRAP.md |
| Hardware | DISABLED: no supervised approved setup | no motion adapter exists |
| Usability/buyer evidence | NOT PERFORMED; blank protocol ready | docs/STUDY_PROTOCOL.md |

Terminal opened for hidden key entry and Windows-account-encrypted local storage. No key was
received in chat or printed. The user then authorized up to $30 of existing Token
Factory credits. This does not establish Nebius AI Cloud GPU quota.

Still required: one-shot held-out evaluation under the frozen protocol, final matched comparison
and evidence package, real worker execution/cancellation, complete investigation loop, React
workbench/replays/browser evidence, and submission packaging. Nebius AI Cloud execution remains
unavailable without a cloud project; real Token Factory inference is verified.

No simulated performance numbers, fake trajectories, cloud completion or participant outcomes.
Proposed controller multipliers remain exploratory limits, not validated recovery bounds.




