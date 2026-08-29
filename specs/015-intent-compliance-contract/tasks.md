# Tasks: Intent Compliance Contract

## Phase 1: Setup

- [x] T001 Record ratification and Speckit handoff in `openspec/changes/add-standing-policy-compliance-contract/` and `specs/015-intent-compliance-contract/`
- [x] T002 [P] Create the family directory and README skeleton in `contracts/intent-compliance/README.md`
- [x] T003 [P] Create focused test directories in `tests/intent-compliance/`

## Phase 2: Foundational schema vocabulary

- [x] T004 Define shared closed value forms in `contracts/intent-compliance/veto-class-vocabulary.schema.yaml`
- [x] T005 [P] Document validator finding and fixture metadata in `specs/015-intent-compliance-contract/contracts/validator-cli.md`

## Phase 3: User Story 1 - Validate governed intent evidence

**Independent test**: the public validator accepts all packaged conforming
records and rejects every single-fault fixture for its declared requirement.

- [x] T006 [P] [US1] Add red tests for five schema kinds in `tests/intent-compliance/test_intent_compliance_validator_gate.py`
- [x] T007 [P] [US1] Add allowance approval schema/template/example in `contracts/intent-compliance/`
- [x] T008 [P] [US1] Add allowance revocation schema/template/example in `contracts/intent-compliance/`
- [x] T009 [P] [US1] Add allowance registry schema/template/example in `contracts/intent-compliance/`
- [x] T010 [P] [US1] Add compliance decision schema/template/example in `contracts/intent-compliance/`
- [x] T011 [US1] Implement schema loading and record dispatch in `scripts/validate-intent-compliance.py`
- [x] T012 [US1] Implement authority, chain, digest, reference, evidence, classifier, and outcome rules in `scripts/validate-intent-compliance.py`
- [x] T013 [P] [US1] Add indexed single-fault fixtures in `contracts/intent-compliance/examples/negative/`
- [x] T014 [US1] Prove fixture coverage closure in `tests/intent-compliance/test_intent_compliance_negative_corpus.py`

## Phase 4: User Story 2 - Revoke authority before dispatch

**Independent test**: current allowance resolves, revoked/reused authority is
rejected, and a registry-head change invalidates conditioned static evidence.

- [x] T015 [P] [US2] Add approval/revocation/identifier state tests in `tests/intent-compliance/test_intent_compliance_validator_gate.py`
- [x] T016 [P] [US2] Add stale trusted-registry-head evidence test in `tests/intent-compliance/test_intent_compliance_validator_gate.py`
- [x] T017 [US2] Implement deterministic static registry-head probe in `scripts/validate-intent-compliance.py`

## Phase 5: User Story 3 - Consume a pinned additive release

**Independent test**: release inventory verifies every family byte against the
exact candidate commit and the public validator runs from a refreshed checkout.

- [x] T018 [P] [US3] Complete family usage and residency documentation in `contracts/intent-compliance/README.md`
- [x] T019 [US3] Register five schemas and validator in `contracts/manifest.yaml` and `contracts/README.md`
- [x] T020 [US3] Refresh remote tags and allocate the next additive version in `contracts/manifest.yaml` and `contracts/CHANGELOG.md`
- [x] T021 [US3] Build and verify the release inventory in `contracts/releases/contract-v2.2.digests.yaml`

## Phase 6: Verification and handoff

- [x] T022 Run family, focused pytest, repository pytest, manifest, doc-health, OpenSpec, and release validators
- [ ] T023 Update completion boxes and realization evidence in `openspec/changes/add-standing-policy-compliance-contract/`
- [ ] T024 Commit, push, open a PR, request Codex review, and resolve all correctness/security findings
- [ ] T025 Merge the green release PR, publish/verify the annotated tag, and record exact remote evidence

## Dependencies

1. T001-T005 establish the governed workspace and shared shape.
2. T006-T014 complete independently testable record validation.
3. T015-T017 complete revocation and static stale-snapshot evidence behavior.
4. T018-T021 complete release registration after implementation stabilizes.
5. T022-T025 verify and publish the exact candidate.

US1 blocks US2 because race and revocation probes consume parsed records. US3
depends on US1 and US2 because release inventory must describe final bytes.
