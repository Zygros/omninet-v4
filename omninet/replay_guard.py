"""Transactional replay protection for OmniNet cell sequences.

This is a small persistent receiver-side guard. It prevents duplicate or stale
sequence acceptance per (sender_id, key_id). It does not authenticate senders:
callers must authenticate/decrypt the envelope before recording acceptance and
must derive sender_id/key_id from trusted authenticated metadata.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Union


class ReplayError(ValueError):
    """Raised when a sequence is duplicated or stale."""


class ReplayGuard:
    """Persist monotonic sequence watermarks using SQLite transactions."""

    def __init__(self, database: Union[str, Path]) -> None:
        self.database = str(database)
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS replay_watermarks (
                    sender_id TEXT NOT NULL,
                    key_id TEXT NOT NULL,
                    last_sequence INTEGER NOT NULL CHECK(last_sequence >= 0),
                    PRIMARY KEY (sender_id, key_id)
                )
                """
            )

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.database, timeout=10.0, isolation_level=None)
        conn.execute("PRAGMA busy_timeout = 10000")
        return conn

    def accept(self, sender_id: str, key_id: str, sequence: int) -> None:
        """Accept and persist a strictly increasing sequence or raise ReplayError."""
        if not sender_id or not isinstance(sender_id, str):
            raise ValueError("sender_id must be a non-empty string")
        if not key_id or not isinstance(key_id, str):
            raise ValueError("key_id must be a non-empty string")
        if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence < 0:
            raise ValueError("sequence must be a non-negative integer")

        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute(
                "SELECT last_sequence FROM replay_watermarks "
                "WHERE sender_id = ? AND key_id = ?",
                (sender_id, key_id),
            ).fetchone()
            if row is not None and sequence <= row[0]:
                conn.rollback()
                raise ReplayError(
                    f"stale or duplicate sequence {sequence}; last accepted is {row[0]}"
                )
            conn.execute(
                """
                INSERT INTO replay_watermarks(sender_id, key_id, last_sequence)
                VALUES (?, ?, ?)
                ON CONFLICT(sender_id, key_id)
                DO UPDATE SET last_sequence = excluded.last_sequence
                """,
                (sender_id, key_id, sequence),
            )
            conn.commit()

    def last_accepted(self, sender_id: str, key_id: str):
        """Return the persisted high-water mark, or None if no sequence was accepted."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT last_sequence FROM replay_watermarks "
                "WHERE sender_id = ? AND key_id = ?",
                (sender_id, key_id),
            ).fetchone()
        return None if row is None else row[0]
