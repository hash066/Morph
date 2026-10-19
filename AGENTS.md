# Morph project instructions

## Mission and scope
Build the Morph product described in docs/PRODUCT_PLAN.md and the matching final PDF in docs/artifacts. Work only in E:/Winter/Morph. This is a fresh implementation. Do not modify E:/Projects/axcas or the other new project. The user has authorized starting implementation and wants visible progress.

Read BOOTSTRAP.md, docs/ARTIFACT_INDEX.md and the matching build-agent prompt file. Current user constraints and this project scope supersede obsolete scope in historical artifacts. In Axys, real Instagram connection/publishing is required; the old private-reel-only/AWS architecture is historical.

## Spending constraints
No new paid services, subscriptions, payment-method enrollment or purchases. Use local tools, existing authorized access and available hackathon credits only. Never assume quota, credit availability or free tiers. Verify before provisioning. Set explicit budgets and stop rules; if spend cannot be bounded by approved existing credit, record the affected live gate as blocked and continue independent work. Do not read unrelated credential stores or print secrets.

SocialClaw is not a default dependency. The user permits it in principle only if it introduces no additional payment and meets the full product requirements. Prefer direct Meta integration for Axys. Evaluate SocialClaw only if already available at zero incremental cost; document capabilities and approval requirements. Do not sign up, subscribe or silently replace the connection flow.

## ECC guidance
Local ECC: D:/Leave/EL/AIML/third_party/ECC, inspected revision 76aaa77. Read relevant complete skill files selectively. Start with verification-loop, api-design, eval-harness, security-review; use frontend-design-direction/e2e-testing for UI, agent-security-hardening for tool actions, python-testing for Morph and cost-aware-llm-pipeline for inference. Exact paths and caveats are in docs/artifacts/agent-prompts-start-here.md.

Do not install ECC globally or enable hooks/background services just to use its guidance. Do not inherit example model IDs, shell commands, third-party services or agent model overrides. NVIDIA/Nebius remains central. Use official current documentation for provider and simulator interfaces.

## Evidence and progress
Maintain docs/STATUS.md and docs/EVIDENCE.md after meaningful milestones. Label implemented, locally tested, live-provider verified, simulation evaluated and hardware tested separately. Missing access never becomes fabricated success. No invented metrics, participant sessions or customer quotes.

Use scoped ownership if delegating; one lead owns shared schemas, migrations and root lockfiles. Complete concrete implementation, tests and reviewable artifacts before requesting necessary external actions. Social publication requires scoped account/content authorization; robot movement requires an approved supervised setup. Starting this coding task is not permission to post arbitrary content or move hardware.
