# Add Doc-Health Contract

Status: ratified
Ratified: 2026-07-09 — record: the archive act, commit `a195244` "Archive five implemented OpenSpec changes and promote capabilities", which applied this change's spec delta into `openspec/specs/doc-health/spec.md`; a change whose spec deltas have PROMOTED is ratified by construction, the derivation `bdd09c2` records and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites. One archive act closed five changes; its body records the promotion in words: "Sync deltas into canonical specs ... move all five change folders to archive/2026-07-09-*". Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".

## Why

The xFactory family governs itself through documents, and the
`document-lifecycle` capability now defines the states, gates, status
taxonomy, explicit-delta rule, and canonical `xspec:` marker grammar those
documents must honor — but nothing checks any of it. There is no CI on
xFactory, openxFactory, or any DomainxFactory; the per-repo validators run
only when someone remembers, and no tool verifies status-vs-gate-history
conformance, marker hygiene, pin drift, or projection drift. Three staged
fragments in `ideation/staging/doc-health-checks/` (`nightly-run-shape.md`,
`status-check-rules.md`, `tag-hygiene-rules.md`) carry the organized
claims. Their declared exit is two OpenSpec changes; this is the first —
the domain-neutral contract. The codexFactory implementation change follows
after this one ratifies.

## What Changes

- Add a new `doc-health` capability defining the deterministic check
  contract for the family's governance corpus:
  - twelve check families: status validity, standard backing, ratified
    provenance, succession integrity, location conformance, record
    immutability, staged/candidate aging, register-lifecycle consistency,
    tag hygiene (enforcing the `xspec:` grammar the `document-lifecycle`
    capability defines — by reference, never restated), submodule pin
    drift, contract-copy drift, and notebook projection drift.
  - the report contract: a dated Markdown report plus a ranked plan in
    which every finding is a ready-to-stage work item; headline metric is
    canon share by words.
  - finding severity levels (`critical | error | warning | info`) and the
    regression rule: new critical or error findings versus the previous
    report open an issue.
  - contract-level aging threshold defaults so reports stay comparable
    across runs.
  - the ownership split: openxFactory owns the contract and report schema,
    codexFactory owns the implementation, the xFactory aggregation repo
    hosts the nightly runner, and each domain factory keeps approval
    authority over its own content.
- Add `docs/doc-health.md` as the ratified contract document.
- Hand an implementation-requirements note to the staged queue for the
  follow-on codexFactory change.

## Archive Discipline Note

This contract change is **doc-only**: its implementation is prose, so it
archives when the documents land, per current practice. The follow-on
codexFactory implementation change will carry the family's first real code
surface (scripts, workflow, report generator); whether that change archives
on doc-landing or on code realization is deliberately NOT decided here — it
is the pilot case for the brownfield release-flow question captured in
`ideation/brainstorm/openspec-speckit-release-flow.md` (Status: brainstorm,
non-normative), and its archive discipline SHALL be decided when it is
proposed.

## Capabilities

### New Capabilities

- `doc-health`: the deterministic health-check contract — check families,
  report and plan schema, severity and regression rules, aging thresholds,
  and the ownership/hosting split — for the whole factory family's
  governance corpus.

### Modified Capabilities

- None. Tag hygiene enforces the `document-lifecycle` marker grammar by
  reference; that capability's requirements are unchanged.

## Impact

- openxFactory: new `docs/doc-health.md` (Status: ratified, citing this
  change); README doc index gains the link; the three
  `ideation/staging/doc-health-checks/` fragments move through the proposal
  gate (reference this change); a new staged handoff fragment scopes the
  implementation change.
- xFactory aggregation repo (on implementation, not now): will host
  `health/reports/` and the nightly workflow caller.
- codexFactory (on implementation, not now): will own the checker scripts,
  reusable workflow, and report generator.
- No runtime, contract schema, or credential impact from this change
  itself; it defines the contract the implementation change builds against.
