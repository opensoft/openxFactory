## 1. Evidence and source verification

- [x] 1.1 **DONE 2026-09-01 —** captured in `evidence/current-publications-2026-09-01.md` with primary URLs, publication/version, steward, term kind, verification date, and confidence.
- [x] 1.2 **DONE 2026-09-01 —** captured the SFIA licensing conflict and Brett's explicit operator override as separate facts; the official source finding remains unchanged in the evidence record.
- [x] 1.3 **DONE 2026-09-01 —** captured APQC PCF 8.0's attribution condition and separated PCF hierarchy reuse from process-definition reuse.

## 2. Registry implementation

- [x] 2.1 **DONE 2026-09-01 —** added distinct `itil5` while preserving the existing `itil4` record.
- [x] 2.2 **DONE 2026-09-01 —** updated SFIA to current SFIA 9 and added the explicit unverified operator override selected by Brett.
- [x] 2.3 **DONE 2026-09-01 —** reconciled APQC PCF 8.0 metadata and added the IT-process crosswalk scope plus attribution requirement.
- [x] 2.4 **DONE 2026-09-01 —** retained descriptive-only semantics; no framework hierarchy, practice text, skill definitions, or process definitions were copied.

## 3. Validation and regression coverage

- [x] 3.1 **DONE 2026-09-01 —** `scripts/standards_body_registry.py` checks current-publication metadata completeness for the amended entries.
- [x] 3.2 **DONE 2026-09-01 —** validator checks override completeness and requires the explicit unverified status.
- [x] 3.3 **DONE 2026-09-01 —** registry regression tests and the existing unknown-body negative fixture cover the selected positive and negative paths.
- [x] 3.4 **DONE 2026-09-01 —** registry tests (5 passed) and `scripts/validate-omnigent-contracts.py` both pass with zero findings.

## 4. Consumer handoff

- [x] 4.1 **DONE 2026-09-01 —** published `handoff/opsx-overlay-current-standards.md` naming `itil5`, SFIA 9's
      unverified status, and APQC PCF 8.0 as the only current-body inputs.
- [x] 4.2 **DONE 2026-09-01 —** authorized the separate OpsxFactory change to evaluate all nine worker
      classes against APQC IT-process terms without forcing a match.
- [x] 4.3 **DONE 2026-09-01 —** recorded the missing SFIA written permission as an explicit follow-up
      owned by the operator/legal-review seat.

## 5. Release and archive

- [x] 5.1 **DONE 2026-09-01 —** no contract release bundle is owed; this amendment changes policy metadata and evidence only.
- [x] 5.2 **DONE LOCALLY 2026-09-01 —** the registry amendment is integrated in
      the working tree and the required registry and Omnigent validations pass.
      Publication as a Git commit/merge remains an operator action; no commit or
      push is performed by this session.
- [x] 5.3 **DONE LOCALLY 2026-09-01 —** the packet is ready to archive with its
      evidence and OpsxFactory handoff preserved.
