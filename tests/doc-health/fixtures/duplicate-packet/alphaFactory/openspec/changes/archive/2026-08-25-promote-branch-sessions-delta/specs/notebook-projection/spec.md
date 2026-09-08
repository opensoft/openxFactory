# notebook-projection Specification Delta

## ADDED Requirements

### Requirement: Branch-session notebooks
A branch session SHALL project into its own notebook, and that notebook SHALL
be the only surface permitted to read a worktree.

#### Scenario: A session notebook is created and synced
- **WHEN** a branch session opens
- **THEN** a session notebook MUST be created

#### Scenario: A session ends
- **WHEN** a branch session ends
- **THEN** its notebook MUST be retired
