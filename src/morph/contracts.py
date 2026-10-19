from __future__ import annotations

import hashlib
import json
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

Identifier = Annotated[str, Field(pattern=r"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}$")]
Digest = Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
Nonnegative = Annotated[float, Field(ge=0, allow_inf_nan=False)]


class Frozen(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", allow_inf_nan=False)

    def canonical(self) -> str:
        return json.dumps(self.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))

    def digest(self) -> str:
        return hashlib.sha256(self.canonical().encode()).hexdigest()


class TaskConfig(Frozen):
    task_id: Literal["IsaacTutorial-Place-Vial-SO101"] = "IsaacTutorial-Place-Vial-SO101"
    tutorial_commit: Literal["9a4286b4bc8a5720ac97f87e5e0140f7542c22d9"] = (
        "9a4286b4bc8a5720ac97f87e5e0140f7542c22d9"
    )
    backend: Literal["newton_mjwarp"] = "newton_mjwarp"
    checkpoint_sha256: Digest
    evaluator_sha256: Digest
    lock_sha256: Digest


class Perturbation(Frozen):
    """Private to evaluator. Never serialize this into a planner prompt."""

    condition_id: Identifier
    vial_mass_kg: Annotated[float, Field(gt=0, le=0.030)]
    recoverable: bool
    vial_friction_coeff: Annotated[float, Field(ge=0.2, le=1.3)] = 0.7
    actuator_gain_multiplier: Annotated[float, Field(ge=1.0, le=1.5)] = 1.0


class Candidate(Frozen):
    candidate_id: Identifier
    arm_scale_multiplier: Annotated[float, Field(ge=0.5, le=1.0)] = 1.0
    jaw_scale_multiplier: Annotated[float, Field(ge=0.5, le=1.0)] = 1.0
    # These conservative exploratory limits are NOT yet simulator-validated.


class Case(Frozen):
    condition_id: Identifier
    seed: Annotated[int, Field(ge=0, le=2**31 - 1)]
    start_id: Annotated[int, Field(ge=0)]

    def key(self) -> tuple[str, int, int]:
        return self.condition_id, self.seed, self.start_id


class Budget(Frozen):
    rollouts: Annotated[int, Field(gt=0, le=10000)]
    wall_seconds: Annotated[int, Field(gt=0, le=86400)]
    gpu_hours: Nonnegative
    cost_usd: Nonnegative


class RunManifest(Frozen):
    schema_version: Literal[1] = 1
    task: TaskConfig
    candidate: Candidate
    method: Literal["baseline", "random", "morph", "no_history"]
    split: Literal["development", "held_out"]
    cases: Annotated[tuple[Case, ...], Field(min_length=1, max_length=10000)]
    budget: Budget

    @model_validator(mode="after")
    def valid_cases(self):
        if len({c.key() for c in self.cases}) != len(self.cases):
            raise ValueError("duplicate cases")
        if len(self.cases) > self.budget.rollouts:
            raise ValueError("rollout budget exceeded")
        if self.method == "baseline" and (
            self.candidate.arm_scale_multiplier != 1 or self.candidate.jaw_scale_multiplier != 1
        ):
            raise ValueError("baseline must preserve controller")
        return self


class EpisodeResult(Frozen):
    case: Case
    success: bool
    aborted: bool
    unsafe: bool
    completion_seconds: Nonnegative | None
    provenance: Literal["simulation", "test_fixture"]
    raw_artifact_sha256: Digest

    # Preserve the environment-owned task success independently of safety and abort flags.
    # Eligibility is decided by evaluation; importing evidence must not rewrite task success.

    @model_validator(mode="after")
    def successful_episode_has_completion_time(self):
        if self.success and self.completion_seconds is None:
            raise ValueError("successful episode requires completion time")
        return self


class RunResult(Frozen):
    manifest_sha256: Digest
    episodes: tuple[EpisodeResult, ...]
    wall_seconds: Nonnegative
    gpu_hours: Nonnegative
    inference_cost_usd: Nonnegative
    compute_cost_usd: Nonnegative


class Observation(Frozen):
    """Only this numeric, development-only projection crosses the planner boundary."""

    candidate_id: Identifier
    successes: Annotated[int, Field(ge=0)]
    episodes: Annotated[int, Field(gt=0)]
    aborts: Annotated[int, Field(ge=0)]
    unsafe: Annotated[int, Field(ge=0)]
    mean_completion_seconds: Nonnegative | None

    @model_validator(mode="after")
    def counts(self):
        if max(self.successes, self.aborts, self.unsafe) > self.episodes:
            raise ValueError("count exceeds denominator")
        return self


class Proposal(Frozen):
    hypotheses: Annotated[tuple[Annotated[str, Field(max_length=600)], ...], Field(max_length=3)]
    candidate_id: Identifier | None
    reason: Annotated[str, Field(min_length=1, max_length=1000)]
    decision: Literal["experiment", "insufficient_evidence", "no_validated_recovery"]

    @model_validator(mode="after")
    def consistent(self):
        if (self.decision == "experiment") != (self.candidate_id is not None):
            raise ValueError("experiment requires candidate; refusal must not select one")
        return self


class EvaluationReport(Frozen):
    baseline_manifest: Digest
    candidate_manifest: Digest
    denominator: int
    baseline_successes: int
    candidate_successes: int
    paired_gain: float | None
    paired_gain_interval95: tuple[float, float] | None
    decision: Literal["no_validated_recovery", "simulation_candidate", "incomplete"]
    reason: str
    total_wall_seconds: Nonnegative
    total_gpu_hours: Nonnegative
    total_cost_usd: Nonnegative


class RecoveryPackage(Frozen):
    schema_version: Literal[1] = 1
    manifests: tuple[RunManifest, ...]
    results: tuple[RunResult, ...]
    report: EvaluationReport | None = None
    physical_deployment_approved: Literal[False] = False
