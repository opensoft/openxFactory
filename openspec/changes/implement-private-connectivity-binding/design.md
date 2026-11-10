# Design: Private connectivity binding

Status: draft

## Context

[The runtime binding plan](../../../docs/self-hosted-runtime-binding-plan.md) already uses reference-only installation outputs. Reuse that seam and existing credential custody. The installer selection is an operator decision. The file scopes and realization authorization in this packet are proposed.

## Decisions

| T001 key | Owner and proposed file scope | Release and verification |
| --- | --- | --- |
| neutral_binding | `opensoft/openxFactory`. `contracts/private-connectivity/`, `scripts/validate-private-connectivity.py`, `tests/private_connectivity/`, and bundle files required by the [versioning policy](../../../docs/contract-versioning-policy.md). | Additive bundle with allocation at cut. Proposed targeted check `python3 -m pytest tests/private_connectivity -q`, plus contract release checks. |
| installer | `opensoft/xFactory-Installer`. Proposed `src/private_connectivity/`, `tests/private_connectivity/`, `docs/private-connectivity.md` with a binding entry point inside that source directory. The current source tree is a scaffold. | Installer release consuming the pinned binding. Run the existing `make validate` and `make test` entry points with new conformance cases discovered under `tests/`. |
| evidence_tooling | `opensoft/openxFactory` feature 040. `specs/040-private-connectivity/verify-evidence.py` and `specs/040-private-connectivity/tests/test_verify_evidence.py`. | Feature branch evidence tool. `python3 -m unittest discover -s specs/040-private-connectivity/tests -p test_verify_evidence.py`. |

Bind installation identity, customer, environment, operator mode, endpoint, network and approval references, and observed policy revision. Keep operation identity stable across retries. Reauthorize retries and reject changed input under the same key. Keep the prior authorized binding active while testing a candidate. On rollback, revoke partial target access and reuse the prior binding only while it remains authorized.

The checker validates evidence shape, dependencies, revisions and numeric thresholds. Owners run their actual tests and reviewers inspect the underlying results. The checker has no provisioning or credential access.

## Risks and trade-offs

Do not activate a binding when authorization, endpoint identity, enrollment, or effective policy verification fails. Check a known-good application connection before counting a denial. Invalid or absent optional fields must not silently select managed mode.

## Migration and verification

Qualify compatibility against unbound installations and synthetic local and managed fixtures. Release the neutral binding before broad installer adoption. Gate live installer tests on G0 and the managed selection test on G1. Confirm native paths and commands with each owner before recording T001 as passed.
