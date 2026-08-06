# ideation-dashboard

## ADDED Requirements

### Requirement: The openDox project-first header
The dashboard header SHALL brand as "Opensoft openDox" and SHALL organize repository navigation around the CURRENT PROJECT: a project dropdown whose first line is "New Project" (opening the create-project commission form) followed by the register's projects, defaulting to the viewer's last-used project when the register projection still names it and to the first register project otherwise — the viewer is always in a project. Repository selection SHALL be a filter scoped to the current project: a popover listing the project's member repositories where selecting one makes it the active served repository, with an "All repositories" line that is disabled (naming the merged view as pending) until the project merged view exists and thereafter selects the project's derived aggregate.

#### Scenario: The header renders project-first
- WHEN the dashboard loads with a register projection available
- THEN the brand reads "Opensoft openDox", the project dropdown shows "New Project" first and the register's projects after it
- AND the current project is the stored last-used project, else the first register project

#### Scenario: The filter switches the served repository
- WHEN a human selects a member repository in the current project's filter popover
- THEN that repository becomes the active served snapshot exactly as the repository selector contract already specifies

#### Scenario: All-repositories awaits the merged view
- WHEN the project merged view is not yet available
- THEN the filter's "All repositories" line renders disabled and names the merged view as pending
- AND once the merged view exists the line selects the project's derived aggregate

#### Scenario: The header degrades without a projection
- WHEN no register projection is served (a static image or no reachable register)
- THEN the project dropdown and filter do not render and the dashboard degrades exactly as the selector contract already specifies

### Requirement: Project membership editing is a recorded commission
The dashboard SHALL offer an `edit-project` verb on the human gate console — the filter popover's manage mode, a checkbox per register repository seeded from current membership — that records a `project-register-edit` workflow-job descriptor carrying the added and removed member lists plus an `edit-project` gate-action record, and SHALL NOT write the register itself. The commission SHALL be refused when the project does not exist in the register projection, when an addition is outside the roster-or-register repository universe, when a removal is not currently a member, when the removals would leave the project with no members, or while the project carries an undelivered edit commission; pending membership changes SHALL render as clearly-marked overlay until the fulfilment lands the register edit.

#### Scenario: A repository is added and another removed
- WHEN a human applies a manage-mode diff adding one repository and removing another
- THEN one `edit-project` descriptor records both lists and one gate-action record names the human
- AND the register is unchanged until the commission's fulfilment applies the edit

#### Scenario: Emptying a project is refused
- WHEN a manage-mode diff would remove every member repository
- THEN the commission is refused citing the at-least-one-member rule and nothing is persisted

#### Scenario: Pending membership renders as overlay
- WHEN an edit-project commission is dispatched and undelivered
- THEN the affected repositories badge as pending in the popover and the register projection's truth plane is unchanged
