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
