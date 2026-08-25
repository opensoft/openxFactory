# intent-compliance Specification (delta)

## ADDED Requirements

### Requirement: Standing-policy vocabulary is machine-readable and authority-bound

openxFactory SHALL define a machine-readable veto-class vocabulary record that
names its ratified policy source, records the source digest, gives every class
a stable identifier and declares the authority allowed to issue allowances for
that class. The record MAY carry domain-owned detection metadata, but the
schema SHALL NOT prescribe one universal class list or treat detection signals
as policy authority.

#### Scenario: vocabulary matches its ratified source

- **WHEN** a veto-class vocabulary record is validated
- **THEN** its declared policy source and digest resolve to the ratified authority it claims
- **AND** every class has a stable identifier and declared allowance issuer authority

#### Scenario: vocabulary drifts from policy

- **WHEN** the declared policy source no longer matches the recorded digest
- **THEN** release or use of that vocabulary fails closed with the drift named
- **AND** detector metadata is not accepted as a replacement policy source

### Requirement: Compliance evaluation emits a closed decision record

openxFactory SHALL define a compliance-decision record with a closed outcome
of `allow`, `block`, or `needs_human_review`, plus the evaluated-content digest,
evaluator identity/version, class findings, rationale, policy source,
allowance-reference resolution facts, correlation identifiers and evaluation
time. Every evaluation SHALL emit the record, including `allow` outcomes.

#### Scenario: compliant intent is allowed with evidence

- **WHEN** an evaluator finds no veto class in an evaluated intent
- **THEN** it emits an `allow` decision bound to the evaluated-content digest
- **AND** the record carries the evaluator version and correlation identifiers

#### Scenario: veto class has no allowance

- **WHEN** an evaluator finds a veto class and no allowance reference covers it
- **THEN** it emits `block` with the class, policy source and rationale named
- **AND** approved intent is not treated as policy authorization

### Requirement: Policy allowances are first-class revocable records

openxFactory SHALL define a policy-allowance record with a stable identifier,
covered veto class and scope, cited policy approval, issuer identity and
authority, approval time, validity bounds and additive revocation state.
Approval facts SHALL be immutable; revocation SHALL append who revoked, when
and why without rewriting the original approval.

#### Scenario: authorized issuer creates an allowance

- **WHEN** an allowance is issued by the declared authority for its class
- **THEN** the record carries a stable identifier, scope, cited approval and approval time
- **AND** it contains no secret, credential or copied provider token

#### Scenario: allowance is revoked

- **WHEN** authorized policy authority revokes an allowance
- **THEN** revocation identity, time and reason are appended to the record
- **AND** the original approval facts remain unchanged

### Requirement: Allowance registry resolves by identifier and never by copied payload

openxFactory SHALL define a governed policy-allowance registry with unique
allowance identifiers, registry identity/version and deterministic lookup.
Bindings and decision records SHALL reference allowance identifiers and SHALL
NOT embed copied allowance payloads as authority evidence.

#### Scenario: binding references a registry allowance

- **WHEN** a binding claims an exception to a veto class
- **THEN** it carries the allowance identifier resolved from the governed registry
- **AND** an embedded allowance object is a contract-validation failure

#### Scenario: duplicate identifiers enter the registry

- **WHEN** two registry records carry the same allowance identifier
- **THEN** the registry is invalid and all resolution from the ambiguous identifier fails closed

### Requirement: Missing and revoked allowances fail closed differently

openxFactory SHALL require every evaluation point to resolve allowance
references against current registry state. An unreadable, absent or ambiguous
reference SHALL produce `needs_human_review`; a resolved allowance that is
revoked, expired, out of scope or issued by unauthorized authority SHALL
produce `block`.

#### Scenario: registry reference cannot be resolved

- **WHEN** an evaluator cannot read or uniquely resolve a claimed allowance identifier
- **THEN** it emits `needs_human_review` and does not dispatch or admit work
- **AND** cached or binding-embedded allowance data is not substituted

#### Scenario: allowance was revoked after approval

- **WHEN** a binding was previously allowed but its referenced allowance is now revoked
- **THEN** the next evaluation emits `block`
- **AND** the earlier `allow` decision does not authorize later dispatch or admission

### Requirement: Dispatch keeps a permanent deterministic compliance floor

openxFactory SHALL require a dispatch pathway consuming governed intent to run
a deterministic compliance evaluation immediately before worker invocation,
regardless of prior approval, prior evidence, classifier use or live Hermes
review. Evaluation failure SHALL fail closed before worker tokens are spent.

#### Scenario: deterministic floor catches a veto class

- **WHEN** the pre-dispatch evaluator detects a veto class without a current valid allowance
- **THEN** worker invocation does not occur and a `block` decision is recorded
- **AND** higher-order reviewer availability does not suppress the refusal

#### Scenario: Hermes intake is live

- **WHEN** a consuming system adds live Hermes intake review
- **THEN** the deterministic pre-dispatch evaluation remains mandatory beneath it
- **AND** Hermes judgment may add findings but cannot erase a deterministic block

### Requirement: Bounded classification only escalates deterministic evaluation

openxFactory SHALL permit a consuming domain to invoke one bounded classifier
only after deterministic evaluation marks ambiguity or a declared sensitive
surface. Classifier cost/turn limits and version SHALL be recorded, and its
output SHALL NOT erase a deterministic class finding or authorize an
allowance.

#### Scenario: ambiguous intent escalates

- **WHEN** deterministic evaluation marks an intent ambiguous under declared rules
- **THEN** one bounded classifier evaluation may run under recorded limits
- **AND** its output is joined into the compliance-decision evidence

#### Scenario: classifier disagrees with a deterministic finding

- **WHEN** a classifier reports no veto class but deterministic evaluation found one
- **THEN** the deterministic finding remains controlling
- **AND** the disagreement is recorded rather than silently normalized

### Requirement: All enforcement points verify the same intent and allowance state

openxFactory SHALL require intent approval, pre-dispatch evaluation and
post-build admission to bind decisions to the evaluated-content digest and to
resolve the same allowance identifiers against current registry state. A
decision for a different digest or stale allowance state SHALL NOT authorize
the next enforcement point.

#### Scenario: content changes after approval

- **WHEN** pre-dispatch content digest differs from the digest approved by the intent gate
- **THEN** dispatch fails closed and names the digest mismatch
- **AND** re-evaluation is required before work can proceed

#### Scenario: admission sees a newly revoked allowance

- **WHEN** dispatch used a valid allowance but admission resolves it as revoked
- **THEN** admission blocks the candidate
- **AND** dispatch-time evidence remains an audit record, not continuing authority
