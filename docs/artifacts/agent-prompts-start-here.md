# Build-agent prompt pack

Prepared 19 October 2026. These prompts build the products described in the two accompanying PDFs; they do not claim either application has been implemented or tested yet.

## How to use

1. Choose Axys or Morph. Give that project's **Lead agent prompt** to one agent in a fresh project folder. Attach the corresponding PDF, or make its path accessible.
2. Let the lead establish the repository, contracts and file ownership before giving the specialist prompts to other agents. Paste the shared contract plus the relevant specialist prompt into each separate agent session.
3. Use separate branches/worktrees if available. One owner changes shared schemas, dependencies and migrations. The lead integrates and runs cross-component tests.
4. If you have only one agent, give it the lead prompt and ask it to execute the specialist workstreams sequentially. There is no requirement for an agent swarm.
5. Run the final review prompt after integration. A mocked integration can pass local tests but cannot pass a live-provider gate.

Files:
- `axys-build-agent-prompts.md`: lead, four specialist assignments and final acceptance prompt.
- `morph-build-agent-prompts.md`: lead, four specialist assignments and final acceptance prompt.

## ECC inspection findings

Found local checkout: `D:/Leave/EL/AIML/third_party/ECC`

Git revision inspected: `76aaa77`. This identifies the local checkout, not a claim that it is the newest upstream version. I inspected its README, skill catalog and relevant instruction excerpts. I did not install it, activate hooks, execute its setup scripts or audit the whole repository.

ECC is useful as selective engineering guidance. It is not a robotics simulator, an Instagram SDK or a guarantee of production correctness. Read complete chosen skill files before applying them. Adapt example commands to the actual shell and repository. Do not paste example model names, hardcoded thresholds or service choices into production without verification.

### Recommended skills and exact local paths

| Work | Skill file | Application |
|---|---|---|
| Milestone verification | `D:/Leave/EL/AIML/third_party/ECC/skills/verification-loop/SKILL.md` | Build, types, lint, tests, security checks and diff review; record actual results. |
| Browser journeys | `D:/Leave/EL/AIML/third_party/ECC/skills/e2e-testing/SKILL.md` | Playwright journeys, traces and failure artifacts. Prefer observable conditions over arbitrary sleeps. |
| Authentication/uploads | `D:/Leave/EL/AIML/third_party/ECC/skills/security-review/SKILL.md` | Secrets, authorization, tenant isolation and external inputs. |
| Agent tool boundaries | `D:/Leave/EL/AIML/third_party/ECC/skills/agent-security-hardening/SKILL.md` | Validate model-requested actions at execution time; enforce scoped authority. |
| AI behavior evaluation | `D:/Leave/EL/AIML/third_party/ECC/skills/eval-harness/SKILL.md` | Define capability and regression cases before implementation; use objective graders where possible. |
| API contracts | `D:/Leave/EL/AIML/third_party/ECC/skills/api-design/SKILL.md` | Resource contracts, errors and status semantics. |
| Inference budgets | `D:/Leave/EL/AIML/third_party/ECC/skills/cost-aware-llm-pipeline/SKILL.md` | Metering, bounded retries and model routing; replace illustrative Claude IDs with verified NVIDIA models on Nebius. |
| Morph Python checks | `D:/Leave/EL/AIML/third_party/ECC/skills/python-testing/SKILL.md` | Pytest fixtures and meaningful regression cases. Coverage does not prove simulator or hardware behavior. |
| Product UI | `D:/Leave/EL/AIML/third_party/ECC/skills/frontend-design-direction/SKILL.md` | Real workflow, explicit loading/error/partial/permission states and visual review. |
| Optional skill installation | `D:/Leave/EL/AIML/third_party/ECC/skills/skill-host-compat/SKILL.md` | Inspect host-specific skill compatibility before copying into another agent's skill directory. |

Also found the local frontend design skill at:
`C:/Users/asus/.claude/plugins/marketplaces/claude-plugins-official/plugins/frontend-design/skills/frontend-design/SKILL.md`

Use it for distinctive interface design, with ECC's design-direction skill for state coverage. Do not load every skill at once. Use approximately two to four relevant skills for the current task.

### Optional reviewer roles

The ECC `agents/` directory contains `architect.md`, `code-reviewer.md`, `security-reviewer.md`, `e2e-runner.md`, `mle-reviewer.md`, `python-reviewer.md`, `pytorch-build-resolver.md` and `silent-failure-hunter.md`. The architect and MLE reviewer instructions were sampled; other role files should be read before use. They are role definitions, not automatically available tools in every host. Keep the host's configured model unless the user chooses otherwise; do not inherit a model override simply from an ECC example.

### Do not enable by default

- `social-publisher`: the inspected skill operates through SocialClaw and needs a separate service account. It does not replace direct Meta OAuth, publishing and insights in Axys.
- Global installers, hooks, background memory collectors or continuous loops: none is needed just to use these prompts. Inspect and intentionally configure any later installation.
- Framework-wide architecture copied from unrelated skills: use patterns that fit the project, not every available service.
- Robotics claims based on generic ML skills: use the pinned official Isaac Lab/task documentation for simulator and action-space details.

## Shared contract: prepend to every specialist prompt

```text
Work on the lead agent's selected project and assigned file ownership only. Read the project's current AGENTS.md, docs/BUILD_CONTRACT.md, docs/INTERFACES.md and docs/STATUS.md before editing. Read the complete relevant ECC skill files named in your assignment; the local ECC root is D:/Leave/EL/AIML/third_party/ECC. If this path is unavailable on your machine, report that and use the task requirements without inventing skill contents.

Follow the host's higher-priority instructions and the user's current requirements. ECC supplies engineering guidance, not permission to change scope or install unrelated tools. Never replace NVIDIA/Nebius runtime inference with another provider because a skill uses it in example code.

Coordinate shared-contract changes with the lead. Do not independently change shared schemas, database migrations, root package dependencies or lockfiles. Preserve other agents' work. Use scoped commits and a handoff containing changed files, commands/results, remaining defects and assumptions. If you cannot communicate with another agent, write the handoff in the repository instead of pretending coordination happened.

Distinguish development fixtures, recorded results, real cloud executions and physical trials. No fake metrics, invented participants, decorative job progress or screenshots presented as proof of functionality. Missing credentials block the affected live gate; they do not justify deleting the integration or labeling it complete. Continue independent implementation and report the precise required action without printing secrets.

Validate security-sensitive and irreversible actions at their actual execution boundary. Do not publish social content, spend beyond the configured budget, upload participant data, or move physical hardware without applicable scoped authorization. Implement the complete reviewable path and tests while awaiting any required external action.

Deliver working code in your assigned scope, meaningful automated checks, manual/browser evidence when relevant and concise setup notes. Do not stop at a plan or scaffold if implementation is possible. Do not conceal failures or weaken acceptance criteria to make tests green.
```

## Important legacy conflict

`E:/Projects/axcas/AGENTS.md` currently describes ProofGate/Axcas under the previous architecture and explicitly prohibits automatic social posting. The current user request is a fresh rebuild with real Instagram publishing and NVIDIA models through Nebius. The lead prompt therefore uses a **new repository** and treats the old repository as read-only historical context. It must not modify or delete that old project or silently inherit its obsolete product scope. Inspect applicable instructions in the new location normally.
