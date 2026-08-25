# intent-compliance Specification (delta)

## ADDED Requirements

### Requirement: Standing-policy vocabulary is authority-bound and canonically identified

openxFactory SHALL define a machine-readable veto-class vocabulary carrying a
policy-source reference with repository, path, immutable 40-hex commit revision,
`sha256:<64 lowercase hex>` content digest, and ratification-record reference
and digest. Source digest is over exact git blob bytes; record/content digests
use RFC 8785 JSON Canonicalization Scheme UTF-8 bytes. Each class identifier
SHALL be unique within the vocabulary and declare its allowance issuer
authority. A consuming domain SHALL resolve and hash both authoritative blobs;
self-reported source/digest presence is not proof of authority.

#### Scenario: vocabulary resolves to ratified policy

- **WHEN** a domain validates a veto-class vocabulary
- **THEN** it resolves policy and ratification blobs at the declared revision and verifies both SHA-256 digests
- **AND** every class identifier is unique and names its allowance issuer authority

#### Scenario: source cannot be proved

- **WHEN** policy or ratification bytes cannot be resolved or a digest differs
- **THEN** vocabulary use fails closed and the unresolved or stale source is named
- **AND** detector metadata is not accepted as policy authority

### Requirement: Compliance decisions are closed, bounded and redacted

openxFactory SHALL define one compliance-decision record with outcome
`allow`, `block`, or `needs_human_review`; canonical evaluated-content digest;
policy-source/vocabulary digest; current registry revision digest; resolved
approval/revocation/scope-verdict digests; evaluator identity/version; bounded
rationale codes and redacted detail; bounded opaque correlation references;
evaluation time; and every layer finding. Raw intent, provider prompt/response,
tenant content, credentials and unbounded evidence SHALL be validation failures.
Every evaluation SHALL emit a decision, including `allow`.

#### Scenario: clean intent is allowed with evidence

- **WHEN** deterministic evaluation finds no veto class and no higher layer adds a block or review finding
- **THEN** an `allow` decision is emitted with an empty allowance-reference list
- **AND** all identity, digest and bounded-evidence fields are present

#### Scenario: evidence embeds raw content

- **WHEN** a decision embeds raw intent, provider payload, tenant content or credential material
- **THEN** contract validation fails and the decision is not admissible evidence

### Requirement: Allowance approval and revocation are separate content-addressed records

openxFactory SHALL define an immutable policy-allowance approval record bound
to vocabulary identity/digest, class identifier, neutral scope reference,
cited policy approval, issuer identity/authority, approval time and validity
bounds. Its canonical approval digest SHALL identify those facts. Revocation
SHALL be a separate content-addressed event targeting the approval digest and
linking its predecessor event/revision; approval facts SHALL NOT be rewritten.

#### Scenario: allowance approval is issued

- **WHEN** declared class authority approves an allowance
- **THEN** the immutable approval record binds the exact vocabulary digest, class, scope, issuer and policy citation
- **AND** its canonical digest becomes the authority reference resolved by the registry

#### Scenario: allowance is revoked

- **WHEN** authorized policy authority revokes an allowance
- **THEN** a new revocation event targets the approval digest and links predecessor state
- **AND** mutation of the approval record is a validation failure

### Requirement: Registry resolution reads current append-only state atomically

openxFactory SHALL define a governed registry with stable registry identity,
append-only revisions linked by predecessor digest, unique allowance IDs and
atomic current-revision lookup. A claimed allowance reference SHALL contain
only `(registry_id, allowance_id)`; copied/embedded allowance payloads are
unconditionally forbidden. Decisions SHALL record the current revision digest
and resolved approval/revocation digests. Historical revision selection SHALL
NOT satisfy current-state evaluation.

#### Scenario: current allowance is resolved

- **WHEN** an evaluation claims `(registry_id, allowance_id)`
- **THEN** the evaluator atomically reads the registry's current revision and records its digest
- **AND** it resolves and records the approval and applicable revocation-event digests

#### Scenario: copied payload appears anywhere

- **WHEN** a binding or decision embeds copied allowance fields under authority, diagnostic or evidence data
- **THEN** contract validation fails regardless of the copied data's claimed purpose

### Requirement: Domain-owned scope evidence maps to neutral closed outcomes

openxFactory SHALL require allowances to bind `scope_kind`, `scope_ref`,
operations and canonical scope digest, while a domain-owned versioned resolver
emits `covers`, `does_not_cover`, or `indeterminate` evidence bound to evaluated-
content and scope digests. `covers` SHALL satisfy that class when all other
allowance checks pass; `does_not_cover` SHALL block; `indeterminate` SHALL need
human review.

#### Scenario: valid allowance covers the finding

- **WHEN** current, unrevoked, unexpired, authorized allowance scope emits `covers` for a veto finding
- **THEN** that finding is satisfied and is not itself a block or review condition
- **AND** resolver identity/version and verdict digest are recorded

#### Scenario: scope cannot be decided

