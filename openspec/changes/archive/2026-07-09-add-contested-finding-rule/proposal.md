# Add Contested Finding Rule

Status: ratified
Ratified: 2026-07-09 — record: the archive act, commit `4781071` "Archive add-contested-finding-rule", which applied this change's spec delta into `openspec/specs/doc-health/spec.md`; a change whose spec deltas have PROMOTED is ratified by construction, the derivation `bdd09c2` records and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites. The commit body records the promotion in words: "Sync both modified requirements into the canonical doc-health spec", "Active changes: none. Strict 11/11". Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".

## Why

Doc-health report #1's first resolution session auto-fixed a compliant
document: the checker's location family flagged the candidate register
(`Status: staged` in `docs/`) by implementing a staged fragment's narrow
wording over the promoted spec — which never required a staged-location
check at all and explicitly allows registers as an organized-state home —
and the session changed the register's status to clear the finding
(ff5b06b). Two gaps enabled this: check families can drift beyond their
contract, and the contract has no distinction between a mechanical defect
and a finding whose "fix" changes a deliberate decision.

## What Changes

- Classify every finding `auto-fixable` or `contested`; contested findings
  are report-and-escalate only, and a contested finding that disappears via
  an uncited state change becomes a new "uncited resolution" error —
  the regression diff enforces the process rule.
- Make staged-location checking spec-backed and correctly scoped: a
  `staged` doc outside `ideation/staging/` is a finding unless it is a
  candidate register (`Kind: register`).
- Bind check families to promoted spec wording explicitly; fragments are
  inputs, not check definitions.
- Instance repair, sequenced: fix the codexFactory location family and add
  the register fixture FIRST, then restore the register to `Status: staged`.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `doc-health`: check families bound to promoted wording; lifecycle
  conformance gains the register-aware staged-location rule; findings gain
  resolution classes with contested-resolution enforcement.

## Impact

- codexFactory: location family fix + fixtures + classification field in
  the finding type and report (cross-repo tasks).
- openxFactory: register restored to `staged`; fix-plan fragment updated
  (document-lifecycle needs no delta — its text already allows registers).
- Future reports gain the resolution-class column; prior reports are not
  rewritten.
