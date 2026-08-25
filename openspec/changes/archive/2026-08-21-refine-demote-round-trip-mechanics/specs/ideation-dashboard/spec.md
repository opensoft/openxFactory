# ideation-dashboard

## MODIFIED Requirements

### Requirement: Demote refreshes a staged topic's outline and never silently replaces it
The reverse transition SHALL leave the demoted topic's primary fragment carrying the ACTUAL text of the last attempted `proposal.md` and the demoted change's own provenance, and MUST NOT reset that fragment to the pre-proposal aspirational snapshot the change folder holds. The primary fragment is the file the existing deterministic, path-only selection already names; this requirement adds no second candidate file and MUST NOT change that selection.

A returning file whose destination is the topic's declared primary fragment SHALL keep `Status: staged`. It MUST NOT be flipped to `Status: draft`: the same selection rule still calls that file the staged topic's outline, so a draft status there makes the document disagree with every reader of it. The `Status: draft` flip remains correct and unchanged for the proposal documents returning to the topic's `openspec/` workspace.

The reverse transition SHALL fill the fragment's round-trip provenance slots from values it holds when it executes — the change id, the date demoted, the demote reason, the date the change was raised, and the change's state at demote. The state-at-demote slot SHALL carry the change's status TOGETHER WITH its task progress where the change records tasks, because the status alone is a constant: the reverse transition refuses any change that is not active, so a status-only slot can never distinguish one demote from another. Where the change records no tasks, the slot SHALL carry the status alone rather than a fabricated count. A value that is genuinely unavailable SHALL be recorded as unavailable and MUST NOT be fabricated or left reading as an unused placeholder.

The fragment's proposal-element sections — the sections wrapped in the ratified `xspec:candidate` marker grammar — SHALL be refreshed from the corresponding sections of the returned `proposal.md`. Only sections present in BOTH the fragment and the returned proposal SHALL be rewritten; the refresh MUST NOT invent a section the proposal does not carry, and MUST NOT delete a section the proposal omits. Where the demoted change carries no `proposal.md`, the provenance slots SHALL still be filled and the sections left untouched.

**The snapshot is a fallback SOURCE, never the authority.** Where the destination fragment already exists and differs from the change folder's snapshot of it, the reverse transition MUST NOT replace the destination's bytes. The refresh SHALL apply INTO the existing fragment, bounded to the provenance slots and the marked proposal-element sections, leaving every other byte of that file unchanged; and the snapshot copy SHALL be preserved in the topic beside it under a non-colliding name and named in the transition's own record, so that nothing is discarded either. Only where no fragment exists at the destination SHALL the snapshot be restored first and then refreshed. No live human work is ever silently replaced by a demote.

EXACTLY ONE addition is carved out of that byte bound, and it is not part of the refresh. Where the destination fragment carries no lifecycle status header at all, the reverse transition SHALL add one — the `staged` status the primary-fragment rule above already requires — and SHALL name that addition in its execution record. Without it the reverse transition leaves behind a fragment the forward transition refuses, making the cycle one-way for the very topic it has just returned material to; a live fragment can reach that state because it is the human's own working document and never had to pass the forward gate to acquire a header. It is an ADDITION and never a rewrite: a header the fragment already carries is the human's statement about their own document and MUST NOT be changed. No other byte outside the provenance slots and the marked proposal-element sections may be written.

The refresh SHALL be idempotent: applying it twice with the same inputs SHALL produce the same bytes. It SHALL preserve the destination document's own line-ending flavor rather than translating it.

#### Scenario: The state-at-demote slot carries progress beside the status
- **WHEN** a change recording tasks is demoted
- **THEN** the state-at-demote slot MUST carry the change's status and its task progress together
- **AND** the progress MUST come from the change's own recorded tasks rather than being counted a second way

#### Scenario: A demoted change records no tasks
- **WHEN** a change with no recorded tasks is demoted
- **THEN** the state-at-demote slot MUST carry the status alone
- **AND** a task count MUST NOT be fabricated

#### Scenario: The returning outline keeps its staged status
- **WHEN** a demote returns a file whose destination is the topic's declared primary fragment
- **THEN** that file MUST keep `Status: staged`
- **AND** the proposal documents returning to the topic's `openspec/` workspace MUST still continue as `Status: draft`

