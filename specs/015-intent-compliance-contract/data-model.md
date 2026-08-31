# Data Model: Intent Compliance Contract

## Shared value forms

- **Digest**: `sha256:` followed by 64 lowercase hexadecimal characters.
- **Canonical record**: RFC 8785 JSON Canonicalization Scheme UTF-8 bytes.
- **Policy source**: repository, path, immutable 40-hex revision, content
  digest, ratification-record reference, and ratification-record digest.
- **Allowance reference**: exactly `registry_id` plus `allowance_id`.
- **Authority proof**: principal identity, authority role, and digest-bound
  citation that closes to the owning policy authority.

## Veto-class vocabulary

Carries vocabulary identity, policy source, unique class identifiers, issuer and
revoker authority roles, and optional bounded domain detection metadata.
Identifiers are unique within one vocabulary. Detection metadata is evidence,
never policy authority.

## Policy allowance

Immutable approval carrying registry-lifetime allowance identity, vocabulary
identity/digest, class identifier, neutral scope, operations, scope digest,
issuer proof, approval time, validity bounds, and canonical approval digest.

## Policy allowance revocation

Append-only event carrying revocation identity, target approval digest,
predecessor event/revision digest, revoking principal and authority proof,
effective time, and canonical event digest. It never mutates approval facts.

## Policy allowance registry

Append-only revision carrying registry identity, revision identity/digest,
predecessor revision digest, publication time, and entries mapping each
lifetime-unique allowance ID to one approval digest plus current revocation
event digests. An identifier can never be repointed.

## Compliance decision

Carries decision identity, closed outcome, evaluated-content digest,
policy/vocabulary digests, registry identity/current revision digest, canonical
allowance-reference set, resolved approval/revocation/scope verdict digests,
all layer findings, bounded rationale/evidence, evaluator identity/version,
optional bounded classifier evidence, correlation references, and evaluation
time.

## State transitions

```text
approval absent -> immutable allowance approval
approval current -> additive revocation event -> approval revoked
registry revision N -> append-only revision N+1
evaluation -> allow | block | needs_human_review
static dispatch evidence(head=N) + trusted snapshot head=N -> evidence valid
static dispatch evidence(head=N) + trusted snapshot head=N+1 -> evidence stale
domain runtime -> re-evaluate and enforce invocation behavior
```

## Closed outcome rules

- Unclaimed veto finding: `block`.
- Claimed but unresolved/ambiguous allowance: `needs_human_review`.
- Revoked, expired, unauthorized, or non-covering allowance: `block`.
- Current authorized covering allowance: satisfies that finding.
- Classifier `veto_signal`, `indeterminate`, `error`, timeout, missing limits, or
  cap breach: at least `needs_human_review`.
- Composition precedence: `block > needs_human_review > allow`.
