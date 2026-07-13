# Proposal Origin Migration Evidence

Status: record
Kind: report
Repository context: openxFactory
Change: add-proposal-origin-contract
Approved by: Brett
Approved on: 2026-07-12

## Purpose

Records, per change, the classification (`already-compliant` / `staged` /
`ad_hoc`), whether an origin block was applied or was already present, and
the quoted or cited evidence each backfilled origin derives from. No origin
in this migration was fabricated: staged classifications derive from a
recorded supporting-docs manifest or an equivalent staging-provenance
record; every other change is classified `ad_hoc` with a reason and
approval drawn from the packet, the repository README, or git history
(read-only).

Task 3.1 (amend the archived bootstrap packet) and task 3.2 (backfill every
other archived change) are both recorded below. Active changes are outside
this migration's scope — task 3.2 explicitly excludes them — and are listed
in the "Active changes (not touched)" section purely for completeness.

## Archived changes

### 3.1 — Bootstrap amendment

**`archive/2026-07-09-add-proposal-supporting-doc-lifecycle`** —
classification: `ad_hoc`. Applied.

Evidence: this is the exact block prescribed verbatim by
`supporting-docs/origin-contract.md`'s Migration section, item 1, in
`openspec/changes/add-proposal-origin-contract/`. The existing
`.openspec.yaml` carried only `schema: spec-driven` / `created: 2026-07-09`,
no origin. Applied block:

```yaml
origin:
  kind: ad_hoc
  id: openxFactory:adhoc:2026-07-09-proposal-support-lifecycle-bootstrap
  reason: The origin contract did not exist when this bootstrap change was created
  approved_by: Brett
  approved_on: 2026-07-09
```

### 3.2 — Backfill

**`archive/2026-06-26-enable-live-openxfactory`** — classification: `ad_hoc`.
Applied.

