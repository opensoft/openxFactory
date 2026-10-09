# Tasks: Factory MCP authorization profile

Status: draft
Kind: plan

**Input**: [`spec.md`](spec.md), [`plan.md`](plan.md), [`research.md`](research.md),
[`data-model.md`](data-model.md), [`contracts/interface.md`](contracts/interface.md),
[`quickstart.md`](quickstart.md), and the change's
[`tasks.md`](../../openspec/changes/amend-factory-mcp-conformance-auth-profile/tasks.md)
§ 2, which holds the governance boxes. This file does not duplicate them.
**Lane**: `openxfactory-5` (display `openXfactory-5`).

Format: `[ID] [P?] [Story] Description`. `[P]` marks a task that touches
different files from its neighbours and depends on no unfinished task. Every
test below lives in `tests/factory-mcp/test_factory_mcp_conformance.py`,
class `ConformanceTests`, in a new section headed for this feature.

## Phase 1: Setup

- [x] T001 Write the feature documents: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/interface.md`, `quickstart.md`, `checklists/` and this file, then run analyze and fold its findings in (change task 2.1).

## Phase 2: Red-first tests (change task 2.2). Before ANY schema, example or validator byte

All of Phase 2 is ONE commit. It changes only the test module.

- [ ] T002 Add the section's constants and the `hosted()` helper, which makes the synthetic service deployed with a valid block supported by an `auth` gap (FR-001, FR-003).
- [ ] T003 [US1] `test_hosted_declaration_without_block` → `hosted_auth_missing` at `/service` (FR-001).
- [ ] T004 [US1] `test_auth_on_an_undeployed_service_is_refused` → `schema_oneOf` at `/service`, and `test_stdio_declaration_needs_no_block` → `valid-with-gaps`. **Characterization: both pass on `main`** (FR-002).
- [ ] T005 [US1] `test_a_valid_hosted_block_is_accepted` (gap-only and evidence-supported blocks, RS256 alone, RS256 with EdDSA, both bindings), and `test_block_shape_is_closed`. The latter asserts the valid block first, so it is red on `main`, then each closed-shape fault (an unknown field, `client_secret`, `jwks`, a wrong type, a binding outside the set, an empty or repeated algorithm list, an issuer as a list, a second issuer field, a missing field) → `schema_oneOf` at `/service` (FR-003).
- [ ] T006 [US1] `test_issuer_must_be_an_https_identifier`: a bare runtime name, http, userinfo, a query, an empty query, a fragment, a URN, no host → `invalid_issuer` at `/service/auth/issuer`; valid issuers accepted (FR-004).
- [ ] T007 [US1] `test_metadata_path_is_the_rfc9728_location`: empty, `/`, one segment, a trailing slash, a port, each derived; the suffix-appended form, the bare path for a path-bearing URI, and another well-known name → `auth_metadata_path_mismatch` (FR-005).
- [ ] T008 [US1] `test_hosted_resource_uri_carries_no_query`: a query and an empty query, with a block and without one (beside `hosted_auth_missing`) → `auth_resource_query` at `/service/canonical_resource_uri` (FR-006).
- [ ] T009 [US1] `test_auth_claims_cite_support`: no support → `unsupported_auth`; support without `auth` → `unsupported_auth`; a dangling id and a repeated id in `evidence_ids` and in `gap_ids` → `missing_support_reference` and `duplicate_support_reference` at their `/service/auth/...` locations; gap-only → `valid-with-gaps` and not verified. Also `test_auth_concern_is_admitted_everywhere` (a not-deployed declaration whose gap carries `auth`) (FR-007).
- [ ] T010 [P] [US2] `test_rs256_is_required` (EdDSA alone; `rs256`), `test_none_and_hmac_are_refused_by_name` (each of the four names in more than one letter case), `test_other_algorithms_are_not_admitted` (ES256, PS256, RS384, `eddsa`, a non-ASCII lookalike) (FR-008 to FR-010).
- [ ] T011 [P] [US3] `test_audience_is_bound_to_the_server`: another resource, a trailing-slash or letter-case variant, a wildcard under each binding, the issuer under each binding → `auth_audience_unbound`; an `issuer_assigned` identifier accepted (FR-011 to FR-013).
- [ ] T012 [P] [US4] `test_dependency_failure_reported_as_an_error_is_an_execution_failure` and `test_result_statuses_are_completed_evaluations`. **Characterization on `main`; red against the mutant** (FR-014).
- [ ] T013 [P] [US4] `test_two_domains_share_a_code_name` and `test_a_code_no_other_domain_uses`. **Characterization: both pass on `main`** (FR-015).
- [ ] T014 `test_auth_diagnostics_are_deterministic` (several faults, two runs, identical and sorted) (FR-016, SC-007) and `test_packaged_deployed_example` (FR-017).
- [ ] T015 Amend `test_resource_identity_without_optional_format_checker` and `test_resource_uri_is_https_without_fragment_or_userinfo` to give the deployed service a valid `issuer_assigned` block, adding `auth_resource_query` where a URI carries a query (research R-15; design *Compatibility*).
- [ ] T016 Commit T002–T015 alone. Run `tests/factory-mcp/` at that commit (that is, against `main`'s schema and validator): every new refusal and both amended tests fail, the characterization tests pass. Record the run in `verification.md`.
- [ ] T017 Mutant run: `git archive` `main` into a scratch directory, remove `check_mapping`'s classification comparison, copy in the test module, run T012's two tests (red), then the same two against `main` (green). Record the diff, the commands and both results in `verification.md` (research R-14).

## Phase 3: User Story 1, the block (P1)

- [ ] T018 [US1] Schema: add `service.deployed.auth` (closed, the six fields, the bounds of R-12) and the `auth` concern to the evidence and gap vocabularies, in `contracts/factory-mcp/declaration.schema.json` (change task 2.3; FR-003, FR-007).
- [ ] T019 [P] [US1] Example: `contracts/factory-mcp/examples/declaration-deployed.example.json` (research R-16; FR-017).
- [ ] T020 [US1] Validator: a service check in `check_catalog`'s position that reports `invalid_resource_uri` (unchanged), `auth_resource_query`, `hosted_auth_missing`, `invalid_issuer` and `auth_metadata_path_mismatch`. Share the tools' support-citation loop to report `missing_support_reference`, `duplicate_support_reference` and `unsupported_auth` for the block, in `scripts/validate-factory-mcp.py` (change task 2.4; FR-001, FR-004 to FR-007, FR-016).

## Phase 4: User Story 2, the algorithms (P1)

- [ ] T021 [US2] Validator: `auth_rs256_missing`, `auth_algorithm_forbidden` and `auth_algorithm_unadmitted` (research R-7; FR-008 to FR-010).

## Phase 5: User Story 3, the audience (P2)

- [ ] T022 [US3] Validator: `auth_audience_unbound` (research R-9; FR-011 to FR-013).

## Phase 6: User Story 4, outcomes and vocabularies (P3)

- [ ] T023 [US4] No code: the enforcement exists (D8, D9). T012 and T013 witness it, and T017 records the mutant.

## Phase 7: Runbook and the stop before the cut

- [ ] T024 Runbook: `docs/factory-mcp-conformance.md` gains the block, its codes, the stdio rule, the narrowed M5 reading, the per-domain vocabulary statement, the deployed example, and links to this feature's records. The release paragraph waits for T026 (change task 2.5; FR-018).
- [x] T024a README: one Documentation-index bullet for this feature, beside the Factory MCP entries (constitution IV; analyze D1). Made with the feature documents.
- [ ] T025 Run `tests/factory-mcp/` green at the branch head. Compute the version the policy allocates, re-check #630 row 4 and the open pull requests that touch `contracts/manifest.yaml` or `contracts/releases/`, record the reasoning in the lane's progress file, push the branch, and STOP with `NEED VERSION` (change task 2.6, first sentence).

## Phase 8: After the coordinator's claim (row 4, #630)

- [ ] T026 One candidate commit: the declaration's manifest row with its digest, the `contracts/CHANGELOG.md` entry, `contracts/releases/<version>.digests.yaml`, the schema title and the runbook's release paragraph moved to the version. Run `release-tag-gate` (`scripts/validate-release-tag-gate.py`) (change task 2.6; FR-019).
- [ ] T027 Verification record (`verification.md`): every gate CI runs, on the branch and on `main` in the same clone kind; `tests/factory-mcp/`; the full suite under `setsid` with its log polled; `git diff --check`; the closing-keyword scan; and the out-of-tree engineering check by `--snapshot`, or "owed" (change task 2.7; SC-006, SC-008).
- [ ] T028 Push and open the DRAFT pull request with `--body-file`; request Copilot; post the Codex trigger once; fix, reply to and resolve every thread. It lands only on Brett Heap's realization word (change task 3.2).

## Dependencies

T001 → T002 … T015 (one commit, T016) → T017 → T018 → T019 and T020 → T021 → T022 → T023 → T024 → T025 → STOP → T026 → T027 → T028.
No schema, example or validator task starts before T016's commit exists.
Within Phase 2, T010–T013 touch independent test methods; they share one file
and one commit.

## Witness map

| FR | Tests |
| --- | --- |
| FR-001 | T003 |
| FR-002 | T004 |
| FR-003 | T005, T015 |
| FR-004 | T006 |
| FR-005 | T007 |
| FR-006 | T008, T015 |
| FR-007 | T009 |
| FR-008 to FR-010 | T005, T010 |
| FR-011 to FR-013 | T005, T011 |
| FR-014 | T012, T017 |
| FR-015 | T013 |
| FR-016 | T014, and every located assertion |
| FR-017 | T014 |
| FR-018 | T024 (review) |
| FR-019 | T026 (`release-tag-gate`) |
