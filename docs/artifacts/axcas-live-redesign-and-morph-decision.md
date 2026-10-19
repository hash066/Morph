# Axcas Live: implementation plan and honest comparison with Morph

**Decision date:** 19 October 2026, Asia/Calcutta  
**Purpose:** a teammate-ready project specification and decision record for the Nebius x NVIDIA Global AI Hackathon.  
**Status:** proposed redesign; not a statement that the functionality below exists or has passed tests.  
**Recommendation:** pursue Axcas Live if its first-day recovery gate passes. Choose Morph only if a concrete simulation/recovery spike passes the stronger switch gate below. Do not split the remaining schedule between two full builds.

## 1. Executive decision

**Axcas Live is the better execution bet for this team and this deadline. Morph has the higher spectacle ceiling and more natural GPU/simulation fit. Neither currently has evidence supporting a grand-prize prediction.**

The important distinction is between the attractiveness of an idea and the likelihood of delivering its strongest version. Axcas has an existing application foundation. Morph currently has a concept, but no demonstrated environment, controller recovery, baseline comparison, or customer in the material inspected for this decision.

That does not establish that your team lacks robotics ability. It means that ability has not yet been demonstrated in this project. Likewise, an Axcas README is not proof of a working customer journey.

Three uncomfortable truths:

1. A voice-controlled website generator is crowded. Adding NVIDIA branding will not make Axcas original.
2. A robot recovering in simulation is also not a new research category. Using Isaac Lab and presenting a successful trajectory will not establish a new contribution.
3. Adding sponsor services can reduce the quality of the entry if it consumes the time needed to make the core workflow reliable.

**The Axcas claim worth testing:** a nontechnical merchant can change business facts through voice and documents, see the consequences across supported materials, and release a consistent, independently checked version without stale approval authorizing a later change.

**The Morph claim worth testing:** model-guided recovery reaches a fixed task objective after a supported actuator change more efficiently than a conventional optimizer under the same experiment budget.

If neither claim survives a small experiment, neither deserves a confident winner label.

## 2. What the event actually rewards

The official rubric equally weights implementation, design, potential impact, and quality of the idea. The organizer describes scoring each from 1 to 5. There is no published criterion rewarding the number of NVIDIA products used. The entry must genuinely fit a track, function as described, and use an NVIDIA open model with Nebius runtime inference or compute. Existing work needs significant in-period updates and disclosure. The deadline is **30 October 2026, 10:30 PM IST**. Keep a working submission accessible through judging, scheduled to end **15 December 2026**. Judges may rely on submission materials rather than test the app. [S1, S2]

Recommended Axcas track: **Best Apps and Agents**. Recommended Morph track: **Physical AI**. Simulation-only Physical AI is allowed by the stated footage alternative; do not imply real-hardware validation. Check the full rules at submission. [S1]

The public judge research supports attention to evaluation, operational evidence, useful tool execution, and constrained capabilities. These are reasonable presentation priorities, not private knowledge of voting preferences. A good entry should make its evidence understandable to the whole panel.

## 3. Evidence available about Axcas

Read-only review covered the local README, architecture documents, contributor instructions, package scripts, selected domain/release-policy code, historical evidence notes, and the earlier project chat. No fresh installation, full test suite, current provider invocation, or live merchant acceptance run was performed for this planning task.

The inspected checkout was on `codex/intake-continuity-source`; do not assume this is the latest production branch. A previous chat referenced another integration checkout. Before implementation, reconcile branches and determine the intended baseline without resetting or overwriting work.

| Area | What the review supports | What remains unproven now |
|---|---|---|
| Product | WhatsApp-first SME website/reel flow and guided Studio are documented | A new merchant completes the current live flow |
| Data | Typed business/site structures and constrained rendering are present/described | Compatibility with the new change-bundle schema |
| Authority | Builder, verifier, and release roles are intentionally separated | End-to-end enforcement in the current deployment |
| Approval | Selected code binds approved call batches to a scope hash; site approval is described separately | New bundle-wide approval, concurrency, and stale-version checks |
| Deployment | Existing AWS, Cloudflare, and Convex integrations are documented | Current health, access, cost, and reliable recovery |
| Verification | Test infrastructure and historical evidence exist | Current suite results and new redesign behavior |
| NVIDIA/Nebius | A migration is proposed | Working adapters, chosen models, quota, deployment receipts |

