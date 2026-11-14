# Portable reference bootstrap authority

Status: draft; commissioned source candidate, isolated-fixture scope only
Baseline: factory #1311 / adapter #60; T013 refresh remains open in adapter #61

## Context and boundaries

The accepted bootstrap trusts an independently approved static selection and
authenticated actual-run readback, then performs full existing admission. This
slice realizes that capability with a portable service and client. Factory owns
this internal composition; adapter feature 017 owns all implementation tasks.
There is no neutral API promotion or new runtime `services` role.

The service always uses reference profile
`openxfactory-portable-bootstrap-reference-v1` and evidence scope
`isolated-fixture`. Actual GitHub authentication, public hosting, hostile-host
defense, deployed administration and human assurance are excluded. Default
operational bindings and all existing offline entrypoints remain unchanged.

## Decisions

### D1 — Explicit durable initialization and one-run binding

An explicit operator initializer creates a new private store and returns its
filesystem identity. Startup requires that expected initialized store, owner-only
directory/database permissions, ordinary unlinked files and exact schema version;
it never recreates missing/replaced/corrupt state. SQLite DELETE journal,
synchronous FULL and bounded busy wait supply local transaction durability.
Each request uses its own connection and transaction.

Operator authorization inserts one immutable static document under an opaque
preauthorization reference. Duplicate authorization cannot reset consumption.
Atomic claim binds it to exactly one complete context/run/attempt, materializes
the full configuration by inserting only the two assigned run fields and issues
a deterministic run-bound operation reference. Same-context refresh returns the
same binding; changed attempts/runs refuse. Revocation persists and cannot be
reactivated. Reservations and audit data are retained after fixture cleanup.
A persistent clock high-water mark refuses observed regression across restart.
Privileged database tampering or restoration of a valid old backup remains out
of scope; loss/recovery requires explicit operator scope replacement.

### D2 — Independent signed fixture context

A separately selected Ed25519 public key verifies domain-separated canonical
control-plane observations. The closed observation binds exact DispatchContext,
event reference, fixture scope and a current interval of at most 60 seconds.
An operator-approved preauthorization/static digest and actual run context must
match. Unknown fields, alternate profiles, keys/URLs from requests, forged,
future/expired or conflicting observations refuse. The authority retains the
authenticated observation and revalidates it before claim/operation readback.

Only the authenticated control-plane role registers observations. The admission
reader can request current readback but cannot approve static selections or
register context. The worker has no allowed authority action. Fixture signatures
are real cryptography over simulated control-plane evidence; they are not GitHub
signatures, tokens or live provider authentication. Compromise of the selected
operator/controller/authority host remains compromise of the trusted boundary.

### D3 — Bounded authenticated reference transport

Use loopback-only HTTPS/mTLS with configured certificate fingerprints and roles
outside request bodies. Roles are operator, controller, reader and denied worker;
actual peer certificates determine permissions. Client validates CA, hostname and
the selected server fingerprint. No redirect, proxy, environment plugin or
request-selected resolver can change its endpoint/trust/credential selection.

POST `/` has a closed internal JSON request with one action: authorize, observe,
claim, operation or revoke. The operator can authorize/revoke, controller can
observe, reader can claim/read operation. Requests/responses are bounded to
64 KiB with strict UTF-8/duplicate-member decoding; nested selection/runtime
documents keep their existing 16 KiB grammar. Concurrency is bounded, sockets and
clients have real timeouts, and SQLite waits are bounded. Errors are fixed; no
raw body, signed envelope, credential, key or provider exception is logged.

Claim returns a fixture-scoped bundle of independently approved full config,
BootstrapReadback and OperationReadback. The client checks profile/principals,
configuration digests/projection and current context before constructing trusted
adapter capabilities. A new fresh authority request is required for bootstrap
and operation readback; a cached bundle does not bypass revocation/admission.
Existing independent configuration/source/protection measurements, scheduler,
active lease and earliest-deadline checks remain separate capabilities.

### D4 — Isolated owning-wallet rehearsal

Prepare a static document before registering the assigned run observation. A
separate authority process authenticates registration and claims; the trusted
embedding binds its result into accepted bootstrap/admission. After assignment,
register the exact full-config-bound plan/lease before readiness. The accepted
owning wallet implementation creates/verifies one cryptographic proof; the
existing replay gate rejects repeated proof use. The authority binds one run,
not a new distributed exactly-once signature protocol.

Test success, refusal before signing, concurrent claims, restart/revocation,
ambiguous response, direct worker authority denial, changed source/run/attempt
and independent cleanup after failure/cancellation/hard runner exit. Preserve
retained replay/authority records and shared resources. Same-user reference
processes and fixture keys do not prove deployed OS/admin separation.

## Risks and trade-offs

- Reference clocks and control-plane roots are operator-selected fixtures;
  live authentication and issuance need separate source and operational review.
- SQLite provides one-host local durability, not a distributed consensus or
  malicious-backup rollback guarantee. Missing/changed state refuses.
- Failure after binding may consume a preauthorization even if the caller gets
  no response. Only same-context recovery is permitted; no unbind/reset exists.
- Existing cleanup and proof replay semantics remain authoritative. A fresh
  authority response alone cannot manufacture runtime/human acceptance.

## Migration and review

No accepted input, machine key, neutral API, dependency pin or consumer lock is
changed. Add opt-in reference modules and substantive fixed-matrix tests. Keep
the production CLI unselected. Adapter candidate is stacked on documentation
PR #61 until it lands; this commission does not merge that PR. Publish paired
factory/adapter candidates for source acceptance after isolated gates and review.
T013/T014/T015 and every setup/dispatch stage remain incomplete/unauthorized.
