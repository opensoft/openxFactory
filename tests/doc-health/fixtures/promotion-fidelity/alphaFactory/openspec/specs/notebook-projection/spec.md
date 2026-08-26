# notebook-projection Specification

## Purpose
Fixture canon reproducing openxFactory's own live gap: a whole ADDED
requirement missing, and a MODIFIED requirement that arrived one scenario short.

## Requirements
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