Do not reuse historical completion percentages as current evidence. Do not assume the call-batch hash function already implements site-bundle release correctness. Several architecture files explicitly describe older targets; the current scope must be reconciled before editing.

## 4. Product definition: Axcas Live

### One-sentence promise

**Tell Axcas what changed in your business. It prepares the affected customer-facing materials, checks them together, and releases only the version you approved.**

### First customer and supported use case

Start with a home bakery that manages a small catalog through WhatsApp. Support one tested language, one currency, and one timezone per merchant. English is the initial baseline because the existing docs describe English intake; add another language only after testing actual speech and document support.

The initial outputs are:

1. The owned catalog website.
2. Its prefilled WhatsApp inquiry message.
3. One downloadable promotional card or short template-based reel, generated from approved merchant assets.

Use the promotional card first. Video generation is a stretch feature, not the reason the core product exists.

### Concrete journey

Existing approved facts: a chocolate box costs INR 500; Saturday orders close Friday at 6 PM.

The merchant sends a menu PDF and voice note: “Chocolate boxes are now 650. Close Saturday orders at noon on Friday. Use the new menu.” The document says 600.

The system asks: “Your voice note says INR 650, while the menu says INR 600. Which price should I use?” It links both sources. The merchant confirms 650.

Axcas proposes a versioned change bundle: catalog price, inquiry message, ordering cutoff, and promotional card. It flags the previous card as stale within Axcas. It cannot retract a file somebody already downloaded or a post on an unintegrated social account.

The verifier checks the candidate site and structured artifacts. The merchant sees a compact before/after preview and approves the exact bundle. The owned public route switches to the new bundle; download links identify the version.

If the merchant changes the price again while approval is pending, the previous approval cannot authorize the new content. If a newer version has already been published, the old pending candidate cannot overwrite it without revalidation.

### What this does not promise

- No autonomous management of an entire business.
- No payment processing, fulfillment proof, inventory reservation, or inferred sales from clicks.
- Capacity is a merchant-provided fact unless a real order ledger is built separately.
- No automatic outbound calls or social publication in the hackathon version.
- No automatic deletion of already shared assets from third-party systems.
- No promise that passing a consistency check proves a price is commercially correct.
- No generic arbitrary-code website builder.

## 5. Scope and user experience

### P0: required for a complete entry

- Existing-merchant onboarding and one working identity/approval path.
- Text intake plus a tested voice path; one supported PDF document format.
- Source-linked extraction into proposed facts.
- Explicit contradiction handling and a consolidated clarification question.
- Typed change planning across the three outputs.
- Immutable candidate versions and independent verification.
- Approval tied to merchant, exact bundle, and expected current version.
- Deterministic promotion with concurrency protection and idempotent retries.
- Viewable proof record, failure messages, and a release history.
- At least one genuine merchant pilot and an independently reproducible test set.

### P1: only after P0 passes

- OpenShell integration if the chosen environment passes a compatibility spike.
- A short approved reel made from supplied assets.
- A second language with evaluated speech/extraction quality.
- A scheduled probe of the owned site and a merchant-visible regression notice.

### Explicitly defer

Custom model training, generated product imagery, arbitrary video models, multiple business verticals, autonomous pricing, social platform publication, cold outreach, a new payment stack, and a complete database/frontend migration.

### Merchant interface

Keep the merchant flow to four states: **understanding your update**, **one question needed**, **ready to review**, and **published / unable to publish**. Show source conflicts and plain explanations, not orchestration jargon. The review should show changed facts, affected outputs, and unresolved blockers. Use “verified for these checks” rather than a universal green safety badge.

Developer/judge evidence belongs on a separate read-only page: model/version, tool calls, candidate hash, assertions, timings, costs, and failure traces. Redact merchant data and credentials.

## 6. NVIDIA and Nebius architecture

```text
Merchant WhatsApp / authenticated Studio
  -> authenticated intake + immutable source assets
  -> speech/document adapters
  -> source-linked candidate facts
  -> clarification when evidence conflicts
  -> Nemotron change planner on Nebius Token Factory
  -> deterministic typed patch + dependency compiler
  -> immutable bundle + private candidate rendering
  -> independent verifier on Nebius compute
  -> exact merchant approval
  -> deterministic release service
  -> owned public site + versioned assets + evidence receipt
```

