"""Portable evidence export with deterministic content-addressed artifact names."""

import hashlib
import io
import json
import zipfile

from morph.contracts import RecoveryPackage
from morph.evaluation import compare, validate_result
from morph.store import Store


def export_bundle(package: RecoveryPackage, store: Store) -> bytes:
    manifests = {m.digest(): m for m in package.manifests}
    if len(manifests) != len(package.manifests):
        raise ValueError("duplicate manifests")
    if len({r.manifest_sha256 for r in package.results}) != len(package.results):
        raise ValueError("duplicate run results")
    if package.report is not None:
        results = {r.manifest_sha256: r for r in package.results}
        report = package.report
        expected = compare(
            manifests[report.baseline_manifest],
            results[report.baseline_manifest],
            manifests[report.candidate_manifest],
            results[report.candidate_manifest],
        )
        if report != expected:
            raise ValueError("report does not match evaluator-owned results")
    files = {"package.json": package.canonical().encode()}
    for result in package.results:
        if result.manifest_sha256 not in manifests:
            raise ValueError("orphan result")
        validate_result(manifests[result.manifest_sha256], result, require_complete=True)
        for episode in result.episodes:
            if episode.provenance != "simulation":
                raise ValueError("fixture results are not exportable simulation evidence")
            digest = episode.raw_artifact_sha256
            files[f"artifacts/{digest}"] = store.artifact(digest)
    # Limit total bundle size as well as individual artifacts.
    if sum(len(content) for content in files.values()) > 64 * 1024 * 1024:
        raise ValueError("bundle exceeds 64 MiB; external replay storage required")
    files["README.txt"] = (
        b"Morph evidence package v1\n"
        b"Mode: Simulation. This package never approves physical deployment.\n"
        b"An empty results list means no simulation result is available.\n"
        b"Verify every file against SHA256SUMS.json before analysis.\n"
        b"Manifests contain task, checkpoint/evaluator/lock hashes, cases, method and budgets.\n"
        b"Recorded replay is not live execution. Raw artifact bytes retain original content.\n"
    )
    files["SHA256SUMS.json"] = json.dumps(
        {name: hashlib.sha256(content).hexdigest() for name, content in sorted(files.items())},
        sort_keys=True,
        indent=2,
    ).encode()
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 19, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, content)
    return stream.getvalue()
