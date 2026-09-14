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

### Requirement: An automated pin advance only ever proposes

An automated lane that advances this repository's pinned decision core MUST propose the advance as a pull request and MUST NOT dispose of it: it SHALL NOT merge, SHALL NOT approve, SHALL NOT push to this repository's default branch, and SHALL NOT hold any authority over the pin that the equivalent hand act does not already have.

The pull request SHALL move the pin and nothing else: no unrelated file, no documentation line, no formatting change, and no edit to the checks that judge it. This requirement composes with, and does not restate, the requirement "The mirror is inert until the pin carries the rule, and the pin moves as one act": that requirement governs WHAT one advance must contain, and this one governs who may author it and what else it may not contain.

#### Scenario: The lane opens a pull request and stops there
- **WHEN** the automated lane has a pin advance to deliver
- **THEN** it opens a pull request carrying that advance and takes no further action on it
- **AND** it neither merges nor approves that pull request

#### Scenario: The lane never writes to the default branch
- **WHEN** the automated lane has a pin advance to deliver
- **THEN** it delivers it on a branch and through a pull request
- **AND** it makes no direct write to this repository's default branch

#### Scenario: The advance carries nothing but the advance
- **WHEN** the automated lane's pull request is read
- **THEN** every changed file is one of the sites that name the pinned core commit
- **AND** no other file in the repository is changed by it

### Requirement: The automated pin advance refuses a decision-core commit the source repository's default branch does not carry

An automated pin advance MUST verify that the codexFactory commit it would pin is reachable from that repository's default branch, and MUST refuse and open nothing when it is not.

The verification SHALL be made against the source repository itself at run time and SHALL NOT be inferred from an event payload, a pull-request head, a tag, or any reference supplied by a caller. A pin at a commit that is not on the source repository's default branch becomes unresolvable the moment that branch is deleted, and this repository has already measured that failure on its own history. Where the source repository's default branch cannot be resolved, the lane SHALL refuse rather than pin at anything else. This requirement composes with, and does not restate, the requirement "The mirror is inert until the pin carries the rule, and the pin moves as one act".

#### Scenario: A commit not on the source default branch is refused
- **WHEN** the candidate core commit is not reachable from the source repository's default branch
- **THEN** the lane refuses, names the commit and the branch, and opens no pull request
- **AND** no site is changed

#### Scenario: The lane resolves the source default branch itself
- **WHEN** the automated lane runs
- **THEN** it resolves the source repository's default branch at run time and reads the candidate commit from that resolution
- **AND** it ignores any commit, branch or reference named by its trigger

#### Scenario: An unresolvable source default branch refuses
- **WHEN** the source repository's default branch cannot be resolved on a run
- **THEN** the lane refuses and opens no pull request
- **AND** it does not pin at any other reference

### Requirement: The automated pin advance moves every pinned site in one commit or opens nothing

An automated pin advance MUST write every site that names the pinned core commit in ONE commit, and MUST verify the result by RE-READING each site after writing rather than by trusting that its edits succeeded.

Where any site does not read the new core commit after the write, the lane SHALL discard the whole advance and open nothing; it SHALL NOT open a pull request carrying a partial advance for a reviewer to complete. This requirement composes with, and does not restate, the requirement "The mirror is inert until the pin carries the rule, and the pin moves as one act", which enumerates the sites and refuses a partial advance; what is added here is that an UNATTENDED author must prove the lockstep by measurement rather than assert it.

#### Scenario: All sites are re-read before anything is opened
- **WHEN** the lane has written the new core commit to every site
- **THEN** it re-reads each site from disk and requires each to equal the new core commit
- **AND** only then does it commit and open a pull request

#### Scenario: A site that did not move discards the run
- **WHEN** any site does not read the new core commit after the write
- **THEN** the lane discards the advance and opens no pull request
- **AND** it names the site that did not move

