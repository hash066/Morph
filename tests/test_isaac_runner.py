from pathlib import Path

import pytest

from morph.contracts import Budget, Candidate, Case, Perturbation, RunManifest, TaskConfig
from morph.isaac_runner import AuditRequest, AuditResult, audit_to_run_result, build_command


def request(tmp_path: Path, **changes):
    checkpoint = tmp_path / "model.pt"
    checkpoint.write_bytes(b"checkpoint")
    values = {
        "checkpoint": checkpoint,
        "output": tmp_path / "audit.json",
        "perturbation": Perturbation(
            condition_id="heavy", vial_mass_kg=0.03, recoverable=True, actuator_gain_multiplier=1.2
        ),
        "candidate": Candidate(candidate_id="c75", arm_scale_multiplier=0.75, jaw_scale_multiplier=0.5),
        "episodes": 20,
        "seed": 42,
        "reset_offset": 5,
    }
    values.update(changes)
    return AuditRequest(**values)


def test_command_is_fixed_and_bounded(tmp_path):
    command = build_command(request(tmp_path), tmp_path)
    assert command[:6] == ("uv", "run", "--locked", "--no-sync", "isaaclab", "play")
    assert "env.events.vial_mass.params.mass_distribution_params=[0.03,0.03]" in command
    assert "env.events.vial_material.params.static_friction_range=[0.7,0.7]" in command
    assert "env.events.vial_material.params.dynamic_friction_range=[0.7,0.7]" in command
    assert "env.actions.arm_action.scale=0.0297" in command
    assert "env.actions.gripper_action.scale=0.012" in command
    assert all("NEBIUS" not in part for part in command)


def test_rejects_noncanonical_range(tmp_path):
    with pytest.raises(ValueError, match="canonical"):
        build_command(request(tmp_path, episodes=20, reset_offset=120), tmp_path)


def test_audit_rows_become_content_addressed_results(store):
    task = TaskConfig(checkpoint_sha256="a" * 64, evaluator_sha256="b" * 64, lock_sha256="c" * 64)
    manifest = RunManifest(
        task=task,
        candidate=Candidate(candidate_id="baseline"),
        method="baseline",
        split="development",
        cases=(Case(condition_id="heavy", seed=42, start_id=5),),
        budget=Budget(rollouts=1, wall_seconds=100, gpu_hours=1, cost_usd=0),
    )
    audit = AuditResult(
        payload={
            "runtime": {"success_criterion": "any_rack_hole_v1"},
            "episodes": [
                {
                    "reset_row": 5,
                    "success": False,
                    "aborted": True,
                    "unsafe_rack_contact": False,
                    "completion_seconds": None,
                }
            ],
        },
        wall_seconds=12,
        command=("uv",),
    )
    result = audit_to_run_result(manifest, audit, store)
    assert result.episodes[0].aborted is True
    assert result.episodes[0].completion_seconds is None
    assert store.artifact(result.episodes[0].raw_artifact_sha256)
