"""Pre-registration and development-only selection; no held-out feedback loop."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field, model_validator

from morph.contracts import Budget, Candidate, Case, Digest, Frozen, RunManifest, RunResult
from morph.evaluation import planner_observation, validate_result


class Protocol(Frozen):
    evaluator_sha256: Digest
    development: Annotated[tuple[Case, ...], Field(min_length=1)]
    held_out: Annotated[tuple[Case, ...], Field(min_length=1)]
    candidates: Annotated[tuple[Candidate, ...], Field(min_length=1)]
    search_budget: Budget
    candidates_per_method: Annotated[int, Field(gt=0)]

    @model_validator(mode="after")
    def separated(self):
        # Upstream starts repeat deterministically. Seed changes alone do not make new trials.
        dev = {(c.condition_id, c.start_id) for c in self.development}
        held = {(c.condition_id, c.start_id) for c in self.held_out}
        if len(dev) != len(self.development) or len(held) != len(self.held_out) or dev & held:
            raise ValueError("duplicate canonical starts or split leakage")
        if len({c.candidate_id for c in self.candidates}) != len(self.candidates):
            raise ValueError("duplicate candidate ID")
        if self.candidates_per_method > len(self.candidates):
            raise ValueError("candidate budget exceeds registry")
        if self.candidates_per_method * len(self.development) > self.search_budget.rollouts:
            raise ValueError("matched rollout budget too small")
        return self


def select_development(
    protocol: Protocol,
    baseline: tuple[RunManifest, RunResult],
    trials: tuple[tuple[RunManifest, RunResult], ...],
) -> Candidate | None:
    """Selection happens once before held-out evaluation. No acceptable candidate means refusal."""
    base, base_result = baseline
    base_obs = planner_observation(base, base_result)
    if base.method != "baseline" or base.task.evaluator_sha256 != protocol.evaluator_sha256:
        raise ValueError("baseline/evaluator mismatch")
    expected = {c.key() for c in protocol.development}
    if {c.key() for c in base.cases} != expected:
        raise ValueError("baseline does not match frozen development cases")
    if len(trials) > protocol.candidates_per_method:
        raise ValueError("candidate budget exceeded")
    if len({m.candidate.candidate_id for m, _ in trials}) != len(trials):
        raise ValueError("repeated candidate")
    if len({m.method for m, _ in trials}) > 1:
        raise ValueError("select each method independently")
    budget = protocol.search_budget
    if (
        sum(len(m.cases) for m, _ in trials) > budget.rollouts
        or sum(r.wall_seconds for _, r in trials) > budget.wall_seconds
        or sum(r.gpu_hours for _, r in trials) > budget.gpu_hours
        or sum(r.compute_cost_usd + r.inference_cost_usd for _, r in trials) > budget.cost_usd
    ):
        raise ValueError("matched development budget exceeded, including inference overhead")
    eligible = []
    for manifest, result in trials:
        if (
            manifest.task != base.task
            or {c.key() for c in manifest.cases} != expected
            or manifest.candidate not in protocol.candidates
        ):
            raise ValueError("trial outside frozen protocol")
        validate_result(manifest, result, require_complete=True)
        observation = planner_observation(manifest, result)
        if any(e.provenance != "simulation" for e in (*result.episodes, *base_result.episodes)):
            continue
        if (
            observation.successes > base_obs.successes
            and observation.aborts <= base_obs.aborts
            and observation.unsafe <= base_obs.unsafe
        ):
            if observation.mean_completion_seconds is None:
                raise ValueError("successful candidate is missing completion timing")
            eligible.append(
                (
                    observation.successes,
                    -observation.mean_completion_seconds,
                    manifest.candidate.candidate_id,
                    manifest.candidate,
                )
            )
    return max(eligible, key=lambda item: item[:3])[3] if eligible else None
