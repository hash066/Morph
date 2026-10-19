# MORPH

Simulation-first robot recovery | Optional hardware validation | 19 October 2026

## The product in one sentence

When a robot starts failing a familiar task after a small change, Morph runs controlled simulation experiments, proposes a bounded recovery configuration and produces an evidence report showing whether the fix actually works.

## A narrow but impressive first task

Use one supported tabletop robot arm performing pick-and-place. Change one or two feasible operating conditions such as payload, friction or control delay. The existing policy starts dropping or missing the object. Morph inspects telemetry, selects experiments, runs them on Nebius, compares candidates and recommends a tested recovery. It must also say when no safe recovery was found.

## What makes this a product

The customer-facing output is a reproducible recovery package: diagnosed possibilities, experiment history, selected parameters, before/after replay and held-out results. The agent is not a natural-language remote control for a robot. Its job is to reduce the engineering work needed to restore a task.

## The honesty boundary

This plan does not promise adaptation to any robot, broken actuators or arbitrary unseen environments. Start with one embodiment and a bounded parameter space. A simulation result establishes behavior in that simulator. Real hardware trials, user usability studies and buyer interviews establish different things and must be reported separately.

## My assessment

Morph has the stronger hackathon ceiling if you demonstrate a real improvement over a fair baseline. It also has higher technical failure risk and a slower route to revenue. The next eleven days are enough for a narrow, well-instrumented experiment, not a general-purpose robot foundation platform.

# 01 / What the user actually sees

Failure -> investigation -> experiments -> evidence -> controlled rollout.

## The workbench

The main screen has a task replay, current success rate, candidate experiment queue and evidence panel. A user selects a failing run and clicks Investigate. They see observations such as late gripper closure or repeated slips, not a fabricated statement of certainty about the cause.

## The agent workflow

Nemotron reads compact telemetry and task context, asks for additional measurements if needed, proposes a small set of plausible causes and selects bounded experiments. A validator rejects illegal parameter changes. Jobs run controlled trials and return structured results. The model summarizes tradeoffs and proposes the next experiment until the budget is exhausted.

## The recovery package

The best eligible candidate includes its parameter diff, simulator version, model identifier, seed list, test conditions, success and failure counts, execution cost and a replay. If there is hardware, it also includes an operator checklist and a separate physical-trial log. Publishing a package never means automatically commanding a physical robot.

## A concrete demo story

A pick-and-place policy works under its original conditions. A changed payload or mild delay produces repeatable failure. Morph selects experiments, finds a better grasp timing or bounded controller configuration, and shows improvement on withheld trials. Then show a condition outside the recoverable range where Morph declines to recommend deployment.

## Why this is more than a tutorial

The contribution is the recovery investigation and evidence workflow under a measured resource budget. Existing training examples supply the environment and baseline. Your new work must show better experiment efficiency, lower operator effort or better diagnosis/rejection behavior. A prettier visualization alone does not establish any of these.

# 02 / Simulation first, hardware second

Use a supported task before inventing a new robot or training pipeline.

## Recommended starting point

The official Isaac Lab tutorial currently provides an SO-101 arm task placing a vial into a rack, with state and camera variants. Its workflow includes training and an optional sim-to-real path. The tutorial uses Newton/MJWarp and does not require the full Isaac Sim application. Pin the exact tutorial and dependency versions after a successful smoke test. Do not mix instructions from incompatible Isaac Lab generations. [3,4]

## First reproducible milestone

Install the supported environment on a compatible NVIDIA GPU, run one episode, train or load a legitimately available baseline, and reproduce its evaluation. Save a video and machine-readable result. Headless cloud rendering and GPU availability must work before promising a serverless deployment. A local recording without the required runtime Nebius/NVIDIA-model integration is incomplete.

## Control the difficulty

Begin with the existing object and task geometry. Introduce mild, plausible perturbations that preserve task feasibility. Avoid changing embodiment, observation representation, reward and control interface simultaneously. Build one failure class well before adding another. If testing a harmless substitute object physically, update and validate the relevant simulator geometry and mass.

## What the hardware path requires

