import pytest

from morph.contracts import Candidate, EpisodeResult, RunResult
from morph.evaluation import compare, planner_observation, simple_search, validate_result


def result(manifest, success=False, provenance="test_fixture"):
    return RunResult(
        manifest_sha256=manifest.digest(),
        episodes=tuple(
            EpisodeResult(
                case=c,
                success=success,
                aborted=False,
                unsafe=False,
                completion_seconds=1,
                provenance=provenance,
                raw_artifact_sha256="d" * 64,
            )
            for c in manifest.cases
        ),
        wall_seconds=1,
        gpu_hours=0,
        inference_cost_usd=0,
        compute_cost_usd=0,
    )


def test_hidden_condition_not_in_planner_projection(manifest):
    observation = planner_observation(manifest, result(manifest))
    assert "opaque" not in observation.canonical()
    assert "seed" not in observation.canonical()
    held = manifest.model_copy(update={"split": "held_out"})
    with pytest.raises(ValueError, match="held-out"):
        planner_observation(held, result(held))


def test_missing_duplicate_unscheduled(manifest):
    r = result(manifest)
    with pytest.raises(ValueError, match="duplicate"):
        validate_result(manifest, r.model_copy(update={"episodes": r.episodes * 2}))
    with pytest.raises(ValueError, match="incomplete"):
        validate_result(manifest, r.model_copy(update={"episodes": ()}), require_complete=True)


def test_fixture_cannot_validate_recovery(manifest):
    base = manifest.model_copy(update={"split": "held_out"})
    trial = base.model_copy(update={"method": "morph", "candidate": Candidate(candidate_id="test")})
    report = compare(base, result(base), trial, result(trial, True))
    assert report.decision == "no_validated_recovery"
    assert "fixtures" in report.reason


def test_incomplete_denominator_and_pairing(manifest):
    base = manifest.model_copy(update={"split": "held_out"})
    trial = base.model_copy(update={"method": "morph"})
    report = compare(base, result(base), trial, result(trial).model_copy(update={"episodes": ()}))
    assert report.denominator == 1
    assert report.decision == "incomplete"
    wrong = trial.model_copy(update={"task": trial.task.model_copy(update={"checkpoint_sha256": "e" * 64})})
    with pytest.raises(ValueError, match="pair"):
        compare(base, result(base), wrong, result(wrong))


def test_matched_random_search_reproducible():
    registry = tuple(Candidate(candidate_id=f"c{i}", arm_scale_multiplier=0.5 + i / 20) for i in range(10))
    assert simple_search(registry, 3, 42) == simple_search(registry, 3, 42)
    assert len(set(simple_search(registry, 3, 42))) == 3
    with pytest.raises(ValueError):
        simple_search(registry, 11, 42)
