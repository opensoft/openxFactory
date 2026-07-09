# Add Contested Finding Rule

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
