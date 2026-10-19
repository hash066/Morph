from concurrent.futures import ThreadPoolExecutor

import pytest

from morph.contracts import Budget, Case
from morph.store import Conflict, Store


def test_idempotency_across_restart(store, manifest):
    with ThreadPoolExecutor(4) as pool:
        ids = list(pool.map(lambda _: store.submit(manifest), range(8)))
    assert len(set(ids)) == 1
    reopened = Store(store.path, store.capacity)
    assert len(reopened.list()) == 1
    with reopened.connect() as db:
        assert db.execute("SELECT COUNT(*) FROM reservations").fetchone()[0] == 1


def test_concurrent_reservation_cap(tmp_path, manifest):
    store = Store(tmp_path / "cap.sqlite", Budget(rollouts=1, wall_seconds=10, gpu_hours=0, cost_usd=0))
    other = manifest.model_copy(update={"cases": (Case(condition_id="opaque", seed=11, start_id=0),)})

    def submit(m):
        try:
            return store.submit(m)
        except Conflict:
            return None

    with ThreadPoolExecutor(2) as pool:
        results = list(pool.map(submit, [manifest, other]))
    assert sum(r is not None for r in results) == 1


def test_cancel_and_expire_never_retry(store, manifest):
    key = store.submit(manifest)
    claim = store.claim()
    assert claim["lease"]
    store.cancel(key)
    assert store.get(key)["state"] == "cancelled"
    assert store.claim() is None
    assert store.expire(float("inf")) == 0


def test_expired_job_is_interrupted(store, manifest):
    key = store.submit(manifest)
    store.claim()
    assert store.expire(float("inf")) == 1
    assert store.get(key)["state"] == "interrupted"
    assert store.claim() is None


def test_artifact_content_addressing_and_tamper(store):
    digest = store.put_artifact(b"real bytes, not a trajectory")
    assert store.artifact(digest) == b"real bytes, not a trajectory"
    with store.connect() as db:
        db.execute("UPDATE artifacts SET content=? WHERE hash=?", (b"tampered", digest))
    with pytest.raises(Conflict):
        store.artifact(digest)
    with pytest.raises(KeyError):
        store.artifact("../outside")
