"""Constrained subprocess adapter for real SO-101 simulator audits."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

from morph.contracts import Candidate, EpisodeResult, Perturbation, RunManifest, RunResult
from morph.store import Store

NOMINAL_ARM_SCALE = 0.033
NOMINAL_JAW_SCALE = 0.02
EVALUATOR = "morph.isaac_callback.install_morph_episode_counter"


@dataclass(frozen=True)
class AuditRequest:
    checkpoint: Path
    output: Path
    perturbation: Perturbation
    candidate: Candidate
    episodes: int
    seed: int
    reset_offset: int
    timeout_seconds: int = 3600

    def validate(self) -> None:
        if not self.checkpoint.is_file():
            raise ValueError("checkpoint does not exist")
        if not 1 <= self.episodes <= 128:
            raise ValueError("an audit batch must contain 1..128 canonical starts")
        if not 0 <= self.reset_offset < 128 or self.reset_offset + self.episodes > 128:
            raise ValueError("audit range exceeds the 128 canonical starts")
        if not 1 <= self.timeout_seconds <= 86400:
            raise ValueError("timeout must be in 1..86400 seconds")


@dataclass(frozen=True)
class AuditResult:
    payload: dict
    wall_seconds: float
    command: tuple[str, ...]


def checkpoint_sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def build_command(request: AuditRequest, tutorial: Path) -> tuple[str, ...]:
    request.validate()
    arm_scale = NOMINAL_ARM_SCALE * request.candidate.arm_scale_multiplier
    jaw_scale = NOMINAL_JAW_SCALE * request.candidate.jaw_scale_multiplier
    mass = request.perturbation.vial_mass_kg
    return (
        "uv", "run", "--locked", "--no-sync", "isaaclab", "play",
        "--rl_library", "rsl_rl",
        "--task", "IsaacTutorial-Place-Vial-SO101",
        "--num_envs", str(request.episodes),
        "--checkpoint", str(request.checkpoint.resolve()),
        "--visualizer", "none",
        "--external_callback", EVALUATOR,
        "presets=newton_mjwarp",
        f"env.seed={request.seed}",
        f"env.events.vial_mass.params.mass_distribution_params=[{mass},{mass}]",
        f"env.actions.arm_action.scale={arm_scale}",
        f"env.actions.gripper_action.scale={jaw_scale}",
    )


def _audit_environment(root: Path, request: AuditRequest) -> dict[str, str]:
    environment = os.environ.copy()
    scoped = {
        "TEMP": "sim-temp", "TMP": "sim-temp", "UV_CACHE_DIR": "uv-cache",
        "WARP_CACHE_PATH": "warp-cache", "CUDA_CACHE_PATH": "cuda-cache",
    }
    for name, relative in scoped.items():
        directory = root / "data" / relative
        directory.mkdir(parents=True, exist_ok=True)
        environment[name] = str(directory)
    environment.update(
        PXR_WORK_THREAD_LIMIT="1",
        PYTHONUNBUFFERED="1",
        PYTHONIOENCODING="utf-8",
        PYTHONPATH=str(root / "src"),
        SO101_EVALUATION_EPISODES=str(request.episodes),
        SO101_EVALUATION_OUTPUT=str(request.output.resolve()),
        MORPH_RESET_OFFSET=str(request.reset_offset),
    )
    for name in ("NEBIUS_API_KEY", "NEBIUS_TOKEN_FACTORY_KEY", "MORPH_API_TOKEN"):
        environment.pop(name, None)
    return environment


def _validate_readback(request: AuditRequest, payload: dict) -> None:
    if payload.get("checkpoint_sha256") != checkpoint_sha256(request.checkpoint):
        raise RuntimeError("simulator checkpoint readback mismatch")
    episodes = payload.get("episodes")
    if not isinstance(episodes, list) or len(episodes) != request.episodes:
        raise RuntimeError("simulator returned an incomplete audit")
    rows = [row.get("reset_row") for row in episodes]
    if len(set(rows)) != len(rows) or any(row is None for row in rows):
        raise RuntimeError("simulator reset-row evidence is missing or duplicated")
    runtime = payload.get("runtime", {})
    event = runtime.get("event_parameters", {}).get("vial_mass", {})
    expected_mass = [request.perturbation.vial_mass_kg] * 2
    if event.get("mass_distribution_params") != expected_mass:
        raise RuntimeError("vial-mass readback mismatch")
    action = runtime.get("action_parameters", {})
    expected_arm = NOMINAL_ARM_SCALE * request.candidate.arm_scale_multiplier
    expected_jaw = NOMINAL_JAW_SCALE * request.candidate.jaw_scale_multiplier
    if action.get("arm_action", {}).get("scale") != expected_arm:
        raise RuntimeError("arm-scale readback mismatch")
    if action.get("gripper_action", {}).get("scale") != expected_jaw:
        raise RuntimeError("jaw-scale readback mismatch")


def run_audit(request: AuditRequest, root: Path, tutorial: Path) -> AuditResult:
    command = build_command(request, tutorial)
    request.output.parent.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    try:
        completed = subprocess.run(
            command,
            cwd=tutorial,
            env=_audit_environment(root, request),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=request.timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("simulator audit timed out") from exc
    diagnostic = request.output.with_suffix(".log")
    diagnostic.write_text(
        "STDOUT\n" + (completed.stdout or "") + "\nSTDERR\n" + (completed.stderr or ""),
        encoding="utf-8",
    )
    if completed.returncode != 0:
        raise RuntimeError(f"simulator audit failed with exit code {completed.returncode}; see {diagnostic}")
    if not request.output.is_file():
        raise RuntimeError("simulator did not write audit evidence")
    payload = json.loads(request.output.read_text(encoding="utf-8"))
    _validate_readback(request, payload)
    return AuditResult(payload, time.monotonic() - started, command)


def audit_to_run_result(manifest: RunManifest, audit: AuditResult, store: Store) -> RunResult:
    """Convert verified callback rows into immutable, content-addressed episode evidence."""
    rows = audit.payload.get("episodes")
    if not isinstance(rows, list):
        raise TypeError("audit episodes missing")
    cases = {case.start_id: case for case in manifest.cases}
    if len(cases) != len(manifest.cases):
        raise ValueError("manifest repeats canonical starts")
    if {row.get("reset_row") for row in rows} != set(cases):
        raise ValueError("audit rows do not match the scheduled canonical starts")
    episodes = []
    runtime = audit.payload.get("runtime")
    for row in rows:
        start_id = row["reset_row"]
        artifact = json.dumps(
            {"format": "morph-so101-episode-v1", "runtime": runtime, "outcome": row},
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
        episodes.append(
            EpisodeResult(
                case=cases[start_id],
                success=row["success"],
                aborted=row["aborted"],
                unsafe=row["unsafe_rack_contact"],
                completion_seconds=row["completion_seconds"],
                provenance="simulation",
                raw_artifact_sha256=store.put_artifact(artifact),
            )
        )
    return RunResult(
        manifest_sha256=manifest.digest(),
        episodes=tuple(episodes),
        wall_seconds=audit.wall_seconds,
        gpu_hours=audit.wall_seconds / 3600,
        inference_cost_usd=0,
        compute_cost_usd=0,
    )
