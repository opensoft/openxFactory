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

## Decisions (Brett, 2026-08-06 — decision round with the fulfilling session)

- **D1 — "All repos in a project" is a TRUE MERGED VIEW.** One wheel, funnel,
  and count set spanning every member repository — a merged projection across
  N snapshots, with explicit rules for cross-repo cluster identity, count
  semantics, and an N-revision freshness header. The filtered
  one-at-a-time posture is the interim (it ships first in the series), never
  the destination.
- **D2 — The register write is a COMMISSION (record-then-fulfil).** A
  `create-project` gate verb on the propose/promote mechanic: the click
  records a `workflow-job` descriptor (the proposed project's id, name, and
  member repositories) plus a gate-action record; the fulfilment applies the
  edit to the aggregation-owned `project-register.yaml`. The dashboard never
  writes across the repository boundary itself, so the served-checkout
  confinement rule stays intact.
- **D3 — Tile operations in a non-served repository PROCEED (L3 happens).**
  Per-tile repository binding is in scope for this topic: multiple real
  checkouts reachable from one serve, action-time repository resolution,
  confinement per resolved repository. It lands as its own session-plane
  change (D6), not on the selector work.
- **D4 — `projects[]` only; no group affordance.** `project_groups` stays
  schema-supported and unpopulated; the create surface offers projects only.
  Groups return the day a real layout needs them.
- **D5 — The local register is dev-plane-authoritative, then a derived
  cache.** Authoritative ONLY until a tenant project catalog exists; when the
  runtime twin lands, the register becomes a derived, replaceable projection
  per the brainstorm's `workstation-project-cache` contract — never an
  override. Declared here so the two models cannot fork.
- **D6 — Three sequenced exit changes, not one.** (1) project CRUD commission
  + project-scoped selection; (2) the merged cross-repo projection; (3) the
  L3 per-tile repository binding. Each lands on its own gate; earlier value
  ships while later pieces are designed.
- **D7 — Content first: the register splits BY ROLE.** `core` (openxFactory),
  `domains` (AdxFactory, LedgerxFactory, MedxFactory, OpsxFactory,
  codexFactory), `medx-clinical` (HealthLinc, MedxEHR, openChart), `installs`
  (agenttower, cloudpc-install, hermes-install, omnigent-install,
  xfactory-installer). *As originally ruled, the schema's single-parent rule
  forced `medx-clinical` to claim only the clinical trio — superseded by D8.*
- **D8 — Repository membership is MULTI-PARENT (Brett, 2026-08-06, ruled
  during exit-1 realization).** "We want a repo to be able to live in
  multiple projects": a project is a named view over repositories, not an
  owner. Realized inside `add-project-scoped-selection` (design D-d): the
  snapshot's singular `project` survives as the first-declaring PRIMARY, an
  additive `projects` list carries full membership, the validator's
  repo-multi-parent error is dropped (project→group stays single-parent),
  and the create-project single-parent guard goes with it. First
  beneficiary: MedxFactory joins `medx-clinical` while staying in `domains`.

- **D9 — Merged-view cluster identity is a VIEW-SIDE UNION (Brett,
  2026-08-06, exit-2 decision round).** The ratified composition rule keeps
  namespacing every id per-repo (`MedxFactory::cl-kill-switch`) so edges
  stay uncorrupted; the wheel and canvas render same-TOPIC clusters as one
  merged tile whose membership lists each repository's contribution.
- **D10 — The merged view is READ-ONLY plus a jump (Brett, 2026-08-06).**
  Every gate verb hides on a composed view; each tile offers
  "open in <repo>", which switches the active snapshot to that tile's
  repository, where all verbs work as today. The honest bridge until exit 3
  lands per-tile binding.
- **D11 — Project aggregates derive from the register (Brett, 2026-08-06).**
  One aggregate per register project, derived automatically (members = the
  project's repositories present in the registry, at the default ref) — no
  hand-declared upkeep, and a commissioned project yields its merged view
  the moment its fulfilment lands.

## Open questions — resolved 2026-08-06

- Q1 (all-repos view shape) — RESOLVED by D1: true merged view, staged behind
  the filtered interim.
- Q2 (register-write authority) — RESOLVED by D2: commission, fulfilled into
  the aggregation repo.
- Q3 (non-served tile operations) — RESOLVED by D3: proceed; L3 is in scope
  as its own change.
- Q4 (project groups) — RESOLVED by D4: projects only.
- Q5 (tenant-catalog authority) — RESOLVED by D5: dev-authoritative, then
  derived cache.

## Exit path

Ruled 2026-08-06 (D6, D7):

1. **Content first (done with the rulings):** split `project-register.yaml`
   by role per D7 — an aggregation-repo edit that makes by-project navigation
   live immediately.
2. **Exit 1 — `add-project-scoped-selection`:** the `create-project`
   commission verb (additive gate-intent / gate-action-record growth, the
   shared undelivered-commission index, engine + route + CLI + selector
   affordance) and project-scoped selection (project picker narrows the
   selector roster to member repos, one at a time). Carries the D5 authority
   declaration.
3. **Exit 2 — `add-project-merged-projection`:** the D1 merged view — the
   cross-repo projection contract (cluster identity, counts, N-revision
   freshness) and the project-wide wheel/funnel rendering.
4. **Exit 3 — `add-project-tile-repository-binding`:** the D3/L3 session-plane
   change — multi-checkout serve, per-tile repository resolution, per-resolved
   -repository confinement. Sequenced strictly after exit 2 and reconciled
   with the `add-workbench-branch-sessions` machinery it touches.
5. Reconcile with `tenant-project-catalog-and-workstation-cache` before exit
   2 lands (D5 names the authority split; the twin names the runtime side).

Parallelism: this topic touches the aggregation register, the dashboard
selector, and (only at L3) the session plane. It has no overlap with the
012 browser-repair work or the doxBench F5–F10 follow-ups, so it can proceed
in a separate session.