| Component | Role | Adoption gate |
|---|---|---|
| Nemotron via Token Factory | Interpret changes, identify ambiguities, propose typed operations | Real structured-output/tool-call test on the selected account |
| NVIDIA speech model | Voice transcription | Confirm license, language, model revision, memory, and accuracy on merchant-like recordings |
| Nemotron Parse | Parse supported menu/price-sheet PDFs | Extract amounts, item names, and locations from representative samples |
| Nebius Jobs or suitable AI Cloud compute | Isolated browser checks, batch evaluations, asynchronous processing | Verify browser dependencies, networking, timeouts, resource availability, and cost |
| Nebius endpoint or supported VM/container | Serve speech/document models when self-hosting is appropriate | Measure cold start, concurrency, memory, and operational burden |
| OpenShell | Additional process/filesystem/network isolation for the agent | Test actual enforcement on the chosen deployment; never auto-broaden policies |
| Existing Cloudflare/Convex interfaces | Identity ingress, state, owned public pages where already reliable | Retain proven boundaries; avoid an unnecessary rewrite |

NVIDIA speech and document models are not assumed to be available through Token Factory. Self-host where supported and licensed, or document an honest fallback. OpenShell is not a substitute for tenant authorization, fact validation, or release policy. Browser verification is often CPU work; allocating a GPU to it just to show usage is wasteful. [S3-S7]

Pin actual model IDs and revisions only after a smoke test. “Nano,” “Super,” and “Ultra” labels do not prove account availability or interchangeability. Record endpoint, revision, decoding settings, and prompt version in evaluation receipts.

### Minimum and richer sponsor integration

**Minimum useful integration:** Nemotron plans real changes on Token Factory and Nebius compute executes actual independent verification/evaluations.

**Richer integration:** add one proven speech model and document parser hosted on Nebius; add OpenShell only after the base journey works. Prefer three well-tested components to six fragile ones. Cosmos and GR00T have no justified role in this merchant workflow.

## 7. Data model and state machine

Use existing tenant identity and canonicalization patterns where appropriate. These are proposed contracts, not claimed existing types:

```ts
type SourceEvidence = {
  id: string; merchantId: string; assetHash: string;
  kind: 'text' | 'audio' | 'pdf';
  location: string; // message span, audio timestamps, or page/region
  receivedAt: string;
};

type BusinessFact = {
  id: string; merchantId: string; entityId: string;
  field: string; value: unknown; unit?: string;
  effectiveFrom?: string; sourceIds: string[];
  status: 'proposed' | 'confirmed' | 'superseded';
};

type ChangeBundle = {
  id: string; merchantId: string; baseVersion: string;
  factSnapshotHash: string; artifactManifestHash: string;
  contractHash: string; bundleHash: string;
  status: 'needs_clarification' | 'draft' | 'verifying' |
    'blocked' | 'awaiting_approval' | 'approved' |
    'published' | 'superseded' | 'failed';
};
```

Implement monetary amounts as integer minor units with currency, explicit units for quantities, and timezone-aware cutoffs. Normalize entity identity: “choc box” and “chocolate box” can be proposed as a match, but ambiguous variants require clarification.

Keep source observations separate from merchant-confirmed facts. Never silently choose between contradictory sources just because one is newer. A merchant answer must identify which conflict it resolves. Do not allow uploaded text to issue tool instructions.

Build a small explicit dependency map: `product.price -> catalog.price, inquiry.price, promo.price`. A model can propose relationships, but only supported, reviewed mappings enter the compiler. This is not a universal semantic dependency graph.

### State transitions

1. Accept authenticated input and assign an idempotency key.
2. Store immutable evidence; extract proposed facts.
3. Resolve ambiguity or enter `needs_clarification`.
4. Freeze confirmed fact snapshot and generate a draft bundle.
5. Compile independently reviewable assertions from confirmed facts, not from generated copy alone.
6. Verify all supported artifacts; any blocker enters `blocked`.
7. Request approval for the exact verified bundle and base version.
8. At release time, recheck approval, verification freshness, tenant identity, and current version.
9. Atomically compare-and-swap the owned publication pointer; write the release event.
10. Mark displaced pending candidates as superseded where their assumptions are no longer valid.

Do not claim atomic updates across unrelated external platforms. This plan owns one publication manifest and its asset references. Artifact creation can happen before promotion; the public pointer changes only after readiness checks. Downloads already outside the service remain outside its control.

### Release predicate

