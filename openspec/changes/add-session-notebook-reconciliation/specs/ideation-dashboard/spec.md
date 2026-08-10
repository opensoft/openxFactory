# ideation-dashboard

## ADDED Requirements

### Requirement: A session notebook is retirable after its session has already ended
A session notebook SHALL have a governed retirement route that does not require its session to still be live, because the two governed endings are not the only ways a session ends: a worktree and its branch can be removed directly — by a probe, or by clearing crash residue — and neither runs the abandon path, so neither retires the notebook.

The targeted retirement route SHALL CONTINUE to refuse a branch with no live session. That refusal is what prevents a caller inventing a session and retiring a notebook belonging to a live one, and it SHALL NOT be relaxed to admit dead sessions. The route for a session that has already ended SHALL instead be RECONCILIATION over the session namespace, which establishes death from the absence of any live session claiming the notebook rather than from a caller's assertion about one branch.

A retirement performed by reconciliation SHALL be reported as a reconciliation, distinguishable from a retirement performed by a governed ending, so the record does not claim an abandon that never happened.

#### Scenario: A hand-removed session's notebook is retired
- **WHEN** a session's worktree and branch have been removed without an abandon, leaving its notebook alive
- **THEN** the reconciliation route establishes that no live session claims that notebook and retires it
- **AND** the targeted `--session-ref` route still refuses that branch, because no live session bears it

#### Scenario: The targeted route keeps refusing a dead branch
- **WHEN** a caller names a branch with no live session for targeted retirement
- **THEN** the request is refused naming the joint liveness signal, unchanged by this capability's new route
