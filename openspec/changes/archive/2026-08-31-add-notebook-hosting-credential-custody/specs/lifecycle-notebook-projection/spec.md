# lifecycle-notebook-projection (delta) — add-notebook-hosting-credential-custody

## ADDED Requirements

### Requirement: The hosting record declares where the hosting identity's credential is held, by reference only
An install declaring an operator-hosted projection SHALL record WHERE that account's credential is held — a reference to the governed custody binding that resolves it — and SHALL NOT record the credential itself. The hosting record already names the account; naming its custody is what makes the account operable by someone other than whoever created it, which is the whole point of moving off a personal identity.

The reference SHALL identify the binding, not the secret's value, and SHALL be sufficient to find the credential through the governed path and insufficient to obtain it without one. A password, a recovery code, a TOTP seed, a session cookie or an exported profile SHALL NOT appear in the hosting record, in the repository, or in any projection artifact.

A SELF-HOSTED declaration SHALL NOT be required to name custody. An individual operating their own account under their own authority has no operator to bear the obligation, exactly as the two-case model already holds elsewhere.

The record SHALL state the custody's honest reach: which secrets the binding covers, and — where the platform's sign-in cannot be performed from that material alone — that the remaining step is interactive. A custody reference that implies unattended access the install does not have is worse than none, because it invites a reader to plan on it.

#### Scenario: An operator-hosted install declares custody
- **WHEN** an install declares the operator-hosted case
- **THEN** its hosting record carries a reference to the governed custody binding for that account's credential
- **AND** the record carries no credential material of any kind

#### Scenario: A secret is placed in the hosting record
- **WHEN** a password, recovery code, TOTP seed, session cookie or exported profile is written into the hosting record
- **THEN** the record is non-conforming, and the remedy is a binding reference rather than redaction in place

#### Scenario: A self-hosted install declares no custody
- **WHEN** an individual declares the self-hosted case against their own account
- **THEN** the absence of a custody reference is conforming, because no operator exists to bear the obligation

#### Scenario: The custody covers less than the sign-in needs
- **WHEN** the declared custody holds material insufficient to complete the platform's sign-in unaided
- **THEN** the record says so plainly, naming the interactive step that remains
- **AND** the projection is not described as having unattended access to its own hosting account
