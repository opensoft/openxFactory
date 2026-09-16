# release-realization Specification

## Purpose

Keep a promoted spec a description of what the code actually does, by
putting a realization axis on every change. Require each proposal to
declare `code_surface:` and `target_release:`, and hold a code-surface
change active as approved-but-unrealized intent until its code is merged
on the implemented target and — where the surface runs — has run green,
with a deployment onto another factory's managed subject citing the
completed handoff request by correlation identifier. Name how a ratified
change reaches engineering: the decomposition scale rule, deltas ordered
against an earlier active change's outcome, and the three branch kinds
as distinct vocabulary. Govern what the archive gate must still find
intact — accepted claims represented in the packet rather than left in
supporting documents, an unmutated origin declaration, pins re-derived
by the landing whose rewrite orphans them, and a pinned corpus
measurement carried one row per subject rather than as a contended
shared total.

## Requirements

### Requirement: Realization axis declaration
Every OpenSpec change proposal SHALL declare `code_surface:` — `none` or
the repositories whose runtime artifacts it changes — and
`target_release:` — `implemented` (the affected repositories' main lines)
or a named release defined in the aggregation repository. A proposal
without the declarations is a doc-only change (`code_surface: none`,
`target_release: implemented`) by default.

#### Scenario: A doc-only change is proposed
- **WHEN** a change alters only governance documents, schemas-as-documents, or contract prose
- **THEN** its code_surface is `none` and it archives when its artifacts land, as before

#### Scenario: A code-surface change is proposed
- **WHEN** a change alters scripts, workflows, services, or other runtime artifacts
- **THEN** its proposal MUST declare the affected repositories as code_surface and its target release

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

### Requirement: Decomposition scale rule
A ratified code-surface change SHALL be an admitted engineering intent
record for the owning domain's intake. Changes whose tasks are executable
directly MAY realize through their own task list; multi-feature changes
SHALL go through feature decomposition into Spec Kit feats; changes
targeting a batched release SHALL decompose late, from the release delta
against the implemented target at release-merge time.

#### Scenario: A small change realizes
- **WHEN** a ratified change's tasks are individually executable without a feature DAG
- **THEN** executing the tasks through the engineering gates satisfies decomposition

#### Scenario: A batched release becomes ready
- **WHEN** a release branch is ready to merge into the implemented line
- **THEN** the feats to implement are decomposed from the delta between the release and the implemented target

### Requirement: Ordered deltas and branch vocabulary
Changes SHALL sequence explicitly: a proposal modifying a requirement
already modified by an active ratified change references that change and
declares its deltas relative to that change's outcome. The three branch
kinds SHALL be used as distinct vocabulary: the change folder (content
branch), Spec Kit feature branches, and release branches (integration);
releases are branches while open and tags at promotion.

**THE ANTECEDENT REACHES A REQUIREMENT AN ACTIVE RATIFIED CHANGE ADDS OR RENAMES
TO, AND NOT ONLY ONE IT MODIFIES.** A proposal MODIFYING a requirement that an
active ratified change ADDS, or that such a change RENAMES a promoted
requirement TO — in either case a title the promoted specification does not yet
carry — SHALL reference that change and declare its deltas relative to that
change's outcome, on the same terms and for the same reason as the
already-modified case: whichever writer archives last is the text canon keeps.
The two antecedents are DISJOINT by construction, a requirement being either
one canon carries or one it does not, so this reaches a shape the
already-modified antecedent cannot and widens that antecedent in no way.

**A RENAME IS A BASIS ON THE SAME TERMS AS AN ADDITION, AND THE COROLLARY IS
THAT IT IS ONE EVERYWHERE OR NOWHERE.** `doc-health`'s promoted resolution rule
already resolves a MODIFIED title against "a requirement an active sibling change
ADDS or RENAMES" (`openspec/specs/doc-health/spec.md:1568-1574`, with the
scenario at `:1783-1786` reading a rename by the title it renames TO), and
`document-lifecycle`'s marker is owed wherever "an active change ADDS or RENAMES
to that title". A rule that took a rename as a basis for the DECLARATION and not
for the ORDER would leave the identical hazard — an unpromoted title two active
changes write, whichever archives last being the text canon keeps — governed in
one capability and ungoverned in the next. What differs between an addition and a
rename is where the requirement's TEXT comes from, not who may archive first, and
the ordering obligation is about the archives.

**THE ORDER OF THE TWO ARCHIVE ACTS IS PART OF THE OBLIGATION, because in this
shape one order is safe and the other destroys review.** A change carrying a
`## MODIFIED Requirements` block for a requirement the promoted specification
does not carry SHALL NOT archive while that requirement is unpromoted, wherever
an ACTIVE change ADDS it or RENAMES a promoted requirement TO its title. The
BASIS change — the one that ADDS the requirement, or that RENAMES a promoted
requirement to its title — archives first, the requirement enters canon under
that title, and the modifying
block is then a block over canon like any other. In the other order the
modifying block promotes a requirement nobody reviewed as an addition or as a
rename, and the basis change is left holding, for a title canon already carries,
either an `## ADDED Requirements` block or a `## RENAMED Requirements` block
whose `TO:` title canon now carries. **THE DIRECTION IS PART OF THE STATEMENT IN
THE RENAME CASE**: the collision is in the NEW title, the `TO:` half, the `FROM:`
half naming the requirement the rename moves away from and which canon may still
carry. This obligation is the RULE the per-packet pre-archive
assertions in individual proposals have been standing in for — BOTH the `grep`
that reads canon for the title AND the CONVERSION CLAUSE some of those packets
carry beside it, which the conversion paragraph below states generally rather
than leaving to be re-derived one packet at a time. Those assertions remain
useful as local evidence and SHALL NOT be read as the source of the obligation,
and a general rule that reached less than the per-packet text it replaces would
be a narrowing wearing a generalization's label.

**THE HOLD KEYS ON THE UNPROMOTED TITLE AND NOT ON THE BASIS'S STANDING, and the
two halves of this obligation are keyed apart on purpose.** The
REFERENCE-AND-DECLARE half above names an active RATIFIED change because what it
asks for is deltas declared relative to an OUTCOME, and a packet no authority has
accepted has no outcome to declare against. The ARCHIVE half asks something else
entirely: that no requirement enter canon through a block written over text canon
does not carry. That loss does not soften when the basis is a draft — it is
WORSE, the text promoted being one no authority accepted at all, arriving by an
order that reviewed it as neither an addition nor a rename. So the hold reaches a
basis of ANY STANDING: while an active change ADDS the title or RENAMES a
promoted requirement TO it, the modifying change SHALL NOT archive, and where
that basis is unratified it SHALL RATIFY AND ARCHIVE before the modifying
change's archive gate opens. The hold ends in exactly three ways and no fourth —
the basis ratifies and archives and the requirement enters canon; the pairing is
converted by the PAIRED act the clause below defines, on that clause's own terms
— its ruling being the ratifying authority's, which for a basis not yet ratified
is the authority that WOULD rule it, one ruling still amending both packets; or
the modifying block is withdrawn. **AND `document-lifecycle`'s DISCLOSURE IS
THE READER'S WARNING, NOT THIS GATE'S CONSENT.** That capability requires a
marker naming an unratified basis to say so in its reason clause; a marker that
does is a marker in good order, and a block in good order is not thereby
archivable. Writing the word `unratified` SHALL NOT be read as lifting this hold,
a pairing being lawfully declared and unarchivable at the same time — two
questions about one pairing, answered in two capabilities.

