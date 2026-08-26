# roles-authority-model Specification

Deltas here are declared RELATIVE TO the OUTCOME of the active ratified change
`add-substantive-review-lane`, per
`openspec/specs/release-realization/spec.md:64-74` ("a proposal modifying a
requirement already modified by an active ratified change references that change
and declares its deltas relative to that change's outcome", with the scenario
"Two changes touch one requirement" making it a MUST). The MODIFIED requirement
below is NOT in the promoted spec today; it is ADDED by
`add-substantive-review-lane`, and the text restated here is that change's
outcome text plus this change's modification. Archive ordering is a consequence
of that mechanism, not a substitute for it.

## ADDED Requirements

### Requirement: Spec authority and code authority are named, held, delegable governance roles
`openxFactory` SHALL define two neutral Hermes-level governance roles — SPEC
AUTHORITY (standing over a governed unit's specifications and contracts) and
CODE AUTHORITY (standing over its implementation) — as roles that are HELD by a
named holder and DELEGATED by an explicit instrument, and SHALL NOT name either
role "owner": the corpus reserves ownership for a relation that explicitly
confers no authority (`openspec/specs/client-infrastructure-liaison/spec.md:18-30`,
scenario "Ownership does not confer authority" at `:28-30`), so a holder's
standing SHALL come entirely from its grant and never from an ownership label.
Both roles take their place in the neutral Owns/Decides table at
`docs/roles-and-authority.md:67-74`, and neither role SHALL be defined in any
domain repository, since this capability already owns Hermes-level governance
role definition.

#### Scenario: A domain defines the roles for itself
- **WHEN** a DomainxFactory declares a spec-authority or code-authority role in its own repository
- **THEN** the declaration MUST be a declared specialization of the neutral roles, never a competing definition

#### Scenario: The roles are named as ownership
- **WHEN** a document or record calls a holder of either role the "spec owner" or "code owner"
- **THEN** the naming is corrected, because ownership in this corpus confers no authority and the collision re-litigates itself at every reading

#### Scenario: Standing is asserted without an instrument
- **WHEN** a holder claims spec authority or code authority with no instrument naming it
- **THEN** the claim confers nothing

### Requirement: A body is not convened over the machinery it is assembled from
A reviewing body SHALL NOT be convened over a candidate that touches the
machinery that body is assembled from, and this rule SHALL be REFUSAL-ONLY: it
can only refuse a convening and SHALL never clear one, widen a candidate class,
raise a tier, or override the constitutional floor. The rule generalizes the
rule-setting/rule-applying separation already carried by the "Company-policy seat
participation in per-PR councils" requirement, and it SHALL be enforced where a
candidate cannot edit it; where no such enforcement point exists for a given
surface, the rule SHALL be recorded as UNENFORCED for that surface rather than
described as though it held.

#### Scenario: A candidate touches its own reviewing machinery
- **WHEN** a candidate modifies the definitions, prompts, mixes, or rules from which the convened body is assembled
- **THEN** the convening is refused and the candidate is parked for human review

#### Scenario: The rule is offered as a clearance
- **WHEN** a candidate does not touch the convening body's machinery
- **THEN** the rule is silent — it confers no eligibility, no tier, and no clearance

#### Scenario: A surface has no enforcement point
- **WHEN** the rule cannot be enforced outside the reviewed tree for some surface
- **THEN** the capability records the rule as unenforced for that surface, and the in-tree defences for it stand as the only defence

## MODIFIED Requirements

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
affirming codexFactory as its reviewing body. The reviewing home is single;
WHAT EACH HOLDER WITHIN IT MAY DO SHALL be carried by an explicit grant and by
nothing else, so extending the lane to a further repository SHALL be an INTAKE
act — issuing grants naming that repository's objects — and SHALL NOT require
the target repository to be restructured, relocated, or split, and no repository
layout SHALL be a precondition of review.

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

#### Scenario: Authority arrives with the reviewer, not with the layout
- **WHEN** the lane is extended to a repository whose specifications and implementation share one tree
- **THEN** the extension is discharged by issuing grants over that repository's objects
- **AND** no repository shape, split, or topology is required of it as a condition of review

#### Scenario: A holder within the single home exceeds its grant
- **WHEN** a seat of a reviewing council acts over an object its grant does not name
- **THEN** the act is outside its authority regardless of the seat's membership in the single reviewing home
