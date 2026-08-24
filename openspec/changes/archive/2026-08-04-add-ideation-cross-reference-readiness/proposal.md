code_surface: openxFactory, codexFactory, xFactory, omnigent-install
target_release: implemented
Status: ratified
Ratified: 2026-07-12 by Brett — record: the commit `1efa575`, "Archive exclude-worktrees-from-notebook-projection; record ratifications", whose body opens "Brett ratified all three active changes 2026-07-12" and names this one — "add-proposal-origin-contract and add-ideation-cross-reference-readiness: ratified as admitted intent; both carry code surfaces so they stay active until realization evidence lands". The date recorded is the ratification's, 23 days before this change's own archive act (`7bf79c6`, 2026-08-04, which promoted the delta into `openspec/specs/ideation-cross-reference/spec.md` and `openspec/specs/doc-health/spec.md`) — exactly the ratified-then-realized gap that commit describes. Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".

## Why

Nothing in the family clusters related ideation material by subject and
scores whether a cluster is mature enough to formalize. `ideation-routing`
resolves ownership and destination; `document-cataloging` tags documents;
`domain-to-neutral-promotion` triggers on one specific maturity case
(cross-domain convergence); `doc-health` checks prose-vs-spec hygiene. None
answers: *is this cluster of related ideas — across brainstorm, staging, and
archive — mature enough, with a viable path to extend something already
promoted, that someone should be asked to open a proposal?* All seven design
questions were decided by Brett on 2026-07-12 (recorded in the supporting
document's decision record).

## What Changes

- Add the `ideation-cross-reference` capability: one unified cross-stage
  topic index at the openxFactory ideation level (`ideation/cross-reference.md`,
  stage column), clustering material by the `Topics:` and
  `Target capabilities:` header fields now and folding in
  `document-cataloging` tags once that capability lands — never blocking on
  the catalog. `staging/INDEX.md` remains the separate staged-file inventory.
- Require every topic entry to carry an extension-fit note that names the
  specific promoted spec or capability the cluster would extend; an
  archive-folder pointer alone is a finding.
- Add the three-tier Hermes readiness panel: independent 1-10 scores from
  the domain tier (owning Domain Hermes), the company tier (openxFactory
  ratify authority), and the project tier (engineering buildability — could
  codexFactory's feature decomposition turn the cluster into a buildable
  Spec Kit feature DAG today). Each score carries the full
  organizer/cataloger evidence contract; no new rationale format.
- Gate on the minimum: a topic is flagged "propose for authorization" only
  when all three tier scores are >= 8, and the flag is always a
  recommendation with `pending_review` disposition — never an autonomous
  action. Wide inter-tier spread is surfaced as a flagged conflict even
  below threshold.
- Bound execution: the pass is non-mutating over source content — it writes
  only the index and its evidence artifacts; archived material is read-only
  reference for the fit check.
- Add the nightly ideation readiness lane to `doc-health`, running after the
  deterministic pass on the same inventory snapshot, report-only in v1; the
  doc-health enumeration delta is declared relative to the
  `add-proposal-origin-contract` outcome (proposed together, in that order)
  per the ordered-deltas rule.
- Pair the contract with a codexFactory worker realization following the
  ideation-routing / document-cataloging two-repo split, deliberately reusing
  their tag and evidence contracts rather than inventing new ones.

## Capabilities

### New Capabilities

- `ideation-cross-reference`: Defines the unified cross-stage topic index,
  cluster membership sources, extension-fit citation strictness, the
  three-tier Hermes readiness panel with the reused evidence contract, the
  minimum-score recommendation gate with conflict flagging, the non-mutating
  execution bound, and nightly snapshot-consistent scheduling.

### Modified Capabilities

- `doc-health`: Adds the ideation readiness lane beside the semantic sweep
  and the document-cataloger and ideation-organizer lanes, including the
  archive-pointer-only extension-fit finding; deterministic-family
  enumeration updated relative to the proposal-origin change's outcome.

## Impact

- **openxFactory:** the cross-reference index contract, schema and examples,
  a strict index validator, and ideation guidance updates.
- **codexFactory:** the readiness-scorer worker (versioned prompt, three-tier
  scoring, evidence-contract validation), index generation, and tests;
  implementation follows the ideation-routing and proposal-origin
  realizations.
- **xFactory aggregation:** nightly lane dispatch after the deterministic
  pass and report links to the index and evidence.
- **omnigent-install:** one bounded read-only readiness-scorer profile
  reusing the existing document-analysis host pattern; no new host class.
- **Compatibility:** source documents are never edited, moved, or promoted
  by this capability; recommendations only ever enter the existing
  human-disposed review flow.
