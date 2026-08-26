# client-infrastructure-request Specification

## Purpose
TBD - created by archiving change add-client-infrastructure-liaison. Update Purpose after archive.
## Requirements
### Requirement: Durable request record
A `client_infrastructure_request` SHALL be a durable coordination record, distinct from the neutral job envelope (it may authorize and correlate to zero or more bounded jobs, and MUST NOT be one). It SHALL carry six distinct identity-reference classes — `organization_ref`, `subject_ref`, `actor_ref`, `authority_ref`, `capability_ref`, `credential_grant_ref` — never conflated, with subject identifiers forbidden in actor, capability, and authority fields; an `idempotency_key` and `correlation_id`; `managed_subject_refs`; a requirements profile and validation profile (id + version); an `execution_binding` (`mode` ∈ `client_managed | managed_host | opsxfactory_executed`, with organization/actor/capability refs and, where privileged, a grant ref); approval and communication blocks; package references carried only as immutable digests from approved publishers; and evidence references. Secret values are forbidden everywhere in the record — references only.

#### Scenario: Duplicate submission with the same idempotency key
- **WHEN** a request is submitted whose `idempotency_key` matches an existing open request
- **THEN** the existing request is returned and no second record is created

#### Scenario: Subject identifier in an authority field
- **WHEN** any actor, capability, or authority field carries a subject identifier
- **THEN** deterministic validation MUST fail the record

#### Scenario: Package reference without an immutable digest
- **WHEN** a `package_refs` entry lacks a digest or names an unapproved publisher
- **THEN** the request MUST NOT pass approval

### Requirement: Lifecycle and transition legality
Request status SHALL be a closed lifecycle — `identified → request_drafted → awaiting_client_approval → submitted → acknowledged → scheduled → implementing → validation_pending → completed`, with exceptional states `blocked`, `declined`, `validation_failed`, `cancelled` — where every transition is legal only for its authorized actor class under its guard (drafting and submission by the liaison owner; approval and decline by the approval authority; acknowledgment through implementation by the execution actor; completion and failure verdicts by the trusted validator; blocking by the current owner or policy gate; cancellation by the requester with required approval). `declined`, `cancelled`, and `completed` are terminal; reopening completed work — or a material scope change (changed target, requirements profile, or security boundary) on an open request — SHALL be a new request carrying `supersedes_request_ref`, never a mutation of the predecessor. Deadline and escalation SHALL be expressed as orthogonal conditions (`overdue`, `escalated`, `maintenance_hold`, `awaiting_external_response`), never as states, each recording type, active, observed_at, policy_ref, and clearing evidence; an active `overdue` condition SHALL escalate along the request's configured escalation path, recorded as condition evidence.

#### Scenario: Unauthorized actor drives a transition
- **WHEN** an actor class other than the matrix's authorized class attempts a transition (e.g. the liaison marks `completed`)
- **THEN** the transition MUST be rejected as illegal

#### Scenario: Terminal state is mutated
- **WHEN** any transition is attempted out of `declined`, `cancelled`, or `completed`
- **THEN** it MUST be rejected, and the only continuation is a new request with `supersedes_request_ref` naming the terminal predecessor

#### Scenario: Escalation modeled as a state
- **WHEN** a record expresses overdue or escalation as a `status` value rather than a condition entry
- **THEN** validation MUST fail the record

#### Scenario: Overdue request follows the escalation path
- **WHEN** a request's `overdue` condition activates under its policy
- **THEN** escalation proceeds along the configured escalation path in order, each step recorded as condition evidence, while the request's `status` is unchanged by the escalation itself

#### Scenario: Material scope change on an open request
- **WHEN** an open request's target, requirements profile, or security boundary materially changes
- **THEN** a superseding request is created carrying `supersedes_request_ref`, and the predecessor MUST NOT be silently rewritten

### Requirement: Handoff correlation
A request bound to an external execution system SHALL keep the neutral request and the execution system's own record as separate records with separate owners: Client Hermes remains the source of truth for outcome and client communication; the execution system becomes the source of truth for privileged execution only after it returns an accepted work-item reference. The acceptance SHALL be recorded in a `handoff` block (infrastructure_request_ref, correlation_id, receiving_system, external work-item ref, accepted_by_actor_ref, projected_status), projection MUST NOT overwrite the execution system's internal state, and loss of connection to the execution system SHALL move the request to `blocked` or an awaiting condition — never toward success. Cancellation and material scope changes SHALL propagate to every active child job and external work item, recording each system's acknowledgment of whether work stopped, partially applied, or completed — history is never rewritten.

#### Scenario: OpsxFactory accepts a handoff
- **WHEN** an `opsxfactory_executed` request is acknowledged
- **THEN** the handoff block records the OpsxFactory service-request reference and accepting actor, and both records stay separately owned and correlated by `correlation_id`

#### Scenario: Execution system becomes unreachable
- **WHEN** the connection to the executing system is lost mid-request
- **THEN** the request becomes `blocked` (or an awaiting condition activates) and MUST NOT progress toward `completed`

#### Scenario: Cancellation propagates to active children
- **WHEN** a request is cancelled after external execution has begun
- **THEN** the cancellation propagates to the external work item and every active child job, each acknowledgment (stopped / partially applied / completed) is recorded, and the final record states the true outcome without rewriting history

### Requirement: Readiness-gated completion
The transition to `completed` SHALL require a fresh passing `infrastructure_readiness_result` — a signed, traceable artifact (never a bare boolean) with status ∈ `ready | degraded | not_ready | unknown | maintenance`, produced by a trusted validator named in the request's validation profile, used only before its `valid_until`, with every mandatory check passing. Validation SHALL be non-privileged: the validator cannot change the target and holds at most granted read-only access. Submission, acknowledgment, or an execution actor's claim of completion SHALL NOT count as readiness evidence.

#### Scenario: Completion claimed without fresh readiness
- **WHEN** `validation_pending → completed` is attempted with no readiness result, a stale one (past `valid_until`), or one whose status is not `ready`
- **THEN** the transition MUST be rejected

#### Scenario: Execution owner reports done but validation fails
- **WHEN** the execution actor claims the outcome but a mandatory readiness check fails
- **THEN** the request moves to `validation_failed` with the failed checks returned to the execution owner, and a new passing result is required after remediation

### Requirement: Deterministic validation
The contract family SHALL ship an openxFactory-owned validator (`scripts/validate-client-infrastructure.py`, invoked from the pinned checkout, never copied into domain repos) that schema-validates both kinds and deterministically enforces what schema cannot: embedded-secret rejection, transition legality (including terminal immutability and readiness-gated completion), actor/authority separation (`execution_binding` actor never equal to the approval authority), and idempotency/supersedes integrity — with packaged valid examples and one-violation-each negative examples self-tested on every run.

#### Scenario: Validator self-test degrades
- **WHEN** any packaged negative example stops failing for its intended reason (or a valid example fails)
- **THEN** the validator MUST exit non-zero, failing closed

#### Scenario: Execution actor equals approval authority
- **WHEN** a request's `execution_binding.actor_ref` resolves to the same identity as `approval.authority_ref`
- **THEN** validation MUST fail the record

