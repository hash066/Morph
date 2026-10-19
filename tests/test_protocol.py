import pytest
from test_evaluation import result

from morph.contracts import Budget, Candidate, Case
from morph.protocol import Protocol, select_development


def protocol(manifest):
    return Protocol(
        evaluator_sha256=manifest.task.evaluator_sha256,
        development=manifest.cases,
        held_out=(Case(condition_id="opaque", seed=20, start_id=1),),
        candidates=(Candidate(candidate_id="c1", arm_scale_multiplier=0.8),),
        search_budget=Budget(rollouts=1, wall_seconds=10, gpu_hours=1, cost_usd=1),
        candidates_per_method=1,
    )


def test_seed_change_does_not_hide_start_leakage(manifest):
    p = protocol(manifest).model_dump(mode="json")
    p["held_out"] = [{"condition_id": "opaque", "seed": 999, "start_id": 0}]
    with pytest.raises(ValueError, match="leakage"):
        Protocol.model_validate(p)


def test_selection_fixture_refusal_and_real_contract(manifest):
    p = protocol(manifest)
    trial = manifest.model_copy(update={"method": "morph", "candidate": p.candidates[0]})
    assert select_development(p, (manifest, result(manifest)), ((trial, result(trial, True)),)) is None
    # Synthetic unit values tagged simulation exercise selection only; never persisted as evidence.
    assert (
        select_development(
            p,
            (manifest, result(manifest, provenance="simulation")),
            ((trial, result(trial, True, "simulation")),),
        )
        == p.candidates[0]
    )


def test_selection_enforces_total_cost_and_split(manifest):
    p = protocol(manifest)
    trial = manifest.model_copy(update={"method": "morph", "candidate": p.candidates[0]})
    expensive = result(trial).model_copy(update={"inference_cost_usd": 2})
    with pytest.raises(ValueError, match="budget"):
        select_development(p, (manifest, result(manifest)), ((trial, expensive),))
    held = trial.model_copy(update={"split": "held_out"})
    with pytest.raises(ValueError, match="held-out"):
        select_development(p, (manifest, result(manifest)), ((held, result(held)),))


def test_success_gain_with_more_unsafe_episodes_is_not_selected(manifest):
    p = protocol(manifest)
    trial = manifest.model_copy(update={"method": "morph", "candidate": p.candidates[0]})
    trial_result = result(trial, True, "simulation")
    trial_result = trial_result.model_copy(
        update={"episodes": tuple(e.model_copy(update={"unsafe": True}) for e in trial_result.episodes)}
    )
    assert (
        select_development(p, (manifest, result(manifest, provenance="simulation")), ((trial, trial_result),))
        is None
    )