Release requires all of: authorized merchant; matching bundle/contract/evidence hashes; no unresolved source conflict; all blocking assertions passed; unexpired approval; matching expected base version; no prior completed release for the idempotency key. Use a transaction or equivalent supported concurrency primitive. A mismatch returns a specific blocker and cannot be overridden by the language model.

Rollback changes the public pointer to a retained version under explicit policy; it does not undo customer actions or retract externally shared material. A newer legitimate merchant change must not be overwritten by an older rollback job.

## 8. Independent verification

The verifier receives a candidate URL, allowed artifact IDs, frozen assertions, and a scoped result capability. It receives no build, promotion, unrestricted storage, or provider credentials. Both the builder and verifier treat page/document content as untrusted.

For each assertion, record expected value, observed value, source, candidate version, check method, timestamp, and status: pass, fail, unsupported, or inconclusive. Unsupported/inconclusive blockers cannot become passes.

Required checks:

- Catalog price and currency equal the confirmed fact.
- Product identity and quantity units match the intended variant.
- WhatsApp inquiry text references the correct item, amount, and recipient.
- Cutoff and timezone agree across supported surfaces.
- Template-rendered promotional text matches the fact snapshot.
- No reference to an obsolete price remains in the current owned bundle.
- The site loads on a supported mobile viewport; links and selected assets resolve.
- Approval for version A cannot authorize version B.
- A concurrent release cannot overwrite a newer base version.
- Replay of a callback or release request does not duplicate publication effects.
- A tenant cannot access another tenant's asset, evidence, or release endpoint.

Do not call a redirect an order confirmation. If generating a visual card, compare its structured text manifest and render output; spot-check pixels/OCR as a secondary check. Model agreement alone is not independent proof.

## 9. Implementation work packages

These are logical owner assignments for the team, not instructions to start new chats or deploy agents automatically.

| Package | Owner profile | Deliverable | Acceptance gate |
|---|---|---|---|
| A. Baseline recovery | Full-stack/infrastructure | Agreed source baseline, current tests, one fresh merchant journey | G0 |
| B. Model adapters | ML/backend | Typed Nemotron adapter, voice/PDF smoke tests, cost receipts | G1 |
| C. Change compiler | Backend/domain | Source facts, dependency map, immutable bundle, conflict resolution | G2 |
| D. Verification/release | Backend/test | Independent assertions, exact approval, transactional publication | G3 |
| E. Product/evidence | Frontend/product | Review UI, read-only proof page, pilot, demo | G4 |

Inspect the existing `packages/domain`, renderer, release-policy, verifier runner, Hermes boundary, and Convex modules before deciding exact new paths. A proposed `change-bundles` domain module and a thin model adapter are reasonable; do not create a second parallel release authority.

The repository instructs that agents modify validated specs, not runtime page code. Preserve that boundary. Retain existing test conventions and update current architecture/evidence documents as work is completed. This plan is not authorization to reset branches or deploy infrastructure.

### Runtime behavior and failure handling

- Give every model call and background job a bounded timeout, retry policy, and correlation ID.
- Retry transient reads safely; side-effecting operations require deduplication and state checks.
- Malformed model output gets bounded repair attempts, then a visible blocked state.
- Lost provider responses require reconciliation; do not blindly repeat an external action.
- Job outputs are immutable and bound to the input bundle hash.
- A missing model/provider must remain visible as a limitation; never substitute a scripted result while presenting it as model execution.
- Keep personal data out of public traces; provide deletion and retention controls consistent with the pilot agreement.

## 10. Schedule and go/no-go gates

All dates below are IST. There are about eleven days until the deadline; avoid describing this as a comfortable research window.

| Date | Work | Required exit evidence |
|---|---|---|
| Oct 19 | Baseline recovery; obtain model/quota access; identify one pilot merchant | G0: current baseline installed, existing journey traced, blockers recorded |
| Oct 20 | One voice/document change through real Nemotron to a typed candidate | G1: model receipts, source conflict, accepted clarification |
| Oct 21-22 | Fact snapshot, dependency map, three artifacts, review interface | G2: unseen price/cutoff updates produce consistent candidates |
| Oct 23-24 | Independent verifier, exact approvals, concurrency and retries | G3: stale approval and stale base version both blocked |
| Oct 25-26 | Merchant pilot, frozen evaluation, cost/latency measurement | G4: independently reproduced flow and published results |
| Oct 27 | Only essential fixes; finish evidence viewer and source disclosure | No critical unresolved release/tenant failures |
| Oct 28 | Feature freeze; fresh-machine install; record video | Reproducible submitted build |
| Oct 29 | Complete submission, rights/license review, access check | Submit early where possible |
| Oct 30 | Buffer only; final access verification | Deadline 10:30 PM IST |