Borrow an SO-101-compatible setup or a robot with a demonstrably supported simulation/control bridge. Match joint conventions, calibration, action limits and sensing. If only an unrelated college arm is available, the port may consume the schedule; do not assume a URDF is enough. Confirm hardware access by 21 October or keep the submission simulation-first.

## Track eligibility versus strength

The rules allow a Physical AI project without hardware when the video shows at least one minute of the key application modules operating. The organizer nevertheless highlights hardware responding to real input as a strong demonstration. Simulation is eligible, but its evidence should be especially rigorous. NVIDIA open-model use remains required; a simulator alone does not satisfy that requirement. [1,2]

# 03 / Sponsor-centered architecture

NVIDIA supplies reasoning and simulation; Nebius executes real work.

## NVIDIA Nemotron on Token Factory

Use Nemotron for telemetry interpretation, hypothesis generation and experiment selection through constrained JSON tools. Verify the exact model ID available to your account. Keep raw trial results outside model memory and retrieve them by run ID. Log model calls, prompt versions, latency and token cost.

## NVIDIA Isaac Lab and GPU simulation

Use the supported task and physics backend for repeatable parallel trials. Nebius GPU compute runs actual simulations, training or candidate evaluation. Start with a stable GPU VM if serverless compatibility is uncertain; move to Serverless Jobs only after the container, driver/runtime requirements, storage and execution duration have been validated.

## Orchestration and storage

Web UI -> experiment API -> durable queue -> simulation workers -> artifact store and result database -> Nemotron planner -> next validated experiment. Use immutable experiment manifests. Store checkpoints, videos and evaluation tables with content hashes. UI progress comes from real job states, not a simulated loading sequence.

## Optional GR00T branch

GR00T may supply a policy if a released checkpoint, data format and supported embodiment fit the task and compute budget. Do not make unproven GR00T fine-tuning a prerequisite. Nemotron already provides the required NVIDIA open-model component. Clearly identify whether the actual controller is a tutorial policy, an adapted policy or GR00T.

## Why Cosmos is optional

Synthetic video is not a physics validator. Add Cosmos only if a specific visual-domain experiment needs it and the generated data is evaluated. It should not displace the recovery benchmark. Four NVIDIA brands with weak integration will be less convincing than two that are essential.

## A serious overlap to acknowledge

Nebius already publishes examples pairing Token Factory with GPU-job sweeps and ranking runs. Therefore, "an LLM launches simulations" is not a sufficient novelty claim. Morph must add useful failure diagnosis, bounded recovery decisions, fair evaluation and a usable evidence package. [6]

# 04 / The recovery algorithm

Keep exploration bounded, reproducible and falsifiable.

## Inputs

A failing rollout, task success definition, robot/action limits, selected telemetry, current policy/controller settings and a fixed experiment budget. Keep the injected fault label hidden from the agent during diagnosis. Otherwise the test merely asks it to repeat the answer you supplied.

## Observations and hypotheses

Compute structured features such as grasp timing, object slip, endpoint error, completion time and abort events. Nemotron proposes at most three hypotheses with supporting observations and a requested discriminating experiment. It may report insufficient evidence. Language confidence is not a calibrated probability.

## Bounded actions

Expose a small typed search space, for example grasp timing offset, approach speed multiplier and a validated controller parameter. Derive ranges from the selected controller and robot limits. Reject arbitrary Python, reward rewrites, unconstrained joint commands and changes to the evaluator. Do not expose parameters the policy ignores.

## Experiment loop

Validate proposal -> allocate paired seeds -> run candidate -> compute evaluator-owned metrics -> append immutable result -> ask planner for next candidate. Stop at a fixed rollout/compute budget. Candidate selection uses development runs only. Keep the final held-out cases unavailable to the planner.

## Choosing and rejecting

A candidate must improve the predeclared task metric without increasing collisions, limit violations or other failure criteria beyond the acceptance threshold. If no candidate meets the requirement, return No validated recovery. Preserve the original policy and settings. Explain the best observed tradeoff without turning it into deployment approval.

## Where the novelty can survive

