# openDox Persistence and Truth — A Database Beside Git — Brainstorm

Status: brainstorm
Kind: architecture
Summary: The ruling adds a database to a product whose entire safety story is
that git is the record, and Brett settled the composition the same day — RULED
2026-09-04: the database owns IDENTITY AND COORDINATION (users, memberships,
projects, the project-to-repository mapping, sessions, unsaved drafts) and git
owns GOVERNED ARTIFACTS, read from repositories and written back only through
the apply lane, so every existing gate stays valid and the database is
disposable relative to the corpus; this document keeps the four-option space it
was chosen from, records what was rejected and why, and works through the
consequences the ruling now makes concrete.
Topics: opendox, openxdox, ideation-dashboard, project-register, persistence,
database, git-authority, derived-cache, governed-derived-model,
workflow-gate-contract, document-lifecycle, tenant-project-catalog, feat-request
Repository context: openxFactory owns `document-lifecycle`,
`workflow-gate-contract` and the `project-register` schema, all three of which
this question touches; the runtime would live in `opensoft/openDox`
Captured: 2026-09-04

## Possible feats

- **A declared authority boundary** — RULED 2026-09-04; the feat is now
  WRITING IT DOWN as a contract (identity and coordination in the database,
  governed artifacts in git, apply lane as the only write path) so the two
  models cannot fork the way D5 was written to prevent.
- **Repository creation as a first-class openDox act** — the ruling keeps specs
  in git, so a new project needs a new repository the app can create, or the
  origin complaint returns one level down.
- **Apply-lane hardening** — under the ruling it is the only write path to
  governed content, and it has one dispatch in its entire history.
- **A pre-governed scratch space** — somewhere a half-thought can live that is
  neither a governed document nor a draft OF one.
- **The governed-write bridge** — every write that changes governed content
  goes to git through a branch session and lands in the database as a
  projection of the commit, not the other way round.
- **A cache with a declared staleness contract** — if the database is derived,
  it needs the same freshness-and-refusal discipline the snapshot registry
  already has.
- **An audit table that is not the audit** — gate acts recorded in Postgres for
  query, with the commit as the record of standing.
- **Event-sourced project state** — projects, membership and settings as an
  append-only log whose materialization is the database and whose export is git.

## RULED — Q1, Brett Heap, 2026-09-04 (issue #656)

**The database owns identity and coordination; git owns governed artifacts.**

- **In the openDox database:** users, memberships, projects, the
  project-to-repository mapping, sessions, and unsaved drafts.
- **In git:** specs, changes, ideation documents and contracts — read from
  repositories, and **written back only through the apply lane**.
- **Therefore:** every existing gate stays valid. doc-health still reads a tree.
  OpenSpec still validates packets. The PR checks still gate on refs. And the
  database is **disposable relative to the corpus** — losing it loses
  coordination state, never governed content.
- **Rejected:** documents in the database with git as an export (option A
  below); and the hybrid where ideas live in the database until promoted
  (the middle of option C).

That is close to option B with the project half of option C, and it is a
narrower answer than any of the four as written — the four options below are
kept as the space the choice was made from, not as live alternatives.

Two consequences worth naming immediately. First, **the apply lane becomes
load-bearing** rather than a demo: it is now the only write path to governed
content, and it has been dispatched exactly once, ever (2026-08-15). Second,
**the origin complaint is answered by the coordination half, not the document
half** — "no good place to store my projects" is solved by projects, members and
the project-to-repository map living in a database that any tenant install has,
while the specs themselves still land in a repository. Which means openDox must
be able to CREATE that repository, or the complaint returns one level down.

## The problem in one paragraph

Everything the workbench does today is safe because git is the record. A gate
act is a commit. A ratification is a reviewable diff. A branch session is a
branch. A snapshot is derived from a checkout at a `(repository, ref)` key and
refuses when it cannot resolve one. Doc-health reads files. The whole
`workflow-gate-contract` and `document-lifecycle` estate rests on the fact that
the thing you are asserting authority over is a blob with a digest that someone
can review. Add a database with users and projects and documents, and you now
have a second store that can disagree with the first — and the interesting
disagreements are exactly the governed ones.

