---
code_surface: openxFactory (`.github/workflows/doc-health-reusable.yml` gains ONE new finalize-job stage — an ideation-dashboard REFRESH lane ordered after the report-delivery step, following the file's established readiness-evaluate + artifact-only-child-dispatch idiom already used five times for `xfactory-artifact-workers`; after the no-change decision, the credentialed hosted parent materializes fresh openxFactory `main` + Omnigent-Install recipe inputs into a bounded sealed source artifact; a refresh-lane module beside `scripts/ideation_dashboard/nightly_lane.py` writes a `health/ideation-dashboard/refresh-status.json` sibling of the existing `lane-status.json`, delivered by the existing `git add health/` rolling-PR step; tests under `tests/ideation-dashboard/` cover the status artifact, the no-change short-circuit, and the envelope-shaped diff the lane may produce). CROSS-REPO REALIZATION, as this program's earlier lane changes had (the artifact-only children live in the aggregation, not here): xFactory aggregation — one new artifact-only child workflow `dashboard-image-worker.yml` (verify and download the parent run's sealed source artifact, `--strict` snapshot generation from its fresh corpus tree at the manifest-pinned source revision/time, `docker build` from the bundled Omnigent-Install `containers/ideation-dashboard/Dockerfile` at ITS recorded `main`, push to `acropensoftxfactoryqa.azurecr.io`, digest emitted as its only result artifact), following `doc-health-analysis-worker.yml`'s shape (`runs-on: {group: xfactory-artifact-workers, labels: <dispatch_label>}`, source delivered as a parent artifact, no repository credential); Omnigent-Install — a SECOND candidate class in the merge-master envelope instance plus the repository-side digest-shape check that gates it, and the `acr_push`-scoped host credential the worker's build needs (worker-host manifest + its schema, both Omnigent-Install-owned). NO change to the deterministic doc-health pass, to any check family, to the existing snapshot lane, to the worker permission matrix, to the dashboard renderer or serve, or to what the overlay renders.
target_release: implementation_pending — the requirements land now; the change archives only on merged code with green realization evidence, because its whole content is a delivery lane. The evidence gate is one real nightly producing a digest-only pin PR against Omnigent-Install that merge-master approves, GitHub auto-merges and Flux reconciles, PLUS one deliberately wider diff from the same lane identity refused and parked. A lane proven only by a dry run is exactly the evidence this program has learned not to accept.
Status: ratified
Ratified: 2026-08-25 by Brett — in-session, verbatim: "ratify add-nightly-dashboard-refresh against its realized system". The ratification is AGAINST THE REALIZED SYSTEM: the lane's code is merged and wired across all three repositories (openxFactory PR #260 `de638933` and #261 `446291d4`; aggregation opensoft/xFactory PR #141 `c1bba45d`; Omnigent-Install PRs #123 `7d0370d5`, #126 `7365eb36`, #129 `509b7d65`, #143 `5b5592e4`, #146 `575bc26f`, #153 `da0bdeba`), with required-check ruleset 21294850 ("dox digest-only pin scope", target `branch`, enforcement `active`) live on Omnigent-Install's default branch — each verified merged at this gate rather than read out of a handoff. It does NOT ratify an exercised lane: no nightly has yet executed the refresh stage, so this change's own `target_release` evidence gate is unmet and the ARCHIVE GATE STAYS OPEN — see tasks §4.8.
Amended: 2026-09-01 by Brett — in-session host ruling, verbatim: "The runner design intentionally requires `repository_credentials_absent`; source is delivered as sealed job artifacts and the runners do not clone or push repositories." This corrects the unexercised realization's raw-clone contradiction without changing the lane's output or authority split: repository reads occur in the credentialed hosted parent, the artifact rider receives a bounded sealed source artifact, and the rider still owns strict generation + build + ACR push while holding no repository credential; the amended delta RE-RATIFIED 2026-09-04 by Brett Heap, in-session, verbatim "re-ratify and merge 595, delete the debug tool, roll out lane-line" (see § AMENDED AFTER RATIFICATION). The 2026-08-25 `Ratified:` line above stands unchanged and governs everything this amendment does not touch.
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

  > **AMENDED 2026-09-01, RE-RATIFIED 2026-09-04 by Brett Heap — in-session,
  > verbatim "re-ratify and merge 595, delete the debug tool, roll out
  > lane-line" — the fresh checkout moves to the credentialed parent.** The
  > sentence above is the text as RATIFIED 2026-08-25 and is retained
  > unedited. Under Brett's 2026-09-01 host ruling, re-ratified 2026-09-04,
  > the lane reads instead: the credentialed hosted parent seals fresh
  > openxFactory `main` plus Omnigent-Install's Dockerfile at ITS `main` into a
  > bounded source artifact; the credential-free child verifies it, runs
  > `--strict` snapshot generation from THAT corpus tree, builds, and pushes to
  > `acropensoftxfactoryqa.azurecr.io` under a date-stamped tag, digest
  > returned. See § AMENDED AFTER RATIFICATION, 2026-09-04.
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

## AMENDED AFTER RATIFICATION, 2026-09-04 — RE-RATIFIED 2026-09-04

**RE-RATIFIED 2026-09-04 by Brett Heap — in-session, verbatim: "re-ratify and merge 595, delete the debug tool, roll out lane-line" — ratifying the amended delta as recorded in this section (the five movements, including the "Git repository" qualification taken in Copilot round 4), on PR #595 at head e84d060a.**

*(Superseded by the re-ratification above; retained as the record of the pending state.)* **NOTHING HERE IS RATIFIED YET.** This section records an amendment to a
packet that was ratified 2026-08-25 and whose docs are already merged on
`main` (PRs #260 `de638933`, #261 `446291d4`, #356). It is written the way
`archive/2026-09-01-add-release-tag-publication-check` § AMENDED AFTER
RATIFICATION was written before its consenting act landed: *"Recorded here as
an amendment awaiting Brett rather than absorbed into the realization, because
the ratified baseline named a delta and this is not that delta."* The same
sentence governs this one. The 2026-08-25 ratification stands for everything
below that this amendment does not touch.

**Provenance of the text.** The amendment was authored 2026-09-01 by the lane
`openxfactory-nightly` and stranded uncommitted in the shared aggregation
checkout at `6612d323`. It was rescued byte-identical as PR #595 (issue #591,
2026-09-02), held 24 hours for its originating lane, and adopted by lane
`openxfactory-f2` on 2026-09-04 on Brett's word, verbatim: "go on 595". The
prose below is the originating lane's; the standing statement, the retained-text
restorations and this section are the adopting lane's.

### The ruling that motivates it

Brett Heap, in session 2026-09-01, verbatim:

> The runner design intentionally requires `repository_credentials_absent`;
> source is delivered as sealed job artifacts and the runners do not clone or
> push repositories.

### The defect the ruling exposes

The ratified delta placed a **raw repository clone on the artifact worker** —
*"a FRESH checkout of openxFactory `main` (never the aggregation's submodule
pin)"* — inside a lane whose own authority requirement holds that *"the worker
SHALL hold no repository credential."* Both input repositories are private, so
the two sentences cannot both be satisfied: an artifact rider with no
repository credential cannot perform the clone the lane's own recipe requires.
The contradiction was latent because the lane has never run (its archive gate
is still open, `target_release: implementation_pending`, tasks §4.8); the first
real child runs surfaced it empirically. The alternative — deploying repository
keys to the rider through Intune — would weaken the host contract to rescue an
implementation detail, which is the trade this program has ruled against
before.

### The correction

Move ONLY the repository-read act to the credentialed hosted parent. The parent
materializes fresh openxFactory `main` plus the Omnigent-Install recipe into a
bounded, sealed Actions artifact carrying a manifest; the credential-free child
verifies and consumes only that artifact. Strict generation, Docker build, ACR
push and digest production stay on the artifact rider, unchanged. **The lane's
output, its authority split, its permission matrix, its `--strict` publication
gate and its evidence gate are all unchanged.** What changes is that the
realization no longer contradicts `repository_credentials_absent`.

### What moved in `specs/doc-health/spec.md` — the whole of it

Two requirements are touched. **No requirement title changes, no requirement is
added or removed, and no `## MODIFIED Requirements` block is introduced** — the
delta remains a single `## ADDED Requirements` block, so no `sequenced_after`
live pin and no `modified-block-currency` arm moves (measured, not predicted;
see the PR body).

1. **`Requirement: Ideation-dashboard image refresh lane`** — the opening
   paragraph's work description is rewritten. BEFORE: *"Its work is then: a
   FRESH checkout of openxFactory `main` (never the aggregation's submodule
   pin); snapshot generation from THAT SAME checkout under `--strict` …"*
   AFTER: *"The credentialed hosted parent SHALL then materialize fresh
   openxFactory `main` (never the aggregation's submodule pin) plus the
   Omnigent-Install recipe at ITS `main` into a bounded sealed source artifact
   carrying the source HEAD, source committer timestamp, and both path-scoped
   input revisions. The credential-free child SHALL verify and download that
   artifact … The worker SHALL perform no repository clone, fetch, or push."*
   The `--strict`-precedes-the-push paragraph beneath it is untouched.
2. **Its `#### Scenario: The lane runs on a night with corpus movement`** —
   the THEN bullet is rewritten to name the parent's seal and the child's
   verification. The AND bullet (*"the snapshot's `source_revision` and the
   baked corpus revision MUST be the same commit"*) is untouched, which is the
   property the whole decision exists to hold.
3. **ONE NEW SCENARIO** on that requirement — `#### Scenario: The sealed source
   artifact is unavailable or invalid` — failing the child before strict
   generation and before any registry credential is used, with no repository
   fallback.
4. **`Requirement: The refresh lane conserves the worker and identity authority
   the nightly already holds`** — ONE NEW PARAGRAPH appended, prohibiting
   repository credentials, deploy keys, credential helpers, raw clones and
   repository network access on the worker. The requirement's existing first
   paragraph, including *"The worker SHALL hold no repository credential"*, is
   untouched; the new paragraph makes the positive mechanism explicit rather
   than widening the prohibition.
5. **ONE NEW SCENARIO** on that requirement — `#### Scenario: The worker is
   asked to fetch repository source` — rejecting any realization that places a
   repository token, deploy key, credential helper or raw clone on the artifact
   worker.

**DISAMBIGUATION BY THE ADOPTING LANE, 2026-09-04 — the only words of the
amendment this lane changed, and it changed them because they contradicted
themselves.** Copilot, reviewing this PR, found that the sentence added at
item 1 — *"The worker SHALL perform no repository clone, fetch, or push"* —
**forbids in its closing clause the very act the same sentence requires**: a
push to `acropensoftxfactoryqa.azurecr.io`. The collision is not hypothetical
prose-picking: this packet itself calls the push target an *"image
repository"* (§2 of `tasks.md`, and the authority requirement's own
"scoped to the single image repository"), so "repository" is genuinely
overloaded across these very requirements. The same ambiguity sat in the new
prohibition paragraph at item 4, whose "repository network access on the
worker are prohibited" would read on the registry too.

Both are now qualified to **GIT** repositories explicitly, and the prohibition
paragraph closes by saying so and by stating that the worker's push-scoped
credential for the single `ideation-dashboard` IMAGE repository is neither
widened nor withdrawn. **NO OBLIGATION MOVES** — this is the reading every
other sentence in the packet already assumes, and the amendment's whole
subject is repository credentials rather than registry ones. It is recorded
here, rather than absorbed silently, because it edits the text put to Brett
for ratification, and a lane that quietly rewrites what it asks to be ratified
has broken the thing this section exists to protect.

**Direction of travel.** Every one of the five is a NARROWING or a
clarification. Nothing the ratified delta forbade becomes permitted; two new
things the ratified delta permitted only by omission become forbidden.

### What moved in this file's own `code_surface:` declaration

The front-matter `code_surface:` line is a single machine-read value, so it
cannot carry the retained text beside the amended one. The pre-amendment
wording is therefore preserved here, phrase by phrase — this is the WHOLE of
what moved in it:

| retained (as ratified 2026-08-25) | amended 2026-09-01 |
| --- | --- |
| *(nothing at this position)* | inserted: "after the no-change decision, the credentialed hosted parent materializes fresh openxFactory `main` + Omnigent-Install recipe inputs into a bounded sealed source artifact;" |
| "(fresh openxFactory `main` checkout," | "(verify and download the parent run's sealed source artifact," |
| "that checkout," | "its fresh corpus tree at the manifest-pinned source revision/time," |
| "Omnigent-Install's" *(Dockerfile)* | "the bundled Omnigent-Install" *(Dockerfile)*, "at ITS **recorded** `main`" |
| "`environment: worker-credentials`, credential-by-reference);" | "source delivered as a parent artifact, no repository credential);" |
| "writing" / "over" *(grammar)* | "writes" / "cover" |

**ONE READER'S NOTE ON THE LAST ROW, raised by the adopting lane and not
resolved here.** The amended clause drops the words `environment:
worker-credentials` from the child's shape description. The ACR PUSH credential
that environment carries is NOT withdrawn by this amendment — §2 of `tasks.md`
is entirely about it, the authority requirement still describes it as "a host
substrate credential, scoped to the single image repository, delivered to the
host BY REFERENCE", and the amendment's own subject is repository credentials,
not registry ones. So the drop reads as compression rather than a withdrawal.
It is recorded because a later reader diffing this line alone could read it the
other way, and because the spec delta — which is the governing text — does not
mention the environment at all in either version.

### What Brett is being asked to do

**One word on the delta.** Accepting it flips this section's heading to
ACCEPTED, converts the `Amended:` front-matter line's pending clause into a
consenting citation naming the act, and leaves the 2026-08-25 `Ratified:` line
and `Status: ratified` exactly as they are. Declining it means the amended
delta text comes out and the ratified delta is restored, with the
`repository_credentials_absent` contradiction filed as an open defect against
the unexercised realization instead.

### The consequence this amendment does NOT discharge

The landed realization may now disagree with the amended delta. Aggregation PR
#141 (`c1bba45d`) and PR #179 (`de9a1d99`) landed the child workflow with a
sparse/blobless repository checkout ON THE CHILD; PR #179's fix was to the
CHECKOUT SHAPE, not to who performs it. If that is still the shape on
`opensoft/xFactory` `main`, the code and the amended spec disagree and a
follow-up realization is owed. **This was not assessed here — the aggregation
is outside this repository and outside this PR's diff** — and it is the reason
the lane's archive gate stays open regardless of how the delta is ruled.

### REALIZED 2026-09-04 — the follow-up realization the paragraph above owed

**The disagreement the section above declined to assess was real, and it is
now closed.** It was assessed on `opensoft/xFactory` `main` immediately after
re-ratification: the child workflow still declared two repository-scoped
**SSH deploy keys** and ran two `git clone --filter=blob:none` fetches, exactly
the shape PR #179 had corrected without moving. That contradicted the lane's
own readiness gate — the AGGREGATION's `scripts/worker_readiness.py` fails it
closed with `repository_credentials_present` unless the host heartbeat attests
`repository_credentials_absent: true` — so the lane could be READY or it could
FETCH, never both. That module and the `scripts/check-worker-readiness.py` CLI
which imports it BOTH live in `opensoft/xFactory`, never in this repository:
`doc-health-reusable.yml` is a REUSABLE workflow, so its
`python3 scripts/check-worker-readiness.py` resolves in the CALLER's checkout.
They are one CLI-plus-module pair, not two competing entrypoints, and this
paragraph names the module because the gate's predicate lives there. Brett ordered the re-realization in-session, verbatim:
"go S2 to S7", then "lets go". Five pull requests landed it, each verified
merged at the gate rather than read out of a handoff:

- **openxFactory #642** (squash `bbc21e41`) — `--generated-at <RFC 3339>` on
  `ideation_dashboard.cli generate` / `generate-and-open`, validated at the CLI
  boundary and REFUSED when malformed. Discharges `tasks.md` § 3.6, the one
  realization task the amendment itself created.
- **openxFactory #641** (squash `19a777d8`) — retires
  `dashboard_refresh_lane.py`'s own raw-clone `--phase build` recipe, a second
  and unreached realization of the pre-amendment recipe that the amended delta
  now forbade whether or not a caller existed.
- **openxFactory #648** (squash `96aa61a3`; path containment hardened in its
  branch commit `5628fab1`, folded into the squash) — the credentialed parent
  SEALS: `--phase seal`, a `manifest.json` carrying the source HEAD, the source
  committer timestamp, both path-scoped input revisions, a per-file sha256
  index and a `tree_digest` over it; the `git archive` pax-header revision
  assertion; `dfr-seal` / `dfr-upload` steps in `finalize`; the dispatch gated
  on `sealed == 'true'` and the upload's `outcome`.
- **opensoft/xFactory #243** (squash `84dbbb24`) — the child CONSUMES: a
  cross-run `actions/download-artifact@v4`, then eight ordered verification
  steps ALL BEFORE the ACR login, which is literally what the new scenario's
  "fail before strict generation and before any registry credential is used"
  requires. The deploy keys, the clones, and every `git` invocation, `GIT_*`
  env, `ssh://` URL and credential helper are gone from the file; the job id
  `build-and-push` and the frozen grandfather enumeration are untouched, so no
  second door is opened. The ACR push is unchanged, per the amendment's own
  GIT qualification.
- **Omnigent-Install #211** (`cdfe3152`) — the worker profile's `description`,
  `capabilities` and `prerequisites` now describe the sealed intake; the raw
  `git clone` prerequisite is gone, so the profile stops contradicting its own
  `repository_credentials_absent` attestation and
  `repository_tokens_allowed: false`. `profile_version` deliberately stays 1 —
  the attested heartbeat keys did not move, so
  `--required-profile-version 1` needs no lockstep edit.

**THE ARCHIVE GATE STAYS OPEN, and nothing above is evidence that it should
not.** These five acts remove a code/spec disagreement and a deadlock;
they make the lane exercisable, which is not the same as exercised. What is
still owed is S7 — the operator's host acts and the first real nightly. Act
**D**, provisioning the SSH deploy-key Git substrate, is DELETED rather than
deferred (there is nothing left on the worker to provision it for); acts
**(A)** the heartbeat publisher advertising label `dashboard-image` and profile
`dashboard-image-refresh` v1, **(B)** `XFW_ACR_PUSH_USER` /
`XFW_ACR_PUSH_TOKEN` in the runner service environment, **(C)** Docker with
Linux containers on the rider — which still carries a RULING, not merely an
act — and **(E)** `python3` + PyYAML for the service account remain. Then the
first real nightly, in both directions: one digest-only pin PR merged and
reconciled, PLUS one deliberately wider diff refused and parked. That is this
change's own `target_release` bar and it is unmoved. Recorded in full at
`tasks.md` § 9a.
