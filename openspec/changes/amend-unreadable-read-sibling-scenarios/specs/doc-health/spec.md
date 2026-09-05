# doc-health

## MODIFIED Requirements

### Requirement: Release-tag publication
The release-tag-publication family SHALL report, for every repository in scope and for EVERY BUNDLE THAT REPOSITORY HAS CUT at or above the version where mandatory tag publication begins, whether that bundle has a published ANNOTATED tag, and whether that tag peels to a commit that declares the bundle.

EVERY CUT BUNDLE, NOT ONLY THE ONE CURRENTLY DECLARED — and this is the
difference between catching the recurrence and reading zero through it. A
bundle is legitimately silent while its declaring commit is the published tip.
Then the NEXT cut advances the manifest, and a family that read only the current
declaration would begin checking the new bundle and NEVER REVISIT the old one.
Run against the incident that motivated this family it would have reported
nothing at all: `contract-v2.3` untagged, `contract-v2.4` declared on top of it,
silence. The set of bundles a repository has cut SHALL be taken from its release
inventories, which are the machine-readable fact that a cut happened.

A SUPERSEDED BUNDLE IS NOT GRADED BY DISTANCE. The distance window exists for
the interval between declaring and tagging, and that interval ENDED for any
bundle the manifest has moved on from. An untagged superseded bundle is
therefore reported at `error` without grading, and its remedy is
retro-publication at the commit the policy's rule identifies — RETRO-PUBLISHED,
NOT RE-DATED, as the 2026-08-25 discharge did.

The obligation being checked belongs to `docs/contract-versioning-policy.md` —
"a bundle is not published until its tag exists", and "the tag SHALL point to
that realized commit". This requirement defines only how doc-health checks it,
in the same by-reference relationship `tag-hygiene` already has with
`document-lifecycle`'s marker grammar and `Release-inventory drift` has with
`release-surface-integrity`.

THE FAMILY SHALL BE DISTANCE-GRADED RATHER THAN IMMEDIATE, because the declaring
commit and the tag are two acts by two actors and the interval between them is
legitimate. A cut declares the bundle; the repository owner publishes the tag
afterwards. A family that fired the moment the manifest moved would redden every
correctly performed release, and a family nobody can leave green is a family
that gets configured away. Distance SHALL be measured in FIRST-PARENT COMMITS ON
PUBLISHED `main` since the earliest commit declaring the bundle, never in wall
time, because landings are what the policy's own retro-publication rule counts
and wall time punishes a quiet week.

THE THRESHOLD SHALL DEFAULT TO FIVE FIRST-PARENT LANDINGS, ruled by Brett Heap on
2026-08-31. It is a threshold default in the sense this capability already gives
that term, configurable in the same place the aging defaults are, and the ruled
number is what an unconfigured run uses. The calibration it answers to:
`contract-v2.3` sat untagged across six first-parent landings before a human
noticed it, so a threshold above five would have stayed silent through the
recurrence this family exists to catch.

THE TWO FAILURE STATES SHALL BE REPORTED IN DIFFERENT WORDS AND AT DIFFERENT
SEVERITIES. An ABSENT tag is an incomplete release — the common case, and the
one the window above exists to tolerate for a while. A tag that exists and peels
to a commit NOT declaring the bundle is a MISPLACED tag: it satisfies every
check that asks only whether a tag exists, it is what consumers will pin, and it
is worse than absence because it looks like completion. Reporting them alike
would let the common one hide the serious one.

THE FAMILY SHALL NOT FIRE BELOW THE ENFORCEMENT LINE. `contract-v1.0` through
`contract-v1.6` predate mandatory annotated tags and carry none by design, as
the changelog's own legacy baseline note records. A family that reported them
would emit seven permanent findings nobody may act on, which is how a report
teaches its readers to stop reading it.

A LIGHTWEIGHT TAG SHALL NOT SATISFY THE OBLIGATION. The policy requires an
ANNOTATED tag; a lightweight ref carries no tagger, no date and no message, and
accepting one would let the weaker object silently discharge the stronger
requirement.

The family SHALL be reported as skipped, never silently omitted, where a
repository declares no bundle at all, or where version control cannot answer —
an unavailable git dependency, tag refs that cannot be listed, or a declaring
commit that does not resolve. THE SKIP IS RESERVED FOR "THE QUESTION COULD NOT
BE ASKED": a declared bundle whose tag is simply absent is an ANSWER, and is
reported by the scenarios below rather than skipped.

THIS FAMILY DOES NOT PROVE THE TARGET IS THE EARLIEST DECLARING COMMIT, and the
residue is disclosed rather than hidden. The policy's target is "the EARLIEST
FIRST-PARENT COMMIT on published `main` that DECLARES the bundle and at which
`verify-commit` PASSES"; the second conjunct is a digest verification per
candidate and is out of scope here. A tag on a LATER declaring commit therefore
passes this family and remains a defect under the policy.

