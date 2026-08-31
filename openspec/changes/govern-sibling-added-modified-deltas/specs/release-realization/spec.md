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
BYTE-IDENTICAL. Everything this change adds is NEW text: two body paragraphs
and two scenarios. NOTHING IS DROPPED, no `Removed from canon by` or
`Merged into` marker is owed, and the modified-block-currency family therefore
reports zero findings against this delta — asserted, not assumed, in
`tasks.md` § 4.2.

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
assertions in individual proposals have been standing in for; those assertions
remain useful as local evidence and SHALL NOT be read as the source of the
obligation.

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
