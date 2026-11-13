## ADDED Requirements

### Requirement: Static selection precedes run-bound authority

The composition SHALL commit every runtime selection except launch run ID and
attempt using a distinct closed canonical selection profile. It MUST retain
the original full runtime digest and exact run/attempt validation.

#### Scenario: No predicted run identity
- **WHEN** selection is prepared before GitHub assigns a run
- **THEN** its digest excludes only run ID/attempt and independent bootstrap later binds the final full digest to the actual run

#### Scenario: Configuration substitution refuses
- **WHEN** any static field changes, unknown fields appear or runtime run fields are absent
- **THEN** selection validation or runtime admission refuses before environment outputs or OIDC

### Requirement: Independent bounded bootstrap

The trusted host SHALL obtain fresh authenticated bootstrap readback binding
approved selection, preauthorization, source, repository, case, actual run/attempt,
full independently approved config and operation grant. The authority MUST
atomically refuse reuse for another run/attempt. Worker hashes/outputs or boolean
approval MUST NOT supply independent authority.

#### Scenario: Independent actual-run binding
- **WHEN** bootstrap and existing admission agree on every selected binding
- **THEN** readiness respects the earliest bootstrap/config/protection/grant/lease deadline

#### Scenario: Replay or stale authority
- **WHEN** run/attempt, source, principal, case, digest, grant or freshness differs or the reader fails
- **THEN** readiness refuses with a fixed safe error before protected work

### Requirement: Migration preserves operational gates

Caller and same-commit reusable SHALL use explicit static selection and
preauthorization inputs, preserve read-only pre-environment admission and repeat
bootstrap/admission after approval. Unselected hosting MUST refuse. Isolation
success SHALL NOT authorize setup, dispatch or human/domain acceptance.

#### Scenario: Old inputs confer no authority
- **WHEN** only the old full-digest/grant input variables or fixture approval flags exist
- **THEN** no new dispatch context or live binding is authorized

#### Scenario: Isolated evidence remains isolated
- **WHEN** synthetic bootstrap and admission tests pass
- **THEN** T013/T014, protected receipts and consumer acceptance remain pending
