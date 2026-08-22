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
human-only. ADMIT is the neutral `roles-authority-model` verdict word, the
same one the existing "Low-risk enforcement envelope" requirement already
uses; the codexFactory realization of this lane expresses "unanimous ADMIT
with no undispositioned conditions" as its three-conjunct merge-readiness
predicate — `verdict == ready` AND every seat concurring AND
`undispositioned_conditions == 0` (the `verdict_required: ready_unanimous`
plus `undispositioned_conditions: 0` pair its rules-as-code carries) — so an
enforcer checking that predicate IS checking this requirement's condition.
The two vocabularies name one condition at two layers and MUST NOT be read as
two conditions.

#### Scenario: The neutral verdict word maps to the enforcement word
- **WHEN** an enforcer realizing this lane evaluates a
  `merge_readiness_council` verdict for the unanimous-ADMIT condition
- **THEN** the condition it checks is that realization's own verdict
  vocabulary — in the codexFactory lane, `ready`, with every seat concurring,
  and zero undispositioned conditions
- **AND** no separate ADMIT-named verdict value is required to exist in the
  realization

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
`merge_readiness_council`; codexFactory's councils SHALL be the reviewing
body for substantive pull requests in EVERY governed xFactory repository
that adopts this lane, whatever domain that repository governs — a pull
request's diff is software regardless of the domain — so no domain
repository instantiates review personas or councils of its own for this
lane, and the tenant `company-policy-lead` seat already seated in
codexFactory's `gate_rules_council` carries the policy dimension for every
adopting repository; extension of the lane to any further repository SHALL
proceed only through a subsequent change naming that repository and
affirming codexFactory as its reviewing body.

#### Scenario: Pilot is codexFactory-reviewed
- **WHEN** a substantive pull request against `opensoft/openxFactory` is
  evaluated under this lane
- **THEN** the reviewing `gate_rules_council` and `merge_readiness_council`
  are codexFactory's instantiated councils

#### Scenario: Extension requires a naming change
- **WHEN** a repository beyond the pilot is proposed for the substantive
  review lane
- **THEN** a subsequent change MUST name the repository and affirm
  codexFactory's councils as its reviewing body before the lane is enabled
  for it

#### Scenario: No second persona home is instantiated
- **WHEN** a governed repository outside codexFactory adopts the substantive
  review lane
- **THEN** it MUST NOT instantiate review personas or councils of its own
  for this lane
- **AND** its substantive pull requests are judged by codexFactory's
  `gate_rules_council` and `merge_readiness_council`

### Requirement: Adoption beyond the pilot qualifies on recorded evidence
Extension of the substantive review lane beyond the pilot repository SHALL be
authorized only by a named follow-up change raised on recorded pilot
evidence, and that evidence MUST show at least three council-cleared
substantive pull requests spanning at least two distinct candidate classes,
zero enforcer incidents, and one completed gate-rules review cycle; and
engineering-owned repositories SHALL be adopted before domain repositories,
so no domain repository is adopted into the lane while any engineering-owned
governed repository remains unadopted — each adoption still meeting the
evidence bar in its own right.

#### Scenario: Adoption proposed below the evidence bar
- **WHEN** a follow-up change proposes extending the lane to a further
  repository and the pilot's recorded evidence shows fewer than three
  council-cleared substantive pull requests, fewer than two distinct
  candidate classes, any enforcer incident, or no completed gate-rules
  review cycle
- **THEN** the extension MUST NOT be authorized
- **AND** the follow-up change MUST record which element of the bar is unmet

#### Scenario: A domain repository does not qualify while an engineering-owned one is unadopted
- **WHEN** a follow-up change proposes a domain repository as the next
  adoption, that repository clears the evidence bar, and it is the only
  repository proposed
- **THEN** the extension MUST NOT be authorized while any engineering-owned
  governed repository has not yet adopted the lane
- **AND** clearing the evidence bar does not by itself qualify a domain
  repository for adoption

#### Scenario: Engineering-owned repositories go first
- **WHEN** an engineering-owned repository and a domain repository are both
  candidates for the next adoption
- **THEN** the engineering-owned repository is adopted first

### Requirement: Company-policy seat participation in per-PR councils
The tenant `company-policy-lead` seat SHALL remain seated in the
`gate_rules_council` only and MUST NOT join per-PR `merge_readiness_council`
deliberation by default, preserving the rule-setting/rule-applying
separation; as the sole exception, a candidate class MAY declare a
company-policy pull-in condition, which the `gate_rules_council` — where that
seat already sits — SHALL define at class-definition time and never per pull
request. The condition is evaluated PER PULL REQUEST: only when a pull
request matches such a class AND that class's declared condition HOLDS for
that pull request is the `company-policy-lead` seat required, and it MUST
then be convened into that pull request's `merge_readiness_council`, with a
convening that cannot seat it refused and the candidate parked rather than
proceeding on the remaining seats. Where the condition does not hold, the
seat is not required and the convening proceeds domain-seats-only, so the
fail-closed cost falls on matched-and-triggered pull requests only and never
on every pull request of a declaring class.

#### Scenario: Default posture is rules-council-only
- **WHEN** a pull request matches a candidate class that declares no
  company-policy pull-in condition
- **THEN** its `merge_readiness_council` convenes with its domain seats only
- **AND** the company-policy dimension is carried by the class rules the
  `gate_rules_council` already set

