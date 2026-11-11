## Purpose

Bind an authenticated reference workload to current bounded factory authority before producing a wallet possession proof, without conferring human approval.

## ADDED Requirements

### Requirement: Current bounded factory authority

The candidate adapter SHALL bind an authenticated workload to operator-selected
current agent, wallet/key/custody and bounded existing grant records at exercise.
It SHALL refuse inactive ancestors, unresolved/cyclic chains, widened scope or
lifetime, unsupported authority and mismatched audience. It SHALL refuse
review-class chains until canonical factory anchor/register checks are composed.
It SHALL NOT derive human approval from workload authentication.

#### Scenario: Current permitted request

- **WHEN** the exact approved workload requests an allowed act/object with a
  current matching wallet binding and bounded active ancestor chain
- **THEN** the gate identifies that agent and chain before signing

#### Scenario: Revoked parent or widened child

- **WHEN** any ancestor is revoked/expired or a child widens authority
- **THEN** the gate refuses without invoking custody

### Requirement: Independently bound workload evidence

The gate SHALL verify exact workload issuer/signature/audience, immutable repository
identity, environment, caller/reusable workflow source and run/attempt, plus a
separate signed observation bound to its trusted challenge, request, token, policy
and composition. The observer SHALL read its own selected reference artifacts.

#### Scenario: Changed evidence

- **WHEN** token, source, run, key, request, observation or measured composition differs
- **THEN** the gate refuses before signing

### Requirement: Durable one-use proof gate

The gate SHALL reserve token and challenge identities durably before invoking the
owning wallet proof API, recheck current authority before returning and retain
reservations after ambiguous failures. It SHALL perform full replay-store
integrity validation at startup and check the exact initialized schema and
uniqueness constraints transactionally at each reservation. Malformed existing
state SHALL refuse without automatic reset. Storage SHALL be protected on a
trusted host; adversarial live byte changes, deletion and valid-backup rollback
are outside this candidate guarantee. It SHALL check a fresh clock against all
evidence deadlines after blocking work and before signing/return.

#### Scenario: Restart or concurrent replay

- **WHEN** a reserved token or challenge is retried after restart or concurrently
- **THEN** no second custody signing call occurs

### Requirement: Honest isolated qualification

Candidate source SHALL be qualified with synthetic identities and disposable
reference processes, including signer bypass, refusal and cleanup evidence.
Source tests SHALL NOT be presented as ratification, live issuer assurance,
human consent, deployed isolation or pilot acceptance.

#### Scenario: Isolated qualification completes

- **WHEN** positive and injected-failure tests finish
- **THEN** owned fixture processes exit and temporary keys are removed while live
  qualification and owner acceptance remain explicitly unperformed
