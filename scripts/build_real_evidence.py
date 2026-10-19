"""Build the real held-out Morph evidence bundle from verified simulator audits."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

from morph.contracts import Budget, Candidate, Case, RecoveryPackage, RunManifest, TaskConfig
from morph.evaluation import compare
from morph.evidence import export_bundle
from morph.isaac_runner import AuditResult, audit_to_run_result
from morph.store import Store

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "docs/verification"


def wall_seconds(payload: dict) -> float:
    return (
        datetime.fromisoformat(payload["finished_at"]) - datetime.fromisoformat(payload["started_at"])
    ).total_seconds()


def main() -> None:
    frozen = json.loads((VERIFY / "frozen-protocol.json").read_text(encoding="utf-8"))
    lock_hash = hashlib.sha256((ROOT / "environments/tutorial.uv.lock").read_bytes()).hexdigest()
    task = TaskConfig(
        checkpoint_sha256=frozen["checkpoint_sha256"],
        evaluator_sha256=frozen["evaluator_sha256"],
        lock_sha256=lock_hash,
    )
    cases = tuple(
        Case(condition_id="actuator150", seed=42, start_id=row) for row in frozen["held_out_start_ids"]
    )
    budget = Budget(rollouts=8, wall_seconds=1200, gpu_hours=1, cost_usd=0)
    manifests = (
        RunManifest(
            task=task,
            candidate=Candidate(candidate_id="fault_baseline"),
            method="baseline",
            split="held_out",
            cases=cases,
            budget=budget,
        ),
        RunManifest(
            task=task,
            candidate=Candidate(
                candidate_id="balanced_75", arm_scale_multiplier=0.75, jaw_scale_multiplier=0.75
            ),
            method="morph",
            split="held_out",
            cases=cases,
            budget=budget,
        ),
        RunManifest(
            task=task,
            candidate=Candidate(
                candidate_id="arm67_jaw80", arm_scale_multiplier=2 / 3, jaw_scale_multiplier=0.8
            ),
            method="random",
            split="held_out",
            cases=cases,
            budget=budget,
        ),
    )
    files = (
        "heldout-fault-baseline.json",
        "heldout-morph-balanced75.json",
        "heldout-random-arm67-jaw80.json",
    )
    store = Store(
        ROOT / "data/real-evidence.sqlite", Budget(rollouts=100, wall_seconds=86400, gpu_hours=24, cost_usd=1)
    )
    results = []
    for manifest, filename in zip(manifests, files, strict=True):
        payload = json.loads((VERIFY / filename).read_text(encoding="utf-8"))
        audit = AuditResult(
            payload=payload, wall_seconds=wall_seconds(payload), command=tuple(payload["argv"])
        )
        results.append(audit_to_run_result(manifest, audit, store))
    report = compare(manifests[0], results[0], manifests[1], results[1])
    package = RecoveryPackage(manifests=manifests, results=tuple(results), report=report)
    bundle = export_bundle(package, store)
    output = ROOT / "dist/morph-evidence-v1.zip"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(bundle)
    random_report = compare(manifests[0], results[0], manifests[2], results[2])
    summary = {
        "format": "morph-held-out-summary-v1",
        "morph_report": report.model_dump(mode="json"),
        "random_report": random_report.model_dump(mode="json"),
        "bundle_sha256": hashlib.sha256(bundle).hexdigest(),
        "bundle_bytes": len(bundle),
    }
    (VERIFY / "heldout-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
