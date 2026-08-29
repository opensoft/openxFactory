# doc-health Specification Delta

ADDED ONLY. No `## MODIFIED Requirements` block is opened on "Currency of an
active change's MODIFIED requirement blocks" — the same measurement
`add-unclassified-finding-class` recorded as its D1 holds here and is re-taken
against today's canon in the proposal's § Orchestrator Decisions D2.

## ADDED Requirements

### Requirement: A MODIFIED block over an active sibling's addition is evaluated for its pairing, not for its carriage
The modified-block-currency family SHALL evaluate every `## MODIFIED
Requirements` block whose title resolves to an active change's ADDED or RENAMED
requirement — the shape its resolver returns as `pending` — and SHALL report the
pairing where it is undeclared, misdeclared, or self-referential, instead of
dropping the block before its checks run.

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

**THE CHECK SHALL REPORT EXACTLY THREE STATES, and be silent on the fourth.**

- **UNDECLARED** — the block carries no marker of the reserved `Modified over`
  form. Reported.
- **MISDECLARED** — the block carries such a marker and the change it names
  neither ADDS nor RENAMES to the block's capability and requirement title.
  Reported, and reported apart from UNDECLARED in the finding's own words,
  because a wrong basis and an absent one have different remedies.
- **SELF-REFERENTIAL** — the change that carries the block is itself the change
  that adds the requirement. Reported, and a marker naming the change itself
  MUST NOT clear it.
- **DECLARED AND RESOLVING** — a marker names an active change that does add or
  rename to the title, and that change is not this one. NO FINDING IS EMITTED.
  A correctly declared pair is the state this check exists to produce, and a
  standing row for it would be a permanent advisory nobody should act on.

**THE FINDINGS SHALL FORM ONE NEW FINDING CLASS of this family**, reported
against the active delta's own path like every other finding this family emits,
carrying the `warning` band and one action line stating both halves of the
remedy: declare the basis by marker, and hold the archive until the declared
change promotes. The class SHALL be registered in the family's own class
registry with its own identifier and label, and SHALL be placed by the family's
class map; a finding this new class emits that the map does not place is an
unplaced finding like any other and is reported by the class that reports those.

**ITS RULE TEXT SHALL BE RENDERED FROM A REGISTERED ARM TEMPLATE.** The family
derives its unplaced-finding mask from its own arm templates, so a rule text
built any other way would have no shape the mask can compute and would be
reported as drift on every run that emitted one. One template SHALL carry all
three reported states, distinguished by an interpolated clause, because one
template is one shape is one map entry — the three states share a band and an
action and differ only in why.

**THE BAND IS `warning` AND THE FAMILY STAYS ABSENT FROM `FAMILY_RESOLUTION`.**
This is the measure-then-flip posture every family of this group launched under,
and here it is also the only honest one: the population this check reports is
the corpus's existing four pairs, none of which was authored under a rule that
existed. Raising the band, or classifying the family `contested`, is one later
decision taken by ruling AFTER that standing population is discharged, never
before; and the family's continued absence from `FAMILY_RESOLUTION` is already
required by "A modified-block-currency finding its own class map cannot place is
itself a finding", which this requirement does not disturb.

**THE CHECK READS EVERY ACTIVE CHANGE REGARDLESS OF LIFECYCLE STANDING**, as
this family's reading rule already provides, and this is deliberately wider than
the ordering obligation `release-realization` scopes to an active ratified
change. A finding SHALL name the declared or resolved basis change and, where
that change is not ratified, SHALL say so, so that a reader can see at a glance
whether an obligation or only an observation stands behind the row.

#### Scenario: A block over a sibling's addition carries no marker
- **WHEN** an active change's MODIFIED block names a requirement the promoted specification does not carry, an active change ADDS or RENAMES to that title, and the block carries no `Modified over` marker
- **THEN** the run MUST emit one `warning` finding against the active delta's own path, naming the requirement, the change whose addition it resolves to, and that no marker declares the pairing
- **AND** the three comparison arms MUST NOT run against that block, there being no promoted requirement to compare it to
- **AND** the finding MUST NOT cause a run configured `--fail-on error` or `--fail-on critical` to fail

#### Scenario: A block over a sibling's addition is correctly declared
- **WHEN** such a block carries a `Modified over` marker naming an active change other than its own that ADDS or RENAMES to the block's capability and requirement title
- **THEN** no finding MUST be emitted for that block, a declared pairing being the state this check exists to produce