#### Scenario: The proposal-element sections carry the real prior text
- **WHEN** a topic that reached proposal is demoted and the change carries a `proposal.md`
- **THEN** the fragment's `xspec:candidate` proposal-element sections MUST carry that proposal's actual text
- **AND** they MUST NOT carry the pre-proposal aspirational text the change folder snapshotted

#### Scenario: The destination fragment already exists and differs
- **WHEN** a demote's primary-fragment destination exists and differs from the change folder's snapshot of it
- **THEN** the destination's bytes MUST NOT be replaced by the snapshot
- **AND** the provenance slots and the marked proposal-element sections MUST be refreshed in place, leaving every other byte of that file unchanged
- **AND** the snapshot MUST be preserved in the topic under a non-colliding name and named in the transition's record

#### Scenario: The live fragment carries no lifecycle status header
- **WHEN** a demote's primary-fragment destination exists, differs from the snapshot, and carries no lifecycle status header
- **THEN** a `staged` header MUST be added and named in the execution record
- **AND** every other byte outside the provenance slots and the marked proposal-element sections MUST still be unchanged
- **AND** a header the fragment already carries MUST NOT be changed

#### Scenario: The refresh runs twice
- **WHEN** the reverse transition's fragment refresh is applied twice with the same inputs
- **THEN** the resulting bytes MUST be identical
- **AND** the document's own line-ending flavor MUST be preserved rather than translated

## ADDED Requirements

### Requirement: The reverse transition resolves its origin staging topic from a declared order
The reverse transition SHALL resolve the staging topic it returns material to through a DECLARED PRECEDENCE ORDER rather than a single source: an explicitly supplied topic first, then the change's own recorded origin where that origin declares a staged kind, then a possibles-register pick edge naming the change. The first source that answers SHALL win, and an explicitly supplied topic SHALL always win, because a human naming the destination is the most direct statement of intent available.

A change whose recorded origin is not staged — an ad-hoc origin, or none — SHALL NOT have a staging topic inferred for it. The reverse transition SHALL refuse with a stated reason and name the explicit option instead, because a change that never came from staging has no topic to return to and inventing one would move material somewhere nobody chose.

The resolution MUST NOT depend solely on register state the forward transition destroys. A pick edge points at a staging folder, the forward transition removes that folder, and a resolution reading only pick edges therefore fails for exactly the changes that actually reached proposal — which is the condition a demote exists to reverse.

#### Scenario: A change that reached proposal is demoted with no pick edge present
- **WHEN** a change whose recorded origin declares a staged kind is demoted, and no possibles pick edge names it
- **THEN** the origin staging topic MUST be resolved from the change's own recorded origin
- **AND** the demote MUST NOT refuse for want of a topic

#### Scenario: An explicitly supplied topic is offered alongside a resolvable origin
- **WHEN** a human supplies a staging topic explicitly and the change's recorded origin also names one
- **THEN** the explicitly supplied topic MUST be used

#### Scenario: A change with no staged origin is demoted
- **WHEN** a change whose recorded origin is ad-hoc or absent is demoted with no explicit topic
- **THEN** the reverse transition MUST refuse with a stated reason
- **AND** it MUST NOT infer a staging topic
- **AND** the refusal MUST name the explicit option

### Requirement: The reverse transition's own artifacts do not block the topic's next transition
Every artifact the reverse transition writes into a staging topic SHALL satisfy the same governed-document rules the forward transition enforces on that topic, so that a topic which has received returned material can be transitioned again without an operator working around an artifact the reverse transition itself left behind. In particular a governed markdown artifact it writes SHALL carry a valid lifecycle status header.

This is a round-trip obligation rather than a formatting preference: the reverse transition is one half of a cycle whose other half refuses governed markdown without a status header, so an artifact that fails that rule makes the cycle one-way for the topic it was applied to.

#### Scenario: A returned topic is transitioned again
- **WHEN** a topic that has received returned material through the reverse transition is transitioned forward again over its whole folder
- **THEN** the forward transition MUST NOT refuse because of an artifact the reverse transition wrote
- **AND** every governed markdown artifact the reverse transition wrote MUST carry a valid lifecycle status header