**AMENDED BY `declare-spent-bundle-state` (2026-09-02).** Every paragraph above
this note stands exactly as promoted; everything from here to the scenarios is
this change's addition, and among the scenarios exactly one `AND` bullet is
added, to *A bundle was cut, superseded, and never tagged*. Nothing else in this
requirement moves. **AND ONE PROMOTED PARAGRAPH IS QUALIFIED RATHER THAN
REPLACED, which is worth saying because its bytes are unchanged**: *A SUPERSEDED
BUNDLE IS NOT GRADED BY DISTANCE* still reads that an untagged superseded bundle
is *"reported at `error` without grading"*, and that remains exactly what such a
bundle reads as WHEREVER NO DECLARATION NAMES IT — which is every bundle in the
estate's history but one, and the default forever. The sentence is kept
byte-faithful rather than rewritten so that a reader arriving at it meets the
promoted rule and then its one exception, instead of a rewritten rule with no
trace of what it replaced.

A SUPERSEDED BUNDLE MAY BE DECLARED SPENT, AND A SPENT BUNDLE IS THE THIRD STATE
THIS FAMILY OTHERWISE LACKS. Between *published* and *owes a tag* sits a number
that was cut, was never publishable, and never will be. The action the
superseded finding prescribes — retro-publication at the commit the policy's
rule identifies — is UNPERFORMABLE for such a bundle, and a finding whose only
prescribed action cannot be taken by anyone is one a reader learns to skip,
which is how a report loses the readers the rest of it needs. The family SHALL
therefore recognize a SPENT state, and SHALL recognize it ONLY from an EXPLICIT
DECLARATION.

SILENCE IS NEVER A DECLARATION, AND THAT SENTENCE CARRIES THE WHOLE OF THIS
STATE'S FAIL-CLOSED CHARACTER. An untagged superseded bundle that no declaration
names SHALL be reported exactly as it is today, at `error` and in the same
words. A bundle MUST NOT become spent by being old, by being ignored, by being
inconvenient, or by any absence whatsoever. Every state below is entered by a
record that exists and is refused by a record that does not.

THREE OUTCOMES, NOT TWO, AND THE MIDDLE ONE IS NOT A REFUSAL — stated here
because a two-way reading of "accepted or refused" makes the ruled `warning`
band unreachable. A declaration is ACCEPTED (the `info`), REFUSED (an `error`,
and the superseded-and-never-published `error` stands alongside it because a bad
declaration must remove nothing), or PROVISIONAL: well formed in every element,
naming a LATER superseding bundle that is CUT but NOT YET PUBLISHED. A
PROVISIONAL declaration SHALL emit the `warning` and SHALL SUPPRESS the
superseded-and-never-published `error` for that bundle, reporting ONE finding
and not two. That is the ruled outcome — this case is a `warning` — and a
conforming family reporting both would be contradicting it. **NOTHING IS LOST BY
THE SUPPRESSION, AND THIS IS WHY THE BAND IS SAFE**: the successor is the bundle
the manifest now declares, so it is graded by the distance arm ON ITS OWN
ACCOUNT — `warning` inside its window, `error` past the threshold — so the
obligation has MOVED ONTO THE SUCCESSOR rather than been discharged, which is
exactly what the successor guard is for. The provisional band is bounded by that
grading and not by this state's patience.

THE DECLARATION SHALL BE READ FROM `contracts/CHANGELOG.md` AT THE PUBLISHED
TIP, and from nowhere else. Three facts pick that document and no other. It is
ON THE RELEASE SURFACE a consumer already pins — it is a member of every release
digest inventory — so the record travels with the bundle rather than sitting
beside it. It is one of the THREE EDITORIAL MEMBERS the versioning policy allows
to move between cuts, so a disposition can be recorded when the fact arises
rather than waiting for a bundle that may never be cut; every other release
member is one whose between-cuts edit is itself a defect. And the changelog is
ALREADY where this estate records supersessions — `contract-v2.3`'s disposition
sits in `contract-v2.4`'s entry and `contract-v2.6`'s sits in `contract-v3.0`'s
— so the state is given a machine-readable handle on a record the estate keeps
anyway, rather than a second record beside it.

THE DECLARATION SHALL NOT BE READ FROM `health/dispositions.yaml`, and the
reason is mechanical rather than a preference. That file SUPPRESSES findings
keyed by `(family, repo, path)`, and every finding this family raised BEFORE
this amendment lands on `contracts/manifest.yaml` — so a single entry on that
path would suppress EVERY absent-tag, misplaced-tag and lightweight-ref finding
this family could ever raise about that repository, including the next genuinely
abandoned bundle. That coarseness is the mechanism's, not this state's: it has
no way to name one bundle. (The findings THIS amendment adds land on per-bundle
inventories for the very same reason — see the path rule below — which is the
distinction the dispositions file cannot draw.) It lives at the AGGREGATION
ROOT, so it is
unreachable both by a consumer reading a pinned policy document and by a
`--single-repo` run, which is the scope this family's own self-gate uses. A
mechanism that cannot name one bundle, cannot be read by the consumer the
obligation protects, and is invisible to the gate that measures it is not the
smaller mechanism; it is the one that fails open.

THE DECLARING ACT IS THE SUPERSEDING BUNDLE'S OWN CHANGELOG ENTRY, and that
answers who may declare a bundle spent. A declaration SHALL be accepted only
where the changelog entry containing it is the entry of the bundle it names as
the superseding one. A bundle therefore cannot declare ITSELF spent, and no
document outside a release entry can declare anything spent: the act costs a
version number, is performed by a release cut, and is recorded on the surface
consumers pin. A family that accepted a repository's declaration about its own
number would be accepting *"I decided not to tag it"*, which is the state this
family exists to refuse.

