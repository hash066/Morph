"""Per-episode evidence callback for the pinned SO-101 tutorial task.

This overlay does not change rewards, terminations, observations, or policy
actions. It records the evaluator-owned terminal state and stops after one
episode for each requested canonical start.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path


def install_morph_episode_counter() -> list[str]:
    import torch  # type: ignore[import-not-found]
    from isaaclab_rl.rsl_rl import RslRlVecEnvWrapper  # type: ignore[import-not-found]
    from isaaclab_tutorial.tasks.place_vial.mdp.events import (  # type: ignore[import-not-found]
        ResetFromDataset,
    )
    from isaaclab_tutorial.utils import evaluation  # type: ignore[import-not-found]

    target = int(os.environ.get("SO101_EVALUATION_EPISODES", "128"))
    offset = int(os.environ.get("MORPH_RESET_OFFSET", "0"))
    if target <= 0 or offset < 0 or offset + target > 128:
        raise ValueError("Morph audit must select a bounded range within 128 canonical starts")

    original_reset_init = ResetFromDataset.__init__

    def init_with_offset(self, cfg, env):
        original_reset_init(self, cfg, env)
        if offset >= len(self.sequential_rows):
            raise ValueError("MORPH_RESET_OFFSET exceeds canonical reset rows")
        self.cursor = offset

    ResetFromDataset.__init__ = init_with_offset
    evaluation.EXACT_EVALUATION_ACTIVE = True

    original_step = RslRlVecEnvWrapper.step
    invocation = sys.argv[1:].copy()
    checkpoint_sha256 = None
    if "--checkpoint" in invocation:
        checkpoint = Path(invocation[invocation.index("--checkpoint") + 1])
        if checkpoint.is_file():
            with checkpoint.open("rb") as stream:
                checkpoint_sha256 = hashlib.file_digest(stream, "sha256").hexdigest()

    counted = None
    initial_rows = None
    runtime = None
    outcomes: list[dict] = []
    started = datetime.now(UTC)

    def counted_step(self, actions):
        nonlocal counted, initial_rows, runtime
        env = self.unwrapped
        if self.num_envs != target:
            raise RuntimeError(f"Morph audit requires exactly {target} environments")
        if runtime is None:
            cfg = env.cfg
            runtime = {
                "success_criterion": "any_rack_hole_v1",
                "first_step_utc": datetime.now(UTC).isoformat(),
                "episode_length_s": cfg.episode_length_s,
                "event_parameters": {
                    name: {
                        key: value
                        for key, value in term.params.items()
                        if isinstance(value, str | int | float | bool | list | tuple | type(None))
                    }
                    for name, term in vars(cfg.events).items()
                    if hasattr(term, "params")
                },
                "action_parameters": {
                    name: {key: getattr(term, key) for key in ("scale", "joint_names") if hasattr(term, key)}
                    for name, term in vars(cfg.actions).items()
                    if hasattr(term, "scale")
                },
            }
        if initial_rows is None and hasattr(env, "_so101_reset_row"):
            initial_rows = env._so101_reset_row.cpu().tolist()

        result = original_step(self, actions)
        dones = result[2].bool()
        if counted is None:
            counted = torch.zeros_like(dones)
        done_ids = dones.nonzero(as_tuple=False).squeeze(-1)
        done_ids = done_ids[~counted[done_ids]]
        if done_ids.numel() == 0:
            return result
        counted[done_ids] = True

        success = env.termination_manager.get_term("success")[done_ids].bool()
        dropped = env.termination_manager.get_term("vial_dropped")[done_ids].bool()
        out_of_bounds = env.termination_manager.get_term("vial_out_of_bounds")[done_ids].bool()
        unstable = env.termination_manager.get_term("unstable_robot")[done_ids].bool()
        timed_out = env.termination_manager.get_term("time_out")[done_ids].bool()
        progress = env._so101_terminal_progress[done_ids]
        peak_force = env._so101_terminal_max_rack_force[done_ids]
        completion = env._so101_terminal_time_to_success_s[done_ids]
        terminal_hole = getattr(env, "_so101_terminal_hole", None)

        for index, env_id in enumerate(done_ids.tolist()):
            succeeded = bool(success[index])
            outcomes.append(
                {
                    "env_id": env_id,
                    "reset_row": initial_rows[env_id] if initial_rows is not None else None,
                    "success": succeeded,
                    "aborted": bool(dropped[index] or out_of_bounds[index] or unstable[index]),
                    "timed_out": bool(timed_out[index]),
                    "unsafe_rack_contact": bool(progress[index, 3]),
                    "grasped": bool(progress[index, 0]),
                    "lifted": bool(progress[index, 1]),
                    "inserted": bool(progress[index, 2]),
                    "completion_seconds": float(completion[index]) if succeeded else None,
                    "peak_rack_force_n": float(peak_force[index]),
                    **(
                        {"hole_index": int(terminal_hole[env_id])}
                        if succeeded and terminal_hole is not None
                        else {}
                    ),
                }
            )

        if len(outcomes) >= target:
            ordered = sorted(outcomes, key=lambda row: row["env_id"])
            summary = {
                "episodes": target,
                "successes": sum(row["success"] for row in ordered),
                "aborts": sum(row["aborted"] for row in ordered),
                "timeouts": sum(row["timed_out"] for row in ordered),
                "unsafe_rack_contacts": sum(row["unsafe_rack_contact"] for row in ordered),
            }
            payload = {
                "format": "morph-so101-audit-v1",
                "summary": summary,
                "argv": invocation,
                "runtime": runtime,
                "checkpoint_sha256": checkpoint_sha256,
                "reset_offset": offset,
                "started_at": started.isoformat(),
                "finished_at": datetime.now(UTC).isoformat(),
                "episodes": ordered,
            }
            output = os.environ.get("SO101_EVALUATION_OUTPUT")
            if not output:
                raise RuntimeError("SO101_EVALUATION_OUTPUT is required for a Morph audit")
            path = Path(output)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            print("MORPH_EVAL_RESULT=" + json.dumps(summary, sort_keys=True), flush=True)
            raise SystemExit(0)
        return result

    RslRlVecEnvWrapper.step = counted_step
    return invocation
