# Cloud/Workstation Topology and the Drive→NotebookLM Projection Mirror — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Fixes the local-vs-cloud custody question for the ideation system:
git (GitHub) stays the ONLY truth; every cloud surface is a derived
projection. Rejects cloning repos into Google Drive (sync clients corrupt
.git and a checked-out branch is the wrong thing for NotebookLM to ingest);
adopts instead a PROJECTION MIRROR — a CI lane exports lifecycle-filtered
markdown (canon/drafts/ideation sets, no .git, revision-stamped) into a
Drive folder owned by the org service identity, which Google's announced
Drive↔NotebookLM sync then keeps ingested. Locks dashboard multiplicity:
ONE shared hosted instance projecting main (per-user identity for actions,
per the dashboard-action-center intents), with each engineer's per-branch
view served by the LOCAL generate-and-open dashboard, not per-engineer
hosted forks.
Topics: notebooklm-projection, lifecycle-projection, ideation-dashboard, google-drive, identity-brokering, keycloak, custody-tiers, doc-management, doc-workflow
Repository context: openxFactory (capability owner; realization spans codexFactory + aggregation lanes)
Captured: 2026-07-23

## The topology principle (Brett + session, 2026-07-23)

System of record ≠ derived surface (the custody-tiers principle, applied to
our own tooling). GitHub holds the governed corpus; the dashboard, the
NotebookLM books, and any Drive presence are PROJECTIONS regenerated from
git — never rival custody planes. Workstations hold clones for authoring;
"the cloud" holds truth (GitHub) plus projections (dashboard image, NLM
notebooks, Drive mirror).

## Rejected: git clones inside Google Drive

Drive-for-desktop syncing a working tree is a documented repo-killer:
tens of thousands of small `.git` object files, `index.lock` races against
the sync client, wholesale re-uploads on every branch switch — and even
when it survives, Drive↔NLM would ingest WHATEVER BRANCH IS CHECKED OUT,
flip-flopping notebook contents on someone's working state. "Move branches
on the gdrive" dissolves once cloud surfaces project main only; branch
exploration is a local concern.

## Locked: the projection mirror

A projection lane (nightly or on-merge; the doc-health lane family's
pattern) EXPORTS the governed corpus to a Drive folder tree owned by the
org Workspace service identity (the hosted-NLM plan's xfactory-notebooks@):

- clean markdown only, filtered by lifecycle set (`canon/`, `drafts/`,
  `ideation/` — mirroring the xf-canon/xf-drafts/xf-ideation notebooks);
- no `.git`, no worktrees, no unmanaged files; deterministic content;
- revision-stamped (each export records the source_revision it projects —
  the hash-locked-evidence discipline);
- Drive↔NotebookLM sync (Google's announced integration) keeps the
  notebooks ingested from those folders, replacing per-source push churn.

The existing `sync-notebooklm-books.py` (nlm CLI) stays as the fallback
until the Drive path is proven. Native NLM sharing remains the grant list
(share = grant, per engineer identity), per the hosted-NLM synthesis.

## Locked: dashboard multiplicity

ONE shared hosted dashboard projecting main — the truth is shared, so the
view is shared; per-user identity scopes ACTIONS (intents carry the actor;
see dashboard-action-center) and per-user UI state stays local (workbench
sets are gitignored by design). Each engineer's per-branch dashboard is the
LOCAL `generate-and-open` against their working tree — per-engineer views
with zero hosted infrastructure and no truth drift.

## Workspace identity implications

Per-engineer Google Workspace users are required by the NLM sharing model
REGARDLESS of Drive topology (share = grant, per identity) — the projection
mirror adds no additional identity cost: one service account owns the Drive
tree and notebooks; engineers receive shares. Keycloak-brokered identity
(existing brainstorm) later drives the share lists automatically.

## Open questions

- Does Drive↔NLM sync ingest markdown files well (vs preferring Docs/PDF),
  and what is its refresh cadence/quota behavior on a few hundred files?
  (Spike before the lane is built.)
- Folder↔notebook mapping: one Drive folder per lifecycle set mapped to one
  notebook, or per-topic subfolders for the hybrid per-set pattern the
  lifecycle-notebook-projection doc already defines?
- Export transform: raw markdown vs light rendering (front-matter headers
  are load-bearing for humans; NLM may read them as noise).
- Service-account custody of the Drive tree: which install repo owns the
  provisioning runbook (OpsxFactory pattern), and where does the Drive API
  credential live (never in the serving pod — a lane credential like the
  factory identity).
- Whether the workbench's ad-hoc reference sets also get ephemeral Drive
  exports for personal notebooks, or stay nlm-CLI-driven.

## Possible feats

- Drive projection-mirror lane (lifecycle-filtered, revision-stamped export
  to a service-owned Drive tree).
- Drive↔NLM markdown-ingestion spike (cadence, quotas, front-matter noise).
- Keycloak-driven NLM share-list automation.
- Local-dashboard quickstart doc (per-branch view as the per-engineer
  dashboard).
