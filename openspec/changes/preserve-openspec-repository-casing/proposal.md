---
Status: draft
Proposed: 2026-11-11
code_surface: openxFactory — scripts/validate-openspec-cli-pin.py and tests/openspec_cli_pin; governed maintenance and generated ledger row only
target_release: implemented — source tooling compatibility; no bundle, tag or runtime activation
---

## Why

The authorized factory casing migration changes GitHub operational names while
retaining repository IDs and frozen contract/provenance identifiers. The
OpenSpec reader currently compares disposition repository names literally, so
codeXfactory cannot apply the four existing codexFactory exceptions at its
selected immutable factory baseline.

## What Changes

- Recognize only the approved spelling pairs `codexFactory` / `codeXfactory`
  and `openxFactory` / `openXfactory` when selecting disposition scope.
- Preserve exact item/path/finding matching, duplicate refusal, whole-corpus
  staleness detection, printed actual identity and every frozen exception byte.
- Backport the reader correction onto selected source
  `93d13d6c8e14008c0b66adea65756d106fef6227`, so the domain does not inherit later
  exception retirements or unrelated contract changes.
- Implement and verify through [Speckit 042](../../../specs/042-openspec-repository-casing/plan.md).
  The qualification-preparation consumer follows by its own reviewed immutable
  pin hop and existing browser identity generator.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `neutral-product-pin`: explicit compatibility for the approved repository
  spelling pairs without weakening disposition scope or retention.

## Impact

This is the narrow maintenance correction requested by Brett Heap: "Go ahead
and fix the codeXfactory OpenSpec naming mismatch through the governed process,
then open the qualification preparation PR and run CI and Codex review. Keep
feedback deferred and don't replay either blocked write."
The existing cross-repository naming authority is xFactory's
`standardize-factory-repository-casing`, authorized 2026-11-11. Verified GitHub
repository IDs are 1281785369 for the codeXfactory repository and 1275848622 for
openXfactory. No grant, exception, source pin, remote configuration, published
contract or archived packet is rewritten here. No model or provider runtime is
activated. The default-branch PR carries the fix forward while the immutable
backport head preserves the consumer's selected contract baseline.
