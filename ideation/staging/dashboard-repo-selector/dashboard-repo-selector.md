# Staged: Dashboard Repo Selector — per-repo wheels, two planes, one neutral core

Status: staged
Kind: architecture
Exit taken: openspec/changes/archive/2026-08-01-add-dashboard-repo-selector — exit 1 (dev plane), ratified 2026-07-29 and archived 2026-08-01. Exit 2 (the runtime plane) is NOT taken and is recorded below.
Summary: Give the ideation dashboard a repository selector over the
workspace's registered repos (per-repo snapshots + a thin index; selecting
`xFactory` composes the all-submodules dev view), as the dev-plane step
toward the decided end state: the dashboard as a NEUTRAL xFactory
capability every DomainxFactory install ships, serving its tenant's domain
ideas (e.g. a running MedxFactory's patient-management funnel) from
governed install content. The two planes are separate systems — the dev
dashboard never reaches a running install's content. A live drive of the
unmodified v1 dashboard against Medx/Adx/Ledgerx (2026-07-25) evidenced
the neutral-core boundary: scan/schema/rendering are already
repo-agnostic; the funnel's middle conventions, pinned-validator
discovery, and station/verb vocabulary are the override pressure points.
The same seam carries the snapshot/image decoupling decided 2026-07-25:
the container bakes the APP and fetches its DATA at runtime, so a
document that lands on main is reachable by a refresh instead of a
rebake. The snapshot source is keyed **(repository, ref)** from day one
(DECIDED 2026-07-26) — the hosted plane exercises only `(repo, main)`,
while the ref key is what later lets branch-session views (sibling topic
`ideation/staging/workbench-branch-sessions/`) and the runtime plane bind
without redesigning the seam.
Topics: ideation-dashboard, workflow-visualization, project-register, lifecycle-projection, domain-neutralization, doc-workflow, snapshot-source, deployment-topology
Repository context: openxFactory owns the `ideation-dashboard` capability
delta (selector + snapshot-source + snapshot-index requirements) and the
index contract; codexFactory realizes lane iteration, the (repository,
ref) snapshot registry, multi-snapshot serving, the selector UI, and the
two refresh bindings; the aggregation repo owns the project-register
instance, the published snapshot data source, and the dispatchable
nightly job; the runtime plane later routes to the install repos as a
neutral capability.
Staging ID: openxFactory:staging:dashboard-repo-selector
Source: ideation/brainstorm/ideation-dashboard.md — the v2 concept sketch
(repo-aware entry, backend seam, per-repo snapshots default) plus
§"Domain drive + the runtime plane (2026-07-25)" (Decided 2026-07-25 by
Brett; drive findings recorded the same day); the snapshot/image
decoupling mission (Brett 2026-07-25, relayed via team003 with its
motivating incident) and Brett's (repository, ref) keying decision
(2026-07-26, live session) fold in as claims 6-12
Target capabilities: ideation-dashboard (MODIFIED); a new ADDED
snapshot-index contract (its own schema, additive — never grown into the
snapshot schema); a later ADDED runtime capability (name open — the
neutral install-shipped ideation surface), registered as a
domain-neutralization candidate at its own gate

## Claims

1. **Two planes, separate systems (DECIDED 2026-07-25).** The dev-plane
   dashboard reads git checkouts; with the selector on `xFactory` it shows
   the dev-time code-and-ideas corpus of ALL submodule repos. It has no
   data path to what a running install holds; a codexFactory dev dashboard
   never sees the installed MedxFactory's patient ideas.
2. **The runtime plane is the end state (DECIDED 2026-07-25).** The
   dashboard becomes a neutral capability every DomainxFactory install
   ships, its wheel fed from governed install content. Structurally the
   snapshot generator's data source is an adapter seam: filesystem-corpus
   adapter (dev) vs governed-content adapter (runtime); the neutral
   snapshot schema is what makes the seam possible.
3. **Per-repo snapshots + a thin index (DECIDED 2026-07-25).** The lane
   generates one snapshot per registered repository; the selector switches
   snapshots; the aggregate view composes from the index. The
   project-register (existing neutral schema, aggregation-owned instance)
   is the selector roster — no second repo list.
4. **Sparse wheels are honest (DECIDED 2026-07-25).** A repo renders
   whatever stations it has data for; installs with only
   `openspec/changes/` show active/archived and nothing else. Convention
   adoption is never a precondition of being selectable.
5. **The neutral core is proven; the override points are named
   (drive-evidenced 2026-07-25).** The unmodified v1 generator snapshot
   Medx (31 docs/1 change), Adx (7/1), Ledgerx (9/3) with zero code
   changes. What showed domain-shape pressure: (a) clusters/possibles/
   staged feed from cross-reference + staging conventions that exist only
   in openxFactory; (b) pinned-validator discovery assumes the
   codexFactory checkout layout; (c) whether the six stations and the
   action verbs are neutral or codex-specific. These — not scan, schema,
   or rendering — are where per-domain overrides (digest-pinned, omnigent
   overlay pattern) would attach, if the override fork is taken.
6. **Bake the APP, not the SNAPSHOT (DECIDED 2026-07-25, Brett via
   team003).** The hosted pod fetches per-repo snapshots AND the thin
   index at runtime from an external data source instead of carrying them
   in the image, so refreshing the data is no longer an image rebake. The
   motivating incident is the whole argument: on 2026-07-25 ~20:30 UTC a
   new staging fragment landed on openxFactory main (`ab2acad`) MINUTES
   after that day's rebake, and was invisible on
   ideation-dashboard.xforge.us until the nightly plus the next rebake —
   and invisible on Brett's local serve until a manual regenerate. Three
   data-source candidates were named: the aggregation repo's
   `health/ideation-dashboard/` raw files, a blob container, or a
   ConfigMap the pipeline updates. **Recommendation: the aggregation-repo
   raw files** — the nightly already writes exactly there, so no new
   publication path is invented, and provenance is trivially auditable
   because the fetched file's commit SHA IS the `source_revision` the
   snapshot already carries. Blob storage's advantage (no repo-read token
   in the pod) and the ConfigMap's (no egress) are real but buy less than
   an auditable revision; ratification is open question 7.