THE DECLARATION SHALL TAKE ONE RESERVED SINGLE-LINE FORM, and the form is stated
here rather than left to an implementation because a deterministic family reading
free prose is a family whose behaviour nobody can predict from its
specification:

    **SPENT BUNDLE:** `<bundle>` — SUPERSEDED BY `<superseding bundle>` — CAUSE: <text> — RULED BY <author>, <YYYY-MM-DD> — MEASUREMENT: <citation>

That is the literal line, shown as a code block so that no delimiter of the
surrounding prose can be misread as part of it — a form quoted inside backticks
invites a reader to copy the backticks, which is a defect a specification can
avoid by not introducing it. The opener `**SPENT BUNDLE:**` is RESERVED: no other text in
`contracts/CHANGELOG.md` may begin a line with it, and a line beginning with it
that does not complete the form is a malformed declaration rather than prose to
be ignored. The form is a HANDLE ON THE RECORD AND NOT A SECOND RECORD — it is
written INSIDE the human disposition subsection the cut writes anyway, in the
pattern `document-lifecycle`'s reserved `Modified over` marker already sets, so
there is one record and one place it can be read from.

FOUR ELEMENTS ARE OWED AND EACH SHALL BE CHECKED FOR PRESENCE: the SUPERSEDING
BUNDLE, the CAUSE, the RULING that disposed it — its author and its date — and
the MEASUREMENT OF RECORD the cause cites. The family SHALL verify that each is
present and non-empty and SHALL verify the superseding bundle mechanically; it
does NOT and CANNOT verify that a cited ruling was really made, and that residue
is disclosed rather than hidden. What makes the state safe is not the family's
belief in the citation but the successor guard below, which cannot be satisfied
by writing anything.

THE SUCCESSOR GUARD IS WHAT MAKES THE STATE UNABUSABLE — RULED BY BRETT HEAP,
2026-09-02 — and it SHALL hold in both directions. A SPENT declaration SHALL be
quiet only where the superseding bundle it names has itself been CUT and has
itself been PUBLISHED: an annotated tag peeling to a commit that declares it. So
the only way to retire a number is to publish its replacement's tag, which is
the very act this family exists to compel; a repository that walks away from a
bundle by declaring it spent has merely moved the obligation onto the successor,
where the same check meets it again. Where the successor is cut but not yet
published the supersession is UNPROVEN and the family SHALL `warning` rather
than accept it; where the successor was never cut at all the declaration points
at nothing and the family SHALL `error`.

AND THE SUCCESSOR SHALL BE LATER THAN THE BUNDLE IT SUPERSEDES, which is the
half a "cut and published" test does not cover and which cannot be omitted. The
superseding bundle's `(major, minor)` SHALL be STRICTLY GREATER than the spent
bundle's, and a declaration naming a successor that is not SHALL be an `error`
that accepts nothing. Without it, the guard above is satisfiable by an ALREADY
PUBLISHED EARLIER BUNDLE — a declaration for `contract-v2.6` written into
`contract-v2.5`'s entry and naming `contract-v2.5`, which was cut, is published,
and carries a valid tag — so an untagged bundle would go quiet with NO
replacement published at all and the guard would have been walked around
backwards rather than broken. Found by Codex on PR #578 against the ratified
shape of this delta, and repaired in it rather than filed. The residue is
disclosed: version ordering is the CHEAP conjunct, and this family does not
prove that the successor actually CARRIES what the spent bundle was to have
carried. That claim lives in the declaration's CAUSE and MEASUREMENT, which are
read for presence and not for truth — the same disclosure this requirement
already makes about the earliest-declaring-commit conjunct.

A CORRECTLY DECLARED SPENT BUNDLE IS RECORDED, NOT SILENT — RULED BY BRETT HEAP,
2026-09-02, on an alternative that was put to him and declined. The family SHALL
emit exactly one `info` for it, naming the spent bundle, the bundle that
superseded it, and where the record is. It is recorded because a reader who
finds a release inventory with no matching tag is owed the answer in the report
rather than only in a changelog they may not read.

AND THE FINDING SHALL LAND ON THAT BUNDLE'S OWN RELEASE INVENTORY —
`contracts/releases/<bundle>.digests.yaml` — NOT on the manifest and NOT on the
changelog, because THE PATH IS THE FINDING'S IDENTITY. A finding's identity in
this capability is `(family, repository, path)`; every other finding of this
family lands on `contracts/manifest.yaml`, so a spent state landed there would
share an identity with every one of them and its disappearance would be masked
by any surviving sibling. The changelog is no better: two bundles legitimately
declared spent would share THAT path too, and removing one declaration while the
other stood would leave the shared identity present and the removal unreported.
The per-bundle inventory is the one path that is unique to the bundle BY
CONSTRUCTION — it is the artifact whose existence made the bundle enumerable in
the first place. Found by Codex on PR #578 against a `contracts/CHANGELOG.md`
path, and repaired rather than filed. The `info` SHALL be classed `contested`,
so that a spent state which stops being reported without a cited change is
re-raised: the way to make it stop is to delete that inventory or that
declaration, and *"never edit the manifest, the changelog or the inventory to
match the absence"* is the sentence this family already prescribes. Every OTHER
finding this state introduces SHALL land on the same per-bundle inventory, with
ONE exception that has no bundle to land on: a declaration naming a bundle this
repository never cut at all disposes nothing and SHALL be reported at `warning`
on `contracts/CHANGELOG.md`, because a mistyped bundle name leaves the real
bundle undeclared and still reported, and an orphan record that looks like a
disposition is worth a reader's attention.

