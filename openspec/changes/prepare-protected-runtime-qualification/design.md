# Proposed protected runtime composition

Status: draft; preparation only

## Context

The source-accepted baseline is factory #1304 / openXwallet #48. Its trusted
embedding injects every loader, verifier, clock, signer and owning proof API.
The worker supplies only a challenge ID, request, token and signed observation.
See the [proposal](proposal.md) for motivation and the existing
[baseline profile](../add-workload-factory-binding/supporting-docs/profile.md)
for immutable signing, grant, time, observation and replay rules.

## Goals / Non-Goals

Prepare an implementation-ready machine proof composition and measurable live
acceptance boundary. No runtime code, socket service, provider key, published
contract, release, protected workflow or domain execution lock is created by
this preparation. No human authentication, consent, marker or production effect
is inferred. Existing source acceptance remains valid within its stated scope.

## Decisions

### D1 — Ownership and operational input

Factory governance owns this composition and its proposed internal operational
projection in [launch inputs](supporting-docs/launch-inputs.md). openXwallet owns
implementation and one Speckit list, feature 017. The projection is not a new
neutral standard, a promoted contract or codeXfactory's executable dependency
lock. Any later canonical promotion requires its own owner-approved schema,
validator and integrity protection. No canonical contract is owned by the adapter.

This reuses the baseline split; placing a keyholding service in openXfactory or
forking wallet/custody schemas in the consumer would violate that split.

### D2 — Issuer transport feeds the accepted verifier

Use a separate opt-in runtime module. Offline validators and the existing
snapshot verifier retain zero network access. Trusted operator configuration
fixes GitHub's issuer, discovery and JWKS locations; validate discovery against
those exact approved strings. Token headers cannot supply endpoints, keys,
loaders or network destinations. HTTPS certificate/hostname validation is
mandatory, redirects disabled, and requests carry no credentials/cookies.

Proposed pilot bounds: 5-second connect / 10-second overall fetch deadline,
256 KiB decoded response, 64 JWK entries, bounded exact kid, duplicate JSON
members or eligible key IDs refused. Require a public RSA signing key compatible
with the existing RS256 verifier. Existing header/x5t and signature rules remain.

Cache only an issuer-scoped public snapshot in memory. Its administrative deadline
is at most 300 seconds after fetch, shortened by applicable HTTP freshness rules.
Respect no-store/no-cache; require successful fresh 200 data when revalidation is
needed. Coalesce refreshes; an unknown kid permits one bounded refresh and one
verification retry, with at most one refresh initiation per issuer per 30 seconds.
Throttled unknown keys refuse. Never extend stale keys on outage or union removed
keys back into a replacement snapshot. These numbers are proposed policy, not
GitHub service guarantees. Removal detection is bounded by freshness, not instant
revocation. No persistent cache or new JWT library/leeway is selected.

A runtime verifier implements the accepted `verify(token, expected, *, now)`
interface and delegates crypto/claim checks to the source-accepted verifier.
The earliest trusted snapshot/token/policy/observation deadline remains effective
at every existing fresh-clock checkpoint after blocking work.

### D3 — Trusted launch, challenge and supervisor

An operator-controlled embedding selects exact accepted source/profile hashes,
issuer/audience, expected signed claims, current canonical records, authenticated
challenge loader, state identity, opaque custody client and supervisor trust.
Expected values never come from an unverified token or worker environment.
Claims bind immutable repository/owner IDs, caller and reusable workflow refs and
SHAs, protected environment, exact configured subject, source ref/SHA and run/attempt.
Name compatibility in browser-origin checks grants no claim normalization.

The challenge loader authenticates its selected service and obtains current
canonical challenge data tied to the verified subject, request and run. A worker
cannot submit a replacement challenge record or select its resolver. No public
service protocol is standardized here; an embedding transport remains internal
and must authenticate/bound its untrusted request before trusted dependencies
can be reached. Its final deployment/service references are execution inputs.

The supervisor is a separately administered control plane with its key, policy,
measurement source and credentials inaccessible to the worker. It measures the
actual approved launch source/configuration and key/transport binding, then signs
the existing per-token/request/challenge/policy/run observation. A shared worker
host or Docker socket cannot establish this boundary. Same-user local fixtures
prove behavior only. The model's own digest, different keys or containers alone
cannot pass deployed independence. The trusted host/admin remain inside the TCB;
no hostile-host, TEE or model-behavior attestation is claimed.

### D4 — Confined gate as custody trust boundary

For this proposed pilot, custody authenticates a confined trusted gate deployment.
Only that approved gate instance receives the narrow signing credential and
owning proof primitive; the gate enforces the per-use workload, challenge,
composition, grant and one-use checks. Direct worker access to the credential,
control plane or a valid canonical signing preimage must be denied.

An mTLS peer/subject allowlist alone is insufficient: deployed credential issuance,
source/configuration selection, network/process boundary and actual worker denial
must be independently demonstrated. This design keeps the existing neutral custody
API. If the owner requires custody itself to verify a new per-use assertion, this
profile refuses that unsupported trust model and requires a neutral-owner change;
the adapter must not invent a replacement custody protocol.

### D5 — Protected state and lifecycle

The operator provisions private persistent replay state with a selected deployment
identity and records its initialization outside worker control. Runtime startup
requires that expected existing state; absent, uninitialized, corrupt or observably
changed state refuses rather than silently bootstrapping a replacement. Existing
reservation-before-signing and consumed-on-failure rules remain unchanged.

The trusted-host boundary is explicit: hostile live byte tampering or rollback
of a valid backup is not solved by this adapter. Restore/replacement is prohibited
for an active pilot scope; recovery requires operator revocation and a new approved
scope, not reuse of consumed identities. State/credential retention, cancellation
and cleanup authority are selected before live execution. Success, failure and
cancellation need independent run-scoped absence readback, preserving shared
resources and safe audit evidence. Missing readback fails qualification.

### D6 — Acceptance before operation

Owner acceptance and implementation commissioning precede runtime implementation.
Source conformance and isolated transport/process tests precede any separately
authorized protected run. The live run must use actual configured services and
GitHub token, not synthetic substitutes. An operator readback of environment
protection is separate from the signed environment claim. Missing input produces
blocked/not-performed. The machine receipt supplies part of codeXfactory T002;
independent human broker acceptance and domain tasks remain separately gated.

## Risks / Trade-offs

- Availability is reduced by strict endpoint/freshness/refresh bounds; test outages
  and obtain owner acceptance of those bounds before implementation.
- A compromised trusted gate/supervisor/host defeats this trust model; keep its
  credential and administrative plane outside worker control and qualify access.
- Post-sign checks detect observed changes but do not provide distributed atomic
  revocation or undo a custody signature already made.
- Live GitHub/service/protection selection remains absent; preparation cannot
  establish real runtime assurance or authorize provider administration.

## Migration Plan

No migration occurs now. Preserve the accepted source profile and pins. Review
this packet and adapter feature 017; implement only after owner commissioning.
Publish no consumer runtime lock until its complete owned validation/protection
contract exists. Later live setup/dispatch needs its own scoped operator act.
Rollback disables only the opt-in bridge and revokes its temporary authority,
preserving replay reservations and approved redacted evidence.

## Deferred operational selections

Exact non-secret service references, protected environment, workflow/source SHAs,
issuer audience/subject, supervisor and gate credential identities, storage and
janitor references are not selected. They do not change this proposed architecture;
all are mandatory execution inputs and fail closed while absent.
