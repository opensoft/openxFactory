# council-cleared-merge-gate Specification

## ADDED Requirements

### Requirement: A council-cleared approval satisfies the merge gate as a review, never as a check
A governed repository adopting the council-cleared merge gate SHALL leave its
required-review rule IN PLACE and SHALL express a clearance's effect as a real
`APPROVE` review cast by the merge-master App identity, so the gate composition
is unchanged and only the set of permitted approvers moves. A repository
adopting this capability SHALL NOT satisfy its review requirement with a
check-run, SHALL NOT reduce its required approving review count to zero in order
to admit the lane, and SHALL NOT configure its ruleset such that the App path is
the only satisfying path — human review remains always available. Where the
required-review rule is inherited from a ruleset governing repositories BEYOND
the adopting one, the adoption SHALL NOT edit that ruleset at all; any hardening
the adoption owes SHALL be expressed in a ruleset scoped to the adopting
repository alone.

#### Scenario: A clearance lands as a review
- **WHEN** a candidate is cleared under the lane and the enforcer approves it
- **THEN** the merge-master App casts a real `APPROVE` review
- **AND** that review is what satisfies the repository's required-review rule

#### Scenario: A check-run is offered as the satisfier
- **WHEN** an adoption proposes a required status check as the satisfier of the review rule
- **THEN** it is refused, because a name-matched check-run emitted by a lesser identity would otherwise buy an approval

#### Scenario: The review rule is inherited from a wider ruleset
- **WHEN** the adopting repository's approval requirement is carried by a ruleset that also governs other repositories
- **THEN** the adoption edits no rule in that ruleset
- **AND** any hardening it owes is written into a ruleset whose targeting names only the adopting repository

#### Scenario: The lane is unavailable
- **WHEN** the council lane produces no verdict, parks a candidate, or cannot run
- **THEN** a human review can still satisfy the rule, and the pull request is blocked rather than admitted

### Requirement: The clearable boundary is declared as named candidate classes, not as prose
An adopting repository SHALL declare its autonomously clearable surface as one or
more NAMED candidate classes, each an envelope candidate committed on the
repository's own default branch and bound to a per-repo gate rule by an explicit
candidate identifier, and each carrying exactly one declared
advisory-versus-clearable intent field as the sole authority for that question.
An adoption SHALL NOT express its boundary only as a list of paths, SHALL NOT
infer a rule-to-candidate binding from a rule identifier or repository field, and
SHALL NOT rely on a pull-request label, body, title or author self-declaration to
determine a class. A candidate class SHALL be declared with a resolvable
approved-scope reference; a class whose scope reference cannot be resolved is
never clearable.

#### Scenario: An adoption states only paths
- **WHEN** an adoption declares a clearable surface as a path list with no named candidate class
- **THEN** it is incomplete, because an enforcer matches candidates and rules, not prose

#### Scenario: A class is read from the pull request
- **WHEN** a classification would be taken from a label, a body marker, a title or the author's own declaration
- **THEN** it is refused, and the class is resolved only from base-branch-committed configuration

#### Scenario: Two surfaces differing in kind
- **WHEN** an adopting repository's clearable surface contains both human-authored prose and machine-regenerated output
- **THEN** they are declared as SEPARATE candidate classes, because a single class cannot distinguish a bad prose judgement from a bad generator run

### Requirement: The declared boundary is the path-shaped subset of a wider floor
An adoption SHALL state that its path-shaped boundary is a SUBSET of the ratified
never-clearable floor and SHALL NOT present the path list as the floor entire.
The adoption SHALL name where the floor's non-path conditions — identity
mismatch, head-reference mismatch, failed or pending required checks, and secret
findings — are enforced for the adopting repository, and an adoption that leaves
those conditions unattributed SHALL be treated as incomplete rather than as
silently inheriting them.

#### Scenario: A path list is presented as the whole floor
- **WHEN** an adoption's boundary section enumerates paths and names no other condition
- **THEN** it is incomplete, because four of the floor's members are not path-shaped

#### Scenario: A mixed diff
- **WHEN** a pull request touches both a clearable path and a human-only path
- **THEN** the whole pull request takes the most restrictive class of any path it touches

### Requirement: Autonomous clearance is gated on named realization evidence, and the gate states are facts re-verified at adoption
An adoption SHALL enumerate every precondition for autonomous approval as a
NAMED gate carrying the artifact that opens it, and each gate's evidence SHALL be
an observable artifact at a stated path — a merged pull request, a named test
file, a captured API response, or a committed record — never a checkbox count, a
prose gate line, or an assertion in a session log. A gate SHALL NOT be opened on
evidence inherited from the adoption document's own text: every gate state
recorded in an adoption is a fact as of its authoring date and SHALL be
re-verified at the moment the gate is claimed. Where the same task numbering
exists in more than one repository's packet, an adoption SHALL name the
repository and path of each, because ticking one does not tick the other.

