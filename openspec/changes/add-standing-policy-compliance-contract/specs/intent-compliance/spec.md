# intent-compliance Specification (delta)

## ADDED Requirements

### Requirement: Standing-policy vocabulary is machine-readable and authority-bound

openxFactory SHALL define a machine-readable veto-class vocabulary record that
names its ratified policy source, records the source digest, gives every class
a stable identifier unique within that vocabulary and declares the authority
allowed to issue allowances for that class. The record MAY carry domain-owned
detection metadata, but the
schema SHALL NOT prescribe one universal class list or treat detection signals
as policy authority.

#### Scenario: vocabulary matches its ratified source

- **WHEN** a veto-class vocabulary record is validated
- **THEN** its declared policy source and digest resolve to the ratified authority it claims
- **AND** every class has a stable identifier and declared allowance issuer authority

#### Scenario: vocabulary repeats a class identifier

- **WHEN** two entries in one veto-class vocabulary carry the same class identifier
- **THEN** the vocabulary is invalid and no compliance decision may use it

#### Scenario: vocabulary drifts from policy

- **WHEN** the declared policy source no longer matches the recorded digest
- **THEN** release or use of that vocabulary fails closed with the drift named
- **AND** detector metadata is not accepted as a replacement policy source

### Requirement: Compliance evaluation emits a closed decision record

openxFactory SHALL define a compliance-decision record with a closed outcome
of `allow`, `block`, or `needs_human_review`, plus the evaluated-content digest,
evaluator identity/version, class findings, rationale, policy source,
allowance-reference resolution facts, correlation identifiers and evaluation
time. Evidence fields SHALL be bounded and redacted: rationale uses bounded
codes/redacted detail, correlation identifiers are bounded opaque references,
and raw intent, provider prompt/response, tenant content and credentials SHALL
NOT be persisted. Every evaluation SHALL emit the record, including `allow`
outcomes.

#### Scenario: compliant intent is allowed with evidence

- **WHEN** an evaluator finds no veto class in an evaluated intent
- **THEN** it emits an `allow` decision bound to the evaluated-content digest
- **AND** the record carries the evaluator version and correlation identifiers

#### Scenario: decision contains raw evidence content

- **WHEN** a decision embeds raw intent, provider payload, tenant content or credential material
- **THEN** contract validation fails and the decision is not admissible evidence

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
allowance identifiers, registry identity/version, a monotonically identified
revision and deterministic lookup. Bindings and decision records SHALL carry a
registry-qualified reference `(registry_id, registry_version, allowance_id)`
and SHALL NOT embed copied allowance payloads as authority evidence.

#### Scenario: binding references a registry allowance

- **WHEN** a binding claims an exception to a veto class
- **THEN** it carries registry identity/version and the allowance identifier resolved from that registry
- **AND** an embedded allowance object is a contract-validation failure

#### Scenario: duplicate identifiers enter the registry

- **WHEN** two registry records carry the same allowance identifier
- **THEN** the registry is invalid and all resolution from the ambiguous identifier fails closed

### Requirement: Allowance scope is resolved by domain evidence under neutral outcomes

openxFactory SHALL require an allowance to bind a neutral scope reference
(`scope_kind`, `scope_ref`, operations and scope digest) and SHALL require the
consuming domain's versioned resolver to emit `covers`, `does_not_cover`, or
`indeterminate` evidence bound to the evaluated-content and scope digests. The
neutral outcome mapping SHALL be fixed: `covers` may satisfy the class,
`does_not_cover` blocks, and `indeterminate` needs human review.

#### Scenario: allowance scope covers the evaluated intent

- **WHEN** the domain scope resolver emits `covers` for the evaluated-content and allowance-scope digests
- **THEN** that allowance may satisfy its class if all other validity checks pass
- **AND** resolver identity/version and verdict are recorded in the decision

#### Scenario: scope resolver cannot decide

- **WHEN** the domain scope resolver emits `indeterminate` or cannot produce digest-bound evidence
- **THEN** the compliance outcome is `needs_human_review` and dispatch does not occur

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

openxFactory SHALL permit a consuming domain to invoke a classifier only after
deterministic evaluation marks ambiguity or a declared sensitive surface, with
exactly one invocation and one turn, no more than 65,536 input bytes, 8,192
output bytes, 4,096 output tokens and 60 seconds. Limits and classifier version
SHALL be recorded; missing limits, limit breach, timeout or invocation failure
SHALL produce `needs_human_review` and no dispatch. Classifier output SHALL NOT
erase a deterministic class finding or authorize an allowance.

#### Scenario: ambiguous intent escalates

- **WHEN** deterministic evaluation marks an intent ambiguous under declared rules
- **THEN** one bounded classifier evaluation may run under recorded limits
- **AND** its output is joined into the compliance-decision evidence

#### Scenario: classifier fails or exceeds a hard limit

- **WHEN** classifier invocation times out, fails, lacks its limit envelope or exceeds any hard cap
- **THEN** the outcome is `needs_human_review` and worker dispatch does not occur
- **AND** failure evidence is bounded and excludes raw provider payloads

#### Scenario: classifier disagrees with a deterministic finding

- **WHEN** a classifier reports no veto class but deterministic evaluation found one
- **THEN** the deterministic finding remains controlling
- **AND** the disagreement is recorded rather than silently normalized

### Requirement: All enforcement points verify the same intent and allowance state

openxFactory SHALL require intent approval, pre-dispatch evaluation and
post-build admission to bind decisions to the evaluated-content digest, veto-
class vocabulary/policy-source digest, registry identity/revision, resolved
allowance-record digests and domain scope-verdict evidence. A decision with a
different digest, registry revision, allowance digest or scope verdict SHALL
NOT authorize the next enforcement point.

#### Scenario: content changes after approval

- **WHEN** pre-dispatch content digest differs from the digest approved by the intent gate
- **THEN** dispatch fails closed and names the digest mismatch
- **AND** re-evaluation is required before work can proceed

#### Scenario: admission sees a newly revoked allowance

- **WHEN** dispatch used a valid allowance but admission resolves it as revoked
- **THEN** admission blocks the candidate
- **AND** dispatch-time evidence remains an audit record, not continuing authority
