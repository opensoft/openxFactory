# ideation-dashboard

## ADDED Requirements

### Requirement: Demote refreshes a staged topic's outline and never silently replaces it
The reverse transition SHALL leave the demoted topic's primary fragment carrying the ACTUAL text of the last attempted `proposal.md` and the demoted change's own provenance, and MUST NOT reset that fragment to the pre-proposal aspirational snapshot the change folder holds. The primary fragment is the file the existing deterministic, path-only selection already names; this requirement adds no second candidate file and MUST NOT change that selection.

A returning file whose destination is the topic's declared primary fragment SHALL keep `Status: staged`. It MUST NOT be flipped to `Status: draft`: the same selection rule still calls that file the staged topic's outline, so a draft status there makes the document disagree with every reader of it. The `Status: draft` flip remains correct and unchanged for the proposal documents returning to the topic's `openspec/` workspace.

The reverse transition SHALL fill the fragment's round-trip provenance slots from values it holds when it executes — the change id, the date demoted, the demote reason, the date the change was raised, and the change's status at demote. A value that is genuinely unavailable SHALL be recorded as unavailable and MUST NOT be fabricated or left reading as an unused placeholder.

The fragment's proposal-element sections — the sections wrapped in the ratified `xspec:candidate` marker grammar — SHALL be refreshed from the corresponding sections of the returned `proposal.md`. Only sections present in BOTH the fragment and the returned proposal SHALL be rewritten; the refresh MUST NOT invent a section the proposal does not carry, and MUST NOT delete a section the proposal omits. Where the demoted change carries no `proposal.md`, the provenance slots SHALL still be filled and the sections left untouched.

**The snapshot is a fallback SOURCE, never the authority.** Where the destination fragment already exists and differs from the change folder's snapshot of it, the reverse transition MUST NOT replace the destination's bytes. The refresh SHALL apply INTO the existing fragment, bounded to the provenance slots and the marked proposal-element sections, leaving every other byte of that file unchanged; and the snapshot copy SHALL be preserved in the topic beside it under a non-colliding name and named in the transition's own record, so that nothing is discarded either. Only where no fragment exists at the destination SHALL the snapshot be restored first and then refreshed. No live human work is ever silently replaced by a demote.

The refresh SHALL be idempotent: applying it twice with the same inputs SHALL produce the same bytes. It SHALL preserve the destination document's own line-ending flavor rather than translating it.

#### Scenario: The returning outline keeps its staged status
- **WHEN** a demote returns a file whose destination is the topic's declared primary fragment
- **THEN** that file MUST keep `Status: staged`
- **AND** the proposal documents returning to the topic's `openspec/` workspace MUST still continue as `Status: draft`

#### Scenario: The provenance slots are filled from the demote itself
- **WHEN** the reverse transition executes
- **THEN** the fragment's round-trip provenance slots MUST carry the change id, the demote date, the demote reason, the raised date, and the change's status at demote
- **AND** a value that cannot be resolved MUST be recorded as unavailable rather than invented

#### Scenario: The proposal-element sections carry the real prior text
- **WHEN** a topic that reached proposal is demoted and the change carries a `proposal.md`
- **THEN** the fragment's `xspec:candidate` proposal-element sections MUST carry that proposal's actual text
- **AND** they MUST NOT carry the pre-proposal aspirational text the change folder snapshotted
- **AND** no section absent from the proposal MUST be invented, and no section the proposal omits MUST be deleted

#### Scenario: A demoted change carries no proposal document
- **WHEN** the reverse transition executes for a change with no `proposal.md`
- **THEN** the provenance slots MUST still be filled
- **AND** the fragment's proposal-element sections MUST be left exactly as they were

#### Scenario: The destination fragment already exists and differs
- **WHEN** a demote's primary-fragment destination exists and differs from the change folder's snapshot of it
- **THEN** the destination's bytes MUST NOT be replaced by the snapshot
- **AND** the provenance slots and the marked proposal-element sections MUST be refreshed in place, leaving every other byte of that file unchanged
- **AND** the snapshot MUST be preserved in the topic under a non-colliding name and named in the transition's record

#### Scenario: The destination fragment is absent
- **WHEN** a demote's primary-fragment destination does not exist
- **THEN** the snapshot MUST be restored to it and then refreshed
- **AND** the restored fragment MUST carry `Status: staged` and the filled provenance slots

#### Scenario: The refresh runs twice
- **WHEN** the reverse transition's fragment refresh is applied twice with the same inputs
- **THEN** the resulting bytes MUST be identical
- **AND** the document's own line-ending flavor MUST be preserved rather than translated