Test whether diagnosis-driven selection finds an acceptable candidate in fewer evaluations than matched random or CEM search. If it does not, investigate whether the product saves measured operator time instead. Report the actual result. Do not claim a new learning algorithm merely because an LLM calls an optimizer.

# 05 / The experiment that earns credibility

One fair benchmark is more persuasive than many cinematic clips.

## Pre-register the comparison

Evaluate the unchanged baseline, a simple search method and Morph under the same task, candidate limits and simulator budget. If possible add an experienced human using the same interface. Include Nemotron overhead in total time and cost; parallel GPU execution can otherwise make an inefficient method look fast.

## Proposed test allocation

Use five development seeds to debug each condition. Reserve 20 held-out seeds for each of three feasible perturbation conditions, giving 60 paired evaluation episodes per method. These are proposed targets; reduce transparently if time or compute requires it. Do not call repeated deterministic replays independent trials.

## Success definition

For the tutorial task, success should mean the object is properly placed and released in the target, not merely that the end effector gets close. Use the environment-owned evaluator and disclose any modifications. Report success count / total, completion time, abort rate, experiment count and total cost.

## Guard against misleading gains

Pair initial conditions across methods, freeze evaluation before running the final test, include failure videos and report seed-level outcomes. Compare uncertainty, not just one aggregate percentage. With small samples, a modest numerical gain may be inconclusive. Do not tune on the held-out set and still call it held out.

## Ablations that matter

Remove diagnosis and use random candidates with the same budget; remove history and plan each experiment independently; compare telemetry-only planning with richer observations if supported. Choose the one ablation that directly tests your core claim rather than adding many shallow comparisons.

## Unrecoverable case

Include an explicitly separate condition outside your declared recovery range. Its desired outcome is safe refusal or escalation, not success at any cost. Do not include impossible cases in a pooled success metric without labeling them. The rejection behavior is itself a useful product demonstration.

# 06 / Optional real-world validation

A small honest transfer test is better than a staged hardware victory.

## Physical trial gate

Proceed only after calibration, joint-direction checks, action-range checks, emergency stop and the original task work with a qualified operator. Confirm the policy observation/action interface matches the real robot. LeRobot provides useful setup, data and evaluation workflows for supported arms, but compatibility still needs testing. [5]

## A manageable experiment

Use a low-energy tabletop task with lightweight objects, a clear workspace and a human operator. Test one mild, measured change within the hardware's rated capability. Avoid deliberately damaging actuators or using fragile objects for dramatic effect. Log camera views and robot telemetry where available.

## Transfer procedure

Run the baseline under the changed condition, stop, calibrate the simulator from measured properties, evaluate candidate recovery, review the diff, then apply an explicitly approved configuration to the robot. Use a bounded number of physical trials. Record every attempt, including failed grasps and manual resets.

## Report the denominator

A possible target is ten before and ten after trials under comparable conditions, with alternating order where practical. This is a small feasibility test, not deployment certification. Show n/N, object and condition details, whether the operator intervened, and what differs from simulation.

## If no robot arrives

Keep the complete simulation workflow and demonstrate a participant launching a new experiment live. Label the video Simulation. Publish reproducible commands, seed manifests and results. You can truthfully submit to Physical AI under the rule, but must not present participant usability testing as sim-to-real validation.

## Do not quietly change robots

If the college offers a mobile base rather than an arm, assess a separate navigation-recovery variant only before the commitment deadline. Switching to an unrelated embodiment during the final week risks losing the entire benchmark. Borrowing the supported platform is often more valuable than buying extra compute.

# 07 / Testing with X, Y and Z people

Three types of evidence; three separate counts.

## A. Workflow usability

Recruit a target of three robotics students or engineers. Give each a failing run and ask them to investigate, launch an experiment, interpret the result and export a recovery package. Measure completion, operator minutes, assistance needed and interpretation errors. Use new conditions rather than the exact demonstration they have already seen.

## B. Physical performance

If hardware exists, count robot trials and conditions independently of the number of people present. Three people watching ten grasps is ten robot trials, not thirty. Record operator interventions and all unsuccessful attempts. Participant feedback cannot establish collision safety or physical robustness.

