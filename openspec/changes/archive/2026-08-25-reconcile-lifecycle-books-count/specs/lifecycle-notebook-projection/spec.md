# lifecycle-notebook-projection — reconcile-lifecycle-books-count deltas

## MODIFIED Requirements

### Requirement: Corpus scan scope
The LIFECYCLE BOOKS' projection — one Ideation book per governed repository, plus the shared Working Drafts and Canon books — SHALL scan exactly the governed corpus at the default branch: the openxFactory repository and each DomainxFactory checked out under `xFactories/`. Nested git working copies below a scanned repository root — feature-branch worktree checkouts (including `<repo>-worktrees/` containers and branch-session worktrees), embedded clones, and nested submodule installs — MUST be excluded from every lifecycle book, so an unmerged or duplicate checkout can never project sources into one: a lifecycle book IS the lifecycle projection, and a projection of unmerged work is a misprojection. Branch-session notebooks (`xf-session-<topic>`) SHALL be the ONLY notebook surface permitted to read a worktree; they are never lifecycle books, they MUST NEVER contribute a source, a title, or a repository name to one, and their existence MUST NOT relax the exclusion above for any book. OpenSpec change artifacts remain excluded from status scanning while promoted capability specs project into the Canon book, and deliberate-violation test fixture corpora remain excluded.

#### Scenario: A worktree container sits under the scan root
- **WHEN** a directory under `xFactories/` holds git worktree checkouts rather than being a governed repository
- **THEN** the lifecycle-book sync MUST NOT scan it
- **AND** no source or repository title may derive from its contents

#### Scenario: A nested working copy sits inside a governed repository
- **WHEN** a directory below a scanned repository root carries its own `.git` entry
- **THEN** documents below that directory MUST be excluded from every lifecycle book

#### Scenario: A governed document also exists in a checkout
- **WHEN** an excluded working copy contains a document that also exists in the governed corpus
- **THEN** only the governed copy projects and no duplicate or colliding source title is created

#### Scenario: A canon book is offered a branch session's drafts
- **WHEN** a branch session holds unmerged drafts in its worktree and any lifecycle book — Ideation, Working Drafts, or Canon — is synced
- **THEN** those drafts MUST NOT appear in any lifecycle book, under any title
- **AND** they MUST reach a lifecycle book only after the session's pull request merges to the default branch

### Requirement: Branch-session notebooks
A branch session MAY carry ONE per-session NotebookLM notebook, named `xf-session-<topic>` for the session's tile, whose sources SHALL be synced FROM the session's git WORKTREE rather than from the served checkout, and it SHALL NOT be one of the lifecycle books. A session notebook's title MUST NOT use the `xf-wb-` workbench reference-set prefix: the two namespaces SHALL be DISJOINT, so the reference-set orphan sweep — which deletes every `xf-wb-*` notebook that no live workbench manifest binds — can never take a live session's notebook as a candidate, and a session needs no workbench manifest to survive it. A session notebook SHALL be created when its session starts and SHALL be RETIRED when the session ends by merge or abandon, torn down together with the worktree and the session's registry entry — its life is the session's life, so a stale notebook cannot outlive the branch it projected. The workbench SHALL offer a "refresh notebook" session action that re-syncs the session notebook from the worktree after edits, granting no authority beyond the sync the projection tooling already performs. Hybrid source-return imports for a session notebook SHALL write into the origin folder INSIDE THE SESSION WORKTREE, landing on the session branch as ordinary working material committed with the session's gate action, and the imported file's header contract — origin lifecycle status, `Kind: reference`, source workspace, `Authority: L1 notebook synthesis`, NotebookLM source id and title, and idempotency by source id — SHALL apply verbatim and unchanged. A session notebook's output SHALL carry `L1 notebook synthesis` authority exactly as a hybrid's does and MUST NOT decide policy, memory, release scope, OpenSpec approval, or customer-facing output. This is a projection-TOOLING capability only: NotebookLM knows uploaded SOURCES and not git, so nothing in the notebook family's contract changes beyond declaring the rule and the naming.

#### Scenario: A session notebook is created and synced
- **WHEN** a branch session starts with a session notebook
- **THEN** the notebook MUST be created as `xf-session-<topic>` for that tile and its sources MUST be synced from the session's worktree, not from the served checkout
- **AND** its title MUST NOT carry the `xf-wb-` reference-set prefix, so the workbench orphan sweep never treats it as a candidate

#### Scenario: A session's drafts change
- **WHEN** a human edits documents in the session worktree and invokes the refresh-notebook action
- **THEN** the session notebook's sources MUST be re-synced from the worktree so the notebook matches the branch's current drafts

#### Scenario: A session ends
- **WHEN** a branch session ends by merge or by abandon
- **THEN** its session notebook MUST be retired — torn down with the worktree and the session's registry entry — and MUST NOT continue to project the branch

#### Scenario: A session notebook returns source material
- **WHEN** an eligible non-seed source is imported from a session notebook
- **THEN** it MUST be written into the origin folder inside the SESSION WORKTREE and land on the session branch
- **AND** the imported file's header contract and idempotency rules MUST apply exactly as they do for a hybrid import on `main`

#### Scenario: Session-notebook output is consumed
- **WHEN** any answer, note, report, mind map, or audio from a session notebook is used in xFactory work
- **THEN** it MUST carry `L1 notebook synthesis` authority and MUST NOT decide policy, memory, release scope, OpenSpec approval, or customer-facing output
