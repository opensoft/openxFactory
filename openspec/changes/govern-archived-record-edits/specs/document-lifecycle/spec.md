# document-lifecycle

## MODIFIED Requirements

### Requirement: Proposal packets carry the lifecycle header
An OpenSpec change packet's `proposal.md`, and EVERY `review/` record under that packet, SHALL be governance documents for the purposes of the controlled status taxonomy and the ratification-citation rule.

Both carry a claim about the document's standing — a proposal says whether it
is `draft` or `ratified`; a review record says what standing its own finding
has, whether that is a ratification, a captured `record` of a review that
happened, or a superseded earlier round. A claim of standing is what the
taxonomy exists to make checkable, and a review record makes one whatever its
subject. The rest of the packet is deliberately NOT ruled here: `tasks.md`,
`design.md`, spec delta files, `supporting-docs/` and `evidence/` are working
files of the change rather than documents making a standing claim, and whether
they are governance documents is a separate question this capability leaves
open.

The two obligations this requirement creates are DIFFERENT in reach, and
conflating them would over-state the rule:

- The **taxonomy** obligation reaches every document named above. A
  `review/` record SHALL carry a `Status:` header drawn from the controlled
  taxonomy, within the lifecycle header window, whatever its subject. A
  review record that is not about a ratification most often carries
  `Status: record`, which is a conforming value and needs nothing further.
- The **ratification-citation** obligation reaches only those documents whose
  status IS `ratified`. A `review/` record carrying any other taxonomy value
  owes no citation, and demanding one of a `record` would be demanding
  provenance for a claim the document does not make.

A `review/` record whose status IS `ratified` and which names its ratifier and
decision date in its own vocabulary SHALL additionally carry a citation in one
of the two sanctioned spellings. Recording the same fact twice is the cost of
having one rule; inventing a third spelling for documents whose whole subject
is ratification would undo the single-rule result the two-spelling sanction
reached.

The pre-existing population SHALL be discharged rather than grandfathered:
this requirement defines NO contract date and NO reduced-severity legacy
class, so a packet carrying no `Status:` header is a current violation
whenever it was authored. Backfilling a header onto an archived packet is an
archived-record edit and takes the route archived-record edits take.

THAT ROUTE IS NOW STATED AND NOT ONLY NAMED. It is *An archived record is
edited only as a bookkeeping correction under a recorded ruling*, and a header
derived from the packet's own record is within that route's bookkeeping class;
it still takes the route's recorded ruling. Where the backfilled file is ALSO a pinned
target, *A change that edits a pinned target re-derives every dependent pin in
the same change* attaches as well and the backfill carries the re-derivation.
The two obligations are independent: clearing the first says nothing about the
second.

Deriving a header is nevertheless authoring, not correcting, and the rule is
bounded accordingly: a `Status:` value and, where that value is `ratified`,
its citation SHALL be derived from the packet's own record — its origin
declaration, its ratification or archive commit, its own task record, or the
index row that announced it. Where the record supports neither, the document
SHALL be reported by name, stating what its record does and does not carry,
and SHALL NOT be given a header the record does not support. A packet whose
own archive record states a decision against carrying a status value keeps
that decision; overturning it takes a ruling naming it, not a backfill pass.

#### Scenario: A proposal declares its standing
- **WHEN** a change packet's `proposal.md` is authored or amended
- **THEN** it MUST carry a `Status:` header drawn from the controlled taxonomy, within the lifecycle header window
- **AND** where that status is `ratified` it MUST carry exactly one ratification citation, in the spelling the citation's own condition of use selects

#### Scenario: A review record records a ratification
- **WHEN** a `review/` document under a change packet records that the change was ratified
- **THEN** it MUST carry `Status: ratified` and one ratification citation in a sanctioned spelling
- **AND** a `Ratifier:` or `Decision date:` header MAY accompany the citation but MUST NOT stand in place of it