**CONVERTING THE BLOCK TO `## ADDED` DOES NOT DISSOLVE THE OBLIGATION, because
the antecedent attaches to the PAIRING and not to the block's form.** Re-shaping
a `## MODIFIED Requirements` block written over an active ratified change's
addition — or over its rename to the title — into an `## ADDED Requirements`
block leaves two changes writing one
requirement — a worse state than the one it escapes, the ordering question being
unresolved and no longer declared anywhere. Conversion is therefore lawful ONLY
AS A PAIRED ACT ruled by the authority that ratified the two packets: ONE ruling
amends BOTH, the BASIS change striking or re-scoping its addition or its rename,
and the converting block RETAINING the `Modified over` marker it carried, as provenance,
so that the pairing stays declared after the block's form changes. That retention
is a retention and not a new marker obligation: `document-lifecycle` scopes the
form's REQUIREMENT to `## MODIFIED Requirements` blocks and this widens that
scope in no way. An UNPAIRED conversion SHALL NOT be taken.
Where one is taken it is a breach, and the evidence it leaves is the shape this
rule's mechanical backstop reads: before either archives, two active changes
writing one title; after the converting change archives, an active block still
writing that title into canon — an `## ADDED Requirements` block for a title
canon now carries, or a `## RENAMED Requirements` block whose `TO:` title canon
now carries.

**LANDED REALITY CAN FALSIFY THE ADDING CHANGE'S SCENARIO BEFORE ITS ARCHIVE, and
the archive order is not the escape from that.** The safe order holds the adding
change open while the repository moves under it, so a cut contract, a merged
realization or a promoted specification may falsify a scenario of the unpromoted
`## ADDED` block that the archive would then promote. Where that happens the
ADDING change SHALL amend the falsified scenario BEFORE it archives, by the route
a ratified packet's amendments take and with its owner consenting. The ordering
obligation above is UNCHANGED by the falsification, and falsification is never
itself licence to invert the order or to convert the block: promoting a scenario
the repository's own landed state contradicts is the loss this rule exists to
prevent, arriving through the safe order instead of the unsafe one.

**A RENAMING BASIS RAISES THIS CLAUSE ONLY THROUGH WHAT IT AMENDS.** A
`## RENAMED Requirements` block carries a pair of titles and no scenarios of its
own — the requirement's scenarios are canon's, under the OLD title — so what
landed reality can falsify in a renaming basis is whatever that change MODIFIES
beside the rename, on the terms this clause already states, and nothing in the
rename itself. The clause is therefore neither widened to a shape that has no
scenarios to falsify nor left ambiguous about which basis form it reaches.

#### Scenario: Two changes touch one requirement
- **WHEN** a proposal modifies a requirement that an active ratified change already modifies
- **THEN** the later proposal MUST reference the earlier change and declare its deltas relative to that change's outcome

#### Scenario: A release promotes
- **WHEN** a release branch merges to the implemented line and realization completes for its changes
- **THEN** the release is tagged and the branch is retired

#### Scenario: A proposal modifies a requirement an active ratified change adds or renames to
- **WHEN** a proposal carries a `## MODIFIED Requirements` block for a requirement the promoted specification does not carry, and an active ratified change ADDS that requirement or RENAMES a promoted requirement TO that title
- **THEN** that proposal MUST reference the basis change and declare its deltas relative to that change's outcome, exactly as it must where the earlier writer MODIFIES
- **AND** the already-modified antecedent MUST NOT be cited as the authority for this shape, its antecedent naming a requirement canon carries and this one naming a requirement canon does not
- **AND** a RENAMING basis MUST be treated on the same terms as an ADDING one, the hazard being the order of the two archives rather than the form the basis wears

#### Scenario: The modifying change reaches its archive gate first
- **WHEN** a change carrying such a block reaches its archive gate while the requirement it modifies is still unpromoted
- **THEN** it MUST NOT archive, the basis change — adding or renaming — archiving first
- **AND** a local pre-archive assertion in that change's own task list MUST NOT be treated as the source of the obligation, being evidence that this rule was met rather than the rule

#### Scenario: The basis is not ratified and the modifying change reaches its archive gate
- **WHEN** a change carrying such a block reaches its archive gate while the requirement it modifies is unpromoted, and the active change that ADDS that requirement — or RENAMES a promoted requirement TO its title — is not ratified
- **THEN** it MUST NOT archive, this hold keying on the unpromoted title rather than on the basis's standing, and that basis MUST ratify AND archive before the gate opens
- **AND** a `Modified over` marker disclosing that the basis is unratified MUST NOT be read as lifting the hold, the disclosure being the reader's warning that no authority has accepted the text rather than a consent to promote it
- **AND** the only other ways out MUST be the paired conversion this requirement defines — one ruling of the authority that would rule both packets, amending both — and the withdrawal of the modifying block, an unratified basis admitting no route a ratified one does not

#### Scenario: The modifying change converts its block rather than waiting
- **WHEN** a change carrying such a block re-shapes it into an `## ADDED Requirements` block instead of waiting for the basis change — adding or renaming — to archive
- **THEN** the conversion MUST NOT be treated as discharging this obligation, its antecedent attaching to the pairing of the two changes and not to the form of either block
- **AND** the conversion MUST be a PAIRED act ruled by the authority that ratified both packets, one ruling amending both so that the basis change strikes or re-scopes its addition or its rename and the converting block retains the `Modified over` marker it carried as provenance
- **AND** an unpaired conversion MUST NOT be taken, and where one is taken the addition — or the rename's `TO:` title — left standing for a title canon then carries is the surviving evidence of the breach

#### Scenario: Landed reality falsifies the adding change's scenario before its archive
- **WHEN** the repository's landed state — a cut contract release, a merged realization, a promoted specification — contradicts a scenario of the `## ADDED Requirements` block a modifying change is waiting on
- **THEN** the adding change MUST amend that scenario before it archives, by the amendment route a ratified packet takes and with its owner consenting
- **AND** the archive order MUST still hold, the falsification being neither licence to invert it nor licence to convert the modifying block

#### Scenario: The basis change renames a promoted requirement to the title
- **WHEN** a proposal carries a `## MODIFIED Requirements` block for a title the promoted specification does not carry, and an active ratified change's `## RENAMED Requirements` block renames a promoted requirement TO that title
- **THEN** that proposal MUST reference the renaming change, declare its deltas relative to that change's outcome, and MUST NOT archive while the title is unpromoted, on the same terms as it must where the basis ADDS
- **AND** the collision the unsafe order leaves MUST be read in the NEW title — the `TO:` half canon then carries — the `FROM:` half naming the requirement the rename moves away from
- **AND** the falsified-scenario clause MUST NOT be read as reaching the rename itself, a `## RENAMED Requirements` block carrying a pair of titles and no scenarios of its own

### Requirement: Proposal support archive gate
An OpenSpec change with proposal supporting documents SHALL NOT archive until
all accepted normative claims have been represented in its proposal, design, or
spec delta; any proposal hybrid has completed its final source import; strict
validation passes; and the supporting folder has been converted into a
deterministic bundle with a readable, verifiable manifest. Packaging SHALL wrap
the normal OpenSpec archive operation rather than replace spec promotion.

#### Scenario: Supporting material contains uncaptured accepted claims
- **WHEN** accepted normative content exists only in `supporting-docs/`
- **THEN** the change MUST remain active until that content is represented in the proposal, design, or spec delta

#### Scenario: Archive preflight succeeds
- **WHEN** implementation and repository tests pass, strict OpenSpec validation passes, final source returns complete, and the support bundle verifies
- **THEN** the normal OpenSpec archive operation MAY run
- **AND** canonical spec promotion MUST proceed unchanged