#### Scenario: The marker names a change that does not add the requirement
- **WHEN** such a block carries a `Modified over` marker naming a change that neither ADDS nor RENAMES to its capability and requirement title
- **THEN** the run MUST emit a `warning` finding naming the change the marker names and stating that it adds no such requirement
- **AND** that finding MUST be worded apart from the undeclared case, a wrong basis and an absent one having different remedies

#### Scenario: A change modifies its own unpromoted addition
- **WHEN** one change carries both an ADDED and a MODIFIED block for one capability and requirement title
- **THEN** the run MUST emit a `warning` finding against that delta
- **AND** a `Modified over` marker naming that same change MUST NOT suppress it

#### Scenario: A declared basis archives
- **WHEN** the change a block is declared over archives and its addition reaches the promoted specification
- **THEN** the block MUST resolve against canon on the next run and the three comparison arms MUST run against it
- **AND** this check MUST emit nothing further for that block, its question having been answered by the promotion

#### Scenario: The `Modified over` marker is not a carriage declaration
- **WHEN** a block carries a `Modified over` marker
- **THEN** that marker MUST NOT suppress any unit of any comparison, and MUST NOT be reported as a marker naming a unit the block still carries
- **AND** the marker paragraph MUST NOT be counted as a body unit of the block or of the requirement it promotes into

#### Scenario: A finding of this class is dispositioned
- **WHEN** `health/dispositions.yaml` carries an entry naming this family, a repository, an active delta path, and a `cite`
- **THEN** findings of this class on that path MUST be suppressed on the same terms as this family's other findings
- **AND** an entry without a `cite`, or an entry naming another family, MUST suppress nothing

### Requirement: An active ADDED block for a requirement the promoted specification already carries is reported
The modified-block-currency family SHALL report every active change's `## ADDED
Requirements` block naming a capability and requirement title the promoted
specification already carries, at `warning`, against that delta's own path.

**THIS IS THE ARCHIVE-ORDERING BACKSTOP, and it is the only direction in which
one can exist.** Where a MODIFIED-over-an-addition pair archives in the safe
order the requirement enters canon first and every existing check resumes. Where
it archives in the unsafe order the modifying block promotes text nobody
reviewed as an addition, and the surviving evidence is precisely this: an active
change still holding an ADDED block for a title canon now carries. Nothing in
the estate reads that shape. The family that compares an archived delta to canon
cannot, canon being the delta after the archive act; the family reading active
MODIFIED blocks does not read ADDED blocks at all. Reading it here costs one
lookup against a promoted-requirement index this family already builds.

**THE CHECK IS NOT LIMITED TO THE PAIR THAT MOTIVATES IT.** An ADDED block over
a requirement canon already carries is a defect however it arose — a stale
packet, a duplicated title, an addition that should have been a modification —
and narrowing the check to blocks that had a MODIFIED partner would decline to
report the same defect for a worse reason.

**THE FINDING SHALL BE ITS OWN CLASS**, registered and templated on the same
terms as every other class this family carries, and SHALL carry an action line
naming the two remedies: promote nothing further until the collision is
resolved, and convert the addition to a modification declared against canon
where the requirement genuinely already exists. The band is `warning` and the
family stays absent from `FAMILY_RESOLUTION`.

**THE POPULATION IS ZERO ON THE AUTHORING TREE, and that is the argument for
building it now.** A check whose standing population is empty costs nothing to
land, pins a state every reader already assumes, and is in place before the
first instance rather than after it — which for this shape matters more than
usual, because the first instance is an archive act that cannot be taken back.

#### Scenario: An active ADDED block names a requirement canon carries
- **WHEN** an active change's `## ADDED Requirements` block names a capability and requirement title the promoted specification already carries
- **THEN** the run MUST emit one `warning` finding against that delta's own path, naming the requirement and the promoted specification that carries it
- **AND** the finding MUST NOT cause a run configured `--fail-on error` or `--fail-on critical` to fail

#### Scenario: The unsafe archive order is taken
- **WHEN** a change carrying a MODIFIED block over an active sibling's addition archives before that sibling, so the requirement enters canon from the modifying block
- **THEN** the sibling's still-active ADDED block MUST be reported by this check on the next run, the collision being the surviving evidence of the ordering breach
- **AND** the report MUST NOT be read as curing the breach, an archive act being outside what any health run can undo

#### Scenario: No active change adds a requirement canon carries
- **WHEN** every active `## ADDED Requirements` block names a title the promoted specification does not carry
- **THEN** this check MUST emit nothing, and its class MUST still render in the family's class block at a count of zero
