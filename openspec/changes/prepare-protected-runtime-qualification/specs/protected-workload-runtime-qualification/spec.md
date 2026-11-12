## ADDED Requirements

### Requirement: Trusted bounded issuer acquisition

The opt-in runtime composition SHALL acquire verification keys only from trusted
configured HTTPS issuer locations with bounded time, response size, key count,
freshness and refresh attempts. It MUST preserve the source-accepted RS256,
claim, timestamp and snapshot-deadline rules. Offline gates MUST remain offline.

#### Scenario: Approved issuer snapshot supports existing verification
- **WHEN** an approved issuer response yields one valid selected public key within all administrative deadlines
- **THEN** the existing verifier checks the signature and exact expected claims with no added clock leeway

#### Scenario: Token or response attempts to expand trust
- **WHEN** a token names a key URL, or discovery/redirect/data changes the approved endpoint or creates ambiguous keys
- **THEN** verification refuses without contacting an unapproved location or invoking custody

#### Scenario: Unknown key requires bounded refresh
- **WHEN** a bounded key identifier is absent from the current fresh snapshot
- **THEN** at most one permitted refresh and one verification retry occur; throttling, unavailability or continued absence refuses

#### Scenario: Stale trust cannot be extended by outage
- **WHEN** the snapshot deadline expires or mandatory refresh fails
- **THEN** the runtime refuses rather than extending old keys or merging removed keys back into replacement trust

### Requirement: Operator-owned protected launch composition

The runtime SHALL obtain expected source, workflow, authority, challenge, state,
supervisor and custody bindings only from trusted operator configuration. It
MUST verify the existing exact signed claim set and independently corroborate
protected environment configuration. A worker MUST NOT select trusted loaders,
verification keys, measurement policy, credentials or expected claim values.

#### Scenario: Exact launch supplies bounded machine proof input
- **WHEN** the real workload matches every approved caller and reusable workflow, immutable identity, environment, subject, source and run/attempt binding
- **THEN** the existing proof gate can continue under its current authority and one-use checks

#### Scenario: Changed launch or worker-selected dependency refuses
- **WHEN** a required signed claim or trusted dependency differs, is missing, or is selected by the worker
- **THEN** the runtime refuses before proof production

### Requirement: Independently administered supervisor and confined custody

A live machine qualification SHALL demonstrate a supervisor and gate/custody
control plane outside worker administrative access. It MUST bind actual measured
launch source/configuration and key identity using the existing observation.
Only the approved gate deployment may exercise the owning signer after per-use
checks. No new neutral custody protocol or human approval semantics are granted.

#### Scenario: Worker cannot sign a valid canonical request directly
- **WHEN** the worker attempts direct custody signing with an otherwise valid preimage
- **THEN** access is denied while the selected trusted gate can produce the bounded proof through the owning API

#### Scenario: Containers or peer allowlists cannot self-attest independence
- **WHEN** evidence consists only of separate keys, same-user containers or an mTLS peer/subject allowlist
- **THEN** deployed independence and workload-bound custody acceptance remain blocked

#### Scenario: Unsupported custody trust model is explicit
- **WHEN** acceptance requires custody to validate a new per-use assertion not supported by the owning API
- **THEN** qualification refuses and requires a neutral-owner decision rather than an adapter-owned protocol fork

### Requirement: Protected replay state and attributable lifecycle

The runtime SHALL require the selected initialized private replay state and retain
existing durable reservation-before-signing and consumed-on-failure behavior.
It MUST refuse observable missing/corrupt state and produce case-bound independent
cleanup readback for success, failure and cancellation. Hostile-host or valid
backup rollback resistance MUST NOT be inferred from the existing ledger.

#### Scenario: Restart preserves consumed authority
- **WHEN** the same token or challenge is retried concurrently or after restart
- **THEN** no second proof-producing custody use is admitted, including after an ambiguous failure

#### Scenario: Missing state or cleanup cannot yield qualification
- **WHEN** expected state is absent/corrupt or fresh independent run-owned absence readback is missing
- **THEN** runtime startup or qualification refuses; no shared resource is deleted to manufacture success

### Requirement: Machine-only acceptance remains separate

The preparation and runtime SHALL separate source conformance, isolated fixtures,
protected machine evidence and attended human/domain acceptance. New-profile owner
acceptance and implementation commissioning MUST precede runtime implementation;
actual protected setup/dispatch MUST require separate operational authorization.
No consumer runtime lock may be published without its owned validation/protection
contract. Missing live inputs MUST be blocked or not-performed.

#### Scenario: Isolated success does not clear live gates
- **WHEN** synthetic issuer or same-user reference-process tests pass
- **THEN** those results establish only their isolated scope and cannot clear live issuer, supervisor, custody or human acceptance

#### Scenario: Successful machine receipt does not complete the domain pilot
- **WHEN** an authorized protected machine qualification passes
- **THEN** its receipt supplies only the corresponding upstream handoff; the consumer dependency gate remains incomplete until every independent human/runtime requirement is accepted
