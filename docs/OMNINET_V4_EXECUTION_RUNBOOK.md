# OmniNet v4 Execution Runbook

**Status:** additive implementation increment on branch `sovereign-execution/secure-cell-verification`.
This runbook describes a testable vertical slice. It does not claim that a production
mesh or HTC-420 deployment is already running.

## Scope of current increment

- Application-layer AES-256-GCM cell sealing and authentication.
- Canonical JSON state digest using SHA-256.
- Authenticated protocol, sequence, timestamp, and state-digest metadata.
- SQLite-backed monotonic replay guard scoped by sender and key identifier.
- Focused tests for cell round trips, tampering, state mismatch, wrong keys, invalid
  inputs, replay rejection, persistence, and independent sender/key scopes.
- Aligned PEP 440 package version declarations across Poetry, setuptools, and runtime.

## Local verification

From the repository root:

```bash
python -m pip install -e . --no-deps
python -m pip install "cryptography>=35.0.0,<36.0.0" pytest
python -m pytest tests/test_secure_cell.py tests/test_replay_guard.py tests/test_package_version.py -q
python -m pytest tests/ -q
```

The focused suite must pass before this increment is promoted. The full repository
test suite remains a separate gate. The focused CI install intentionally avoids
installing every legacy application dependency; the existing pandas <2.0 constraint
is not needed by the secure-cell slice and currently has no compatible wheel for
the Python 3.12 matrix job.

## Security constraints

1. Use a cryptographically random 32-byte key for AES-256-GCM.
2. Never reuse a nonce with the same key. This implementation generates a random
   96-bit nonce; high-volume production use requires a reviewed nonce strategy.
3. Store keys in a platform-appropriate secret store. Never commit keys, tokens,
   onion-service private keys, or wallet secrets.
4. State hashes detect mismatch against a supplied expected state; they do not prove
   that the state is trusted. Trust requires authenticated provenance.
5. The sequence field is authenticated but does not prevent replay by itself.
   The SQLite guard rejects duplicate/stale monotonic sequences per sender/key.
6. The caller must authenticate/decrypt the envelope before recording acceptance
   and must derive sender/key identifiers from authenticated metadata. Strictly
   increasing sequences reject out-of-order delivery; a bounded replay window may
   be preferable for transports where reordering is expected.
7. The replay guard uses SQLite transactions and a unique sender/key watermark.
   Multi-host deployments require a shared strongly consistent store or another
   explicitly designed distributed replay protocol.
8. Tor provides its own circuit-level protections. This module is additional
   application-layer protection, not a custom Tor relay implementation.
9. Do not describe this increment as a complete zero-trust mesh or security
   certification.

## HTC-420 mapping

- Tier 1: payload arrives as validated bytes or a schema-validated object.
- Tier 2: dispatch routes envelopes without sharing secret keys by default.
- Tier 3: persist sequence/replay state transactionally.
- Tier 4: recovery retains failed envelopes and diagnostics as append-only evidence.
- Tier 5: verify authentication, schema, state binding, and replay policy.
- Tier 6: anchor a manifest containing hashes and test receipts, never secret material.

## Deployment gates

- [ ] Focused tests pass in CI.
- [ ] Full test suite passes in CI.
- [ ] Dependency and secret scans pass.
- [ ] Key provisioning and rotation are documented and tested.
- [ ] Live Tor integration is tested in a controlled environment.
- [ ] Multi-host replay semantics are designed and tested before federation.
- [ ] Merkle/OTS/Arweave receipts are independently verified.
- [ ] Runtime measurements and a rollback plan are recorded.

## Evidence labels

Use **DESIGNED**, **IMPLEMENTED**, **TESTED**, **DEPLOYED**, and
**INDEPENDENTLY VERIFIED** as distinct states. A commit establishes source
provenance; it does not establish that code has run successfully in production.