## C. Buyer discovery

Interview a target of two lab managers or robotics integrators about their last calibration or commissioning problem. Ask how long it took, how frequently it happens, who owns the budget and what proof they require before testing a tool. A positive comment is not a purchase commitment.

## An exact study script

Provide the same task brief, allow a timed unassisted attempt, then offer help and log the intervention. Ask the participant to explain the evidence in their own words. Finish with a comparison to their current workflow and a request for a concrete next step, such as supplying a second failure case.

## The demo claim format

"Three engineers used Morph; two completed the investigation unaided. We evaluated 60 simulated episodes per method. We separately ran 20 physical trials on one arm." These numbers are examples to replace with actual outcomes. Show a small evidence table with participant IDs, dates, task and result; obtain recording consent.

## What makes the study stronger

Recruit at least one person outside your team, preserve failed sessions, disclose coaching and publish an anonymized protocol. Ask a participant to reproduce a result using only the README. That is stronger evidence of a useful developer product than collecting compliments.

# 08 / Hardware and startup routes

Specific avenues to investigate; no partnership or availability is implied.

## Route 1: a college SO-101 / LeRobot arm

This is the best fit for the proposed benchmark if an existing calibrated setup is available. Ask the robotics club or mechatronics lab for the exact model, controller, cameras, software versions, operator and access dates. The official SO-101 documentation is a practical assembly/calibration reference. Buying a kit now adds shipping and setup risk. [5]

## Route 2: RigBetel Labs

RigBetel publicly offers mobile robots, manipulators and robotics development/mentorship resources. It is a concrete organization to approach for platform access, an engineering interview or a failure case. Its public pages do not establish an available SO-101 or a willingness to partner. Confirm those details directly before designing around its hardware. [7]

## Route 3: an integration or automation lab

Ask a local integrator for a non-sensitive repeatable task affected by small setup changes. The initial request should be a recorded failure and technical interview, not production robot control. An introduction to the engineer who recalibrates fixtures may be more useful than a senior executive pitch.

## Three startup wedges to compare

1. Gripper/fixture commissioning assistant: reduce repeated retuning after an object or fixture changes. Best match to Morph. 2. Robot regression workbench: rerun task suites before a policy update and package evidence. Easier to standardize, but overlaps existing simulation tooling. 3. Mobile-robot recovery experiments: test navigation changes after layout shifts. Promising, but it is a different embodiment and should not be added to the arm MVP.

## An outreach draft, not a sent message

"We are building a tool that investigates repeatable robot-task failures using controlled simulation experiments. Could we interview the engineer responsible for commissioning and, if appropriate, test one low-risk failure case on a supervised setup? We can share a reproducible report and will not publish your data without permission."

## Choose access over spectacle

Do not select drones, humanoids or high-force industrial demonstrations just because they look impressive. A supported tabletop task with credible recovery evidence is a better eleven-day project than an ambitious robot that cannot be evaluated reliably.

# 09 / Build schedule and stop conditions

Make the technical uncertainty visible by 21 October.

## 19-20 October: feasibility spike

Owner A reproduces the supported simulation baseline on available GPU compute. Owner B connects Nemotron and a constrained experiment tool. Owner C builds run storage, replay and results UI. Owner D recruits evaluators and investigates robot access. Gate: a repeatable failure, one real Nebius execution and an initial bounded recovery experiment.

## 21 October: commit or switch

Choose Morph if the environment is reproducible, the failure is meaningful and a recovery candidate shows signal without changing the evaluator. Hardware is optional. If these fail, commit to Axys only if its real Instagram gate has passed. Do not spend the entire week hoping an unsupported training stack will become stable.

## 22-24 October: the complete loop

Implement immutable manifests, job orchestration, bounded search, telemetry diagnosis and honest result summaries. Establish the simple-search baseline. Freeze the task and evaluation split. Add no second robot. If hardware is available, complete calibration and baseline trials before attempting transfer.

## 25-27 October: evidence

