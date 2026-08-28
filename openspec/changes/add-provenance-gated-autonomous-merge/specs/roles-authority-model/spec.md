# roles-authority-model Specification

Deltas here are declared RELATIVE TO the OUTCOME of the active ratified change
`add-substantive-review-lane`, per
`openspec/specs/release-realization/spec.md` ("Ordered deltas and branch
vocabulary": "a proposal modifying a requirement already modified by an active
ratified change references that change and declares its deltas relative to that
change's outcome", with the scenario "Two changes touch one requirement" making
it a MUST). The MODIFIED requirement below is NOT in the promoted spec today; it
is ADDED by `add-substantive-review-lane`, and the text restated here is that
change's outcome text plus this change's modification. Archive ordering is a
consequence of that mechanism, not a substitute for it.

## MODIFIED Requirements

### Requirement: Constitutional floor for autonomous clearance
The ratified never-clearable floor SHALL be tier-independent — identity
mismatch, HEAD-REF mismatch, failed or pending required checks, secret
findings, security-touching paths, and gate-weakening changes — and no risk
tier, clearance rule, unanimous council verdict, OR governed provenance SHALL
ever override it. The floor's SOURCE OF TRUTH is the `gate_rules_council`'s
ratifying record of 2026-07-23 (codexFactory
`hermes/domain/review-councils/records/2026-07-23-gate-rules-nightly-sweep-clearance.md`,
whose `per_repo_gate_rules` block records the floor's six members: identity,
head ref, any failed check, secret findings, security-touching paths,
gate-weakening changes); the enumeration restated here is a convenience, and
where it and that record ever diverge the record governs and this text MUST
be corrected against it. Any candidate class touching contract bytes, gate or
workflow definitions, credential surfaces, or security posture SHALL be
permanently human-only regardless of unanimity OR provenance.

Autonomous clearance eligibility SHALL be an ORTHOGONAL, EITHER-OR judgment on
two independent axes: a candidate is eligible if its blast radius is docs- or
derived-artifact-shaped (the blast-radius axis, which today is exactly the
proven docs class), OR if its provenance is fully governed under the interim
provenance-completeness criterion (the provenance axis, defined in the
"Provenance-completeness eligibility for autonomous clearance" requirement).
Eligibility on either axis SHALL grant nothing the never-clearable floor
forbids; the floor binds IDENTICALLY on both axes. Neither the introduction of
the provenance axis nor any widening of a definition-time eligibility predicate
to realize it SHALL weaken, bypass, or demote the floor's enforcement.

The enumerated, ordered tier vocabulary and its per-tier clearance eligibility
are deliberately NOT fixed by this requirement; they are deferred to a named
follow-up change raised on pilot evidence, and until then the "Substantive
candidate classes defined by the gate-rules council" requirement's
declare-presence-not-vocabulary rule governs tier naming.

#### Scenario: Unanimity does not override the floor
- **WHEN** a candidate trips any floor condition and the
  `merge_readiness_council`'s verdict is nonetheless a unanimous ADMIT
- **THEN** the enforcer MUST NOT approve the pull request
- **AND** it parks the candidate for human review

#### Scenario: Provenance does not override the floor
- **WHEN** a candidate satisfies the full provenance-completeness criterion but
  trips any floor condition — including touching the decision core, the suites
  that prove it, or any gate, workflow, credential, or governance surface
- **THEN** the enforcer MUST NOT approve the pull request
- **AND** it parks the candidate for human review, so a ratified proposal can
  never autonomously merge a change to its own checker

#### Scenario: Permanently human-only surfaces
- **WHEN** a candidate class is defined whose matching pull requests can
  touch contract bytes, gate or workflow definitions, credential surfaces,
  or security posture
- **THEN** the `gate_rules_council` MUST declare that class human-only
- **AND** no verdict under it SHALL ever produce an autonomous approval,
  on either the blast-radius or the provenance axis

#### Scenario: Autonomous eligibility is blast-radius bounded OR provenance bounded
- **WHEN** a candidate class whose blast radius is not docs- or
  derived-artifact-shaped is proposed as autonomously clearable
- **THEN** the `gate_rules_council` MUST refuse to publish it as
  autonomously clearable UNLESS it qualifies on the provenance axis under the
  provenance-completeness criterion and its verifier contract
- **AND** in either case the never-clearable floor still binds

## ADDED Requirements

