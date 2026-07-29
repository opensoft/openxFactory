## MODIFIED Requirements

### Requirement: Realization archive gate
A change with a non-empty code surface SHALL NOT archive until realization
evidence exists: its code merged on the implemented target through the
owning domain's engineering gates, and — where the surface is runnable — a
green run of that surface. Where realization deploys onto a surface that is
a registered managed subject of another factory, the realization evidence
SHALL reference the completed deployment handoff request by correlation
identifier — correlation, not duplication: the request record remains with
the executing factory. Until then the change remains active as
approved-but-unrealized intent, preserving the invariant that promoted
specs describe what the code does.

#### Scenario: Implementation is merged but the run fails
- **WHEN** a code-surface change's artifacts are merged but its runnable surface has not run green
- **THEN** the change remains active
- **AND** archiving it is a contested-class act requiring an explicit disposition

#### Scenario: Realization completes
- **WHEN** merge evidence and a green run exist on the implemented target
- **THEN** the change archives and its deltas promote, exactly as doc-only changes do on landing

#### Scenario: Realization deploys onto a managed subject
- **WHEN** a change's realization includes deployment onto a registered managed subject of another factory
- **THEN** the realization evidence references the completed handoff request's correlation identifier
- **AND** a deployment claim with no correlatable accepted request MUST NOT count as realization evidence
