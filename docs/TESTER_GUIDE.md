# Morph external tester guide

## Who to recruit

Recruit three workflow testers: one robotics or Isaac Lab engineer, one controls/automation
engineer, and one lab/manufacturing operator who reviews failure evidence. Recruit two buyer-side
reviewers: a robotics engineering manager, automation lead, lab operations manager, or systems
integrator responsible for approving simulation or commissioning work. Testers need no robot and
should not receive the Nebius API key.

## What Morph asks them to do

Give the tester the public repository and README. For a guided local review, start the API and
workbench yourself and provide only a temporary local `MORPH_API_TOKEN`. Ask the tester to:

1. Identify what changed in the failed task and state the failure rate.
2. Explain which measurements came from simulation and which claims remain disallowed.
3. Compare the Nemotron-selected and matched-random candidates for success, safety, and speed.
4. Interpret the confidence interval and `simulation_candidate` decision.
5. Locate the frozen protocol and evidence bundle hash.
6. Decide whether the evidence is sufficient to schedule another simulation experiment.

Do not ask testers to approve hardware deployment. Record participant IDs rather than names in
project artifacts. Obtain explicit consent before recording a session or publishing a quote.

## 25-minute session

- 0–3 min: consent, background, and unaided task brief.
- 3–13 min: unaided Investigation, Experiments, and Evidence workflow.
- 13–18 min: tester explains the result in their own words.
- 18–23 min: assisted retry and trust questions.
- 23–25 min: System Usability Scale-style rating and one most important improvement.

Record completion, active minutes, assistance, interpretation errors, simulation/physical
confusion, and whether the tester finds the evidence export reviewable. Keep failed attempts.

## Recruitment message — technical tester

> I built Morph, an open-source workbench that investigates a robot-task failure in Isaac Lab,
> uses NVIDIA Nemotron through Nebius Token Factory to select a bounded recovery experiment, and
> exports reproducible evidence. Could you spend 25 minutes testing whether the failure, comparison,
> and safety evidence are understandable? No robot, account access, API key, or purchase is needed.

## Recruitment message — buyer reviewer

> I am validating Morph, a simulation-first tool for reviewing robot recovery experiments before
> physical deployment. Could you spend 20–25 minutes assessing whether its evidence would help your
> team approve, reject, or reproduce a proposed controller change? This is product discovery, not a
> sales commitment, and no confidential operational data is required.

## Buyer questions

Ask about the last commissioning or manipulation failure, current time to reproduce it, who owns
the decision, what evidence is required, acceptable simulator provenance, audit/export needs, and
what would block a pilot. Interest is not purchase intent. Do not invent or paraphrase customer
quotes without consent.