#### Scenario: One commit, not several
- **WHEN** the lane opens a pin advance
- **THEN** every site moves in a single commit
- **AND** no commit in the branch's history carries a partial advance

### Requirement: The automated advance re-copies the vendored snapshot and recomputes its witnesses from the bytes it wrote

An automated pin advance MUST obtain the vendored floor snapshot by COPYING the authoritative document from the source repository at the new core commit, and MUST compute the snapshot's declared digest and entry count from the bytes it actually wrote.

The lane SHALL NOT hand-edit, patch, or partially update the snapshot, and SHALL NOT carry the digest or the entry count forward from any report, pull-request body or message produced by the source repository: a witness restated from the party being witnessed is not a witness. Where the copy cannot be obtained, the lane SHALL refuse and open nothing rather than advance the other sites without it. This requirement composes with, and does not restate, the requirement "The grace changes what the lanes report and nothing they witness", which fixes the snapshot's status as a byte witness.

**MODIFIED BY `relocate-review-authority-floor-mirror` (2026-09-08) IN WHAT "OBTAIN" MEANS, AND IN NOTHING ELSE.** The copy, the byte-witness rule, the prohibition on carrying a digest forward and the refusal are all untouched. What changes is that the lane SHALL resolve the authoritative document through an ORDERED LIST of declared candidate paths in the source repository rather than through a single path, trying them in order and taking the FIRST one obtained; and the refusal SHALL fire only when EVERY candidate fails, naming every path tried. THE LIST EXISTS FOR ONE PURPOSE AND SHALL BE BOUNDED BY IT: a GOVERNED RELOCATION of the document in the source repository, which cannot be atomic across two repositories. So the list SHALL name the relocation that opened it, SHALL be ordered with the path in force FIRST so that adding a successor changes no behaviour on the day it lands, SHALL be returned to a single entry once one advance has been observed against the successor, and SHALL NOT be used to give the lane a standing choice of homes. A firing that resolves any entry but the FIRST SHALL say so in its report, so that a migration in progress is visible in the run and not only in the diff. THE LANE SHALL NOT SEARCH: it SHALL NOT locate the document by kind, by basename, by code search or by any other discovery, because a discovered file is one an author elsewhere can plant, and an explicit list that fails closed is what makes the read surface reviewable. The list SHALL be declared in the lane's own sources, and the lane SHALL NOT read it at run time from any artifact a check compares it against: a value read from the artifact it is used to check makes the check a tautology, and the agreement between the declarations SHALL instead be asserted. WHERE THE LIST IS ALSO DECLARED IN THE CREDENTIAL BINDING'S READ SURFACE — which this packet RECOMMENDS as decision M-4 and does NOT require, M-4 being put for veto with MQ-2 open — that declaration SHALL be covered by the same agreement assertion and SHALL likewise never be read at run time. A REQUIREMENT SHALL NOT MANDATE WHAT ITS OWN PACKET LEAVES OPEN: the mandate is the declaration in the lane's sources plus the run-time prohibition, the binding is an ADDITIONAL site, and vetoing M-4 removes a site without touching this requirement.

**Modified over `mirror-floor-regeneration-automation`'s addition by relocate-review-authority-floor-mirror (2026-09-08):** — the requirement this block restates is not in canon: it is ADDED by the ACTIVE change `mirror-floor-regeneration-automation`, which is ratified (2026-09-06, PR #708) but not yet archived, so the basis is a sibling's addition rather than a promoted specification. The pairing is declared here per requirement, as `govern-sibling-added-modified-deltas` requires, and the archive order follows from it: this packet SHALL NOT archive until that change promotes, which `.openspec.yaml`'s `related` entry and the `sequenced_after` front matter already record. THE SIBLING PACKET ON THE SAME PARENT IS DISJOINT FROM THIS ONE, and that was checked rather than assumed: `amend-mirror-floor-regeneration-merge-authority` (#807, ratified and landed 2026-09-08 at `6cc06288`) restates *An automated pin advance only ever proposes*; this packet restates the snapshot-copy requirement. Two requirements of one parent, one block each, so neither delta supersedes the other and no ordering between them is owed.

