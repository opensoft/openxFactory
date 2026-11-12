---
code_surface: openxFactory
target_release: deferred-allocation
sequenced_after: [implement-private-connectivity-binding]
---

# Proposal: Register private connectivity pilot evidence references

Status: ratified
Ratified: 2026-11-10 by Brett Heap. [Ratification record](review/ratification-2026-11-10.md)
Kind: proposal
Proposed: 2026-11-10

## Why

The required doc-health check on PR #1303 reports that feature 040's evidence records carry commit references outside the shared pin register's declared inventory. T001 authorizes only the feature checker and its self-tests; it does not authorize changing the shared reader or its measured census.

## What Changes

- Authorize narrowly scoped pin-class declarations for `specs/040-private-connectivity/evidence/*.json`, with explicit repository ownership and reachability treatment for each reference family.
- Keep local derivation pins subject to existing reachability obligations. Classify foreign-owner references explicitly and keep original observation references distinct from current candidates.
- Add regression coverage and update only measured census expectations that the additional declarations actually change.
- Record this additional authority in T001 and hand implementation to feature 040 before accepting its final gate.

## Capabilities

### New Capabilities

None. This is an inventory completion in existing tooling; `skip_specs: true` records that no normative requirement changes.

### Modified Capabilities

None. The existing declared-coverage and reachability requirements remain in force.

## Impact

Proposed additional files: `scripts/doc_health/pin_class.py`, directly affected cases in `tests/doc-health/test_pin_reachability.py`, feature 040 evidence records and self-tests, and generated ledger/README records required by repository governance. No global exclusion, required-check removal, pin-floor advance, contract release cut, or runtime scope expansion is authorized. All six implementation PRs remain drafts. Human G4 sign-off remains required.

## Implementation placement note

The measured standing-census assertion is in `tests/doc-health/test_sentinel_vocabulary.py`, not the initially named sibling test module. The authorized measured-census update applies there; the shared reader continues to use existing declarations and the coverage sweep remains intact. This is a placement correction within the ratified narrow repair.
