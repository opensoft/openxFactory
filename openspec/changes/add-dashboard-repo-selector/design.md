# Design: Repository Selector + (repository, ref) Snapshot Source + Refresh

## Context

Two decisions made a week apart turn out to need the same seam, and Brett
decided to build them together rather than in sequence.

The first is the REPOSITORY SELECTOR, decided 2026-07-25 with three
companions: the runtime plane (a neutral install-shipped ideation surface)
is the real end state, the dev plane and the runtime plane are SEPARATE
SYSTEMS with no data path between them, per-repository snapshots plus a
thin index is the mechanism, and sparse wheels are honest — a repository
renders whatever stations it has data for. A same-day drive of the
unmodified v1 generator against MedxFactory, AdxFactory, and LedgerxFactory
proved the generator, the schema, and the rendering are already neutral;
what is missing is the selector, the per-repository snapshots, and the
index.

The second is SNAPSHOT/IMAGE DECOUPLING, decided 2026-07-25 (Brett,
relayed via team003, endorsing team003's option 2 over bolting a
bake-trigger onto the pod). Its motivating incident: a staging fragment
landed on openxFactory main minutes after that day's rebake and stayed
invisible on the hosted dashboard until the nightly ran and the image was
rebuilt. Bake the APP, not the SNAPSHOT.

The third input is Brett's 2026-07-26 keying decision: the snapshot source
is addressed by the PAIR (repository, ref), `ref` defaulting to `main`.
The hosted plane will exercise only `(repo, main)`. The reason to carry
`ref` anyway is that two named consumers already need it — the branch
sessions of the `workbench-branch-sessions` staged topic (whose session
panels read a snapshot generated from a git WORKTREE) and the runtime
plane (which binds its own source behind the same seam) — and this is the
one interface every renderer, the index, and both refresh bindings pass
through. Re-cutting it later is the expensive path.

Three facts about the existing code set the shape:

1. **The generator is already per-repository.** It takes `--repository`
   and `--project-register`, resolves the repository through the register
   into `project`/`project_group` snapshot fields, and emitted three
   domain snapshots in the drive with zero code changes. The nightly lane
   calls it once; iterating the register is a loop, not a redesign.
2. **The bundle has a grep-proven no-external-network boundary.**
   `tests/ideation-dashboard/test_renderer.py` bans `https?://`,
   `XMLHttpRequest`, `WebSocket`, `EventSource`, and
   `navigator.sendBeacon` across every bundle file, and pins each `fetch(`
   to a small set of same-origin backend routes with per-file call counts.
   That invariant is load-bearing (the dashboard projects internal
   governance state) and this change must not be the one that edits it.
3. **`serve.py` has a relative-import quirk.** POST routes 500 unless the
   server is reached through module invocation
   (`python3 -m ideation_dashboard.serve` / `.cli`). This change adds a
   POST route and a fetch path; carrying a workaround into new surfaces is
   how a workaround becomes a contract.

## Goals / Non-Goals

**Goals**: make every registered repository selectable without asking any
repository to adopt a convention; make the hosted dashboard's data
refreshable without an image rebake; make freshness legible at a glance;
give the serving layer ONE snapshot-source seam keyed (repository, ref)
that the selector, both refresh bindings, the future branch sessions, and
the eventual runtime plane all bind to; keep the pod's authority exactly
where it is (read derived data, execute nothing).

**Non-Goals**: the runtime plane itself (exit 2 of the staged topic); the
one-neutral-versus-per-domain-overrides fork; any pod-side build, rollout,
or rebake authority; branch/session snapshot GENERATION and the workbench
branch sessions that will consume this seam; the aggregate `xFactory`
view's rendering shape beyond "compose from the index, never scan"; new
funnel data of any kind.

## Decisions

### D1 — Bake the app, fetch the data; the pod never gains build authority
**Decision**: the container image carries the APPLICATION (renderer,
assets, server) and the DATA is fetched at runtime from a declared
external source. The baked snapshot stays as a fallback (D6). No affordance
anywhere in the running dashboard can trigger an image build or a rollout.