#### Scenario: The snapshot is copied, not edited
- **WHEN** the lane advances the pin
- **THEN** the vendored snapshot is a byte copy of the authoritative document at the new core commit
- **AND** no line of it is edited in place

#### Scenario: The witnesses are computed from what was written
- **WHEN** the lane declares the snapshot's digest and entry count
- **THEN** both are computed from the bytes the lane wrote to the snapshot file
- **AND** neither is taken from a message or report produced by the source repository

#### Scenario: A missing copy refuses the whole advance
- **WHEN** the authoritative document cannot be obtained at the new core commit from any declared candidate path
- **THEN** the lane refuses and opens no pull request
- **AND** the other sites are not advanced without it, and the refusal names every path it tried

#### Scenario: The first candidate resolves and nothing is different
- **WHEN** the document is obtained at the first declared candidate path
- **THEN** the advance proceeds exactly as it would with a single declared path
- **AND** the run reports no migration

#### Scenario: A later candidate resolves during a governed relocation
- **WHEN** the first declared candidate path does not resolve and a later one does
- **THEN** the advance proceeds from the document obtained there
- **AND** the run reports which candidate resolved and names the relocation the list declares

#### Scenario: The list is returned to one entry
- **WHEN** one advance has been observed against the successor path
- **THEN** the superseded entry is removed and the list carries one path again
- **AND** the lane has no standing choice of homes for the document

#### Scenario: The document is never discovered
- **WHEN** the document is absent from every declared candidate path but present elsewhere in the source repository
- **THEN** the lane refuses rather than finding it
- **AND** no search by kind, basename or code search is performed

#### Scenario: The declarations are asserted to agree
- **WHEN** the candidate list is declared in more than one place
- **THEN** a test asserts that every declaration carries the same ordered list
- **AND** no declaration is read at run time from the artifact a check compares it against

### Requirement: An automated pin advance is judged by the freshness checks that already exist, with no exemption

The checks that verify this repository's pinned-core consumption MUST judge an automated pin advance at exactly the strictness they judge a hand-authored one, and no exemption keyed on the pull request's author, branch, or automated origin SHALL be introduced.

Specifically: the coverage assertion over the floored surface, the negative controls that guard it, and the byte-for-byte comparison of the vendored snapshot against the pinned core SHALL apply unchanged; no skip, allowlist, relaxed assertion or adjusted expected-skip bookkeeping SHALL be added for the automated lane. An automated advance that fails any of them SHALL stay red and SHALL be repaired rather than exempted. This requirement composes with, and does not restate, the requirements "Both floor lanes apply the pinned decision core's completeness rule" and "The required assertion mirrors the rule and is falsified by the core's own vectors".

#### Scenario: The bot's pull request meets the same bar
- **WHEN** an automated pin advance is evaluated by the required suite
- **THEN** every assertion that would run on a hand-authored advance runs on it
- **AND** none of them is relaxed, skipped or bypassed on account of the author

#### Scenario: No author-keyed exemption exists
- **WHEN** the checks that judge a pin advance are read
- **THEN** none of them branches on the pull request's author, branch name or automated origin
- **AND** an exemption of that shape is a defect rather than a policy

#### Scenario: A failing automated advance is repaired, not waived
- **WHEN** an automated pin advance fails a freshness check
- **THEN** the advance stays red until the underlying disagreement is repaired
- **AND** it is not landed by weakening the check that caught it

### Requirement: The automated advance's pull request carries the witnesses its reviewer needs

An automated pin advance's pull request MUST state, in its own body, every value a reviewer would otherwise have to recompute, so that the human word that merges it is an informed one.

