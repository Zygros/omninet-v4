import pytest

from omninet.replay_guard import ReplayError, ReplayGuard


def test_accepts_increasing_sequence_and_persists(tmp_path):
    db = tmp_path / "replay.db"
    guard = ReplayGuard(db)
    guard.accept("node-a", "key-1", 4)
    guard.accept("node-a", "key-1", 5)
    assert guard.last_accepted("node-a", "key-1") == 5
    assert ReplayGuard(db).last_accepted("node-a", "key-1") == 5


def test_rejects_duplicate_and_stale_sequences(tmp_path):
    guard = ReplayGuard(tmp_path / "replay.db")
    guard.accept("node-a", "key-1", 10)
    with pytest.raises(ReplayError):
        guard.accept("node-a", "key-1", 10)
    with pytest.raises(ReplayError):
        guard.accept("node-a", "key-1", 9)
    assert guard.last_accepted("node-a", "key-1") == 10


def test_sender_and_key_scopes_are_separate(tmp_path):
    guard = ReplayGuard(tmp_path / "replay.db")
    guard.accept("node-a", "key-1", 10)
    guard.accept("node-b", "key-1", 1)
    guard.accept("node-a", "key-2", 1)
    assert guard.last_accepted("node-b", "key-1") == 1
    assert guard.last_accepted("node-a", "key-2") == 1


@pytest.mark.parametrize("sequence", [-1, True, 1.5])
def test_rejects_invalid_sequence(tmp_path, sequence):
    guard = ReplayGuard(tmp_path / "replay.db")
    with pytest.raises(ValueError):
        guard.accept("node-a", "key-1", sequence)
