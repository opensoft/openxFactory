## Purpose

Propose purpose-separated actual GitHub bootstrap identity and independently
correlated readiness without promoting fixture evidence into operational authority.

## ADDED Requirements

### Requirement: Explicit opt-in admission identity policy

The new profile SHALL permit bootstrap-purpose identity before environment approval
only after explicit owner acceptance of that policy amendment and source commissioning.
Existing fixture/default behavior MUST remain unchanged and refuse while unselected.
Proposal preparation MUST NOT mint tokens, edit permissions, provision or dispatch.

#### Scenario: Proposal exists without activation
- **WHEN** this proposal is prepared or reviewed without later source and operational decisions
- **THEN** no current workflow, credential, operational binding or authorization changes

#### Scenario: Strict no-preflight-OIDC remains selected
- **WHEN** the owner does not accept the proposed admission identity amendment
- **THEN** the new profile remains disabled and an independently reviewed alternative is required

### Requirement: Authenticated purpose-separated readiness client

Bootstrap readiness SHALL require verified GitHub issuer/signature, trusted distinct
audience, exact selected source/workflow/repository/owner/run/attempt and current
time/phase/subject policy. Audience or public metadata alone MUST NOT confer a role.
Tokens/request credentials MUST remain outside worker access and retained evidence.

#### Scenario: Actual approved admission identity corroborates readiness
- **WHEN** a current signature-valid GitHub identity matches every independently approved and corroborated binding
- **THEN** only the selected readiness/operation-read capability for that case and run may proceed

#### Scenario: Valid signature with changed purpose or context refuses
- **WHEN** a token has a wrong audience, phase, subject, source, caller, reusable workflow, repository, event, run or attempt
- **THEN** readiness refuses before output or any proof-producing dependency

#### Scenario: Worker can obtain control identity
- **WHEN** a worker can read the orchestration token or request an eligible control token
- **THEN** the deployed client boundary is ineligible rather than accepted by different principal labels

### Requirement: Protected proof policy remains mandatory

Bootstrap identity SHALL NOT satisfy protected machine proof identity, environment
approval, policy/challenge, signer/custody, replay, human or domain approval.
The existing proof verifier MUST retain every required protected claim and audience.

#### Scenario: Protected-phase bootstrap audience is independently refused
- **WHEN** a signature-valid protected-phase token has every proof claim otherwise matching but only its audience is changed to bootstrap
- **THEN** proof verification refuses for purpose separation before custody, with an otherwise identical proof-audience token as a successful control

#### Scenario: Proof audience cannot replace the protected environment
- **WHEN** a signature-valid token keeps the proof audience and every other proof claim but lacks only the protected environment
- **THEN** proof verification independently refuses the missing environment before custody; a provider-shaped unprotected admission token requested with proof audience must also refuse

#### Scenario: Environment is approved
- **WHEN** a protected job is released
- **THEN** readiness is repeated with the selected protected identity class and fresh actual approval/protection/grant/lease readback

### Requirement: Durable at-most-one dispatch attempt

A separately authorized broker SHALL durably consume the approved dispatch attempt
before external I/O, allow at most one request attempt and preserve consumption
across concurrency, restart, crash and ambiguity. It MUST NOT claim exactly-once
provider execution or retry/reset consumed scope automatically. It MUST revalidate
current approval, exact scope, revocation and trusted window before reservation
and after blocking work immediately before transmission; expired/revoked scope
must not send even if already reserved.

#### Scenario: Concurrent brokers or crash before I/O
- **WHEN** callers compete for the same scope or the reservation winner crashes before sending
- **THEN** only the durable winner may attempt one request and restart does not release or retry the consumed attempt

#### Scenario: Reserved winner expires or is revoked before send
- **WHEN** a reservation winner stalls or blocking work outlasts its window, or authority is revoked before transmission
- **THEN** it sends zero dispatch requests, preserves consumed scope and does not retry/reset

#### Scenario: Response is lost or insufficient
- **WHEN** a dispatch outcome is ambiguous or lacks the required provider-returned run identity
- **THEN** the scope stays indeterminate for separately authorized reconciliation with no newest-run or worker-output fallback

### Requirement: Independent actual-run corroboration

Readiness SHALL require agreement between independently approved static scope,
authenticated broker correlation, signed client identity and current selected
provider run/attempt/source facts. Worker values or a successful API response MUST
NOT approve themselves. Missing or ambiguous required provenance MUST refuse.

#### Scenario: Returned run and signed identity disagree
- **WHEN** any approved case, repository, workflow, actor, source, ref, run or attempt binding disagrees or is unavailable
- **THEN** no actual-run full configuration/operation readiness is issued

#### Scenario: Main moves during dispatch
- **WHEN** the actual dispatched source differs from the approved source
- **THEN** wallet authority and qualification refuse; no automatic redispatch or atomic-prevention claim follows

### Requirement: Originating operator and review separation

The broker SHALL preserve the initiating human identity separately from its App
actor. Protected readiness MUST independently verify eligible approval excludes
the initiating operator; GitHub App actor separation alone MUST NOT establish this.
Environment approval MUST NOT be reported as domain human consent.

#### Scenario: Initiator reviews an App-dispatched run
- **WHEN** provider review identifies the initiating human as approver despite a distinct App run actor
- **THEN** independent-review acceptance refuses

### Requirement: Bounded fresh authority and retained evidence

Every bootstrap use SHALL enforce approved transport/data/freshness/concurrency
bounds, current revocation and the earliest applicable deadline. Missing state,
authentication, source/approval/lease readback or required selection MUST fail closed.
Logs and receipts MUST omit tokens, request credentials and raw provider payloads.
Consumed authority, shared resources and replay reservations MUST be preserved.

#### Scenario: Outage or expiry during readiness
- **WHEN** a required observation expires, state is lost, or authentication/readback fails
- **THEN** no stale or cached approval extends readiness and the result contains only a fixed safe refusal

#### Scenario: Runner dies after a bounded proof
- **WHEN** independently authorized qualification loses its runner
- **THEN** independent cleanup/readback remains required and source/fixture evidence alone cannot clear live acceptance

### Requirement: Operational and source acceptance remain separate

Implementation SHALL require explicit owner acceptance/source commissioning.
Actual target, subjects, credential/admin boundaries, source-update exposure policy,
setup, dispatch and live qualification SHALL remain separately approved gates.
No neutral profile, consumer execution lock, human or domain acceptance is granted.

#### Scenario: Source checks pass
- **WHEN** source and isolated tests pass for a future implementation
- **THEN** operational selections, deployed isolation, actual token corroboration and setup/dispatch authority remain ungranted until separately accepted
