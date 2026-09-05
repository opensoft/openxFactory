# review-lane-floor-mirror Specification

## Purpose

Keep the two lanes that measure this repository's review-authority floor
applying ONE completeness rule — the one the pinned decision core implements —
so that the REQUIRED coverage assertion inside `pytest-suite` and the ADVISORY
`merge-master-approval` report can never disagree about a path. Under that one
rule a pull request that CREATES a path under the floored prefix is reported
covered-pending and owes a floor regeneration AFTER it lands, instead of being
refused for creating the path the floor exists to protect; a removal, a rename,
a copy or a modification is graced by nothing; and an unresolvable base, merge
base or pin grants no grace at all, because an unresolvable pin is a reason to
refuse and never a reason to excuse.

## Requirements
### Requirement: Both floor lanes apply the pinned decision core's completeness rule

The REQUIRED coverage assertion and the ADVISORY reporting lane SHALL classify every tracked path under the floored prefix by the same completeness rule the pinned decision core implements, so that a path graced in one lane is graced in the other and a path refused in one is refused in the other.

Under that rule a tracked path under the floored prefix that is ABSENT from the floor is COVERED-PENDING when the candidate's own diff CREATES it — git change status `added`, relative to the candidate's base — or when it was ADDED TO THE BASE BRANCH after the commit the floor's generated block declares as `generated_at`; it is UNCOVERED otherwise. A removal, a rename, a copy and a modification SHALL NEVER be graced under any status. An EMPTY or DEGENERATE floored surface SHALL NEVER pass: a surface over which nothing is tracked is a verdict about nothing and is refused for that reason alone, and a prefix that names no surface at all is a caller error rather than a verdict about the candidate. A covered-pending path SHALL NOT be reported as floored, SHALL NOT be counted as a floor entry, and SHALL NOT be returned among the floor's matched paths.

#### Scenario: The candidate that promotes a capability creates its own spec path
- **WHEN** a candidate adds a tracked path under the floored prefix that the floor does not name, and its own diff creates that path
- **THEN** the required coverage assertion does not fail for that path
- **AND** the advisory lane reports it as covered-pending with the path named and counted
- **AND** neither lane adds the path to the floor's declared entries

#### Scenario: A bystander is not charged for somebody else's landed addition
- **WHEN** a candidate touches nothing under the floored prefix, and the base branch carries a path added after the floor block's `generated_at` that the floor does not name
- **THEN** both lanes report that path as covered-pending
- **AND** neither lane refuses the candidate on account of it

#### Scenario: A removal is refused in both lanes
- **WHEN** a candidate removes or renames a path the floor names
- **THEN** both lanes attribute the drift to that candidate and refuse
- **AND** no grace of any kind is applied to the removed or renamed name

#### Scenario: A surface that tracks nothing refuses rather than passing
- **WHEN** the floored prefix names a surface over which the evaluated tree tracks no path
- **THEN** the outcome is refused rather than reported clean
- **AND** the refusal states that the verdict was taken over an empty surface

#### Scenario: A disagreement between the two lanes is a defect
- **WHEN** the required assertion and the advisory lane return different verdicts about the same candidate and the same path
- **THEN** the divergence is a defect to be repaired at the causing commit
- **AND** it is not recorded as an intentional difference in strictness

### Requirement: The required assertion measures the candidate's own additions from the checkout it runs in

The required coverage assertion SHALL derive both the created-path set and the pin window from the repository checkout it runs in, using git reads alone, with no network call and no cross-repository fetch, so that it stays hermetic and stays inside the required suite it already runs in.

The created-path set SHALL be the adding changes between the merge base of the checkout's head and the base branch and that head, restricted to the floored prefix. The pin window SHALL be the adding changes between the commit the vendored floor snapshot's generated block declares as `generated_at` and the base branch tip, restricted to the same prefix. The measurement SHALL FAIL SAFE, and the fail-safe is the default rather than an exception: where the base branch does not resolve, where the merge base cannot be computed, where `generated_at` does not resolve, or where `generated_at` is not an ancestor of the base branch, the corresponding grace SHALL NOT be applied to any path, and an off-floor path SHALL be reported UNCOVERED exactly as it was before this change existed. An unresolvable base or pin is a reason to refuse, never a reason to excuse.

#### Scenario: A checkout without history grants no grace
- **WHEN** the assertion runs in a checkout whose base branch or whose merge base cannot be resolved
- **THEN** no path is graced by either half of the rule
- **AND** an off-floor path fails the assertion exactly as it did before this change

#### Scenario: A pin the base branch does not carry measures nothing
- **WHEN** the commit the snapshot's generated block declares as `generated_at` is not reachable from the base branch
- **THEN** the pin window is not measured and no path is graced by it
- **AND** the paths it would have graced are reported uncovered

