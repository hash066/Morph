from __future__ import annotations

import math
import random
from typing import Literal

from morph.contracts import Candidate, EvaluationReport, Observation, RunManifest, RunResult


def validate_result(manifest: RunManifest, result: RunResult, require_complete: bool = False):
    if result.manifest_sha256 != manifest.digest():
        raise ValueError("manifest hash mismatch")
    expected = {c.key() for c in manifest.cases}
    keys = [e.case.key() for e in result.episodes]
    if len(set(keys)) != len(keys) or not set(keys) <= expected:
        raise ValueError("duplicate or unscheduled episode")
    if require_complete and set(keys) != expected:
        raise ValueError("incomplete scheduled cases")
    if len({e.provenance for e in result.episodes}) > 1:
        raise ValueError("mixed provenance")


def planner_observation(manifest: RunManifest, result: RunResult) -> Observation:
    if manifest.split != "development":
        raise ValueError("held-out results are never planner inputs")
    validate_result(manifest, result, require_complete=True)
    rows = result.episodes
    completion_times = [e.completion_seconds for e in rows if e.completion_seconds is not None]
    return Observation(
        candidate_id=manifest.candidate.candidate_id,
        successes=sum(e.success for e in rows),
        episodes=len(rows),
        aborts=sum(e.aborted for e in rows),
        unsafe=sum(e.unsafe for e in rows),
        mean_completion_seconds=(sum(completion_times) / len(completion_times) if completion_times else None),
    )


def simple_search(registry: tuple[Candidate, ...], count: int, seed: int) -> tuple[Candidate, ...]:
    if not 0 < count <= len(registry):
        raise ValueError("search count outside eligible candidate budget")
    if len({c.digest() for c in registry}) != len(registry):
        raise ValueError("duplicate registry entry")
    return tuple(random.Random(seed).sample(list(registry), count))


def compare(
    base: RunManifest, baseline: RunResult, trial: RunManifest, candidate: RunResult
) -> EvaluationReport:
    validate_result(base, baseline)
    validate_result(trial, candidate)
    if base.method != "baseline" or base.split != "held_out" or trial.split != "held_out":
        raise ValueError("final comparison requires baseline and held-out runs")
    if base.task != trial.task or {c.key() for c in base.cases} != {c.key() for c in trial.cases}:
        raise ValueError("comparison must pair task, checkpoint, evaluator and cases")
    if len({(c.condition_id, c.start_id) for c in base.cases}) != len(base.cases):
        raise ValueError("repeated canonical starts cannot be counted as independent trials")
    if len({c.condition_id for c in base.cases}) != 1:
        raise ValueError("report each condition separately; do not pool recoverable and impossible cases")
    n = len(base.cases)
    complete = len(baseline.episodes) == n == len(candidate.episodes)
    provenance = {e.provenance for e in (*baseline.episodes, *candidate.episodes)}
    gain = None
    interval = None
    decision: Literal["incomplete", "no_validated_recovery", "simulation_candidate"] = "incomplete"
    reason = "Missing scheduled episodes; denominator includes all scheduled cases."
    if complete:
        b = {e.case.key(): e for e in baseline.episodes}
        deltas = [int(e.success) - int(b[e.case.key()].success) for e in candidate.episodes]
        gain = sum(deltas) / n
        # Distribution-free paired Hoeffding interval, range [-1,1]; conservative for small n.
        radius = math.sqrt(2 * math.log(40) / n)
        interval = (max(-1.0, gain - radius), min(1.0, gain + radius))
        safe = sum(e.unsafe for e in candidate.episodes) <= sum(e.unsafe for e in baseline.episodes) and sum(
            e.aborted for e in candidate.episodes
        ) <= sum(e.aborted for e in baseline.episodes)
        decision = "no_validated_recovery"
        reason = "No statistically supported paired gain without increased safety failures."
        if provenance != {"simulation"}:
            reason = "Test fixtures cannot validate simulation recovery."
        elif interval[0] > 0 and safe:
            decision = "simulation_candidate"
            reason = "Paired simulation gain clears conservative interval; no physical approval."
    return EvaluationReport(
        baseline_manifest=base.digest(),
        candidate_manifest=trial.digest(),
        denominator=n,
        baseline_successes=sum(e.success for e in baseline.episodes),
        candidate_successes=sum(e.success for e in candidate.episodes),
        paired_gain=gain,
        paired_gain_interval95=interval,
        decision=decision,
        reason=reason,
        total_wall_seconds=baseline.wall_seconds + candidate.wall_seconds,
        total_gpu_hours=baseline.gpu_hours + candidate.gpu_hours,
        total_cost_usd=sum(r.inference_cost_usd + r.compute_cost_usd for r in (baseline, candidate)),
    )