The body SHALL carry: the source-repository commit being pinned and how it was resolved, including the evidence that it is reachable from that repository's default branch; the pinned core commit before and after; the vendored snapshot's declared digest and entry count before and after; the floor's generated-block pin and entry count before and after; the count of covered-pending paths this advance is expected to clear; and a reference to the run that produced it. Every stated value SHALL be one another party can recompute from the two repositories and the named commits.

#### Scenario: The body states the before and after for every witness
- **WHEN** the lane opens a pin advance pull request
- **THEN** the body states the pinned core commit, the snapshot digest and the snapshot entry count both before and after
- **AND** it states the generated block's pin and entry count both before and after

#### Scenario: The landedness of the pinned commit is evidenced, not asserted
- **WHEN** the body names the source-repository commit being pinned
- **THEN** it states how that commit was resolved and how its reachability from the source default branch was verified
- **AND** a reviewer can repeat that verification

#### Scenario: A value only the lane could know does not appear
- **WHEN** the body is read
- **THEN** every value in it is recomputable from the two repositories at the named commits
- **AND** no claim rests on the lane's own report of what it did

### Requirement: The automated advance lane is triggered by the pinned core's own movement and every firing is idempotent

An automated pin advance lane MUST be reachable from the movement of the source repository's floor document and from a schedule, and every firing MUST be sweep-shaped: it re-measures the source repository's default branch, acts only when the pinned sites disagree with it, and otherwise reports a clean, named no-op.

The lane SHALL NOT depend on being notified by the source repository's own automation: a pin advance is owed whenever the floor document has moved, including when it moved by a hand act, so the sweep SHALL be sufficient on its own and any notification leg SHALL be an accelerator rather than the mechanism. At most one automated pin advance pull request SHALL be open at a time, and a firing that finds one open SHALL bring it up to date rather than open a second.

#### Scenario: Nothing to advance is a clean named no-op
- **WHEN** a firing finds every pinned site already equal to the source repository's default-branch commit for the floor document
- **THEN** the lane reports that nothing is owed and exits successfully
- **AND** it opens no pull request

#### Scenario: A hand-authored source change is picked up too
- **WHEN** the source repository's floor document moves by a hand act with no notification sent
- **THEN** the scheduled sweep still detects the disagreement and opens the advance
- **AND** the lane's correctness does not depend on the source repository's automation

#### Scenario: A second firing does not open a second pull request
- **WHEN** a firing occurs while an automated pin advance pull request is already open
- **THEN** the lane updates that pull request rather than opening another
- **AND** at most one automated pin advance pull request is open at any time

### Requirement: The automated advance lane runs under a declared credential binding and refuses rather than widening or degrading

An automated pin advance lane MUST run under a credential binding declared in this repository as a template carrying no live value, and MUST refuse to run when that binding does not resolve.

The binding SHALL name the consuming system that holds it, the identity it fetches with, and the least privilege the lane needs — read access to the source repository holding the decision core, and the ability to push a branch and open a pull request in this repository. The lane SHALL NOT fall back to any other identity when the binding is absent or unresolvable: an identity that cannot read the source repository would find no disagreement and report a clean no-op, converting a missing credential into a silent pass. An unresolvable binding SHALL be a loud failure. No raw credential value SHALL appear in this repository under any circumstance.

#### Scenario: A missing binding fails loudly
- **WHEN** the lane runs and its declared credential binding does not resolve
- **THEN** the run fails and names the unresolved binding
- **AND** it does not fall back to another identity and does not report a clean no-op

#### Scenario: The declared binding is a template
- **WHEN** the credential binding for the lane is declared in this repository
- **THEN** it is an instantiation template carrying placeholder references only
- **AND** no raw credential value appears in the repository

#### Scenario: The binding is least-privilege and says what it is for
- **WHEN** the binding is read
- **THEN** it names the consuming system, the identity, and the privileges the lane needs and no others
- **AND** it grants no write privilege over the source repository
