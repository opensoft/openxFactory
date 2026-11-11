# Candidate factory/workload binding profile

Status: ratified for source acceptance only, 2026-11-11. Not a published contract or accepted pilot
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

## Reviewed conformance and refusal rules

The verifier accepts the documented optional GitHub x5t header as metadata only;
kid plus the approved key snapshot still selects trust. Both iat and nbf must
independently be at or before the trusted clock, with now before exp and a maximum
300-second exp-minus-iat lifetime. A backdated nbf grants no lifetime extension.

Every grant parent field that is present must be a valid reference; null is not
a root. Review-class chains (the existing exact review act token) refuse until
the factory's canonical operator-anchor and review-register checks are composed.
This candidate never bypasses them or implements an alternative issuer anchor.

Existing replay state must retain its initialized schema/version and uniqueness
constraints. Full database integrity, including index/table consistency, is
checked at startup. The exact schema/version/constraints are checked inside every
reservation transaction; uninitialized or malformed state is never reset.
Storage remains a trusted-host boundary. No resistance to hostile live byte
changes, deletion/recreation or restoration of an older valid backup is claimed.

After blocking validation, after reservation and before returning a proof, the
gate checks a fresh trusted clock against the earliest policy, wallet, grant,
challenge, token, key-snapshot and observation deadline. Clock errors are fixed
refusals. The observer validates the actual launched worker's invocation context
and measures its verified owner source, transport identity and public binding.