#### Scenario: A review record is not about a ratification
- **WHEN** a `review/` document under a change packet records a finding, a disposition, a captured review round, or any other subject that is not the ratification of that change
- **THEN** it MUST still carry a `Status:` header drawn from the controlled taxonomy, within the lifecycle header window, because it is a governance document under this requirement whatever its subject
- **AND** it MUST NOT be required to carry a ratification citation, because the citation rule binds a `ratified` status and this document does not claim one

#### Scenario: A pre-existing packet carries no header
- **WHEN** a proposal packet authored at any date carries no `Status:` header
- **THEN** it MUST be reported as a current violation at full severity, because this requirement defines no contract date and no pre-contract legacy class
- **AND** the remedy MUST be a header derived from that packet's own record, not a reduced severity that leaves the claim unmade

#### Scenario: A record cannot support a derived header
- **WHEN** a packet's own record supports neither a `Status:` value nor, for a `ratified` value, a citation clearing the ratification floor
- **THEN** the document MUST be reported by name together with what its record does and does not carry
- **AND** a header the record does not support MUST NOT be written, because an invented provenance is a worse defect than the missing one it hides
- **AND** where the packet's archive record states a decision against carrying a status value, that decision stands until a ruling names it

#### Scenario: A packet working file carries no lifecycle header
- **WHEN** a change packet's `tasks.md`, `design.md`, spec delta, supporting document, or evidence file carries no `Status:` header
- **THEN** no finding is emitted under this requirement, because this requirement does not reach those files

#### Scenario: A header defect is discharged on an archived packet
- **WHEN** a missing or defective `Status:` header or ratification citation is repaired on a packet under `openspec/changes/archive/`
- **THEN** the repair MUST take the archived-record edit route — a ruling recorded before the edit, a bookkeeping note clearing the neutral minimum or the stricter form the repository's own convention requires, and nothing altered beyond the packet's own standing metadata
- **AND** where the edited file is a pinned target, every dependent pin MUST be re-derived and recorded in the same change
- **AND** a discharge that repairs the header and leaves a dependent pin naming bytes that no longer exist MUST be reported against the change that made it, a repair being incomplete while it holds a pin open

## ADDED Requirements

### Requirement: An archived record is edited only as a bookkeeping correction under a recorded ruling
A file under `openspec/changes/archive/` SHALL be edited ONLY as a
lifecycle-header or bookkeeping correction, under a ruling recorded BEFORE the
edit, and carrying a bookkeeping note; every other edit of an archived byte
SHALL be refused.

**THE NOTE HAS A NEUTRAL MINIMUM, BECAUSE THE PROMOTING REPOSITORY HAS NO
CONVENTION OF ITS OWN.** An earlier spelling of this requirement said "the
bookkeeping note the editing repository's own archived-packet convention already
requires", which is unsatisfiable where no such convention exists — and
openxFactory, the repository this capability is promoted in, HAS NONE. Only
OpsxFactory has written one down. A rule whose note obligation is delegated
entirely to local conventions is absent exactly where no local convention
exists, which would leave the loosest repository in the estate the one that
promoted the rule.

The minimum is therefore stated here: a DATED LINE in the edited file's OWN
lifecycle-header block — the block every governance document already carries
under *Controlled document status taxonomy* — of the form

`Edited (bookkeeping): <UTC date> by <change-id> — <edit class>`

A repository's own convention MAY be stricter and MUST NOT be absent;
OpsxFactory's note on the archived change's `tasks.md` is such a stricter form
and is unaffected. The note sits in the lifecycle header ON PURPOSE: that block
is the one part of an archived file this requirement already permits the edit to
touch, so recording the edit cannot itself become an edit the rule forbids.

**AN ARCHIVE IS NOT MERELY HISTORY, AND THAT IS WHY THIS RULE EXISTS.** Two
things in this corpus read archived bytes as CURRENT. *Ratified spec deltas
reach the promoted specification* makes "the MOST RECENT archived delta that
touches it, and that one alone" the authority for a promoted requirement — so
editing an archived delta edits the standard canon is checked against, with no
proposal, no review, and no ratification anywhere in the act. And archived
files are content-address TARGETS: consent instruments, evidence manifests and
digest inventories name them by locator and `sha256`, so an archived byte
moving silently breaks a pin somewhere else. An archived packet is a RECORD in
the taxonomy's own sense — captured once — and the whole value of a record is
that it says today what it said when it was captured.

