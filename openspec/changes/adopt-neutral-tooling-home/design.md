# Design: adopt-neutral-tooling-home

Grounded in the 2026-08-03 codexFactory neutrality sweep (full evidence in
`supporting-docs/codexfactory-neutrality-sweep.md`): ~73k LOC of
neutral-or-neutral-in-purpose source hosted in the engineering domain
repo, against a domain-legitimate core more than an order of magnitude
smaller.

## D1. History handling — copy with provenance, never graft

The moved trees are plain-copied at a pinned codexFactory commit, each
tranche's commit message carrying `Provenance: adopted from codexFactory
<branch>@<sha>` (the established pattern from
`contracts/avatar-client-lab/avatar-state-derivation-table.md`). git
filter-repo grafting is explicitly rejected: openxFactory is slated for
open-sourcing, and codexFactory's private commit history (messages,
author trails, incident references) must not ride into a public repo.
The private history remains intact and citable in codexFactory.

## D2. Tranche order — doc-health spine first, dashboard second

Tranche A moves `scripts/doc_health/` (which physically contains the
routing/organizer/readiness-scorer/possibles lanes) plus
`scripts/doc-health.py`, `scripts/sync-notebooklm-books.py` (doc-health
family 12 shells out to it, so it rides the same tranche), their test
suites, prompt contracts, and `doc-health-reusable.yml`. Tranche B moves
the ideation dashboard runtime (`scripts/ideation_dashboard/`, `web/`,
the three nightly entrypoints, the session runbook, tests). Tranche C is
the codexFactory shedding change; Tranche D repoints the aggregation
repo. A and B land in openxFactory with green suites BEFORE C deletes
anything — the workspace never has zero homes for a tool.

## D3. CloudPC readiness evaluators go to the aggregation repo

`readiness.py` + `readiness_dispatch.py` evaluate self-hosted-runner
readiness. That is CI-host infrastructure: it moves to the aggregation
repo (which hosts the runners and the nightly), not openxFactory.

## D4. The one engineering default stays a config default

`kickoff.py`'s `DEFAULT_WORKFLOW = "speckit-realization"` is retained as
the documented default with its existing comment (domain workflows pass
their own id). Neutralizing the default's VALUE is not this change's
business; the mechanism is already neutral.

## D5. The routing ownership amendment lands pre-promotion

`add-cross-factory-ideation-routing` is active and unpromoted; its
ownership requirement is edited in place under this change's ratification
(recorded in both changes' task ledgers) rather than via a MODIFIED delta
against canon that does not yet exist.

## D6. Only the doc-health reusable workflow moves

`review-lane-reusable.yml`, `council-lane-reusable.yml`, and
`execution-lane-reusable.yml` stay in codexFactory: their decision cores
(merge_master, review lane PR half, execution lane) are engineering-owned
and stay. The credential tax on the remaining callers is accepted until
those lanes' own ownership is revisited.

## D7. Relationship to staged dashboard-repo-selector exit 2

This change relocates the dashboard IMPLEMENTATION so the neutral repo
owns it; the staged exit 2 (install-shipped neutral runtime plane,
DTN path) remains future work and is neither realized nor blocked here.
The relocation makes that future change a same-repo evolution instead of
a cross-repo extraction.

## D8. Sonar / open-sourcing consequence (recorded intent)

After this change: openxFactory (public candidate) carries the large
neutral tooling LOC under public analysis; codexFactory (private) shrinks
to engineering lanes, Hermes/Omnigent content, credentials families, and
its schemas/workflows — the intended Sonar split (Brett, 2026-08-03).
