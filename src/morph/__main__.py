import argparse
import json
import os
from pathlib import Path

from morph.contracts import Budget
from morph.planner import CreditAuthorization, Nemotron, ProviderBlocked
from morph.store import Store


def main():
    parser = argparse.ArgumentParser(description="Morph feasibility and evidence tools")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("status")
    provider = commands.add_parser("provider-check", help="Read-only account model availability check")
    provider.add_argument("--authorization", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "status":
        print(
            json.dumps(
                {
                    "simulation": "blocked",
                    "hardware": "disabled",
                    "nebius_key_present": bool(os.environ.get("NEBIUS_API_KEY", "").strip()),
                    "credit_verified": False,
                    "performance_results": 0,
                },
                indent=2,
            )
        )
        return
    authorization = CreditAuthorization.model_validate_json(args.authorization.read_text(encoding="utf-8"))
    store = Store(
        Path("data/inference.sqlite"),
        Budget(rollouts=100, wall_seconds=3600, gpu_hours=0, cost_usd=authorization.inference_cap_usd),
    )
    client = Nemotron(os.environ.get("NEBIUS_API_KEY", ""), authorization, store)
    try:
        client._check_credit()
        models = client._request("GET", "/models")
        available = authorization.model_id in {r.get("id") for r in models.get("data", [])}
        print(
            json.dumps(
                {"model": authorization.model_id, "available": available, "inference_completed": False}
            )
        )
        if not available:
            raise SystemExit(2)
    finally:
        client.close()


if __name__ == "__main__":
    try:
        main()
    except ProviderBlocked as exc:
        print(json.dumps({"blocked": str(exc)}))
        raise SystemExit(2) from None
