---
code_surface: openxFactory (`.github/workflows/doc-health-reusable.yml` gains ONE new finalize-job stage — an ideation-dashboard REFRESH lane ordered after the report-delivery step, following the file's established readiness-evaluate + artifact-only-child-dispatch idiom already used five times for `xfactory-artifact-workers`; a refresh-lane module beside `scripts/ideation_dashboard/nightly_lane.py` writing a `health/ideation-dashboard/refresh-status.json` sibling of the existing `lane-status.json`, delivered by the existing `git add health/` rolling-PR step; tests under `tests/ideation-dashboard/` over the status artifact, the no-change short-circuit, and the envelope-shaped diff the lane may produce). CROSS-REPO REALIZATION, as this program's earlier lane changes had (the artifact-only children live in the aggregation, not here): xFactory aggregation — one new artifact-only child workflow `dashboard-image-worker.yml` (fresh openxFactory `main` checkout, `--strict` snapshot generation from that checkout, `docker build` from Omnigent-Install's `containers/ideation-dashboard/Dockerfile` at ITS `main`, push to `acropensoftxfactoryqa.azurecr.io`, digest emitted as its only result artifact), following `doc-health-analysis-worker.yml`'s shape (`runs-on: {group: xfactory-artifact-workers, labels: <dispatch_label>}`, `environment: worker-credentials`, credential-by-reference); Omnigent-Install — a SECOND candidate class in the merge-master envelope instance plus the repository-side digest-shape check that gates it, and the `acr_push`-scoped host credential the worker's build needs (worker-host manifest + its schema, both Omnigent-Install-owned). NO change to the deterministic doc-health pass, to any check family, to the existing snapshot lane, to the worker permission matrix, to the dashboard renderer or serve, or to what the overlay renders.
target_release: implementation_pending — the requirements land now; the change archives only on merged code with green realization evidence, because its whole content is a delivery lane. The evidence gate is one real nightly producing a digest-only pin PR against Omnigent-Install that merge-master approves, GitHub auto-merges and Flux reconciles, PLUS one deliberately wider diff from the same lane identity refused and parked. A lane proven only by a dry run is exactly the evidence this program has learned not to accept.
Status: ratified
Ratified: 2026-08-25 by Brett — in-session, verbatim: "ratify add-nightly-dashboard-refresh against its realized system". The ratification is AGAINST THE REALIZED SYSTEM: the lane's code is merged and wired across all three repositories (openxFactory PR #260 `de638933` and #261 `446291d4`; aggregation opensoft/xFactory PR #141 `c1bba45d`; Omnigent-Install PRs #123 `7d0370d5`, #126 `7365eb36`, #129 `509b7d65`, #143 `5b5592e4`, #146 `575bc26f`, #153 `da0bdeba`), with required-check ruleset 21294850 ("dox digest-only pin scope", target `branch`, enforcement `active`) live on Omnigent-Install's default branch — each verified merged at this gate rather than read out of a handoff. It does NOT ratify an exercised lane: no nightly has yet executed the refresh stage, so this change's own `target_release` evidence gate is unmet and the ARCHIVE GATE STAYS OPEN — see tasks §4.8.
Proposed: 2026-08-22
Origin: The hosted openXdox dashboard's baked snapshot and baked `/source` corpus are refreshed only when a human rebuilds and repins the image by hand — twice so far, 2026-08-21 and 2026-08-22. The companion change `add-dox-gitops-reconciliation` (Omnigent-Install, merged to `main` 2026-08-22 as `7d0370d`) took the APPLY; it deliberately deferred the two questions this change must answer.
---

# Proposal: add-nightly-dashboard-refresh

## Why

The hosted dashboard's data is frozen at build time and thawed by hand.

`containers/ideation-dashboard/Dockerfile` (Omnigent-Install) bakes three
things that are not application code: the snapshot at
`health/ideation-dashboard/openxFactory-snapshot.json`, and the governed corpus
roots under `openxFactory/` that serve the read-only `/source/` document
viewer. Its own comment states the consequence — "Frozen at build time: the
SAME staleness model as the snapshot, refreshed by the SAME rebuild+rollout."
So refreshing the hosted plane's data means rebuilding the image, pushing it,
and repinning the digest in
`deploy/kubernetes/overlays/aks-qa/kustomization.yaml`.

That has happened twice, both times by a human at a keyboard. The record is
sitting in the overlay right now, in the comment above the current pin:
"BAKED SNAPSHOT + /source corpus refreshed to openxFactory main @ 7ae4fe9,
generated --strict from that same checkout so data and corpus share one
source_revision." A hand-written provenance note is a good habit and a bad
mechanism — the plane is as fresh as the last time somebody remembered.

**The apply half is already solved and is waiting on this half.**
`add-dox-gitops-reconciliation` merged to Omnigent-Install `main` on 2026-08-22
(`7d0370d`). It put the dox overlay under the cluster's own Flux reconciler, so
merging a digest change to `main` deploys it, and it ruled that a digest-only
pin PR from "the governed nightly-refresh lane identity" may merge without
human review. Its proposal says in as many words that legs 1 and 2 — snapshot
regeneration, image build and push, pin-PR authoring — "belong to the companion
change `add-nightly-dashboard-refresh` (openxFactory, planned)", and its task 7
is explicitly ORDERED BEHIND this change, because "a grant whose subject is
unresolved must not be created."

Its two open questions are this change's to close:

1. **the auto-merge mechanism** — approver-bot grant versus ruleset bypass;
2. **the lane identity's concrete name** — left as a placeholder precisely so
   the auto-merge grant would not be written against an unresolved subject.

**And the third hand needed for legs 1–2 already exists too.** The nightly
doc-health run mints a short-lived GitHub App installation token per run
(`XFACTORY_APP_ID` / `XFACTORY_APP_PRIVATE_KEY` through
`actions/create-github-app-token@v2`, `owner: ${{ github.repository_owner }}`),
and it already dispatches five artifact-only children onto the
`xfactory-artifact-workers` runner group behind a fail-closed readiness gate
(runner-group membership plus an authenticated Hermes heartbeat, evaluated by
`scripts/check-worker-readiness.py`). The worker host `cpc-omni01` runs
docker-ce and is bound to `acropensoftxfactoryqa.azurecr.io`. Every part of
legs 1–2 is a thing this lane already does, for other payloads.

So the gap is not capability. It is that nobody has written the stage.

## What Changes

- **The nightly gains an ideation-dashboard REFRESH lane.** One new stage in
  `doc-health-reusable.yml`'s finalize job, ordered AFTER the existing snapshot
  lane and the report/rolling-PR delivery step, so the refresh can never
  jeopardise the report it depends on. The lane dispatches an artifact-only
  child onto `cpc-omni01`: fresh checkout of openxFactory `main`, `--strict`
  snapshot generation from THAT checkout, `docker build` against
  Omnigent-Install's Dockerfile at ITS `main`, push to
  `acropensoftxfactoryqa.azurecr.io` under a date-stamped tag, digest returned.
- **`--strict` is the publication gate.** `--strict` on
  `ideation_dashboard.cli generate` means zero errors AND zero warnings — the
  validator's own contract is "0 ok, 1 findings (or warnings under `--strict`)"
  — and a non-zero exit publishes nothing: no push, no tag, no PR.
- **One revision, not two.** The snapshot is generated from the same fresh
  checkout whose corpus roots get baked, so the snapshot's `source_revision`
  and the baked `/source` tree are the same commit by construction rather than
  by a human's care. This is the recipe the two manual builds used and the
  property the current pin's comment claims.
- **The stage SKIPS rather than falls back.** No eligible runner or a stale
  heartbeat records a skip and the nightly continues — the same fail-closed
  posture the five existing worker lanes take. There is deliberately NO
  GitHub-hosted inline fallback: the docker build and the ACR push belong to
  the worker host that holds the registry binding, and an inline fallback would
  need registry credentials in a hosted job, which is the one thing this design
  is built to avoid.
- **No change means no BUILD, let alone no PR.** The no-change decision is made
  on INPUTS, before anything is built: the lane compares the current corpus
  revision and the current build-recipe revision against the two revisions
  recorded with the currently pinned image, and stops there when both match —
  no checkout, no snapshot, no build, no push, no branch, no PR. It deliberately
  does NOT compare the digest it built against the pinned digest: that
  comparison can never find equality (a fresh checkout re-stamps file
  modification times, so the copied layers differ byte-wise even when every
  file's content is identical, and the base image is referenced by a floating
  tag), so the short-circuit would never fire and the lane would redeploy
  content-equivalent images nightly. The provenance the check reads is written
  into the pin's own comment block — machine-readable, and the same fact the
  two hand-written pins already record in prose. Absent or unparseable
  provenance (today's bootstrap pin) counts as changed: the lane builds once and
  its pin establishes provenance from then on.
- **The pin PR is envelope-shaped by construction.** Authored by the lane's App
  identity on a fixed head branch, changing ONLY the `digest:` line and its
  adjacent provenance comment on the `ideation-dashboard` entry inside the
  `images:` block of the ONE overlay file. The body carries the provenance the
  human note carries today: snapshot `source_revision`, the pushed tag and
  digest, and the strict-validation counts.
- **RULING (a) — the auto-merge mechanism is the merge-master pattern,
  extended.** The approver-bot shape wins, and it is not a new invention: the
  aggregation already runs `merge-master-approval.yml`, whose reviewed
  rules-as-code envelope at `.github/merge-approval-envelope.yml` carries a
  `candidates:` LIST with `target_repos`. Omnigent-Install gets that same
  workflow and its own envelope instance with ONE candidate class for this
  lane. No org-ruleset bypass is created.
- **RULING (b) — the lane identity is the existing `XFACTORY_APP`.** The App
  the reusable workflow already mints per run authors the pin PR, through a
  token minted with Omnigent-Install in its installation scope. What must be
  verified and extended is the App's INSTALLATION on Omnigent-Install:
  `contents: write` and `pull_requests: write` there (plus `actions: write` if
  the cross-repo approval dispatch is the chosen trigger). A new App is minted
  ONLY if that installation cannot be extended, and that contingency is
  recorded rather than assumed away.
- **Authority is conserved on every rung.** The worker builds and pushes and
  holds no repository credential; the App authors a proposal and holds no
  cluster credential; merge-master approves exactly one envelope and issues no
  merge call; GitHub merges; the in-cluster reconciler applies.
  `execute_final_action` and `access_secrets` stay `const: false`.
- **The outcome is visible where the lane's siblings are visible.** A
  `health/ideation-dashboard/refresh-status.json` artifact beside the existing
  `lane-status.json`, delivered by the report's rolling PR, plus a report
  section — so a skipped stage, a strict-validation failure, and a parked PR
  are all readable in the morning without opening Actions.

Out of scope: the APPLY (the companion change owns it — this lane claims no
apply capability and no kubeconfig); any change to the deterministic doc-health
pass or its check families; the existing snapshot lane's own behaviour;
realizing the dashboard's promoted RUNTIME snapshot fetch (named in Design as
the standing conformance gap this lane mitigates and does not close); a
rebake-on-demand verb on the served surface (already refused by the
`ideation-dashboard` capability); and any refresh lane for another surface's
image.

## Capabilities

### Capability placement, and why it is split

Two capabilities, deliberately, along the seam that already exists between
them.

**`doc-health` takes the LANE.** Every nightly lane in this program is a
`doc-health` requirement — "Ideation dashboard snapshot lane", "Possibles
derivation lane", "Ideation readiness lane", "Neutrality drift is scouted
nightly" — and `doc-health` owns both the reusable workflow ("Ownership and
hosting split": the implementation and the reusable workflow "move home with
the contract they follow") and the execution-authority idiom this lane inherits
("Sweep execution split", "Bounded analysis worker profile"). A sixth lane
belongs beside the five, stated in the vocabulary they already established.
Putting lane mechanics into `ideation-dashboard` would split the nightly's
contract across two capabilities for no benefit.

**`ideation-dashboard` takes the SERVED PLANE.** What the rebake must bake, at
which revision, and how stale the baked artifacts may get is a property of the
delivery contract that capability already owns ("Delivery and regeneration",
"Runtime snapshot fetch with baked fallback and displayed freshness",
"Dispatchable publication, never from the served surface"). The freshness
header, the stale banner, and the "an image rebuild MUST NOT be required to
reflect newly published snapshots" rule all live there, and the one thing this
change genuinely owes that capability is a STALENESS BOUND on the baked
artifacts plus an honest record of the gap between the promoted runtime-fetch
design and what the hosted image does today.

### Modified Capabilities

- `doc-health`: SIX ADDED requirements — the refresh lane and its ordering, the
  no-change short-circuit, the envelope-shaped pin PR, the four-authority
  landing chain, the lane's observability and failure posture, and authority
  conservation. No existing requirement is amended: the "Ideation dashboard
  snapshot lane" requirement governs the SNAPSHOT lane and is untouched, and
  this lane is its downstream consumer rather than a change to it.
- `ideation-dashboard`: ONE ADDED requirement (the scheduled rebake's
  one-revision contract and the digest-pin delivery boundary) and ONE MODIFIED
  requirement — "Runtime snapshot fetch with baked fallback and displayed
  freshness" — which gains a staleness bound on the baked fallback and states
  plainly that a served plane whose runtime fetch is not yet realized is
  reading its baked artifacts as data, which is a conformance gap to be
  recorded and closed, not a design to be settled into. All four of its
  promoted scenarios are restated verbatim; the "no rebuild required to reflect
  published data" rule is preserved exactly, because this change must not be
  allowed to read as a licence to make rebuilds the data path.

### New Capabilities

None. Both surfaces are extensions of promoted capabilities through their own
established shapes.

## Impact

- **`openxFactory`** (this repo): one new finalize-job stage in
  `.github/workflows/doc-health-reusable.yml`; one refresh-lane module beside
  `scripts/ideation_dashboard/nightly_lane.py`; one new status artifact under
  `health/ideation-dashboard/`; tests under `tests/ideation-dashboard/`.
- **`opensoft/xFactory` (aggregation)**: one new artifact-only child workflow
  for the build+push, registered like its five siblings, sharing the
  `xfactory-artifact-worker` concurrency group so the singleton host is never
  double-booked.
- **`opensoft/Omnigent-Install`**: a merge-master workflow + envelope instance
  with ONE candidate class, the repository-side digest-shape check that gates
  it, and the `acr_push` host-credential declaration the build needs (a
  worker-host-manifest schema addition — that schema is
  `additionalProperties: false`, so the field cannot be smuggled in).
- **`add-dox-gitops-reconciliation`** (Omnigent-Install, merged `7d0370d`):
  UNBLOCKED. Its task 7 was ordered behind this change's ruling on the lane
  identity; rulings (a) and (b) supply the subject its grant needs, and its
  task 8.3 notification is this change's counterpart.
- **The `XFACTORY_APP` installation**: gains one repository (Omnigent-Install)
  at `contents: write` + `pull_requests: write`. It gains NO cluster authority,
  no registry authority, and no permission on any repository it does not
  already hold.
- **The worker host `cpc-omni01`**: gains a push-scoped registry credential on
  its own host, delivered by reference like its other credentials. It gains no
  repository credential, no kubeconfig, and no permission-matrix change — the
  build is `write_artifacts`, which the matrix already grants.
- **The hosted openXdox plane**: its baked snapshot and `/source` corpus become
  at most about one day plus one reconcile interval behind openxFactory `main`
  under normal operation, instead of "as fresh as the last manual rebuild."
- **Review load**: one digest-only PR per changed night, approved by
  merge-master inside a fail-closed envelope. Nights with no corpus change
  produce nothing at all.