Evidence: no supporting-docs manifest, no staging reference in
`proposal.md`/`design.md`. `git log --follow` on `.openspec.yaml` traces
through a rename (`enable-live-openworkflow-factory` →
`enable-live-openxfactory`) to commit `229761cb` "Add live factory runtime
OpenSpec change (#19)" by Brett Heap, 2026-06-25/26 — the second OpenSpec
proposal ever created in this repo (only `restructure-factory-repo-boundaries`
predates it), authored and merged directly by the repo owner.
`ideation/staging` did not exist until commit `cf96b14` "Organize all
brainstorm material into orthogonal staged topics" on 2026-07-08
(`git log --diff-filter=A -- 'ideation/staging/*'` shows no earlier entries)
— the staging pipeline could not have existed at creation.

**`archive/2026-06-26-migrate-canonical-policy-to-openxfactory`** —
classification: `ad_hoc`. Applied.

Evidence: no supporting-docs manifest, no staging reference in
`proposal.md`/`design.md`. `git log --follow` on `.openspec.yaml` traces to
commit `584bf0ec` "Add OpenSpec content migration proposal" by Brett Heap,
2026-06-26, archived the same day via PR #18 (commit `d7b66d72`). Predates
the ideation/staging pipeline (introduced 2026-07-08, see prior entry's
evidence).

**`archive/2026-06-26-restructure-factory-repo-boundaries`** —
classification: `ad_hoc`. Applied.

Evidence: no supporting-docs manifest, no staging reference in
`proposal.md`/`design.md`. `git log --diff-filter=A` shows commit
`ffded73` "Add OpenSpec repo boundary proposal", authored by Brett Heap
2026-06-26 08:55:44 — this is the very first OpenSpec change created in the
repository (introduces the `.codex/skills/openspec-*` tooling itself). No
staging pipeline could predate the first-ever proposal.

**`archive/2026-07-08-add-customer-memory-gateway-architecture`** —
classification: `ad_hoc`. Applied.

Evidence: no supporting-docs manifest, no staging reference in
`proposal.md`/`design.md`/`tasks.md`. `.openspec.yaml` recorded
`created: 2026-07-02`. `git log` traces the earliest related commit to
`493fb33` "Define xFactory memory gateway taxonomy" by Brett Heap,
2026-07-03 (predates the 2026-07-08 introduction of `ideation/staging`).
`tasks.md` line 4 notes "Retrospectively record approval for tasks 7.6/7.7
... before this change was archived", confirming direct, retrospectively
approved authorship rather than a staged pipeline.

**`archive/2026-07-09-add-contested-finding-rule`** — classification:
`staged`. Applied (created `.openspec.yaml`; none existed).

Evidence: `supporting-docs.manifest.yaml` records
`"origin_path": "ideation/staging/contested-findings"`,
`"source_revision": "18fcf803470ba4e43aace476cda43eda1ac9ddf0"`,
`"transitioned_at": "2026-07-09"`. Topic slug derived from `origin_path`.

**`archive/2026-07-09-add-doc-health-contract`** — classification: `staged`.
Applied (created `.openspec.yaml`; none existed).

Evidence: `supporting-docs.manifest.yaml` records
`"origin_path": "ideation/staging/doc-health-checks"`,
`"source_revision": "18fcf803470ba4e43aace476cda43eda1ac9ddf0"`,
`"transitioned_at": "2026-07-09"`. Creation date 2026-07-08 per
`git log --diff-filter=A`.

**`archive/2026-07-09-add-document-lifecycle-vocabulary`** —
classification: `ad_hoc`. Applied (created `.openspec.yaml`; none existed).

Evidence: no `.openspec.yaml` and no supporting-docs manifest at all.
`proposal.md`/`design.md` show this change itself ratifies the
`ideation/brainstorm` + `ideation/staging` convention ("Ratify the ideation
work area convention ... as the sanctioned pre-proposal path"). `git log`
traces creation to commit `eb640dc` "Propose document lifecycle vocabulary
OpenSpec change", Brett Heap, 2026-07-08 19:03:53 UTC. Since this change
creates the staging convention, no staged source could logically have
preceded it.

**`archive/2026-07-09-add-lifecycle-notebook-hybrid-imports`** —
classification: `staged`. Applied.

Evidence: existing `.openspec.yaml` had only `schema: spec-driven` /
`created: 2026-07-09`, no origin. `supporting-docs.manifest.yaml` records
`"origin_path": "ideation/staging/lifecycle-notebook-hybrids"`,
`"source_revision": "18fcf803470ba4e43aace476cda43eda1ac9ddf0"`,
`"transitioned_at": "2026-07-09"`.

**`archive/2026-07-09-add-lifecycle-notebook-projection`** —
classification: `ad_hoc`. Applied (created `.openspec.yaml`; none existed).

Evidence: no `.openspec.yaml` and no supporting-docs manifest at all.
`git log` traces creation to commit `52fd6aa` "Propose lifecycle notebook
projection OpenSpec change", Brett Heap, 2026-07-08 20:04:39 UTC — one hour
after the document-lifecycle-vocabulary proposal that itself created the
staging convention (`eb640dc`, 19:03:53 UTC same day). No staged topic
could have existed for this in the intervening hour, and none is
referenced in `proposal.md`.

**`archive/2026-07-09-add-release-realization-flow`** — classification:
`staged`. Applied (created `.openspec.yaml`; none existed).

Evidence: `supporting-docs.manifest.yaml` records
`"origin_path": "ideation/staging/release-flow"`,
`"source_revision": "18fcf803470ba4e43aace476cda43eda1ac9ddf0"`,
`"transitioned_at": "2026-07-09"`.

**`archive/2026-07-09-adopt-workflow-visualization-stack`** —
classification: `staged`. Applied (created `.openspec.yaml`; none existed).

Evidence: `supporting-docs.manifest.yaml` records
`"origin_path": "ideation/staging/workflow-visualization"`,
`"source_revision": "18fcf803470ba4e43aace476cda43eda1ac9ddf0"`,
`"transitioned_at": "2026-07-09"`.

**`archive/2026-07-09-concretize-prose-tagging-syntax`** — classification:
`staged`. Applied (created `.openspec.yaml`; none existed).

Evidence: `supporting-docs.manifest.yaml` records
`"origin_path": "ideation/staging/prose-tagging"`,
`"source_revision": "18fcf803470ba4e43aace476cda43eda1ac9ddf0"`,
`"transitioned_at": "2026-07-09"`. Creation date 2026-07-08 per
`git log --diff-filter=A`.

**`archive/2026-07-09-neutralize-job-envelope`** — classification:
`staged`. Applied (created `.openspec.yaml`; none existed).

Evidence: `supporting-docs.manifest.yaml` records
`"origin_path": "ideation/staging/job-envelope-neutralization"`,
`"source_revision": "18fcf803470ba4e43aace476cda43eda1ac9ddf0"`,
`"transitioned_at": "2026-07-09"`.

**`archive/2026-07-09-promote-credential-contracts`** — classification:
`staged`. Applied (created `.openspec.yaml`; none existed).

Evidence: `supporting-docs.manifest.yaml` records
`"origin_path": "ideation/staging/credential-contracts"`,
`"source_revision": "18fcf803470ba4e43aace476cda43eda1ac9ddf0"`,
`"transitioned_at": "2026-07-09"`.

**`archive/2026-07-09-promote-workflow-gate-contract`** — classification:
`staged`. Applied (created `.openspec.yaml`; none existed).

Evidence: `supporting-docs.manifest.yaml` records
`"origin_path": "ideation/staging/workflow-gate-contract"`,
`"source_revision": "18fcf803470ba4e43aace476cda43eda1ac9ddf0"`,
`"transitioned_at": "2026-07-09"`.

**`archive/2026-07-09-reconcile-domain-neutral-and-engineering-spec-ownership`**
— classification: `ad_hoc`. Applied.

Evidence: existing `.openspec.yaml` had only `schema: spec-driven` /
`created: 2026-07-08`, no origin. No supporting-docs manifest. `proposal.md`
"Why" describes a direct doc/spec mismatch fix ("Current openxFactory
documentation says ... but promoted OpenSpec specs still say ..."), not
staged material. `git log` traces creation to commit `d5ada44` "Reconcile
domain-neutral spec ownership", Brett Heap, 2026-07-08, authored and landed
directly.

**`archive/2026-07-09-refine-promotion-provenance`** — classification:
`staged`. Applied (created `.openspec.yaml`; none existed).

Evidence: `supporting-docs.manifest.yaml` records
`"origin_path": "ideation/staging/promotion-refinements"`,
`"source_revision": "18fcf803470ba4e43aace476cda43eda1ac9ddf0"`,
`"transitioned_at": "2026-07-09"`.

**`archive/2026-07-09-split-roles-authority`** — classification: `staged`.
Applied (created `.openspec.yaml`; none existed).

Evidence: `supporting-docs.manifest.yaml` records
`"origin_path": "ideation/staging/roles-authority-split"`,
`"source_revision": "18fcf803470ba4e43aace476cda43eda1ac9ddf0"`,
`"transitioned_at": "2026-07-09"`.

**`archive/2026-07-10-add-xfactory-installer-repository`** —
classification: `ad_hoc`. Applied.

Evidence: existing `.openspec.yaml` had only `schema: spec-driven` /
`created: 2026-07-10`, no origin. `supporting-docs.manifest.yaml` explicitly
records `"origin_path": null` and `"source_revision":
"not-applicable-ad-hoc"` — already flagged ad hoc at packaging time. The
bundled `repository-boundary.md` (extracted from `supporting-docs.tar.gz`,
read-only) states verbatim: "Proposal origin: ad hoc", "Authorized by:
explicit user direction in the xFactory Cloud PC intake task", "Captured:
2026-07-09", and "This proposal was authorized directly from design
discussion and did not derive from an existing brainstorm or staging
folder. It is therefore explicitly ad hoc rather than assigned a fabricated
staging identifier."

**`archive/2026-07-12-add-doc-health-semantic-sweep`** — classification:
`staged`. Applied.

Evidence: existing `.openspec.yaml` had only `schema: spec-driven` /
`created: 2026-07-09`, no origin. `supporting-docs.manifest.yaml` records
`"origin_path": "ideation/staging/semantic-health-sweep"`,
`"source_revision": "18fcf803470ba4e43aace476cda43eda1ac9ddf0"`,
`"transitioned_at": "2026-07-09"` (packaged/archived 2026-07-12).

**`archive/2026-07-12-define-human-escalation-contract`** —
classification: `ad_hoc`. Applied.

Evidence: existing `.openspec.yaml` had only `schema: spec-driven` /
`created: 2026-07-12`, no origin. No supporting-docs manifest. `git log`
traces creation to commit `aacd932` "Propose define-human-escalation-contract",
Brett Heap, 2026-07-12 12:55:14 UTC, which "Resolves the dangling HR
consultation carried since the original canonical roles doc" — a direct
fix, not staged material; archived the same day (`code_surface: none`) per
commit `5d95fdf`.

**`archive/2026-07-12-exclude-worktrees-from-notebook-projection`** —
classification: already-compliant. Not touched.

Evidence: `.openspec.yaml` already declares
`origin: {kind: ad_hoc, id: openxFactory:adhoc:2026-07-12-notebook-projection-worktree-scope,
reason: "Nightly-sync-blocking scan defect ... fixed directly on Brett's
instruction; no staged source material exists", approved_by: Brett,
approved_on: 2026-07-12}`.

**`archive/2026-07-13-align-avatar-first-ui-standard`** — classification:
already-compliant. Not touched.

Evidence: `.openspec.yaml` already declares
`origin: {kind: ad_hoc, id: openxFactory:adhoc:2026-07-10-avatar-first-ui-standard-split,
reason: "Split from define-avatar-client-runtime by explicit user
approval", approved_by: Brett, approved_on: 2026-07-10}`.

**`archive/2026-07-13-clarify-avatar-revocation-client-enforced`** —
classification: `ad_hoc`. Applied (created `.openspec.yaml`; none existed).

Evidence: no `.openspec.yaml` and no supporting-docs manifest. `git log`
traces creation to commit `ba322bf` "Propose clarify-avatar-revocation-client-enforced
(ACR-005 disposition)", brettheap, 2026-07-12 17:10:03 UTC — the commit
message states this disposes "the F0-D revocation finding (kernel-owner
ruling 2026-07-12)" directly from `qualify-avatar-brokered-call-feasibility`
evidence; `proposal.md` cites that change's evidence file directly, not a
staging folder. Archived 2026-07-13 via commit `44f523b` ("Archive 3
realized avatar changes").

**`archive/2026-07-13-define-avatar-client-contract-kernel`** —
classification: already-compliant. Not touched.

Evidence: `.openspec.yaml` already declares
`origin: {kind: staged, id: openxFactory:staging:avatar-client, path: ideation/staging/avatar-client}`.

**`archive/2026-07-13-implement-avatar-reference-runtime`** —
classification: already-compliant. Not touched.

Evidence: `.openspec.yaml` already declares
`origin: {kind: ad_hoc, id: openxFactory:adhoc:2026-07-10-avatar-reference-runtime-split,
reason: "Split from define-avatar-client-runtime by explicit user
approval", approved_by: Brett, approved_on: 2026-07-10}`.

## Active changes (not touched)

Task 3.2 excludes active changes. All six already declare a compliant
origin and required no action:

- `add-cross-factory-ideation-routing` — `staged`,
  `openxFactory:staging:ideation-routing`.
- `add-document-cataloging` — `ad_hoc`,
  `openxFactory:adhoc:2026-07-09-document-cataloging-split`.
- `add-ideation-cross-reference-readiness` — `staged`,
  `openxFactory:staging:ideation-cross-reference-readiness`.
- `add-ideation-dashboard` — `staged`,
  `openxFactory:staging:ideation-dashboard`. Owned by another operator's
  lane; already compliant, so no block was proposed or applied.
- `add-proposal-origin-contract` (this change) — `staged`,
  `openxFactory:staging:proposal-origin-contract` — the self-application
  acceptance proof described in `proposal.md`/`design.md`.
- `qualify-avatar-brokered-call-feasibility` — `ad_hoc`,
  `openxFactory:adhoc:2026-07-10-avatar-brokered-call-feasibility-split`.
  Owned by another operator's lane; already compliant, so no block was
  proposed or applied.

## Summary

- Archived changes: 27 total. 4 already-compliant (not touched); 1 bootstrap
  amendment applied (task 3.1); 22 backfilled (task 3.2) — 12 `staged`, 10
  `ad_hoc`.
- Active changes: 6 total, all already-compliant; none touched, per scope.
- No staging history was fabricated: every `staged` classification cites a
  recorded `origin_path` in a supporting-docs manifest (or, for this
  change's own self-application, the staged topic's `Staging ID:` header);
  every `ad_hoc` classification cites either an explicit ad-hoc statement in
  the packet's own supporting docs, or dated git history predating the
  2026-07-08 introduction of the `ideation/staging` pipeline, or a direct
  fix/split documented in the change's own proposal/tasks text.