**G0 failure:** if the baseline is still not recoverable by the end of Oct 20, withdraw the assumption that Axcas is the easy option. Do not automatically switch to Morph; Morph must independently pass its switch gate. Reduce Axcas to a supported change workflow only if it remains useful and honestly demonstrable.

**G3 failure:** if approval binding or publication correctness is broken, stop feature work. A prettier demo cannot compensate for an agent releasing the wrong business facts.

## 11. Evaluation plan

Create a frozen set of at least 30 small cases before final tuning: 10 straightforward updates, 8 source conflicts, 6 stale-version/concurrency/retry cases, and 6 ambiguous or unsupported inputs. Include at least five consented merchant-derived cases where available; distinguish them from synthetic cases. Split by scenario/template so near-duplicate wording does not leak from development into held-out evaluation.

Compare:

1. A form/template workflow without model reasoning.
2. A single-pass model that drafts outputs without the change/verification loop.
3. Axcas Live's complete pipeline.

Metrics:

- Correct fact extraction and correct ambiguity detection.
- End-to-end task completion with merchant-approved ground truth.
- False contradiction warnings and unnecessary clarification turns.
- Unsupported inputs correctly left unresolved.
- Stale/unauthorized release attempts blocked in the tested suite.
- Median and tail completion time, including cold starts separately.
- Cost per successfully verified bundle, including retries and failed jobs.
- Merchant time and assistance needed compared with the baseline.

Initial acceptance targets, not achieved results: all designed stale-approval/tenant/concurrency tests must pass; at least 90% correct outcomes on supported ordinary cases in the frozen set; no silently released conflicting amount; at least one merchant completes the journey without developer intervention. These small-sample results do not establish universal reliability.

Freeze assertions independently of proposed repairs. A repair cannot make itself pass by editing the acceptance condition. Keep failed attempts in the evidence package.

## 12. Compute and cost discipline

Do not infer credit eligibility, quotas, or GPU availability from registration. Record actual account entitlements and model access on Oct 19. Do not launch paid workloads solely because this plan exists.

Budget formula:

`cost per successful change = (inference + speech/document hosting + verification jobs + rendering + allocated idle time) / successful verified changes`

Choose a team-approved total spend cap before provisioning. Log model tokens, job runtime, GPU/CPU allocation, failed retries, and endpoint idle time. Set job duration and concurrency caps. Warm only what the demo needs; retaining a giant GPU endpoint for a small document workload may make the product uneconomic.

If self-hosted speech or document parsing is too expensive or unreliable, preserve the core Nemotron + verification contribution and label the reduced scope. Explain the tradeoff rather than adding an unused service to the architecture slide.

Keep the judge-facing deployment funded and available through the judging window. Separate the merchant environment from a resettable evaluation tenant. The judge tenant should not send real customer messages or publish to a real merchant without their authorization.

## 13. Three-minute submission story

Target 2:50 to leave buffer.

| Time | Screen/action | Evidence |
|---|---|---|
| 0:00-0:20 | Real merchant explains one update problem; show existing materials | Specific user and task |
| 0:20-0:50 | Voice + PDF disagree; Axcas asks one useful question | Real extraction and source locations |
| 0:50-1:20 | Merchant answers; affected outputs are prepared | Change bundle, before/after preview |
| 1:20-1:50 | A deliberately stale artifact fails verification | Actual failed assertion, labeled injected fault |
| 1:50-2:15 | Correction passes; stale approval is rejected | Exact version evidence |
| 2:15-2:40 | Merchant approves current bundle; public site works | Runtime release and browser checks |
| 2:40-2:50 | Show measured results and sponsor execution trace | Real sample size, latency/cost, honest limitations |

Do not pretend long jobs happened instantly. Mark time compression and prerecorded stages. Never describe simulated inquiries as customers or click counts as revenue. Keep the video's central story about the merchant, not the infrastructure inventory.

## 14. Commercial test

The near-term buyer hypothesis is a merchant or small agency repeatedly maintaining a small catalog and promotional assets. The pain must occur often enough to justify a subscription. A one-time launch service is not automatically recurring software revenue.