## The precedent that already ruled a piece of this

**D5, `dashboard-project-scoping`, ruled 2026-08-06 and promoted.** For
PROJECTS specifically, the answer already exists. The promoted requirement
"Local register authority is declared against the tenant catalog" says the
register consumed by the dashboard is authoritative for the DEVELOPMENT PLANE
ONLY until a tenant project catalog exists; once a runtime catalog is
authoritative for project-to-repository composition, the local register becomes
"a derived, replaceable workstation cache" and "SHALL NOT override the catalog".
The staged topic states why it was declared at all: "Declared here so the two
models cannot fork."

That is a direct hit on the ruling. openDox's database with projects in it IS
the runtime catalog D5 anticipated. So for projects, the ruling does not open a
question — it FIRES a trigger that was already set, and the consequence is
already written down: `project-register.yaml` becomes a derived cache, and the
`create-project` commission loop (descriptor → fulfilment lane → register edit)
becomes a legacy path for the development plane.

Two things follow that are not yet written down anywhere:

1. **D5 names the direction but not the mechanism.** "Derived projection of the
   catalog" does not say who derives it, how often, what happens to a
   development-plane edit made while the catalog is unreachable, or whether the
   aggregation's register file continues to exist at all.
2. **D5 covers projects only.** Documents, ideas, gate acts, sessions,
   abstracts and model bindings are all unaddressed, and they are not the same
   question — a project is navigation metadata, a ratification is an authority
   claim.

## Four candidate authority boundaries

### A. Database-authoritative, git as an export — **REJECTED 2026-09-04**

The app is the truth. Documents live in Postgres, are edited there, and are
pushed to git as a publication step. Users, projects, ideas, threads and
abstracts are ordinary rows.

Best for: the thing Brett asked for. A new project in a new repo with some specs
in it needs no checkout, no submodule, no register row.

Breaks: `governed-derived-model` and `workflow-gate-contract` both assume the
reviewable artifact. Doc-health reads a tree. Branch protection, codexFactory's
merge-gate floor, and every required check in the estate gate on git refs. A
ratification whose only home is a table is not something a merge gate can
enforce, and "external enforcement" is the bottom layer of the whole xFactory
model.

### B. Git-authoritative, database as a cache — **closest to the ruling**

Git stays the record for everything governed. The database holds users,
sessions, projects-as-navigation, abstracts, threads, model bindings, telemetry
— and a materialized projection of the corpus for query speed.

Best for: nothing in the governance estate changes. The snapshot registry
already IS this design, with a freshness key and honest refusal; a database
version is the same contract with a faster backend.

Breaks: the origin complaint. If git is authoritative for documents, then a
project still needs a repository, and "no good place to store my projects" is
answered with "make a repo first". It also makes openDox-without-openXdox a
strange product: an app whose documents must live in someone's git remote.

### C. Split by object class — the pragmatic middle; its PROJECT half is ruled in, its ideas-until-promoted half REJECTED

Governed content (documents that carry a lifecycle status, gate acts,
ratification records) is git-authoritative. App state (users, sessions,
projects, membership, settings, threads, abstracts, caches, telemetry) is
database-authoritative. A document that has never been published is
database-only until it is; publication is the act that makes git authoritative
for it.

Best for: it is probably right, and it matches D5's shape (a per-object-class
declaration rather than a global answer).

Breaks: the boundary runs through the middle of the document object, which is
the most-used object. "Draft in the DB, governed in git" means every read path
has two backends and every write path has to know which one it is in. And the
transition — the first publish — is a migration of authority mid-object-life,
which is the class of thing that produces the worst bugs.

### D. Event-sourced, git as the published log — not chosen

Every act is an append-only event. The database materializes current state; git
receives a serialization of the events that matter, as commits. The commit is
still the reviewable record; the database is still the queryable store; neither
is a cache of the other because both are projections of the log.

