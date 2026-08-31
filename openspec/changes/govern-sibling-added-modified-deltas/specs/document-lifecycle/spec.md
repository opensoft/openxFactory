# document-lifecycle Specification Delta

ADDED ONLY. No `## MODIFIED Requirements` block is opened on "A MODIFIED
requirement block restates the requirement as canon currently states it" —
see the proposal's § Orchestrator Decisions D2, which measures rather than
prefers that shape.

## ADDED Requirements

### Requirement: A MODIFIED block over a requirement no promoted specification carries declares its basis by marker
A `## MODIFIED Requirements` block SHALL declare its basis by a reserved marker
inside that block where the requirement it names is one the promoted
specification does not carry and an active change ADDS or RENAMES to that
title, naming the change whose addition or rename the block is written over.

**THE SHAPE IS LAWFUL, AND IT IS THE DECLARATION THAT MAKES IT SO.** Modifying
a requirement a sibling is still adding — or still renaming a promoted
requirement into, the two basis forms being one basis on the same terms wherever
this corpus reads them — is a legitimate and frequent act in a
corpus where changes are long-lived: the successor arrives before the
predecessor archives, and asking it to wait would be asking governance to run at
the speed of the slowest packet. What is not lawful is doing it silently. The
obligation to order the two writers belongs to `release-realization` ("Ordered
deltas and branch vocabulary"), which this requirement neither restates nor
widens; the obligation this requirement adds is that the pairing be declared
where a reader and a checker can both find it, per requirement rather than per
packet.

**THE MARKER IS A THIRD RESERVED FORM, recognized by form and never by prose**,
taking its place beside the two this capability already defines and read under
the same rules: one paragraph inside the MODIFIED block, read after the same
whitespace normalization every other unit gets, and of marker form only where it
begins with the prefix COMPLETE. The form is
``**Modified over `<basis change-id>`'s addition by <change-id> (<YYYY-MM-DD>):**``
followed by ` — <reason>`. The basis change-id is written as a code span, as
every change-id this capability's markers name already is.

**THE WORD `addition` IN THAT PREFIX IS FIXED PROSE, NOT A CLAIM ABOUT THE
BASIS'S BLOCK KIND.** The form is recognized by a COMPLETE prefix, so its literal
text is a token a parser matches rather than a description a reader must verify;
it names the RELATION the marker declares — this block rests on what that change
writes into canon — and a basis that RENAMES a promoted requirement to the title
is declared by the same unchanged form. Spelling a second prefix for the rename
case would make one relation two shapes, two parse branches and two class-map
entries for one remedy, which is what this capability's reserved forms exist to
avoid.

**AT MOST ONE MARKER OF THIS FORM SHALL STAND IN ONE BLOCK — ONE PAIRING, ONE
DECLARATION.** This capability's other two reserved forms carry no such bound
and SHALL keep none, and the difference is the structural one this requirement
states below: they NAME UNITS, so their declarations ACCUMULATE — two `Removed from
canon by` markers declare two sets of removed units, both are read, and the
corpus's reading voids a marker per NAME rather than wholly — so a bound on
their count would be a bound on how many units one change may lawfully remove,
which no capability has ever asked for. This form names no units. It declares
ONE RELATION between two documents, so a second marker in one block does not add
to the first: it states a SECOND BASIS for one text, and a block resting on two
bases rests on neither, no reader being told which addition the text was written
over. A block carrying more than one marker of this form SHALL be reported, with
the same remedy a wrong basis has — withdraw every declaration but the one that
is true.

**THE `by` IDENTIFIER SHALL BE THE CHANGE THAT CARRIES THE BLOCK, and it is
VALIDATED rather than merely resolved.** The identifier written after `by` SHALL
EQUAL the id of the change whose delta carries the marker's block, on the reading
this capability's other two reserved forms already have: `Removed from canon by`
and ``Merged into `<title>` by`` name the change that PERFORMED the declared act,
and the change performing this declaration is the one writing the block. A marker
whose basis is right and whose `by` names an unrelated change is NOT a lesser
defect than a wrong basis — it is a FALSE PROVENANCE, sending every later reader
who follows the identifier to a packet that declared nothing, while the block
promotes looking declared. BOTH halves are therefore checked and a marker failing
either SHALL be reported: the obligation is stated HERE, where the form is
defined, and `doc-health` is where the reading of it is enforced, neither being a
substitute for the other.

**A PAIRED CONVERSION DOES NOT MOVE THE IDENTIFIER, and needs no exception to
this rule.** `release-realization` provides that a conversion of the block to
`## ADDED Requirements`, lawful only as a paired act, RETAINS this marker as
provenance. The block's FORM changes and its CARRIER does not — the converting
change is the same change that wrote the block — so the retained marker's `by`
identifier is still the carrying change's own id, and the retention stands
without narrowing or widening what this paragraph requires.

**THIS FORM NAMES NO UNITS, and that is the difference that matters.** The two
existing forms name units they declare removed; this one names a DOCUMENT PAIR
and declares nothing about carriage, because in this shape there is nothing to
compare — no promoted requirement exists to compare against. A marker of this
form SHALL NOT suppress any unit, SHALL NOT be read as naming any unit, and
SHALL NOT be reported under the rule that reports a marker naming a unit the
block still carries. Like every marker, it is NOT itself a carriage unit in
either direction, so no later block restates it and dropping it declares
nothing.

**THE PROPOSAL'S CROSS-REFERENCE IS STILL OWED AND IS NOT A SUBSTITUTE.**
`release-realization` requires the modifying proposal to reference the change it
is declared relative to, and that reference is a fact about the two CHANGES. The
marker is a fact about the two BLOCKS: a proposal may name a sibling for a dozen
reasons and may carry several MODIFIED blocks, so a change-level mention cannot
say which requirement rests on which sibling. Both are required and they are
different declarations.

**A BASIS THAT IS NOT RATIFIED SHALL BE DECLARED AS SUCH AND NOT AS CANON.**
`release-realization` scopes its ordering obligation to an active RATIFIED
change and this requirement does not widen it. Where the declared basis is a
change that is not ratified, the declaring block rests on text no authority has
accepted; the marker is still owed, the reason clause SHALL DISCLOSE that the
basis is unratified, and the modifying change SHALL NOT describe the requirement
it modifies as settled.

**THE DISCLOSURE HAS A FORM, because an obligation only a reader can check is an
obligation nothing checks.** The reason clause discloses by CARRYING THE WORD
`unratified` — in prose or as a code span, this form naming no units either way
— read case-insensitively after the same whitespace normalization the marker
itself is read under. The sentence it sits in stays the author's to write. This
is the bargain every reserved form in this capability already strikes: the FORM
is what a checker reads and the PROSE is what a reader reads, and asking a
checker to decide whether a sentence discloses would be the prose rule this
whole marker design refuses. The obligation is stated HERE, where every reserved
marker in the corpus is defined; `doc-health` is where the reading of it is
enforced, and neither is a substitute for the other.

#### Scenario: A block is written over a sibling's addition
- **WHEN** an active change's `## MODIFIED Requirements` block names a requirement the promoted specification does not carry, and an active change ADDS or RENAMES to that title
- **THEN** the block MUST carry a marker of the reserved `Modified over` form naming that change as a code span, and naming as its `by` identifier the change whose delta carries the block
- **AND** the change's own `proposal.md` MUST still reference that change as `release-realization` requires, the two declarations being about different things

#### Scenario: The marker names a change that does not add the requirement
- **WHEN** a `Modified over` marker names a change that neither ADDS nor RENAMES to the block's capability and requirement title
- **THEN** the declaration MUST be reported, a basis that does not exist being worse than an undeclared one because it stops the next reader looking

#### Scenario: The marker's `by` identifier names a change other than the carrier
- **WHEN** a `Modified over` marker names as basis a change that does ADD or RENAME to the block's capability and requirement title, and its `by` identifier is an id other than that of the change whose delta carries the block
- **THEN** the declaration MUST be reported, a marker naming the right basis under the wrong author being a false provenance rather than an incomplete declaration
- **AND** a marker whose `by` identifier IS the carrying change's own id MUST NOT be reported on that ground, the identifier being validated against the carrier rather than merely resolved
- **AND** a marker RETAINED as provenance through a paired conversion MUST NOT be reported on that ground either, the converting change being the change that carried the block

#### Scenario: A block carries two markers of this form
- **WHEN** one `## MODIFIED Requirements` block carries more than one paragraph of the reserved `Modified over` form
- **THEN** the block MUST be reported, one pairing admitting one declaration and a second marker stating a second basis for one text rather than adding to the first
- **AND** the remedy MUST be to withdraw every such marker but the one that is true, no reading of two bases making the block rest on either
- **AND** the two unit-naming forms MUST NOT be read as bounded by this rule, their declarations accumulating because each names its own units

#### Scenario: The marker is read as declaring a deletion
- **WHEN** a block carries a `Modified over` marker and omits a unit
- **THEN** the marker MUST NOT be read as declaring that omission, this form naming no units
- **AND** the marker MUST NOT itself be reported as a marker naming a unit the block still carries, that rule reaching only the forms that name units

#### Scenario: The declared basis is not ratified
- **WHEN** the change whose addition a block is written over carries a status other than `ratified`
- **THEN** the marker MUST still be carried and its reason clause MUST state that the basis is unratified, by carrying the word `unratified`
- **AND** a reason clause omitting that word MUST NOT be read as disclosing it however the rest of the sentence is worded, this disclosure being read by form like every other part of this marker
- **AND** `release-realization`'s ordering obligation MUST NOT be read as reaching that change, its antecedent naming an active ratified change and this requirement widening it in no way

#### Scenario: One change both adds and modifies one requirement
- **WHEN** a single change carries both an `## ADDED Requirements` block and a `## MODIFIED Requirements` block for one capability and requirement title
- **THEN** the delta MUST be reported, a change modifying its own unpromoted addition having written two texts for one requirement where the second is simply the first
- **AND** a `Modified over` marker naming the change itself MUST NOT be read as curing it
- **AND** a change that RENAMES a promoted requirement to that title and modifies it in one delta MUST NOT be reported on this ground, that shape being the rename-and-amend one `doc-health`'s promoted resolution order resolves against canon under the OLD name (`openspec/specs/doc-health/spec.md:1568-1574`, with the scenario at `:1783-1786`), a `## RENAMED Requirements` block carrying a pair of titles rather than a second text