Interview five users about their last actual pricing/menu change: how many places were edited, what became inconsistent, how long it took, and who corrected it. Have two try a real update and ask one to pay for a small ongoing pilot. Do not select a subscription price from a desired million-dollar ARR calculation.

Potential packaging: monthly merchant plan with a bounded number of verified updates, or an agency plan managing several merchants. Watch onboarding labor, messaging charges, inference, and support. Shopify Sidekick already offers broad commerce assistance; the product must win a specific workflow through lower effort or better consistency, not just natural-language interaction. [S8]

Reject the commercial thesis if users mostly need a one-time website or if a simple shared catalog/form solves their problem just as well. Revenue and acquisition outcomes remain unproven.

## 15. Reassessing Morph without hype

### Strongest feasible interpretation

Morph is a simulation-based recovery workbench for one robot/controller family. After a supported actuator-efficiency change, it searches a bounded controller parameter space and evaluates recovery on held-out conditions.

Start with a small mobile robot with redundant actuation or a deliberately chosen task that remains physically achievable after the supported change. Do not disable a critical joint and assume the original task is still feasible. Include an impossible case and require the system to report failure rather than redefine success.

Use Isaac Lab/Isaac Sim only after confirming a stable supported version, GPU/driver compatibility, headless operation, assets, and reproducible installation. Do not choose a beta solely for novelty. [S9]

### Proper sponsor role

- NVIDIA simulation software provides the environment and parallel trials.
- Nebius GPU compute runs actual rollouts/optimization, with logs and costs.
- An NVIDIA open model on Token Factory interprets telemetry and proposes bounded hypotheses or candidate search regions.
- A numerical controller executes fast actions and a fixed evaluator determines success.

Isaac simulation alone does not satisfy the open-model requirement. A Nemotron narration panel is insufficient as a technical contribution. To justify the model, show that its experiment choices improve recovery efficiency or another predefined outcome compared with an equally budgeted baseline.

Do not add Cosmos-generated videos as evidence that a controller works. Use real simulator rollouts. Do not claim GROOT applies to the chosen robot without checking embodiment and action-space compatibility.

### One-day Morph switch gate

Before choosing Morph, a named team member must produce all of:

1. A reproducible supported environment running on available Nebius compute.
2. A baseline controller reaching a fixed task objective across several seeds.
3. A supported perturbation that degrades that controller without making the task impossible.
4. A conventional recovery baseline, such as random search or a suitable optimizer, with bounded candidate evaluations.
5. A model-guided candidate-selection loop using the same action space, objective, and evaluation budget.
6. Recovery on at least five held-out conditions, with every trial retained, including failures.
7. An interpretable advantage or a clear hypothesis supported by initial data; one lucky trajectory is insufficient.

This is a screening experiment, not a publishable result. For the final submission, expand seeds and variation, report dispersion, count model overhead, and keep the evaluator frozen. A robot recovering only after the system weakens the task does not count.

### Why Morph is risky

Robot adaptation and morphology-conditioned control already exist, including MetaMorph. [S10] An impressive moving robot is not automatically original. The team must distinguish its recovery protocol, evaluation, or practical workflow. It must also explain who would pay; robotics customers require much more evidence than a simulation clip.

There is no current evidence in this conversation that a compatible simulator, usable controller, recovery method, or robotics pilot exists for your team. This is the principal reason Morph is not the default recommendation. Generic confidence in a strong team does not remove these dependencies.

## 16. Side-by-side decision

The judgments below are qualitative. No prototype was evaluated, so numerical predicted judge scores would create false precision.

| Dimension | Axcas Live | Morph |
|---|---|---|
| Immediate visual spectacle | Moderate; needs a clear human story | High if recovery genuinely works |
| Natural NVIDIA/GPU fit | Strong model/speech/document stack; many checks are CPU work | Strong simulation/GPU fit; model contribution still must be justified |
| Reusable work evidenced here | Application code, schemas, approval/verification structure | No demonstrated project foundation |
| Main technical unknown | Whether the current live flow can be recovered and safely extended | Whether recovery works and beats a conventional baseline |
| Originality | Modest unless cross-artifact change handling is strong | Modest unless recovery/evaluation adds beyond prior work |
| Design by Oct 30 | More plausible if baseline recovery succeeds | Higher risk of a technical prototype with weak product experience |
| Impact evidence | Merchant trials can be arranged quickly through claimed distribution | Requires a robotics user's validation; simulation alone is limited |
| Commercial path | Earlier small paid pilot, but crowded and potentially low willingness to pay | Potential specialist value, but long validation/sales path |
| Failure mode | A polished wrapper around templates and approvals | A canned robot demo with an LLM narrating it |
| Default choice today | Yes, conditional on G0/G1 | No, unless the switch gate is already achievable |

