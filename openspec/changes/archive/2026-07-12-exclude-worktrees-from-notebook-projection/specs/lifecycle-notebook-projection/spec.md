# lifecycle-notebook-projection Delta: Corpus Scan Scope

## ADDED Requirements

### Requirement: Corpus scan scope
The projection SHALL scan exactly the governed corpus: the openxFactory
repository and each DomainxFactory checked out under `xFactories/`. Nested
git working copies below a scanned repository root — feature-branch
worktree checkouts (including `<repo>-worktrees/` containers), embedded
clones, and nested submodule installs — MUST be excluded, so an unmerged or
duplicate checkout can never project sources into a lifecycle book. OpenSpec
change artifacts remain excluded from status scanning while promoted
capability specs project into the Canon book, and deliberate-violation test
fixture corpora remain excluded.

#### Scenario: A worktree container sits under the scan root
- **WHEN** a directory under `xFactories/` holds git worktree checkouts rather than being a governed repository
- **THEN** the sync MUST NOT scan it
- **AND** no source or repository title may derive from its contents

#### Scenario: A nested working copy sits inside a governed repository
- **WHEN** a directory below a scanned repository root carries its own `.git` entry
- **THEN** documents below that directory MUST be excluded from every book

#### Scenario: A governed document also exists in a checkout
- **WHEN** an excluded working copy contains a document that also exists in the governed corpus
- **THEN** only the governed copy projects and no duplicate or colliding source title is created
