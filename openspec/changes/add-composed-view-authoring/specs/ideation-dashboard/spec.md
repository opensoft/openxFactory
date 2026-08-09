# ideation-dashboard

## MODIFIED Requirements

### Requirement: Composed views are read-only with a repository jump
On a composed snapshot every TILE-BOUND gate-bearing affordance SHALL hide — such a verb binds to the tile's own repository, and a serve has a writable checkout for one repository only — and the expanded tile SHALL offer one navigation verb, "open in <repo>", which switches the active snapshot to that tile's member repository, where every verb works as on any single-repository view. Per-tile repository binding remains a successor change.

CREATING A NEW DOCUMENT is not tile-bound and SHALL remain available on a composed view. A new document lands in the serve's OWN checkout — the same tree an unscoped view would have written to — so the composed projection makes it no less safe; refusing it made the one view where cross-repository convergence is visible the one view unable to act on it. The affordance SHALL read the serve's own capability rather than the view's projection, and SHALL be offered only where the serve declares a writable repository.

The serve SHALL DECLARE that repository on its capabilities route, reported from the same authority a write is refused against, so the two cannot disagree. A client SHALL NOT infer it: under a composed view the rendered snapshot's repository is the PROJECT identifier, which names no repository and is correctly refused. A created document SHALL name the declared repository, and the existing refusal of any write naming a repository this serve does not write to SHALL remain in force unchanged.

#### Scenario: Tile-bound gate verbs hide on a composed view
- WHEN the rendered snapshot carries `generation.composed_from`
- THEN no tile-bound gate-bearing affordance renders anywhere in the view

#### Scenario: A tile jumps to its repository
- WHEN a human invokes "open in <repo>" on a composed tile
- THEN the active snapshot switches to that tile's `(repository, ref)` and the page reloads with every verb available as today

#### Scenario: A new document may be drafted from a composed view
- WHEN a human drafts a staging seed on a composed project view and the serve declares a writable repository
- THEN the hand-off into the authoring surface is offered
- AND the created document names the declared repository rather than the project

#### Scenario: The serve declares what it can write
- WHEN the capabilities route is read
- THEN it reports the repository this serve writes into, matching the value a write is refused against

#### Scenario: No writable repository, no offer
- WHEN the serve declares none
- THEN the hand-off is not offered and the reason is stated where the control would be
