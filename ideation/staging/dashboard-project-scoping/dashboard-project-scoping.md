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

- **D12 — The dashboard is "Opensoft openDox" (Brett, 2026-08-06, header
  design round).** The brand line and page title rename; "xFactory /
  ideation dashboard" retires. The header's crowded picker cluster
  (repo chip + project picker + repo select + "+ project") is the
  confusion this round fixes.
- **D13 — The current project is a dropdown; "New Project" is its first
  line (Brett, 2026-08-06).** Then the register's projects. Default: the
  last-used project (session-stored), falling back to the first register
  project — the user is always IN a project; no unscoped line. "New
  Project" opens the create-commission form (the existing verb, rehomed).
- **D14 — Repo selection becomes a FILTER icon scoped to the current
  project (Brett, 2026-08-06).** The popover lists the project's member
  repositories; single-select makes one the active (served) repository. An
  "All repositories" line sits on top, disabled with a coming-merged-view
  note until exit 2 lands, then it selects the project's merged projection.
- **D15 — Membership edits are an `edit-project` COMMISSION (Brett,
  2026-08-06).** The filter popover gains a manage mode (checkbox per
  register repository); applying commissions a register-edit descriptor
  carrying add[]/remove[] — recorded, human-gated, fulfilled like
  create-project, with pending changes badged until the fulfilment lands.
  A project always keeps at least one member (the schema's own rule).

- **D16 — The filter works like the dropdown (Brett, 2026-08-06, ruled
  via the vibe-annotate channel on the live header).** The popover's first
  line is "add repository…" (an inline candidate pick commissioning a
  single-addition edit-project); each member row carries an eyeball on the
  left showing whether the repository is visible in the current view, and a
  trash control on the right that arms on first click and commissions the
  single-removal edit on the second. Manage mode retires; same engine verb,
  same pending badges.

- **D17 — A project may be EMPTY (Brett, 2026-08-06).** "It is better if
  we allow a project to exist without a repo defined": create the project
  first, add repositories later through edit-project commissions. The
  register schema's minItems rule is reversed, the create-project non-empty
  guard and the edit-project last-member floor are dropped, and the create
  panel marks members optional.

- **D19 — The view is the VISIBLE SET, union or intersection (Brett,
  2026-08-07).** "The 'view' selector would be best as 1. all, 2. the
  visible union, 3. the visible intersection. We can make this a toggle of
  union and intersection. Then make a select all or deselect all." The
  filter popover's eyeball stops being an indicator and becomes the
  control: each member row ticks its repository into or out of the view,
  the composed snapshot spans exactly the ticked set, and one toggle
  chooses union (everything the ticked repositories have) or intersection
  (only identities EVERY ticked repository has — matched on the composed
  id's tail). `all` / `none` are the two bulk moves, so "all" needs no
  line of its own. One visible repository serves ITS OWN snapshot, fully
  interactive — which is the pre-D19 single-select outcome reached through
  the same control — and two or more serve the project's composed,
  read-only aggregate; the member name solos as the one-click shortcut.
  Narrowing happens BEFORE the D9 cluster union, so tallies count the
  visible set, and `composed_from` is trimmed so the freshness header names
  what is on screen. Intersection FILTERS rather than merges: each
  repository's copy stays its own openable row.

- **D21 — The repo selector IS a lens; give it the lens widget (Brett,
  2026-08-07).** "Our repo selector is now very similar to the lens function
  but for documents in repos vs keywords in documents. Figure out how to
  make a lense widget for this repo selector where the repos would be our
  selector checkboxes instead of keywords. We can then make a drill in
  dashboard that looks at that set of documents only." The observation is
  exact: the lens engine reads a snapshot in only two places (the
  vocabulary with counts; which terms a document carries), so a projection
  — repositories as terms, cross-repository document IDENTITIES as
  documents — serves the whole widget unchanged, and the rings become
  CARRIER COUNTS. Which also names D19/D20 in the lens's own vocabulary:
  union is ring 1 and inward, shared is ring 2 and inward, and the old
  strict intersection was the centre. Realization ruled the same day: the
  switch lives inside the Lens tab (one widget, two vocabularies); the
  filter keeps its own quick control with the lens as the deep view, both
  driving one visible set; and the drill-in is a scoped dashboard view with
  no new persistence — saving a repository recipe would be a successor
  change with real gate-verb growth. Realized as `add-repository-lens`.

- **D20 — SHARED means two or more, not all (Brett, 2026-08-07).** "Make
  intersection mean shared by 2+ visible repos." D19's second mode was
  strict set intersection (present in EVERY visible repository); the live
  data showed why that is the wrong threshold — across the five-factory
  `domains` project, all-of-them keeps 2 document identities while
  two-or-more surfaces the 8 cluster topics the factories actually
  converge on (`cl-consent`, `cl-handoff`, `cl-mailbox`…). The mode is
  therefore renamed SHARED: the label reads `∩ shared`, and the code stops
  claiming a set operation it no longer performs. With two repositories
  visible the two rules coincide, so this only changes behaviour at three
  or more.

- **D18 — Project edits QUEUE (Brett, 2026-08-07).** Ruled after two live
  one-in-flight refusals while populating `xfactory` member by member: the
  single-flight guard on `edit-project` is dropped. Successive edits each
  record their own commission, validated against the register WITH the
  project's dispatched, undelivered commissions applied oldest-first — a
  pending CREATE counts, so a just-created project can be populated before
  its fulfilment lands — and the fulfilment lane delivers them oldest-first
  in one pass. `create-project` keeps its single-flight guard: a project is
  created once.

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
