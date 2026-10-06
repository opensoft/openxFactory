# Factory MCP conformance design

Lane: mcp-family-contract

## Context

See [proposal](proposal.md). Existing codex tools already have closed schemas,
host-derived evaluation context and lossless transport mappings. A shared
profile must explain those boundaries without rewriting them. Ops DNS planning
is the second comparison; no executable DNS behavior belongs here.

## Goals / Non-Goals

Produce a locally verifiable declaration contract. Record where behavior is
demonstrated, merely declared, or unresolved. Neither validation success nor
the presence of a tool name establishes a deployed or accepted service.

## Decisions

### D1. A versioned artifact, separate from MCP wire descriptors

Use a closed JSON Schema (Draft 2020-12) for a declaration document:
`schema_version: 1`, `kind: factory_mcp_conformance`,
`profile: advisory-v1`, `domain`, `contract_version`, `source`,
`service`, `tools`, `evidence`, and `gaps`.
All nested records are closed; tool IDs and evidence/gap IDs are unique.

`source` names repository, immutable revision and artifact references.
`service` distinguishes domain identity from optional installation,
environment and canonical resource URI. A non-deployed contract declares
deployment state explicitly; it cannot pretend an example URI is live.

Each tool declares its owner, input/output/error schema references, binding
mapping, effects, outcome mapping, evidence policy, repetition policy, limits
and supporting evidence IDs. These are declaration fields, not additions to
MCP tools/list. Schemas stay domain-specific; no generic submit_job is imposed.

Semantic checks operate on structured declarations, not prose interpretation.
Binding authority is an explicit trusted-host source; revocation is an explicit
posture enum. Each outcome-map entry names its domain discriminator value,
completed-evaluation or execution-failure class and isError boolean. Finite
status/code inventories point to enum/const nodes in the pinned schemas.
Coverage is checked against those resolved finite sets, including union
variants. A schema whose status vocabulary cannot be mechanically resolved is
an explicit mapping gap; the validator must not infer completeness from prose.
Evidence and gap records have IDs and declared concern keys referenced by the
tool, so missing support and contradictory assertions are mechanically visible.

Alternative rejected: a universal request envelope. It would change closed
codex schemas and impose irrelevant domain fields and job lifecycles.

### D2. References are pinned and offline

A schema reference names its repository, full revision, relative artifact path
and SHA-256 digest. Local verification takes an explicit mapping from
repository/revision to supplied snapshot roots. It verifies requested digests,
JSON Schema validity and contained local references without network fetches,
dynamic imports or executing schema content. Unknown, absolute, traversal or
symlink-escaping paths fail. Remote JSON Schema references cannot trigger I/O.

For records of external implementation observations, a source citation can name
a pinned file plus an explanatory mapping. It is evidence for the claimed
observation, not executable implementation and not a conformance certificate.

### D3. Declare effects independently from authority

The initial profile fixes `authority_effect: none`. Effects separately declare
external reads, execution, persistence and mutation; all are explicit booleans.
Mutation means target business-state mutation and must be false for this
profile; replay storage is persistence, not a DNS write. Execution is allowed
only when declared bounded and host-controlled. Each declared effect identifies
its trusted boundary and supporting evidence or an unresolved gap.

No boolean read_only annotation overrides this declaration. MCP annotations are
descriptive hints; validation does not turn them into enforcement.

### D4. Mappings preserve domain meaning

A binding mapping explains verified principal input, host-resolved subject,
permitted operation, policy origin, neutral scope references and revocation
posture. Existing neutral vocabulary is referenced, never duplicated as a
second authority registry. A startup-frozen binding records that limitation.

Outcome mapping exhaustively covers the referenced domain result statuses and
error codes. Negative findings are completed evaluations; execution failures
are errors. structuredContent contains the domain object unchanged. A separate
mapping states MCP isError behavior. No common wrapper is inserted into an
existing result digest or signature.

The evidence policy declares allowed output, redaction, input/context identity,
timestamps and artifact-provenance association. Missing runtime sinks and
unresolved scope mappings remain gaps, not promises.

### D5. Repetition is a tagged choice

Closed modes: `reevaluate`, `lease_replay`, `fresh_observation`.
Each declares deadline behavior. lease_replay requires key/principal scoping,
conflict/in-progress semantics, storage/coordination evidence and timestamp
preservation. fresh_observation requires host-pinned maximum age, observation
time and a final freshness check; a caller cannot extend the host limit.

The semantic validator rejects contradictions such as lease_replay with no
persistence declaration, fresh_observation with no external-read declaration,
an error mapping that turns dependency failure into eligibility, or an advisory
profile that grants approval.

### D6. Validation reports facts at the level it can prove

Report structural validity, reference integrity, semantic consistency and
unresolved gaps separately, with stable diagnostic codes and JSON locations.
Malformed input or contradictory declarations exit nonzero.
A structurally valid declaration with honest gaps is valid-with-gaps and cannot
claim verified conformance. Source-pinned behavioral evidence is recorded for
review; this offline validator does not certify its sufficiency or certify a
deployment. The CLI returns 0 only for valid declarations (with gap status
explicit in machine and human output), 1 for invalid declarations, and 2 for
unreadable inputs or unavailable reference roots.

### D7. Implementation and domain examples stay separated

Neutral fixtures use synthetic domains and synthetic schemas. A narrative
codex compatibility mapping records the two tools at immutable source revisions,
including exact schema digests, result mapping and explicit gaps; it does not
ship engineering evaluation code. Ops authors the executable DNS mapping in
its own repository. No codex adoption or package amendment happens here.

## Risks / Trade-offs

- Declaration mistaken for certification → distinct validation dimensions and
  explicit gaps, with no deployment-ready conclusion from offline checks.
- Caller-selected reference paths → resolve within explicitly supplied
  snapshot roots and reject escaping or network references.
- Policy duplication → domain status/code meanings remain source-owned.
- Sibling release races → allocate versions and claim shared release metadata
  only at realization; current proposal reserves none.

## Migration Plan

Additive, opt-in profile. Existing clients and tools keep working unchanged.
One Speckit feature builds schema, validator, fixtures and guidance after
ratification. Adoption is separately reviewed against accepted immutable
artifacts. Rollback of an adoption restores the prior consumer pin under its
existing governance; this proposal itself moves no pin.

## Open Questions

Later hosting work selects installation identities, freshness values, audit
sinks and reader implementations. A common transport library requires evidence
from two real adapters. None changes the first offline validation slice.
