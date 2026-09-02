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

**AMENDED BY `declare-spent-bundle-state` (2026-09-02).** Everything above this
note stands exactly as promoted; everything from here to the scenarios is this
change's addition, and one `AND` bullet is added to the scenario *A bundle was
cut, superseded, and never tagged*. Nothing else in this requirement moves.

A SUPERSEDED BUNDLE MAY BE DECLARED SPENT, AND A SPENT BUNDLE IS THE THIRD STATE
THIS FAMILY OTHERWISE LACKS. Between *published* and *owes a tag* sits a number
that was cut, was never publishable, and never will be. The action the
superseded finding prescribes — retro-publication at the commit the policy's
rule identifies — is UNPERFORMABLE for such a bundle, and a finding whose only
prescribed action cannot be taken by anyone is one a reader learns to skip,
which is how a report loses the readers the rest of it needs. The family SHALL
therefore recognise a SPENT state, and SHALL recognise it ONLY from an EXPLICIT
DECLARATION.

SILENCE IS NEVER A DECLARATION, AND THAT SENTENCE CARRIES THE WHOLE OF THIS
STATE'S FAIL-CLOSED CHARACTER. An untagged superseded bundle that no declaration
names SHALL be reported exactly as it is today, at `error` and in the same
words. A bundle MUST NOT become spent by being old, by being ignored, by being
inconvenient, or by any absence whatsoever. Every state below is entered by a
record that exists and is refused by a record that does not.

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
keyed by `(family, repo, path)`; every finding this family raises against a
repository lands on `contracts/manifest.yaml`, so one entry would suppress EVERY
finding this family could ever raise about that repository — including the next
genuinely abandoned bundle. It lives at the AGGREGATION ROOT, so it is
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

``**SPENT BUNDLE:** `<bundle>` — SUPERSEDED BY `<superseding bundle>` — CAUSE:
<text> — RULED BY <author>, <YYYY-MM-DD> — MEASUREMENT: <citation>``

The opener `**SPENT BUNDLE:**` is RESERVED: no other text in
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

THE SUCCESSOR GUARD IS WHAT MAKES THE STATE UNABUSABLE, and it SHALL hold in
both directions. A SPENT declaration SHALL be quiet only where the superseding
bundle it names has itself been CUT and has itself been PUBLISHED — an annotated
tag peeling to a commit that declares it. So the only way to retire a number is
to publish its replacement's tag, which is the very act this family exists to
compel; a repository that walks away from a bundle by declaring it spent has
merely moved the obligation onto the successor, where the same check meets it
again. Where the successor is cut but not yet published the supersession is
UNPROVEN and the family SHALL `warning` rather than accept it; where the
successor was never cut at all the declaration points at nothing and the family
SHALL `error`.

A CORRECTLY DECLARED SPENT BUNDLE IS RECORDED, NOT SILENT. The family SHALL emit
exactly one `info` for it, on `contracts/CHANGELOG.md` rather than on the
manifest, naming the spent bundle, the bundle that superseded it, and where the
record is. It is recorded because a reader who finds a release inventory with no
matching tag is owed the answer in the report rather than only in a changelog
they may not read, and because THE PATH IS THE POINT: landing it on the document
that carries the declaration gives the state its own finding key, distinct from
every other finding of this family, which is what lets its disappearance be
noticed at all. The `info` SHALL be classed `contested` for exactly that reason
— a spent state that stops being reported has had its inventory or its
declaration removed, and *"never edit the manifest, the changelog or the
inventory to match the absence"* is the sentence this family already prescribes.
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
- **AND** this MUST hold wherever no accepted SPENT declaration names that bundle — silence, an absent changelog record, and a refused declaration all leave this scenario in force

#### Scenario: A superseded bundle is declared SPENT and its successor is published
- **WHEN** a bundle has a release inventory, has no published annotated tag, the manifest has moved on from it, `contracts/CHANGELOG.md` at the published tip carries exactly one SPENT declaration naming it — carrying the superseding bundle, the cause, the ruling's author and date, and the measurement of record — inside the changelog entry of that superseding bundle, and that superseding bundle has itself a published annotated tag peeling to a commit that declares it
- **THEN** the family MUST NOT emit the superseded-and-never-published `error`, and MUST instead emit exactly one `info` on `contracts/CHANGELOG.md` naming the spent bundle, the bundle that superseded it, and where the record is
- **AND** that `info` MUST be classed `contested`, so that its disappearance without a cited change is re-raised rather than read as a resolution — the state is permanent, and the only way it stops being reported is that the inventory or the declaration was removed
- **AND** the family MUST NOT record it as the tag obligation having been met, which it was not: it was extinguished by an owner act at the cost of a version number

