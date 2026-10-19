import hashlib
import io
import json
import zipfile

import pytest
from test_evaluation import result

from morph.contracts import RecoveryPackage
from morph.evaluation import compare
from morph.evidence import export_bundle


def test_empty_bundle_truthful_and_hash_verifiable(store, manifest):
    package = RecoveryPackage(manifests=(manifest,), results=())
    bundle = export_bundle(package, store)
    assert bundle == export_bundle(package, store)
    with zipfile.ZipFile(io.BytesIO(bundle)) as archive:
        checksums = json.loads(archive.read("SHA256SUMS.json"))
        for name, digest in checksums.items():
            assert hashlib.sha256(archive.read(name)).hexdigest() == digest
        assert json.loads(archive.read("package.json"))["results"] == []


def test_fixture_and_missing_artifacts_refused(store, manifest):
    with pytest.raises(ValueError, match="fixture"):
        export_bundle(RecoveryPackage(manifests=(manifest,), results=(result(manifest),)), store)
    with pytest.raises(KeyError):
        export_bundle(
            RecoveryPackage(manifests=(manifest,), results=(result(manifest, provenance="simulation"),)),
            store,
        )


def test_forged_report_refused_before_export(store, manifest):
    baseline = manifest.model_copy(update={"split": "held_out"})
    trial = baseline.model_copy(update={"method": "morph"})
    baseline_result, trial_result = result(baseline), result(trial)
    report = compare(baseline, baseline_result, trial, trial_result)
    forged = report.model_copy(update={"candidate_successes": 999})
    with pytest.raises(ValueError, match="report"):
        export_bundle(
            RecoveryPackage(
                manifests=(baseline, trial), results=(baseline_result, trial_result), report=forged
            ),
            store,
        )
