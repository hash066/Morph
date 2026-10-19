"""Single-account local durable queue. Reservations survive worker crashes."""

from __future__ import annotations

import hashlib
import json
import sqlite3
import time
import uuid
from contextlib import contextmanager
from pathlib import Path

from morph.contracts import Budget, RunManifest, RunResult


class Conflict(ValueError):
    pass


class Store:
    def __init__(self, path: Path, capacity: Budget):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self.capacity = capacity
        with self.connect() as db:
            db.executescript("""
                PRAGMA journal_mode=WAL;
                CREATE TABLE IF NOT EXISTS jobs (
                  id TEXT PRIMARY KEY, manifest TEXT NOT NULL, state TEXT NOT NULL,
                  lease TEXT, deadline REAL, error TEXT, result TEXT);
                CREATE TABLE IF NOT EXISTS reservations (
                  id TEXT PRIMARY KEY, rollouts INTEGER NOT NULL, wall REAL NOT NULL,
                  gpu REAL NOT NULL, cost REAL NOT NULL);
                CREATE TABLE IF NOT EXISTS events (
                  seq INTEGER PRIMARY KEY AUTOINCREMENT, job TEXT NOT NULL,
                  time REAL NOT NULL, state TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS calls (
                  id TEXT PRIMARY KEY, receipt TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS artifacts (
                  hash TEXT PRIMARY KEY, content BLOB NOT NULL);
            """)

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=30)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    def _reserve(self, db, key: str, budget: Budget):
        totals = db.execute(
            "SELECT COALESCE(SUM(rollouts),0),COALESCE(SUM(wall),0),"
            "COALESCE(SUM(gpu),0),COALESCE(SUM(cost),0) FROM reservations"
        ).fetchone()
        requested = (budget.rollouts, budget.wall_seconds, budget.gpu_hours, budget.cost_usd)
        cap = (
            self.capacity.rollouts,
            self.capacity.wall_seconds,
            self.capacity.gpu_hours,
            self.capacity.cost_usd,
        )
        if any(t + r > c + 1e-12 for t, r, c in zip(totals, requested, cap)):
            raise Conflict("account budget exhausted")
        db.execute("INSERT INTO reservations VALUES (?,?,?,?,?)", (key, *requested))

    def reserve_call(self, cost: float, wall_seconds: int) -> str:
        key = uuid.uuid4().hex
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            # Calls consume a scheduler slot as well as time and spend.
            self._reserve(db, key, Budget(rollouts=1, wall_seconds=wall_seconds, gpu_hours=0, cost_usd=cost))
        return key

    def receipt(self, key: str, receipt: dict):
        with self.connect() as db:
            db.execute("INSERT INTO calls VALUES (?,?)", (key, json.dumps(receipt, sort_keys=True)))

    def submit(self, manifest: RunManifest) -> str:
        manifest = RunManifest.model_validate_json(manifest.canonical())
        key = manifest.digest()
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            if db.execute("SELECT 1 FROM jobs WHERE id=?", (key,)).fetchone():
                return key
            self._reserve(db, key, manifest.budget)
            db.execute(
                "INSERT INTO jobs(id,manifest,state) VALUES (?,?,'queued')", (key, manifest.canonical())
            )
            db.execute("INSERT INTO events(job,time,state) VALUES (?,?,'queued')", (key, time.time()))
        return key

    def list(self, limit: int = 100, offset: int = 0) -> list[dict]:
        with self.connect() as db:
            return [
                dict(r)
                for r in db.execute(
                    "SELECT id,state,error FROM jobs ORDER BY rowid DESC LIMIT ? OFFSET ?",
                    (max(1, min(limit, 100)), max(0, offset)),
                )
            ]

    def get(self, key: str) -> dict:
        with self.connect() as db:
            row = db.execute("SELECT * FROM jobs WHERE id=?", (key,)).fetchone()
            if row is None:
                raise KeyError(key)
            return dict(row)

    def claim(self) -> dict | None:
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT * FROM jobs WHERE state='queued' ORDER BY rowid LIMIT 1").fetchone()
            if row is None:
                return None
            lease = uuid.uuid4().hex
            manifest = RunManifest.model_validate_json(row["manifest"])
            db.execute(
                "UPDATE jobs SET state='running',lease=?,deadline=? WHERE id=?",
                (lease, time.time() + manifest.budget.wall_seconds, row["id"]),
            )
            db.execute("INSERT INTO events(job,time,state) VALUES (?,?,'running')", (row["id"], time.time()))
            return {**dict(row), "state": "running", "lease": lease}

    def cancel(self, key: str):
        self.get(key)
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            changed = db.execute(
                "UPDATE jobs SET state='cancelled',lease=NULL WHERE id=? AND state IN ('queued','running')",
                (key,),
            ).rowcount
            if changed:
                db.execute("INSERT INTO events(job,time,state) VALUES (?,?,'cancelled')", (key, time.time()))

    def expire(self, now: float | None = None) -> int:
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            rows = db.execute(
                "SELECT id FROM jobs WHERE state='running' AND deadline < ?",
                (time.time() if now is None else now,),
            ).fetchall()
            for row in rows:
                db.execute(
                    "UPDATE jobs SET state='interrupted',lease=NULL,error='lease_expired' WHERE id=?",
                    (row["id"],),
                )
                db.execute(
                    "INSERT INTO events(job,time,state) VALUES (?,?,'interrupted')", (row["id"], time.time())
                )
            return len(rows)

    def finish(self, key: str, lease: str, result: RunResult):
        from morph.evaluation import validate_result

        result = RunResult.model_validate_json(result.canonical())
        manifest = RunManifest.model_validate_json(self.get(key)["manifest"])
        validate_result(manifest, result, require_complete=True)
        if any(e.provenance != "simulation" for e in result.episodes):
            raise Conflict("test fixtures cannot enter the production queue")
        for episode in result.episodes:
            self.artifact(episode.raw_artifact_sha256)
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            changed = db.execute(
                "UPDATE jobs SET state='succeeded',result=?,lease=NULL "
                "WHERE id=? AND state='running' AND lease=? AND deadline>=?",
                (result.canonical(), key, lease, time.time()),
            ).rowcount
            if not changed:
                raise Conflict("inactive or expired lease")
            db.execute("INSERT INTO events(job,time,state) VALUES (?,?,'succeeded')", (key, time.time()))

    def fail(self, key: str, lease: str, code: str):
        if code not in {"runtime_failed", "budget_exceeded", "artifact_invalid", "cancelled_worker"}:
            raise ValueError("failure must use a redacted error code")
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            changed = db.execute(
                "UPDATE jobs SET state='failed',error=?,lease=NULL "
                "WHERE id=? AND state='running' AND lease=?",
                (code, key, lease),
            ).rowcount
            if not changed:
                raise Conflict("inactive lease")
            db.execute("INSERT INTO events(job,time,state) VALUES (?,?,'failed')", (key, time.time()))

    def put_artifact(self, content: bytes) -> str:
        if len(content) > 16 * 1024 * 1024:
            raise ValueError("artifact exceeds 16 MiB; large replay storage not enabled")
        key = hashlib.sha256(content).hexdigest()
        with self.connect() as db:
            db.execute("INSERT OR IGNORE INTO artifacts VALUES (?,?)", (key, content))
        return key

    def artifact(self, key: str) -> bytes:
        with self.connect() as db:
            row = db.execute("SELECT content FROM artifacts WHERE hash=?", (key,)).fetchone()
        if row is None:
            raise KeyError(key)
        content = bytes(row["content"])
        if hashlib.sha256(content).hexdigest() != key:
            raise Conflict("artifact integrity failed")
        return content