7. **The baked snapshot is DEMOTED, not deleted (DECIDED 2026-07-25).**
   The image keeps a baked snapshot as a first-boot and offline fallback
   only. When the fallback is what renders, the page says so — a stale
   banner carrying the fallback's `generated-at` — and it MUST NEVER
   degrade silently: a dashboard quietly serving last week's governance
   state is the failure mode this whole fold-in exists to end.
8. **One refresh affordance, two plane bindings (DECIDED 2026-07-25).**
   Hosted: refresh = re-fetch the index plus the ACTIVE snapshot and
   re-render — strictly read-only, no new authority, because fetching
   fresh derived data is a read. Local serve: regenerate = a POST action
   route that re-runs the generator against the checkout root and
   reloads. Same gesture in the UI, two bindings — which mirrors the
   local/served seam the dashboard already has.
9. **Off-cycle publication is a governed CI action, NEVER the pod
   (DECIDED 2026-07-25; constitutional).** The nightly snapshot job gains
   `workflow_dispatch` so a human or a session can refresh the published
   data off-cycle. The pod gains NO build or rollout authority:
   `execute_final_action: false` is constitutional for serving surfaces,
   which dispatch recorded requests and never execute. A button on the
   running dashboard that triggers a bake is out of scope BY DESIGN; if a
   recorded-dispatch "commission a rebake" verb is ever wanted it is a
   separate change at its own gate, not smuggled in here.
10. **The snapshot source is keyed (repository, ref) (DECIDED 2026-07-26,
    Brett).** Every snapshot request names a repository AND a ref, with
    `ref` DEFAULTING to `main`, and the serving layer keeps a registry
    keyed by that pair. The hosted plane exercises only `(repo, main)` —
    nothing else is published — but the seam carries `ref` from day one so
    that branch-session views (the sibling `workbench-branch-sessions`
    topic, where a session's panels read a snapshot generated from a
    worktree) and the future runtime plane bind to it WITHOUT a redesign.
    Adding the second key later would mean re-cutting the one interface
    every renderer, the index, and both refresh bindings go through.
11. **Freshness is displayed, never inferred (DECIDED 2026-07-26).** The
    header carries `repo @ ref · source_revision short SHA ·
    generated-at`. This is the actual user question behind the refresh
    ask — "did my doc make it in?" — and it must be answerable at a
    glance rather than by reasoning about deployment times.
12. **Branch snapshots are session-local derived data and are NEVER
    published (DECIDED 2026-07-26).** A snapshot generated for a ref other
    than `main` exists for the session that asked for it; it is never
    committed to the published data source, never enters the index the
    hosted plane fetches, and never becomes a shared view. Main stays the
    shared truth on every surface.

## Idea notes (pre-document, non-documented)

None recorded at staging.

## Conflicts

No conflicts recorded.

## Open questions

1. **Aggregate rendering**: `xFactory` selection = one merged funnel with
   repo badges, drill-in per repo from a roll-up, or counts-only overview.
