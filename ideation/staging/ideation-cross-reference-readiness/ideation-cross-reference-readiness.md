# Staged: Ideation Cross-Reference Readiness Index

Status: staged
Kind: architecture
Summary: Defines a topic-indexed cross-reference spanning brainstorm, staging,
and archived material, scored 1-10 for staging readiness by three independent
Hermes-tier reviewers (engineering-buildability, company/openxFactory, domain),
where minimum score >= 8 triggers a "propose for authorization" recommendation
— never an autonomous action.
Topics: ideation-cross-reference, readiness-scoring, hermes-review-panel, extension-fit, doc-health, staging-readiness
Repository context: openxFactory (contract-level, cross-factory topic)
Staging ID: openxFactory:staging:ideation-cross-reference-readiness
Source: [Ideation Cross-Reference Readiness Index — Brainstorm](../../brainstorm/ideation-cross-reference-readiness.md),
design session 2026-07-12; all seven open questions decided by Brett
2026-07-12 (decisions recorded below and inline in the brainstorm).
Target capabilities: `ideation-cross-reference` (ADDED) and `doc-health`
(MODIFIED — new nightly readiness-scoring lane).

## Problem

Nothing in the family clusters related ideation material by subject and scores
whether a cluster is mature enough to formalize. `ideation-routing` resolves
ownership and destination; `document-cataloging` tags documents;
`domain-to-neutral-promotion` triggers on one specific maturity case
(cross-domain convergence); `doc-health` checks prose-vs-spec hygiene. None
answers: *is this cluster of related ideas mature enough — with a viable path
to extend something already promoted — that someone should be asked to open a
proposal?*

## Decided Contract

### Cross-reference index

One unified cross-stage index file at the `ideation/` level (working name
`ideation/cross-reference.md`), organized by topic/tag with a stage column —
clusters span brainstorm, staging, and archive by design, so a per-folder file
misfits. `staging/INDEX.md` remains the separate staged-file inventory; the
two files do not overlap in purpose.

- Cluster membership bootstraps from the `Topics:` (brainstorm and staging)
  and `Target capabilities:` (staging) header fields already in place;
  `document-cataloging` tags fold in once that capability lands. Do not block
  on the catalog.
- Each topic entry carries an **extension-fit note** that MUST name the
  specific promoted spec or capability the cluster would extend; a pointer to
  an archived change folder alone is a doc-health finding.
- Each topic entry carries three independent 1-10 readiness scores, one per
  Hermes tier, each with the **full evidence contract** already used by the
  `document-cataloger` and `ideation-organizer` (source revision, passage
  hash, confidence, alternatives, `pending_review` disposition) — reuse, not
  a new rationale format.

### Hermes-tier scoring panel

- **Domain layer** — the owning DomainxFactory's Domain Hermes (professional,
  regulatory, domain-evidence expertise).
- **Company layer** — openxFactory ratify authority (cross-factory,
  whole-product-family lens).
- **Project layer** — engineering buildability: codexFactory's engineering
  lens, i.e. could `feature-decomposition` turn this cluster into a buildable
  Spec Kit feature DAG today. Aggregation/composition concerns stay with the
  company lens.

### Readiness gate

A topic is flagged **"propose for authorization"** — a recommendation, never
an autonomous action — only when the **minimum** of the three tier scores is
>= 8, so no single tier can be outvoted into silence. A wide spread between
tiers is surfaced as a flagged conflict even below threshold.

### Execution

- Non-mutating over source content: the pass only writes the cross-reference
  index file itself; it never edits, moves, promotes, or deletes a brainstorm,
  staging, or archived document. Archived material is read-only reference for
  the extension-fit check.
- Re-run: a new nightly lane in the doc-health pipeline, beside the
  deterministic checks and the semantic sweep; reports land with the nightly
  corpus-health reports.

## Decision Record (Brett, 2026-07-12)

1. Project-layer reviewer: engineering-buildability lens (codexFactory
   `feature-decomposition`).
2. Score-combination rule: minimum of the three tiers >= 8.
3. Index placement: one unified cross-stage file at `ideation/` level with a
   stage column; `staging/INDEX.md` stays the file inventory.
4. Re-run trigger: nightly doc-health lane.
5. Tag source of truth: bootstrap from `Topics:`/`Target capabilities:`
   headers now; fold in `document-cataloging` tags when it lands.
6. Per-tier rationale: full organizer/cataloger evidence contract.
7. Extension-fit citation: must name the specific promoted spec/capability.

## Required Deltas and Tests

- ADDED `ideation-cross-reference`: index schema (topic entry, stage column,
  per-tier score + evidence contract, extension-fit note), the three-tier
  review contract, the min>=8 recommendation gate, the spread-conflict flag,
  and the non-mutating execution bound.
- MODIFIED `doc-health`: the nightly readiness-scoring lane and the
  archive-pointer-only extension-fit finding.
- Tests: gate fires only at min>=8; spread conflict flagged below threshold;
  recommendation is advisory (no state transition performed); index pass
  rejects any write outside the index file; tag bootstrap reads both header
  fields; evidence contract validates against the existing organizer/cataloger
  schema.

## Exit

Create one OpenSpec change, recommended ID
`add-ideation-cross-reference-readiness`, defining the cross-reference/scoring
schema and the Hermes-tier review contract, paired with a codexFactory delta
for the worker implementation — the same two-repo split pattern as
`ideation-routing` and `document-cataloging`, whose tag and evidence contracts
this design deliberately reuses rather than re-invents. At the proposal gate
this file moves into that change's `supporting-docs/`, preserving the staging
origin above.