### Requirement: Origin retention at archive
The archive gate SHALL verify that a change's `.openspec.yaml` still carries
its original origin declaration unchanged. For staged origins, the
compressed supporting-document manifest SHALL retain the same origin id and
path; for ad-hoc origins, the archived change SHALL retain the reason and
approval provenance even when no support bundle exists. Mutation of an
origin declaration after ratification SHALL be rejected at the archive gate.

THE DECLARATION PRESENT AT RATIFICATION IS FOUND UNDER THE IDENTITY THE PACKET
WAS RATIFIED UNDER, WHICH IS NOT ALWAYS THE IDENTITY IT CARRIES NOW. Where the
packet declares a former identity, the gate SHALL resolve the ratifying commit
across the current identity and every declared former identity together, and
SHALL take the EARLIEST commit at which any of them declares `Status:
ratified`. Earliest is the whole of it: the failure this requirement exists to
catch is a baseline LATER than the real ratification, which waves through every
mutation made in between, so a resolution that could return a later commit than
some identity of the same packet offers would reintroduce the defect by another
route.

THE RESOLUTION IS BY IDENTITY AND NEVER BY HISTORY. Each identity is resolved
to the path it occupies at the commit being read, the way this estate already
locates a packet at a ref — the active location, or the dated archive
directory that carries the same id — and the gate SHALL NOT infer an identity
from rename detection, from similarity between two packets, or from any walk
over a lineage. An identity the packet has not declared is not an identity of
that packet, whatever history suggests.

AND THE COMPARISON ITSELF DOES NOT MOVE. A declared former identity changes
WHERE the baseline declaration is read and changes nothing about what is then
required of it: the origin block of the packet being archived must equal the
declaration at that baseline exactly, the support manifest's repeated origin
fields are measured against the same declaration, and an accepted mutation
still takes the explicit disposition this requirement's own scenario names. A
rename SHALL NOT be a way to acquire a later baseline, and therefore SHALL NOT
be a way to launder a mutation.

EVERY READ BEHIND THE BASELINE SHALL FAIL CLOSED, AND ABSENT SHALL BE
DISTINGUISHED FROM UNREADABLE. A checkout that cannot read the history holding
the baseline answers "there is nothing there" and "I cannot tell you" with the
same silence, and a gate that reads the second as the first is a gate that
switches itself off exactly where it can prove nothing. So the gate SHALL
establish whether a path is PRESENT at a commit from the tree, SHALL treat a
read it could not perform as a refusal — CANNOT RUN, naming the read that
failed and the identity it was for — and SHALL NOT report an unreadable
history as an unratified one. An EXISTING probe that collapses the two SHALL
NOT be reused for this read merely because it already resolves a packet by id.

AND AN IDENTITY THAT RESOLVES TO MORE THAN ONE PATH AT A COMMIT SHALL REFUSE
RATHER THAN CHOOSE. Where the current id or a declared former id matches more
than one candidate location in the tree being read, the gate SHALL refuse as
CANNOT RUN naming the candidates, on the same ground the estate's own
archived-directory lookup already states: two archive dates for one id is an
ambiguity to report, not a collision to resolve by taking one.

#### Scenario: A staged-origin change archives
- **WHEN** a change with a staged origin reaches its archive gate
- **THEN** the archived `.openspec.yaml` and the readable support manifest MUST carry the identical origin id and path declared at creation

#### Scenario: An ad-hoc change without a support bundle archives
- **WHEN** a change with an ad-hoc origin and no supporting documents reaches its archive gate
- **THEN** the archived packet MUST retain the origin's reason, approving authority, and approval date

#### Scenario: An origin was mutated after ratification
- **WHEN** the archive gate finds the origin declaration differs from the declaration present at ratification
- **THEN** the archive MUST fail
- **AND** restoring or accepting the mutation is a contested-class act requiring an explicit disposition

#### Scenario: A packet that declares a former identity reaches its archive gate
- **WHEN** a change declares a former identity and a commit under that identity declares `Status: ratified` earlier than any commit under the identity the packet carries now
- **THEN** the declaration present at that earlier commit MUST be the baseline
- **AND** the packet's current origin block and its support manifest MUST be measured against that declaration on the same terms as any other packet

#### Scenario: A mutation rides in the commit that renamed the packet
- **WHEN** a declared move also edits the origin declaration, so the packet's origin differs from the declaration at the baseline the declared former identity resolves
- **THEN** the archive MUST fail as an origin mutated after ratification
- **AND** the move having been lawfully declared MUST NOT be read as accepting the mutation

#### Scenario: The history holding the baseline cannot be read
- **WHEN** the gate cannot perform a read it needs to resolve the baseline — the tree says a path is present at a commit and the checkout cannot produce what stands there
- **THEN** the gate MUST refuse as CANNOT RUN, naming the read that failed
- **AND** it MUST NOT report the packet as unratified, and MUST NOT establish a baseline from the reads that did succeed

#### Scenario: A declared identity resolves to two locations at one commit
- **WHEN** the current id or a declared former id matches more than one candidate location in the tree being read
- **THEN** the gate MUST refuse as CANNOT RUN, naming the candidates
- **AND** it MUST NOT resolve the ambiguity by preferring one of them

### Requirement: A history-rewriting landing re-derives the pins its rewrite orphans
A history-rewriting landing SHALL re-derive or re-pin every committed artifact
whose derivation pin names a commit that landing orphans, as part of the landing
itself, and MUST NOT move a pin by hand without regenerating the artifact the
pin describes. A history-rewriting landing is one that lands a branch by rebase,
squash, amend, or force-update.

The obligation belongs to the LANDING and not to a later sweep, and the reason
is mechanical rather than stylistic. Before the rewrite, the pinned commit is
reachable and the artifact can be regenerated from it, so the equivalence
between old pin and new pin is measurable. After the rewrite, the old commit may
be reachable from nothing, and the very state a regeneration would read is gone.
A rule that says "fix it afterwards" therefore describes a repair that may no
longer be performable, which is why this reads as a landing obligation and why
the check that discharges it belongs on the branch rather than on `main`.

RE-PINNING IS DEFINED BY REPRODUCTION, not by the pin's value. Where the
artifact's own tooling defines how the artifact is derived — the cross-reference
derivation and its strict index validator are this repository's worked example —
the re-pin SHALL reproduce the committed body BYTE-FOR-BYTE at the new pin, and
the landing SHALL record that it ran the reproduction rather than asserting the
equivalence. Where no tool defines reproduction, the re-pin SHALL name the
measurement that established equivalence at the new pin, or the artifact SHALL
be regenerated so that the question does not arise. A pin edited to a value that
happens to be reachable, with no reproduction and no measurement, satisfies
nothing: it converts an unverifiable claim into a plausible one, which is worse,
because the next reader has no signal that the claim was never checked.

The rewrite's own commits are not the only pins in question. A landing SHALL
consider every artifact its branch touched AND every artifact already on `main`
whose pin names a commit the rewrite orphans, because a branch can orphan a
commit that a previously landed artifact pins without touching that artifact's
file at all.

Where a landing completes and leaves an orphaned pin behind, accepting it SHALL
be a contested-class act requiring an explicit disposition, and the repair route
SHALL be the one the pinned artifact's own class allows rather than whichever is
convenient.

