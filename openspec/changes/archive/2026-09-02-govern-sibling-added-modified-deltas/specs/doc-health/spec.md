# doc-health Specification Delta

TWO ADDED REQUIREMENTS AND ONE MODIFIED, AND THE MODIFIED ONE IS NOT THE
REQUIREMENT D2 MEASURES. No `## MODIFIED Requirements` block is opened on
"Currency of an active change's MODIFIED requirement blocks" — the same
measurement `add-unclassified-finding-class` recorded as its D1 holds for that
requirement and is re-taken against today's canon in the proposal's
§ Orchestrator Decisions D2.

THE BLOCK BELOW IS OPENED ON A DIFFERENT REQUIREMENT, "A modified-block-currency
finding its own class map cannot place is itself a finding", and it is opened
for a reason that has nothing to do with the two new classes. That requirement
says the family "SHALL remain absent from `FAMILY_RESOLUTION`"
(`openspec/specs/doc-health/spec.md:2088`), with a scenario at `:2126` resting a
MUST on that absence — and on 2026-08-31 the family JOINED the table, at
`7f656980` (PR #529), which amended no specification. Canon and code contradict
each other on `main` today. A packet adding two classes to that same family
cannot archive alongside a promoted requirement its own design contradicts, so
the contradiction is SUPERSEDED here rather than named and left standing: canon
catches up with a row the code already carries, and #529 is regularized by the
successor rather than by a reversion.

AND THE THIRD MENTION IS NAMED RATHER THAN MISSED. Promoted `doc-health` says
`FAMILY_RESOLUTION` in three places, and only two are superseded here. The third
is at `:1726`, inside "Currency of an active change's MODIFIED requirement
blocks" — "the family is deliberately absent from `FAMILY_RESOLUTION`, so its
findings are not classified `contested`". That sentence is NOT in the same
position as `:2088`, and the difference is in the promoted text itself: it sits
under "This family SHALL be advisory AT LAUNCH", and the same paragraph RESERVES
its own reversal — "Raising the scenario-completeness arm to `error` and adding
the contested classification are ONE later decision taken together by ruling,
and SHALL follow the discharge of the standing population rather than precede
it". `7f656980` is that decision, taken together, on a measured population of
zero everywhere. A launch state a requirement provides for leaving is SPENT when
the reserved act is taken; it is not contradicted by it. `:2088` reserves
nothing — it is an unconditional SHALL with a MUST resting on it — which is why
it, and it alone, needs superseding. Restating a ~290-line requirement with 14
scenarios to freshen a description its own text already retired is the cost D2
measured and declined.

THE CARRIAGE OF THAT BLOCK, STATED AS MEASURED RATHER THAN AS SUMMARISED. Canon
carries THIRTY-FIVE units for that requirement — 10 body sentences, 6 scenario
titles, 19 scenario bullets. THIRTY-THREE are restated BYTE-IDENTICAL. TWO are
dropped, and both are declared by one `Removed from canon by` marker naming each
as a code span: the body sentence asserting the absence, and the last bullet of
"The class map grows the pattern the drift named", whose reason clause rests on
it. Everything else the block adds is NEW text — four body paragraphs, one
replacement bullet and two scenarios — so the carriage ledger and the
scenario-title arm report nothing against this delta, asserted in `tasks.md`
§ 4.2 rather than assumed.

## ADDED Requirements

### Requirement: A MODIFIED block over an active sibling's addition is evaluated for its pairing, not for its carriage
The modified-block-currency family SHALL evaluate every `## MODIFIED
Requirements` block whose title resolves to an active change's ADDED or RENAMED
requirement — the shape its resolver returns as `pending` — and SHALL report the
pairing where it is undeclared, misdeclared, self-referential, or declared over
a basis that is not ratified without the disclosure `document-lifecycle`
requires of the marker, placing every such block in EXACTLY ONE of those states,
instead of dropping the block before its checks run.

**NOTHING IS COMPARED, AND THAT RULING STANDS.** Synthesising a basis from the
sibling's ADDED text was ruled against on 2026-08-27 for a reason that has not
changed: it would measure a block against text no promoted requirement carries.
The three comparison arms this family's currency requirement defines therefore
do NOT run against such a block, and this requirement adds no fourth comparison
arm — it adds a check on the PAIRING, whose inputs are the delta's own marker
and the set of active additions, and which compares no requirement text at all.
What was wrong was never that the arms declined; it was that the block was
dropped before anything at all looked at it, so the arms' silence read as
clearance when it was uncomparability.

**THE CHECK SHALL REPORT EXACTLY FOUR STATES, be silent on the fifth, and PLACE
EVERY BLOCK IN EXACTLY ONE OF THEM.** The five are MUTUALLY EXCLUSIVE BY
DEFINITION rather than by convention: they are examined IN THE ORDER WRITTEN
BELOW, a block placed in one state is NOT examined for any state below it, and
each state's antecedent below carries the exclusion that order performs. One
block therefore yields at most one finding of this class, and the words a reader
is given are never a choice between two true descriptions of one defect.

**THE CLASSIFICATION READS THE BLOCK'S WHOLE MARKER SET, AND THE COUNT IS THE
FIRST THING IT READS OF IT.** The family's derivation preserves EVERY paragraph
of marker form a block carries, in document order, so "the marker" is a SET and
not a singular the check may pick a member from. `document-lifecycle` bounds
that set — AT MOST ONE marker of the `Modified over` form per block, one pairing
and one declaration — and the states below are predicates over the WHOLE set
rather than over a chosen member of it. The checks therefore run in this order:
the carrier's own addition; then the COUNT of pairing markers; then, for the
single marker a lawful block carries, its basis, then its `by` identifier, THEN
ITS REASON, then its disclosure.
**A BLOCK IS DECLARED AND RESOLVING, OR UNDISCLOSED, ONLY WHERE
EXACTLY ONE PAIRING MARKER STANDS AND IT PASSES EVERY CHECK ABOVE IT; OTHERWISE
THE BLOCK IS PLACED BY THE FIRST CHECK IT FAILS, IN THAT ORDER.** Without the
count the promise this requirement makes is not kept by the states themselves: a
block carrying one valid marker and one naming a change that adds nothing
satisfies MISDECLARED and DECLARED AND RESOLVING at once, and which of the two a
run reported would be settled by which marker an implementation happened to look
at — the same false provenance accepted or refused by an accident of iteration
order.

- **SELF-REFERENTIAL** — the change that carries the block ADDS the block's
  capability and requirement title in its OWN `## ADDED Requirements` block.
  Reported, and a marker naming the change itself MUST NOT clear it. **THIS STATE
  IS EXAMINED FIRST AND EXCLUDES THE OTHER FOUR**, because it is a fact about the
  DELTA and not about the marker: a self-referential block carrying no marker is
  reported here and NOT as UNDECLARED, and one carrying any marker at all is
  reported here and NOT as MISDECLARED. Its remedy is to withdraw one of the two
  blocks, which no marker supplies, so a second finding over the same block would
  offer a remedy that does not reach the defect. **THE CARRIER'S OWN RENAME TO
  THE TITLE IS NOT THIS STATE**, for the reason the paragraph below states.
- **UNDECLARED** — the block is NOT self-referential and carries no marker of the
  reserved `Modified over` form. Reported.
- **MISDECLARED** — the block is NOT self-referential, carries at least one
  marker of the reserved form, and the declaration is wrong in one of the FOUR
  ways a declaration of this form can be wrong. **FIRST, THE COUNT**: the block
  carries MORE THAN ONE such marker, `document-lifecycle` admitting one pairing
  and one declaration, and this ground is read BEFORE the other three so that a
  block carrying a good marker and a bad one is placed by a fact about the BLOCK
  rather than by which marker was examined. Otherwise the block carries EXACTLY
  ONE, and that one is wrong in one of the remaining THREE ways: EITHER the change
  it names AS BASIS is not an active change
  OTHER THAN THE CARRIER that ADDS or RENAMES to the block's capability and
  requirement title — it names a change that neither adds nor renames to that
  title, or it names the carrying change itself — OR its `by` identifier is not
  the change that carries the block — OR it CARRIES NO REASON, the ` — <reason>`
  tail `document-lifecycle` requires being absent, or present and empty, so that
  the declaration the marker makes is one that capability calls incomplete.
  **AND THOSE THREE ARE READ IN THAT ORDER — basis, then `by`, then reason** —
  the single marker's own fields taken in the order its form writes them, so
  that one finding names the field a repair actually touches and a marker wrong
  in two of them is repaired from the front. Reported, and reported apart from UNDECLARED
  in the finding's own words, because a wrong basis and an absent one have
  different remedies. **THE BASIS GROUND IS THE EXACT NEGATION of the silent state's
  basis clause**, so that narrowing SELF-REFERENTIAL to the carrier's own addition
  leaves no block outside all five states: a marker naming the carrier as its own
  basis is reported here wherever the carrier is not reported self-referential.
  **THE REMEDY IS SINGULAR PER GROUND AND THE FINDING SHALL SAY
  WHICH GROUND IT NAMES**: more than one marker is repaired by withdrawing every
  declaration but the true one, a wrong basis by naming the change that
  actually adds the requirement or renames to its title, a wrong `by` by writing
  the carrying change's own
  identifier, an absent reason by writing the one the form requires,
  and one finding naming two of them without saying which would leave
  its reader to guess which paragraph, or which word of one paragraph, to
  change.
- **UNDISCLOSED** — the block is NOT self-referential and carries EXACTLY ONE
  marker of the reserved form, and that marker is not misdeclared — naming as
  basis an active change, other than this one, that
  does add or rename to the title, carrying as its `by` identifier the change
  that carries the block, AND CARRYING A REASON — that basis change is NOT
  `ratified`, and the marker's
  reason clause does not carry the disclosure `document-lifecycle` requires of it.
  Reported, and reported apart from the other three: here the pairing is declared
  and the basis is real, and what is missing is the reader's warning that the text
  the block rests on has been accepted by no authority. **THE REASON'S PRESENCE
  IS THIS STATE'S PRECONDITION AND NOT ONE OF ITS TESTS**: a marker with no
  reason clause is placed MISDECLARED one check earlier, so this state never
  reads an absent clause and never hands a reader "write the word `unratified`"
  as the remedy for a marker with no sentence to write it into.
- **DECLARED AND RESOLVING** — the block is NOT self-referential and carries
  EXACTLY ONE marker of the reserved form, and that marker is neither misdeclared
  nor undisclosed: it names as basis an active
  change other than this one that does add or rename to the title, its `by`
  identifier is the change that carries the block, it carries the nonempty
  reason `document-lifecycle`'s form requires, and either that basis is
  `ratified` or the marker discloses that it is not. NO FINDING IS EMITTED.
  A correctly declared pair is the state this check exists to produce, and a
  standing row for it would be a permanent advisory nobody should act on.

**A CHANGE'S OWN RENAME TO THE TITLE IS THE RENAME-AND-AMEND SHAPE, NOT A
DEFECT, AND PROMOTED CANON ALREADY DECIDES IT.** The resolution order this family
runs under examines the CARRYING change's own `## RENAMED Requirements` block
BEFORE the set of titles active changes add or rename to, and where that block
renames a promoted requirement TO this title the three comparison arms SHALL run
against canon under the OLD name, "a rename being a change of title rather than
of the content a block must carry"
(`openspec/specs/doc-health/spec.md:1568-1574`), with the promoted scenario "A
change renames a requirement and modifies it in one delta" resting a MUST on that
reading (`:1783-1786`). That PRECEDENCE IS PRESERVED AHEAD OF THE EXAMINATION
ABOVE and is widened, narrowed and reordered in no way: a rename-and-amend block
resolves against canon under the old name and never reaches this check at all.
Defining self-reference to reach a carrier's own RENAME would therefore do one of
two wrong things and never a right one — report the supported shape as a defect
where it reached, and stand as unreachable words where the precedence held. The
state is defined by the carrier's own ADDITION because the defect is TWO TEXTS
FOR ONE REQUIREMENT: an `## ADDED Requirements` block carries the requirement's
text and a `## RENAMED Requirements` block carries a pair of titles, so only the
first can be the same text written twice. Where a carrier's own rename names a
`FROM:` title the promoted specification does NOT carry, that precedence does not
resolve and the block reaches this check like any other, to be placed by its
marker or by the absence of one; there is no self-reference in it, a title pair
being no second text.

**THE `by` IDENTIFIER IS COMPARED TO THE CARRIER, AND THE OBLIGATION THAT
COMPARISON ENFORCES IS NOT THIS CAPABILITY'S TO STATE.** `document-lifecycle`
defines the form and requires its `by` identifier to BE the change whose delta
carries the block; this family reads that identifier and compares it, exactly as
it reads the basis and resolves it. Checking the basis ALONE would leave a marker
naming the right predecessor under an unrelated author in DECLARED AND RESOLVING,
so a block would promote carrying FALSE PROVENANCE — a declaration that sends its
next reader to a packet which declared nothing, which is worse than the
undeclared state it wears the appearance of curing. The comparison belongs INSIDE
MISDECLARED rather than in a state of its own: the defect is one wrong marker
with one paragraph to repair, on the same terms as a wrong basis, and the number
of states this check reports stays FOUR.

**THE REASON IS HARVESTED IN RECOGNITION AND JUDGED IN CLASSIFICATION, AND THE
TWO STAY APART FOR THE REASON THE `by` IDENTIFIER'S DO.** `document-lifecycle`
recognizes this form by its COMPLETE PREFIX and requires a nonempty ` — <reason>`
tail after it; this family reads that tail off every recognized marker and
reports its absence, exactly as it reads the `by` identifier and compares it.
Making the tail a condition of RECOGNITION instead would drop a prefix-only
paragraph to an ordinary body unit, so the block would be reported UNDECLARED
and its author told to add a marker the block already carries — the absent-marker
remedy for a defective declaration. Reading the absence NOWHERE is the hole this
ground closes: a paragraph carrying that complete prefix and its closing colon
and nothing after it names a basis, carries the carrier's own `by`, and would
otherwise satisfy every remaining check and reach DECLARED AND RESOLVING, so a
declaration the form itself calls incomplete would promote as a complete one and
the block would look declared to every later reader while declaring nothing. The
check belongs INSIDE MISDECLARED on the same terms as the `by` comparison — one
wrong marker with one paragraph to repair, one band and one action — so it adds
a GROUND and not a state, and the number of states this check reports stays
FOUR.

**AND IT IS READ BEFORE THE DISCLOSURE, which is not an ordering preference but
the condition of the disclosure being readable at all.** The disclosure is A
WORD LOOKED FOR IN THE REASON CLAUSE, so a marker with no reason clause offers
it nothing to look in. Taken the other way round, an unratified basis under a
prefix-only marker would be reported UNDISCLOSED and its author told to write
`unratified` into a sentence that does not exist, while the identical marker
over a RATIFIED basis would pass in silence — one defect named two ways at two
titles, and at one of the two not named at all. Reading BOTH would be worse
again: two findings and two remedies for one missing tail, which the
exactly-one-state rule forbids. So the reason is read FOURTH and the disclosure
FIFTH, and a prefix-only marker is MISDECLARED on the reason ground whatever its
basis's standing is.

**THE FOURTH STATE, UNDISCLOSED, EXISTS BECAUSE THE OBLIGATION WOULD OTHERWISE
BE DECLARED IN ONE CAPABILITY AND ENFORCED IN NONE.** `document-lifecycle` requires the reason
clause of a marker naming an unratified basis to disclose that standing; without
this state a marker that names its basis and says nothing about its standing
falls into DECLARED AND RESOLVING and passes in silence, and the disclosure
becomes a rule with no reader. The state is a NARROWING of the silent one and
not a fifth thing to look for: its antecedent is the silent state's antecedent
plus two conditions, so it reaches ONLY a block whose pairing is otherwise in
good order, and it restates no defect the other three already name.

**THE DISCLOSURE IS READ AS A WORD AND NOT AS A SENTENCE.** The form belongs to
`document-lifecycle`, which defines the marker and reserves the word; this
family only looks in the reason clause for it. A reason that carries the word
and denies it in the same breath is past what any deterministic family can read,
and it is a defect of authorship its reviewers catch — the alternative, a
checker arbitrating whether a sentence discloses, is the prose rule this marker
design refuses everywhere else.

**A DISCLOSURE THAT OUTLIVES THE STATUS IT DISCLOSED IS NOT REPORTED.** The
marker is a dated statement about the moment it was written, so a basis that
ratifies afterwards ends the question rather than turning the marker into a
defect. Nothing obliges the modifying change to go back and strike the word, and
a stale disclosure SHALL NOT be read as a wrong one.

**AND THE SILENCE THAT FOLLOWS A DISCLOSURE IS SILENCE ABOUT A DECLARATION,
NEVER CLEARANCE FOR AN ARCHIVE.** `release-realization` holds the modifying
change's archive while the title is unpromoted, and that hold keys on the
UNPROMOTED TITLE rather than on the basis's standing — so it stands over EVERY
pending pairing this check passes in silence, the ratified-basis ones included.
The hold is therefore NOT a defect of this class, and keeping the
disclosed-unratified case alone actionable would mis-locate it twice: it would
leave the identical hold unreported over a ratified basis, so that one run's
silence meant two different things at two titles; and it would stand a permanent
advisory over a block that is in good order, whose only remedy — the basis's own
archive — belongs to another packet and another owner, which is the state the
silent state exists to refuse. **THE HOLD IS ENFORCED WHERE THE ACT IT FORBIDS IS
TAKEN**, at the modifying change's archive gate, and what that gate reads is THIS
FAMILY'S OWN RESOLUTION OF THE BLOCK: while the block resolves `pending` the
title is unpromoted and the gate is shut; when the basis archives the block
resolves against canon, the three comparison arms run, and the gate opens with
them. That is a mechanical fact this family already computes for every block, so
the obligation is falsifiable without a finding standing over a correctly
declared pairing — the class's action line carries the same half of the remedy,
hold the archive until the declared change promotes, and the collision class
below is the evidence a breach leaves behind. No arm, no class and no read is
added by this paragraph; it records which instrument enforces what.

**THE FINDINGS SHALL FORM ONE NEW FINDING CLASS of this family**, reported
against the active delta's own path like every other finding this family emits,
carrying the `warning` band and one action line stating every half of the
remedy: declare the basis by ONE marker and no more than one, name the carrying
change itself as that marker's `by` identifier, give that marker the reason its
form requires, disclose in that reason clause
where that basis is not ratified, and hold the archive until the declared change
promotes.
The class SHALL be registered in the family's own class registry with its own
identifier and label, and SHALL be placed by the family's class map; a finding
this new class emits that the map does not place is an unplaced finding like any
other and is reported by the class that reports those.

**ITS RULE TEXT SHALL BE RENDERED FROM A REGISTERED ARM TEMPLATE.** The family
derives its unplaced-finding mask from its own arm templates, so a rule text
built any other way would have no shape the mask can compute and would be
reported as drift on every run that emitted one. One template SHALL carry all
four reported states — MISDECLARED's four grounds included, they being one state
with one action that differ only in the same interpolated clause — distinguished
by that clause, because one template is one shape is one map entry: the four
states share a band and an action and differ only in why.

**THE BAND IS `warning`, AND THE CLASS IS `contested` BY A ROW THIS REQUIREMENT
DOES NOT ADD AND CANNOT DECLINE.** The band is the measure-then-flip posture
every family of this group launched under, and here it is also the only honest
one: the population this check reports is the corpus's existing four pairs, none
of which was authored under a rule that existed, and raising the band is one
later decision taken by ruling AFTER that standing population is discharged. The
RESOLUTION CLASS is not a second half of that choice. `FAMILY_RESOLUTION` already
carries this family, its table has no per-class grain, and this requirement adds
no row and can remove none — so a finding of this class is `contested` from its
first emit. The promoted sentence that once denied that row is superseded by
this change's `## MODIFIED Requirements` block below, so the classification is
one thing canon and code now say together rather than two things they say
apart.

**THE CLASS'S REMEDY IS THE MARKER, AND THE TWO ROUTES TO IT ARE ORDERED RATHER
THAN OFFERED.** A `contested` finding that stops being emitted owes a citation
under this capability's own uncited-resolution rule, so a class whose whole
design is that its findings are discharged SHALL NOT be introduced against a
population it could have declared first.

1. **SEQUENCING IS THE ROUTE.** Where a repository carries undeclared pairings at
   the moment this check is introduced, they SHALL be declared by marker BEFORE
   the check runs there, so that it launches at a population of zero. A finding
   never emitted never vanishes and owes no citation, so this route ends the
   question rather than answering it.
2. **THE CITATION IS THE EXCEPTION, IT CARRIES ITS OWN RETIREMENT, AND IT IS
   AVAILABLE ONLY WHERE THE ORDERING ARM HAS NOTHING IT COULD EMIT.** Where
   that sequencing is not available — a pairing arising after the check is
   running, or a population in a repository the introducing measurement did not
   reach — the act that ADDS the marker SHALL record the citation that resolution
   requires, on the same terms as every other `contested` finding of this family.
   A disposition SHALL NOT be recorded IN PLACE OF a marker. **AND THIS ROUTE
   SHALL NOT BE TAKEN AT ALL while any active change OTHER THAN the one whose
   delta carries the block, and whose declared standing is `ratified`, carries a
   `## MODIFIED Requirements` block for the same capability and requirement
   title.** In that state SEQUENCING IS THE ONLY ROUTE: the marker is written and
   no entry is recorded, and where the marker cannot yet be written the finding
   stands until it can.

   **THE BOUND IS READ OFF THE MECHANISM RATHER THAN CHOSEN.** This family's
   two-writers ordering arm is armed BY COUNT — it takes the active MODIFIED
   blocks over one capability and requirement title, keeps those whose carrying
   change is `ratified`, and returns nothing whatever below TWO of them. It runs
   BEFORE any block of that group is resolved against canon, it emits one finding
   PER RATIFIED BLOCK against that block's own delta path, and its findings are
   then filtered through THE SAME family/repository/path disposition read,
   narrowed by THE SAME requirement title. An entry recorded to answer a pairing
   finding on a block therefore reaches the ordering finding over that same block
   wherever one is emitted — and the ordering defect is a SEPARATE defect with a
   SEPARATE remedy, which would stay hidden for as long as the entry stood.

   **SO THE SENTENCE THIS ROUTE ONCE RESTED ON IS MADE TRUE BY CONSTRUCTION
   RATHER THAN ASSERTED.** That a citation "suppresses nothing" is not a property
   of the citation — the entry carries no finding-class grain and silences
   whatever shares its key — it is a property of the STATE it is recorded in. The
   bound admits the entry only where the ordering arm has NO SUBJECT at that
   title, so there is nothing of that class for it to hide; the pairing finding it
   answers is already answered by the marker landed in the same act; and the three
   comparison arms do not run over a pending block. The route suppresses nothing
   because it exists only where there is nothing to suppress.

   **THE BOUND IS ONE CASE WIDER THAN THE ARM'S ARMING CONDITION, DELIBERATELY.**
   The arm needs TWO ratified writers and this refuses the route at ONE OTHER, so
   it also refuses where the carrier's own change is not ratified and exactly one
   other ratified writer stands — a state in which the arm emits nothing today.
   The width is the point: standing is one header edit on the carrier's own
   proposal, and an entry recorded under the reading "my own change is not
   ratified, so the arm is silent" would begin suppressing the ordering class the
   moment that change was ratified, with no act anywhere to notice. A bound a
   later edit can invalidate while the entry stands is not a bound. For the same
   reason the bound reads the arm's SUBJECT and not its current emit: two ratified
   writers with exactly one declaration between them are the ordered pair the arm
   passes in silence, and one proposal edit withdrawing that declaration turns the
   silence into a finding the standing entry would then hide.

   **AND THE BOUND'S POPULATION IS ZERO ON THE AUTHORING TREE.** Measured with
   the family's own reader over this branch, this packet's own two MODIFIED
   blocks included: no capability-and-requirement title carries more than ONE
   active MODIFIED block at all, so none carries two ratified writers and the
   route is refused nowhere. Like the collision class, the bound costs nothing to
   land and is in place before its first instance rather than after it.

**A DISPOSITION RECORDED FOR A PAIRING SHALL BE SCOPED SO THAT IT CANNOT OUTLIVE
THE PAIRING IT ANSWERS, and the scope is dictated by the mechanism rather than
chosen.** This family reads its dispositions at FAMILY, REPOSITORY and PATH grain
with an optional REQUIREMENT narrowing, NEVER at finding-class grain, and it
reads them BEFORE a block is resolved against canon AND before the two-writers
ordering arm's findings are collected. An entry recorded to answer
a finding of this class therefore suppresses the three comparison arms over that
block as well — and goes on suppressing them after the declared basis archives
and the block becomes comparable, which is the one moment those arms exist for —
and, where the ordering arm has a subject at that title, the ordering finding
over that same block with them. A
remedy that ends by disabling the checks its own subject is finally eligible for
is not a remedy, and one that hides a live defect of another class the whole time
it stands is worse, so THREE obligations attach to the entry and all three are
part of it. The first is the AVAILABILITY bound route 2 states, which is what
keeps the ORDERING reading above empty; the other two are here:

- **GRAIN.** The entry SHALL name the REQUIREMENT and not the delta path alone,
  so that it reaches the one block it answers rather than every finding this
  family raises against a delta file that may carry several blocks.
- **RETIREMENT.** The entry SHALL be retired when the declared basis archives,
  that being the act after which it silences a comparison instead of answering a
  disappearance. **AND THE INTERVAL BEFORE THAT ACT IS EMPTY BY THE AVAILABILITY
  BOUND AND NOT BY THE PENDING STATE ALONE.** A pending block's three comparison
  arms do not run, so while the basis is unpromoted the entry silences nothing of
  theirs; the ordering arm is the exception, running before resolution and read
  through the same key, and route 2's bound is what makes that reading empty for
  as long as the entry stands. Without it this interval would carry one class of
  live finding the entry hid. The retirement is an obligation of THE ARCHIVING
  CHANGE — the
  act that promotes the requirement is the act that makes the arms able to read
  the block — and it is evidenced at that change's own archive gate. The
  MODIFYING change's archive gate SHALL confirm that no such entry stands over
  its block, a block whose carriage no arm has been allowed to read being exactly
  what that gate exists to refuse. The ORDER of the two archive acts stays
  `release-realization`'s obligation and is neither restated nor widened here;
  what this requirement adds is only the bound on an instrument this capability
  owns.

**THE CHECK READS EVERY ACTIVE CHANGE REGARDLESS OF LIFECYCLE STANDING**, as
this family's reading rule already provides, and this is deliberately wider than
the REFERENCE-AND-DECLARE half `release-realization` scopes to an active ratified
change — though not wider than that capability's ARCHIVE HOLD, which keys on the
unpromoted title and reaches a basis of any standing. A finding SHALL name the
declared or resolved basis change and, where that change is not ratified, SHALL
say so, so that a reader can see at a glance
whether an obligation or only an observation stands behind the row. **THE
BASIS'S OWN STANDING IS READ THE WAY THIS FAMILY ALREADY READS STANDING** —
through the one lifecycle-header reader its two-writers arm uses for
`release-realization`'s `ratified` scoping, never a private regex — so the fact
that qualifies a finding's wording and the fact the UNDISCLOSED state turns on
are one fact read once. A basis whose header declares no standing this reader
can resolve SHALL be treated as not ratified, the whole point of the disclosure
being to warn a reader about text no authority has been shown to accept, and a
standing nobody can read being no such showing.

#### Scenario: A block over a sibling's addition carries no marker
- **WHEN** an active change's MODIFIED block names a requirement the promoted specification does not carry, an active change ADDS or RENAMES to that title, the change carrying the block does not itself ADD that title, and the block carries no `Modified over` marker
- **THEN** the run MUST emit one `warning` finding against the active delta's own path, naming the requirement, the change whose addition it resolves to, and that no marker declares the pairing
- **AND** the three comparison arms MUST NOT run against that block, there being no promoted requirement to compare it to
- **AND** the finding MUST NOT cause a run configured `--fail-on error` or `--fail-on critical` to fail

#### Scenario: A block over a sibling's addition is correctly declared
- **WHEN** such a block carries EXACTLY ONE `Modified over` marker, naming as basis an active change other than its own that ADDS or RENAMES to the block's capability and requirement title, that marker's `by` identifier is the change whose delta carries the block, that marker carries the nonempty reason its form requires, and the basis change is `ratified`
- **THEN** no finding MUST be emitted for that block, a declared pairing being the state this check exists to produce
- **AND** the reason's presence MUST be one of the conditions of that silence, an otherwise identical marker carrying the prefix alone being reported rather than passed

#### Scenario: The marker names a change that does not add the requirement
- **WHEN** such a block carries EXACTLY ONE `Modified over` marker, naming as basis a change that neither ADDS nor RENAMES to its capability and requirement title, and the change carrying the block does not itself ADD that title
- **THEN** the run MUST emit a `warning` finding naming the change the marker names and stating that it adds no such requirement
- **AND** that finding MUST be worded apart from the undeclared case, a wrong basis and an absent one having different remedies
- **AND** a marker naming the CARRYING change itself as basis MUST be reported in this state wherever that change is not reported self-referential, a block's basis being a change other than the one that writes it

#### Scenario: The marker's `by` identifier is not the change carrying the block
- **WHEN** such a block carries EXACTLY ONE `Modified over` marker, whose basis DOES add or rename to the block's capability and requirement title, and whose `by` identifier is a change other than the one whose delta carries the block
- **THEN** the run MUST emit one `warning` finding in the misdeclared state, naming the identifier the marker carries and the change that carries the block, a right basis under a wrong author being a FALSE provenance rather than an incomplete one
- **AND** an otherwise identical marker whose `by` identifier IS the carrying change MUST NOT be reported on that ground, the identifier being validated against the carrier rather than merely resolved
- **AND** no undeclared finding MUST be emitted for that block alongside it, the marker being present and the states being exclusive

#### Scenario: A block carries two pairing markers
- **WHEN** such a block carries MORE THAN ONE paragraph of the reserved `Modified over` form — one of them naming a basis that does add the requirement and carrying as its `by` identifier the change that carries the block, the other naming a change that adds nothing
- **THEN** the run MUST emit exactly ONE `warning` finding for that block, in the misdeclared state and on the count ground, naming how many such markers the block carries
- **AND** the finding MUST NOT depend on which of the markers is examined, the count being read before any marker's basis or `by` identifier is
- **AND** an otherwise identical block carrying EXACTLY ONE valid marker MUST NOT be reported, this ground reaching a plurality of declarations and never a lawful single one

#### Scenario: The marker carries its prefix and no reason
- **WHEN** such a block carries EXACTLY ONE `Modified over` marker, naming as basis an active change other than its own that ADDS or RENAMES to the title and carrying as its `by` identifier the change whose delta carries the block, the basis change is `ratified`, and that marker carries no ` — ` separator or carries one with nothing but whitespace after it
- **THEN** the run MUST emit one `warning` finding for that block in the misdeclared state, on the reason ground, stating that the marker carries no reason
- **AND** the block MUST NOT be placed in DECLARED AND RESOLVING, a declaration `document-lifecycle` calls incomplete not being one this check passes in silence
- **AND** the block MUST NOT be reported UNDECLARED, the paragraph being a recognized marker of this form whose declaration is defective rather than an absent one, and the remedy being to write the reason rather than to add a marker

#### Scenario: A prefix-only marker names an unratified basis
- **WHEN** such a block carries EXACTLY ONE `Modified over` marker with a right basis and a right `by` identifier and no reason at all, and the basis change carries a status other than `ratified`
- **THEN** the run MUST emit exactly ONE finding for that block, in the misdeclared state and on the reason ground, the reason being read before the disclosure
- **AND** the block MUST NOT be reported UNDISCLOSED, that state reading a word in a reason clause and there being no clause to read it in, so that its remedy would name a word rather than the missing tail
- **AND** the finding MUST NOT depend on the basis's standing, the identical marker over a `ratified` basis being reported on the same ground

#### Scenario: A change modifies its own unpromoted addition
- **WHEN** one change carries both an ADDED and a MODIFIED block for one capability and requirement title
- **THEN** the run MUST emit a `warning` finding against that delta
- **AND** a `Modified over` marker naming that same change MUST NOT suppress it
- **AND** exactly ONE finding of this class MUST be emitted for that block, in the self-referential state, whether the block carries no marker, one, or several — that state being examined first and excluding the undeclared and misdeclared readings the same block would otherwise also satisfy

#### Scenario: The carrier renames the requirement and modifies it in one delta
- **WHEN** one change carries a `## RENAMED Requirements` block renaming a promoted requirement TO a title and a MODIFIED block for that same title
- **THEN** the block MUST NOT be reported in the self-referential state, nor in any other state of this class, the promoted resolution order resolving it against canon under the OLD name before this check is reached
- **AND** the three comparison arms MUST run against it under that old name, this requirement preserving that precedence rather than displacing it

#### Scenario: A block is declared over a basis no authority has accepted
- **WHEN** such a block carries EXACTLY ONE `Modified over` marker, naming as basis an active change other than its own that ADDS or RENAMES to the title, whose `by` identifier is the change whose delta carries the block, that marker CARRIES A REASON, that basis change carries a status other than `ratified`, and that reason clause does not carry the disclosure `document-lifecycle` requires
- **THEN** the run MUST emit one `warning` finding against the active delta's own path, naming the basis change and its declared standing and stating that the marker does not disclose it
- **AND** that finding MUST be worded apart from the undeclared and the misdeclared cases, a pairing declared over text no authority has accepted being a different defect from an absent basis or a wrong one
- **AND** a marker carrying no reason at all MUST be reported in the misdeclared state instead and never here, the reason being read before the disclosure and an absent clause being nothing for the disclosure to be read in

#### Scenario: The unratified basis is disclosed
- **WHEN** such a marker carries a reason, and that reason clause carries that disclosure or the change it names is `ratified`
- **THEN** no finding MUST be emitted for that block, the disclosure being the whole of what THIS CHECK asks of a declared pairing beyond the form's own reason
- **AND** a `ratified` basis MUST NOT be read as excusing the reason, a marker carrying the prefix alone being reported on the reason ground whatever its basis's standing
- **AND** that silence MUST NOT be read as archive clearance, `release-realization`'s hold standing over the block for as long as the title is unpromoted and keying on that title rather than on the basis's standing
- **AND** a disclosure MUST NOT be reported once the basis it discloses ratifies, the marker being a dated statement about the moment it was written

#### Scenario: A disclosed unratified pairing reaches the modifying change's archive gate
- **WHEN** a block this check passes in silence names a basis that is not ratified and whose marker discloses it, and the change carrying that block reaches its archive gate while the title is still unpromoted
- **THEN** this check MUST emit nothing for that block, its pairing being in good order, and that silence MUST NOT be read at the gate as clearance
- **AND** the fact the gate reads MUST be the block's own `pending` resolution — this family's, computed for every block — the title being unpromoted for exactly as long as the block resolves `pending`, and the hold that fact serves being `release-realization`'s obligation rather than this requirement's
- **AND** no finding of THIS class MUST be emitted for the held block, its remedy being the basis's ratification and archive rather than any edit to the block
- **AND** where that change archives regardless, the still-active basis's `## ADDED Requirements` block — or its `## RENAMED Requirements` block's `TO:` title — MUST be reported by the collision class on the next run, that being the mechanical evidence the breach leaves

#### Scenario: A declared basis archives
- **WHEN** the change a block is declared over archives and its addition reaches the promoted specification
- **THEN** the block MUST resolve against canon on the next run and the three comparison arms MUST run against it
- **AND** this check MUST emit nothing further for that block, its question having been answered by the promotion
- **AND** the modifying change's archive gate MUST open at that promotion and not before, whatever the basis's standing was while the block was pending

#### Scenario: The `Modified over` marker is not a carriage declaration
- **WHEN** a block carries a `Modified over` marker
- **THEN** that marker MUST NOT suppress any unit of any comparison, and MUST NOT be reported as a marker naming a unit the block still carries
- **AND** the marker paragraph MUST NOT be counted as a body unit of the block or of the requirement it promotes into

#### Scenario: A pairing finding is discharged by its marker
- **WHEN** a block this check reports gains a `Modified over` marker naming the change that adds its requirement, and the finding stops being emitted on the next run
- **THEN** the resolution MUST carry the citation this capability's uncited-resolution rule requires of a `contested` finding, recorded on the act that added the marker
- **AND** the citation MUST NOT be recorded IN PLACE OF the marker, a disposition standing in for the remedy being the state this class's band posture exists to avoid

#### Scenario: A finding of this class is dispositioned
- **WHEN** `health/dispositions.yaml` carries an entry naming this family, a repository, an active delta path, and a `cite`
- **THEN** findings of this class on that path MUST be suppressed on the same terms as this family's other findings, and the entry MUST be read as reaching the whole block rather than this class — the disposition is read before the block resolves and there is no finding-class grain for it to read
- **AND** the entry MUST name the requirement, an entry without that narrowing disposing every finding this family raises against a delta file that may carry several blocks
- **AND** an entry without a `cite`, or an entry naming another family, MUST suppress nothing

#### Scenario: A citation is recorded while a second ratified writer stands
- **WHEN** a pairing finding stands over a block, and an active change other than the one whose delta carries that block, whose declared standing is `ratified`, carries a `## MODIFIED Requirements` block for the same capability and requirement title
- **THEN** the citation route MUST be refused for that block and the pairing MUST be declared by marker with no entry recorded, an entry at this family's grain reaching the ordering finding over that title as well as the pairing one it answers
- **AND** the refusal MUST rest on the ordering arm having a SUBJECT at that title rather than on its having emitted, the declarations between two ratified writers being one proposal edit away from turning that arm's silence into a finding the standing entry would hide
- **AND** where no active change other than the carrier, whose declared standing is `ratified`, writes a MODIFIED block for that title any longer — that change having archived, or its standing having ceased to be `ratified` — the route MUST open, the arm having no subject there and nothing it could emit
- **AND** this bound MUST NOT be read as adding a finding class or a check to this family: it is an obligation on the act that records the entry, read from a state the family's own reader already computes

#### Scenario: The declared basis archives while a pairing disposition still stands
- **WHEN** the change a pairing disposition was recorded against archives, its addition reaches the promoted specification, and the entry still stands in `health/dispositions.yaml`
- **THEN** the entry MUST be retired by that archiving act, the block resolving against canon from that moment and the three comparison arms being the only reading of it there is
- **AND** the run's silence on that block MUST NOT be read as those arms clearing it, the disposition being read before the block resolves so that the silence is suppression rather than comparison
- **AND** the modifying change MUST NOT meet its own archive gate while the entry stands, a stale MODIFIED block deleting newly promoted clauses unreported being the defect those arms exist to report

### Requirement: An active block writing a title the promoted specification already carries is reported
The modified-block-currency family SHALL report every active change's `## ADDED
Requirements` block naming a capability and requirement title the promoted
specification already carries, AND every active change's `## RENAMED
Requirements` block whose `TO:` title the promoted specification already carries
for that capability, at `warning`, against that delta's own path.

**THIS IS THE ARCHIVE-ORDERING BACKSTOP, and it is the only direction in which
one can exist.** Where a MODIFIED-over-a-sibling's-basis pair archives in the
safe order the requirement enters canon first and every existing check resumes.
Where it archives in the unsafe order the modifying block promotes text nobody
reviewed as an addition or as a rename, and the surviving evidence is precisely
this: an active change still writing that title into canon — an ADDED block for
a title canon now carries, or a RENAMED block whose `TO:` title canon now
carries. Nothing in
the estate reads that shape. The family that compares an archived delta to canon
cannot, canon being the delta after the archive act; the family reading active
MODIFIED blocks reads ADDED and RENAMED blocks ONLY to build the pending set,
never against canon. Reading it here
costs one lookup against a promoted-requirement index this family already builds,
and one more pass over the rename pairs `resolve` already parses.

**THE RENAME'S COLLISION IS IN THE `TO:` HALF, AND THE DIRECTION IS THE WHOLE OF
WHAT MAKES THE CHECK READABLE.** A `## RENAMED Requirements` block names a
`FROM:` title and a `TO:` title. The `FROM:` half is expected to name a title
canon carries — that is what a rename renames — so reading THAT half would
report every lawful rename in the corpus. The collision shape is the `TO:` half:
a title canon ALREADY carries while an active change is still proposing to
rename something INTO it, which is the same surviving evidence an unpromoted
addition leaves, reached through the other basis form. Canon's own resolution
rule reads a rename BY ITS TARGET for exactly this reason — "where that block
renames a promoted requirement to this title"
(`openspec/specs/doc-health/spec.md:1568-1574`), with the scenario at
`:1783-1786` — so the half this class reads is the half canon already reads.

**A BASIS IS A BASIS EVERYWHERE OR NOWHERE.** `document-lifecycle`'s marker
requirement is owed where "an active change ADDS or RENAMES to that title", the
pairing check's misdeclared state accepts a basis that RENAMES to the title, and
`release-realization`'s ordering obligation reaches a requirement an active
change ADDS OR RENAMES TO — its reference-and-declare half at a ratified basis,
its archive hold at a basis of any standing. A backstop that read additions
alone would leave a rename-based pair with the declaration and the ordering rule both
reaching it and no mechanical evidence of a breach at all — the one hole this
requirement exists to close, left open for the one basis form that arrives less
often.

**THE CHECK IS NOT LIMITED TO THE PAIR THAT MOTIVATES IT.** An ADDED block, or a
rename's target, over a requirement canon already carries is a defect however it
arose — a stale packet, a duplicated title, an addition that should have been a
modification, a rename into a title that has since been added — and narrowing
the check to blocks that had a MODIFIED partner would decline to report the same
defect for a worse reason.

**THE FINDING SHALL BE ITS OWN CLASS**, registered and templated on the same
terms as every other class this family carries, and SHALL carry an action line
naming the two remedies: promote nothing further until the collision is
resolved, and — where the requirement genuinely already exists — convert the
addition to a modification declared against canon, or withdraw or re-target the
rename whose `TO:` title canon already carries. The band is `warning`; the
class is `contested` by the family's standing `FAMILY_RESOLUTION` row, which this
requirement neither adds nor can decline. Its exposure to the
uncited-resolution rule is smaller than the pairing class's and not absent: its
population is zero, so nothing is owed at launch, and a collision that stops
being reported has been resolved by a governance act with a change to cite.

**THE POPULATION IS ZERO ON THE AUTHORING TREE ACROSS BOTH BASIS FORMS, and that
is the argument for
building it now.** Measured: of the tree's active `## ADDED Requirements` blocks
none names a title the promoted specification already carries, and the tree
carries no active `## RENAMED Requirements` pair at all, so the widening to
renames costs a population of zero rather than a discharge. A check whose
standing population is empty costs nothing to
land, pins a state every reader already assumes, and is in place before the
first instance rather than after it — which for this shape matters more than
usual, because the first instance is an archive act that cannot be taken back.

#### Scenario: An active ADDED block names a requirement canon carries
- **WHEN** an active change's `## ADDED Requirements` block names a capability and requirement title the promoted specification already carries
- **THEN** the run MUST emit one `warning` finding against that delta's own path, naming the requirement and the promoted specification that carries it
- **AND** the finding MUST NOT cause a run configured `--fail-on error` or `--fail-on critical` to fail

#### Scenario: An active RENAMED block targets a title canon carries
- **WHEN** an active change's `## RENAMED Requirements` block names a `TO:` title the promoted specification already carries for that capability
- **THEN** the run MUST emit one `warning` finding against that delta's own path, on the same terms and in the same class as an ADDED block naming that title, a rename being a basis wherever an addition is
- **AND** the block's `FROM:` title MUST NOT be read for this class however it resolves, a rename's source being a title canon is expected to carry and reading it reporting every lawful rename

#### Scenario: The unsafe archive order is taken
- **WHEN** a change carrying a MODIFIED block over an active sibling's addition, or over an active sibling's rename to the title, archives before that sibling, so the requirement enters canon from the modifying block
- **THEN** the sibling's still-active block MUST be reported by this check on the next run — its `## ADDED Requirements` block, or its `## RENAMED Requirements` block's `TO:` title — the collision being the surviving evidence of the ordering breach
- **AND** the report MUST NOT be read as curing the breach, an archive act being outside what any health run can undo

#### Scenario: No active change writes a title canon carries
- **WHEN** every active `## ADDED Requirements` block names a title the promoted specification does not carry, and every active `## RENAMED Requirements` block names a `TO:` title it does not carry
- **THEN** this check MUST emit nothing, and its class MUST still render in the family's class block at a count of zero

## MODIFIED Requirements

### Requirement: A modified-block-currency finding its own class map cannot place is itself a finding
The modified-block-currency family SHALL emit ONE ADDITIONAL `warning` finding
per run for each DISTINCT SHAPE of rule text its own class map does not place,
naming how many of that run's findings carry that shape and, verbatim, the rule
text of the first of them in the family's own report order, and carrying that
first finding's repository and delta path. Where the map places every finding
the family emits, no such finding SHALL be emitted.

Two unplaced findings SHALL be treated as ONE SHAPE where their rule texts are
equal after EVERY FIELD THE ARM'S TEMPLATE INTERPOLATES has been replaced by a
fixed placeholder — quoted spans, runs of digits, repository-relative paths,
change identifiers, unit-kind lists, and any other value the arm substitutes
into its fixed prose — so that one shape is one template and one remedy.

The family SHALL derive that mask from its own arm templates: an arm's FIXED
PROSE is the shape and every value the arm interpolates into it is not, so the
rule cannot drift from the arms it describes.

The finding's action line SHALL name both remedies and where the first is
applied: "extend the class map in `scripts/doc_health/modified_block_currency.py`,
or fix the drifted rule text the finding names".

The finding SHALL itself be placed by the class map, in a FIFTH class of the
family's own registry carrying the `warning` band and that action line, so that
it is never counted by the residual it reports.

The pattern that places that class SHALL be anchored at the start of the rule
text, this finding carrying a quoted rule text that may itself begin in the shape
of an arm's.

The family's residual row SHALL continue to render whenever its count is
nonzero.

**THE FAMILY IS PRESENT IN `FAMILY_RESOLUTION`, AND THIS REQUIREMENT RECORDS
THAT ROW RATHER THAN CONTRADICTING IT.** `scripts/doc_health/families.py` reads
`"modified-block-currency": CONTESTED` as of `7f656980` (PR #529, 2026-08-31),
landed as the second half of `add-modified-block-currency-check` § 7.2's
reserved flip together with `_LAUNCH_SEVERITY`'s move to `error`. The absence
this requirement asserted was SPENT on that day, and it is superseded here so
that promoted canon states what the code does rather than the reverse — the
landing amended no specification, and this block is that catch-up rather than a
new decision. That table has NO PER-CLASS GRAIN: it is applied by finding FAMILY
alone, one string every arm and every class of this module shares, so neither
this requirement nor any other can hold one class of the family out of it, and
the finding this requirement defines is `contested` from that landing.

**THE PROTECTION THE ABSENCE BOUGHT IS NOT ENDANGERED BY A MAP EXTENSION, AND
NOTHING IS OWED FOR ONE.** What the absence was held for is that a finding
designed to stop being emitted must never become an uncited-resolution `error`
for having worked. Measured against the machinery rather than reasoned from the
shape of the rule, a map extension cannot raise that error at all:
`report.uncited_resolutions` keys a resolution on `(family, repository, path)` —
`Finding.match_key()`, which reads neither rule text nor severity — and this
finding is emitted with the FAMILY, REPOSITORY and PATH of the very finding it
names, `_drift_findings` in `scripts/doc_health/modified_block_currency.py`
constructing it from that finding's own `repo` and `path`. Extending the map
changes what `classify` PLACES and nothing that an arm EMITS, so the finding
this one named is still emitted, under that same key, on the next run. The key
therefore never leaves the current report, the rule's own `in current` test
skips it, and no error is raised. A protective clause that fires on no reachable
state protects nothing, and stating it would misdescribe the mechanism it claims
to guard.

**AND AN ACT THAT EXTENDS THE CLASS MAP SHALL NOT RECORD A DISPOSITION FOR THE
FINDING IT RECLASSIFIES.** Such an entry answers no disappearance; it causes
one. This family's dispositions are read BEFORE a block is resolved against
canon, at family, repository and path grain with an optional requirement
narrowing and NEVER at finding-class grain, so an entry recorded over the delta
path this finding carries suppresses the three comparison arms over that block —
including the finding that SURVIVED the extension, the one the map has merely
learned to name. **A MAP EXTENSION CLASSIFIES A DEFECT; IT DOES NOT FIX ONE.**
Recording a disposition for it would hide a live finding on every report until
the entry was retired — the exact failure the citation was imagined to prevent,
reached by the instrument imagined to prevent it.

**WHAT THE UNCITED-RESOLUTION RULE STILL REACHES IS UNCHANGED, AND IT IS NOT
RESTATED HERE.** Where some OTHER act makes this family emit nothing at all at a
`(repository, path)` the previous report carried — the block repaired, the delta
withdrawn — that IS a disappearance under the key the rule reads, and this
capability's promoted contested-finding rule applies to it on its own terms,
this family being present in `FAMILY_RESOLUTION`. This requirement adds nothing
to that rule and takes nothing from it. It records only that extending the class
map is not such an act, and that treating it as one is itself the defect.

This requirement adds no deterministic check family: the finding is emitted by
the modified-block-currency family under its own id, and the enumeration and its
numerals in the "Deterministic check families" requirement are untouched and
unrestated.

**Removed from canon by govern-sibling-added-modified-deltas (2026-08-31):** `` The family SHALL remain absent from `FAMILY_RESOLUTION`, so that a finding designed to stop being emitted as soon as the map is extended is never classified `contested` and its disappearance is never reported as an uncited resolution. ``; `` **AND** the disappearance MUST NOT be reported as an uncited resolution, the family being deliberately absent from `FAMILY_RESOLUTION` and its findings therefore never classified `contested` `` — the family joined the resolution table on 2026-08-31, at the landing PR #529 named above, so both units assert an absence that no longer holds; each is superseded in this same block, the sentence by the four paragraphs above and the bullet by the one that replaces it, and neither is dropped without replacement

#### Scenario: Every finding the family emits is placed by its map
- **WHEN** a run of the modified-block-currency family emits findings and the class map places every one of them
- **THEN** no additional finding MUST be emitted, the map and the arms agreeing being the state this requirement exists to leave alone
- **AND** the family's rendered class counts MUST still sum to the rows the report prints for it

#### Scenario: A rule text the class map does not place
- **WHEN** a run of the modified-block-currency family emits one or more findings whose rule text no pattern of its class map matches
- **THEN** the run MUST emit exactly one additional `warning` finding for each distinct shape among them, naming the number of that run's findings carrying that shape and, verbatim, the rule text of the first of them in the family's own report order
- **AND** each such finding MUST carry the repository and delta path of that first finding, and the action line this requirement states
- **AND** each such finding MUST itself be placed by the map into the fifth class, so that it is never counted by the residual it reports and the rendered counts still sum to the rows

#### Scenario: Two unplaced findings from one arm template
- **WHEN** two unplaced findings come from the SAME arm template and differ only in the values that template interpolates — a different quoted title, a different promoted-spec path, a different unit-kind list, different change identifiers
- **THEN** ONE additional finding MUST be emitted for both, naming the count two, one drifted arm template being one remedy
- **AND** two unplaced findings from DIFFERENT arm templates — differing in the fixed prose the mask leaves standing — MUST yield two additional findings, being two remedies

#### Scenario: The quoted rule text begins in the shape of an arm
- **WHEN** an unplaced rule text itself begins with the phrase an arm's rule texts begin with, and this finding quotes it
- **THEN** this finding MUST be placed in the fifth class and MUST NOT be placed under the class its quotation resembles
- **AND** the unplaced finding it names MUST still be counted by the residual row, the two being counted apart

#### Scenario: The warning is worked from the ranked plan
- **WHEN** a report is rendered for a run that emitted the additional finding
- **THEN** the finding MUST appear in the ranked plan as a ready-to-stage work item stating its severity, repository, path and action, on the same terms as every other finding
- **AND** the family's residual row MUST still render in the family's own report block, the row and the finding being two readings of one fact rather than alternatives

#### Scenario: The class map grows the pattern the drift named
- **WHEN** the class map is extended with a pattern that places the rule text the finding named, and the family is run again over the same tree
- **THEN** the additional finding MUST NOT be emitted, and the residual row MUST NOT render
- **AND** the disappearance MUST NOT be reported as an uncited resolution, and no citation and no disposition MUST be recorded for it — the finding this one named being still emitted at the same `(family, repository, path)` the uncited-resolution rule keys on, so the key never leaves the current report and the rule never fires

#### Scenario: The act that extends the class map records a disposition for the finding it reclassifies
- **WHEN** an act extends the class map so that a drifted rule text is placed, and that same act records an entry in `health/dispositions.yaml` naming this family, the repository and the delta path the additional finding carried
- **THEN** the entry MUST be refused, this requirement forbidding it: it answers no disappearance, the finding the additional one named still being emitted under the key the uncited-resolution rule reads
- **AND** the entry MUST be read as suppressing rather than resolving — dispositions of this family being read before a block resolves and carrying no finding-class grain, it silences the three comparison arms over that block, and with them the surviving finding the extension only classified, on every run until it is retired

#### Scenario: The family's resolution class is read from the table and not from this requirement
- **WHEN** a reader asks whether a finding of this class is classified `contested`
- **THEN** the answer MUST be read from `FAMILY_RESOLUTION`, which carries this family and has no per-class grain, and this requirement MUST NOT be read as holding this class out of it
- **AND** the row MUST be read as standing since `7f656980` (PR #529, 2026-08-31), the landing that added it without amending this specification, so that a reader of the code and a reader of canon are not told two different things
