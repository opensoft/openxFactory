# consent-instrument — add-client-identity-roster deltas

## MODIFIED Requirements

### Requirement: Termination Cascades Through Declared Dependent References
The instrument SHALL carry first-class dependent-artifact references
(derived consent profiles, credential grants, adapter activations, and
governed identities standing in the consenting party's tenant), and
on termination or withdrawal each reference falls due under the record's
revocation SLA with an evidence obligation; cascade mechanics stay in the
owning contract families. A governed identity is a dependent artifact
because revoking a credential grant leaves the identity itself standing —
still registered, and still admitted in the provider's own administrative
surfaces — so an instrument whose cascade reaches only credentials leaves
reachable authority behind after withdrawal.

#### Scenario: Termination raises the whole chain

- **WHEN** an instrument enters `terminated`
- **THEN** every declared dependent reference must show cascade evidence
  within the record's revocation SLA
- **AND** an undeclared dependent discovered later is a conformance
  finding against the instrument, not the dependent

#### Scenario: Withdrawal reaches the identity, not only its credentials

- **WHEN** an instrument authorizing a governed identity in the consenting party's tenant enters `terminated` or `withdrawn`
- **THEN** the identity's roster entry falls due alongside its credential grants
- **AND** cascade evidence covers the identity's removal or retirement and the withdrawal of its provider-side admission, not merely the revocation of its credentials

### Requirement: The Lifecycle Enum Is Closed With Declared Aliases
The instrument status SHALL be the closed six-state lifecycle `draft →
pending_signatures → executed → amended → terminated`, with `withdrawn` a
second terminal state reachable once the instrument is past execution;
`withdrawn` is a DISTINCT member and MUST NOT be declared as an alias of
`terminated`, because withdrawal by the consenting party and termination are
distinct events that both raise the cascade obligation. A domain spelling
outside the enum maps via an alias DECLARED at conformance time, and a class
may skip `pending_signatures` only when its class declaration says so —
class-appropriate skipping, never silent.

#### Scenario: A domain alias maps at conformance time

- **WHEN** the Ledgerx record carries `status: active`
- **THEN** its conformance declaration maps `active` → `executed`
- **AND** the underlying record keeps its domain spelling

#### Scenario: A non-signature class enters executed directly

- **WHEN** a `portal_acceptance` instrument is accepted
- **THEN** it may enter `executed` without `pending_signatures` because
  its class declares no signature phase
- **AND** an undeclared skip is nonconformant

#### Scenario: Withdrawal is its own terminal state, never an alias

- **WHEN** a consenting party withdraws an executed instrument
- **THEN** the record carries `status: withdrawn`, not `terminated`
- **AND** a class registry declaring `withdrawn` as an alias of `terminated`
  is nonconformant