#### Scenario: A branch whose commits are pinned lands rebased
- **WHEN** a branch is landed by rebase or squash, and a committed artifact pins one of the commits that landing rewrites
- **THEN** the landing MUST re-derive or re-pin that artifact as part of itself, before the rewritten commits become unreachable
- **AND** the landing MUST NOT be treated as complete while the artifact still names an orphaned commit

#### Scenario: A pin is moved by hand without regeneration
- **WHEN** a pin is edited to a new commit and the artifact's body is not regenerated at that commit
- **THEN** the reproduction obligation MUST reject the re-pin, because reproduction was neither run nor recorded
- **AND** the pin's reachability MUST NOT be accepted as evidence that the body matches the state it now claims

#### Scenario: The rewrite orphans no pinned commit
- **WHEN** a landing rewrites history and no committed artifact pins any commit the rewrite orphans
- **THEN** no re-derivation is owed and the landing proceeds unchanged
- **AND** the absence MUST be established by looking, not assumed from the branch's file list

#### Scenario: A landing completes with an orphaned pin on main
- **WHEN** a landing has completed and an artifact on `main` names a commit no ref reaches
- **THEN** accepting that state MUST be a contested-class act carrying an explicit disposition
- **AND** the repair MUST follow the route the artifact's own class allows, which for captured evidence is retention of the commit rather than an edit to the pin

### Requirement: A pinned corpus measurement is carried per subject, never as a shared total
A corpus measurement that a committed check PINS SHALL be carried as ONE ROW PER
MEASURED SUBJECT, and every total a check asserts SHALL be DERIVED from those
rows rather than asserted as a literal. A total is a shared mutable that every
contributor writes: two changes moving two different subjects' readings edit the
same line, cannot be auto-merged, and serialize on each other for one continuous
integration window per round — a cost paid by whichever lands second, repeatedly,
and paid for bookkeeping rather than for any disagreement about the corpus.

THE ROW IS THE UNIT OF THE PIN. A row SHALL record what the measurement reads
ABOUT ITS OWN SUBJECT and SHALL record, as provenance, the pull request that
last moved it and the date. Rows SHALL be ordered deterministically by subject
identity, so that two subjects entering the corpus insert at two positions
rather than at one growing tail. A change SHALL move its own row, and SHALL move
another subject's row in the SAME COMMIT when its own delta is what moved that
subject's reading — a partner flipping class because of this change's delta is
this change's move to make, not a drift for a later sweep to find.

THE DERIVATION SHALL BE CROSS-CHECKED AGAINST THE MEASUREMENT IT PINS, by a
computation independent of it, and the two SHALL be compared FIELD BY FIELD with
the field and both values named on a disagreement. A derivation refactored out of
the measurement it checks agrees with itself by construction and proves nothing;
naming only that "something moved" tells an author to re-derive a total to find
out what, which is the cost this requirement exists to remove.

EVERY FAILURE SHALL NAME THE SUBJECT. A row absent for a subject in the corpus, a
row for a subject that is not, a row whose recorded value differs from the live
reading, and rows out of order SHALL each be reported naming the subject — and,
for a differing value, naming the key with the recorded value beside the live
one.

A VERIFICATION OR RECORD FILE SHALL CITE ITS OWN SUBJECT'S ROW AND THE
CONSISTENCY OF THE LEDGER WITH THE CORPUS AT A NAMED COMMIT, and SHALL NOT cite a
corpus-wide total. A total moves whenever any other contributor lands, so a
record quoting one owes re-derivation on every merge from the main line, for a
number that was never that record's claim.

THE NAMED COMMIT SHALL BE ONE AT WHICH THE CONSISTENCY CHECK WAS ACTUALLY RUN
AND PASSED, and SHALL NOT be a seeding or creation stamp the ledger happens to
carry. A stamp recording where a file came from is preserved as history and goes
further out of date with every landing; citing it would name a commit at which
the ledger is provably INCONSISTENT, while reading as though it had been
checked.

A DATED HAND-WRITTEN NARRATIVE SHALL BE KEPT IN EXACTLY ONE PLACE and SHALL be
appended only where a move is NOT explained by the row diff itself — a change to
the counting method, a subject whose reading moved because of another subject's
delta, a reading that is not per-subject, or a re-seeding of the ledger. Where
the row diff states the move, no entry is owed, and generating the narrative from
the diff is not permitted: a narrative that restates what the diff already says
is noise that hides the entries that carry judgement.

#### Scenario: Two changes move two different subjects' readings
- **WHEN** two changes in flight each move only their own subject's row, and their rows are not adjacent in the ordering
- **THEN** each edits its own row and the two merge without a textual conflict
- **AND** neither is required to re-derive a total the other moved

#### Scenario: Two new subjects sort adjacently
- **WHEN** two changes each ADD a row and their identities sort with no existing row between them
- **THEN** they share one insertion point and MAY still conflict, which the ordering reduces rather than removes
- **AND** that residue MUST be resolved by the repository's landing convention rather than by re-deriving a total

#### Scenario: A change flips another subject's reading
- **WHEN** a change's own delta is what moves another subject's recorded reading
- **THEN** it MUST move that subject's row in the same commit as its own
- **AND** the check's failure MUST name both subjects rather than report a moved total

#### Scenario: The ledger disagrees with the corpus
- **WHEN** a row is missing, extra, or differs from the live reading
- **THEN** the check MUST fail naming the subject, and for a differing value the key with the recorded value beside the live one
- **AND** the derived totals MUST be compared field by field against the independent measurement, naming any field that disagrees

#### Scenario: A record cites the measurement
- **WHEN** a verification or record file cites the corpus measurement
- **THEN** it MUST cite its own subject's row and the ledger's consistency with the corpus at a named commit
- **AND** it MUST NOT cite a corpus-wide total

#### Scenario: A move the row diff already explains
- **WHEN** a change's move is fully stated by the row diff
- **THEN** no narrative entry is owed
- **AND** where a move is NOT so explained — a counting-method change, a partner's flip, a non-per-subject reading, or a re-seeding — a dated entry in the single narrative is owed

### Requirement: Equivalent declaration sites for the ordered-delta parent declaration
A `sequenced_after:` declaration written as a LIFECYCLE HEADER LINE SHALL
declare exactly what the same declaration written in the `---`-fenced
realization-axis front matter declares, and the two sites SHALL be read by ONE
loader under ONE shape, ONE entry grammar, ONE resolution rule, ONE cycle rule
and ONE retention rule. Neither site is preferred and neither is a fallback of
lesser standing: a corpus whose proposals carry no fence is not a corpus whose
authors declared nothing.

A LIFECYCLE HEADER LINE IS A BOUNDED CONSTRUCT, AND THE BOUND IS THE
REQUIREMENT'S SUBSTANCE. It is a line whose first characters are the field's own
name followed by a colon, at column 0, case-sensitively, sitting within the
document's BOUNDED LIFECYCLE HEADER WINDOW — the same window, counted in the same
REAL LINES (CR, LF and CRLF only), that this corpus already reads a document's
`Status:` header in — and outside any leading `---` fence, whose lines are read
by the front-matter reader and MUST NOT be counted a second time as header lines
of the same document. BEYOND THAT WINDOW THE SAME BYTES ARE PROSE AND SHALL
DECLARE NOTHING. The bound is what front matter was chosen FOR: the alternative
it refused was unbounded prose parsing, in which a `sequenced_after:` written in
a body paragraph would authorize as loudly as one written in a header, and this
capability already refuses a mention as a parent link. An INDENTED line is a
continuation of what precedes it and SHALL NOT declare. The legacy free-text
`Sequenced-after:` header SHALL continue to declare nothing and SHALL continue
to be counted as the prose header it is.

