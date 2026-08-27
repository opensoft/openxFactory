# document-lifecycle Specification Delta

## ADDED Requirements

### Requirement: A MODIFIED requirement block restates the requirement as canon currently states it
A `## MODIFIED Requirements` block SHALL restate its promoted requirement as
canon states it when the block is written or last amended — carrying every
scenario the requirement keeps and every body clause the change is not
deliberately changing — and any scenario or clause the change deliberately
deletes SHALL be named as deleted in the delta itself.

**OpenSpec's `MODIFIED` REPLACES a requirement wholesale; it does not merge.**
Whatever the block says is what canon says after the archive act, so a clause
or scenario the block does not restate is a clause or scenario the archive
DELETES. Nothing in the gate set notices: `openspec validate --strict` checks a
delta's SHAPE — the heading, the keyword on the first line, at least one
scenario — and never what promotion will do to the document being replaced.

**The defect is a function of TIME, not of care.** A block written correctly
against the canon of the day goes stale as canon moves under it, and it goes
stale silently, because nothing re-reads it. `add-doxchat-model-intake` was
written on 2026-08-21 against a pre-`02a71d6e` canon and was, on 2026-08-25,
holding the deletion of six body clauses, two scenarios and one reverted
scenario line (issue #351, corrected by PR #358).
`add-release-inventory-drift-check`, `add-promotion-fidelity-check` and
`add-duplicate-packet-check` each restated ONE of the eight scenarios of
`doc-health`'s "Deterministic check families" (issue #329). Every one of the
four was caught by a human, and one was caught only because a byte-for-byte
promotion verification was run by hand at the archive gate.

**Currency is owed continuously, not once at authoring.** The obligation
attaches to the block for as long as the change is active: a change whose
requirement moved in canon after the block was written SHALL bring the block
forward before it archives. This is what makes the rule enforceable at
authoring time rather than only at an archive gate, and it is the half that
the ordinary reading of "write a correct delta" misses.

**A deliberate deletion is legitimate, and it SHALL be declared where it
happens.** Removing a scenario or a clause is a normal governance act; removing
one by not mentioning it is not. The declaration SHALL be carried in the delta
itself, naming each deleted scenario by its exact title and quoting each
deleted clause, so that the record of the deletion travels with the text that
performs it. A recorded disposition in the aggregation checkout's
`health/dispositions.yaml` is the fallback for a delta that is ratified and
cannot be re-authored; nothing else declares a deletion — not a label, not a
title, not a claim in prose elsewhere in the packet.

**Where two active changes write one requirement, `release-realization`
already governs the order and this requirement does not restate it.** That
capability's "Ordered deltas and branch vocabulary" requires the later proposal
to reference the earlier change and declare its deltas relative to that
change's outcome. This requirement adds only the consequence for currency: a
block declared relative to another active change's outcome is measured against
THAT outcome rather than against canon, and it therefore carries the earlier
change's additions as well as canon's.

#### Scenario: A block omits a scenario the requirement keeps
- **WHEN** an active change's `## MODIFIED Requirements` block restates a promoted requirement and does not restate a scenario that requirement currently carries
- **THEN** the block MUST be brought forward to carry that scenario, or the deletion MUST be declared in the delta
- **AND** health tooling MUST report the omission against the active delta's own path, before the change archives

#### Scenario: Canon moves under a long-lived active change
- **WHEN** a requirement is amended in canon after an active change's MODIFIED block for it was written
- **THEN** the block MUST be brought forward before that change archives
- **AND** the passage of time MUST NOT be read as an excuse: the obligation attaches to the block for as long as the change is active

#### Scenario: A deletion is deliberate
- **WHEN** a change intends to delete a scenario or a body clause the promoted requirement carries
- **THEN** the delta MUST name that scenario by its exact title, or quote that clause, as deleted
- **AND** a declared deletion MUST NOT be reported as a currency defect

#### Scenario: Two active changes modify one requirement
- **WHEN** two active changes each carry a MODIFIED block for the same capability and requirement title
- **THEN** the later one MUST reference the earlier change and declare its block relative to that change's outcome, as `release-realization` requires
- **AND** the later block MUST carry the earlier change's additions as well as canon's, because whichever archives last is the text canon keeps

#### Scenario: A MODIFIED block names a requirement canon does not carry
- **WHEN** a MODIFIED block names a capability and requirement title the promoted specification does not carry
- **THEN** the title MUST resolve to a requirement an active sibling change ADDS or RENAMES, and that sibling MUST be referenced by this change
- **AND** a title resolving to neither canon nor an active sibling MUST be reported, a block modifying nothing being a block whose promotion silently ADDS text nobody reviewed as an addition