**Rationale**: the motivating incident is not "the nightly was late", it is
"data freshness was coupled to a build". Decoupling them is the only fix
that scales past one repository, because with N repositories a rebake per
data change is N times more absurd. The alternative team003 explicitly
rejected — a bake trigger on the pod — collides with a constitutional
rule, not a preference: serving surfaces carry
`execute_final_action: false`; they dispatch recorded requests and never
execute. A recorded-dispatch "commission a rebake" verb is a coherent
future thing and a SEPARATE change at its own gate.

**Consequence**: image rebuilds become APP-change events only, which also
makes the deployment story honest — a rebake means the app changed.

### D2 — The data source is the aggregation repo's published raw files
**Decision**: the declared data source is the aggregation repo's
`health/ideation-dashboard/` tree — the per-repository snapshots and the
index as raw files at a pinned path. Recommended, pending ratification
(open question 1).

**Rationale**: three candidates were named. Raw repo files win on
provenance and on inventing nothing: the nightly ALREADY writes exactly
there, so there is no new publication path to build, and the fetched
file's commit SHA IS the `source_revision` the snapshot already carries —
provenance is a git question, answerable after the fact, by anyone. A blob
container's advantage is real (no repository read credential in the pod)
and a ConfigMap's is real (no egress at all), but each buys that by
turning provenance into a pipeline promise rather than a revision.

**Consequence, recorded plainly**: the aggregation repo is private, so
raw-file fetching means a READ-ONLY, narrowly-scoped credential in the
serving side — the single strongest argument for blob, and the reason
ratification is Brett's rather than assumed. The seam (D4/D5) is
source-agnostic either way: the source is configuration, so a ratification
that goes to blob changes a fetcher and no contract.

### D3 — The index gets its OWN schema; the snapshot schema is untouched
**Decision**: the snapshot INDEX is a new schema-versioned contract
(`ideation-dashboard-snapshot-index`) with its own packaged examples. The
`ideation-dashboard-snapshot` schema grows nothing.

**Rationale**: the index describes a SET of snapshots; a snapshot
describes ONE repository's corpus at one revision. Folding the index into
the snapshot would make every snapshot carry facts about its siblings —
which breaks the determinism property the snapshot schema is built around
(the same tree must yield a byte-identical snapshot; sibling facts change
without the tree changing). A separate artifact also means the index can
be fetched cheaply and often while the snapshots stay large and stable,
which is exactly the traffic shape a refresh wants.

**Consequence**: the new schema registers in
`scripts/validate-ideation-dashboard-contracts.py`'s `SCHEMA_FILENAMES`
and `KIND_TO_SCHEMA`, and its examples land under
`examples/ideation-dashboard/` where the validator's example sweep finds
them automatically. A validator-side rule the shape cannot express: every
index entry's (repository, ref) pair is unique.

### D4 — The source is keyed (repository, ref), with `ref` defaulting to main
**Decision**: every snapshot request, index entry, and registry key names
BOTH a repository and a ref. A caller that names no ref gets `main`.

**Rationale**: Brett's 2026-07-26 decision, and the cheap-now/expensive-
later argument is the whole of it. Two consumers already need the second
key (branch sessions; the runtime plane), and it touches the one interface
everything passes through. Defaulting to `main` is what keeps it additive:
every existing snapshot and every existing caller is a `main` caller
already, so nothing needs rewriting and no `schema_version` bumps.

**Consequence**: the serve keeps ONE registry keyed by the pair — the
single piece of new server plumbing this change adds, and the piece
`add-workbench-branch-sessions` will consume rather than duplicate.

### D5 — The serving side fetches; the browser stays same-origin
**Decision**: the runtime fetch of the index and snapshots happens on the
SERVING side (into a same-origin snapshot directory the registry serves).
The browser bundle continues to talk only to its own origin, through the
same-origin routes it already uses.

