## Context

The xFactory aggregate currently records `opensoft/openChart` directly at
`xFactories/openChart`. The repository itself is independently usable and its
Medx integration is already digest/pin based, so the required boundary is a
small composition repository rather than a fork or copy of the upstream
application. The local workspace contains unrelated dirty changes in the
aggregate and MedxFactory checkouts; implementation must use explicit paths and
must not sweep those changes into commits.

## Goals / Non-Goals

**Goals:**

- Establish a local `MedxChart` Git repository as the Medx-facing composition
  boundary.
- Pin the current `openChart` commit through a nested submodule and a readable
  manifest using repository-relative or remote URLs only.
- Replace the xFactory aggregate's direct `openChart` submodule with a
  `MedxChart` submodule and keep the aggregate cloneable once the remote exists.
- Move the standalone `openChart` checkout to the workspace root without
  changing its Git history or tracked content.
- Update only the affected register, documentation, and provenance references.

**Non-Goals:**

- Creating, pushing, or changing a GitHub remote or repository visibility.
- Forking, copying, or rewriting the openChart application history.
- Changing clinical APIs, Frappe behavior, or vendored evidence digests.
- Rewriting unrelated dirty work in xFactory or MedxFactory.

## Decisions

### 1. MedxChart is a wrapper repository with a nested openChart submodule

`MedxChart/openChart` is a gitlink pinned to the current local openChart HEAD.
The wrapper contains the Medx boundary documentation and pin manifest, not a
second copy of the upstream source. A nested submodule makes the dependency
auditable and prevents accidental drift from a moving branch.

**Alternative considered:** fork or copy openChart into MedxChart. Rejected
because it would create two application histories and make upstream provenance
ambiguous.

### 2. The aggregate uses a relative MedxChart submodule URL

The xFactory superproject records `xFactories/MedxChart` with a relative URL
(`../MedxChart`). Locally this resolves to the new workspace-root repository;
when the xFactory remote and MedxChart remote are published under the same
GitHub owner, the same URL resolves to the sibling remote repository.

**Alternative considered:** commit a host-absolute local path. Rejected because
it violates portability and breaks other workstations.

### 3. Preserve upstream pins and distinguish them from aggregate pins

The nested gitlink records the exact openChart commit. The manifest records the
repository, commit, and source path for human and validator inspection. The
xFactory gitlink records the MedxChart wrapper commit. These are separate pins:
one selects the upstream application and one selects the Medx composition.

### 4. Keep existing runtime/vendored contracts stable

The change updates the aggregate's repository identity and path references, but
does not rewrite existing MedxFactory proof evidence whose source provenance is
already explicitly `openChart`. A future contract migration can promote
MedxChart as the source owner after the wrapper exposes a governed compatibility
surface; this topology change alone must not launder that provenance.

## Risks / Trade-offs

- [No remote yet] → The new local repository is cloneable from the current
  workspace but its eventual remote is not created by this change; the
  relative URL documents the intended same-owner remote layout.
- [Existing xFactory worktrees] → Other xFactory worktrees retain their old
  submodule checkout until they refresh from the aggregate change; only the
  canonical checkout is moved.
- [Spec Kit sibling path] → openChart's relative worktree-root setting must be
  adjusted or accompanied by a root-level worktree directory after the move.
- [Dirty shared trees] → Explicit pathspec staging and status checks prevent
  unrelated user changes from being committed.

## Migration Plan

1. Record the current openChart HEAD and verify the destination is absent.
2. Move the standalone checkout to the workspace root.
3. Initialize MedxChart, add the nested openChart submodule, and commit only
   MedxChart-owned files and its gitlink.
4. Replace the aggregate gitlink and `.gitmodules` entry, update the register
   and affected links, then commit only those aggregate paths.
5. Validate both submodule pins, portability, Git status, and YAML/Markdown
   consistency. Rollback is a reverse move plus restoring the previous
   aggregate gitlink; no upstream history is deleted.

## Open Questions

- The GitHub `opensoft/MedxChart` remote does not currently exist. Publishing
  it is intentionally outside this local change and requires a separate
  explicit remote-creation decision.