A LEADING FENCE'S OWN LINES COUNT TOWARD THE WINDOW'S BUDGET, AND DO NOT BUY IT
A FRESH ONE. The window is counted from the document's own line 1: the `---`
that opens a leading fence, every line between it and the closing `---`, and
the closing `---` itself are REAL LINES of the document like any other and
SHALL be counted among the window's lines exactly as any other line is, even
though those same lines — already read once by the front-matter reader — are
excluded from being read AGAIN as a header-line declaration site. The window
SHALL NOT be re-measured as though it began fresh after the fence closes: a
header-line declaration MUST sit within the window counted from line 1
inclusive of the fence, so a fence occupying part of the window leaves
correspondingly FEWER lines available inside it for a header-line declaration,
and one long enough MAY leave none at all.

THE HEADER-LINE FORM IS A SINGLE LINE, because an unfenced document supplies no
closing delimiter: a multi-line value has no defined end, and a window boundary
falling inside one would show a reader one declaration and authorize another. A
self-delimiting flow sequence on the line SHALL be the admitted form; a
valueless field line followed by an indented continuation SHALL be refused BY
NAME, naming the forms that work, rather than read as null. A field line with no
value and no continuation SHALL be PRESENT-but-null and SHALL be refused by the
field's own shape validation, never read as absence — presence is decided by the
KEY on both sites.

THIS EQUIVALENCE IS GRANTED TO THE PARENT DECLARATION ALONE. The structured
path-scope declaration `scope_globs:` SHALL NOT be declarable as a header line.
The asymmetry is deliberate: `sequenced_after:` declares WHERE IN A CHAIN a
change sits, and every consumer applies its own root proof, co-modifier
cross-check and refusals on top, so making an author's existing declaration
legible authorizes nothing that absence did not already refuse; `scope_globs:`
declares WHICH PATHS an autonomous merge MAY WRITE, and a second place to
declare it is a second place to widen a path grant. Reading a position is not
granting a path.

#### Scenario: An unfenced proposal declares its parent as a header line
- **WHEN** a proposal carries no `---` front matter and writes `sequenced_after:` with a flow sequence at column 0 within the lifecycle header window
- **THEN** the declaration is read, and it is the same declaration the fenced form would have made
- **AND** it is validated, resolved, cycle-checked and freeze-checked by exactly the machinery the fenced form goes through

#### Scenario: The same bytes appear beyond the header window
- **WHEN** a `sequenced_after:` line sits below the lifecycle header window, or is indented, or appears inside a body paragraph
- **THEN** it MUST declare nothing, because beyond the window it is prose and a mention is not a parent link

#### Scenario: Fence lines consume the header window budget
- **WHEN** a proposal opens with a well-formed `---`-fenced front-matter block, and a `sequenced_after:` header line follows the closing fence
- **THEN** the window is still counted from the document's own line 1, so the fence's lines — both `---` delimiters and every line between them — count toward it rather than being excluded from the count
- **AND** a header line that the fence's length pushes past the window's last line is NOT read, exactly as a header line beyond the window is not read in an unfenced document

#### Scenario: An unfenced declaration attempts a multi-line value
- **WHEN** a header line carries no value on its own line and the next line is an indented continuation
- **THEN** the reader MUST refuse it by name and name the forms that work, because an unfenced document supplies no closing delimiter for the value

#### Scenario: The path-scope declaration is written as a header line
- **WHEN** an unfenced proposal writes `scope_globs:` as a header line
- **THEN** no path scope is declared, because the equivalence is granted to the parent declaration alone

### Requirement: One parent declaration across both sites, and its retention
A change SHALL carry AT MOST ONE `sequenced_after:` value however many sites it
writes it in, and a reader that finds the field at both sites SHALL treat equal
declarations as ONE declaration and SHALL REFUSE unequal ones rather than prefer
either site. Equality is decided under the SAME canonical form the archive
retention gate compares with, so entry ORDER is significant and a
self-qualified entry equals its bare form. A reader that preferred one site
would show a reviewer the other — the show-one-authorize-another defect the
strict loader's duplicate-key refusal already closes, one file apart rather than
one key apart — and the refusal SHALL name both values so the author can delete
the one that is not true. Two header lines for the same field SHALL be refused
as the duplicate key they are.

READING A NEW DECLARATION SITE SHALL NOT LICENSE WRITING INTO IT AFTER
RATIFICATION. Admitting the header-line form changes what a reader can SEE; it
changes nothing about what a ratified proposal may CARRY. Where a change's
declaration is ABSENT at its ratified head and present in the working tree —
whether because a header line was added, or because an existing line was MOVED
from beyond the window to inside it — the archive retention gate SHALL report a
contested-class mutation requiring an explicit recorded disposition, exactly as
it does for the fenced form. A declaration that was already present at the
ratified head SHALL be read as RETAINED, because both sides of the comparison
are read by the same reader; making an existing declaration legible is not a
mutation of it.

#### Scenario: Both sites carry the same declaration
- **WHEN** a proposal declares `sequenced_after:` in its front matter and again as a header line, and the two are equal under the canonical form
- **THEN** it is ONE declaration and validation proceeds

#### Scenario: The two sites disagree
- **WHEN** a proposal's front-matter declaration and header-line declaration differ — including the case where one is the empty root claim and the other names a parent
- **THEN** the reader MUST refuse, naming both values
- **AND** it MUST NOT resolve the disagreement by preferring a site

#### Scenario: A header-line declaration is added after ratification
- **WHEN** a ratified change's proposal gains a `sequenced_after:` header line, or an existing one is moved into the header window, after its ratified head
- **THEN** the archive retention gate MUST report a contested-class mutation requiring an explicit recorded disposition
- **AND** a declaration already present at the ratified head MUST read as retained rather than as a mutation

### Requirement: Realization axis vocabulary is gated
An ACTIVE change proposal's `target_release:` declaration SHALL carry a value
the ratified vocabulary admits — `implemented`, or a release identifier that
resolves to a release this estate defines — and a house validator SHALL REFUSE
any other value on an active proposal, naming the proposal's path and the value
it carries. A vocabulary stated in prose and read by nobody is a vocabulary the
next proposal diverges from, which is what the corpus shows.

THE DECLARATION IS A VALUE TOKEN FOLLOWED BY AN OPTIONAL PROSE GLOSS, and the
gate SHALL judge the TOKEN and never the gloss. That is the corpus's own form
rather than a rule invented at the gate: the house writes `target_release:
implemented (the openxFactory main line). No contract bundle is cut …`, and a
reader that judged the whole string would refuse every declaration that explains
itself. The token is the first whitespace-delimited word of the declaration.

A BLOCK THAT DECLARES `target_release:` TWICE SHALL BE REFUSED RATHER THAN READ
FROM ITS FIRST TOKEN. The declaration is a prose header, and a prose header's
repeat is joined into one value rather than refused as the duplicate key a
structured field's repeat would be — so a block declaring `implemented` and then
`none` would show a reviewer two declarations and authorize the first. One
declaration per block, and a repeat is a finding against that proposal.

ABSENCE IS THE PROMOTED DEFAULT AND SHALL NEVER BE A FINDING. *Realization axis
declaration* makes a proposal without the declarations a doc-only change
(`code_surface: none`, `target_release: implemented`) by default, so a proposal
that declares nothing declares the default. Only a PRESENT declaration is
judged — and a declaration present with no value SHALL be refused, because the
author wrote the key and the default is available by omitting it.

