# Tasks: Add Contested Finding Rule

## 1. Checker Fix (cross-repo: codexFactory)

- [x] 1.1 Fix fam_location_conformance: staged docs outside
      `ideation/staging/` are findings only when not `Kind: register`.
- [x] 1.2 Add fixture: a register with staged status outside staging that
      must produce no location finding.
- [x] 1.3 Add resolution class (`auto-fixable`/`contested`) to the finding
      type, per-family defaults, and the report/plan item shape.
- [x] 1.4 Implement the uncited-resolution regression rule for contested
      findings.

## 2. Instance Restore (openxFactory, after 1.x)

- [x] 2.1 Restore the candidate register to `Status: staged`, citing this
      change; run the location family to confirm no finding.
- [x] 2.2 Update the contested-findings fix-plan fragment: exit satisfied;
      note the no-document-lifecycle-delta correction.

## 3. Validation

- [x] 3.1 `OPENSPEC_TELEMETRY=0 openspec validate add-contested-finding-rule --strict`
      and `--all --strict` pass.
- [x] 3.2 codexFactory doc-health tests pass including the new fixtures.
