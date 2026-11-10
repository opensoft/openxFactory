# Design: Headscale install ownership

Status: ratified
Ratified: 2026-11-10 by Brett Heap. [Ratification record](review/ratification-2026-11-10.md)

## Context

Headscale-Install is a proposed repository name. The authenticated GitHub lookup returned 404 for the candidate slug. Use the repository boundary and reviewed bootstrap pattern established for [Keycloak-Install](../implement-keycloak-install-repo/proposal.md).

## Decisions

| T001 key | Owner and proposed scope | Release and verification |
| --- | --- | --- |
| headscale_install | Proposed private `opensoft/Headscale-Install`, default branch `main`. Seed scope `README.md`, `SECURITY.md`, `docs/ownership.md`, and `Makefile`. Runtime scope for separate approval `packaging/`, `deploy/`, `docs/runbooks/`, `tests/qualification/`, and `release/`. | Independently versioned install artifact. Proposed `make validate` and `make test` entry points plus pinned real-client qualification under the authorized pilot. Bootstrap confirms the verification entry points and governance before runtime scope is recorded. |
| ops | `opensoft/OpsxFactory`. Proposed `workflows/private-connectivity/`, `docs/private-connectivity/`, and `tests/private_connectivity/`. | OpsxFactory operating procedure revision pinned to the qualified install release. Proposed `python3 -m pytest tests/private_connectivity -q` plus owner repository gates. |

The install repository owns repeatable packaging, dedicated instance deployment, policy initialization, backup, restore and upgrade mechanisms, and release pins. OpsxFactory owns the operator procedures, approvals, revocation, recovery authorization, incident handling, and evidence. Product onboarding consumes the install and operations interfaces.

Treat each managed boundary as a dedicated Headscale instance. Verify an explicit deny-by-default policy before issuing enrollment. Require separate route approval. Recover in quarantine, fence the prior writer and reconcile current revocations before serving traffic.

## Risks and trade-offs

Qualify restore and upgrade against pinned builds and record the results with the install release. Recovery of one boundary must preserve the other boundary's availability. Keep policy, key material, and customer backups in their authorized custody.

## Migration and verification

Approve the repository name, accountable maintainer, bootstrap scope, review controls and release ownership first. Verify repository identity and route membership through the estate inventory process. Confirm the OpsxFactory owner and exact paths independently. Run G0 before live enrollment and require G1 and G4 for pilot qualification.