A RELEASE IDENTIFIER SHALL RESOLVE AGAINST THE REGISTRY THE SCANNED TREE
DEFINES, AND WHERE THE TREE DEFINES NONE THE SHAPE SHALL BE THE WHOLE TEST AND
THE RUN SHALL SAY SO. Where the tree carries a release registry, a name that
resolves to nothing in it is NOT a named release and SHALL be refused. Where
the tree carries no registry at all — every consuming repository that defines
no releases of its own — refusing every release name would make the gate
unusable outside the repository that defines them, so the identifier's SHAPE is
accepted on its own; that is a WEAKER judgment and SHALL NOT be silent, so the
run SHALL report that it judged on shape alone. The identifier's shape SHALL be
the shape this estate DEFINES for a release tag rather than one the gate
invents, so the gate cannot refuse a release the estate's own inventory admits.

AN ARCHIVED PROPOSAL SHALL BE READ AND NEVER JUDGED. An archived packet's front
matter is frozen record — `record-immutability` and `govern-archived-record-edits`
put it beyond a plain fix — so the gate SHALL count what the archive carries and
report it, and SHALL refuse nothing there. A gate that demanded an edit nobody
may make would be a standing finding with no remedy, which is the defect this
estate disposes of rather than creates.

THE STANDING DIVERGENCE SHALL BE NAMED IN A CLOSED REGISTER RATHER THAN
FORGIVEN IN CODE. Where the corpus at the gate's landing carries declarations
outside the vocabulary that are not corrected by the same act, each SHALL be
named in a register carried beside the validator, with the value token as it
stands, the class of divergence, the reason, a citation, and the event that
retires the entry. The register SHALL be CLOSED: an entry may be REMOVED when
its declaration is corrected or its packet archives, and admitting a NEW value
to the vocabulary SHALL be a change to this specification rather than an
addition to the register. CLOSURE SHALL BE ENFORCED AND NOT MERELY DECLARED:
the validator SHALL carry the baseline of entries the register holds when the
gate lands and SHALL REFUSE any entry that baseline does not carry, so an
exception cannot be granted by appending a line to a data file — granting one
takes an edit where the refusal itself is written, and the diff shows the act
for what it is. A registered declaration is REPORTED and not refused;
every declaration the register does not name is judged from the day the gate
lands, so the gate is a ratchet and the divergence cannot grow.

THE TWO REFUSALS ARE ASYMMETRIC AND SHALL STAY SO. An off-vocabulary
declaration the register does not name is a statement about the PROPOSAL and
the run SHALL fail; a register entry that matches nothing on a whole-corpus scan
is a statement about the REGISTER — the exception outlived the condition it was
granted for — and the run SHALL refuse with a distinct status until the entry is
deleted. Silently tolerating the second is how an exception list rots into a
blanket, and refusing makes the correction, or the archive, the event that
forces the re-examination.

#### Scenario: An active proposal declares a value outside the vocabulary
- **WHEN** an active change's `proposal.md` declares a `target_release:` whose value token is neither `implemented` nor a release identifier that resolves, and the register does not name it
- **THEN** the validator MUST fail, naming the proposal's path and the value token it carries
- **AND** the remedy belongs to the declaring packet, which corrects its own declaration

#### Scenario: An active proposal declares the implemented target
- **WHEN** an active change declares `target_release: implemented`, with or without a prose gloss after the token
- **THEN** the validator passes, the gloss being explanation and not declaration

#### Scenario: An active proposal names a release the estate defines
- **WHEN** an active change declares a release identifier and the scanned tree's release registry carries that release
- **THEN** the validator passes
- **AND** where that tree HAS a registry, a release-shaped name the registry does not carry MUST be refused, because a name that resolves to nothing is not a named release

#### Scenario: The scanned tree defines no release registry at all
- **WHEN** the tree carries no release registry, so no name in it could resolve, and an active change declares a release-shaped identifier
- **THEN** the identifier's shape MUST be the whole test and the declaration passes, because refusing every release name in a tree that cannot define one would make the gate unusable outside the repository that defines them
- **AND** the run MUST report that it judged on shape alone, the weaker judgment never being silent

#### Scenario: An archived proposal carries an off-vocabulary value
- **WHEN** the scan reaches a proposal under `openspec/changes/archive/` whose declaration is outside the vocabulary
- **THEN** it MUST NOT be a finding, and the run reports how many such records the archive carries

#### Scenario: A standing declaration is named by the register
- **WHEN** an active declaration outside the vocabulary is named by a register entry carrying its current value token, its class, its reason, its citation and its retirement event
- **THEN** the validator reports it as registered and does not refuse it

#### Scenario: A proposal declares the target release twice
- **WHEN** an active change's `proposal.md` front matter carries two `target_release:` header lines, the shared prose-header loader joining them into one value
- **THEN** the validator MUST refuse that proposal, naming it, rather than judging the first token and ignoring the second declaration

#### Scenario: An entry is appended to the closed register
- **WHEN** a register entry names a change and value token the validator's recorded closed baseline does not carry
- **THEN** the run MUST refuse, because the register is removable and never addable
- **AND** granting the exception takes an edit to the baseline in the same pull request, where the diff shows it

#### Scenario: A register entry matches nothing
- **WHEN** a whole-corpus scan finds a register entry whose change has archived, or whose declaration has been corrected so the value token no longer matches
- **THEN** the run MUST refuse with a status distinct from an off-vocabulary failure, naming the entry
- **AND** the remedy is to delete the entry in the same pull request that made it stale

#### Scenario: A proposal declares no target release
- **WHEN** an active change's `proposal.md` declares no `target_release:` at all
- **THEN** the validator passes, the proposal having taken the promoted doc-only default

### Requirement: A moved packet declares the identity it was ratified under
A change packet whose directory MOVES to a new change id SHALL declare the id it
moved from, in its own `.openspec.yaml`, as a member of a top-level
`former_ids:` list — a list, because a packet may move more than once, ordered
oldest first, and appended to rather than rewritten. The declaration is the
author's statement THIS DIRECTORY IS THAT PACKET, MOVED, and it is the only
thing in the corpus that carries that statement: history records that two paths
are similar and cannot record what the author meant by the similarity.

THE DECLARATION IS A SIBLING OF `origin:` AND NEVER A MEMBER OF IT, and the
reason is the freeze this specification already imposes. The origin declaration
is fixed at ratification and any post-ratification edit to it is a mutation
requiring an explicit disposition; a former-id entry is written by the very act
that MOVES the packet, which happens after ratification by construction, because
a draft that moves needs no declaration at all. A field inside the origin block
would therefore make every lawful move a mutation of a frozen declaration and
would need a disposition for each one. A top-level sibling is outside the block
the gate freezes, and it is the archive gate's own reader of that block — the
one that collects the `origin:` mapping's own lines and stops at the first
line that is not part of it — that makes this true rather than a convention.

AN ENTRY NAMES AN ID AND NEVER A PATH. This estate addresses a packet by its
change id and derives the path, at a ref as well as in the working tree — the
active location, or the dated archive directory carrying the same id — so an id
is declared ONCE per identity change and both of the paths it can occupy follow
from it. A declared PATH would have to restate the archive-directory convention
in every packet that ever moved, and would have to be re-declared when the
packet archives, which is not an identity change at all.

THE ARCHIVE RELOCATION IS NOT A MOVE UNDER THIS REQUIREMENT and SHALL NEVER BE
DECLARED. Archiving relocates `openspec/changes/<id>/` to
`openspec/changes/archive/<YYYY-MM-DD>-<id>/` and PRESERVES the id; it is
performed by the archive wrapper, it is recognizable from the id alone, and a
packet that declared it as a former identity would be declaring that it used to
be itself.

