# Compute gate

No resources provisioned. No deployment manifest can claim a verified image/GPU combination yet.
Use an existing authorized Nebius VM first; do not assume Serverless Jobs compatibility.

Required before provisioning: project/account identity, current remaining hackathon credit,
region GPU quota and availability, exact hourly instance/storage/transfer rates, aggregate cap,
maximum runtime, idle shutdown, and provider-side spend/termination controls. If any is absent,
stop at this gate. A local reservation does not cap cloud billing for an orphaned instance.

Runtime target is the exact tutorial pin, Python 3.12, CUDA 13 Torch, Newton/MJWarp, without
Isaac Sim. Linux driver minimum 580.65.06 (580.95.05+ recommended); Docker GPU execution
requires NVIDIA Container Toolkit. Save nvidia-smi, driver/runtime versions, resolved lock,
image digest, headless renderer test and actual billing evidence. Do not adopt a legacy Isaac Sim
container for this backend. Container/image pin remains BLOCKED until tested on the target VM.

Run the zero-action test before training. Run one short benchmark to measure wall/GPU time,
then allocate a bounded training/evaluation job that fits verified credits. Stop on timeout,
failed artifact integrity, invalid physics, exhausted reservation or cancellation. Preserve logs
and partial outcomes. No retry may silently consume a new budget.

Controller integration follow-up: nominal arm scale 0.033 rad, jaw 0.02 rad; proposed multipliers
[0.5,1.0] only reduce these offsets but are NOT validated recoveries. Demonstrate target/action
sensitivity without altering observations/reward/termination. Confirm mass/friction after
play_mode before labeling a trial perturbed. No second embodiment or GR00T dependency.
