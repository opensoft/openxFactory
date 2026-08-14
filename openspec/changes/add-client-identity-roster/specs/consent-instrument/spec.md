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