A DECLARED FORMER ID SHALL RESOLVE TO A PACKET THAT ACTUALLY MOVED. A former id
that stands as a live packet directory at the commit that declared it is a claim
to be the move of something that did not move, and SHALL be refused naming both
ids — that shape is a COPY, and a copy is a new packet with its own origin.

AN ENTRY IS ADDED ONLY BY THE COMMIT THAT PERFORMS THE MOVE IT RECORDS, and a
commit that adds a former id while moving nothing into this packet SHALL be
refused. Absence of a live directory is not proof of predecessorship: an id that
has archived, or that never existed, has no live directory either, so a rule
that only checks for one would let a standing packet append an unrelated
identity in an ordinary edit, acquire that identity's ratification as its
baseline, and capture every reference written under it. The entry a commit adds
SHALL therefore be exactly the source of the move that commit performs.

THE LIST IS APPEND-ONLY ACROSS COMMITS AND NOT ONLY WITHIN ONE. A commit that
REMOVES, REORDERS or REWRITES an entry an earlier commit established SHALL be
refused, whether or not that commit moves anything. Without that, a lawful move
could be declared at its landing and the declaration deleted the day after,
which would hand the archive gate the later ratification under the current id —
the very baseline this mechanism exists to keep it away from — and would do it
in a commit no arrival check ever looks at.

A FORMER IDENTITY HAS EXACTLY ONE OWNER. Where two packets declare the same
former id, or where an id is at once a live packet id and some packet's declared
former id, the declaration SHALL be refused naming every claimant: an identity
claimed twice resolves to a set, and a baseline chosen from a set is a baseline
chosen by the resolver rather than by an author.

#### Scenario: A ratified packet is renamed and declares where it came from
- **WHEN** the commit that renames a ratified packet also adds the former id to the destination packet's `former_ids:`
- **THEN** the move is lawful, the packet keeps the ratification it had under the former id, and its archive gate reads the baseline there

#### Scenario: A packet moves more than once
- **WHEN** a packet that already declares a former id moves again
- **THEN** the new former id MUST be appended to the existing list, oldest first, and no existing entry may be rewritten or removed

#### Scenario: A fork by copy declares nothing
- **WHEN** a new packet is authored as a copy of a ratified one, the source packet still standing in the tree
- **THEN** it MUST declare no former id, MUST carry its own origin declaration, and is baselined at its own first ratification
- **AND** the gate MUST NOT refuse it, the source having not moved

#### Scenario: A declared former id still stands in the tree
- **WHEN** a packet declares a former id and a live packet directory carries that id at the same commit
- **THEN** the declaration MUST be refused, naming both ids, because a packet that still stands was copied and not moved

#### Scenario: A draft is renamed
- **WHEN** a packet that has never declared `Status: ratified` is renamed
- **THEN** no declaration is owed, the packet having no ratification for a former identity to carry

#### Scenario: A former id is appended by a commit that moves nothing
- **WHEN** a standing packet adds a former id in a commit that performs no move of that id into it
- **THEN** the declaration MUST be refused, naming the id and the commit
- **AND** the id having no live directory MUST NOT be read as evidence that it moved here

#### Scenario: A later commit removes or reorders a declared former id
- **WHEN** a commit rewrites `former_ids:` so that an entry an earlier commit established is removed, reordered or respelled
- **THEN** that commit MUST be refused, the list being append-only across commits and not only within one

#### Scenario: Two packets claim the same former identity
- **WHEN** two packets declare the same id in `former_ids:`, or an id is both a live packet id and a declared former id
- **THEN** the declaration MUST be refused, naming every claimant
- **AND** the resolver MUST NOT settle the claim by preferring one of them

### Requirement: An undeclared rename arrival is refused at its landing
A landing SHALL be REFUSED where its commit brings a change packet directory in
by a MOVE from another change packet directory WHOSE IDENTITY HAS EVER DECLARED
`Status: ratified`, and the arriving packet does not declare the source id in
`former_ids:` in that same commit. The refusal is taken AT THE LANDING of
the commit that performs the move, which is the only place the question is
cheap: a move lands as one commit, so the gate reads one commit and never a
chain, and the author who made the move is the author who is asked.

THE SOURCE IDENTITY IS THE SOURCE PACKET'S WHOLE DECLARED LINEAGE — its own id
TOGETHER WITH every id it declares in `former_ids:` at that commit's parent —
and the "ever ratified" test SHALL be taken over all of them. Reading the source
id alone would lose a packet that has already moved once lawfully: X ratified,
X moved to Y with the move declared and the header returned to draft, then Y
moved to Z undeclared. Y's own id never declared `Status: ratified`, so a test
over Y alone would pass the second landing and Z would stand with no lineage at
all. THIS IS NOT A HISTORY WALK: the source packet's own declaration is one
blob at one commit, and every id it names is asked directly, exactly as the
baseline resolution asks them.

AND THE ARRIVING PACKET'S LIST SHALL BE THE SOURCE'S LIST WITH THE SOURCE ID
APPENDED — every entry the source carried, in the order it carried them, then
the id the move came from. A move that drops an entry the source declared is a
move that sheds a lineage, which is the same defect as never declaring one.

A MOVE OF A PACKET THAT HAS NEVER BEEN RATIFIED IS OUT OF SCOPE AND STAYS
LAWFUL. Renaming a draft is an ordinary authoring act this estate performs, the
promoted realization record says so in as many words — *"renaming a DRAFT
change, and a single commit that renames a draft and ratifies it, are
unaffected"* — and a refusal reaching it would make the mechanism cost more than
the defect. The qualification is EVER, read over the source identity's whole
history up to that commit, and never its blob at the parent: a packet renamed
and un-ratified in one commit is back in DRAFT for every later hop, so a test
taken at the parent would exempt exactly the shape this refusal exists to catch.

THE REFUSAL IS WHAT MAKES THE DECLARATION MORE THAN AN HONOUR SYSTEM. A
mechanism that only reads declarations protects the author who writes one; the
failure this gate exists to catch is a rename that sheds a ratification, which
is by construction a rename whose author would not declare it. So the
UNDECLARED case is the refused case, and the declared case is the ordinary one.

THE ARCHIVE RELOCATION IS EXCEPTED BY ID, and it is the only exception. A
destination under `openspec/changes/archive/<YYYY-MM-DD>-<id>/` whose id equals
the source's id is the archive wrapper's own relocation and SHALL pass without a
declaration.

THE ARRIVAL READ SHALL FAIL CLOSED. Where the gate cannot perform the read that
would pair an arrival with a departure — a checkout that cannot produce the
content the pairing is computed from — and the tree at that commit shows both a
packet directory arriving and a packet directory leaving, the gate SHALL refuse
as CANNOT RUN, naming the read it could not perform, rather than reporting that
no arrival was found. A silence that cannot be distinguished from an answer is
not an answer.

AND SO SHALL THE RATIFICATION LOOKUP, WHICH IS A SECOND READ AND NOT A COROLLARY
OF THE FIRST. Deciding whether the source lineage has EVER declared
`Status: ratified` reads history at every identity in that lineage, and a
checkout that cannot produce those blobs returns the same silence as a lineage
that was never ratified — which would pass an undeclared landing on the one
checkout where nothing can be proved. So this read SHALL distinguish ABSENT from
UNREADABLE on the same terms the archive gate's baseline read does, and a read
it could not perform SHALL refuse as CANNOT RUN naming the identity and the
read, never resolve to "never ratified".