### Requirement: Provenance-completeness eligibility for autonomous clearance
The neutral authority model SHALL define an INTERIM provenance-completeness
criterion under which a real code pull request MAY become autonomously
clearable. A code pull request SHALL be provenance-eligible if and ONLY if ALL
of the following hold: (1) the repository is ENROLLED for council clearance via
its base-branch `.github/merge-approval-envelope.yml` record; (2) the pull
request is TIED TO A RATIFIED PROPOSAL — mechanically verified per the
"Provenance-tie verifier contract" requirement: the pull request resolves to a
single OpenSpec change that is currently `Status: ratified` and carries a
council ratification record; (3) ALL required checks are GREEN, including the
council merge-readiness verdict of `ready`; and (4) the candidate is STILL
OUTSIDE the never-clearable floor. This criterion is ADDITIVE to the
blast-radius eligibility axis and SHALL NOT relax the floor. It is explicitly
INTERIM and time-boxed, superseded by the full-pipeline-green successor. The
criterion's safety basis SHALL be recorded as the complete, mechanically
verified governed traceability chain — NOT review quality or council seat
composition — and this requirement SHALL take no position on the open
seat-diversity question (`seat_diversity_disposed_on_soak_evidence`).

#### Scenario: All four conditions hold
- **WHEN** a code pull request is in an enrolled repository, resolves to a
  currently-ratified OpenSpec change with a council ratification record, has all
  required checks green including a `ready` merge-readiness verdict, and trips no
  floor condition
- **THEN** it is provenance-eligible for autonomous clearance on the provenance
  axis

#### Scenario: Any one condition fails
- **WHEN** any of the four conditions does not hold
- **THEN** the candidate is NOT provenance-eligible and parks for human review

#### Scenario: The repository is not enrolled
- **WHEN** the base-branch `.github/merge-approval-envelope.yml` does not enroll
  the candidate's effort or class
- **THEN** condition (1) fails and the candidate parks — enrollment is never
  inferred from the pull request itself

#### Scenario: Safety basis is provenance, not review quality
- **WHEN** the eligibility of a provenance-axis candidate is asserted
- **THEN** the asserted basis is the complete governed traceability chain, and
  no claim is made that review quality or seat diversity established the safety

### Requirement: Provenance-tie verifier contract
The provenance tie SHALL be established by a mechanical verifier evaluated at
clearance time from the BASE branch, and the verifier SHALL FAIL CLOSED — park
for human review — on any broken, ambiguous, out-of-scope, stale-status,
unsigned-record, or non-enumerable-scope link. The verifier SHALL: (i) resolve
the tie from an explicit anchor and CORROBORATE it against a source the pull
request head cannot author (a base-branch effort/change record), so an
author-controlled string alone — a head branch name or a pull-request-body
reference — NEVER establishes the tie; (ii) resolve the tied change's
ratification state at evaluation time, never from a cached earlier resolution,
and require both a CURRENTLY-ratified status (not superseded, not retired) and a
SIGNED, identity-bound council ratification record, trusted only as a signed
artifact and never as a plain committed file any tree-writer could fabricate;
(iii) confirm the pull request's changed paths fall WITHIN the tied change's
MACHINE-READABLE path scope (a glob allowlist), treating a change whose declared
scope is prose or repository-level as INELIGIBLE rather than as "all paths in
scope"; and (iv) pin its evaluation to the same head/base commit pair as the
merge-readiness verdict, so any base advance re-runs the tie. When the verifier
parks a candidate, the park record SHALL name which of the eligibility
conditions or verifier sub-checks failed.

#### Scenario: Tie rests on an author-controlled string alone
- **WHEN** the only evidence of the tie is a head branch name or pull-request
  body reference, with no corroborating base-branch effort/change record
- **THEN** the tie is insufficient and the candidate parks

#### Scenario: Tied change is not currently ratified
- **WHEN** the tied change's status at evaluation time is anything other than
  currently-`ratified` — including superseded or retired after the pull request
  opened
- **THEN** the candidate loses provenance eligibility and parks, regardless of
  any prior ratified state

#### Scenario: Ratification record is not a signed artifact
- **WHEN** the council ratification record is presented only as a plain
  committed file rather than a signed, identity-bound artifact
- **THEN** the tie is not established and the candidate parks

#### Scenario: Scope is prose or repository-level
- **WHEN** the tied change's declared scope is prose `code_surface` or
  repository-granularity, with no machine-readable path allowlist
- **THEN** the candidate is ineligible and parks — scope is never widened to
  "all paths in scope"

#### Scenario: Changed paths fall outside the tied scope
- **WHEN** any changed path in the pull request falls outside the tied change's
  machine-readable path allowlist