Run the held-out comparison and the selected ablation. Conduct participant sessions and buyer interviews. Run optional supervised physical trials. If Morph does not beat search, present the result accurately and assess measured operator effort; do not conceal the baseline.

## 28-30 October: package

Freeze the tested environment, write reproduction commands, publish allowed assets and code with a license, record the demo and submit early. Keep the app and artifacts available for judging. The official deadline is 30 October at 10:00am PDT / 10:30pm IST. [1]

## Compute and cost control

Benchmark one short run first. Estimate GPU spend as instance hourly price times total worker-hours, then add inference, storage and transfer. Set per-experiment and account spend caps and stop idle workers. No dollar estimate is reliable until your quota, selected GPU and measured runtime are known. Keep both total compute and wall-clock time in the results.

# 10 / Demo, economics and decision

A great failure-to-recovery story still needs a buyer.

## A 2 minute 50 second demonstration

0:00-0:20: show the task and changed condition. 0:20-0:45: show repeatable baseline failure. 0:45-1:45: show at least one minute of operating application modules: investigation, jobs, live status, replay and candidate evaluation. 1:45-2:15: show held-out comparison and refusal case. 2:15-2:35: show real hardware only if performed, otherwise participant reproduction. 2:35-2:50: state measured outcome and target buyer. Clearly label time compression and simulation.

## First commercial offer

Sell an engineering pilot on one supported task: instrument the baseline, reproduce a failure, evaluate bounded changes and deliver a report. Test willingness to pay $1,000-$5,000 for the pilot; that is an unvalidated pricing experiment. Only move to a recurring platform fee when customers have repeated evaluation needs.

## How this could scale

A hypothetical $500/month team plan requires 167 paying teams to reach about $1M ARR. This is arithmetic, not demand evidence. Robotics integration, support, security review and hardware variation can make the business service-heavy. Your initial moat would be useful failure datasets, reliable adapters and customer workflow integration, not exclusive access to NVIDIA tools.

## Brutal comparison

Morph is the stronger technical bet for this hackathon if it proves recovery beyond a fair baseline. Axys is the stronger near-term merchant revenue bet if it really connects and publishes. Neither has a defensible million-dollar valuation from a demo alone. Starting Axys from scratch means it no longer has an assumed existing-product advantage.

## My choice

Give Morph the 48-hour technical gate, then commit only on evidence. I would not replace the entire project with a generic startup idea or bolt physical AI onto Axys. A narrow Morph result that is reproducible and useful is the best grand-prize attempt of these two; a tutorial with an LLM narrator is not.

# 11 / Sources and boundaries

Primary references for feasibility, eligibility and known overlap.

## [1] Official rules

https://nebiusglobalaihackathon.devpost.com/rules

## [2] Organizer judging guidance

https://nebiusglobalaihackathon.devpost.com/updates/46204-here-s-how-judging-works

## [3] Isaac Lab supported tutorial

https://isaac-sim.github.io/IsaacLab/develop/source/setup/tutorial.html

## [4] Tutorial implementation and NVIDIA learning path

https://github.com/isaac-sim/IsaacLabTutorial
https://docs.nvidia.com/learning/physical-ai/getting-started-with-isaac-lab/latest/index.html

## [5] LeRobot and SO-101 setup

https://huggingface.co/docs/lerobot/index
https://github.com/huggingface/lerobot/blob/main/docs/source/so101.mdx

## [6] Nebius existing compute and inference workflows

https://github.com/nebius/nebius-physical-ai/blob/main/docs/workbench/cookbooks/tokenfactory-compute-combos.md
https://github.com/nebius/nebius-physical-ai/blob/main/docs/workbench/token-factory.md

## [7] Potential robotics contact, not a partner

https://www.rigbetellabs.com/
https://www.rigbetellabs.com/mentorship

## What remains unverified

No simulator run, model deployment, robot booking, participant study or recovery gain has been completed by this planning work. Library branches, checkpoint access and GPU requirements must be pinned and tested. Performance targets, sample sizes, pricing and the decision gate are proposed by this plan, not published guarantees. Do not claim universal adaptation, physical safety certification or a judge's endorsement.
