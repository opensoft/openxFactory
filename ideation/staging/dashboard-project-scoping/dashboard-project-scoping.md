# Staged: Dashboard Project Scoping — a project is a named set of repos you can create, select, and work inside

Status: staged
Kind: capability-proposal
Summary: The dashboard already knows about projects — `project-register.yaml` declares `projects[].repositories[]`, the snapshot generator consumes it, and the surface renders by-repository / by-project / by-project-group toggles. What it cannot do is let a human MAKE one. Brett named the gap 2026-08-02: *"I am looking for something that lists existing projects and allows for use to create new project. when the user selects create new, they type the name and then select repos to add to that project. we then store that. then allow the user to later select the project, then a repo in that project or all repos in that project. so selecting the repo in a project really becomes a filtering property. The dashboard then shows the items in that project. and when i click on a tile on a wheel, that is tied to a repo and my dashboard operations for that tile are in that repo."* Three layers sit inside that sentence, and only the first is small.
Topics: ideation-dashboard, project-register, repo-selector, project-scoping, multi-repository, tenant-project-catalog, session-plane, governed-write
Repository context: the register instance is aggregation-owned (`xFactory/project-register.yaml`); openxFactory owns the neutral `project-register` schema; codexFactory owns the dashboard, the selector, and the session/gate plane that layer 3 would change
Staging ID: `openxFactory:staging:dashboard-project-scoping`
Source: Brett, 2026-08-02, after the doxBench engagement closed — asked whether the repo selector could grow project grouping and whether the work could run in parallel with the 012 browser-repair wave
Target capabilities: MODIFIED `ideation-dashboard` (project CRUD affordance, project-scoped selection, per-tile repository binding); possibly MODIFIED `project-register` schema if a project acquires state beyond navigation
Related: `ideation/brainstorm/tenant-project-catalog-and-workstation-cache.md` (2026-07-27) is the runtime-authoritative version of the same idea — this topic is its dashboard-side, single-workstation realization and should not contradict it

## What already exists (so the delta is honest)

- `project-register.yaml` (aggregation root) declares `projects[]` with `id`,
  `name`, `repositories[]`, and an optional `project_groups[]` roll-up.
- `openxFactory/contracts/schemas/project-register.schema.yaml` is the
  ratified neutral shape; grouping is explicitly **descriptive navigation
  only — it confers no lifecycle state and no authority**.
- The generator resolves `repository -> project -> project_group` and stamps
  those fields onto every snapshot; the surface already offers the three
  grouping toggles.
- The publication lane iterates every repository id in the register.
- TODAY'S CONTENT: exactly ONE project (`xfactory`) holding all eleven
  repositories, and ZERO project groups. The register's own header says why:
  *"Brett has not named a grouping layout."*

So the navigation machinery is built and idle. What is missing is (1) a way to
author the register from the surface, (2) a meaning for "the whole project" as
a view, and (3) a repository binding for tile operations.

## The three layers

### L1 — Project CRUD from the surface (small)

List the register's projects; create one by naming it and checking
repositories; persist. The schema already fits, so this is a form plus a
write.

The write is the only interesting part: `project-register.yaml` is currently
READ-ONLY input, lives in the **aggregation** repo (not the served corpus),
and every existing dashboard write is a human-gated, loopback-only, recorded
gate action confined to the served checkout. A register write is none of
those things by default — it is a different repository and a config file
rather than corpus content.

### L2 — Project as a filter (medium; one real decision)

"Select the project, then a repo in it **or all repos in it**."

- *One repo in the project* is nearly free: narrow the existing selector's
  roster to the project's members. The active snapshot stays a single
  `(repository, ref)` key, which is what everything downstream expects.
- *All repos in the project* is not free. The dashboard serves exactly ONE
  snapshot at a time; every wheel, funnel, count, and health aggregate derives
  from that one document. A project-wide view needs either a merged projection
  across N snapshots or an honest one-at-a-time compromise.

### L3 — Tile operations bound to the tile's repository (large)

*"when i click on a tile on a wheel, that is tied to a repo and my dashboard
operations for that tile are in that repo."*

