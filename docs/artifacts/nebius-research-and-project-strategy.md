# Nebius × NVIDIA: research and project strategy

Research snapshot: 3 October 2026. Recommendation assumes a strong technical team and distribution, with software preferred and basic college hardware available.

My preferred direction is **Relay: executable commissioning reviews**. Turn contradictions between industrial engineering documents and control software into reproducible behavioral tests, with evidence an engineer can inspect. **Cutover**, which tests business behavior across database migrations, is the strongest entirely software alternative. These are proposed product wedges, not claims of unprecedented invention or proven demand. Winning and creating a valuable business require different evidence; neither is guaranteed by the idea.

## Coverage and limits

Reviewed the overview, full rules, resources page, schedule, all 25 discussion threads and seven updates linked on the public pages, and the project-gallery status. Searched all 23 listed judges; public technical writing, profiles and posts were available for many, but not all. Reviewed relevant resource documentation and cookbooks, not every page in the vendors' documentation or every linked event/video. The workshop writeup was read; the full recording was not watched. Private Discord discussions and complete X/LinkedIn histories were not accessible. Public search is not an exhaustive competitor or patent search.

Sources are linked beside findings. Official requirements outrank marketing summaries; participant reports are not organizer rulings. Community posts demonstrate individual problems, not market size or willingness to pay. Vendor pages establish claimed capabilities, not independently verified performance. All project designs, rankings, proposed prices, targets and schedules below are my recommendations.

## What the competition requires