**Rationale**: the bundle's no-external-URL boundary is grep-proven by
`test_renderer.py` (`https?://` and every network primitive banned across
every file; each `fetch(` pinned to a same-origin route with a per-file
count). Fetching a data source from the browser would require editing that
pin, and it would also put the data-source credential (D2's consequence)
in a place the browser can see. Keeping the fetch server-side preserves an
invariant that was deliberately made mechanical, and it keeps the
credential where credentials belong.

**Consequence**: the "hosted refresh" affordance is a same-origin call
that asks the serving side to re-pull and then re-reads the registry —
still strictly read-only in governance terms (it fetches derived data and
writes only the derived cache), and still no new authority. Realization
detail left open: whether the pull runs in the serving process, an init
container plus a periodic sidecar, or both. All three satisfy the
requirement; the requirement names the behaviour, not the topology.

### D6 — The baked snapshot is demoted to a LOUD fallback
**Decision**: the image keeps a baked snapshot for first boot and for an
unreachable data source. When it is what renders, the page shows a stale
banner naming its generated-at.

**Rationale**: a fallback is what keeps an unreachable data source from
turning into a blank dashboard, and today's baked-snapshot behaviour is
already the fallback's behaviour — so the fallback path is proven before
this change ships. The banner is the non-negotiable half: the failure this
change exists to end is not "old data", it is "old data that looked
current". Silence is the bug.

### D7 — One refresh affordance, two plane bindings
**Decision**: the same UI affordance binds differently per plane. Served:
re-pull the index plus the active snapshot and re-render. Local: POST a
regenerate that re-runs the generator against the served checkout, then
re-render.

**Rationale**: it mirrors the local/served seam the dashboard already has
everywhere else, and each binding is honest about its own plane's
authority. The served binding is a READ — fetching fresher derived data
grants nothing. The local binding WRITES, but only the derived snapshot
artifact, from a checkout the human already controls, on a loopback bind.
Neither can publish, build, or roll out anything (D1).

**Consequence**: whether the local regenerate is GATED is open question 3.
Recommendation: ungated, on the `open-workbench` precedent — the snapshot
is derived data and regeneration mutates nothing governed. The caveat that
makes it a question rather than an assumption: it would be the first POST
route that is not a gate verb, so the posture must be stated in the
requirement rather than inherited.

### D8 — Off-cycle publication is `workflow_dispatch`, never the pod
**Decision**: the nightly snapshot job gains manual dispatch. That is the
ONLY off-cycle path to fresher published data.

**Rationale**: publication writes to a governed repository, so it belongs
to CI where it is attributable and reviewable, and it is already there —
this is a trigger, not a new lane. Combined with D1 it closes the loop the
acceptance sketch describes: dispatch the job, click refresh, see the
document, with no rebake and no pod-side write authority anywhere in the
sequence.

### D9 — The project register is the selector's roster
**Decision**: the selector offers what the project register declares, and
the dashboard keeps no second repository list. A repository present in the
index but absent from the register is still selectable and renders
ungrouped.

**Rationale**: the register is the existing neutral contract for exactly
this ("repository -> project -> project-group navigation", instance owned
by the aggregation layer), the promoted grouping requirement already says
renderers read grouping from the SNAPSHOT rather than the register, and
that requirement already rules that an unregistered repository renders
ungrouped without failing the dashboard. A second list would be a second
truth about which repositories exist.

**Consequence**: adding a repository to the dashboard is an aggregation-repo
register edit plus a nightly run — no code change and no image change.

### D10 — Sparse is rendered, never refused
**Decision**: a repository renders whatever funnel stations its snapshot
populates. An install repo with only `openspec/changes/` shows active and
archived and nothing else.

**Rationale**: Brett's 2026-07-25 decision, and the drive's second finding
is the evidence for why it matters: the funnel's MIDDLE (clusters,
possibles, staged) feeds from cross-reference and staging conventions that
today exist only in openxFactory, so every other repository is sparse in
the middle right now. Refusing sparse repositories would make convention
adoption a precondition of visibility, which inverts the incentive — a
domain should be able to SEE its corpus before it decides to adopt
anything.

### D11 — Freshness display is contract, not decoration
**Decision**: the header carries `repo @ ref · source_revision short SHA ·
generated-at` on every plane.