THE REFUSAL SHALL NAME THE REMEDY AND SHALL CARRY NO BYPASS FLAG. It names the
commit, the source path, the destination path, and the one repair: declare the
source id in the destination packet's `former_ids:` in the same commit. A flag
would be the declaration nobody writes.

#### Scenario: A ratified packet is renamed with no declaration
- **WHEN** a commit moves a change packet directory to a new id and the arriving packet declares no former id
- **THEN** the gate MUST refuse that landing, naming the commit, both paths, and the declaration that would repair it

#### Scenario: A rename chain is attempted one hop at a time
- **WHEN** a packet is renamed, un-ratified, renamed again while draft, and ratified under its third id, each hop landing as its own commit
- **THEN** the FIRST undeclared hop MUST be refused at its own landing, so no later hop is ever reached
- **AND** the gate MUST NOT need to walk the chain to reach that answer
- **AND** the first hop qualifies because its source had declared `Status: ratified`, whatever the destination declares at that commit

#### Scenario: A never-ratified draft is renamed
- **WHEN** a commit moves a packet directory whose identity has never declared `Status: ratified` anywhere in its history
- **THEN** the landing passes with no declaration, the move being an ordinary authoring act

#### Scenario: A once-ratified packet is moved while back in draft
- **WHEN** a commit moves a packet whose identity declared `Status: ratified` earlier in its history but does not at that commit
- **THEN** the landing MUST be refused unless the arriving packet declares the source id
- **AND** the test MUST be the source identity's whole history and never its blob at the commit's parent

#### Scenario: A packet that already moved lawfully moves again
- **WHEN** a packet ratified under one id, moved to a second with the move declared and the header returned to draft, is moved to a third
- **THEN** the "ever ratified" test MUST reach the id the packet declares as its former identity, so the second move is refused unless it too is declared
- **AND** the arriving packet's list MUST be the source's list with the source id appended, so no entry the source declared is dropped

#### Scenario: A move drops an entry the source declared
- **WHEN** a declared move's destination omits an id the source packet carried in its own `former_ids:`
- **THEN** the landing MUST be refused, a move that sheds a lineage being the same defect as never declaring one

#### Scenario: The declared move lands
- **WHEN** the moving commit carries the source id in the destination packet's `former_ids:`
- **THEN** the landing passes and the identity continuity is on the record where the archive gate will read it

#### Scenario: A packet archives
- **WHEN** a commit relocates `openspec/changes/<id>/` to `openspec/changes/archive/<YYYY-MM-DD>-<id>/` with the id unchanged
- **THEN** the landing passes with no declaration, the archive relocation preserving the identity rather than changing it

#### Scenario: The pairing read cannot be performed
- **WHEN** the checkout cannot produce what the arrival pairing is computed from, and the tree at that commit shows a packet directory arriving and a packet directory leaving
- **THEN** the gate MUST refuse as CANNOT RUN, naming the read it could not perform
- **AND** it MUST NOT report that no arrival was found

#### Scenario: The ratification lookup cannot be performed
- **WHEN** the gate cannot read the history that would say whether an identity in the source lineage ever declared `Status: ratified`
- **THEN** the gate MUST refuse as CANNOT RUN, naming that identity and the read
- **AND** it MUST NOT resolve the unreadable history to "never ratified" and pass an undeclared landing

### Requirement: A packet reference resolves by identity, not by path
A reference that addresses a change packet SHALL be resolved BY ITS CHANGE ID —
against the location that id occupies now, whether active or archived, and
against any packet that declares that id in `former_ids:` — and a reference is
dangling only when it resolves to nothing under that rule. A path written into a
record is a spelling of an identity at one moment; the identity is what the
record meant, and it is the identity that has to resolve.

A PACKET-RELATIVE PATH CARRIES THE ID IT ADDRESSES, so this rule reaches
citations written as paths and not only citations written as ids: the second
segment of `openspec/changes/<id>/…` names the packet, and the remainder names a
file within it, which is what makes the reference re-resolvable at all.

BOTH HALVES SHALL RESOLVE, AND A FAILURE SHALL SAY WHICH HALF FAILED. Where a
citation names a file inside the packet, the location the identity resolves to
MUST also carry that remainder; an identity that resolves to a packet which does
not carry the cited file is a DANGLING reference, reported against the file and
not against the packet. Resolving the identity alone would accept a citation to
a file that was deleted, renamed or never written — a defect this rule exists to
find, spelled at a finer grain than the one the archive relocation breaks.

THE DEFECT IS THAT NOTHING RESOLVES THEM. A citation contract that requires a
citation and never checks that it leads anywhere accepts a citation to a path
that has not existed for weeks, and the corpus's own citations break by an act
nobody thinks of as breaking anything — the archive relocation, which every
packet performs exactly once.

RESOLUTION IS TO EXACTLY ONE PACKET, OR TO NOTHING, AND NEVER TO A SET. Where an
id would resolve to more than one candidate — two dated archive directories
carrying the same id, a live directory and some packet's declared former id, or
two packets declaring the same former id — the reference SHALL be reported as
AMBIGUOUS and SHALL NOT be resolved by preferring one. This estate already draws
that line where it resolves a packet by id: its archived-directory lookup
returns every match as a LIST rather than a path, on the stated ground that two
archive dates for one id is "an AMBIGUITY the resolver must be able to report,
not a collision to resolve by taking the newest". A resolver that silently picks
one candidate makes the record's meaning depend on sort order.

CORRECTING A RECORD IS NOT THE REMEDY THIS REQUIREMENT IMPOSES. Where a
reference resolves by identity, it is not a defect and nothing is owed; the
reader resolves it. Only a reference that resolves to no identity at all is a
defect, and it belongs to the record that wrote it. An AMBIGUOUS reference is
neither: it is a defect of the corpus that made one identity resolve twice, and
it belongs to the declaration that created the collision.

#### Scenario: A cited path names a packet that has since archived
- **WHEN** a record cites `openspec/changes/<id>/<file>` and that packet now stands at `openspec/changes/archive/<YYYY-MM-DD>-<id>/<file>`
- **THEN** the reference MUST resolve by id to the archived location and MUST NOT be reported as dangling
- **AND** no edit to the citing record is owed

#### Scenario: A cited path names an id a packet declares as a former id
- **WHEN** a record cites a packet by an id that no directory carries, and some packet declares that id in `former_ids:`
- **THEN** the reference MUST resolve to that packet
- **AND** the declaration is what authorizes the resolution, a path similarity never being one

#### Scenario: A cited path resolves to no identity at all
- **WHEN** a cited packet id names no active directory, no archived directory, and no declared former id
- **THEN** the reference is dangling and is a defect of the citing record

#### Scenario: The identity resolves and the cited file does not
- **WHEN** a citation's packet id resolves but the location it resolves to does not carry the remainder the citation names
- **THEN** the reference is dangling and the report MUST name the FILE as the half that failed, the identity having resolved

#### Scenario: A reference names another repository's packet
- **WHEN** a citation names a packet in a repository other than the one being read
- **THEN** it MUST NOT be reported as dangling on that tree, a reference out of scope being no evidence about the reference

#### Scenario: An id resolves to more than one packet
- **WHEN** a cited id matches two dated archive directories, or a live directory and a declared former id, or two packets' declared former ids
- **THEN** the reference MUST be reported as AMBIGUOUS and MUST NOT be resolved by preferring one candidate
- **AND** the defect belongs to the declaration that made one identity resolve twice, not to the citing record
