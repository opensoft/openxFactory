## Why

Abandoned-session cleanup currently recognizes only an exact staged topic linked to an active proposal. Once that proposal archives or is explicitly demoted—or the tile becomes orphaned after its material is dispositioned—the cleanup gate can never open even though durable lifecycle evidence exists, leaving local branches permanently stranded.

## What Changes

- Replace the active-proposal-only cleanup precondition with an evidence-based retention-disposition check.
- Continue accepting a live proposal, and additionally accept an archived change whose recorded staged origin resolves to the exact tile.
- Accept an explicitly demoted proposal only when execution—not merely a demotion plan—is durably evidenced for the exact destination tile; add an execution receipt for new demotions and a bounded compatibility proof for existing returned drafts.
- Permit an absent/orphaned current tile to be cleaned when branch ownership, session abandonment, and an accepted retention disposition all resolve independently to the same tile identity.
- Add an explicit human retention-release lane for abandoned branches whose material was deliberately discarded or superseded outside the exact proposal lineage, with a required reason and a main-resident record naming the tile, branch tip, and prior abandonment proof.
- Keep refusing dispatch-only proposals, unexplained missing tiles, crashed or merely non-live sessions, live worktrees, mismatched branch families, and any cleanup lacking durable abandonment proof.
- Record and report the exact evidence that released retention so a deletion remains auditable after the branch is gone.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `ideation-dashboard`: Broaden human-invoked abandoned-session branch cleanup from active-proposal presence to durable, exact-tile lifecycle disposition evidence while preserving all existing fail-closed ownership and abandonment checks.

## Impact

- Affected specification: `openspec/specs/ideation-dashboard/spec.md`.
- Affected implementation: `scripts/ideation_dashboard/branch_session.py`, cleanup routing/CLI reporting, demotion execution recording, and the lifecycle evidence readers used to resolve active, archived, and demoted changes.
- Affected contracts: additive `cleanup-abandoned-branch` gate-action vocabulary and its exact scope/head/evidence record shape in `contracts/schemas/gate-action-record.schema.yaml`.
- Affected tests: abandoned-session cleanup, archive-origin resolution, demotion transition evidence, orphaned-tile handling, and negative evidence/mismatch cases under `tests/ideation-dashboard/`.
- Affected documentation: `docs/ideation-dashboard-session-runbook.md` and related operator guidance.
- No GitHub branch-protection, remote-branch deletion, or automatic cleanup behavior changes; cleanup remains local, explicit, and human-invoked.
