import pytest

from morph.contracts import Budget, Candidate, Case, RunManifest, TaskConfig
from morph.store import Store


@pytest.fixture
def manifest():
    return RunManifest(
        task=TaskConfig(checkpoint_sha256="a" * 64, evaluator_sha256="b" * 64, lock_sha256="c" * 64),
        candidate=Candidate(candidate_id="baseline"),
        method="baseline",
        split="development",
        cases=(Case(condition_id="opaque", seed=10, start_id=0),),
        budget=Budget(rollouts=1, wall_seconds=10, gpu_hours=0, cost_usd=0),
    )


@pytest.fixture
def store(tmp_path):
    return Store(tmp_path / "test.sqlite", Budget(rollouts=100, wall_seconds=1000, gpu_hours=1, cost_usd=1))