Best for: it dissolves the fork question rather than answering it, and gate acts
are already event-shaped (a `workflow-job` descriptor plus a gate-action record
is an event pair).

Breaks: it is the most machinery, and it invents a third store. Also the mapping
from events to a review-shaped diff is not obvious: a reviewer wants to see a
document, not a replay.

## What a gate means when the record is in Postgres

This is the part that has to be settled before any of the four is chosen,
because it is a constitutional question rather than a storage one.

- **A ratification is trusted for a reason, not for its location.**
  `record_binding.py` exists precisely to make that true, and
  `identity-brokering` already warns that a ratification record's actor needs
  standing. So in principle a Postgres-held ratification with a bound actor is
  no worse than a file-held one.
- **But external enforcement is the bottom layer.** The layer model ends in
  GitHub branch protection, the clinical chart, DNS, the ledger. A gate whose
  verdict cannot be read by a required check on a pull request is not enforced;
  it is advertised.
- **So the likely answer is a hybrid regardless of A–D:** the database may HOLD
  the act, but the act's enforceable form is a commit, and the two must be
  linked by a digest so that "which record did the gate read" is an auditable
  fact. That is exactly the discipline `neutral-product-pin` invented for
  pinned readers, applied to a record instead of a tool.

## Consequences nobody has costed

- **Doc-health.** It reads a tree. If governed content can exist only in a
  database, doc-health either grows a database backend or stops being complete.
  A check family that cannot see half the corpus is worse than no check.
- **The nightly lanes.** Three lanes exist to thaw the hosted dashboard's
  snapshot and `/source` corpus from git. With a database, most of that machine
  disappears — which is an argument FOR the database, and also an argument for
  not building any more of the refresh lane first. (Noting the measured state:
  the refresh lane has three runs, none successful, and has never produced its
  status artifact.)
- **Backup, migration and tenancy.** Git gives you disaster recovery for free
  and a per-tenant boundary for free. A per-tenant database gives you neither
  for free; the Hermes install pays for both with ordered SQL migrations and a
  lifecycle CLI, which is the precedent to copy rather than reinvent.
- **The 300-source NotebookLM cap.** The projection is per-repo today. Per
  project-in-a-database it is per project, which is better shaped — but the
  capacity guard is written against repos.
- **`ideation/cross-reference.yaml` and the possibles register.** Both are
  derived indexes maintained as files. In a database they are queries. That is a
  strict improvement and a real migration.

## What the ruling leaves, and one contradiction kept

Settled: the authority boundary, and with it most of Q1's risk — an unstated
split was the worst outcome and there is now a stated one.

Left open by it, and worth naming so nobody assumes otherwise:

- **The draft-to-governed transition.** "Unsaved drafts" live in the database
  and governed documents live in git, so the first save of a new document is
  still a migration of authority mid-object-life. The ruling names both ends and
  not the crossing.
- **The apply lane is the only write path and is nearly unexercised.** One
  dispatch, ever. Under the ruling it carries every governed write from every
  tenant instance. That is a large promotion for a path with no operating
  history, and it makes the lane's own hardening a precondition rather than a
  follow-up.
- **What "read from repositories" costs per tenant.** Each instance now needs
  read access to the repositories its projects map to, which is the content
  App's scope question from `openxdox-install-app-provisioning` arriving in a
  new form.
- **Ideas.** They were the hybrid's subject and the hybrid is rejected, so an
  idea is a governed document in git from the moment it is saved. That is
  consistent and it makes the brainstorm stage heavier than a lab assistant may
  want — a student jotting a half-thought now writes a file through an apply
  lane. Whether openDox needs a pre-governed scratch space that is NOT a "draft
  of a document" is a real residual.

Contradiction kept: this reading and the origin complaint still pull against
each other. The ruling keeps documents in git, and Brett's complaint was that
there is nowhere to put a project's specs. Both are satisfied only if openDox
can create and populate a repository for a new project as a first-class act —
otherwise "no good place to store my projects" is answered with "make a repo
first", which is the complaint restated.
