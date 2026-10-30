# OmniNet v4 packaging and secure-cell CI reconciliation — 2026-10-30

## Scope

This is an additive execution record for [PR #1](https://github.com/Zygros/omninet-v4/pull/1), branch `sovereign-execution/secure-cell-verification`.

- Verified head commit: `a3badb9faea0ae2206b57a03803d7b368a44467b`
- Base branch: `main`
- PR state at recording: open, unmerged
- Operating boundary: local prototype and focused CI only; no production deployment or external anchor is claimed.

## Findings and implemented corrections

1. The original Poetry version `3.0.0-UNITY` was rejected as invalid PEP 440 metadata.
2. After normalizing it to `3.0.0+unity`, Poetry could parse the version but could not infer the package directory because the distribution is named `omninet-v4` while the Python package is `omninet`.
3. The all-dependencies editable install also pulled the legacy `pandas<2.0` constraint. On Python 3.12 that resolved to a source build and failed in the hosted environment. The focused secure-cell tests do not need the complete legacy application dependency set.

The branch now:

- Uses `3.0.0+unity` consistently in `pyproject.toml`, `setup.py`, and `omninet/__init__.py`.
- Declares Poetry's package mapping explicitly: `packages = [{ include = "omninet" }]`.
- Adds `tests/test_package_version.py` to keep all three version declarations aligned and require the intended PEP 440 local build label.
- Installs the project editable with `--no-deps` in the focused workflow, then installs only `cryptography>=35.0.0,<36.0.0` and `pytest`.
- Runs secure-cell, replay-guard, and package-version tests across Python 3.10, 3.11, and 3.12.
- Updates the runbook to match the actual focused verification command and to explain why the legacy pandas dependency is excluded from this test slice.

## Source blob identities at the verified head

| Path | Blob SHA |
|---|---|
| `pyproject.toml` | `b15c64edee2159e8a52b53544441663add670682` |
| `setup.py` | `ad7937e36a1a668e3515a25828350cf61d089bed` |
| `omninet/__init__.py` | `13739ff9c495a9eda866e17e3c1407696ce24359` |
| `tests/test_package_version.py` | `3f66f13a2d32250db3f62cef060f5ea5e6868e5b` |
| `.github/workflows/secure-cell-tests.yml` | `1bac5237eeeff954246de85da883e51b9a64415d` |
| `docs/OMNINET_V4_EXECUTION_RUNBOOK.md` | `305b1d217a94499466e01a3368c97ab0a43a813b` |

## Verification results

### Focused secure-cell / replay / package-version matrix

- [Pull-request workflow run 41113319963](https://github.com/Zygros/omninet-v4/actions/runs/41113319963): **SUCCESS**.
- [Push workflow run 41113315066](https://github.com/Zygros/omninet-v4/actions/runs/41113315066): **SUCCESS**.
- Python 3.10: **14 passed**.
- Python 3.11: **14 passed**.
- Python 3.12: **14 passed**.

The test job installs the project metadata and the minimal cryptography/test dependencies required for this focused slice. Pip reports that the remaining declared application dependencies are intentionally not installed because the job uses `--no-deps`; this is an expected dependency-scope warning, not a failed test.

### Phoenix Audit

- [Pull-request Phoenix Audit run 41113320040](https://github.com/Zygros/omninet-v4/actions/runs/41113320040): **SUCCESS**, Python suite **21 passed**.
- [Push Phoenix Audit run 41113315001](https://github.com/Zygros/omninet-v4/actions/runs/41113315001): **SUCCESS**, Python suite **21 passed**.

The Phoenix Audit compile/test path completed successfully for this revision.

## Evidence classification

| Item | State |
|---|---|
| PEP 440 version correction | IMPLEMENTED |
| Poetry package mapping | IMPLEMENTED |
| Version consistency regression test | TESTED |
| Focused secure-cell/replay tests | TESTED |
| Python 3.10/3.11/3.12 matrix | TESTED |
| Phoenix Audit | TESTED |
| Full repository test suite | NOT CLAIMED by this focused workflow |
| Dependency/security review | NOT COMPLETED by this record |
| Live Tor integration | NOT RUN |
| Multi-host replay semantics | NOT RUN |
| Production deployment | NOT PERFORMED |
| OTS/Bitcoin/Arweave anchoring | NOT PERFORMED or independently verified |

Earlier failed runs on intermediate commits remain historical evidence. The successful runs above are bound to the corrected head and supersede those intermediate failures for the current focused checks only.
