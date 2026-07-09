# Refine Promotion Provenance

## Why

The promoted `document-lifecycle` capability binds promotion to the
documented process but leaves three operational questions open (staged in
`ideation/staging/promotion-refinements/`): who drafts neutralizations, how
promotion provenance stays machine-readable, and which copy is authoritative
mid-promotion. The first DTN candidates (DTN-001/002/003, all P0) cannot
execute cleanly while these are unanswered — an executing session would have
to invent answers mid-change.

Scope note: the staged fragment leaned toward folding these into the first
DTN execution change. This proposal reverses that with rationale: with all
prior changes archived there is no delta-stacking hazard, the refinements
are pure process policy (no candidate-specific content), and answering them
first means every DTN change starts from settled rules rather than carrying
process debate inside a promotion.

## What Changes

- Assign neutralization drafting: codexFactory doc-engineering workers draft,
  the originating domain's Hermes reviews and approves the surrender —
  the same execution/authority split used everywhere else in the family.
- Make promotion provenance machine-readable: optional `promoted_from` and
  `specializes` fields on the domain stack contract, so the doc-health run
  can verify adopted candidates against declared lineage.
- Define mid-promotion authority: the domain-local copy remains authoritative
  until the re-pin gate completes; the candidate register entry's status is
  the tiebreaker consumers check.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `document-lifecycle`: the Promotion process binding requirement gains
  drafting ownership, provenance fields, and mid-promotion authority rules.

## Impact

- openxFactory: `docs/domain-to-neutral-promotion-process.md` gains the three
  rules (explicit supersedes-free update — the doc is `standard`, so the
  edits land only via this change); `contracts/schemas/xfactory-domain-stack.schema.yaml`
  gains two optional fields; contract CHANGELOG entry per versioning policy.
- Domain repos: no immediate change; fields are optional until first use.
- Doc-only change; archives on doc landing.
