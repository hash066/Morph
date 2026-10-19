# Axys: copy-ready build prompts

Use the shared specialist contract in `agent-prompts-start-here.md`. Give the lead prompt first; specialist assignments follow after shared interfaces are established.

## Lead agent prompt

```text
Build AXYS, a fresh implementation of the complete Axcas product for the Nebius x NVIDIA hackathon. Implement the application; do not merely produce another plan or landing page.

Read this specification PDF:
C:/Users/asus/Documents/Codex/2026-10-03/https-nebiusglobalaihackathon-devpost-com-ref-content/outputs/axys-full-rebuild-plan.pdf
If you are on another machine, ask for or use the attached PDF rather than inventing its contents.

Product: merchant voice/text/photos -> confirmed business facts -> generated editable website AND reel -> merchant approves exact versions -> deployed website AND genuine Instagram publication -> real available analytics -> proposed coherent revision. Preserve the guided Website/Reels/Both studio. Keep WhatsApp intake as a scoped adapter alongside browser intake; establish the complete web-to-Instagram path first. No replacement of Instagram publishing with a download-only workflow.

Use the fresh project workspace provided for this task. If opened in E:/Projects/axcas, leave that repository unchanged and establish a separate fresh sibling checkout, checking parent instructions first. The old repository is reference material only. Its previous AWS/Bedrock focus and prohibition on automatic posting do not define this new project. Preserve useful product concepts, asset rights and any required attribution; do not copy code without recording provenance.

Use Nemotron through Nebius Token Factory for core campaign planning and tool decisions. Verify available model IDs with the actual account and pin them. Verify current official Nebius and Meta documentation rather than guessing APIs. Optional NVIDIA speech should be deployed on compatible Nebius compute and explicitly tested; do not assume text endpoint access implies ASR/TTS access. Do not add Cosmos/GROOT to this product just for branding.

Start by reading applicable repository instructions and relevant ECC skills at D:/Leave/EL/AIML/third_party/ECC: api-design, security-review, eval-harness and verification-loop. Read skill files completely when using them. Use frontend-design-direction for the studio. Read the adjacent prompt-pack guide for verified paths and cautions. Do not install ECC globally or activate its hooks as a prerequisite.

Choose a small deployable architecture: TypeScript/React studio and typed renderer, Node API/worker, relational durable state, private object storage and durable jobs. Prefer one package manager and a lockfile. Use Zod/JSON Schema at model and API boundaries. Pick and pin actual supported dependencies after inspection. Record decisions rather than debating stacks indefinitely.

Before parallel implementation, create docs/BUILD_CONTRACT.md, docs/INTERFACES.md, docs/STATUS.md and docs/EVIDENCE.md. Establish Campaign, Product, Asset, SiteVersion, ReelVersion, Approval, Connection, PublishAttempt and MetricSnapshot contracts. Define tenant ownership, artifact hashes, idempotency and independent channel states. Assign exclusive component ownership; the lead owns shared schemas, root dependencies and migrations. Freeze initial interfaces, then delegate or execute the specialist assignments sequentially.

First milestone: a real Nemotron response, one rendered/deployed website, one real authorized Instagram test publication and retrieval of its confirmed identifier/permalink. Start Meta OAuth/account access immediately; it is a schedule dependency. App-role testing and public merchant onboarding are different capabilities. Record which is actually available. If missing credentials or review status block the live test, finish the adapter and fixtures, record the exact blocker and continue independent work. Do not claim the milestone passed.

Build the studio around Brief, Create, Review, Publish and Results. One campaign drives page facts, storyboard, caption and offer destination. Provide mobile/desktop site previews, final encoded video preview, editing and visible pending/error states. Approval must bind exact artifact versions, caption, account and schedule. Changes invalidate approval. Model-generated arbitrary executable page code is out of scope.

Publishing must survive restart and ambiguous provider timeouts. A site success plus Instagram failure is PartialFailure. Reconcile before retrying uncertain publication. Never show Published before confirmed provider evidence. Insights absent or delayed are Unknown, not zero. Visits/contact clicks are not purchases or causal sales lift.

Implement tenant isolation, encrypted server-side OAuth secrets, OAuth state validation, media URL restrictions, upload validation, bounded jobs, redacted logs, disconnect and retention controls. The model proposes tool calls; deterministic code authorizes and executes them. Add per-campaign/account spending limits and use real measured cost data, not hardcoded marketing estimates.

Acceptance: a new merchant can complete the full path; a price/time edit propagates across surfaces; stale approval is rejected; duplicate clicks/retries do not duplicate publication; revoked access fails clearly; two tenants cannot access each other's assets or connections; the real final video renders and publishes; results show provenance/timestamps. Test the behavior, not just mocked method calls.

Provide local setup, .env.example with names only, migrations, container/deployment configuration, health checks, CI, browser tests, meaningful unit/integration tests, provider smoke-test commands, rollback/recovery guidance and a demo runbook. Separate local/mock CI from opt-in authorized live tests. Run relevant checks and visually inspect the real application. Fix failures before calling a gate complete.

Recruitment and external social actions require actual consent. Prepare the five-merchant study protocol and evidence template without inventing results or contacting anyone automatically. Prepare a sub-three-minute demo script based only on completed evidence. Keep the app usable through judging. Recheck the current official rules before submission packaging; do not submit or publish the repository without the user's applicable authorization.

Work until the full authorized implementation is complete or precise external blockers remain. Keep progressing on independent tasks. End each milestone with shipped behavior, commands/results, evidence paths and next gate; do not label the whole product production-ready from a passing unit suite.
```

