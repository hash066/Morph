"""Restartable local simulator worker for bounded Morph development jobs."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from morph.contracts import Perturbation, RunManifest
from morph.isaac_runner import AuditRequest, AuditResult, audit_to_run_result, run_audit
from morph.store import Conflict, Store


class ExecutionRejected(ValueError):
    pass


def validate_execution_manifest(manifest: RunManifest, root: Path) -> None:
    frozen = json.loads((root / "docs/verification/frozen-protocol.json").read_text(encoding="utf-8"))
    lock_hash = hashlib.sha256((root / "environments/tutorial.uv.lock").read_bytes()).hexdigest()
    task = manifest.task
    if (
        task.checkpoint_sha256 != frozen["checkpoint_sha256"]
        or task.evaluator_sha256 != frozen["evaluator_sha256"]
        or task.lock_sha256 != lock_hash
    ):
        raise ExecutionRejected("task provenance does not match the frozen executable stack")
    if manifest.split != "development" or manifest.method not in {"morph", "random", "no_history"}:
        raise ExecutionRejected("worker accepts bounded development experiments only")
    rows = sorted(case.start_id for case in manifest.cases)
    if rows != list(range(rows[0], rows[0] + len(rows))) or rows[-1] >= 64:
        raise ExecutionRejected("development starts must be contiguous and remain below held-out rows")
    if len({case.seed for case in manifest.cases}) != 1 or {
        case.condition_id for case in manifest.cases
    } != {"actuator150"}:
        raise ExecutionRejected("unsupported seed or private condition reference")


@dataclass
class LocalSimulatorWorker:
    store: Store
    root: Path
    executor: Callable[[AuditRequest, Path, Path], AuditResult] = run_audit

    def run_one(self) -> str | None:
        row = self.store.claim()
        if row is None:
            return None
        key, lease = row["id"], row["lease"]
        try:
            manifest = RunManifest.model_validate_json(row["manifest"])
            validate_execution_manifest(manifest, self.root)
            starts = sorted(case.start_id for case in manifest.cases)
            request = AuditRequest(
                checkpoint=self.root
                / "vendor/IsaacLabTutorial/logs/rsl_rl/so101_vial_state/"
                "2026-10-19_10-15-22_morph_baseline_seed42/model_799.pt",
                output=self.root / "data/jobs" / f"{key}.json",
                perturbation=Perturbation(
                    condition_id="actuator150",
                    vial_mass_kg=0.020,
                    vial_friction_coeff=0.7,
                    actuator_gain_multiplier=1.5,
                    recoverable=True,
                ),
                candidate=manifest.candidate,
                episodes=len(starts),
                seed=manifest.cases[0].seed,
                reset_offset=starts[0],
                timeout_seconds=manifest.budget.wall_seconds,
            )
            audit = self.executor(request, self.root, self.root / "vendor/IsaacLabTutorial")
            if self.store.get(key)["state"] == "cancelled":
                return key
            result = audit_to_run_result(manifest, audit, self.store)
            self.store.finish(key, lease, result)
        except (Conflict, ExecutionRejected, RuntimeError, ValueError, KeyError):
            if self.store.get(key)["state"] == "running":
                self.store.fail(key, lease, "runtime_failed")
        return key
