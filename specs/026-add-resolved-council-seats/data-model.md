# Data Model: Resolved Council Seats

Status: draft

**Date**: 2026-08-28

**Feature**: `026-add-resolved-council-seats`

## Modeling Rules

- A convening has exactly one candidate revision, one matched candidate class,
  one immutable governed rule revision, and one resolved required-seat roster.
- `required_seats` is a non-empty ordered list with unique seat identifiers; its
  authority is set membership, while order is retained for reproducible output.
- Every standing seat is required. A conditional seat is required exactly when
  independent evaluation of its cited governed condition against the recorded
  normalized facts returns true.
- Producer authentication establishes who submitted an artifact, not whether its
  roster is correct. Admission reproduces the resolution independently.
- The admitted candidate head must equal the provenance candidate head. Drift,
  ambiguity, missing facts, or an unavailable immutable rule fails closed.
- The validated roster and provenance become immutable before seat jobs exist.
- A frozen snapshot remains authoritative when rules or candidate-class content
  later change.
- Private signing key material is forbidden from neutral convening, snapshot,
  job, return, fixture, and evidence artifacts.

## Contract Entities

### CouncilConvening

The neutral producer-to-consumer handoff for one per-candidate council.

| Field | Required | Rules |
|---|---:|---|
| `schema_version` | yes | Contract-family version; closed supported value |
| `kind` | yes | `resolved-council-convening` |
| `convening_id` | yes | Durable non-empty identifier for this convening attempt |
| `required_seats` | yes | Non-empty unique seat IDs; no undeclared identifier |
| `required_seats_provenance` | yes | Complete RosterProvenance |

The canonical schema is closed at every object boundary. Domain-specific job
payloads, GitHub events, policy source text, and signing material are not fields.

### CandidateRevision

Exact candidate under review and the observation used to detect stale facts.

| Field | Required | Rules |
|---|---:|---|
| `repository` | yes | Canonical `owner/repository` identifier |
| `pull_request` | yes | Positive integer in that repository |
| `head_revision` | yes | Lowercase 40-hex Git object ID used for resolution |

At admission, the consumer receives or obtains an authoritative current head and
compares it to `head_revision`. A mismatch is `candidate_head_stale`; it is never
silently refreshed inside the old artifact.

### GovernedRuleReference

Immutable locator for the candidate-class rule independently loaded by producer
and consumer.

| Field | Required | Rules |
|---|---:|---|
| `repository` | yes | Canonical `owner/repository` identifier |
| `path` | yes | Normalized repository-relative path; no traversal |
| `revision` | yes | Lowercase 40-hex Git object ID |
| `matched_class` | yes | Non-empty domain-owned class identifier |

The locator must resolve to exactly one governed rule object. Missing,
unavailable, mutable, or ambiguous resolution is `rule_revision_unavailable`.

### NormalizedFacts

A closed-for-the-matched-rule mapping of the exact fact values consumed by its
conditions. Fact names and scalar/list value domains are defined by the governed
rule, not by openxFactory. Raw provider payloads and unused observations are
excluded.

Rules:

- facts bind to CandidateRevision and cannot describe another head;
- every fact referenced by the matched condition is present exactly once;
- unknown or unused facts may be refused by the domain evaluator;
- no secret, credential, private key, absolute host path, or raw webhook payload
  is permitted.

### SeatResolutionEvidence

Producer-recorded decomposition of the final roster. It supports deterministic
neutral set arithmetic but does not substitute for independent rule evaluation.

| Field | Required | Rules |
|---|---:|---|
| `standing_seats` | yes | Non-empty unique list declared by matched class |
| `conditional_seats` | yes | Zero or more ConditionalSeatEvaluation records |

### ConditionalSeatEvaluation

| Field | Required | Rules |
|---|---:|---|
| `seat` | yes | Declared conditional seat identifier; unique in evaluation list |
| `condition_ref` | yes | Stable condition identifier within the cited rule object |
| `required` | yes | Producer result recorded for audit; consumer recomputes it |

The expected roster set is `standing_seats` union every `seat` whose independently
evaluated condition is true. Producer `required` and consumer result must agree,
and that set must equal `CouncilConvening.required_seats`.

### RosterProvenance

| Field | Required | Rules |
|---|---:|---|
| `candidate` | yes | CandidateRevision |
| `governed_rule` | yes | GovernedRuleReference |
| `normalized_facts` | yes | NormalizedFacts |
| `resolution` | yes | SeatResolutionEvidence |

No opaque digest or producer conclusion alone satisfies provenance.

## Consumer Runtime Entities

These entities are successor obligations and are not canonical openxFactory
runtime records.

### FrozenConveningSnapshot

Immutable admission result binding:

- convening and candidate identity;
- exact `required_seats` order and set;
- complete RosterProvenance;
- admitted rule/candidate revisions;
- one initially empty seat-to-job mapping.

The snapshot is written atomically before job allocation. Any failure before the
snapshot exists issues zero jobs.

### SeatJobAssignment

One-to-one mapping from a frozen seat to one issued job identity. The seat set is
not editable and job code receives only its assigned seat plus frozen context.
Adding a seat, allocating two jobs for one seat, or sharing a job across seats is
invalid.

### SeatReturn

One signed result from one admitted SeatJobAssignment. The consumer validates
job/seat identity and signature, rejects unlisted seats, determines substantive
return status, and reads the declared outcome field for unanimity. Signature and
provenance fields do not participate in outcome equality.

## State Transitions

```text
producer facts + immutable rule
          |
          v
       resolved
          |
          v
consumer reproduces roster and candidate head
      |                           |
      | valid                     | invalid / stale / unavailable
      v                           v
     frozen                    refused
      |
      v
one job per frozen seat
      |
      v
collect admissible substantive returns
      |                           |
      | every frozen seat         | required return missing
      v                           v
evaluate unanimity              parked
      |
      +--> unanimous outcome --> completed
      +--> verdict-less failure/recovery remains governed by existing behavior
```

`refused`, `frozen`, and the snapshot's roster/provenance are terminal for one
admission attempt. A fresh candidate head or rule requires a new resolution and
new attempt, not mutation.

## Validation Invariants And Finding Codes

| Invariant | Primary finding code |
|---|---|
| `required_seats` exists, is non-empty, and is well formed | `roster_absent`, `roster_empty`, or `roster_malformed` |
| Seat identifiers are unique | `roster_duplicate` |
| Every seat is declared by the matched rule | `roster_unknown_seat` |
| Every standing seat is present | `roster_standing_incomplete` |
| Submitted roster equals independently reproduced set | `roster_mismatch` |
| Provenance includes retrievable immutable rule and consumed facts | `provenance_opaque`, `rule_revision_unavailable`, or `fact_missing` |
| Candidate head still equals provenance head | `candidate_head_stale` |
| No job exists before snapshot freeze | successor invariant; admission fails without issuance |
| Returns come only from frozen seats/jobs | successor finding `return_seat_unlisted` |
| Signing key is job-local and private material absent from artifacts | successor isolation and artifact tests |

## Security And Privacy Boundaries

- Repository identifiers, PR numbers, Git revisions, class IDs, seat IDs, and
  normalized non-secret facts are contract data.
- Provider tokens, OIDC tokens, database credentials, raw webhooks, private key
  bytes, and local checkout paths are forbidden.
- Fixture repositories and revisions are synthetic or immutable public test
  objects; no fixture depends on mutable network state.
- The neutral validator does not authorize work. It supplies portable contract
  conformance; the consuming admission transaction owns authorization and freeze.
