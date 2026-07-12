# Ideation Cross-Reference Readiness Index — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Proposes a topic/tag-indexed cross-reference file spanning
brainstorm, staging, and archived material, scored 1-10 for staging readiness
by three independent Hermes-tier reviewers (project, company/openxFactory,
domain), with a minimum-score->=8 gate triggering a recommendation — not an
action — to open an OpenSpec proposal.
Topics: ideation-cross-reference, readiness-scoring, hermes-review-panel, extension-fit, staging-readiness
Repository context: openxFactory (contract-level, cross-factory topic)
Captured: 2026-07-12
Participants: Brett Heap, Claude (design session)

## Problem

Nothing in the family currently clusters related ideation material by subject
and scores whether that cluster is mature enough to formalize. The adjacent
capabilities each solve a different piece:

- `ideation-routing` (active, unimplemented) recommends WHO owns an idea and
  WHERE it should go — ownership and destination, not maturity.
- `document-cataloging` (active, unimplemented) tags and classifies documents
  but never cross-references them into topic clusters or scores readiness.
- `domain-to-neutral-promotion` (organized brainstorm) defines trigger signals
  for one specific maturity case — the same concept appearing independently in
  two or more domain repos — but has no general cross-topic scoring mechanism.
- `doc-health-pipeline` (organized brainstorm) checks prose-vs-spec health and
  tag hygiene, not idea maturity.

None of them answer: *is this cluster of related ideas, across brainstorm and
staging, mature enough — and does it have a viable path to extend something
already promoted — that someone should be asked to open a proposal?*

## Design sketch

### Cross-reference index

A new file, e.g. `ideation/brainstorm/INDEX.md` (sibling to the existing
`ideation/staging/INDEX.md`), organized **by topic/tag**, not by file:

- Each topic entry lists every related doc across `ideation/brainstorm/`,
  `ideation/staging/`, and archived supporting-docs, drawn from the `Topics:`
  header field (brainstorm), `Target capabilities:` (staging), and eventually
  `document-cataloging` tags once that capability lands.
- Each topic entry carries an **extension-fit note**: does a promoted,
  archived capability already exist that this idea would extend, and how —
  citing the specific promoted spec/capability, not just a link to the
  archive folder. This is a fit-check against current architecture, distinct
  from the maturity score below.
- Each topic entry carries **three independent readiness scores, 1-10**, one
  per Hermes tier (see below), each with a short rationale — mirroring the
  evidence-backed-recommendation contract already used by the
  `document-cataloger` and the `ideation-organizer` (rationale, evidence,
  confidence, `pending_review` disposition), just per-tier instead of a
  single score.

### Hermes-tier scoring panel

Three independent reviewers score every topic cluster from their own
expertise, mapped as far as possible onto authorities already named in the
family's designs:

- **Domain layer** -> the owning DomainxFactory's Domain Hermes. Already
  named ("approves surrender of domain meaning") with professional,
  regulatory, and domain-evidence expertise.
- **Company layer** -> openxFactory ratify authority. Already named
  ("approves neutral content") — the cross-factory, whole-product-family
  lens.
- **Project layer** -> no existing named match; see open questions.

### Readiness gate

A topic is flagged **"propose for authorization"** — a recommendation, never
an autonomous action — only when the **minimum** of the three scores is >= 8,
so no single tier can be outvoted into silence by the other two. A wide
spread between tiers (e.g. company high, domain low) is surfaced as a flagged
conflict even when it stays below threshold, the same way the
domain-to-neutral-promotion design already treats domain/neutral disagreement
as meaningful signal rather than noise to average away.

### Non-mutating scope

Like every other Omni worker in this family (`document-cataloger`,
`ideation-organizer`), this pass is non-mutating over source content. It only
writes and updates the cross-reference index file itself; it never edits,
moves, promotes, or deletes a brainstorm, staging, or archived document.
Archived material is read-only reference for the extension-fit check, never
something to merge or rewrite.

## Relationship to existing designs

- `ideation-routing`: orthogonal. Its organizer resolves ownership/
  destination; this index resolves whether a cluster is mature enough to
  formalize at all. A topic can be routing-resolved and still sit below the
  readiness threshold, or vice versa.
- `document-cataloging`: supplies the tag/topic taxonomy this index should
  reuse rather than reinvent — the same reuse pattern the ideation-organizer
  already uses for catalog signals.
- `domain-to-neutral-promotion`: its cross-domain trigger signal is one
  specific case of "this topic cluster looks mature"; this index generalizes
  that signal beyond cross-domain convergence.
- `doc-health-pipeline`: natural home for scheduling this pass as a new lane
  alongside the deterministic checks and the semantic sweep.

## Open questions

- **Project-layer definition**: an engineering-buildability lens (could
  codexFactory's `feature-decomposition` turn this into a Spec Kit feature
  DAG), the xFactory aggregation-repo composition/pinning/release-assembly
  lens, or something else entirely?
- **Score-combination rule**: is "minimum of the three >= 8" the right gate,
  or should scores combine differently (average, majority, all-must-agree-
  within-N-points)?
- **Index placement**: a peer file `ideation/brainstorm/INDEX.md` alongside
  `ideation/staging/INDEX.md`, or one unified index spanning both stages with
  a stage column?
- **Re-run trigger**: scheduled nightly like doc-health, or on every new or
  materially-changed brainstorm commit like the ideation-organizer's
  selection rule?
- **Tag source of truth**: bootstrap from the `Topics:`/`Target capabilities:`
  header fields already in place today, with `document-cataloging` tags
  folded in once that capability lands, or wait for the catalog first?
- **Per-tier rationale format**: the same full evidence contract shape as the
  existing organizer/cataloger (source revision, passage hash, confidence,
  alternatives, `pending_review`), or a lighter-weight version scoped to this
  index?
- **Extension-fit citation strictness**: must a fit note name a specific
  promoted spec/capability, or is a pointer to the archived change folder
  sufficient?

## Exit

Organize into a staged topic once the open questions above have
recommendations. Likely exits as an openxFactory contract change defining the
cross-reference/scoring schema and the Hermes-tier review contract, paired
with a codexFactory delta for the worker implementation — following the same
two-repo split pattern as `ideation-routing` and `document-cataloging`.
