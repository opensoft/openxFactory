# roles-authority-model — add-substantive-review-lane deltas

## ADDED Requirements

### Requirement: Substantive review authority generalization
Governed councils SHALL be authorized to review substantive pull requests —
human- and agent-authored alike — across governed xFactory repos, generalizing
beyond the single narrow bot-authored candidate class in force as of
2026-08-15, and this authority SHALL NEVER be exercised by moving review
judgment into the Merge Master enforcer: Merge Master SHALL remain a
mechanical operator that consumes a council verdict and never originates one.

#### Scenario: Generalization adds classes, not judgment
- **WHEN** a new substantive candidate class is added under this authority
- **THEN** the class carries a council-verdict requirement rather than an
  enforcer-evaluated content rule
- **AND** Merge Master's own logic gains no new judgment capability

#### Scenario: Existing narrow class is undisturbed
- **WHEN** the existing `doc-health-nightly` candidate class and its
  `docs_only_path_overflow` council-clearable condition continue to operate
- **THEN** this generalization requires neither their removal nor their
  modification

### Requirement: Substantive candidate classes defined by the gate-rules council
For each governed repository, the `gate_rules_council` SHALL define the set
of substantive candidate classes — human- and agent-authored pull requests
eligible for autonomous council-cleared approval — and every class MUST
declare a risk tier and a clearance rule; the council's review in defining or
revising any class MUST cover both company-policy compliance, via its tenant
company-policy-lead seat, and domain best practices, via its domain seats.

#### Scenario: A repo without defined classes has none
- **WHEN** a governed repository has no `gate_rules_council`-defined
  substantive candidate classes
- **THEN** no pull request in that repository may be autonomously approved
  under the substantive review lane
- **AND** every review path for that repository falls back to human review

#### Scenario: A class omits its risk tier or clearance rule
- **WHEN** a candidate class is authored without a declared risk tier or a
  declared clearance rule
- **THEN** the `gate_rules_council` MUST refuse to publish it as an
  enforceable class

#### Scenario: Company-policy and best-practice review are both exercised
- **WHEN** the `gate_rules_council` defines or revises a substantive
  candidate class
- **THEN** its record MUST show the company-policy-lead seat's compliance
  rationale and a domain seat's best-practice rationale

### Requirement: Substantive review accountability
Every seat participating in a substantive-review verdict SHALL produce a
written rationale, the verdict SHALL transport as a signed, identity-bound
check-run, an audit artifact SHALL record the reviewed inputs, the gate
rules version in force, and every seat's verdict, and the approving review
on the pull request SHALL be cast by a dedicated reviewer/merge-master App
identity that MUST NOT be `GITHUB_TOKEN` and MUST NOT be the identity that
authored the pull request.

#### Scenario: A verdict without a seat rationale is incomplete
- **WHEN** a council-verdict check-run is produced without a written
  rationale from every participating seat
- **THEN** the enforcer MUST treat the verdict as absent
- **AND** the candidate parks for human review

#### Scenario: Approval identity is dedicated
- **WHEN** Merge Master submits an approving review under this lane
- **THEN** the review MUST be cast by the dedicated merge-master App identity
- **AND** it MUST NOT be cast using `GITHUB_TOKEN` or the pull request's own
  authoring identity

#### Scenario: Audit artifact is produced
- **WHEN** a substantive-review verdict clears a pull request for autonomous
  approval
- **THEN** an audit artifact recording the reviewed inputs, the gate rules
  version, and every seat's verdict MUST exist
- **AND** the approval MUST reference that audit artifact

### Requirement: Reviewer and enforcer identity separation from the author
The reviewing council and the enforcing identity SHALL be distinct from the identity that authored the pull request, whether the author is human or agent, and every candidate-class rule SHALL be evaluated by reading its definition from the repository's base branch, never from the pull request's own head.

#### Scenario: Author identity cannot self-clear
- **WHEN** a pull request's author identity matches a participating seat's
  identity or the merge-master approving identity
- **THEN** the candidate MUST be refused clearance under this lane
- **AND** it parks for human review

#### Scenario: Rules read from base branch only
- **WHEN** the enforcer evaluates a candidate against its repository's gate
  rules
- **THEN** it MUST read the rule definitions from the base (default) branch
- **AND** it MUST NOT honor rule content proposed within the pull request's
  own head

### Requirement: Fail-closed substantive review envelope
An enforcer acting under the substantive review lane SHALL approve a pull
request only when it matches a `gate_rules_council`-defined candidate class
AND the `merge_readiness_council`'s verdict is unanimous ADMIT with no
undispositioned conditions AND the low-risk enforcement envelope otherwise
holds; any pull request outside a defined candidate class, any non-unanimous
or conditioned verdict, and any stale or missing gate-rules version SHALL
result in no approval and a parked candidate carrying an explanation, and
`needs_human_review` escalation SHALL remain available at every candidate
class, with the `gate_rules_council` empowered to declare any given class
human-only.

#### Scenario: Outside every candidate class
- **WHEN** a pull request matches no `gate_rules_council`-defined candidate
  class for its repository
- **THEN** the enforcer MUST NOT approve it
- **AND** it MUST park the candidate with an explanation naming the absent
  class

#### Scenario: Conditioned or non-unanimous verdict
- **WHEN** the `merge_readiness_council`'s verdict is `needs_human_review`,
  is not unanimous, or carries an undispositioned condition
- **THEN** the enforcer MUST NOT approve the pull request

#### Scenario: Stale gate rules
- **WHEN** the gate rules version referenced by a verdict does not match the
  version currently in force for the repository
- **THEN** the enforcer MUST treat the verdict as missing
- **AND** it MUST park the candidate

#### Scenario: Human-only class
- **WHEN** the `gate_rules_council` declares a candidate class human-only
- **THEN** no verdict under that class SHALL ever produce an autonomous
  approval, regardless of unanimity

### Requirement: Pilot repository and reviewing domain
`opensoft/openxFactory` SHALL be the pilot repository for the substantive
review lane, reviewed by codexFactory's `gate_rules_council` and
`merge_readiness_council` under the software-engineering domain reviewing the
engineering-contracts repository, and extension of the lane to any further
repository SHALL proceed only through a subsequent change naming that
repository and, where the repository is not itself engineering-owned, the
reviewing domain's persona home.

#### Scenario: Pilot is codexFactory-reviewed
- **WHEN** a substantive pull request against `opensoft/openxFactory` is
  evaluated under this lane
- **THEN** the reviewing `gate_rules_council` and `merge_readiness_council`
  are codexFactory's instantiated councils

#### Scenario: Extension requires a naming change
- **WHEN** a repository beyond the pilot is proposed for the substantive
  review lane
- **THEN** a subsequent change MUST name the repository and its reviewing
  domain's persona home before the lane is enabled for it
