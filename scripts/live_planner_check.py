"""One bounded, evidence-producing Token Factory planner integration check."""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path

from morph.contracts import Budget, Candidate
from morph.planner import CreditAuthorization, Nemotron
from morph.store import Store

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    authorization = CreditAuthorization.model_validate_json(
        (ROOT / "data" / "credit-authorization.json").read_text(encoding="utf-8")
    )
    store = Store(
        ROOT / "data" / "live-planner.sqlite",
        Budget(rollouts=20, wall_seconds=900, gpu_hours=0, cost_usd=authorization.inference_cap_usd),
    )
    registry = (
        Candidate(candidate_id="arm_90", arm_scale_multiplier=0.9),
        Candidate(candidate_id="arm_75", arm_scale_multiplier=0.75),
        Candidate(candidate_id="arm_jaw_75", arm_scale_multiplier=0.75, jaw_scale_multiplier=0.75),
    )
    client = Nemotron(os.environ.get("NEBIUS_API_KEY", ""), authorization, store)
    try:
        # No synthetic observation is supplied. This checks the real constrained planner boundary
        # without representing an unrun simulation as evidence.
        proposal = client.propose((), registry)
    finally:
        client.close()
    record = {
        "checked_at": datetime.now(UTC).isoformat(),
        "kind": "live_nebius_nemotron_planner_check",
        "model": authorization.model_id,
        "proposal": proposal.model_dump(mode="json"),
        "simulation_observations_supplied": 0,
        "recovery_claimed": False,
    }
    output = ROOT / "docs" / "verification" / "nebius-live-planner.json"
    output.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "validated", "model": authorization.model_id, "output": str(output)}))


if __name__ == "__main__":
    main()
