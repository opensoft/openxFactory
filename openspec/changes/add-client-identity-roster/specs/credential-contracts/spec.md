# credential-contracts — add-client-identity-roster deltas

## MODIFIED Requirements

### Requirement: Canonical credential record shapes
Credential contract records SHALL validate against the canonical
`contracts/schemas/xfactory-credential-contracts.schema.yaml`, which owns
the five record kinds: `xfactory_credential_requirements`,
`xfactory_runtime_capability_grant_template`,
`xfactory_credential_binding_template`,
`xfactory_credential_broker_contract`, and
`xfactory_credential_audit_policy`. Domain content — credential families,
scopes, providers, workflow and action names — is domain-local; the schema
constrains shape only, and semantic invariants remain owned by the
credential access model.
The schema SHALL additionally own an `issuance_preconditions` vocabulary: a
CLOSED set of neutral precondition tokens that a credential requirement
record MAY declare, each naming a governed condition which must hold before a
grant is issued against that requirement. Its first member is the
ROSTER-DRIFT precondition — an open drift finding recorded against the roster
entry covering the identity a grant would name blocks issuance of that grant.
Declaring a precondition is optional and additive; declaring a member outside
the vocabulary is invalid, because a free-text precondition riding a schema
that neither declares nor forbids it is unenforceable and invisible to every
consumer of the pinned contract. Precondition EVALUATION — which drift
records exist and who reads them — stays with the owning contract families
and the domain mint surface that issues the grant; this schema owns the
vocabulary and the declaration shape only.

#### Scenario: A domain authors a credential contract
- **WHEN** a DomainxFactory adds or edits a file under `credentials/` carrying one of the five kinds
- **THEN** it MUST validate against the pinned canonical schema

#### Scenario: A file lacks the envelope
- **WHEN** a credentials file has no `kind`
- **THEN** the validator MUST report an error

#### Scenario: A domain policy record is present
- **WHEN** a credentials file carries a kind outside the five contract kinds
- **THEN** the validator MUST skip it with notice — such kinds are candidates for future promotion, not silent failures

#### Scenario: A requirement record declares the roster-drift precondition
- **WHEN** a credential requirement record declares the roster-drift member of `issuance_preconditions`
- **THEN** it validates, and the declaration is the neutral expression of the ratified refusal: an open drift finding on the covering roster entry blocks issuance of a grant naming that identity
- **AND** a requirement record declaring no preconditions remains valid, because the vocabulary is optional and additive

#### Scenario: A precondition outside the vocabulary
- **WHEN** a requirement record declares an `issuance_preconditions` member that is not in the closed vocabulary
- **THEN** the validator MUST report an error naming the closed vocabulary rather than accepting an unenforceable free-text condition

#### Scenario: The neutral layer proves the precondition by fixture
- **WHEN** the neutral realization of the roster-drift precondition is demonstrated
- **THEN** the demonstration is a conformant requirement-record fixture declaring it, because the neutral layer holds no producer of live drift findings and issues no grant itself
- **AND** at this capability's modification no live drift producer existed anywhere in the family, so the fixture is the whole neutral criterion and live refuse-then-allow behaviour is proven at the domain mint surface as a follow-up
