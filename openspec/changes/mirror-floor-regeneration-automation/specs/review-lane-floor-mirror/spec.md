## ADDED Requirements

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

#### Scenario: The snapshot is copied, not edited
- **WHEN** the lane advances the pin
- **THEN** the vendored snapshot is a byte copy of the authoritative document at the new core commit
- **AND** no line of it is edited in place

#### Scenario: The witnesses are computed from what was written
- **WHEN** the lane declares the snapshot's digest and entry count
- **THEN** both are computed from the bytes the lane wrote to the snapshot file
- **AND** neither is taken from a message or report produced by the source repository

#### Scenario: A missing copy refuses the whole advance
- **WHEN** the authoritative document cannot be obtained at the new core commit
- **THEN** the lane refuses and opens no pull request
- **AND** the other sites are not advanced without it

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