**WHAT COUNTS AS BOOKKEEPING, AND WHAT DOES NOT.** A bookkeeping correction
adds or repairs the packet's OWN standing metadata and nothing the packet
ASSERTS: a `Status:` header or ratification citation derived from the packet's
own record; a corrected index row, path or cross-reference naming the packet; a
DATED AMENDMENT NOTE APPENDED BESIDE STALE TEXT THAT IS KEPT. It is NOT a spec
delta's requirement or scenario text, a task record or its tick state, a
decision, a measurement, a number, an evidence digest, or the deletion of any
of these. THE TEST IS WHETHER THE EDIT CHANGES WHAT THE ARCHIVED RECORD
ASSERTS, and it is deliberately a test of effect rather than a list of
filenames: `proposal.md` carries both classes, and a rule keyed to paths would
license a substantive rewrite inside a file the list called safe. Where the
edit does change an assertion, the route is a NEW change that supersedes, and
never an edit in place.

**THE RULING IS RECORDED BEFORE THE EDIT, AND THE NOTE IS NOT THE RULING.**
The recording SHALL name the ruler, the date, and the class of edit authorized,
and SHALL be resolvable — a ruling comment, a disposition, a review record, or
an approving change. A bookkeeping note written into the packet says WHAT was
changed; the ruling says THAT IT MAY BE. A convention satisfied by the note
alone authorizes every edit its author believed was bookkeeping, which is the
same thing as authorizing every edit.