## A1 — Campaign intelligence and contracts

```text
Own packages/campaign and packages/inference after agreement with the lead. Use ECC api-design, eval-harness, cost-aware-llm-pipeline and agent-security-hardening.

Implement the actual Nebius Token Factory adapter and constrained Nemotron tool loop for brief extraction, missing-fact questions, SiteSpec/ReelSpec generation and consistent revisions. Validate schemas server-side. Keep model IDs configurable and verify supported capabilities, streaming/tool behavior and error formats from official documentation and live smoke tests. Record model/configuration, input version, request IDs, latency, usage and pricing provenance.

Facts must retain merchant/source provenance. Missing price, ambiguous date, unsupported claim and absent asset are repairable states. Never invent testimonials, inventory or discounts. Extract user intent from uploaded content without obeying embedded instructions to publish or reveal secrets. Limit retries, tokens and tool iterations. Never fall back to another vendor silently.

Deliver 20 representative development cases, a held-back regression set, deterministic price/date/product checks and model-output quality evaluation. Compare coordinated revision against a simpler generation baseline. Make speech optional until a supported NVIDIA deployment is tested. Hand off real contracts and adapters, not fake text generation hidden behind a live label.
```

## A2 — Studio, website and reel rendering

```text
Own apps/studio and packages/renderers. Use ECC frontend-design-direction and e2e-testing; optionally read the local frontend-design skill listed in the guide.

Build the usable merchant workflow, not just a marketing page. Use realistic sample merchant assets explicitly labeled as samples. Implement Brief/Create/Review/Publish/Results, accessible responsive navigation, account status, side-by-side previews and edits. Render validated SiteSpec through controlled components with three polished layout families. Implement two reel styles using actual media composition and encoded output. Preview the final file and validate target-platform constraints using current documentation.

Provide loading, empty, validation-error, partial-success, expired-connection and retry states. Connect the real API as it lands. Fixtures are acceptable for isolated component development but must never masquerade as connected accounts or successful publication.

Check mobile/desktop widths, keyboard navigation, contact links, broken images, subtitle placement and video duration/audio. Capture and inspect screenshots and the actual video. Test that changed price/time appears consistently in page, reel and review panel. Avoid exposing agent/infrastructure jargon in merchant screens. Hand off browser traces and artifact paths.
```

## A3 — Instagram, persistence and publication

```text
Own services/publishing and the approved provider adapters. Coordinate database migrations through the lead. Use ECC security-review, agent-security-hardening and api-design. Do not use ECC social-publisher/SocialClaw as a substitute for the requested direct Meta integration.

Implement one verified Instagram authentication route end to end. Keep the route's scopes, tokens and account IDs consistent. Explain professional-account eligibility, app-role testing and public-customer review requirements. Build secure callback/state handling, encrypted token storage, refresh where supported, disconnect and permission diagnostics. Never request account passwords.

Implement container creation, processing polling, publish, reconciliation and confirmed media/permalink retrieval. Use durable attempts and idempotency keys; prevent duplicates after double-clicks, timeouts, retries and restarts. Bind actions to exact merchant approval. Keep website and Instagram publication states separate. Validate externally fetched media and retain it for provider processing without exposing other private assets.

Implement insight snapshots with version/metric provenance and missing-data states. Do not infer purchases or per-reel attribution that the provider does not supply. Provide fixtures for provider failures plus an opt-in real smoke test requiring the owner's scoped test-post approval. A live gate passes only with actual receipts. Document any app-review blocker exactly.
```

## A4 — Independent verification and delivery

```text
Own tests/e2e, docs/evidence and deployment verification; do not rewrite other agents' product code without coordinating. Use ECC verification-loop, e2e-testing, security-review and eval-harness.

Test the complete merchant journey using the running application. Check tenant isolation, stale approvals, worker restart, timeout reconciliation, duplicate prevention, revoked tokens, incomplete inputs, broken media and UI partial states. Use fixtures for failure injection but require separate real provider evidence for publication. Verify independent assertions against outputs, not the same transformation code being tested.

Review secrets/logs, dependency licenses, provenance, spending caps, health checks and recovery runbooks. Produce a matrix of requirement, test, result, evidence and live/fixture classification. Prepare a five-merchant study script, anonymous result sheet and sub-three-minute demo outline. All unperformed tests stay Not run. Run the relevant build/types/lint/tests and browser checks; report actual failures, not generic assurances.
```

## Final acceptance prompt

```text
Audit Axys against the specification and docs/BUILD_CONTRACT.md. Independently attempt the full workflow from a clean session. Produce a requirement-by-requirement PASS/FAIL/BLOCKED matrix with evidence. Prioritize defects that make a demo misleading: download-only Instagram flow, fixture metrics, stale approval acceptance, cross-tenant access, duplicate publication, silent provider fallback and UI success before provider confirmation.

Fix implementation defects in the authorized scope and rerun affected checks. Do not weaken tests or silently remove requirements. Distinguish code complete, locally verified, live-provider verified and merchant validated. State the exact remaining human/provider steps. Finish with a reproducible demo runbook and only claims supported by the evidence bundle.
```
