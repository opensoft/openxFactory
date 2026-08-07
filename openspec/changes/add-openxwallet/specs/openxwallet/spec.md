# agent-wallet-identity Specification (delta)

## ADDED Requirements

### Requirement: Agent identity is a governed record

openxFactory SHALL define a neutral agent identity record carrying a
stable decentralized identifier, a reference to the agent's signing key
(never the key material), the agent's declared COMPOSITION — model
version, prompt contract, tool manifest, policy version, parameters, and
retrieval corpus where one applies — a declared key-custody model, and a
lifecycle state. The record is the subject of authority: a grant, a
refusal, or an audit entry names an agent identity, not the service
credential that carried the call.

#### Scenario: the record names the agent, not the credential

- WHEN an agent acts through a shared service credential
- THEN the act is attributed to the agent identity record
- AND the shared credential is recorded as transport, never as the actor

#### Scenario: key material never enters the record

- WHEN an agent identity record is validated
- THEN it carries a key reference and a custody model
- AND a record containing private key material is a validation failure

### Requirement: An asserted identifier is never identity

openxFactory SHALL require proof of control for any request that claims an
agent identity: the request carries a signature verifiable against the
identity's declared key, and a request asserting an identifier without
verifiable proof is refused. The refusal names the missing proof rather
than the missing identifier, because the identifier was supplied and is
not the thing that was lacking.

#### Scenario: a claimed identifier is refused

- WHEN a request names an agent identity and carries no verifiable signature
- THEN the request is refused with the missing proof named
- AND no authority is granted on the strength of the claim

#### Scenario: verification failure is not identity absence

- WHEN a signature is present but does not verify against the declared key
- THEN the request is refused and the failure is recorded as a verification
  failure, distinct from an unidentified request
- AND the distinction survives into the audit record

### Requirement: Custody is declared and caps authority

openxFactory SHALL require every agent identity to declare its key-custody
model from a closed set, SHALL state what each model evidences, and SHALL
cap the authority an identity may hold by that model. A signature proves
only what its custody permits: a host-held key evidences that the HOST
acted, and only a custody model isolating the key from the agent's own
execution context evidences that the AGENT acted. The contract SHALL NOT
present these as equivalent.

#### Scenario: custody bounds the authority

- WHEN an identity requests authority above what its custody model evidences
- THEN the request is refused with the custody ceiling named
- AND raising the authority requires changing custody, not asserting trust

#### Scenario: what a signature proves is recorded, not assumed

- WHEN an act is audited
- THEN the record carries the custody model in force at the time of the act
- AND a reader can tell whether the agent or its host was evidenced

### Requirement: Authority reuses the approval-policy vocabulary

openxFactory SHALL express an agent identity's authority scope using the
neutral job envelope's existing `approval_policy` values rather than a
parallel vocabulary, so that what an agent may do is stated in the same
terms a job already carries.

#### Scenario: no parallel vocabulary is introduced

- WHEN an agent identity's authority is recorded
- THEN it names an existing approval-policy value
- AND a value outside that vocabulary is a validation failure

### Requirement: A composition change ends authority immediately

openxFactory SHALL treat any change to an agent's declared composition as
the end of that certified identity: authority is revoked at once, with no
tolerance band and no grace period, and resuming requires a new
certification of the changed agent. The rule generalizes an invalidation
the stack already practices on outputs — a prompt-contract version bump
invalidated every prior classification, because a judgment by prompt-v1 is
not the same classifier's judgment — from what an agent PRODUCED to what
it is PERMITTED.

#### Scenario: a changed agent is a different agent

- WHEN an attested composition hash differs from the certified hash
- THEN the identity's authority is revoked immediately
- AND outstanding grants issued to that identity are treated as expired

#### Scenario: revocation is not a percentage

- WHEN any single component of the composition changes
- THEN the change is sufficient on its own to revoke
- AND no threshold, score, or tolerance is consulted for a declared change

### Requirement: The capability is an authority control, never an identity substrate

openxFactory SHALL keep agent wallet identity composable and optional for
domains: it SHALL NOT become a prerequisite for reconstructing a record,
resolving a subject, or operating a domain without it, and a wallet
reference SHALL NOT become a subject identifier. This preserves the
ratified constraints in MedxFactory's `patient-identity-and-assembly` (a
wallet address is not identity proof) and `patient-snapshot-ledger-custody`
(custody remains wallet neutral and reconstructable with no wallet
available).

#### Scenario: a domain operating without wallets is conformant

- WHEN a domain adopts no agent wallet identity
- THEN its records remain reconstructable and its subjects resolvable
- AND no capability refuses it for the absence

#### Scenario: a wallet reference never becomes an identifier

- WHEN a subject or record carries an optional wallet reference
- THEN the reference is attestation, not identity
- AND any resolution treating it as the identifier is a validation failure
