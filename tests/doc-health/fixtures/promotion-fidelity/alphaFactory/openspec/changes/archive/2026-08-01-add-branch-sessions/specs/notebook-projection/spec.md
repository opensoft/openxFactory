# notebook-projection Specification Delta

## ADDED Requirements

### Requirement: Branch-session notebooks
A branch session SHALL project into its own notebook.

#### Scenario: A session notebook is created and synced
- **WHEN** a branch session opens
- **THEN** a session notebook MUST be created

#### Scenario: A session ends
- **WHEN** a branch session ends
- **THEN** its notebook MUST be retired

## MODIFIED Requirements

### Requirement: Corpus scan scope
The sync SHALL bound its scan.

#### Scenario: A worktree container sits under the scan root
- **WHEN** a worktree container is found
- **THEN** it MUST be skipped

#### Scenario: A nested working copy sits inside a governed repository
- **WHEN** a nested copy is found
- **THEN** it MUST be skipped

#### Scenario: A governed document also exists in a checkout
- **WHEN** a document exists twice
- **THEN** the governed copy wins

#### Scenario: A canon book is offered a branch session's drafts
- **WHEN** a canon book is offered session drafts
- **THEN** it MUST refuse them
