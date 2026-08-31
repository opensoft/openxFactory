# release-realization Specification Delta

THE BLOCK BELOW IS DECLARED AGAINST CANON, not against any sibling's outcome.
`openspec/specs/release-realization/spec.md:64-78` carries this requirement
today and NO OTHER ACTIVE CHANGE WRITES THIS REQUIREMENT — measured with the
currency family's own resolver, which returns `canon` for this block.

THE NEIGHBOUR IS NAMED RATHER THAN LEFT TO SILENCE, a preamble that is true only
because it says nothing being the shape this packet exists to report.
`add-structured-scope-substrate` holds an active `## MODIFIED Requirements` block
on THIS SAME SPECIFICATION, over "Realization axis declaration" — a different
requirement, which the block below neither restates nor touches. Two active
changes writing two different requirements of one spec raises no ordering
question between them, and the currency family's ordering arm groups by
`(capability, requirement)` rather than by capability for exactly that reason.

THE CARRIAGE, STATED AS MEASURED RATHER THAN AS SUMMARISED. Both promoted body
sentences are restated BYTE-IDENTICAL and both promoted scenarios are restated
BYTE-IDENTICAL. Everything this change adds is NEW text: FOUR body paragraphs
and FOUR scenarios (the antecedent, the archive order, the conversion clause and
the falsified-scenario clause, each with its own scenario). NOTHING IS DROPPED,
no `Removed from canon by` or `Merged into` marker is owed, and the
modified-block-currency family therefore reports zero findings against this
delta — asserted, not assumed, in `tasks.md` § 4.2.

## MODIFIED Requirements

### Requirement: Ordered deltas and branch vocabulary
Changes SHALL sequence explicitly: a proposal modifying a requirement
already modified by an active ratified change references that change and
declares its deltas relative to that change's outcome. The three branch
kinds SHALL be used as distinct vocabulary: the change folder (content
branch), Spec Kit feature branches, and release branches (integration);
releases are branches while open and tags at promotion.

**THE ANTECEDENT REACHES A REQUIREMENT AN ACTIVE RATIFIED CHANGE ADDS, AND NOT
ONLY ONE IT MODIFIES.** A proposal MODIFYING a requirement that an active
ratified change ADDS — a requirement the promoted specification does not yet
carry — SHALL reference that change and declare its deltas relative to that
change's outcome, on the same terms and for the same reason as the
already-modified case: whichever writer archives last is the text canon keeps.
The two antecedents are DISJOINT by construction, a requirement being either
one canon carries or one it does not, so this reaches a shape the
already-modified antecedent cannot and widens that antecedent in no way.

**THE ORDER OF THE TWO ARCHIVE ACTS IS PART OF THE OBLIGATION, because in this
shape one order is safe and the other destroys review.** A change carrying such
a block SHALL NOT archive while the requirement it modifies is unpromoted. The
adding change archives first, the requirement enters canon, and the modifying
block is then a block over canon like any other. In the other order the
modifying block promotes a requirement nobody reviewed as an addition, and the
adding change is left holding an `## ADDED Requirements` block for a title canon
already carries. This obligation is the RULE the per-packet pre-archive
assertions in individual proposals have been standing in for — BOTH the `grep`
that reads canon for the title AND the CONVERSION CLAUSE some of those packets
carry beside it, which the next paragraph states generally rather than leaving to
be re-derived one packet at a time. Those assertions remain useful as local
evidence and SHALL NOT be read as the source of the obligation, and a general
rule that reached less than the per-packet text it replaces would be a narrowing
wearing a generalization's label.

**CONVERTING THE BLOCK TO `## ADDED` DOES NOT DISSOLVE THE OBLIGATION, because
the antecedent attaches to the PAIRING and not to the block's form.** Re-shaping
a `## MODIFIED Requirements` block written over an active ratified change's
addition into an `## ADDED Requirements` block leaves two changes adding one
requirement — a worse state than the one it escapes, the ordering question being
unresolved and no longer declared anywhere. Conversion is therefore lawful ONLY
AS A PAIRED ACT ruled by the authority that ratified the two packets: ONE ruling
amends BOTH, the adding change striking or re-scoping its addition, and the
converting block RETAINING the `Modified over` marker it carried, as provenance,
so that the pairing stays declared after the block's form changes. That retention
is a retention and not a new marker obligation: `document-lifecycle` scopes the
form's REQUIREMENT to `## MODIFIED Requirements` blocks and this widens that
scope in no way. An UNPAIRED conversion SHALL NOT be taken.
Where one is taken it is a breach, and the evidence it leaves is the shape this
rule's mechanical backstop reads: before either archives, two active additions of
one title; after the converting change archives, an active `## ADDED
Requirements` block for a title canon now carries.

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

#### Scenario: Two changes touch one requirement
- **WHEN** a proposal modifies a requirement that an active ratified change already modifies
- **THEN** the later proposal MUST reference the earlier change and declare its deltas relative to that change's outcome

#### Scenario: A release promotes
- **WHEN** a release branch merges to the implemented line and realization completes for its changes
- **THEN** the release is tagged and the branch is retired

#### Scenario: A proposal modifies a requirement an active ratified change adds
- **WHEN** a proposal carries a `## MODIFIED Requirements` block for a requirement the promoted specification does not carry and an active ratified change ADDS
- **THEN** that proposal MUST reference the adding change and declare its deltas relative to that change's outcome, exactly as it must where the earlier writer MODIFIES
- **AND** the already-modified antecedent MUST NOT be cited as the authority for this shape, its antecedent naming a requirement canon carries and this one naming a requirement canon does not

#### Scenario: The modifying change reaches its archive gate first
- **WHEN** a change carrying such a block reaches its archive gate while the requirement it modifies is still unpromoted
- **THEN** it MUST NOT archive, the adding change archiving first
- **AND** a local pre-archive assertion in that change's own task list MUST NOT be treated as the source of the obligation, being evidence that this rule was met rather than the rule

#### Scenario: The modifying change converts its block rather than waiting
- **WHEN** a change carrying such a block re-shapes it into an `## ADDED Requirements` block instead of waiting for the adding change to archive
- **THEN** the conversion MUST NOT be treated as discharging this obligation, its antecedent attaching to the pairing of the two changes and not to the form of either block
- **AND** the conversion MUST be a PAIRED act ruled by the authority that ratified both packets, one ruling amending both so that the adding change strikes or re-scopes its addition and the converting block retains the `Modified over` marker it carried as provenance
- **AND** an unpaired conversion MUST NOT be taken, and where one is taken the addition left standing for a title canon then carries is the surviving evidence of the breach

#### Scenario: Landed reality falsifies the adding change's scenario before its archive
- **WHEN** the repository's landed state — a cut contract release, a merged realization, a promoted specification — contradicts a scenario of the `## ADDED Requirements` block a modifying change is waiting on
- **THEN** the adding change MUST amend that scenario before it archives, by the amendment route a ratified packet takes and with its owner consenting
- **AND** the archive order MUST still hold, the falsification being neither licence to invert it nor licence to convert the modifying block