- **WHEN** scope resolution is `indeterminate` or lacks digest-bound evidence
- **THEN** the outcome is `needs_human_review` and dispatch does not occur

### Requirement: Allowance resolution precedence is deterministic

openxFactory SHALL define allowance precedence per veto finding: no allowance
claim SHALL `block`; a claimed but unreadable, absent, duplicate or ambiguous
reference SHALL produce `needs_human_review`; a resolved revoked, expired,
unauthorized or non-covering allowance SHALL `block`; and a current authorized
covering allowance SHALL satisfy the finding. Final `allow` SHALL require every
finding satisfied and no remaining block or review condition.

#### Scenario: veto class has no allowance claim

- **WHEN** an evaluator finds a veto class and no allowance is claimed for it
- **THEN** the compliance outcome is `block`
- **AND** approved intent is not treated as policy authorization

#### Scenario: claimed allowance is unresolvable

- **WHEN** an allowance ID is claimed but cannot be uniquely resolved from current registry state
- **THEN** the outcome is `needs_human_review` and work does not proceed

#### Scenario: all veto findings have current covering allowances

- **WHEN** every veto finding resolves to a current authorized in-scope allowance and no other layer adds a finding
- **THEN** the final compliance outcome is `allow`

### Requirement: Binding approval requires current compliance allow

openxFactory SHALL prohibit a governed binding from reaching
`status: approved` until it carries a current compliance decision of `allow`
bound to the identical canonical content digest, policy/vocabulary digest and
current registry revision. `block`, `needs_human_review`, missing evidence or
digest mismatch SHALL keep the binding blocked or in review.

#### Scenario: approval has no compliance decision

- **WHEN** a binding requests `status: approved` without a current digest-bound compliance decision
- **THEN** approval is refused before worker dispatch

#### Scenario: approved content changed

- **WHEN** binding content differs from the content digest in its `allow` decision
- **THEN** approval is invalidated and compliance re-evaluation is required

### Requirement: Dispatch keeps a permanent deterministic floor and closed composition

openxFactory SHALL require deterministic compliance immediately before worker
invocation regardless of prior approval, classifier use or live Hermes review.
All deterministic, classifier and Hermes findings SHALL compose into one
decision under precedence `block > needs_human_review > allow`; no higher layer
may erase a deterministic block. Evaluation failure SHALL stop dispatch.

#### Scenario: deterministic floor finds a veto class

- **WHEN** pre-dispatch evaluation finds an uncovered veto class
- **THEN** worker invocation does not occur and the composed decision is `block`

#### Scenario: Hermes requests review after deterministic allow

- **WHEN** deterministic evaluation allows but Hermes adds a review finding
- **THEN** the composed decision is `needs_human_review` and all layer findings are retained

### Requirement: Classifier escalation has closed triggers, hard caps and fail-closed results

openxFactory SHALL permit classifier escalation only for trigger
`deterministic_ambiguity` or `policy_sensitive_surface`; a sensitive-surface
trigger SHALL reference and digest current vocabulary detection metadata.
Decision evidence SHALL record trigger kind/reference/digest, model/version,
one-invocation/one-turn limits, maximum 65,536 input bytes, 8,192 output bytes,
4,096 output tokens and 60 seconds, actual consumption, closed result and
result digest. Missing/invalid trigger, blanket undeclared sensitivity, absent
limits, breach, timeout or invocation failure SHALL produce
`needs_human_review`; a positive classifier finding SHALL also produce
`needs_human_review` and SHALL NOT authorize an allowance.

#### Scenario: declared ambiguity escalates once

- **WHEN** deterministic evaluation records ambiguity under a valid trigger
- **THEN** one bounded classifier invocation may run and its bounded evidence joins the decision

#### Scenario: classifier reports a veto signal

- **WHEN** bounded classification reports a possible veto class
- **THEN** the composed outcome is at least `needs_human_review` and dispatch does not occur

#### Scenario: classifier limit or invocation fails

- **WHEN** any classifier cap is absent/exceeded or invocation fails/times out
- **THEN** the outcome is `needs_human_review` with bounded failure evidence and no dispatch

### Requirement: Enforcement points bind to identical policy and current authority state

openxFactory SHALL require intent approval, pre-dispatch evaluation and post-
build admission to bind decisions to identical canonical content digest,
policy-source/vocabulary digest and registry identity, while each later point
atomically reads current registry revision and records resolved approval,
revocation and scope-verdict digests. Stale revision selection, digest mismatch
or newly revoked authority SHALL NOT authorize the later point.

#### Scenario: registry changes after dispatch

- **WHEN** admission observes a registry revision newer than dispatch
- **THEN** it evaluates current state and records the new revision/resolution digests
- **AND** a newly effective revocation blocks admission

#### Scenario: enforcement points use different policy vocabulary

- **WHEN** dispatch policy/vocabulary digest differs from the approved decision
- **THEN** dispatch fails closed and requires re-evaluation under the current authority
