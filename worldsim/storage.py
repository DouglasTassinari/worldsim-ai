"""SQLite persistence for worlds and annual snapshots."""
import json
import sqlite3
from pathlib import Path
from worldsim.models import WorldState, YearRecord


class SimulationStore:
    def __init__(self, path: str = "data/worldsim.sqlite3"):
        self.path = path
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT NOT NULL,
                year INTEGER NOT NULL,
                payload TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )""")

    def _connect(self):
        return sqlite3.connect(self.path)

    def save(self, run_id: str, world: WorldState, records: list[YearRecord]):
        payload = {"world": world.model_dump(mode="json"), "records": [r.model_dump(mode="json") for r in records]}
        with self._connect() as db:
            db.execute("INSERT INTO snapshots(run_id, year, payload) VALUES (?, ?, ?)",
                       (run_id, world.year, json.dumps(payload)))

    def load_latest(self, run_id: str):
        with self._connect() as db:
            row = db.execute("SELECT payload FROM snapshots WHERE run_id=? ORDER BY id DESC LIMIT 1",
                             (run_id,)).fetchone()
        return json.loads(row[0]) if row else None
