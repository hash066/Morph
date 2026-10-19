import pytest
from test_evaluation import result

from morph.store import Conflict


def test_finish_requires_real_artifact_and_active_lease(store, manifest):
    key = store.submit(manifest)
    claim = store.claim()
    fixture = result(manifest)
    with pytest.raises(Conflict, match="fixtures"):
        store.finish(key, claim["lease"], fixture)
    # Unit-test values only. This test never writes into production data/.
    simulation_contract = result(manifest, provenance="simulation")
    with pytest.raises(KeyError):
        store.finish(key, claim["lease"], simulation_contract)
    digest = store.put_artifact(b"explicit unit-test artifact, not simulator output")
    simulation_contract = simulation_contract.model_copy(
        update={
            "episodes": tuple(
                e.model_copy(update={"raw_artifact_sha256": digest}) for e in simulation_contract.episodes
            )
        }
    )
    store.finish(key, claim["lease"], simulation_contract)
    assert store.get(key)["state"] == "succeeded"
    with pytest.raises(Conflict, match="lease"):
        store.finish(key, claim["lease"], simulation_contract)


def test_failure_is_redacted_and_terminal(store, manifest):
    key = store.submit(manifest)
    claim = store.claim()
    with pytest.raises(ValueError):
        store.fail(key, claim["lease"], "secret-token-in-error")
    store.fail(key, claim["lease"], "runtime_failed")
    assert store.get(key)["error"] == "runtime_failed"
    with pytest.raises(Conflict):
        store.fail(key, claim["lease"], "runtime_failed")
