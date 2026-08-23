---
code_surface: openxFactory (receives scripts/doc_health/ incl. routing/organizer/possibles lanes, scripts/doc-health.py, scripts/sync-notebooklm-books.py, scripts/ideation_dashboard/ + web/ + nightly entrypoints, their test suites, and .github/workflows/doc-health-reusable.yml), codexFactory (sheds the moved trees; README/stack.yaml redirect), xFactory aggregation (nightly caller repointed; CloudPC readiness evaluators adopted)
target_release: none
Status: ratified
Ratified: Brett's approval of `adopt-neutral-tooling-home` on 2026-08-03, with design D1-D8 carried as decided (copy-with-provenance, tranche order, readiness split to aggregation, pre-promotion routing amendment)
---

# Proposal: adopt-neutral-tooling-home

## Why

Three ratified capabilities deliberately split contract from
implementation with the implementation half assigned to codexFactory: the
doc-health checker suite (13.5k LOC + 11.9k test LOC), the ideation
dashboard runtime (32.7k LOC py+web + 32.4k test LOC), and the
cross-factory ideation routing/organizer/possibles lanes (5.6k LOC inside
the doc_health package). That split has aged badly on four measurable
axes:

1. **Layering inversions.** Neutral artifacts now cite domain-repo file
   paths (`xfactory-document-catalog-snapshot.schema.yaml` and
   `validate-document-catalog.py` name `scripts/doc_health/*.py`;
   `ideation/cross-reference.yaml` is producible only by a codexFactory
   script; `examples/lifecycle-notebook-workspaces.yaml` declares a
   domain script as `managed_by`). A capability literally named
   *cross-factory* routing runs from inside one factory.
2. **A standing credential tax.** codexFactory is a private sibling, so
   every neutral consumer pays for the dependency: the aggregation repo's
   workflows must mint a GitHub App token just to READ the reusable
   doc-health workflow and decision cores.
3. **Unclaimed mass.** None of this tooling appears in codexFactory's own
   `stack.yaml` declared-artifact inventory — the domain repo hosts it
   but does not claim it. The neutral tooling outweighs codexFactory's
   actual engineering content by more than an order of magnitude in LOC.
4. **The open-sourcing plan (Brett, 2026-08-03).** openxFactory is slated
   to be open-sourced. Housing the neutral tooling there puts its large
   LOC under public scrutiny and Sonar analysis in the public repo, while
   the private codexFactory shrinks to its true engineering core with a
   correspondingly smaller private Sonar surface.

Every month of divergence makes the move harder: the dashboard runtime is
growing (branch sessions, wheel verbs, repo selector), and each new
feature deepens the path citations. Relocating now, immediately after
contract-v1.29, is the cheapest this move will ever be.

## What Changes

- MODIFIED `doc-health` — Ownership and hosting split: the implementation
  (checker scripts, report generator, reusable workflow) moves to
  openxFactory alongside the contract it follows. The nightly runner
  stays hosted by the xFactory aggregation repo; content authority stays
  with each owning factory (unchanged).
- MODIFIED `lifecycle-notebook-projection` — Projection implementation
  ownership: openxFactory owns both the contract and the conforming sync
  implementation (`scripts/sync-notebooklm-books.py`). Conformance
  framing (book identity, charter, prefixes via OpenSpec delta) is
  unchanged.
- RELOCATE (realization tranches, no further spec text): the ideation
  dashboard runtime (`scripts/ideation_dashboard/`, `web/`, nightly
  entrypoints, session runbook, tests) moves to openxFactory. The
  ideation-dashboard capability spec is silent on implementation home, so
  no delta is required; the staged `dashboard-repo-selector` exit 2
  (install-shipped runtime plane) is NOT realized by this change — this
  change only gives that future work a neutral home to grow in.
- COORDINATE: the active `add-cross-factory-ideation-routing` change's
  unpromoted ownership requirement ("codexFactory SHALL own selection,
  orchestration adapters, validation, and report integration") is amended
  in place to name openxFactory, since the lanes move with the doc_health
  package that hosts them.
- ADOPT into the aggregation repo (not openxFactory): the CloudPC
  self-hosted-runner readiness evaluators (`readiness.py`,
  `readiness_dispatch.py`) — CI-host infrastructure that belongs with the
  runner host.
- codexFactory sheds the moved trees and updates its README and
  `stack.yaml`; engineering-owned lanes (execution_lane, merge_master,
  review lane's PR half, the nine engineering workflows) stay put.

## Impact

- Specs: `doc-health`, `lifecycle-notebook-projection` (MODIFIED);
  `add-cross-factory-ideation-routing` amended pre-promotion.
- Consumers repointed: the aggregation nightly workflow's `uses:` line,
  the workspace CLAUDE.md sync command, openxFactory docs' eight
  invocation paths, `examples/lifecycle-notebook-workspaces.yaml`
  `managed_by`, the two neutral-schema path citations (which become
  truthful in-repo references), `ideation/cross-reference.yaml`'s
  producer note.
- The moved test suites (~46k LOC) run under openxFactory's pytest
  surface; doc-health remains self-gating.
- History: file trees are copied with provenance notes (branch@sha), NOT
  history-grafted — codexFactory's private commit history must not ride
  into a repo slated for open-sourcing (design D1).
- No contract bundle: nothing in contracts/manifest.yaml changes; this is
  tooling relocation, `target_release: none`.
