# ideation-dashboard

## ADDED Requirements

### Requirement: The merged view spans the visible member set
The composed view SHALL render exactly the member repositories the human has made VISIBLE in the project's filter, under one of two set modes: UNION (every item belonging to a visible repository) or INTERSECTION (only items whose identity — the composed id's tail, or the unnamespaced key a collection uses instead — exists in EVERY visible repository). Intersection SHALL filter and never merge, so each repository's own copy stays a separately badged, separately openable row and two repositories' takes on one document can be read side by side. The narrowing SHALL be applied BEFORE the cluster union, so merged tallies count the visible contributions rather than the whole project, and `generation.composed_from` SHALL be trimmed to the visible members so the freshness header names the repositories actually rendered. Exactly one visible repository SHALL serve that repository's own snapshot with every capability it normally carries; any other count SHALL serve the project's composed, read-only aggregate, and an empty visible set SHALL render honestly empty rather than refusing. The visible set and mode are viewer state stored per project and resolved against current membership: a repository that leaves the project drops out of the stored set, a stored set that membership has outlived falls back to every member rather than rendering nothing, and nothing stored means every member under union — the composition's own answer.

#### Scenario: The union narrows to the ticked repositories
- WHEN a human hides a member repository in the project's filter
- THEN the composed view drops that repository's items, merged cluster tallies fall to the visible contributions, and the freshness header counts only the visible members

#### Scenario: The intersection shows only what every visible repository has
- WHEN the view mode is intersection over two or more visible repositories
- THEN only items whose identity exists in every visible repository render, each repository's copy as its own badged row
- AND an identity carried by some but not all of them does not render

#### Scenario: One visible repository is the interactive single view
- WHEN exactly one repository is visible
- THEN that repository's own snapshot is served with its full capabilities, exactly as selecting it directly always did

#### Scenario: The stored set survives a membership change
- WHEN a repository leaves the project after the human ticked a set
- THEN it drops out of the visible set, and a stored set that membership has outlived falls back to every member rather than rendering nothing

## MODIFIED Requirements

### Requirement: The openDox project-first header
The dashboard header SHALL brand as "Opensoft openDox" and SHALL organize repository navigation around the CURRENT PROJECT: a project dropdown whose first line is "New Project" (opening the create-project commission form) followed by the register's projects, defaulting to the viewer's last-used project when the register projection still names it and to the first register project otherwise — the viewer is always in a project. Repository selection SHALL be a filter scoped to the current project: a popover listing the project's member repositories. Where the project can be composed, that popover SHALL be a VISIBILITY control — each member row's indicator ticks its repository into or out of the view, one toggle chooses union or intersection over the visible set, `all` and `none` are offered as the two bulk moves, and the member name is the shortcut that makes that repository the only visible one — and the filter's own label SHALL state the visible count against the total. Where no member snapshot is published, and therefore nothing can be composed, the popover SHALL degrade to naming the merged view unavailable with the rows selecting one repository at a time.

#### Scenario: The header renders project-first
- WHEN the dashboard loads with a register projection available
- THEN the brand reads "Opensoft openDox", the project dropdown shows "New Project" first and the register's projects after it
- AND the current project is the stored last-used project, else the first register project

#### Scenario: The filter ticks repositories into the view
- WHEN a human toggles a member repository in the current project's filter popover
- THEN that repository enters or leaves the visible set, the view re-renders over the new set, and the filter label restates the visible count

#### Scenario: A member name selects that repository alone
- WHEN a human clicks a member repository's name in the filter popover
- THEN that repository becomes the only visible one and its own snapshot is served, exactly as the repository selector contract already specifies

#### Scenario: All-repositories awaits the merged view
- WHEN no member snapshot is published, so the project has no derived aggregate
- THEN the filter names the merged view as unavailable and the rows select one repository at a time

#### Scenario: The header degrades without a projection
- WHEN no register projection is served (a static image or no reachable register)
- THEN the project dropdown and filter do not render and the dashboard degrades exactly as the selector contract already specifies

### Requirement: Project membership editing is a recorded commission
The dashboard SHALL offer an `edit-project` verb on the human gate console — the filter popover's add line offering the known-repository candidates, and each member row a two-click removal control — that records a `project-register-edit` workflow-job descriptor carrying the added and removed member lists plus an `edit-project` gate-action record, and SHALL NOT write the register itself. Membership edits QUEUE: a project MAY carry several dispatched, undelivered edit commissions at once, each validated at commission time against the register with that project's pending commissions applied oldest-first — a dispatched create-project commission counting as the project existing, so a just-created project can be populated before its fulfilment lands — and same-second commissions MUST land as distinct descriptors. The commission SHALL be refused when the project exists neither in the register projection nor as a pending creation, when an addition is outside the roster-or-register repository universe, when an addition is already an effective member (register or pending), or when a removal is not an effective member. Removing the last member is legal, because a project MAY be empty (created first, populated later); pending membership changes SHALL render as clearly-marked overlay, netted across the queue, until the fulfilment lands the register edit.

#### Scenario: A repository is added and another removed
- WHEN a human commissions an addition from the filter's add line or a removal from a member row's armed removal control
- THEN one `edit-project` descriptor records the diff and one gate-action record names the human
- AND the register is unchanged until the commission's fulfilment applies the edit

#### Scenario: An empty project is legal
- WHEN a project is created with no member repositories, or an edit removes its last member
- THEN the commission is accepted — the project exists awaiting its next additions, and the register schema admits the empty set

#### Scenario: Successive edits queue instead of refusing
- WHEN a human commissions a second membership edit while the project's earlier edit commission is dispatched and undelivered
- THEN the second commission records as its own descriptor, validated against the register with the pending commissions applied oldest-first
- AND a duplicate addition against that pending-applied state is still refused
- AND the fulfilment delivers the queued commissions oldest-first

#### Scenario: Pending membership renders as overlay
- WHEN edit-project commissions are dispatched and undelivered
- THEN the affected repositories badge as pending in the popover, netted across the queue, and the register projection's truth plane is unchanged