#### Scenario: A SPENT declaration names a superseding bundle that is not itself published
- **WHEN** a SPENT declaration carries every element it owes and the superseding bundle it names has a release inventory but no published annotated tag
- **THEN** the family MUST emit a `warning` on `contracts/CHANGELOG.md` saying the supersession is UNPROVEN, because a bundle is not published until its tag exists and a successor that is not published cannot yet be shown to have carried anything forward
- **AND** the family MUST NOT emit the `info`, and MUST NOT suppress the successor's own finding, which is raised on the successor's own account by the scenarios above

#### Scenario: A SPENT declaration names a superseding bundle this repository never cut
- **WHEN** a SPENT declaration names as its superseding bundle a name for which the repository holds no release inventory
- **THEN** the family MUST emit an `error` on `contracts/CHANGELOG.md` saying the declaration names a bundle that was never cut, because retiring a number by pointing at one that does not exist is the abuse this state is most exposed to
- **AND** the superseded-and-never-published `error` on the spent bundle MUST also stand, so that a bad declaration removes nothing

#### Scenario: A SPENT declaration omits an element it owes
- **WHEN** a declaration of the reserved form is present and any of the superseding bundle, the cause, the ruling's author, the ruling's date or the measurement of record is absent or empty
- **THEN** the family MUST emit an `error` on `contracts/CHANGELOG.md` naming which element is missing, and MUST NOT accept the declaration
- **AND** it MUST NOT report that omission in the absent-tag words, because a malformed declaration is worse than none: it looks like a record

#### Scenario: A SPENT declaration sits outside its superseding bundle's own changelog entry
- **WHEN** a well-formed SPENT declaration names a superseding bundle other than the one whose changelog entry contains it, including a declaration written inside the spent bundle's own entry
- **THEN** the family MUST emit an `error` and MUST NOT accept it, because the act that spends a number is the LATER CUT that allocates its replacement
- **AND** a bundle that could declare itself spent could decline to be published, which is the whole of what this family refuses

#### Scenario: More than one SPENT declaration names the same bundle
- **WHEN** `contracts/CHANGELOG.md` carries two or more SPENT declarations naming one bundle
- **THEN** the family MUST emit an `error` and MUST accept none of them, because two records of one disposition is how they come to disagree

#### Scenario: A SPENT declaration names the bundle the manifest currently declares
- **WHEN** a SPENT declaration names the bundle `contracts/manifest.yaml` declares at the published tip
- **THEN** the family MUST emit an `error` and MUST NOT accept it, because a repository declaring a bundle it also calls spent asserts two incompatible things about one number
- **AND** that bundle MUST continue to be graded by distance exactly as it is today

#### Scenario: A SPENT declaration does not quiet a misplaced or lightweight tag
- **WHEN** a bundle named by an accepted SPENT declaration nevertheless carries a published ref of its own name — annotated but peeling to a commit that declares something else, or lightweight
- **THEN** the family MUST report that ref exactly as it does today, at `error` and in the MISPLACED or LIGHTWEIGHT words
- **AND** the SPENT state MUST reach the ABSENT-tag arm and nothing else

#### Scenario: The changelog cannot be read at the published tip
- **WHEN** the blob read for `contracts/CHANGELOG.md` at the published tip answers nothing — the commonest cause being a checkout that has not fetched that commit
- **THEN** the family MUST report a skip naming that read, and MUST NOT treat the absence of a declaration it could not look for as the absence of a declaration
- **AND** this is the same conflation the manifest read already guards one document over: not fetched is not an answer, in either direction

#### Scenario: The bundles untagged before this state existed are not retrofitted
- **WHEN** the family reads the five bundles the versioning policy records under § Untagged Bundles After Enforcement Began
- **THEN** no finding about any of them changes, because all five were publishable and all five were published: they carry annotated tags on declaring commits and never reach this arm
- **AND** the SPENT state MUST NOT be read backwards onto them, nor onto any bundle below the enforcement line

#### Scenario: The manifest cannot be read at the published tip
- **WHEN** the blob read for the manifest at the published tip answers nothing — the commonest cause being a checkout that has not fetched that commit
- **THEN** the family MUST report a skip saying so, and MUST NOT report it as the repository declaring no bundle
- **AND** the same MUST hold for the commit a tag peels to, so a tag pointing at an unfetched commit is never reported as a tag pointing at a commit that declares nothing — this is the conflation `verify_tag` is filed for at #338, and a family that repeated it would be reporting the benign case in the serious case's words

#### Scenario: A repository declares no bundle
- **WHEN** a repository in scope carries no declared contract bundle at all
- **THEN** the family MUST report a skip naming the reason, never an empty pass

#### Scenario: Version control cannot answer
- **WHEN** the git dependency is unavailable, the repository's tag refs cannot be listed, or the declaring commit cannot be resolved
- **THEN** the family MUST report a skip naming which of those it was, never a finding
- **AND** the family MUST NOT read a tag's existence from a local ref alone where the published refs could not be consulted, because an unpushed local tag is not a published tag

