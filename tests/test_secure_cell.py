import copy

import pytest
from cryptography.exceptions import InvalidTag

from omninet.secure_cell import CellError, open_cell, seal_cell, state_digest


def test_round_trip_and_state_binding():
    key = b"k" * 32
    state = {"epoch": 7, "mode": "test"}
    envelope = seal_cell(key, b"hello mesh", state, 1)
    assert open_cell(key, envelope, state) == b"hello mesh"
    assert len(state_digest(state)) == 64
    with pytest.raises(CellError, match="state digest mismatch"):
        open_cell(key, envelope, {"epoch": 8, "mode": "test"})


def test_tampering_is_rejected():
    key = b"k" * 32
    envelope = seal_cell(key, b"payload", {"ok": True}, 9)
    changed = copy.deepcopy(envelope)
    changed["header"]["sequence"] = 10
    with pytest.raises(CellError):
        open_cell(key, changed, {"ok": True})


def test_wrong_key_is_rejected():
    envelope = seal_cell(b"a" * 32, b"payload", {}, 0)
    with pytest.raises(CellError):
        open_cell(b"b" * 32, envelope, {})


@pytest.mark.parametrize("key", [b"", b"x" * 31, b"x" * 33])
def test_bad_key_length_is_rejected(key):
    with pytest.raises(CellError, match="32 bytes"):
        seal_cell(key, b"payload", {}, 0)


def test_invalid_sequence_is_rejected():
    with pytest.raises(CellError, match="sequence"):
        seal_cell(b"x" * 32, b"payload", {}, -1)
