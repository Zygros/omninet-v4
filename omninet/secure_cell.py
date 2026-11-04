"""Authenticated cell envelope primitives for the OmniNet research prototype.

This module provides application-layer AES-256-GCM authenticated encryption.
It is not a replacement for Tor's circuit encryption, key exchange, or a full
production key-management system. Callers must supply a fresh 32-byte key and
must never reuse a nonce with the same key.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from typing import Any, Dict

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

PROTOCOL = "omninet.cell.v1"
KEY_BYTES = 32
NONCE_BYTES = 12


class CellError(ValueError):
    """Raised when a cell is malformed or fails authentication."""


def canonical_json(value: Any) -> bytes:
    """Serialize JSON deterministically for hashing and authenticated data."""
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def state_digest(state: Any) -> str:
    """Return the SHA-256 digest of a canonical JSON state value."""
    return hashlib.sha256(canonical_json(state)).hexdigest()


def seal_cell(key: bytes, payload: bytes, state: Any, sequence: int) -> Dict[str, Any]:
    """Encrypt and authenticate a payload bound to a state digest and sequence.

    The sequence is authenticated metadata, not a replay-prevention mechanism by
    itself. Receivers must persist and enforce their own replay window.
    """
    if not isinstance(key, bytes) or len(key) != KEY_BYTES:
        raise CellError("key must be exactly 32 bytes (AES-256)")
    if not isinstance(payload, bytes):
        raise CellError("payload must be bytes")
    if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence < 0:
        raise CellError("sequence must be a non-negative integer")

    nonce = os.urandom(NONCE_BYTES)
    header = {
        "protocol": PROTOCOL,
        "sequence": sequence,
        "state_sha256": state_digest(state),
        "created_at": int(time.time()),
    }
    aad = canonical_json(header)
    ciphertext = AESGCM(key).encrypt(nonce, payload, aad)
    return {
        "header": header,
        "nonce": nonce.hex(),
        "ciphertext": ciphertext.hex(),
    }


def open_cell(key: bytes, envelope: Dict[str, Any], expected_state: Any) -> bytes:
    """Authenticate, validate state binding, and decrypt a cell envelope."""
    if not isinstance(key, bytes) or len(key) != KEY_BYTES:
        raise CellError("key must be exactly 32 bytes (AES-256)")
    try:
        header = envelope["header"]
        nonce = bytes.fromhex(envelope["nonce"])
        ciphertext = bytes.fromhex(envelope["ciphertext"])
        if header["protocol"] != PROTOCOL:
            raise CellError("unsupported protocol")
        if nonce.__len__() != NONCE_BYTES:
            raise CellError("invalid nonce length")
        if header["state_sha256"] != state_digest(expected_state):
            raise CellError("state digest mismatch")
        if not isinstance(header["sequence"], int) or header["sequence"] < 0:
            raise CellError("invalid sequence")
        aad = canonical_json(header)
        return AESGCM(key).decrypt(nonce, ciphertext, aad)
    except CellError:
        raise
    except Exception as exc:
        raise CellError("malformed envelope or authentication failure") from exc
