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

### 2. The aggregate records MedxChart at the absolute `git@github.com:` URL its siblings use

**REVERSED 2026-08-25, RECORDED HERE 2026-09-03.** As authored this decision
read: "The xFactory superproject records `xFactories/MedxChart` with a relative
URL (`../MedxChart`). Locally this resolves to the new workspace-root
repository; when the xFactory remote and MedxChart remote are published under
the same GitHub owner, the same URL resolves to the sibling remote repository."
That is what landed at `bed2a69`, and it broke the nightly.

**What broke.** A relative submodule URL resolves against whatever URL cloned
the SUPERPROJECT, not against a fixed owner. On the nightly runner the
superproject is cloned over HTTPS, so `../MedxChart` resolved to a plain
`https://` URL — a form the workflow's `git@`-only token rewrite never touches
— and every nightly from 2026-08-24 died at the clone of these two submodules.

**What stands.** `opensoft/xFactory` `386e7ee2` (2026-08-25T19:13:51Z),
verbatim: *"A relative submodule URL resolves to whatever cloned the
superproject / MedxChart and MedxPractice entered .gitmodules as ../Medx* — on
the nightly runner the superproject is HTTPS, so they resolved to plain https://
URLs the workflow's git@-only token rewrite never touches, and every nightly
since 2026-08-24 died at their clone. Normalize both to the git@github.com: form
their eighteen siblings use; the openxfactory App now carries both repos, so the
rewritten token'd clone succeeds."* The live entry is
`url = git@github.com:opensoft/MedxChart.git`, and the ratified obligation in
`specs/medxchart-overlay-boundary/spec.md` is now that form.

**Alternatives considered.** (a) A host-absolute local path — rejected then and
still rejected: it violates portability and breaks other workstations. (b) The
relative `../MedxChart` — TRIED, LANDED, AND REVERSED for the reason above; it
is recorded rather than erased, because the argument for it ("the same URL
resolves to the sibling remote repository") is exactly the argument a later
reader would reinvent, and the thing that defeats it is not visible from the
argument. The residual cost of the absolute form is that a fork under another
owner must rewrite the URL; that cost is paid by eighteen sibling submodules
already and is what makes one convention rather than two.

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
  **DISCHARGED 2026-09-03 — the risk is spent and both halves of it turned
  out differently than written.** The remote EXISTS
  (https://github.com/opensoft/MedxChart, private, last pushed
  2026-08-23T20:23:45Z), so "not created by this change" is true of the task
  list and false of the world; and the relative URL did not document the
  intended layout, it broke the nightly and was reversed at `386e7ee2` —
  Decision 2.
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

- ~~The GitHub `opensoft/MedxChart` remote does not currently exist. Publishing
  it is intentionally outside this local change and requires a separate
  explicit remote-creation decision.~~
  **ANSWERED 2026-09-03: the remote exists and no separate decision is owed.**
  `gh repo view opensoft/MedxChart --json visibility,pushedAt,url` returns
  `{"pushedAt":"2026-08-23T20:23:45Z","url":"https://github.com/opensoft/MedxChart","visibility":"PRIVATE"}`
  — published the same day the boundary landed, hours after this question was
  written, and the aggregation has resolved `xFactories/MedxChart` against it
  ever since (`.gitmodules`: `git@github.com:opensoft/MedxChart.git`; gitlink
  `68d2f1f5db932cb5099ceac75dab66316ef22579`, equal to that repository's
  `main`). The visibility is PRIVATE, which is the answer to the half of the
  question that was really open: publishing the boundary does not publish the
  Medx composition. The question is closed and does not travel to another
  change.

**No open question remains in this packet.** The one thing it does not yet have
is the descendant's own pin validator and required check, and that is not an
open question — it is the BOUND FOLLOW-ON commissioned at `tasks.md` § 5, which
gates this change's ARCHIVE.