The `info` MUST NOT be read as the tag obligation having been MET. It was not
met; it was EXTINGUISHED, by an owner act, at the cost of a version number, and
the record says which.

THE SPENT STATE REACHES THE ABSENT-TAG ARM AND NOTHING ELSE. It SHALL NOT quiet
a MISPLACED tag, SHALL NOT quiet a LIGHTWEIGHT ref, SHALL NOT quiet the
distance-graded findings on the bundle the manifest currently declares, and
SHALL NOT be accepted for that bundle at all. The state answers *"this number
will never be published"*; it does not answer *"whatever ref exists under this
name is acceptable"*, and a tag that exists and points wrongly is the condition
this family already calls worse than absence.

THE STATE SHALL NOT BE READ BACKWARDS. The five bundles the versioning policy
records under § *Untagged Bundles After Enforcement Began* are NOT retrofitted:
all five were publishable, all five were published, and all five carry annotated
tags on declaring commits, so none of them reaches this arm at all. Neither does
any bundle below the enforcement line. `contract-v2.6` is the first bundle of
this kind in the estate's history, and a state introduced for one instance must
not acquire a second by being applied to cases that were only late.

**AMENDED BY `add-release-tag-gate` (2026-09-04).** Every paragraph above this
note stands exactly as promoted and exactly as `declare-spent-bundle-state` left
it; everything from here to the scenarios is this change's addition, and SIX
scenarios are added after the ones above. Nothing else in this requirement
moves: no severity changes, no arm is removed, no threshold moves, no path
moves, and what the family READS over a tree is not altered by one line. **THIS
BLOCK DROPS NO UNIT OF CANON** — it restates the requirement in full and adds to
it — so no `Removed from canon by` and no `Merged into` marker is owed.

THE CONDITION SHALL BE REPORTED NIGHTLY AND ENFORCED AT THE CUT, AND THOSE ARE
TWO MOMENTS OF ONE OBLIGATION RATHER THAN TWO OBLIGATIONS. The family above is
the REPORT: it runs in the nightly doc-health lane over published `main`, at the
severities this requirement already sets, and a cut landed without its tag stays
visible there however it landed, including on an administrative bypass. The
ENFORCEMENT is a required status check on the pull request that changes the
release surface, and it asks the SAME FAMILY the SAME QUESTION about a different
tree. One family, one definition of "published", two moments — never a second
implementation, a second severity ladder, or a second notion of when a tag
counts.

THE ENFORCING MOMENT IS THE PULL REQUEST THAT TOUCHES THE RELEASE SURFACE, AND
NO OTHER PULL REQUEST. The release surface, for this purpose, is
`contracts/manifest.yaml` and the release inventories under
`contracts/releases/`. A pull request that changes neither SHALL be passed
without the family being consulted about it at all, and this is the point of the
arrangement rather than an optimisation: the tag is published by a second actor
AFTER the cut merges, so any enforcement that reached every pull request would
make one actor's pending act every other lane's merge blocker. **THAT IS NOT
HYPOTHETICAL AND THE MEASUREMENT IS WHY THIS PARAGRAPH EXISTS.** On 2026-09-03
`contract-v3.3` was declared at 22:27Z and tagged five and a half hours later,
and for that whole window every open pull request in the repository failed a
required check on that one fact.

THE CHECK SHALL BE REQUIRED AND SHALL THEREFORE REPORT ON EVERY PULL REQUEST,
deciding for itself rather than being filtered by path. A required status
context that does not report on some pull requests is expected forever and
blocks them, so the scope rule above SHALL be evaluated INSIDE the check and not
by the trigger that starts it.

THE BAR IS THE ONE THAT WAS ALREADY BEING ASSERTED, MOVED RATHER THAN WEAKENED:
no `error` and no `warning` from this family over the tree under judgment. A
`warning` refuses too. The distance window this requirement grants a fresh cut
is for LANDINGS THAT LEAVE THE RELEASE SURFACE ALONE; a pull request that
touches that surface again is asserting the surface is in order, and is answered
on that assertion.

THE BUNDLE THE PULL REQUEST ITSELF CUTS SHALL NOT BE REQUIRED TO CARRY A TAG,
AND THE OBLIGATION SHALL BE RECORDED INSTEAD. The tag cannot exist yet: under
the versioning policy's realization order the reviewed commit lands first and
the annotated tag is published afterwards at the commit that landed. A check
demanding it before the merge would be unsatisfiable by construction, and an
unsatisfiable gate is one that gets configured away. No new rule is needed for
this, which is the load-bearing part: the bundle a cutting pull request declares
has its declaring commit AS THE TIP of the tree under judgment, so the distance
arm above already emits nothing — the scenario *The declaring commit is still
the published tip* answers it, and it answers it in the same words for a merge
tree as for published `main`. WHAT THE CHECK ADDS IS THAT THE SILENCE IS
RECORDED RATHER THAN PASSED OVER: the outstanding tag SHALL be named in the
check's own report, so that a reader of the passing check is told what is still
owed and by whom.