2. **One neutral vs neutral core + domain overrides**: a single neutral
   dashboard in openxFactory that handles all domains as-is, or per-domain
   digest-pinned overrides (stations, verbs, station sources). Deliberately
   held open until the domain drive produces vocabulary evidence.
3. **Runtime content kind**: what an "idea" IS as governed install content
   (a document-lifecycle doc kind? a new content family alongside
   `review_council`/`deliberation_mix`?) and how the six funnel stations
   map to the lifecycle in a running stack. The heart of the later
   neutralization change.
4. **Index contract home**: a new `ideation-dashboard-index` schema vs an
   extension of the project-register family.
5. **Sequencing**: the parent `add-ideation-dashboard` change is still
   active (awaits realization evidence to archive); codexFactory's
   dashboard surfaces are mid-flight on team004's wheel branch (PR #41).
   The selector change must state its relation to both before proposing.
6. **Where "local" is**: the drive surfaced that a dev-container workflow
   breaks the local/served seam's assumption that local = where the
   browser is (loopback in a container is unreachable from the host
   browser; non-loopback binds correctly drop write actions). The backend
   seam should name the forwarded-port topology explicitly.
7. **Data-source ratification** (claim 6) — **CLOSED 2026-07-26, recorded
   here 2026-08-28.** Brett ruled aggregation-repo raw files, read with a
   deploy-time read-only token; the recommendation was taken. The ruling
   is cited in the archived exit-1 packet's `Ratified:` line
   (`openspec/changes/archive/2026-08-01-add-dashboard-repo-selector`).
8. **Index polling cadence** — **CLOSED 2026-07-26, recorded here
   2026-08-28.** Brett ruled passive polling on roughly a five-minute
   interval with a newer-data badge and NEVER an auto-reload, which is
   neither of the two readings offered above: it takes the proactive
   freshness without taking the reload. Cited in the same `Ratified:`
   line.
9. **Whether the local regenerate action is gated or ungated** — **CLOSED
   2026-07-26, recorded here 2026-08-28.** Brett ruled it ungated,
   loopback-only and derived-artifact-only; the recommendation was taken,
   and its caveat — the first POST route that is not a gate verb — was
   stated rather than assumed. Cited in the same `Ratified:` line.

Questions 1–6 were also resolved into the exit-1 packet's twelve locked
decisions; they are left as written above because the packet, not this
fragment, is their record. Recording 7–9 here is the correction of a
narrower defect: these three were carried as OPEN in this document for a
month after the ruling that closed them, so a reader of the topic saw
three live forks where none remained.

## Exit path

Exit 1 (this gate, dev plane): a change pair — openxFactory
`add-dashboard-repo-selector` (MODIFIED `ideation-dashboard`: the
selector, the (repository, ref) snapshot-source seam, the runtime fetch
with baked fallback and its stale banner, the freshness header, both
refresh bindings, and the dispatchable publication lane; plus the ADDED
snapshot-index contract as its own additive schema) realized by a
codexFactory delta (nightly-lane iteration over the register, a
snapshot registry keyed (repository, ref), multi-snapshot + multi-root
serving, selector UI, the two refresh affordances, and the `serve.py`
relative-import fix the POST routes need) and an aggregation-repo delta
(the project-register instance, the published data source, and
`workflow_dispatch` on the nightly job), sequenced against open question
5. Exit 2 (separate, later) — **NOT TAKEN; deferred with its gate named,
2026-08-28**: the runtime-plane neutralization change — the ADDED
install-shipped capability with the governed-content adapter seam —
registered as a domain-neutralization candidate when scoped. **GATE:
open question 3, what an "idea" IS as governed install content** (a
document-lifecycle doc kind, or a new content family alongside
`review_council`/`deliberation_mix`) and how the six funnel stations map
to the lifecycle in a running stack. Nothing schedules that decision
today and no consumer is blocked on it, which is what makes this a
deferral rather than a queue position. The deferral records the gate; it
does NOT stop this topic being counted as work — there is no `deferred`
status for a staged topic and this record deliberately invents none.

Related staged work: the sibling topic
[workbench-branch-sessions](../workbench-branch-sessions/workbench-branch-sessions.md)
CONSUMES the (repository, ref) seam this topic defines — its session
snapshots are generated from a git worktree and read through the same
registry — so `add-dashboard-repo-selector` strictly precedes
`add-workbench-branch-sessions`. Both stack on the unpromoted
`ideation-dashboard` capability alongside `add-staging-workbench`,
`add-lens-gate-verbs`, and `add-workbench-bullseye-and-create`.
