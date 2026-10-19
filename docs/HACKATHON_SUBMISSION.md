# Morph — hackathon submission draft

## Tagline
Evidence-first recovery experiments for robot failures, selected by Nemotron and verified before motion.

## Track
Physical AI. Morph is a simulation-first application with no submitted hardware component. The demo
must therefore show at least one minute of the key application modules operating.

## What it does
Morph turns a repeatable robot-task failure into a bounded, auditable recovery investigation. An
engineer opens the frozen failure, inspects evaluator-owned episode evidence, compares constrained
controller experiments, sees the Nemotron-selected candidate beside an equal-budget random candidate,
and exports a content-addressed evidence package. Morph never lets the model write evaluator code,
execute arbitrary commands, approve physical deployment, or inspect held-out outcomes while selecting.

## Nebius and NVIDIA use
Morph makes real runtime calls to NVIDIA Nemotron 3 Super through Nebius Token Factory. Nemotron sees
typed development observations and a validator-owned candidate registry, then selects only an eligible
experiment ID or refuses. Six measured calls cost USD 0.00288942 total. Provider responses, prompt and
response hashes, token counts, latency, model ID, pricing, and rejected attempts are retained. The robot
simulation ran locally; no Nebius AI Cloud execution is claimed.

## Measured result
- Nominal trained policy: 8/8 successes, zero unsafe contacts.
- Frozen actuator-drift failure: development 3/8; held-out 4/8 with two unsafe contacts.
- Nemotron-selected balanced-0.75: held-out 8/8, zero unsafe contacts, 6.56 s mean completion.
- Matched random candidate: held-out 8/8, one unsafe contact, 8.05 s mean completion.
- Paired point gain over the fault baseline: +50 percentage points for both candidates.
- The preregistered n=8 conservative interval crosses zero. Morph reports the result as inconclusive
  and does not claim statistically validated superiority.

## Technical stack
Python 3.11, FastAPI, Pydantic, SQLite, React, TypeScript, Vite, NVIDIA Nemotron 3 Super through Nebius
Token Factory, and the pinned NVIDIA Isaac Lab SO-101 tutorial task with Newton MJWarp. CI runs tests,
Ruff, mypy, coverage, package builds, dependency audit, and the React production build.

## Testing instructions
1. Clone the public repository and follow README.md.
2. Start the authenticated API on port 8091 with a random 32+ character local token.
3. Start `web` with `npm run dev`; enter the same token.
4. Inspect Investigation, Experiments, and Evidence. Counts and hashes come from committed frozen audits.
5. Optional simulator execution requires the pinned tutorial checkout, assets, compatible NVIDIA GPU,
   and the locked setup described in README.md. Judges can review the committed evidence without it.

## Repository and evidence
- Repository: https://github.com/hash066/Morph
- Frozen protocol: `docs/verification/frozen-protocol.json`
- Held-out summary: `docs/verification/heldout-summary.json`
- Evidence build: `uv run python scripts/build_real_evidence.py`
- Demo script: `docs/DEMO_RUNBOOK.md`

## Required submission actions not performed by automation
Record a sub-three-minute English demo with at least one minute of the workbench operating, upload it
publicly to YouTube, add the final video URL and public repository URL to Devpost, provide required
Nebius/NVIDIA feedback, and submit through the authorized entrant account before the deadline.
