# Candidate factory/workload binding profile

Status: draft candidate, 2026-11-11. Not a published contract or accepted pilot
binding. Runtime adapter API: `opensoft/openXwallet`,
`specs/016-factory-workload-binding/contracts/adapter-api.md`.

The operator selects the policy, current wallet registry and existing wallet/grant
records, supervisor trust and issuer key snapshot. A worker can supply only its
token, requested act/object/run context, challenge ID and signed observation.
It cannot choose loaders, authority records, verification keys or custody client.

A policy binds one agent holder, active wallet, exact key/custody/binding revision,
public-key digest and selected grant. Every ancestor must be active and current,
address that holder/wallet, and restrict explicit acts/objects at `act` authority.
Child sets/lifetimes can only narrow; required approval posture stays true and
agents cannot approve. This profile authorizes proof production, never an apply
operation or human approval.

Workload identity requires RS256, trusted issuer/audience and fresh approved key
snapshot; exact repository/owner immutable IDs, caller/reusable workflow refs and
SHAs, environment, subject, source and run/attempt; strict bounded timestamps.
Reusable-workflow claims are mandatory. No wildcard or token-selected JWKS URL.

The independently signed observation covers a domain-separated canonical payload:
token digest, challenge/request digests, policy ID/revision, wallet/key/subject/grant,
run/attempt, measured artifact/configuration digest and at most 60 seconds of
validity. An operator-selected separate supervisor key verifies it. The reference
observer hashes files it reads; worker-provided measurement claims are insufficient.

The trusted gate loads its own active challenge and checks the bound request. It
atomically and durably reserves both issuer/token JTI and issuer/challenge ID
before invoking opaque custody through the owning wallet primitive. Failures stay
reserved. Current policy, grant and registry facts are rechecked before returning.
Output separates existing possession proof from local authority facts and always
states that no human approval is supplied.

Live issuer authenticity/refresh, environment protection, observer independence,
custody-client confinement and challenge-service authentication require later
deployment qualification. Fixtures use synthetic OIDC and ephemeral keys. Their
success cannot clear codeXfactory T002 or authorize any external effect.

Unsupported grant constraints (including distinct-holder references) and unknown authority fields refuse. The selected wallet public-key material must match the current registry; the observer launches the selected reference worker and hashes its source/configuration independently. No hostile OS-isolation claim is made.
