# Add Document Lifecycle Vocabulary

Status: ratified
Ratified: 2026-07-09 — record: the archive act, commit `a195244` "Archive five implemented OpenSpec changes and promote capabilities", which applied this change's spec delta into `openspec/specs/document-lifecycle/spec.md`; a change whose spec deltas have PROMOTED is ratified by construction, the derivation `bdd09c2` records and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites. One archive act closed five changes; its body names this one's promotion, "document-lifecycle with the prose-tagging modification applied". Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".

## Why

The xFactory family governs itself through documents, but document state is
asserted in free-form prose rather than earned through gates. A scan on
2026-07-08 found 77 of 112 governance docs carry a `Status:` header using
roughly 25 distinct uncontrolled values; 14 docs self-declare
"shared xFactory standard" without any ratifying OpenSpec change. Three
partial state vocabularies exist (the ideation draft convention, the
domain-neutralization candidate register, and OpenSpec change states) with no
spine connecting them.

This blocks the planned doc-health pipeline: an automated checker cannot
verify "does this document's status match its gate history" until the states
are canonical. The vocabulary is the keystone; tagging, staging, nightly
health reporting, and the promotion process all reference it.

## What Changes

- Define one canonical document lifecycle: `captured -> organized -> proposed
  -> ratified -> implemented -> promoted -> adopted`, with `superseded` and
  `retired` as terminal transitions and `rejected`/`deferred` as exits.
- Define a controlled `Status:` header taxonomy that projects lifecycle states
  onto documents, separating document *state* from document *kind*.
- Restrict status claims: no document may claim standard status unless a
  promoted spec or contract backs it.
- Ratify the ideation work area convention (`ideation/brainstorm/`,
  `ideation/staging/`, and their gates) as the sanctioned pre-proposal path.
- Ratify the explicit-delta rule: prose that changes promoted policy must be
  expressed as an OpenSpec delta or carry an explicit supersedes marker;
  contradiction is legal only inside `ideation/brainstorm/`.
- Ratify the domain-to-neutral promotion process and align the candidate
  register statuses with the lifecycle vocabulary.

## Capabilities

### New Capabilities

- `document-lifecycle`: canonical lifecycle states, controlled status
  taxonomy, ideation convention, explicit-delta rule, and promotion process
  binding for all governance documents across openxFactory and every
  DomainxFactory.

### Modified Capabilities

- None. (`repo-boundary-governance` and `shared-contract-ownership` placement
  rules are unchanged; this change governs how documents move, not where they
  live.)

## Impact

- openxFactory: `docs/domain-to-neutral-promotion-process.md` and
  `docs/domain-neutralization-candidate-register.md` move from draft to
  ratified; `ideation/README.md` loses its draft caveat; a new
  `docs/document-lifecycle.md` states the vocabulary and taxonomy.
- All repos: existing `Status:` headers migrate to the controlled taxonomy in
  a follow-up sweep (grandfathered until swept; the mapping table lives in
  this change's `design.md`).
- Doc-health pipeline (planned): the deterministic pass gains its core check —
  status validity and status-vs-gate-history conformance.
- No runtime, contract schema, or credential impact.
