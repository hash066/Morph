"""Bounded local smoke test only. Never provisions cloud resources or moves hardware."""
import argparse
import hashlib
import json
import os
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TUTORIAL = ROOT / "vendor" / "IsaacLabTutorial"
PIN = "9a4286b4bc8a5720ac97f87e5e0140f7542c22d9"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout-seconds", type=int, default=180)
    args = parser.parse_args()
    if not 1 <= args.timeout_seconds <= 900:
        raise SystemExit("Timeout must be between 1 and 900 seconds")
    commit = subprocess.check_output(["git", "-C", str(TUTORIAL), "rev-parse", "HEAD"],
                                     cwd=ROOT, text=True).strip()
    if commit != PIN:
        raise SystemExit("Tutorial commit differs from pin")
    actual_lock = (TUTORIAL / "uv.lock").read_bytes()
    if actual_lock != (ROOT / "environments" / "tutorial.uv.lock").read_bytes():
        raise SystemExit("Tutorial dependency lock differs from pin")
    command = ["uv", "run", "--project", str(TUTORIAL), "--locked", "--no-sync", "isaaclab",
               "zero_agent", "--task", "IsaacTutorial-Place-Vial-SO101", "--num_envs", "1",
               "--max_steps", "100", "--visualizer", "none",
               "presets=newton_mjwarp", "env.seed=42"]
    output = ROOT / "docs" / "verification" / "simulator-smoke.log"
    environment = os.environ.copy()
    environment["PYTHONUNBUFFERED"] = "1"
    for name, relative in {
        "TEMP": "runtime-temp", "TMP": "runtime-temp", "UV_CACHE_DIR": "uv-cache",
        "WARP_CACHE_PATH": "warp-cache", "CUDA_CACHE_PATH": "cuda-cache",
        "TORCH_HOME": "torch-cache", "HF_HOME": "hf-cache",
    }.items():
        directory = ROOT / "data" / relative
        directory.mkdir(parents=True, exist_ok=True)
        environment[name] = str(directory)
    for name in ("NEBIUS_API_KEY", "NEBIUS_TOKEN_FACTORY_KEY", "MORPH_API_TOKEN"):
        environment.pop(name, None)
    started = time.monotonic()
    with output.open("w", encoding="utf-8") as log:
        process = subprocess.Popen(command, cwd=ROOT, env=environment, stdout=log, stderr=subprocess.STDOUT)
        try:
            code = process.wait(timeout=args.timeout_seconds)
        except subprocess.TimeoutExpired:
            # Kill the process tree on Windows, process group support required before Linux worker rollout.
            subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], cwd=ROOT,
                           capture_output=True, check=False)
            process.wait(timeout=15)
            code = 124
    evidence = {"command": command, "returncode": code, "seconds": time.monotonic()-started,
                "timeout_seconds": args.timeout_seconds,
                "tutorial_commit": PIN, "lock_sha256": hashlib.sha256(actual_lock).hexdigest(),
                "kind": "local_zero_action_smoke", "baseline_policy_evaluated": False}
    (output.parent / "simulator-smoke.json").write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    print(json.dumps(evidence, indent=2))
    raise SystemExit(code)


if __name__ == "__main__":
    main()
