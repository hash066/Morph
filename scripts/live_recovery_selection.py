"""Select one bounded recovery experiment from real development evidence."""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path

from morph.contracts import Budget, Candidate, Observation
from morph.planner import CreditAuthorization, Nemotron
from morph.store import Store

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    evidence = json.loads(
        (ROOT / "docs/verification/perturbation-actuator150-audit.json").read_text(encoding="utf-8")
    )
    sensitivity = json.loads(
        (ROOT / "docs/verification/sensitivity-actuator150-comp067-audit.json").read_text(
            encoding="utf-8"
        )
    )

    def observation(candidate_id: str, payload: dict) -> Observation:
        rows = payload["episodes"]
        completion = [row["completion_seconds"] for row in rows if row["completion_seconds"] is not None]
        return Observation(
            candidate_id=candidate_id,
            successes=sum(row["success"] for row in rows),
            episodes=len(rows),
            aborts=sum(row["aborted"] for row in rows),
            unsafe=sum(row["unsafe_rack_contact"] for row in rows),
            mean_completion_seconds=sum(completion) / len(completion) if completion else None,
        )

    observations = (
        observation("fault_baseline", evidence),
        observation("balanced_67", sensitivity),
    )
    registry = (
        Candidate(candidate_id="balanced_67", arm_scale_multiplier=2 / 3, jaw_scale_multiplier=2 / 3),
        Candidate(candidate_id="balanced_75", arm_scale_multiplier=0.75, jaw_scale_multiplier=0.75),
        Candidate(candidate_id="arm67_jaw80", arm_scale_multiplier=2 / 3, jaw_scale_multiplier=0.8),
        Candidate(candidate_id="arm80_jaw67", arm_scale_multiplier=0.8, jaw_scale_multiplier=2 / 3),
    )
    authorization = CreditAuthorization.model_validate_json(
        (ROOT / "data/credit-authorization.json").read_text(encoding="utf-8")
    )
    store = Store(
        ROOT / "data/live-planner.sqlite",
        Budget(rollouts=20, wall_seconds=900, gpu_hours=0, cost_usd=authorization.inference_cap_usd),
    )
    client = Nemotron(os.environ.get("NEBIUS_API_KEY", ""), authorization, store)
    try:
        proposal = client.propose(observations, registry, attempted=frozenset({"balanced_67"}))
    finally:
        client.close()
    record = {
        "checked_at": datetime.now(UTC).isoformat(),
        "kind": "live_nebius_nemotron_recovery_selection",
        "model": authorization.model_id,
        "source_evidence": "docs/verification/perturbation-actuator150-audit.json",
        "observations": [item.model_dump(mode="json") for item in observations],
        "candidate_registry": [candidate.model_dump(mode="json") for candidate in registry],
        "proposal": proposal.model_dump(mode="json"),
        "recovery_claimed": False,
    }
    output = ROOT / "docs/verification/nebius-recovery-selection.json"
    output.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "validated", "proposal": proposal.model_dump(mode="json")}))


if __name__ == "__main__":
    main()