Use a real Nebius inference call or eligible Cloud deployment, plus an NVIDIA open model. Choose a matching track. Supply a working project, public licensed source and setup instructions, description, public YouTube demonstration under three minutes, and specific platform/model feedback. Existing projects need substantial changes during the submission period. English materials or translations are required. Judges need free access through judging; Physical AI has different access/video provisions. Eligibility includes age, location and conflict restrictions. Entrants retain IP, but public-source and promotion terms apply. Four criteria are equally weighted; ties prioritize implementation, then the remaining listed criteria. Do not assume prizes stack freely. See the complete [official rules](https://nebiusglobalaihackathon.devpost.com/rules).

Submit by **30 October 2026, 10:00 a.m. PDT / 10:30 p.m. IST**. Judging is **1–15 December**; winners are scheduled around **11 January 2027**. Budget for the gap. [Schedule](https://nebiusglobalaihackathon.devpost.com/details/dates).

The overall grand prize is $20,000. There are four tracks: coding/agentic engineering, apps/agents, personal AI and physical AI. The gallery is not yet published, so competitor visibility is incomplete. [Overview](https://nebiusglobalaihackathon.devpost.com/), [gallery](https://nebiusglobalaihackathon.devpost.com/project-gallery).

The organizers specifically encourage complete autonomous workflows, real repository work, persistent assistants that take actions, and live physical responses. Their latest advice emphasizes a clear problem-first pitch, audible identification of the required platforms/models, and useful technical feedback. This is stronger evidence than speculation about a judge's taste. [Judging update](https://nebiusglobalaihackathon.devpost.com/updates/46204-here-s-how-judging-works), [submission advice](https://nebiusglobalaihackathon.devpost.com/updates/46205-how-to-build-a-winning-project).

## Resources and contradictions that affect execution

The resource page advertises $25 Token Factory credits via activation code `NEBIUS-DEVPOST-GLOBAL26`, plus another $25 through the Builders Program. It links community support and city events. Do not treat inference credits as a GPU-compute budget. The resource page says city association can qualify without attendance, while the rules' city-prize language requires attendance. Rely on the rules and obtain written clarification if pursuing that bonus. [Resources](https://nebiusglobalaihackathon.devpost.com/resources).

Use the [Builders hub](https://dev.nebius.com/) and [program](https://dev.nebius.com/builders) for current onboarding and support. The [Token Factory quickstart](https://docs.tokenfactory.nebius.com/quickstart), [structured output](https://docs.tokenfactory.nebius.com/ai-models-inference/json) and [tool-calling documentation](https://docs.tokenfactory.nebius.com/ai-models-inference/function-calling) are the useful implementation starting points.

Current official model material lists Lightning, Super and Ultra, with model-specific deployment availability. Do not assume that a vision model is available on a public endpoint or that every Nemotron model supports self-service fine-tuning. Validate the exact account/model combination before designing around it. [Current model guidance](https://nebius.com/services/token-factory/models/nvidia-nemotron-models-inference).

The [agent cost cookbook](https://dev.nebius.com/cookbook/agent-cost-benchmark) is particularly useful: it measures completed tasks, correctness, tokens and latency, rather than comparing token prices alone. Reuse that measurement discipline. The [Agents Blueprint](https://nebius.com/blog/posts/introducing-the-nebius-agents-blueprint) already includes a compliance-agent example; a generic compliance agent would need much more differentiation.

## Is hardware historically favored?

I did not find a verified previous edition of this exact global contest. Related events are evidence of sponsor interests, not a statistical estimate of this jury's preferences.

| Related event | Observed result | Interpretation |
|---|---|---|
| Nebius Serverless AI Builders Challenge, August 2026 | MediSimplifier first; model-evaluation dashboard second; Balagan multi-agent chaos testing third; robotics received a special award | Strong direct evidence that software can take Nebius's top awards. [Official results](https://nebius.com/blog/posts/serverless-ai-builders-challenge-winners) |
| LlamaCon, May 2025, supported by Nebius and other sponsors | OrgLens first, Compliance Wizards second, CCTV Operator third; Geo-ML won API usage | Software and applied domain workflows performed well. Different organizers, model requirement and panel. [Meta results](https://ai.meta.com/blog/llamacon-hackathon/) |
| Nebius-supported 2025 events | Sponsor winners included dataset generation and longevity evidence/causal-network projects | Further software precedent, not a hardware requirement. [Nebius event record](https://github.com/nebius/token-factory-cookbook/blob/main/community/events.md) |
| Hardcore CUDA Hackathon, July 2024 | steriOMG for Apple Vision Pro won | A hardware-linked application can win a specialized event. [Nebius announcement](https://www.linkedin.com/posts/nebius_winners-hackathon-cuda-activity-7218133664084176896-ZeXM) |
| Nebius.Build SF, March 2026 | Injester creator reports first place for agent-to-merchant commerce | Additional software signal, but self-reported rather than an organizer result table. [Creator report](https://benjaminshyong.com/hackathons/nebius-build) |
| Robotics & Physical AI Awards, December 2025 | Dedicated awards for robotics companies | Exclude from any claim of general hackathon preference: the selection pool was explicitly physical AI. [Official announcement](https://nebius.com/newsroom/nebius-debuts-the-robotics-and-physical-ai-awards-and-summit-to-support-next-generation-startups-with-1-5-million-in-compute-credits) |

**Decision:** build software whose value is independently clear. Add a small physical demonstration only if it strengthens the evidence. Buying a robot is not a demonstrated strategy for improving your odds.

## Judge-by-judge evidence

The final column is an inference about persuasive evidence, not a prediction of votes. Public reposts show interest, not necessarily authorship or endorsement of every claim. No private preferences are inferred.

| Judge | Public evidence inspected | What to demonstrate |
|---|---|---|
| Nancy Agarwal | [NVIDIA author page](https://developer.nvidia.com/blog/author/nancya/) describes inference pipelines, NIM and developer experience; lists data-flywheel and multimodal work | Working integration, clear deployment and measured improvement loops |
| Abhinav Balasubramanian | [Public profile/posts](https://www.linkedin.com/in/abhi-bala); coauthor of [FACTS](https://arxiv.org/abs/2407.07858) and [adaptive data flywheel work](https://arxiv.org/abs/2510.27051) | Evaluation beyond a successful demo; reliability under realistic constraints |
| Dylan Bristot | [Personal site](https://dylanbristot.com/) and [Data Lab article](https://nebius.com/blog/posts/your-best-dataset-is-already-in-your-logs) emphasize production workflows, economics and feedback data | A specific buyer, cost per successful task and learning from actual usage |
| AbdulMajed Raja | Authored [deep-research recipe](https://dev.nebius.com/cookbook/deep-research-agent-tavily) and [OpenHands integration](https://dev.nebius.com/cookbook/openhands-agent-canvas) | A reproducible workflow extending well beyond readily available cookbook functionality |
| Rob Spectre | [Nebius livestream](https://nebius.com/events/build-with-nebius-livestream) and [production-agents event](https://luma.com/tavily-d1pw) | Actual working code, recovery behavior and realistic operating costs |
| Evan Rimer | [Public profile/posts](https://www.linkedin.com/in/evan-rimer-119047138) discuss search inside agent decisions and coding agents | Retrieval that changes a verifiable action; useful source and execution traces |
| Lakshmi Rameish | Exact Devpost spelling produced little independent evidence. [NVIDIA's Lakshmi Ramesh](https://developer.nvidia.com/blog/author/lramesh/) is a plausible match, not conclusively established | No personalized prediction; assess against the common rubric |
| Surbhi Jha | Named coauthor of [FACTS](https://arxiv.org/abs/2407.07858); public name search has significant identity ambiguity | Grounding, evaluation and failure analysis; no reliable post-history inference |
| Joe Sarabia | [Profile](https://www.linkedin.com/in/joe-sarabia) found, with little accessible substantive recent writing | Integration and product coherence based on listed role only; low-confidence personalization |
| Marouane Khoukh | [Serverless office hours](https://nebius.com/events/webinar-cloud-office-hours-serverless) and [Aether session](https://nebius.com/events/webinar-aether-3-6) | Sensible infrastructure choices, logs and reproducibility |
| Ricky Johnson | [Public posts](https://www.linkedin.com/in/ricky-johnson-621704b2) discuss observing search calls and build-versus-buy tradeoffs; [official office hours](https://www.tavily.com/events/tavily-office-hours-coffee-chat-ama) | Transparent retrieval behavior and a justified role for search |
| Selena Williams | [Public posts](https://www.linkedin.com/in/selena-joet-williams) discuss local agents, private data and DGX Spark | Data control and useful actions; avoid claims that hosted inference is fully local |
| Aleksandr Patrushev | [Serverless webinar](https://nebius.com/events/webinar-serverless-for-ai) | Explain why jobs/endpoints fit the workload, including utilization and cost |
| Unmesh Kurup | Listed on event, but no strong current Nebius-linked public writing found; older research results are insufficient to infer current priorities | Do not manufacture a judge-specific preference |
| Daniel Myers | [Public posts](https://www.linkedin.com/in/jdanielmyers) emphasize building on open models and the full Nebius stack | A developer can adopt and run the product with minimal friction |
| Jacquie Capur | [Live-build program](https://nebius.com/events/build-with-nebius-livestream) and the hackathon workshop writeup | Clear live workflow, visible output, understandable UX and practical iteration |
| Lakshya Prakash Agarwal | [Public profile/posts](https://ca.linkedin.com/in/lakshyaag) feature open-model comparisons, retrieval, observability and simulation | Same-task comparisons with honest quality/cost tradeoffs |
| Johnny Nunez | [Personal technical portfolio](https://johnnynunez.github.io/) spans simulation, robotics, edge deployment and open-source contributions | A reproducible path from model output to runtime behavior; benchmark real limitations |
| Evan Helda | [Public sim-to-real post](https://www.linkedin.com/posts/evanhelda_sim-2-real-is-one-of-the-most-common-buzz-activity-7465401447862644736-uy__) | Distinguish simulation evidence from real-world validation |
| Mikhail Rozhkov | [Practical serverless workshop](https://nebius.com/events/webinar-practical-serverless-ai-for-developers) | Working orchestration, inspectable outputs and operational simplicity |
| Dhruv Diddi | [Public post](https://www.linkedin.com/posts/dhruvdiddi_getsolotech-ownyourai-activity-7442962777150963712-z8a1) emphasizes deployment and real-time physical systems; [robotics event](https://luma.com/msdcorrg) | Outcomes on the intended runtime, not just attractive architecture |
| Aditya Sahu | [NVIDIA portfolio](https://developer.nvidia.com/blog/author/adsahu/) and [edge optimization article](https://developer.nvidia.com/blog/frontier-reasoning-reaches-the-edge-how-to-deploy-and-optimize-models-on-nvidia-jetson) | Resource measurements if using edge hardware; realistic deployment limits |
| Sayali Kandarkar | [NVIDIA biography](https://developer.nvidia.com/blog/author/skandarkar/) and [verified agent-skills article](https://developer.nvidia.com/blog/nvidia-verified-agent-skills-provide-capability-governance-for-ai-agents/) | Evaluation, constrained capabilities and traceable execution |

I would prepare one excellent evidence package for this panel, rather than 23 personalized pitches. Jensen Huang and Linus Torvalds are not listed as judges. Treat their names as your standard for engineering ambition, not as a basis for invented endorsements.

## Market research: useful signals and rejected directions

| Focus | Evidence | Decision |
|---|---|---|
| Industrial commissioning | Engineers describe mismatched tags, revisions and signoffs in [r/PLC](https://www.reddit.com/r/PLC/comments/1opvwr7/the_biggest_delays_during_commissioning_usually/). A buyer ties final payment to updated documentation on [PLCtalk](https://www.plctalk.net/threads/malware-in-a-plc.126096/page-2). | Strong problem hypothesis and identifiable buyer; quantify with actual project packets and interviews |
| AI code verification | [HN discussion](https://news.ycombinator.com/item?id=48655020) describes shallow browser tests; [Lobsters](https://lobste.rs/s/1xyudo/we_are_qa_engineers_now) discusses engineers still owning signoff | Real pain, but generic verification is crowded |
| Production reproduction | [FixBugs founder's HN launch](https://news.ycombinator.com/item?id=48900465) already describes reproducing bugs and verifying fixes | Do not present “agent finds and fixes production bugs” as a new category |
| Distributed-system verification | [Antithesis](https://antithesis.com/blog/2026/mutation-testing/) already uses agents to infer properties and mutation-test their checks | A generic proof/testing agent has strong incumbents |
| GPU optimization | [r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/comments/1ldg17j) shows utilization confusion; [nCompass founder's X post](https://x.com/adityaraja0/status/2028519599176908975) describes an existing optimization agent; [NVIDIA profiling agent](https://github.com/NVIDIA/TensorRT-LLM/blob/main/.claude/agents/perf-profiling-specialist.md) covers many basics | Reject a profiler-chat wrapper; only reconsider with a distinct measurable technical advance |
| Database migration | [HN practitioner discussion](https://news.ycombinator.com/item?id=34602318) values real database tests and historical edge cases; [Atlas](https://atlasgo.io/use-cases/ai-safe-migrations) already targets AI-safe migrations | Narrow to cross-version application behavior and realistic traffic rather than generating safe DDL |
| Parts substitution | [Manufacturer checklist](https://www.raypcb.com/resources/bom-alternative-approval/) ties changes to firmware/test limits; [PCNshark](https://pcnshark.com/) already handles notices, BOM matching and alternates | Plain alternate-parts recommendation is insufficiently differentiated |
| Robot validation | [BootLoop](https://bootloop.ai/industries/robotics), [Dirac](https://diracrobotics.com/evals), [Brio](https://www.getbrio.dev/) already offer overlapping tests and regression workflows | Hardware access and a narrow unsolved failure class are prerequisites |

X supplied a useful first-party competitor announcement, but broad X searches were thin. PLCtalk and vendor issue/research material were more useful than popularity-driven idea lists. None of these anecdotes validate a million-dollar business.

## Ranked project hypotheses

This ranking weighs demonstrable novelty, buyer specificity, sponsor fit, and a 27-day delivery window. It is judgment, not a numerical probability of winning.

### 1. Relay — executable commissioning reviews

**Buyer:** controls integrators and machine builders doing repeated factory/site acceptance work. Start with one domain, such as pump skids or small material-handling cells.

**Input:** two document revisions, a functional description, an I/O register and a supported PLC code export. **Output:** an engineer-reviewed change-impact report containing source references, a runnable failing test, the affected control behavior and regression evidence after an approved correction.

Example: the latest instrument specification changes the engineering range of a transmitter, but the PLC scaling and acceptance checklist still use the old range. Relay ties the conflicting source locations to the same signal, proposes the intended behavior for review, generates an input sequence that makes the alarm trip at the wrong physical value, then replays the corrected case. A disagreement remains unresolved until a person confirms the authoritative requirement.

The core technical contribution should be a typed, versioned intermediate representation that preserves source provenance and compiles accepted requirements into tests. The language model interprets messy evidence; executable checks establish what happened within the modeled scope. It must distinguish “contradiction found,” “counterexample reproduced,” “not reproduced within this bound,” and “insufficient evidence.”

**Competitive boundary:** [Tagsight](https://tagsight.io/) already extracts registers; [Pathnovo](https://pathnovo.com/blog/p-and-id-cross-document-validation-epc) markets cross-document validation; [Copia](https://docs.copia.io/docs/copilot/copia-copilot) generates control code and documentation. [LLM4PLC](https://arxiv.org/abs/2401.05443) already combines LLM generation with external verification. Your claim is the productized link from conflicting revisions to an independently replayable behavioral consequence. That differentiation must be shown, not merely described.

**Hackathon boundary:** one controller/code subset, three artifact types, two small process examples, and a handful of high-value fault families. No universal CAD interpreter, arbitrary ladder-logic support, plant-wide digital twin or autonomous live controller writes. Use Coding and Agentic Engineering if generating/executing tests is central; choose Apps and Agents if the implemented product is mainly engineering review.

**Optional hardware:** college PLC trainer or microcontroller with safe indicator lights/sensor inputs. Run the identical counterexample on it. The browser replay should remain sufficient to understand the software product.

**Commercial hypothesis:** paid project review, then annual team deployment for recurring commissioning and changes. Pilot price to test: $2,000–$5,000 per scoped packet; annual hypothesis: $15,000–$30,000 per team. These are proposed offers, not observed market prices. Repeated use, trusted adapters and customer-approved evidence history are more defensible than the prompt.

**Kill condition:** no usable redacted packets, no engineer-confirmed material finding, or review burden comparable to doing the work manually. Customer data access matters more than team size here.

### 2. Cutover — test the business behavior of a migration

**Buyer:** SaaS platform teams shipping risky data transformations and rolling releases.

Given old/new application versions, migration SQL and a sanitized workload, identify candidate business invariants, obtain acceptance, run both versions through intermediate migration states, then minimize a failing transaction schedule. Show the exact records and sequence that cause duplicate entitlements, incorrect balances or lost relationships. Offer a tested migration correction.

**Demo:** row counts match and the migration completes, but an old background worker interacting with new application code produces an incorrect business result. Cutover produces a small deterministic replay and a corrected sequence.

**Difference to establish:** [Atlas](https://atlasgo.io/use-cases/ai-safe-migrations) and [Stripe's pg-schema-diff](https://github.com/stripe/pg-schema-diff/blob/main/CLAUDE.md) already address safe schema changes. [Google's migration guidance](https://docs.cloud.google.com/architecture/database-migration-concepts-principles-part-1) already recognizes completeness/consistency complexity. Cutover should target application semantics during coexistence of versions, not SQL linting or simple row comparisons.

Scope PostgreSQL, one application language and one queue pattern. Nemotron proposes invariants and experiment plans; real database execution determines outcomes. It remains useful without hardware. Proposed annual test price: $12,000–$24,000 per team, contingent on avoided engineering work and repeated use. Reject it if standard integration tests or existing migration tooling deliver the same result with comparable setup.

### 3. TaskFoundry — turn an expensive agent workflow into a qualified open-model deployment

**Buyer:** AI software teams already spending materially on a recurring workflow.

Capture a permitted workflow specification and evaluation cases, generate adversarial variations, compare open-model/harness configurations, and return the cheapest configuration meeting pre-agreed task criteria. The deliverable includes deployment settings, reproducible failure cases, and explicit limits on the claim. Treat tool side effects as part of task correctness.

**Demo:** a cheaper model looks good on average but fails one critical tool-use case. The system blocks that configuration, changes the harness, reruns hidden cases and shows the cost-quality tradeoff with failures preserved.

This is exceptionally aligned with Nebius, but less novel: [its own Blueprint](https://nebius.com/blog/posts/introducing-the-nebius-agents-blueprint), [cost benchmark](https://dev.nebius.com/cookbook/agent-cost-benchmark) and the recent evaluation-dashboard winner overlap. Build only if you have a distinctive workload-specific verification method and a real customer. A dashboard comparing models is inadequate. Proposed $2,000/month offer needs significant measured savings after compute and support.

### 4. Fault Atlas — minimize a robot failure into a portable regression case

**Buyer:** robotics teams integrating one specific class of manipulation policy.

From a failed trajectory, search a bounded set of scene perturbations and timing changes to find a smaller reproducible failure. Export scene, seed, policy version, execution trace and a replay. Test the repair on held-out perturbations. An NVIDIA model can interpret the trajectory and guide which experiments to run, while the simulator measures results.

The interesting output is the minimal failure and transfer evidence, not a generated simulation video. [Dirac](https://diracrobotics.com/evals), [Brio](https://www.getbrio.dev/) and [BootLoop](https://bootloop.ai/industries/robotics) make the general category crowded. Without a real policy partner and some physical verification, it ranks below the software options. Simulation success alone does not establish real-world reliability. Proposed commercial offer: a scoped paid validation engagement before recurring platform pricing.

### 5. PartWitness — challenge an electronic component substitution in circuit context

**Buyer:** hardware teams managing component obsolescence or supplier substitutions.

Connect datasheet evidence, the circuit's actual operating envelope, firmware assumptions and a small test model. Find a condition where a seemingly equivalent replacement fails a required behavior; deliver an engineer-reviewable experiment rather than a similarity score.

**Demo:** two parts match a catalog filter, but one fails a startup/timing corner in the supported circuit. Source-linked constraints lead to a replayable simulation; the tool identifies missing evidence when a model is unavailable.

[PCNshark](https://pcnshark.com/) and [engineering-change platforms](https://www.sensedrive.ai/use-cases/engineering-change-impact) already cover much of the discovery workflow. Differentiate on circuit-context counterexamples. Limit to one well-modeled component family; model availability and accuracy are the main risks. Treat an annual $20,000/team offer as a hypothesis to test, not a market fact.

## Relay implementation and evaluation plan

Use this pipeline:

1. Parse supported files; preserve page/line/cell references, hashes and revisions.
2. Build typed entities with units, ranges, aliases and provenance. Deterministic checks catch arithmetic and exact mismatches.
3. Use Nemotron on Token Factory to resolve language/identity ambiguities and propose candidate behavioral requirements. Present unresolved conflicts explicitly.
4. Have the engineer accept the requirement and operating assumptions. Freeze this test oracle independently of any proposed repair.
5. Compile to bounded executable tests against supported control logic. Model timers, scan semantics and sensor assumptions explicitly.
6. Execute in isolated workers; minimize failing sequences where supported. Never let a generated patch rewrite its own acceptance condition.
7. Show synchronized evidence and behavior: source discrepancy, affected variable, failing trace, proposed correction, rerun and coverage limits.
8. Export a replay bundle and review record. A cryptographic hash proves artifact identity, not physical correctness.

Token Factory should do meaningful interpretation and test planning. Use a smaller Nemotron model for simpler work and a stronger model where evaluation justifies it. Nebius Jobs can run batch validations; CPU execution is sensible where no GPU is needed. Tavily is optional for obtaining current manufacturer evidence, with exact part/revision checks and provenance. Do not add a search call purely for a bonus.

**Evaluation design:** obtain at least three independent redacted project packets; keep one entirely held out. Supplement with clearly labeled synthetic cases and seeded changes. Compare deterministic checks alone, a single-pass model, and the full pipeline. Measure confirmed finding precision/recall against expert labels, false alarms, unsupported claims, reproducibility, time to confirmed diagnosis, engineer review time and cost per confirmed finding. Report sample sizes and separate real from seeded results.

Initial targets, not results: more than 90% precision on the supported fault families; reproduce at least 80% of accepted in-scope fault cases; a second engineer can rerun every published counterexample; at least 50% reduction in measured review time on the pilot packet. Revisit targets after a real baseline. Do not generalize small-sample success to universal plant safety.

| Dates | Deliverable and decision |
|---|---|
| Oct 3–5 | Five buyer interviews; three usable packets; Token Factory access; one independently confirmed problem. Kill or narrow the idea if evidence/data cannot be obtained. |
| Oct 6–10 | End-to-end parse → accepted requirement → failing executable test on one process; versioned replay format |
| Oct 11–16 | Second process, regression after correction, supported fault families, baseline comparisons and held-out evaluation |
| Oct 17–21 | Pilot feedback, review-time measurements, onboarding and clear scope/error states; optional trainer hardware only if core is complete |
| Oct 22–25 | Reproducible installation, final benchmarks, source licenses, hosted reviewer flow, specific platform feedback |
| Oct 26–28 | Public video, final submission, fresh-machine test and a second person's review |
| Oct 29–30 | Submission buffer and judge-access verification |
| Until Dec 15 | Keep the submitted build accessible and funded; label any recorded examples and preserve a working evaluator route |

Three-minute video structure: 0–20 seconds buyer/problem; 20–45 contradictory evidence; 45–100 executable failure; 100–135 approved correction and same-test replay; 135–160 measured pilot/baseline results and limitations; 160–175 platform/model integration, product and buyer. Leave a few seconds of margin.

## Product value and the million-dollar objective

Winning a $20,000 award, generating $1 million in ARR, receiving a $1 million acquisition offer and personally retaining $1 million are different outcomes. There is no evidence here for promising any of them.

The practical target for Relay is repeatable annual customer value. **50 customers × $20,000/year = $1 million ARR** is arithmetic, not a forecast. Alternatively, **100 × $10,000/year** reaches the same number with different sales/support requirements. Services and one-off pilot fees are not ARR.

Start with a paid scoped review and measure hours saved plus material findings. Convert only where recurring projects or changes create repeated use. Track sales cycle, onboarding labor, support time, inference/compute cost, renewal intent and concentration risk. Ten enthusiastic free users are weaker commercial evidence than three repeat paid buyers.

Open-source the complete submitted implementation. Sell managed execution, integrations, enterprise administration, support and maintained deployment as the commercial hypothesis. Build a defensible corpus of customer-authorized failure cases and validated adapters; do not assume private customer data can be reused across customers. Acquisition value would depend on adoption, retention, defensible technology and strategic fit, not the hackathon badge.

## Public discussion audit

Every thread linked on the public discussion index was read. Most operational questions received a Discord referral, which is not an answer or an exception. The source slug identifies the topic for direct follow-up.

| Thread | Finding |
|---|---|
| [45423 deployment](https://nebiusglobalaihackathon.devpost.com/forum_topics/45423-nebius-deployment-clarification) | Whether inference credits cover deployment: no answer at review |
| [45422 Nepal access](https://nebiusglobalaihackathon.devpost.com/forum_topics/45422-token-factory-access-for-participants-in-unsupported-countries-nepal-not-in-billing-list) | Billing blocker; participant describes a Rust coding-agent runtime; no ruling |
| [45412 Pakistan routes](https://nebiusglobalaihackathon.devpost.com/forum_topics/45412-participant-from-pakistan-nebius-billing-not-available-which-route-is-accepted) | Alternate-provider eligibility unresolved |
| [45409 Pakistan credits](https://nebiusglobalaihackathon.devpost.com/forum_topics/45409-not-able-to-get-my-nebius-token-factory-credits-for-pakistan) | Discord referral |
| [45408 Cloud credits](https://nebiusglobalaihackathon.devpost.com/forum_topics/45408-nebius-ai-cloud-credits) | Remote participant access question; no resolution |
| [45407 Physical AI](https://nebiusglobalaihackathon.devpost.com/forum_topics/45407-physical-ai-projects) | Simulation question redirected; current rules include no-hardware language |
| [45402 China onboarding](https://nebiusglobalaihackathon.devpost.com/forum_topics/45402-token-factory-onboarding-blocked-for-china-based-participant) | Discord referral |
| [45387 beginners](https://nebiusglobalaihackathon.devpost.com/forum_topics/45387-can-total-begginers-can-join-this-hackhatthon-with-little-python-experience) | Participant encouragement, not organizer guidance |
| [45379 country restrictions](https://nebiusglobalaihackathon.devpost.com/forum_topics/45379-nebius-token-factory-restrics-some-countries-from-signing-in) | Billing reports and referral |
| [45378 Alpamayo](https://nebiusglobalaihackathon.devpost.com/forum_topics/45378-physical-ai-track-can-we-use-alpamayo-instead-of-the-four-listed-models) | Manager explicitly permits Alpamayo |
| [45370 tokens](https://nebiusglobalaihackathon.devpost.com/forum_topics/45370-tokens) | Card-access question unresolved |
| [45366 simulation only](https://nebiusglobalaihackathon.devpost.com/forum_topics/45366-simulation-only-project-for-physical-ai-track) | Discord referral |
| [45365 no card](https://nebiusglobalaihackathon.devpost.com/forum_topics/45365-token-factory-access-without-a-credit-debit-card) | Delayed credits, card and expired-invite reports |
| [45362 delayed robot](https://nebiusglobalaihackathon.devpost.com/forum_topics/45362-regarding-physical-ai-submission) | Discord referral |
| [45357 China access](https://nebiusglobalaihackathon.devpost.com/forum_topics/45357-cannot-complete-token-factory-onboarding-china-not-in-billing-country-list) | Participant describes IntentRadar; access unresolved |
| [45352 trial versus judging](https://nebiusglobalaihackathon.devpost.com/forum_topics/45352-hackathon-credits-vs-the-30-day-trial-how-do-we-keep-apps-live-for-judging-dec-1-15) | Participant budget/runbook advice; no official guarantee of model continuity or free hosting |
| [45344 solo/team](https://nebiusglobalaihackathon.devpost.com/forum_topics/45344-team-clarification) | Manager confirms either |
| [45334 Pakistan activation](https://nebiusglobalaihackathon.devpost.com/forum_topics/45334-unable-to-activate-nebius-token-factory-credits-from-pakistan) | Participant describes FirmwareProof; later reports support rejection; no alternate-route ruling |
| [45324 team size](https://nebiusglobalaihackathon.devpost.com/forum_topics/45324-how-many-members-can-a-team-have-at-max) | Manager states no maximum |
| [45298 company email](https://nebiusglobalaihackathon.devpost.com/forum_topics/45298-i-have-created-an-account-in-devpost-with-company-email) | Discord referral |
| [45290 Libya](https://nebiusglobalaihackathon.devpost.com/forum_topics/45290-libya-missing-from-nebius-token-factory-billing-country-list) | Discord referral |
| [45288 no card](https://nebiusglobalaihackathon.devpost.com/forum_topics/45288-i-dont-have-access-to-a-card-for-nebuis-token-factory-what-do-i-do) | Discord referral |
| [45280 requirements](https://nebiusglobalaihackathon.devpost.com/forum_topics/45280-requirement-clarification) | External hosting/additional-model questions redirected |
| [45269 proprietary backend](https://nebiusglobalaihackathon.devpost.com/forum_topics/45269-hiii) | SentryNode author asks about closed core; no approval given |
| [45232 Serverless](https://nebiusglobalaihackathon.devpost.com/forum_topics/45232-nebius-serverless) | Manager confirms Serverless optional and reports Cloud-credit top-up prerequisite |

**Recommendation:** pursue Relay only if early customer packets establish the differentiation. If that access or semantic extraction fails, switch promptly to Cutover. Spend the first days trying to disprove the business and technical assumptions; spend the remaining weeks producing evidence that a skeptical judge and a paying buyer can both inspect.