WHERE THE QUESTION CANNOT BE ASKED, THE CHECK SHALL FAIL CLOSED, AND THIS IS
WHERE IT DIVERGES FROM THE NIGHTLY ON PURPOSE. The family reports a SKIP when
version control cannot answer, and the nightly is right to carry that skip as an
`info`: it reads an environment it does not control and a skip there is the
honest answer. The check is the ENFORCING moment for a tree that is about to
become the published one, so an unasked question SHALL NOT be a pass.

THE CONDITION SHALL NOT ALSO BE PINNED AS A ZERO-FINDINGS ASSERTION OVER THIS
REPOSITORY IN ITS OWN TEST SUITE, and the prohibition is deliberate rather than
incidental. A test asserting that the repository currently reads zero findings
of this family is a pin on a fact that a legitimate, in-progress release makes
false, held inside a suite that every pull request must pass — so it converts
one actor's pending act into every lane's failure, which is the defect this
amendment removes and which it MUST NOT be able to re-acquire by having the
assertion written back beside the moved one. **WHAT IS KEPT IS THE POSITIVE
CONTROL.** A probe that only ever reads zero cannot be told apart from a reader
that answers nothing, so the suite SHALL go on demonstrating, over a tree
constructed to be untagged, that this family can fire.

**AMENDED BY `amend-published-tip-unreadable-scenario` (2026-09-05).** Every
paragraph above this note stands exactly as promoted, and the ONLY change this
block makes is to the scenario *The manifest cannot be read at the published
tip*: its `WHEN` bullet is replaced and two `AND` bullets are added. No other
scenario moves, no severity changes, no arm is removed, no threshold moves, and
what the family READS over a tree is not altered by one line — this is CANON
CATCHING UP WITH THE CHECKER, not a change to the checker.

