# OmniNet v4 Execution Runbook

**Status:** implementation increment on branch `sovereign-execution/secure-cell-verification`.
This runbook describes an additive, testable vertical slice. It does not claim
that a production mesh or HTC-420 deployment is already running.

## Scope of this increment

- Application-layer AES-256-GCM cell sealing and authentication.
- Canonical JSON state digest using SHA-256.
- Authenticated protocol, sequence, timestamp, and state-digest metadata.
- Tests for round trips, tampering, wrong keys, invalid key lengths, and invalid sequences.

## Local verification

From the repository root:

```bash
python -m pip install -e .
python -m pip install pytest
python -m pytest tests/test_secure_cell.py -q
python -m pytest tests/ -q
```

The focused test suite must pass before this increment is promoted. The full
repository test suite remains a separate gate.

## Security constraints

1. Use a cryptographically random 32-byte key for AES-256-GCM.
2. Never reuse a nonce with the same key. This implementation generates a
   random 96-bit nonce; high-volume production use requires a reviewed nonce
   allocation strategy and key rotation policy.
3. Store keys in a platform-appropriate secret store. Do not commit keys,
   tokens, onion-service private keys, or wallet secrets.
4. State hashes detect mismatch against a supplied expected state; they do not
   prove that the state is trusted. Trust requires authenticated provenance.
5. The sequence field is authenticated but does not prevent replay alone.
   Receivers must persist replay windows and reject duplicate/stale sequences.
6. Tor provides its own circuit-level protections. This module is additional
   application-layer protection, not a custom Tor relay implementation.
7. Do not describe this increment as a complete zero-trust mesh or security
   certification.

## HTC-420 mapping

- Tier 1: payload must arrive as validated bytes or a schema-validated object.
- Tier 2: dispatch may route envelopes but must not share secret keys by default.
- Tier 3: persist sequence/replay state transactionally.
- Tier 4: recovery must retain failed envelopes and diagnostics as append-only evidence.
- Tier 5: verify authentication, schema, state binding, and replay policy.
- Tier 6: anchor a manifest containing hashes and test receipts, never secret material.

## Deployment gates

- [ ] Focused tests pass in CI.
- [ ] Full test suite passes in CI.
- [ ] Dependency and secret scan pass.
- [ ] Replay protection is implemented at the receiver.
- [ ] Key provisioning and rotation are documented and tested.
- [ ] Tor integration is tested in a controlled environment.
- [ ] Merkle/OTS/Arweave receipts are independently verified.
- [ ] Runtime measurements and a rollback plan are recorded.

## Evidence labels

Use **DESIGNED**, **IMPLEMENTED**, **TESTED**, **DEPLOYED**, and **INDEPENDENTLY VERIFIED**
as distinct states. A commit establishes source provenance; it does not establish
that code has run successfully in production.
