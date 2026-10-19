import hashlib
import json
from pathlib import Path

from morph.contracts import Budget, Candidate, Case, RunManifest, TaskConfig
from morph.isaac_runner import AuditResult
from morph.store import Store
from morph.worker import LocalSimulatorWorker

ROOT = Path(__file__).resolve().parents[1]


def trusted_manifest() -> RunManifest:
    frozen = json.loads((ROOT / "docs/verification/frozen-protocol.json").read_text())
    return RunManifest(
        task=TaskConfig(
            checkpoint_sha256=frozen["checkpoint_sha256"],
            evaluator_sha256=frozen["evaluator_sha256"],
            lock_sha256=hashlib.sha256((ROOT / "environments/tutorial.uv.lock").read_bytes()).hexdigest(),
        ),
        candidate=Candidate(
            candidate_id="worker_test", arm_scale_multiplier=0.75, jaw_scale_multiplier=0.75
        ),
        method="morph",
        split="development",
        cases=(Case(condition_id="actuator150", seed=42, start_id=8),),
        budget=Budget(rollouts=1, wall_seconds=120, gpu_hours=1, cost_usd=0),
    )


def test_worker_claims_executes_and_finishes_real_evidence_shape(tmp_path):
    store = Store(tmp_path / "worker.sqlite", Budget(rollouts=2, wall_seconds=240, gpu_hours=2, cost_usd=0))
    manifest = trusted_manifest()
    key = store.submit(manifest)

    def execute(request, root, tutorial):
        assert request.reset_offset == 8
        assert request.perturbation.actuator_gain_multiplier == 1.5
        return AuditResult(
            payload={
                "runtime": {"success_criterion": "any_rack_hole_v1"},
                "episodes": [
                    {
                        "reset_row": 8,
                        "success": True,
                        "aborted": False,
                        "unsafe_rack_contact": False,
                        "completion_seconds": 7.2,
                    }
                ],
            },
            wall_seconds=8,
            command=("isaaclab",),
        )

    assert LocalSimulatorWorker(store, ROOT, execute).run_one() == key
    row = store.get(key)
    assert row["state"] == "succeeded"
    assert json.loads(row["result"])["episodes"][0]["provenance"] == "simulation"


def test_cancelled_queued_job_is_never_claimed(tmp_path):
    store = Store(tmp_path / "worker.sqlite", Budget(rollouts=2, wall_seconds=240, gpu_hours=2, cost_usd=0))
    key = store.submit(trusted_manifest())
    store.cancel(key)
    assert LocalSimulatorWorker(store, ROOT, lambda *_: None).run_one() is None
    assert store.get(key)["state"] == "cancelled"