THE FAMILY SHALL NOT NAME A CAUSE IT HAS NOT ESTABLISHED. A per-path answer of
nothing carries two facts at once — an unfetched commit, and a commit this
checkout holds that simply has no manifest — and the promoted wording named the
first as the commonest without the family being able to tell them apart. It can
now: it asks whether the commit is present and attempts one bounded fetch where
it is not, and reports each fact in its own words. **THE MEASUREMENT THAT
SETTLED WHICH IS COMMONER RAN THE OTHER WAY** — on the aggregation nightly the
commit WAS fetched, the workflow's own fetch step having put all ten published
tips in the store, and nine of the ten governed repositories simply carry no
`contracts/manifest.yaml` at all (openxFactory #612, remedied by #646). A
parenthetical that misnames the common case sends every reader of the report to
look for a fetch defect that is not there, which is the cost this amendment
removes.

**Removed from canon by amend-published-tip-unreadable-scenario (2026-09-05):**
``**WHEN** the blob read for the manifest at the published tip answers nothing — the commonest cause being a checkout that has not fetched that commit`` — the
clause after the dash asserts which cause is commonest, and the measurement
above shows it is the other one; the unit is REPLACED rather than deleted, by
the `WHEN` that names both facts and the `AND` that requires the family to
establish which holds before it speaks. Nothing else in this requirement is
dropped.

**AMENDED BY `amend-unreadable-read-sibling-scenarios` (2026-09-05).** Every
paragraph and every scenario above this note stands exactly as promoted —
including the note and the marker `amend-published-tip-unreadable-scenario` left
here, which promote with the requirement and are carried, not restated — and the
ONLY change this block makes is to the scenario *The changelog cannot be read at
the published tip*: its `WHEN` bullet is replaced and two `AND` bullets are
added. No other scenario moves, no severity changes, no arm is removed, no
threshold moves, and the set of trees over which this family speaks is not
altered by one line.

THE SAME RULE, AT THE SECOND READ THAT ANSWERS NOTHING. The clause the note
above retired for the manifest read had been written a second time, word for
word, over `contracts/CHANGELOG.md`; the amendment that removed one left the
other standing, and said so before it landed. **THE TWO READS ARE NOT IN THE
SAME POSITION, AND THAT DIFFERENCE IS WHAT THIS AMENDMENT RECORDS RATHER THAN
COPIES OVER.** The changelog read has no presence probe of its own — it INHERITS
the manifest read's, and it inherits it COMPLETELY, because the manifest is read
AT THE SAME COMMIT and must have answered before this arm can be reached. A blob
cannot be read out of a commit the checkout does not hold, so by the time the
changelog answers nothing the unfetched fact is not merely the rarer one: IT IS
EXCLUDED, and the only fact left standing is a tip this checkout holds that
carries no `contracts/CHANGELOG.md`. Naming the other one is therefore not a bad
guess but a statement the family's own position already contradicts — so the
skip SHALL say WHICH FACT HOLDS and SHALL state the presence, rather than leave
a reader of the report to infer a fetch defect that cannot be there.

**Removed from canon by amend-unreadable-read-sibling-scenarios (2026-09-05):**
``**WHEN** the blob read for `contracts/CHANGELOG.md` at the published tip answers nothing — the commonest cause being a checkout that has not fetched that commit`` — the
clause after the dash names one of two causes as the commonest, and at this read
the one it names is the one that cannot hold at all; the unit is REPLACED rather
than deleted, by the `WHEN` that names both facts and the `AND` that requires
the family to have established which of them holds before it speaks. Nothing
else in this requirement is dropped.

#### Scenario: The declaring commit is still the published tip
- **WHEN** a repository declares a bundle at or above the enforcement line, that bundle has no published annotated tag, and the earliest commit declaring it is still the tip of published `main`
- **THEN** the family MUST emit no finding, because the cut has only just landed and the owner's tag act legitimately follows it
- **AND** the family MUST NOT record this as a pass that discharges the obligation, which remains owed

#### Scenario: Landings have accumulated on an untagged declared bundle
- **WHEN** the bundle has no published annotated tag and further first-parent commits have landed on published `main` above the earliest commit declaring it, up to and including the configured threshold
- **THEN** the family MUST emit a `warning` naming the bundle, the declaring commit, and how many first-parent landings have accumulated
- **AND** the action MUST name publishing the annotated tag at the commit the policy's rule identifies, never editing the manifest, the changelog or the inventory to match the absence

#### Scenario: An untagged declared bundle passes the threshold
- **WHEN** the accumulated first-parent landings exceed the configured threshold
- **THEN** the family MUST emit an `error`, because a bundle being consumed while unpublished is the state the policy calls a breach rather than an exception
- **AND** the finding MUST say that the bundle is NOT PUBLISHED in the policy's own terms, so no reader infers from its presence in the manifest that it was released

#### Scenario: The declared bundle carries an annotated tag on a declaring commit
- **WHEN** the bundle has a published annotated tag and that tag peels to a commit whose manifest declares that same bundle
- **THEN** the family MUST emit no finding

#### Scenario: A tag exists but peels to a commit that does not declare the bundle
- **WHEN** the bundle has a published annotated tag and the commit it peels to does not declare that bundle
- **THEN** the family MUST emit an `error` in DIFFERENT WORDS from the absent-tag findings, naming it a MISPLACED tag and naming both the commit it peels to and the bundle that commit actually declares, if any
- **AND** this MUST NOT be graded by distance, because a misplaced tag is not a release in progress and no interval makes it correct

#### Scenario: The published tag is lightweight rather than annotated
- **WHEN** a ref of the bundle's tag name exists but is not an annotated tag object
- **THEN** the family MUST emit an `error` naming the ref as lightweight, never treat it as satisfying the obligation, and never report it in the absent-tag words

#### Scenario: A bundle below the enforcement line
- **WHEN** the declared bundle is below the version at which mandatory tag publication begins
- **THEN** the family MUST emit no finding, and MUST NOT report the legacy sequence's untagged bundles at any severity

#### Scenario: A bundle was cut, superseded, and never tagged
- **WHEN** a repository has a release inventory for a bundle at or above the enforcement line, that bundle has no published annotated tag, and the manifest now declares a different bundle
- **THEN** the family MUST emit an `error` naming the superseded bundle and the bundle that replaced it, and MUST NOT grade it by distance — the window it would be graded against closed when the next cut replaced it
- **AND** the action MUST name retro-publication at the commit the policy's rule identifies, never a re-dating and never an edit to the inventory
- **AND** this MUST hold wherever no accepted SPENT declaration names that bundle — silence, an absent changelog record, and a REFUSED declaration all leave this scenario in force, while a PROVISIONAL one (well formed, its later successor cut but not yet published) SUPPRESSES it in favour of its own `warning`, the successor being graded on its own account

#### Scenario: A superseded bundle is declared SPENT and its successor is published
- **WHEN** a bundle has a release inventory, has no published annotated tag, the manifest has moved on from it, `contracts/CHANGELOG.md` at the published tip carries exactly one SPENT declaration naming it — carrying the superseding bundle, the cause, the ruling's author and date, and the measurement of record — inside the changelog entry of that superseding bundle, and that superseding bundle has itself a published annotated tag peeling to a commit that declares it
- **AND** that superseding bundle's version is STRICTLY GREATER than the spent bundle's
- **THEN** the family MUST NOT emit the superseded-and-never-published `error`, and MUST instead emit exactly one `info` on `contracts/releases/<spent bundle>.digests.yaml` naming the spent bundle, the bundle that superseded it, and where the record is
- **AND** that `info` MUST be classed `contested`, so that its disappearance without a cited change is re-raised rather than read as a resolution — the state is permanent, and the only way it stops being reported is that the inventory or the declaration was removed
- **AND** the family MUST NOT record it as the tag obligation having been met, which it was not: it was extinguished by an owner act at the cost of a version number

#### Scenario: A SPENT declaration names a superseding bundle that is not itself published
- **WHEN** a SPENT declaration carries every element it owes and the superseding bundle it names has a release inventory but no published annotated tag
- **THEN** the family MUST emit a `warning` on `contracts/releases/<spent bundle>.digests.yaml` saying the supersession is UNPROVEN, because a bundle is not published until its tag exists and a successor that is not published cannot yet be shown to have carried anything forward
- **AND** the family MUST NOT emit the `info`, and MUST NOT ALSO emit the superseded-and-never-published `error` for that bundle — this state is PROVISIONAL rather than REFUSED, ONE finding is reported and not two, and reporting both would contradict the ruling that this case is a `warning`
- **AND** the family MUST NOT suppress the SUCCESSOR's own finding, which is raised on the successor's own account by the scenarios above and is what bounds this band: past the successor's threshold the estate carries an `error` again, on the bundle that owes the tag

#### Scenario: A SPENT declaration names a superseding bundle this repository never cut
- **WHEN** a SPENT declaration names as its superseding bundle a name for which the repository holds no release inventory
- **THEN** the family MUST emit an `error` on `contracts/releases/<spent bundle>.digests.yaml` saying the declaration names a bundle that was never cut, because retiring a number by pointing at one that does not exist is the abuse this state is most exposed to
- **AND** the superseded-and-never-published `error` on the spent bundle MUST also stand, so that a bad declaration removes nothing

#### Scenario: A SPENT declaration names a superseding bundle that is not later than the bundle it supersedes
- **WHEN** a SPENT declaration is well formed, and the superseding bundle it names is cut and carries a published annotated tag on a declaring commit, but its version is not STRICTLY GREATER than the spent bundle's — including the case of a declaration written into an earlier, already-published bundle's changelog entry and naming that earlier bundle
- **THEN** the family MUST emit an `error` and MUST accept nothing, because a tag that already existed before the spent bundle was cut is not a replacement for it, and a guard satisfied by an earlier release has been walked around backwards rather than met
- **AND** the superseded-and-never-published `error` on the spent bundle MUST also stand, so that no untagged bundle goes quiet without a LATER published one

#### Scenario: A SPENT declaration's SUBJECT is a bundle this repository never cut
- **WHEN** a SPENT declaration's SUBJECT — the bundle it declares spent — is a name for which the repository holds no release inventory
- **THEN** the family MUST emit a `warning` on `contracts/CHANGELOG.md` saying the declaration disposes nothing, this being the one finding of this state that has no per-bundle inventory to land on
- **AND** it MUST NOT be read as disposing any other bundle, because a mistyped subject leaves the real bundle undeclared — and that bundle is still reported by the scenarios above, which is the fail-closed behaviour a typo must not be able to defeat

#### Scenario: A SPENT declaration omits an element it owes
- **WHEN** a declaration of the reserved form is present and any of the superseding bundle, the cause, the ruling's author, the ruling's date or the measurement of record is absent or empty
- **THEN** the family MUST emit an `error` on `contracts/releases/<spent bundle>.digests.yaml` naming which element is missing, and MUST NOT accept the declaration
- **AND** it MUST NOT report that omission in the absent-tag words, because a malformed declaration is worse than none: it looks like a record

#### Scenario: A SPENT declaration sits outside its superseding bundle's own changelog entry
- **WHEN** a well-formed SPENT declaration names a superseding bundle other than the one whose changelog entry contains it, including a declaration written inside the spent bundle's own entry
- **THEN** the family MUST emit an `error` and MUST NOT accept it, because the act that spends a number is the LATER CUT that allocates its replacement
- **AND** a bundle that could declare itself spent could decline to be published, which is the whole of what this family refuses

#### Scenario: More than one SPENT declaration names the same bundle
- **WHEN** `contracts/CHANGELOG.md` carries two or more SPENT declarations naming one bundle
- **THEN** the family MUST emit an `error` and MUST accept none of them, because two records of one disposition is how they come to disagree

#### Scenario: Two different bundles are each declared SPENT
- **WHEN** two bundles are each named by their own accepted SPENT declaration, under their own superseding bundles
- **THEN** the family MUST emit ONE `info` per spent bundle, each on that bundle's OWN release inventory path, so the two findings carry DIFFERENT identities
- **AND** removing either declaration MUST re-raise that bundle's state on its own — a shared path would leave the surviving finding holding the identity, and the removal would be reported by nothing

#### Scenario: A SPENT declaration names the bundle the manifest currently declares
- **WHEN** a SPENT declaration names the bundle `contracts/manifest.yaml` declares at the published tip
- **THEN** the family MUST emit an `error` and MUST NOT accept it, because a repository declaring a bundle it also calls spent asserts two incompatible things about one number
- **AND** that bundle MUST continue to be graded by distance exactly as it is today

#### Scenario: A SPENT declaration does not quiet a misplaced or lightweight tag
- **WHEN** a bundle named by an accepted SPENT declaration nevertheless carries a published ref of its own name — annotated but peeling to a commit that declares something else, or lightweight
- **THEN** the family MUST report that ref exactly as it does today, at `error` and in the MISPLACED or LIGHTWEIGHT words
- **AND** the SPENT state MUST reach the ABSENT-tag arm and nothing else

#### Scenario: The changelog cannot be read at the published tip
- **WHEN** the blob read for `contracts/CHANGELOG.md` at the published tip answers nothing — ONE ANSWER STANDING FOR TWO DIFFERENT FACTS: the commit is not in this checkout's object store, or the commit IS held and carries no `contracts/CHANGELOG.md` at all
- **AND** the family has ESTABLISHED WHICH OF THE TWO HOLDS before choosing the words it reports — here by INHERITANCE and completely, the manifest read at that SAME COMMIT having already answered, which a commit this checkout does not hold cannot do — rather than naming a cause it did not check
- **THEN** the family MUST report a skip naming that read, and MUST NOT treat the absence of a declaration it could not look for as the absence of a declaration
- **AND** where the commit IS held and simply carries no `contracts/CHANGELOG.md`, the skip MUST SAY THAT and MUST state the presence, because a tip this checkout holds is an ANSWER rather than a read that failed, and reporting it in the unfetched case's words sends a reader to look for a fetch defect that does not exist
- **AND** this is the same conflation the manifest read already guards one document over: not fetched is not an answer, in either direction

#### Scenario: The bundles untagged before this state existed are not retrofitted
- **WHEN** the family reads the five bundles the versioning policy records under § Untagged Bundles After Enforcement Began
- **THEN** no finding about any of them changes, because all five were publishable and all five were published: they carry annotated tags on declaring commits and never reach this arm
- **AND** the SPENT state MUST NOT be read backwards onto them, nor onto any bundle below the enforcement line

#### Scenario: The manifest cannot be read at the published tip
- **WHEN** the blob read for the manifest at the published tip answers nothing — ONE ANSWER STANDING FOR TWO DIFFERENT FACTS: the commit is not in this checkout's object store, or the commit IS held and carries no manifest at all
- **AND** the family has ESTABLISHED WHICH OF THE TWO HOLDS before choosing the words it reports — asking whether the commit is present, and attempting ONE BOUNDED FETCH of exactly that commit where it is not — rather than naming a cause it did not check
- **THEN** the family MUST report a skip saying so, and MUST NOT report it as the repository declaring no bundle
- **AND** where the commit IS present and simply carries no manifest, the skip MUST say THAT instead and MUST state the presence, because a tip this checkout holds is an ANSWER rather than a read that failed, and reporting it in the unfetched case's words sends a reader to look for a fetch defect that does not exist
- **AND** the same MUST hold for the commit a tag peels to, so a tag pointing at an unfetched commit is never reported as a tag pointing at a commit that declares nothing — this is the conflation `verify_tag` is filed for at #338, and a family that repeated it would be reporting the benign case in the serious case's words

#### Scenario: A repository declares no bundle
- **WHEN** a repository in scope carries no declared contract bundle at all
- **THEN** the family MUST report a skip naming the reason, never an empty pass

#### Scenario: Version control cannot answer
- **WHEN** the git dependency is unavailable, the repository's tag refs cannot be listed, or the declaring commit cannot be resolved
- **THEN** the family MUST report a skip naming which of those it was, never a finding
- **AND** the family MUST NOT read a tag's existence from a local ref alone where the published refs could not be consulted, because an unpushed local tag is not a published tag

#### Scenario: A pull request that touches no release surface path while a bundle is untagged
- **WHEN** a bundle is declared and has no published annotated tag, and a pull request changes neither `contracts/manifest.yaml` nor any file under `contracts/releases/`
- **THEN** the cut-time check MUST report success on that pull request WITHOUT consulting the family about its tree, so that a pending tag act is never another lane's merge blocker
- **AND** the nightly report MUST go on carrying that bundle at the severity the scenarios above give it, the relief being to the pull request and never to the record

#### Scenario: A cutting pull request while an earlier bundle is still untagged
- **WHEN** a pull request changes the release surface and the tree it would produce carries a bundle that this requirement's scenarios above report at `error` or at `warning`
- **THEN** the cut-time check MUST fail, naming the bundle and the finding in the family's own words
- **AND** the failure MUST be carried by that pull request alone, because it is the one asserting that the release surface is in order

#### Scenario: A cutting pull request declares a bundle that cannot be tagged yet
- **WHEN** a pull request changes the release surface, the bundle it declares has no published annotated tag, and the commit declaring it is the tip of the tree under judgment
- **THEN** the cut-time check MUST report success, because the tag is published after the merge at the commit that landed and demanding it earlier would be unsatisfiable
- **AND** the check MUST RECORD the outstanding tag in its own report, naming the bundle, so that success is not read as the obligation having been discharged
- **AND** the nightly report MUST continue to report that bundle until the tag exists

#### Scenario: A cutting pull request moves the declaration onto a bundle that is already published
- **WHEN** a pull request changes the release surface, the bundle it declares differs from the one its base declares, and that bundle already has a published tag peeling to a commit OTHER than the tree under judgment
- **THEN** the cut-time check MUST fail, because a version number that has been published is never reused and a defective release is corrected by a superseding one
- **AND** a tag peeling to the tree under judgment itself MUST NOT be refused this way, that being the obligation met early rather than a number cut twice
- **AND** this reaches ONLY the MOVED declaration: where the base already declares the same bundle the check MUST NOT be read as covering the case, which the realization order's rebase-and-recheck step answers instead

#### Scenario: The cut-time check cannot ask the family's question
- **WHEN** a pull request changes the release surface and the family reports a skip over the tree under judgment — the published refs unlistable, a required blob unreadable, or a declaring commit unresolvable
- **THEN** the cut-time check MUST fail closed, naming the reason, because it is the enforcing moment and an unasked question is not a pass
- **AND** the nightly report MUST still be permitted to carry that same skip as an `info` with its reason, the two moments answering the same skip differently on purpose

#### Scenario: The repository's own test suite is asked what it asserts about this family
- **WHEN** the repository's test suite is read for assertions about this family over the repository itself
- **THEN** it MUST carry no assertion that the repository currently reads zero findings of this family
- **AND** it MUST still carry a positive control demonstrating, over a tree constructed to be untagged, that the family fires