#### Scenario: The creation is measured against the base, not against the working tree
- **WHEN** an off-floor path exists in the checkout but is present at the merge base with the base branch
- **THEN** it is not treated as created by this candidate
- **AND** it is graced only if the pin window carries it, and otherwise reported uncovered

#### Scenario: A run on the base branch itself has no candidate diff to read
- **WHEN** the assertion runs at a commit with no additions relative to the base branch
- **THEN** the created-path set is empty and grants nothing
- **AND** only the pin window can grace a path on that run

### Requirement: The required assertion mirrors the rule and is falsified by the core's own vectors

The required coverage assertion SHALL implement the completeness rule in this repository's own tree rather than by importing the pinned decision core, and SHALL be falsified by replaying the core's exported completeness vectors — both the accepted vectors and the refused ones — read from the pinned core checkout when that checkout is present.

The ground is the REQUIRED suite's own standing rule that a required check must not fail for a reason the candidate cannot fix: the pinned core checkout is deliberately non-fatal there, so an assertion that could not run without it would have to either skip — which is the blocking assertion silently ceasing to block — or fail on a cross-repository outage. The BLOCKING coverage assertion SHALL therefore remain computable OFFLINE, from the vendored floor snapshot and git alone, and SHALL NOT skip. The VECTOR REPLAY is the part that MAY skip when the pinned core is absent, and where it does, that skip SHALL be watched BY NAME in the required check's own report, in the same manner and for the same reason as the snapshot freshness comparison already is, with any exact skip pin moved in the same act. The ADVISORY lane, which already refuses to run at all when the pinned core is unreadable, SHALL IMPORT the core's completeness evaluation directly and SHALL NOT restate the rule.

#### Scenario: A cross-repository outage does not stop the required check from blocking
- **WHEN** the pinned core checkout fails on a run of the required suite
- **THEN** the coverage assertion still runs from the vendored snapshot and still refuses an uncovered path
- **AND** the vector replay skips rather than failing the candidate

#### Scenario: A skipped replay is visible by name
- **WHEN** the vector replay does not run and pass on a run of the required suite
- **THEN** the required check reports that fact against the replay's own name
- **AND** the failure states that the two lanes were not compared on that run

#### Scenario: A mirror that drifts from the core fails a vector
- **WHEN** the mirrored rule and the pinned core's evaluation disagree about any exported vector
- **THEN** the replay fails and names the vector
- **AND** the divergence surfaces as a failing test rather than as a contradictory verdict on a candidate

#### Scenario: The advisory lane does not re-derive the rule
- **WHEN** the advisory lane evaluates the floor's completeness
- **THEN** it calls the pinned core's evaluation
- **AND** it carries no second implementation of the classification

### Requirement: The advisory lane reports a graced path under its own named stage

The advisory lane MUST report covered-pending paths under a stage distinct from both the clean outcome and the uncovered-path refusal, naming every graced path, stating the count, and carrying the reason each path was graced, so that a reader or a machine consumer keying on the reported stage cannot mistake a graced path for a floored one.

The stage SHALL be `pending_floor_extension`, distinct from `floor_incomplete`, `floor_drift_caused_by_candidate` and `floor_partially_unreachable`. The meaning `refusals[0].stage` carries today SHALL be preserved: a graced path SHALL NOT displace a refusal, and the graced stage SHALL be reported only when nothing refuses. The lane's rendered verdict SHALL gain a row stating the pending count, and SHALL show the deterministic escalation state when the pinned core reports it. The lane's anti-vacuity assertion SHALL gain a POSITIVE assertion that the pending computation produced a result, in the same form its existing assertions take, so a computation that silently stopped running is distinguishable from one that found nothing.

#### Scenario: A graced run is reported, not refused
- **WHEN** every off-floor path in a run is covered-pending and nothing else refuses
- **THEN** the lane reports the stage `pending_floor_extension` with the paths named and counted
- **AND** the run is not refused and the owed regeneration is stated

#### Scenario: A grace never hides a refusal
- **WHEN** a run carries both a covered-pending addition and a candidate-caused removal
- **THEN** the run's stage is the removal's stage and the run is refused
- **AND** the pending paths are still reported, under their own stage, in their own list

#### Scenario: The escalation is shown when the core reports it
- **WHEN** the pinned core reports that the pending set has exceeded the tolerance the floor declares
- **THEN** the lane shows the escalated state with the count and the declared tolerance
- **AND** the run is refused as the core's evaluation refuses it

#### Scenario: The pending computation is proved to have run
- **WHEN** the lane's anti-vacuity assertion is evaluated
- **THEN** it asserts positively that the pending result exists
- **AND** a run that produced no pending result fails that assertion rather than passing silently

### Requirement: The advisory lane's base checkout carries the history the pin window needs

The advisory lane's checkout of the base tree SHALL carry enough history for the range from the floor block's `generated_at` to the base branch tip to be measurable, because that lane's checkout is shallow today and a shallow checkout cannot resolve the pin the window is measured from.

