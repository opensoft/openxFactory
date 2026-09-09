# document-lifecycle Delta: Gates Happen On Main

## ADDED Requirements

### Requirement: Gates happen on main
A lifecycle transition (organize, propose, ratify, archive, and register dispositions) SHALL be performed against, and merged promptly to, the default branch to be considered real; an unmerged transition on any branch is exploration, not status, and MUST NOT be represented as the document's lifecycle state on shared surfaces.

The shared (hosted) dashboard projects the default branch, so this rule makes "visible on the dash" synonymous with "governed"; per-branch previews are the local dashboard's role. Intent-plane applications satisfy this by construction (the apply lane commits to the default branch via rolling PR).

#### Scenario: A branch-side move is not a transition
- **WHEN** an engineer moves a document between lifecycle areas on an unmerged branch
- **THEN** shared surfaces continue to show the document's main-branch state until the move merges

#### Scenario: Console actions land on main
- **WHEN** a gate-console verb or applied intent performs a transition
- **THEN** the resulting artifacts are committed to the default branch (directly by an authorized human, or via the lane's rolling PR)