### Firm recommendation

**Build Axcas Live for this deadline if it passes G0 and G1.** Its advantage is execution leverage and accessible user validation, not a belief that it is inherently more innovative than Morph.

**Switch to Morph only if the one-day recovery gate produces real evidence and someone owns the robotics work.** A successful Morph spike can change the recommendation because it resolves the main uncertainty. Liking Morph more, having a better-looking animation, or installing Isaac Lab does not resolve it.

If your sole objective were a longer-term robotics research project, Morph could be the more interesting choice. For this hackathon on 19 October, with the evidence available, choosing it from scratch is a high-variance gamble.

Do not spend the next several days re-ranking ideas. Make the decision using the first experiment, then preserve enough time for design, evaluation, and submission quality.

## 17. Final acceptance checklist

- [ ] Baseline branch and inherited functionality identified; no history rewritten.
- [ ] Fresh installation and relevant current test suite pass.
- [ ] Real Nemotron runtime calls on Nebius recorded.
- [ ] Supported voice/document inputs tested; unsupported cases clearly handled.
- [ ] Three artifacts agree with confirmed facts in held-out cases.
- [ ] Independent verifier has no release authority.
- [ ] Stale approval, stale base version, replay, and tenant isolation tests pass.
- [ ] At least one real merchant trial completed, with consented evidence.
- [ ] Evaluation includes simple baselines, costs, latency, and failures.
- [ ] Sponsor integrations have demonstrated roles; no unused logos.
- [ ] Existing project and new in-period contributions disclosed precisely.
- [ ] Dependencies/assets are licensed and public repository is reproducible.
- [ ] Judge-accessible environment contains no private merchant material.
- [ ] Public video is under three minutes and matches the submitted build.
- [ ] Deployment remains available and funded through judging.

## 18. Sources and research limits

Sources reviewed for this plan on 19 October 2026 or in the immediately preceding research. Availability and product details must be rechecked during integration. Local source review was limited as described in section 3.

- **S1:** [Official hackathon rules](https://nebiusglobalaihackathon.devpost.com/rules) - requirements, dates, testing, existing projects, rubric, and submission terms.
- **S2:** [Organizer explanation of judging](https://nebiusglobalaihackathon.devpost.com/updates/46204-here-s-how-judging-works) - 1-5 equally weighted criteria and stronger track examples.
- **S3:** [Nebius Nemotron inference](https://nebius.com/services/token-factory/models/nvidia-nemotron-models-inference) - model-serving direction; exact account availability remains a deployment check. A direct refresh failed during this turn; prior research established the page.
- **S4:** [Nebius Serverless AI](https://dev.nebius.com/serverless) - Jobs and Endpoints concepts; verify actual runtime capabilities and quotas.
- **S5:** [NVIDIA Nemotron Parse documentation](https://docs.nvidia.com/rag/latest/nemotron-parse-extraction.html) - document extraction integration.
- **S6:** [NVIDIA Parakeet model card](https://build.nvidia.com/nvidia/parakeet-ctc-1_1b-asr/modelcard) - example speech model; not a claim of universal language support.
- **S7:** [NVIDIA OpenShell developer guide](https://docs.nvidia.com/openshell/latest/home) - sandbox and policy interfaces; deployment enforcement must be tested.
- **S8:** [Shopify Sidekick](https://help.shopify.com/en/manual/ai-powered-tools/sidekick) - important commerce-assistant overlap.
- **S9:** [Isaac Lab installation documentation](https://isaac-sim.github.io/IsaacLab/develop/source/setup/installation/index.html) - simulator installation and requirements; pin a tested stable release for the project.
- **S10:** [MetaMorph research](https://metamorph-iclr.github.io/site/) - prior morphology-conditioned control, not evidence of the proposed Morph prototype.

This document is a build and decision plan, not proof of novelty, market demand, financial returns, security certification, or a likely prize. The strongest next evidence is a reproducible core experiment and a real user completing the task.