**Rationale**: the user question behind the whole refresh ask was "did my
doc make it in?", and that question is answerable only against a stated
revision and stamp. Putting it in the requirement rather than leaving it
to the UI is deliberate: a dashboard that renders a projection has an
obligation to say WHICH projection, and the fallback banner (D6) is a
special case of the same obligation.

### D12 — The relative-import fix rides this change
**Decision**: fix `serve.py`'s relative-import quirk here rather than
adding a second and third surface that depend on the module-invocation
workaround.

**Rationale**: the workaround is already load-bearing for the existing POST
routes and is documented in the live serve command. This change adds a POST
route and a serving-side fetch path; the moment those depend on it too, the
workaround stops being a backlog item and becomes an interface. Fixing it
in the change that would otherwise entrench it is the cheapest moment.

## Risks / Trade-offs

- **A credential in the serving side (D2's consequence).** Raw-file
  fetching from a private aggregation repo needs a read-only token in the
  pod, where today there is none. Mitigation: the scope is one repository
  path and read-only; the seam is source-agnostic (D5), so a ratification
  that picks blob or ConfigMap removes the credential without touching a
  contract; and the credential never reaches the browser (D5).
- **Fresh data can now disagree with a running app.** Once data refreshes
  independently of the image, a snapshot can carry fields the baked
  renderer does not know. Mitigation: the snapshot schema's additive
  posture is explicit that consumers MUST ignore unknown properties, which
  is exactly this case; and the freshness header makes the pairing
  visible. Residual risk: a snapshot that REMOVES a field a running app
  reads would break the page — which is why breaking snapshot changes need
  a `schema_version` bump and a coordinated rollout, as they already do.
- **A refresh button invites a rebake button.** The affordance sits next to
  the exact frustration ("my doc is not here") whose other cause is a stale
  APP. Mitigation: D1 states the constitutional boundary in the change
  itself and the requirement forbids the path, so the ask arrives as a
  proposal for a recorded-dispatch verb at its own gate rather than as a
  quiet feature.
- **`ref` is carried before anything exercises it.** Unused generality is
  usually a smell. Mitigation: two named consumers exist (branch sessions,
  runtime plane), the hosted plane's restriction to `main` is a REQUIREMENT
  rather than an accident, and a ref-defaults-to-main scenario pins the
  behaviour so the unexercised path cannot silently rot.
- **Selecting a sparse repository looks broken.** A wheel with three empty
  stations reads as a bug to someone who has only seen openxFactory.
  Mitigation: D10 is deliberate and the empty-state rendering must SAY
  what it is (no data for this station in this repository), not merely be
  blank — the same honesty rule as the stale banner.
- **More snapshots, more index churn.** N repositories mean N snapshot
  files rewritten nightly in the aggregation repo, and the index changes
  whenever any of them does. Mitigation: per-repository files keep each
  fetch small (which is why the split is right for refresh as well as for
  the selector), and the index is thin by construction (D3).

## Open Questions

1. **Data-source ratification.** Aggregation-repo raw files
   (recommended — nothing new is invented, commit SHA = provenance, at the
   cost of a read-only credential in the serving side), a blob container
   (no repository credential; provenance becomes a pipeline promise), or a
   ConfigMap the pipeline updates (no egress; couples data refresh to a
   cluster write). **Recommendation: raw files**, with the credential
   consequence recorded above. Brett decides.
2. **Index polling cadence.** Fetch the index on load and on explicit
   refresh only, or poll it on an interval so the page can advertise that
   newer data EXISTS (a "newer snapshot available" hint). Polling makes
   freshness proactive and makes the serving side chatty against the data
   source. **Recommendation: explicit-refresh-only in v1**, because the
   freshness header already answers the question that motivated the ask
   and a hint can be added additively. Brett decides.
3. **Whether the local regenerate is gated.** Gate verb (recorded
   dispatch, human-only, actor-resolved) or ungated action like
   `open-workbench`. **Recommendation: ungated** — the snapshot is derived
   data, regeneration mutates nothing governed, and a gate record per
   regeneration would be audit noise about a cache. The caveat: it is the
   first non-gate POST route, so the requirement states the posture
   (loopback-only, derived-artifact-only, no governed mutation) explicitly
   rather than inheriting it. Brett decides.
