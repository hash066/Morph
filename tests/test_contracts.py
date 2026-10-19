import pytest
from pydantic import ValidationError

from morph.contracts import Candidate, Case, EpisodeResult, Proposal


@pytest.mark.parametrize("value", [float("nan"), float("inf"), 0.49, 1.01])
def test_controller_bounds(value):
    with pytest.raises(ValidationError):
        Candidate(candidate_id="c", arm_scale_multiplier=value)


def test_no_executable_fields_or_mutation():
    with pytest.raises(ValidationError):
        Candidate.model_validate({"candidate_id": "c", "shell": "anything"})
    candidate = Candidate(candidate_id="c")
    with pytest.raises(ValidationError):
        candidate.arm_scale_multiplier = 0.7


def test_task_success_preserved_independently_of_safety():
    episode = EpisodeResult(
        case=Case(condition_id="a", seed=0, start_id=0),
        success=True,
        aborted=False,
        unsafe=True,
        completion_seconds=1,
        provenance="test_fixture",
        raw_artifact_sha256="a" * 64,
    )
    assert episode.success and episode.unsafe


def test_failed_episode_may_have_no_completion_time():
    episode = EpisodeResult(
        case=Case(condition_id="a", seed=0, start_id=0),
        success=False,
        aborted=False,
        unsafe=False,
        completion_seconds=None,
        provenance="test_fixture",
        raw_artifact_sha256="a" * 64,
    )
    assert episode.completion_seconds is None


def test_success_requires_completion_time():
    with pytest.raises(ValidationError, match="completion"):
        EpisodeResult(
            case=Case(condition_id="a", seed=0, start_id=0),
            success=True,
            aborted=False,
            unsafe=False,
            completion_seconds=None,
            provenance="test_fixture",
            raw_artifact_sha256="a" * 64,
        )


def test_refusal_cannot_also_select_candidate():
    with pytest.raises(ValidationError):
        Proposal(hypotheses=(), candidate_id="c", reason="none", decision="no_validated_recovery")