**THE NARROW PERMISSION IS NOT A PRECAUTION — THE PERMISSIVE READING WAS TRIED
AND MEASURED.** OpsxFactory's `docs/packet-lifecycle-headers.md` § *Editing an
archived packet*, ratified 2026-08-24, permitted an archived-packet edit on a
bookkeeping note alone. On that same UTC day commit `57fd9fd2` ("Discharge all 55
lifecycle-header defects in the OpenSpec scan set", 63 files) wrote SIXTEEN
files under that repository's archive tree under it, inserting one `Ratified:`
line per target, and broke THREE executed consent instruments' `custody.sha256`
— one of them in a change directory that has never been archived, which is why
the class is pinned-target integrity and not archiving. It went thirteen days
unnoticed. Two packets in that repository had read `FR-072` as forbidding
archive writes; that was one feature's close-time fence, not a general rule, so
there was no general rule to break — the permissive convention was the whole of
the governance. This requirement is that general rule, stated estate-wide, and
its domain-realized twin is OpsxFactory's `govern-archived-record-edits`, which
states it over that repository's archive tree at the repository's own altitude.

**A REPOSITORY MAY BE STRICTER AND MAY NOT BE LOOSER.** A DomainxFactory's
local archived-packet convention SHALL be read as an ADDITION to this
requirement. A convention that permits an edit this requirement refuses is
superseded on that point by force of this rule, and remains in force for
everything it says that this rule does not reach.

#### Scenario: A lifecycle-header defect is discharged on an archived packet
- **WHEN** a change repairs a missing or defective `Status:` header or ratification citation on a file under `openspec/changes/archive/`
- **THEN** a ruling authorizing the class of edit MUST be recorded before the edit, naming ruler, date and class, and resolvable from the change
- **AND** the neutral minimum MUST be present — a dated `Edited (bookkeeping): <UTC date> by <change-id> — <edit class>` line in the edited file's own lifecycle-header block — whatever else the editing repository requires
- **AND** a stricter local convention MAY require a further note and MUST NOT stand in place of the minimum, a local form ADDING to the minimum rather than substituting for it
- **AND** nothing beyond the packet's own standing metadata may be altered in the same act

#### Scenario: An edit would change what an archived record asserts
- **WHEN** a proposed edit to an archived file would change a requirement or scenario, a task record or its tick state, a decision, a measurement, a number, an evidence digest, or would delete any of these
- **THEN** the edit MUST be refused whatever file it sits in and however small it is
- **AND** the correction MUST take the form of a new change that supersedes the archived record, the archived bytes staying as captured

#### Scenario: An archived-packet edit carries a note and no ruling
- **WHEN** an archived file is edited under a local convention satisfied by a bookkeeping note alone, with no ruling recorded before the edit
- **THEN** the edit MUST be reported, the note recording WHAT changed and never THAT IT MAY
- **AND** the report MUST name the archived files the change wrote, so the scope of an unruled edit is visible rather than inferred

#### Scenario: The editing repository has no archived-packet convention
- **WHEN** an archived-record edit is made in a repository that has written no archived-packet convention of its own
- **THEN** the neutral minimum applies unchanged — a dated `Edited (bookkeeping): <UTC date> by <change-id> — <edit class>` line in the edited file's own lifecycle-header block
- **AND** the absence of a local convention MUST NOT be read as the absence of a note obligation

#### Scenario: A local convention is more permissive than this requirement
- **WHEN** a repository's own archived-packet convention permits an edit this requirement refuses
- **THEN** this requirement governs and the convention is superseded on that point
- **AND** the convention MUST be amended by a DATED AMENDMENT that keeps its stale text rather than by a rewrite, an archived-record rule that erased its own history being self-refuting

### Requirement: A change that edits a pinned target re-derives every dependent pin in the same change
A change that edits a PINNED TARGET SHALL re-derive every dependent pin and
SHALL RECORD the re-derivation in the SAME change, by the rule that pin's own
family declares. A PINNED TARGET is any file that an in-repo content-address pin
names, whether that file is ARCHIVED OR LIVE.

**THE REACH IS PINS, NOT THE ARCHIVE.** This requirement and its neighbour
above are stated separately because their failures are invisible to each other.
That one is unmet when an archived record is edited outside the bookkeeping
class. THIS one is unmet when a pin's target moves and the pin does not — and
the target need never have been archived. In the measured case one of the three
broken pins named a change directory that has never archived at all, so a rule
scoped to the archive tree would have left it broken while reporting itself
satisfied.

**THE OBLIGATION THIS REQUIREMENT CREATES IS THE RECORDING; THE DETECTION IS
THE GATES'.** Nothing here asks an author to notice a broken pin unaided, and a
rule that did would be a rule discharged by diligence. What this requires is
that a change which knows it is editing a pinned target carries the
re-derivation. Making an unrecorded edit VISIBLE is the work of running gates —
the pre-archive citation gate and the content-address integrity gate in
OpsxFactory are the first two — and a repository that has no such gate owes
this obligation exactly as much, with nothing but review to catch a breach.

**PER FAMILY, BY THE FAMILY'S OWN RULE, WHICH THE FAMILY MUST DECLARE.**
Re-derivation is not one act: a consent instrument's custody pin, an evidence
digest, a plan-acceptance desired-state reference and a contract-bundle digest
each re-derive differently and record differently. A family's rule SHALL be
declared either in the declaring repository's content-address register OR in
the neutral contract that owns the family — both homes are real and the
distinction is not cosmetic: the consent family's rule is a property of the
INSTRUMENT SCHEMA and lives in the contract wherever the instrument is held,
while a repository-local family's rule has no contract to live in. For consent
instruments the rule is the structured `custody_rederivations[]` entry proposed
by `add-consent-custody-rederivation-record`, which is a CONTRACT home;
OpsxFactory's `add-content-address-integrity-gate` proposes the estate's first
REGISTER home.

**A FAMILY THAT DECLARES NO RE-DERIVATION RULE HAS NOT EARNED A PIN — AND THE
CONSEQUENCE ARRIVES WITH THE DECLARATION, NOT WITH THIS REQUIREMENT.** Until a
family has declared its rule, an edit of that family's pinned target SHALL be
REPORTED — naming the family, the pinned target, and the register or contract
that owes the rule — and SHALL NOT be refused on that ground. It becomes a
REFUSAL for that family on the day that family declares, and thereafter an
ad-hoc re-derivation performed for the occasion is not accepted in place of the
declared rule, because "re-derive by whatever means" is a promise nobody can
check and nobody can repeat.

**THE TRANSITION IS NOT A SOFTENING; IT IS WHAT KEEPS THE RULE FROM FREEZING
THE ESTATE ON THE DAY IT LANDS.** Measured at this packet's authoring: NO
family anywhere in the estate has a declared re-derivation rule. The consent
family's is PROPOSED and not declared — the contract still reads
`contract_schema_version: 2`, the schema carries no `custody_rederivations`
property, and all 46 boxes of the proposing packet are unticked. The register
home does not exist at all: `models/content-address-families.yaml` is absent
from OpsxFactory's `main` AND from the branch that proposes it, where it is
task 2.1. A refuse-on-landing reading would therefore refuse EVERY pinned-target
edit in the estate from the moment this requirement is promoted — including the
routine lifecycle-header discharge that the neighbouring requirement and
*Proposal packets carry the lifecycle header* both require to be performed. A
rule whose first act is to forbid the corrective work it exists to govern is a
rule that will be worked around rather than followed.

**"IN THE SAME CHANGE" IS THE WHOLE OF IT.** A re-derivation deferred to a
successor is a broken pin with a promise attached, and the promise is not what
the pin's consumer reads. Where the dependent pin lives in another repository,
the same change SHALL record the owed consumer act by name, and the consumer's
re-pin is that repository's change — deferral ACROSS a boundary is legitimate
because the bytes are not in one tree; deferral WITHIN one is not.

**AN EDIT THAT CANNOT RE-DERIVE ITS DEPENDENTS MAY NOT LAND.** Where a
dependent pin cannot be re-derived — the target cannot be resolved through its
declared mapping, or the re-derivation does not verify — the correct outcome is
a REFUSAL naming what could not be derived, never an edit that lands with the
question open. Converting "cannot tell" into "fine" is precisely the state the
measured case sat in for thirteen days. **An UNDECLARED RULE is deliberately
NOT in that list**: it is not a failed re-derivation but an absent obligation,
it is the state of every family in the estate today, and it takes the REPORT
above rather than a refusal until that family declares.

#### Scenario: A pinned target's bytes change
- **WHEN** a change edits a file that an in-repo content-address pin names, whether that file is archived or live
- **THEN** every dependent pin MUST be re-derived and the re-derivation MUST be recorded in that same change, by the rule the pin's family declares
- **AND** a change that edits the target and moves no dependent pin MUST be reported against its own commit

#### Scenario: A pinned target's path changes
- **WHEN** a pinned target is moved or renamed and its bytes are unchanged
- **THEN** the dependent pin's locator MUST be re-derived in the same change and the record MUST say that the bytes did not change
- **AND** an unchanged digest MUST NOT be read as an unchanged pin, a locator being half of a content address

#### Scenario: A pin's family has not yet declared a re-derivation rule
- **WHEN** a change edits a pinned target whose family has declared no re-derivation rule, in either home
- **THEN** the edit MUST be REPORTED, naming the family, the pinned target, and the content-address register or neutral contract that owes the rule
- **AND** it MUST NOT be refused on that ground, an absent obligation being a different fact from a failed re-derivation
- **AND** the report MUST NOT be read as a re-derivation having been performed

#### Scenario: A family has declared its rule and an edit does not follow it
- **WHEN** a family has declared its re-derivation rule, in its register or in the neutral contract that owns it, and a change edits one of its pinned targets without following that rule
- **THEN** the edit MUST be refused
- **AND** an ad-hoc re-derivation performed for the occasion MUST NOT be accepted in place of the declared rule

#### Scenario: A dependent pin lives in another repository
- **WHEN** the pin depending on the edited target is held by a consuming repository
- **THEN** the editing change MUST record the owed consumer re-pin by name, repository and instrument
- **AND** the consumer's own change MUST carry the re-derivation, cross-boundary deferral being legitimate exactly because the bytes are not in one tree

#### Scenario: A dependent pin cannot be re-derived
- **WHEN** a dependent pin's target cannot be resolved, or the re-derivation does not verify
- **THEN** the change MUST be refused, naming the pin and what could not be derived
- **AND** the edit MUST NOT land on the reading that an underivable pin is an unaffected one