This changes an assumption the whole session/gate plane rests on. Today the
serve binds `session_repository` ONCE at startup from the served checkout, and
path confinement is enforced per `(repository, ref)` entry. Every gate verb —
`create-document`, `edit-document`, `open-pr`, `abandon-session`, `propose` —
assumes one repository with one real checkout on disk, and the branch-session
machinery creates worktrees beside it.

Per-tile repository binding implies: multiple real checkouts reachable from
one serve, per-tile repository resolution instead of a bound value,
confinement per resolved repository rather than per bound one, and a session
key whose repository half is chosen at action time. That is a plane change,
not a UI change.

## Claims

1. **The grouping layer is content-starved, not missing.** One register edit
   naming real projects makes by-project navigation work immediately, with no
   code. Any proposal here should be able to state what the register edit
   alone buys, so the code delta is only what content cannot do.
2. **Authoring the register from the surface crosses a repository boundary
   the dashboard has never crossed.** Every governed write to date lands in
   the served corpus checkout. This one lands in the aggregation repo. Whether
   that is a gate action, a local-only config write, or an out-of-band edit is
   a decision, not a detail.
3. **"All repos in a project" is a derivation question wearing a UI hat.**
   The single-active-snapshot assumption is load-bearing for the wheel, the
   funnel, the counts, and the freshness header. Merging is possible; pretending
   the question does not exist is not.
4. **L3 is where the cost is, and it is not a dashboard cost.** It reopens
   `session_repository`, the confinement rule, and the worktree layout — the
   exact machinery `add-workbench-branch-sessions` ratified and doxBench has
   just finished exercising. It deserves its own change if it happens.
5. **This is the workstation-side twin of an existing brainstorm.**
   `tenant-project-catalog-and-workstation-cache` puts project→repository
   composition in a company runtime with per-principal projection. A local
   register-editing surface must not fork that model; at minimum it should
   name which side is authoritative when both exist.

## Open questions

- **Q1 — "All repos in a project": merged view or filtered one-at-a-time?**
  A merged projection needs rules for cross-repo counts, cluster identity,
  and a freshness header that must now describe N revisions. A filtered view
  keeps every existing derivation intact and makes "the project" a roster
  rather than a document. Which does Brett mean?
- **Q2 — Where does the register write land, and under what authority?**
  A gate action recorded in the served corpus (but the file is in another
  repo), a local-only preference the dashboard reads first, or a printed
  descriptor the human applies by hand (the existing degrade-to-CLI pattern)?
- **Q3 — Does a tile operation in a NON-served repository proceed or refuse?**
  Refusing keeps the plane's one-checkout assumption intact and makes project
  scope purely navigational. Proceeding is L3 and reopens the session plane.
  A middle path — operations allowed only in the served repository, with tiles
  from other repositories read-only and saying so — may be the honest v1.
- **Q4 — Do project groups get used, or is `projects[]` enough?** The schema
  supports a roll-up nobody has populated. Two levels of grouping that nobody
  needs is a cost.
- **Q5 — Authority when the tenant catalog exists.** If the runtime becomes
  authoritative for project→repository composition, is the local register a
  cache, an override, or retired?

## Exit path

Content first, then a proposal shaped by the answers:

1. **Immediate, no change needed:** Brett names the real projects in
   `project-register.yaml` (splitting the single `xfactory` project). This is
   an aggregation-repo edit that makes by-project navigation live and reveals
   how much of the ask was content.
2. Rule Q1 and Q3 — they decide whether this is a modest selector change or a
   plane change.
3. Raise an OpenSpec change against `ideation-dashboard` for L1 + L2 at the
   scope those rulings set. L3, if wanted, is a SEPARATE change against the
   session plane and should not ride the selector work.
4. Reconcile with `tenant-project-catalog-and-workstation-cache` before either
   lands, so the local surface and the runtime catalog agree about who owns
   project composition.

Parallelism: this topic touches the aggregation register, the dashboard
selector, and (only at L3) the session plane. It has no overlap with the
012 browser-repair work or the doxBench F5–F10 follow-ups, so it can proceed
in a separate session.