Where the history is nonetheless insufficient, the lane SHALL apply the fail-safe of the measurement requirement above — no pin-relative grace, the affected paths reported uncovered — and SHALL NOT invent, approximate or widen a window it could not measure. The depth SHALL be a DECLARED choice carrying its cost, whether taken as full history or as a targeted fetch of the base branch's history back to the pin; the required suite's own checkout already carries full history and needs no change.

#### Scenario: A base checkout with history resolves the pin
- **WHEN** the lane's base checkout carries the commit the block declares as `generated_at`
- **THEN** the window is measured and the pin-relative grace can apply
- **AND** the lane reports which pin the window was measured from

#### Scenario: A shallow base checkout grants no pin-relative grace
- **WHEN** the lane's base checkout does not carry the declared pin
- **THEN** no path is graced by the pin window
- **AND** the affected paths are reported uncovered rather than under a window the lane guessed

#### Scenario: The required suite's checkout is unchanged
- **WHEN** the required suite runs the coverage assertion
- **THEN** it measures the window from the full history its checkout already carries
- **AND** no change to that checkout's depth is required by this change

### Requirement: The mirror is inert until the pin carries the rule, and the pin moves as one act

Realization of this change SHALL NOT land before the pinned decision core has advanced to a codexFactory commit that carries the addition grace, because a mirror of a rule the pinned core does not implement is a divergence rather than a mirror.

The advance SHALL move every site that names the core commit in ONE act, and those sites are the pin file's `core_commit`, the advisory caller's pinned-commit constant, the advisory caller's checkout reference, the required suite's core checkout reference, and the vendored floor snapshot with its declared digest and entry count. Where the advance and the mirror land in one pull request, the advance SHALL be the earlier commit, so that no commit in the history carries a mirror of a rule its own pin does not yet have. AFTER the grace is in force, the first regeneration of the floor's generated block SHALL be performed at a LANDED commit of this repository — one reachable from its default branch — which is what the grace makes possible and which retires the measured defect that three of the last five declared pins are not ancestors of this repository's default branch.

#### Scenario: The mirror cannot precede the pin
- **WHEN** the mirrored rule is proposed to land while the pin still names a core without the grace
- **THEN** it is refused as a divergence
- **AND** the pin advance is the prior act

#### Scenario: A partial pin advance is refused
- **WHEN** an advance moves some but not all of the sites naming the core commit
- **THEN** the disagreement is refused by the checks that already compare them
- **AND** the advance is not recorded as complete

#### Scenario: The first regeneration after the grace pins at a landed commit
- **WHEN** the floor's generated block is regenerated after the grace is in force
- **THEN** its declared `generated_at` is reachable from this repository's default branch
- **AND** the regeneration follows the landing of the addition rather than preceding it

#### Scenario: The non-ancestor pin defect is retired rather than carried
- **WHEN** the first post-grace regeneration lands
- **THEN** the live pin that is not an ancestor of the default branch is replaced by one that is
- **AND** the fact that it was not an ancestor is recorded rather than tidied away

### Requirement: The grace changes what the lanes report and nothing they witness

The addition grace MUST leave unchanged every witness this repository holds over the floor, who may author the floor, what the floor matches, and what the negative controls prove.

Specifically: the vendored floor snapshot remains a BYTE WITNESS, its declared digest and entry count continue to read the floor's DECLARED ENTRIES, and the byte-for-byte comparison against the pinned core is untouched; the enumeration remains EXACT and a covered-pending path is not an entry and is not a match; the floor document's sole author is unchanged and no candidate in this repository gains any ability to add an entry to it; and the negative controls guarding the coverage assertion keep their meaning — a fabricated off-floor path that NO candidate diff creates and NO pin window carries SHALL still be refused, so the grace can never be read as making additions free.

#### Scenario: A fabricated off-floor path with no creating diff is still refused
- **WHEN** a path under the floored prefix is absent from the floor, is created by no candidate diff, and lies in no measured pin window
- **THEN** the coverage assertion refuses and names that path
- **AND** the grace does not apply to it

#### Scenario: The witnesses still count entries
- **WHEN** a covered-pending path exists and the snapshot's digest, its declared entry count and its freshness comparison are evaluated
- **THEN** each reads the floor's declared entries only
- **AND** none of them moves on account of the pending path

#### Scenario: Authorship is unchanged
- **WHEN** a candidate in this repository creates a path under the floored prefix
- **THEN** it gains no ability to add an entry to the floor
- **AND** the floor document remains authored only in the repository that owns it, by its generator

#### Scenario: The ordering guard still proves the shipped surface
- **WHEN** the negative controls run over the repository's real tree
- **THEN** the unmutated surface is proved to produce no uncovered path before any mutation is applied
- **AND** each control drives the same expression the coverage assertion drives

