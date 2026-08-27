# document-lifecycle Specification Delta

## ADDED Requirements

### Requirement: A MODIFIED requirement block restates the requirement as canon currently states it
A `## MODIFIED Requirements` block SHALL restate its promoted requirement as
canon states it when the block is written or last amended — carrying every
scenario the requirement keeps and every body clause the change is not
deliberately changing — and any scenario or clause the change deliberately
deletes SHALL be declared by a reserved marker in the delta itself.

**OpenSpec's `MODIFIED` REPLACES a requirement wholesale; it does not merge.**
Whatever the block says is what canon says after the archive act, so a clause
or scenario the block does not restate is a clause or scenario the archive
deletes. Nothing in the gate set notices: `openspec validate --strict` checks a
delta's shape — the heading, the keyword on the first line, at least one
scenario — and never what promotion will do to the document being replaced.

**The defect is a function of time, not of care.** A block written correctly
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
authoring time rather than only at an archive gate, and it is the half that the
ordinary reading of "write a correct delta" misses.

**A deliberate deletion is legitimate, and it SHALL be declared by form rather
than by prose.** Removing a scenario or a clause is a normal governance act;
removing one by not mentioning it is not. The declaration SHALL be a reserved
marker paragraph inside the MODIFIED block, naming each deleted unit as a
CommonMark code span: `**Removed from canon by <change-id> (<YYYY-MM-DD>):**`
for a deletion, and
``**Merged into `<destination scenario title>` by <change-id> (<YYYY-MM-DD>):**``
where two scenarios legitimately become one — the destination being where the
superseded scenarios went rather than a unit the marker names. A unit that
itself contains backticks is fenced with a longer run of them, as CommonMark
provides. Naming a scenario title declares the bullets that scenario carried
removed with it, unless they appear elsewhere in the block. A marker is not
itself a unit anything later has to restate. The marker is deliberately a NEW reserved
form and NOT the corpus's existing dated bold note, because every such note in
the corpus today records a caught near-miss and a restoration rather than a
deletion — one of them naming seven scenario titles in backticks as restored —
so a rule that read deletion out of prose would misread faithful restatements
as declarations of loss. A recorded disposition in the aggregation checkout's
`health/dispositions.yaml` is the fallback for a delta that is ratified and
cannot be re-authored; nothing else declares a deletion.

**Where two active changes write one requirement, `release-realization` already
governs the order and this requirement does not restate or widen it.** That
capability's "Ordered deltas and branch vocabulary" requires that a proposal
modifying a requirement already modified by an active RATIFIED change
references that change and declares its deltas relative to that change's
outcome; the reference is read as that change's id occurring as a whole token
in the later change's own `proposal.md`. This requirement adds only the
consequence for currency: a block declared relative to another active change's
outcome is measured against THAT outcome rather than against canon, and it
therefore carries the earlier change's additions as well as canon's.

#### Scenario: A block omits a scenario the requirement keeps
- **WHEN** an active change's `## MODIFIED Requirements` block restates a promoted requirement and does not restate a scenario that requirement currently carries
- **THEN** the block MUST be brought forward to carry that scenario, or the deletion MUST be declared by marker in the delta
- **AND** health tooling MUST report the omission against the active delta's own path, before the change archives

#### Scenario: Canon moves under a long-lived active change
- **WHEN** a requirement is amended in canon after an active change's MODIFIED block for it was written
- **THEN** the block MUST be brought forward before that change archives
- **AND** the passage of time MUST NOT be read as an excuse: the obligation attaches to the block for as long as the change is active

#### Scenario: A deletion is deliberate
- **WHEN** a change intends to delete a scenario or a body clause the promoted requirement carries
- **THEN** the delta MUST carry a reserved marker naming that unit as a code span
- **AND** a declared deletion MUST NOT be reported as a currency defect
- **AND** a marker naming a unit the block still carries MUST NOT be read as declaring anything

#### Scenario: Two active changes modify one requirement
- **WHEN** a proposal modifies a requirement that an active ratified change already modifies
- **THEN** the later proposal MUST reference the earlier change and declare its deltas relative to that change's outcome, exactly as `release-realization` requires and with no wider obligation added here
- **AND** the later block MUST carry the earlier change's additions as well as canon's, because whichever archives last is the text canon keeps

#### Scenario: A MODIFIED block names a requirement canon does not carry
- **WHEN** a MODIFIED block names a capability and requirement title the promoted specification does not carry
- **THEN** the title MUST resolve to a requirement an active sibling change ADDS or RENAMES
- **AND** a title resolving to neither canon nor an active sibling MUST be reported, a block modifying nothing being a block whose promotion silently adds text nobody reviewed as an addition
