"""Run a bounded real simulator audit for one saved SO-101 checkpoint."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from morph.contracts import Candidate, Perturbation
from morph.isaac_runner import AuditRequest, run_audit

ROOT = Path(__file__).resolve().parents[1]
TUTORIAL = ROOT / "vendor" / "IsaacLabTutorial"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("checkpoint", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--episodes", type=int, default=8)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--mass", type=float, default=0.020)
    parser.add_argument("--friction", type=float, default=0.7)
    parser.add_argument("--actuator-gain", type=float, default=1.0)
    parser.add_argument("--arm", type=float, default=1.0)
    parser.add_argument("--jaw", type=float, default=1.0)
    parser.add_argument("--timeout", type=int, default=1200)
    args = parser.parse_args()
    audit = run_audit(
        AuditRequest(
            checkpoint=args.checkpoint,
            output=args.output,
            perturbation=Perturbation(
                condition_id="audit",
                vial_mass_kg=args.mass,
                recoverable=True,
                vial_friction_coeff=args.friction,
                actuator_gain_multiplier=args.actuator_gain,
            ),
            candidate=Candidate(
                candidate_id="audit", arm_scale_multiplier=args.arm, jaw_scale_multiplier=args.jaw
            ),
            episodes=args.episodes,
            seed=args.seed,
            reset_offset=args.offset,
            timeout_seconds=args.timeout,
        ),
        ROOT,
        TUTORIAL,
    )
    print(json.dumps({"status": "complete", "summary": audit.payload["summary"], "wall_seconds": audit.wall_seconds}))


if __name__ == "__main__":
    main()