#### Scenario: A gate is claimed on the adoption's own record
- **WHEN** a gate is asserted open because the adoption document lists it
- **THEN** the claim is refused and the gate is re-verified against the running system

#### Scenario: Evidence is a checkbox
- **WHEN** a gate's only evidence is a checked task box or a prose gate line
- **THEN** the gate remains closed until a named test file, merged pull request or captured artifact is produced

#### Scenario: A refusal path is demonstrated by its audit trail
- **WHEN** a fail-closed refusal is evidenced only by an existing council or enforcement audit trail
- **THEN** the evidence is insufficient and a named test asserting the refusal is required

### Requirement: Enrollment is advisory first and the clearable flip is its own ratified act
An adopting repository's candidate classes SHALL be enrolled at advisory intent
first, and the change of intent to clearable SHALL require its own ratified act
naming the classes it flips, with every realization gate green and the canary
complete. An adoption change SHALL NOT authorize the flip it prepares.
Where the rules-as-code refuses clearable intent for a class whose target
repository is not yet wired, that refusal SHALL be recorded as the structural
reason for advisory enrollment rather than presented as caution.

#### Scenario: An adoption authorizes its own flip
- **WHEN** an adoption change would set a class's intent to clearable on landing
- **THEN** it is refused, because the flip is one field in one file and must be a separate reviewed act

#### Scenario: The target repository is unwired
- **WHEN** a class is defined before its target repository carries an envelope on its default branch
- **THEN** the class is advisory, because the class-floor derivation reads a base-branch allowlist that does not yet exist

### Requirement: A dual-run canary spans every enrolled class before the flip
An adoption SHALL run a dual-run canary in which the council reaches and records
a verdict AND a human casts the approving review that merges the pull request,
and the canary SHALL span EVERY enrolled candidate class rather than accumulating
within one, because a canary confined to a single class cannot detect a
class-boundary error. Each canary observation SHALL be recorded as a committed
artifact naming the pull request, the verdict, the human judgement and whether
they agreed; a verdict that lands at no path is not an observation. A single
disagreement SHALL stop the canary and reopen the adoption.

#### Scenario: The canary fills inside one class
- **WHEN** every canary observation comes from one candidate class
- **THEN** the canary is not complete, whatever the count, because the boundary between classes went untested

#### Scenario: A verdict is reported but not recorded
- **WHEN** a council verdict is produced and no committed record names the pair
- **THEN** it does not count toward the canary

#### Scenario: The council and the human disagree
- **WHEN** one canary observation shows the council clearing what the human would not
- **THEN** the canary stops and the adoption reopens

### Requirement: The approving identity is authority-separated from the gate it satisfies
The identity casting a council-cleared approving review SHALL NOT hold
permission to modify the enforcement configuration of the gate it satisfies, and
SHALL NOT be granted repository administration. An adoption SHALL name the
approving identity's permission set explicitly, and SHALL mint a dedicated
identity token for the approval act rather than reusing the ambient workflow
credential.

#### Scenario: The approver could edit the ruleset
- **WHEN** the identity casting the approval also holds ruleset or branch-protection write
- **THEN** the adoption is refused, because an identity that can weaken the gate it is subject to is not gated

#### Scenario: The ambient credential is used to review
- **WHEN** an approval would be cast with the ambient workflow token
- **THEN** it is refused, and a dedicated App token is minted for the act

### Requirement: The adoption declares what ending the bypass does and does not mean
An adoption whose stated purpose is to end an administrative bypass ritual SHALL
state explicitly whether it narrows or removes the bypass ACTOR, and where it
does not, SHALL claim only that the bypass's ROUTINE USE ends rather than that
the bypass is closed. The adoption SHALL record the measured evidence that the
ritual exists.

#### Scenario: The bypass actor is untouched
- **WHEN** an adoption ends the routine use of a bypass but leaves the bypass actor configured
- **THEN** it says so plainly, and does not describe the bypass as removed

### Requirement: The lane stops by revocation, and every stop traces to running code
An adoption SHALL provide at least one stop that does not require editing a
ruleset, and SHALL trace each declared stop to the specific running mechanism
that enforces it — a revocation checked at verdict consumption, a standing
kill-switch or intent field the rules-as-code reads, or the removal of the
approving identity's credential. An adoption SHALL NOT attribute a stop to a
component that cannot perform the act being stopped.

#### Scenario: A stop is attributed to a read-only component
- **WHEN** a kill switch is described as removing credentials from a workflow that holds no write permission and mints no approver token
- **THEN** the description is corrected, because removing that component's credential stops a report and not an approval

#### Scenario: The holder's authority is revoked
- **WHEN** the reviewing holder's registered authority is revoked or has expired at the moment a verdict is consumed
- **THEN** the candidate parks with a named refusal and no approval is cast
