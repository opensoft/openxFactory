# Staged: Dashboard Repo Selector — per-repo wheels, two planes, one neutral core

Status: staged
Kind: architecture
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
Topics: ideation-dashboard, workflow-visualization, project-register, lifecycle-projection, domain-neutralization, doc-workflow
Repository context: openxFactory owns the `ideation-dashboard` capability
delta (selector + snapshot-index requirements) and the index contract;
codexFactory realizes lane iteration, multi-snapshot serving, and the
selector UI; the aggregation repo owns the project-register instance; the
runtime plane later routes to the install repos as a neutral capability.
Staging ID: openxFactory:staging:dashboard-repo-selector
Source: ideation/brainstorm/ideation-dashboard.md — the v2 concept sketch
(repo-aware entry, backend seam, per-repo snapshots default) plus
§"Domain drive + the runtime plane (2026-07-25)" (Decided 2026-07-25 by
Brett; drive findings recorded the same day)
Target capabilities: ideation-dashboard (MODIFIED); a later ADDED runtime
capability (name open — the neutral install-shipped ideation surface),
registered as a domain-neutralization candidate at its own gate

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

## Exit path

Exit 1 (this gate, dev plane): a change pair — openxFactory
`add-dashboard-repo-selector` (MODIFIED `ideation-dashboard`: selector,
per-repo snapshot + index requirements; the index contract) realized by a
codexFactory delta (nightly-lane iteration over the register,
multi-snapshot + multi-root serving, selector UI), sequenced against open
question 5. Exit 2 (separate, later): the runtime-plane neutralization
change — the ADDED install-shipped capability with the governed-content
adapter seam — registered as a domain-neutralization candidate when
scoped; open question 3 is its gating design decision.
