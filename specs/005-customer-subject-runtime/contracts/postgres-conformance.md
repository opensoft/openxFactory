# Planning Contract: PostgreSQL 15/16 Conformance

Status: draft

## Namespaces

| Namespace | Authority |
|---|---|
| `xfactory_runtime_v2` | Authoritative topology, principals, grants, bindings, jobs, evidence, and migration ledger |
| `xfactory_runtime_api_v2` | Governed security-definer entrypoints only |
| `xfactory_legacy_quarantine_v2` | Admin-only non-authoritative migration evidence |

PUBLIC receives no schema/table/function authority. V1 `public.hermes_*` remains unchanged.

## Role Classes

- `xfactory_v2_owner`: NOLOGIN object/function owner.
- `xfactory_v2_migrator`: NOLOGIN controlled cutover authority.
- `xfactory_v2_runtime`: NOLOGIN class for per-principal logins.
- `xfactory_v2_control`: NOLOGIN governed API execution only.
- `xfactory_v2_audit`: NOLOGIN approved audit export only.

Runtime/control/audit are NOSUPERUSER, NOCREATEDB, NOCREATEROLE, NOREPLICATION, and NOBYPASSRLS. They cannot assume owner/migrator, create schemas, truncate, reference quarantine, or directly access cross-layer tables/blobs.

## Scope And RLS

- Installation, stack, and layer registration rows are immutable and hold only their initial state; separate append-only predecessor-linked lifecycle-event tables are authoritative for current state.
- A governed transition function serializes on the entity/latest event, appends exactly one valid successor, and updates a non-authoritative current-state projection in the same transaction. Direct registration/event/projection writes and every transition out of `retired` are denied; readiness recomputes projections from event chains.
- `principals` uses composite `(installation_id, stack_id, layer_id, principal_id)` identity and append-only lifecycle events.
- `database_principal_bindings` maps one unique authenticated `session_user` to one exact Principal and role class; no login may map to multiple active Principals, and revocation is append-only.
- Every layer table uses full composite scope/keys and forced RLS.
- `assume_scope` binds `session_user` to an active `assume_scope` grant and live layer/principal.
- Security-definer functions use a fixed safe search path and revoke PUBLIC execute.
- Transaction-local scope is revalidated from authoritative grant data; caller-set custom settings are never sufficient.
- Pool reuse, revoked grants, retired principals/layers, forged settings, role escalation, and cross-stack/install access fail.

## Atomic Cross-Layer Operation

One governed API transaction locks trust/grant/binding/resource identities in canonical order, validates exact source and target resources and time-bound authority, inserts the target projection/artifact, inserts OperationAuthorization, and inserts TraceabilityEdge. Revocation uses the same lock identities/order. The result is either a fully evidenced operation before revocation or no operation after revocation.

## Migration

1. Validate and content-address the mapping outside SQL.
2. Begin SERIALIZABLE and acquire fixed v1 table locks before the first query.
3. Capture snapshot/WAL identity, counts, and deterministic dataset digest.
4. Migrate authoritative rows and quarantine unverifiable evidence.
5. Reconcile IDs/counts/digests and append success ledger evidence.
6. Commit atomically.

Attempt events survive outside the authoritative transaction so crashes/rollbacks can be recorded. Identical `(migration_id, snapshot, mapping_digest)` retry converges; changed input fails.

Before attempt-state evaluation, every runner takes a transaction advisory lock derived from the canonical migration tuple. Allowed latest-event transitions are `started -> succeeded|failed|abandoned`, `failed|abandoned -> started` for an identical retry, and `succeeded` terminal. Concurrent identical runners serialize; the winner executes once and the observer returns the same succeeded result without reapplying rows.

## Runner And Image Contract

```text
scripts/run-hermes-runtime-postgres-tests.sh [--major 15|16] [--json]
scripts/run-hermes-runtime-postgres-tests.sh --update-image-lock
```

- Compose definition: `tests/hermes_runtime_contracts/postgres/compose.yaml`.
- Image lock: `tests/hermes_runtime_contracts/postgres/images.lock.yaml`, with `schema_version`, `kind`, source tag, resolved `postgres@sha256:...`, platform, and update evidence for majors 15/16.
- Normal and release runs use only digest-pinned image references from the lock; `--update-image-lock` is an explicit pre-candidate action and is forbidden after candidate freeze.
- Each run uses a unique Compose project, isolated internal network, no published host port, throwaway named volume, read-only repo mount, healthcheck, and a same-image psql client.
- The runner generates a cryptographically random ephemeral password in memory, passes it without printing, redacts environment/evidence, unsets it, and removes containers/volume/network through an EXIT trap. No fixed password or trust-auth exception is committed.
- Evidence under `tests/hermes_runtime_contracts/postgres/evidence/` records image digests, cases, outcomes, and redacted command metadata; it contains no password or raw database rows.

## Canonical Security Drift Fingerprint

Readiness computes deterministic catalog records/checksums for tables, columns,
constraints, indexes, policies, functions, and triggers plus every security
authority that can bypass isolation: role attributes and memberships;
schema/table/function ownership and ACLs; `relrowsecurity` and
`relforcerowsecurity`; function `prosecdef`, volatility, language, body identity,
and fixed `search_path`; PUBLIC `EXECUTE`/`USAGE`/`CREATE`; and every grant on
authoritative, API, and quarantine namespaces. Canonicalization fixes catalog
query ordering and normalizes only server-generated syntax proven equivalent on
PostgreSQL 15/16. A missing, extra, or altered record fails readiness.

## Required Matrix

- PostgreSQL 15 official image.
- PostgreSQL 16 official image.
- Clean apply and verified reapply.
- Same-name catalog drift.
- Security drift cases independently add `BYPASSRLS`, grant owner/migrator membership, change schema/table/function owner or ACL, disable RLS/FORCE RLS, grant direct authoritative/quarantine access, grant PUBLIC execute/create/usage, make a trusted schema writable, or alter a security-definer function/search path; every case fails readiness.
- Actual non-owner login/RLS/scope pooling.
- Direct topology registration/event/projection mutation, forked predecessor, projection drift, and transition out of retired; every case fails and immutable history remains unchanged.
- Grant/binding/revocation serialization races.
- One-subject/two-subject migration and single-default proof.
- Concurrent v1 write, crash/retry, changed-map replay, and reconciliation failure.
- Quarantine read/reference/promotion denial.
- Concurrent identical migration retry: one executor and one convergent observer.
- No published host port, no persistent network/volume after teardown, and no credential in evidence/log output.

No database test may be skipped at release because Docker or an image is unavailable.
