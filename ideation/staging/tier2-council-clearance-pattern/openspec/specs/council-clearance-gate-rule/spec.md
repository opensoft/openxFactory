# council-clearance-gate-rule

## ADDED Requirements

### Requirement: Tier-2 council-clearance pattern
An instantiation of the council-clearance pattern SHALL compose a tier-2 clearance path onto an existing conjunctive tier-1 autonomous-approval envelope: when the envelope fails ONLY on conditions inside the instance's declared council-clearable set, the named council convenes, and its unanimous `ready` verdict pinned to the exact head SHA authorizes the approval the envelope would otherwise withhold.

#### Scenario: Envelope fails on a clearable condition
- WHEN the tier-1 envelope fails solely on a condition in the instance's declared clearable set
- THEN the instance's council convenes on the exact head SHA
- AND a unanimous `ready` verdict pinned to that SHA authorizes the approval
- AND any non-unanimous or unpinned verdict parks the item for the human

### Requirement: Owner-attributed static clearable set
An instance's council-clearable set SHALL be a static allowlist with a named owning seat, and every change to it SHALL be an owner-accepted recorded event — never an inline or unrecorded edit.

#### Scenario: Widening the clearable set
- WHEN an instance wants a new condition class admitted to its clearable set
- THEN the change is ruled through the instance's council and accepted by the named owning seat as a recorded event
- AND the amended allowlist remains static between such events

### Requirement: Never-clearable floor
Every instance SHALL park security-touching failures, check failures, and identity mismatches for the human. An instance MAY widen this floor and SHALL NOT narrow it.

#### Scenario: A floor condition fails
- WHEN the tier-1 envelope fails on a security-touching condition, a check failure, or an identity mismatch
- THEN the item parks for the human regardless of the clearable set or any council verdict

### Requirement: Anti-normalization rule
An instance SHALL demote a condition that is cleared repeatedly: past the instance's declared recurrence threshold the condition stops being clearable and parks with a fix-the-generator flag, so council clearance never becomes the standing substitute for fixing the source.

#### Scenario: A condition is cleared repeatedly
- WHEN the same condition is council-cleared more times than the instance's declared threshold
- THEN that condition is removed from the effective clearable set
- AND subsequent failures on it park for the human carrying a fix-the-generator flag

### Requirement: Instantiation is a recorded council exercise
Adopting this pattern in a repo SHALL be performed as a recorded Gate-Rules Council exercise — seat verifications, the clearable-set and allowlist-owner ruling, transport blessing, and the accountable authority's acknowledgement — and the instance SHALL ship `configured_but_inactive` behind an activation gate until council orchestration exists in its executing lane.

#### Scenario: A second repo instantiates the pattern
- WHEN a repo adopts the pattern for one of its autonomous sweeps
- THEN a Gate-Rules Council convening is recorded with seat verifications, the clearable-set ruling, and the named allowlist owner
- AND the instance activates only after its activation-gate requirements, including orchestrated council transport, are met