#### Scenario: A declared pull-in condition seats the tenant seat per-PR
- **WHEN** a pull request matches a candidate class whose declared
  company-policy pull-in condition holds
- **THEN** the `company-policy-lead` seat MUST be convened into that pull
  request's `merge_readiness_council`
- **AND** its rationale MUST appear in that pull request's verdict record

#### Scenario: A declared condition that does not hold for this pull request
- **WHEN** a pull request matches a candidate class that DOES declare a
  company-policy pull-in condition, but that condition does not hold for this
  particular pull request
- **THEN** its `merge_readiness_council` convenes with its domain seats only
- **AND** the `company-policy-lead` seat is not required, so its
  unavailability MUST NOT park this pull request

#### Scenario: A pull-in class fails closed without the seat
- **WHEN** a convening cannot seat the `company-policy-lead` seat for a pull
  request whose matched class declares a pull-in condition that DOES hold
- **THEN** the convening MUST be refused and the candidate parked
- **AND** the enforcer MUST NOT approve the pull request on the remaining
  seats

#### Scenario: Only the rules council defines the condition
- **WHEN** a company-policy pull-in condition is introduced for a candidate
  class
- **THEN** it MUST be defined by the `gate_rules_council` at
  class-definition time
- **AND** it MUST NOT be introduced or altered per pull request

### Requirement: Ruleset interaction shape for the substantive review lane
Where a candidate IS cleared under this lane, the approval SHALL satisfy the
governed repository's required-review rule by the merge-master App casting a
real `APPROVE` review — this requirement fixes the SHAPE of a clearance's
effect on the ruleset and creates no obligation to clear or to approve any
particular pull request; the council-verdict check-run SHALL remain
verdict transport only and MUST NEVER be configured as a ruleset-accepted
satisfier; and human review SHALL remain an always-available alternate
satisfying path on every governed repository, so no repository's ruleset may
be configured such that only the council-cleared App path satisfies it — any
per-repo divergence from this default requires its own recorded decision
inside that repository's adoption change.

#### Scenario: Approval satisfies by a real review
- **WHEN** a council verdict clears a candidate and the enforcer approves it
- **THEN** the merge-master App casts a real `APPROVE` review
- **AND** that review is what satisfies the repository's required-review rule

#### Scenario: The check-run is never a ruleset satisfier
- **WHEN** a repository's ruleset is wired for this lane
- **THEN** the `council-verdict/merge-readiness` check-run MUST NOT be
  configured as a satisfier of the review gate
- **AND** the recorded reason is the lane's own anti-spoofing analysis: a
  name-matched check-run emitted by a lesser App would otherwise buy an
  approval

#### Scenario: Human review is never removed
- **WHEN** the council lane is unavailable, produces no verdict, or parks a
  candidate
- **THEN** a human review MUST still be able to satisfy that repository's
  required-review rule
- **AND** no repository's ruleset may be configured App-path-only

#### Scenario: Divergence requires its own recorded decision
- **WHEN** a repository proposes a ruleset interaction shape differing from
  this default
- **THEN** that repository's adoption change MUST record the divergence as
  its own decision before the lane is enabled for it

### Requirement: Constitutional floor for autonomous clearance
The ratified never-clearable floor SHALL be tier-independent — identity
mismatch, HEAD-REF mismatch, failed or pending required checks, secret
findings, security-touching paths, and gate-weakening changes — and no risk
tier, clearance rule, or unanimous council verdict SHALL ever override it.
The floor's SOURCE OF TRUTH is the `gate_rules_council`'s ratifying record of
2026-07-23 (codexFactory
`hermes/domain/review-councils/records/2026-07-23-gate-rules-nightly-sweep-clearance.md`,
whose `per_repo_gate_rules` block records the floor's six members: identity,
head ref, any failed check, secret findings, security-touching paths,
gate-weakening changes); the enumeration restated here is a convenience, and
where it and that record ever diverge the record governs and this text MUST
be corrected against it. Any candidate class
touching contract bytes, gate or workflow definitions, credential surfaces,
or security posture SHALL be permanently human-only regardless of unanimity;
and autonomous clearance SHALL be eligible only for candidate classes whose
blast radius is docs- or derived-artifact-shaped, which today is exactly the
proven docs class. The enumerated, ordered tier vocabulary and its per-tier
clearance eligibility are deliberately NOT fixed by this requirement; they
are deferred to a named follow-up change raised on pilot evidence, and until
then the "Substantive candidate classes defined by the gate-rules council"
requirement's declare-presence-not-vocabulary rule governs tier naming.

#### Scenario: Unanimity does not override the floor
- **WHEN** a candidate trips any floor condition and the
  `merge_readiness_council`'s verdict is nonetheless a unanimous ADMIT
- **THEN** the enforcer MUST NOT approve the pull request
- **AND** it parks the candidate for human review

#### Scenario: Permanently human-only surfaces
- **WHEN** a candidate class is defined whose matching pull requests can
  touch contract bytes, gate or workflow definitions, credential surfaces,
  or security posture
- **THEN** the `gate_rules_council` MUST declare that class human-only
- **AND** no verdict under it SHALL ever produce an autonomous approval

#### Scenario: Autonomous eligibility is blast-radius bounded
- **WHEN** a candidate class whose blast radius is not docs- or
  derived-artifact-shaped is proposed as autonomously clearable
- **THEN** the `gate_rules_council` MUST refuse to publish it as
  autonomously clearable
