# release-realization Delta: Proposal Origin Contract

## ADDED Requirements

### Requirement: Origin retention at archive
The archive gate SHALL verify that a change's `.openspec.yaml` still carries
its original origin declaration unchanged. For staged origins, the
compressed supporting-document manifest SHALL retain the same origin id and
path; for ad-hoc origins, the archived change SHALL retain the reason and
approval provenance even when no support bundle exists. Mutation of an
origin declaration after ratification SHALL be rejected at the archive gate.

#### Scenario: A staged-origin change archives
- **WHEN** a change with a staged origin reaches its archive gate
- **THEN** the archived `.openspec.yaml` and the readable support manifest MUST carry the identical origin id and path declared at creation

#### Scenario: An ad-hoc change without a support bundle archives
- **WHEN** a change with an ad-hoc origin and no supporting documents reaches its archive gate
- **THEN** the archived packet MUST retain the origin's reason, approving authority, and approval date

#### Scenario: An origin was mutated after ratification
- **WHEN** the archive gate finds the origin declaration differs from the declaration present at ratification
- **THEN** the archive MUST fail
- **AND** restoring or accepting the mutation is a contested-class act requiring an explicit disposition