- **THEN** the candidate parks, so the tie proves the diff was authorized rather
  than only that a same-named ratified change exists

#### Scenario: Base advances after evaluation
- **WHEN** the base commit advances after the tie was evaluated
- **THEN** the tie is re-evaluated against the new base before any approval

#### Scenario: Park record names the failed check
- **WHEN** the verifier parks a candidate
- **THEN** the park record names which eligibility condition (1)–(4) or verifier
  sub-check (i)–(iv) failed

### Requirement: Floor primacy and per-repository floor instantiation for the provenance axis
Realizing the provenance axis SHALL NOT demote floor enforcement. Any candidate
class made eligible on the provenance axis SHALL be judged through the SAME
definition-time floor walk over the class's entire path allowlist that governs
the blast-radius axis, never a structurally separate check that could bypass it.
The realization SHALL state EXPLICITLY which enforcement is primary for the
provenance axis: where a provenance-eligible class carries a broad allowlist, the
per-pull-request provenance-tie verifier SHALL be the primary enforcement and the
definition-time floor a MANDATORY backstop; this SHALL be stated, not implied.
Each enrolling repository SHALL publish its OWN tree-validated never-clearable
floor covering that repository's decision core, gate, workflow, credential,
governance, and council-record surfaces BEFORE any non-docs-shaped class is
enabled for it, because floor semantics are tree-specific and do not transfer
between repositories.

The definition-time floor predicate and its protected-surface set SHALL be the
ENROLLING REPOSITORY'S floor instance, never a neutral default: codexFactory's
global protected-surface constants are codexFactory's own instance, not the
canonical floor for any other tree. The floor predicate SHALL be
repository-parameterized — a per-tree floor input, tree-validated — and
instantiating it SHALL be a HARD, human-gated precondition sequenced BEFORE any
provenance-eligible class in a repository other than the floor's origin
repository, symmetric with how the machine-readable path-scope substrate is
sequenced.

Every source the verifier reads to establish or authorize a provenance tie
SHALL be a never-clearable floor member of EVERY enrolled repository —
specifically (i) the enrollment envelope (`.github/merge-approval-envelope.yml`),
(ii) the base-branch corroboration record, (iii) the tied OpenSpec change and
its Status/supersession state, (iv) the machine-readable path-scope
(`scope_globs`) substrate, and (v) the ratification-signing identity's
configuration and its invoking workflow. No autonomous provenance merge SHALL
write to any of these trust-root sources, so an earlier governed merge can never
author the input a later tie corroborates against — closing the
self-authorization recursion.

#### Scenario: A provenance class is judged by the shared floor walk
- **WHEN** a provenance-eligible class's allowlist is validated at definition time
- **THEN** it is judged by the same union-judged floor walk as any other class,
  and a class whose allowlist intersects a decision-core, gate, workflow,
  credential, governance, or council-record surface is refused

#### Scenario: Floor coverage is not yet instantiated for a repository
- **WHEN** an enrolling repository has not published a tree-validated floor
  covering its own sensitive surfaces
- **THEN** no non-docs-shaped provenance-eligible class may be published for it

#### Scenario: Primary enforcement is left implicit
- **WHEN** a realization admits a broad provenance-eligible class without stating
  whether the verifier or the definition-time predicate is the primary floor
  enforcement
- **THEN** the realization is incomplete and the class MUST NOT be published

#### Scenario: A repository lacks its own tree-validated floor or floors a trust-root source outside it
- **WHEN** a repository enables a non-docs provenance-eligible class WITHOUT its
  own tree-validated floor, OR with any trust-root source (i)–(v) outside that
  floor
- **THEN** the class is REFUSED at definition time

### Requirement: Full-pipeline-green successor and interim sunset
The provenance-completeness criterion SHALL be documented as INTERIM, with the
full-pipeline-green end state — the whole build governed and watched from the
proposal down, the whole pipeline green — named as its successor. The interim
criterion SHALL carry a SUNSET clause: it SHALL be retired by a NAMED successor
change raised on pilot evidence, and until that successor lands the interim
criterion governs. The exact evidence bar for supersession is deferred to that
successor and SHALL NOT be fixed by this requirement.

#### Scenario: The successor lands
- **WHEN** the named full-pipeline-green successor change is ratified
- **THEN** it supersedes the interim provenance-completeness criterion, which is
  retired

#### Scenario: No successor has landed
- **WHEN** no full-pipeline-green successor change has been ratified
- **THEN** the interim provenance-completeness criterion continues to govern, as
  a time-boxed regime rather than a permanent second lane
