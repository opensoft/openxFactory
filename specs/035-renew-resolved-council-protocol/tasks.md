# Tasks: Neutral resolved council protocol

**Input**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [contracts/](contracts/), [quickstart.md](quickstart.md)

**Tests are required, and they come first.** The spec's Assumptions require "deterministic corpus, race, isolation, authorization and migration verification", and SC-001 to SC-003 are measured by executed vectors. In every implementation phase:

1. The test and vector tasks are written first.
2. They are run red, with the failure count recorded in `evidence.md`.
3. Only then do the implementation tasks begin.

The phase is done when the quickstart's per-phase proof passes.

**One phase is one reviewed pull request**, from this branch line, landing only on Brett Heap's word. Every PR carries:

- `Lane: codexfactory-2 (codeXfactory-2)` in its body and commit trailers;
- explicit-pathspec commits;
- no Copilot review request by any route.

Phase 1 joins the template's *Setup* and *Foundational* phases, so that the first PR is self-consistent. Owner-act tasks are marked **OWNER**, stay unticked, and record dated evidence beside them.

**Format**: `- [ ] T### [P?] [US?] Description with file path`. `[P]` means different files with no dependency on an incomplete task. It never means permission to skip a dependency or a claim.

## Out of scope (R20)

None of the following belongs to this feature:

- producer or consumer code;
- HTTP envelopes, persistence or transactions (025);
- domain rule-file adapters;
- broker or credential provisioning;
- deployment;
- successor pin advances;
- activation;
- any spec delta;
- the archive.

No task edits `openspec/changes/renew-resolved-council-protocol/`, `governance/review-authority/` or `openXwallet/`.

---

## Phase 1: Setup and foundational (PR-1)

**Purpose**: the family skeleton, the shared grammar, the protocol identifiers, the two digest subjects, the corpus format and its adjudicator, the validator skeleton, and the CI gate. Nothing here selects or activates anything.

**Unblocks**:

- 049: T027 and the T026→T030 binding of selectors, through the protocol identifier values; T001's follow-up dated section in 049's `contracts/interfaces.md`.
- 025: FR-001 and FR-011, the identifiers.

### Setup

- [ ] T001 Create `specs/035-renew-resolved-council-protocol/evidence.md`. Record:
  - the lane claim on `opensoft/openxFactory:openspec/changes/renew-resolved-council-protocol` (brett-wip `lanes/log/codeXfactory-2.md`);
  - Brett Heap's 2026-10-08 word;
  - the base commit and `origin/main` at start.
- [ ] T002 [P] Create the skeleton:
  - `contracts/council-convening/conformance/vectors/` with one subdirectory per area: `foundation`, `resolution`, `assignment`, `signing`, `binding`, `migration`;
  - `scripts/council_convening/__init__.py`;
  - `tests/council_convening/conftest.py`.
- [ ] T003 [P] Write `contracts/council-convening/README.md`:
  - headers `Status: ratified`, `Ratified by: renew-resolved-council-protocol`, `Kind: reference`;
  - purpose and ownership boundary, from provider-interface § What stays the successors';
  - the dormancy statement;
  - the out-of-scope list (R20);
  - the adapter residual risk (R6);
  - "wallet trust controls outside worker registration are unchanged" (FR-010);
  - owner acts named, not performed.

### Tests first

- [ ] T004 [P] Write failing `tests/council_convening/test_shared_definitions.py`, covering every grammar in data-model § Shared definitions:
  - whole-string matching, including a trailing-newline refusal;
  - `full_sha` refusing an abbreviated id, an uppercase id and a branch;
  - `pull_number` bounds, with a boolean refused;
  - every `relative_path` refusal;
  - `utc_instant` calendar validity;
  - base64url lengths;
  - closed `candidate`;
  - closed `refusal_code`.
- [ ] T005 [P] Write failing `tests/council_convening/test_protocol_registry.py`:
  - exactly two entries;
  - identifiers, roles, signing contexts and recognition rules per data-model E1;
  - statuses `available` and `in_use`;
  - tag fields `null`;
  - an added, removed or renamed entry is refused (`council-convening-registry-closure`).
- [ ] T006 [P] Write failing `tests/council_convening/test_digest_subjects.py`:
  - `council_convening` and `council_seat_return_payload` are present in both `contracts/signed-execution-chain/digest-construction.schema.yaml` `$defs/digest_subject` and `scripts/signed_execution_chain/canonical.py` `SUBJECTS`;
  - they are appended after `daily_batch_root`, with no member reordered;
  - `construction_name` is unchanged;
  - `canonical.serialize` refuses a float, an integer above 2^53 − 1 and a lone surrogate.
- [ ] T007 [P] Write failing `tests/council_convening/test_corpus_index.py`:
  - index closure in both directions;
  - raw-byte `sha256` rows;
  - bytewise path order;
  - `case_id` equals the basename;
  - `$parts` join, and an object leaf elsewhere is refused;
  - `evaluation_time` required;
  - unknown members refused;
  - JSON byte form: no byte-order mark, LF, one trailing newline.
- [ ] T008 [P] Write failing `tests/council_convening/test_validator_cli.py`:
  - exits 0, 1 and 2;
  - the finding-line format;
  - every Phase 1 proof-of-work note from contracts/validator-cli.md;
  - `corpus --json` shape;
  - `check` emitting `council-convening-not-offline-checkable` rather than a pass.
- [ ] T009 [P] Write failing `tests/council_convening/test_gate_wiring.py` against `.github/workflows/council-convening-gate.yml`:
  - job id `council-convening-gate` with no `name:` key;
  - a `pull_request` trigger on `main`;
  - installs `requirements/hermes-runtime-contracts.lock` with `--require-hashes`;
  - runs the validator;
  - a positive assertion step requiring every proof-of-work note;
  - no `secrets` context and no `id-token`;
  - plus a repository check that no path under `governance/review-authority/` or `openXwallet/` is changed by this feature's commits.

### Implementation

- [ ] T010 Widen `$defs/digest_subject` in `contracts/signed-execution-chain/digest-construction.schema.yaml`:
  - append exactly `council_convening` and `council_seat_return_payload`;
  - add a comment in the file's tranche style naming `renew-resolved-council-protocol` D1/D3 and what each subject is taken over;
  - subjects are added; no construction is added (R3).
- [ ] T011 Mirror both subjects in `scripts/signed_execution_chain/canonical.py` `SUBJECTS`, with the same comment.
- [ ] T012 Refresh the `signed-execution-chain-digest-construction` row `sha256` in `contracts/manifest.yaml` to the new bytes:
  - add a row comment;
  - make no version and no CHANGELOG change, because a row moves with its bytes and the version is the cutting session's act (the row's own precedent).
  - Then run `tests/signed_execution_chain tests/clearing tests/code_surface tests/intent-compliance tests/manifest_digests` green.
- [ ] T013 Author `contracts/council-convening/shared-definitions.schema.yaml`:
  - house header: `schema_version`, `kind: openxfactory-council-convening-contract-schema`, `name`, `$schema`, and an `$id` under `https://xforge.us/schemas/openxfactory/council-convening/v1/`;
  - `contract_id`, `contract_schema_version: 1`, `title`, `description`;
  - every definition in data-model § Shared definitions, with `digest` taken by `$ref` to the construction file.
- [ ] T014 Author `contracts/council-convening/protocol-registry.schema.yaml` and the closed instance `contracts/council-convening/protocol.registry.yaml`, per data-model E1 and research R10. The legacy entry has status `in_use`; the replacement has status `available`; all tag fields are `null`.
- [ ] T015 Implement `scripts/council_convening/records.py`:
  - the schema registry, using `Draft202012Validator`, `FormatChecker` and `referencing.Registry`;
  - whole-match identifier enforcement;
  - the canonicalizability pre-check through `canonical.serialize`;
  - a `Refused(code, member)` exception whose messages never echo values.
- [ ] T016 Implement `scripts/council_convening/corpus.py`:
  - index loading, closure and raw-byte digests;
  - `$parts` join;
  - a dispatch table by `boundary`, with handlers registered by later modules;
  - exact outcome, refusal and `derived` comparison;
  - refusal-code and requirement coverage.
- [ ] T017 Implement `scripts/council_convening/generate.py`:
  - deterministic JSON writing: sorted keys, 2-space indent, LF, one trailing newline;
  - labelled test-key derivation, a SHA-256 of a fixed public phrase plus a label, used as the Ed25519 seed, with signing through `cryptography`;
  - no seed or private key is ever written;
  - `--check`, which regenerates into a temporary tree and byte-compares (R18).
- [ ] T018 Author the `foundation` vectors in `contracts/council-convening/conformance/vectors/foundation/`: identifier grammars, the trailing newline, non-canonicalizable values and `protocol_unknown`. Each carries `applies_to: [producer, consumer]`. Then generate `contracts/council-convening/conformance/index.json`.
- [ ] T019 Implement `scripts/validate-council-convening.py`:
  - a thin CLI over the package, with the self-test, `check` and `corpus` modes;
  - finding format, notes and exit codes per contracts/validator-cli.md;
  - `select` and `--historical` are added in Phase 6, and an unknown subcommand is argparse's exit 2.
- [ ] T020 Add `.github/workflows/council-convening-gate.yml` per R17, with a header stating that the gate reports and does not gate until the owner requires it.
- [ ] T021 Run quickstart steps 1–4. Record base and head runs in `evidence.md` § Phase 1: the red counts, the green counts, the validator notes, the OpenSpec totals, the doc-health diff, and pytest selected, passed and skipped. Open PR-1 as a draft, stating the unblocks above.

**Checkpoint**: The validator self-test passes on the foundation corpus. Successors can read the protocol identifiers at a reviewed commit.

---

## Phase 2: User Story 1 — Agree on membership before work (P1) — MVP (PR-2)

**Goal**: the commission record and its provenance reproduce identically in independent implementations, and every refusal happens before work or assignment (spec US1; FR-001–FR-004; D1, D2).

**Independent test**: `python3 scripts/validate-council-convening.py` adjudicates every `resolution` vector. Every positive yields the expected `required_seats` and `convening_digest`, and every negative yields exactly its code.

**Unblocks**:

- 049: T003 (a corpus to pin), T010 (payload shape), T011b (the POST body's provider half, with 025), T012 (the head-race half), T013.
- 025: FR-001–FR-004.

**Depends on**: Phase 1. OPEN-3 (rule currency) governs the `rule_superseded` vectors. If it is unruled when the phase is otherwise ready, this phase lands without `rule_superseded` in the closed vocabulary, and a follow-up PR adds the code and its vectors after the ruling.

### Tests first

- [ ] T022 [P] [US1] Write failing `tests/council_convening/test_predicates.py`:
  - both predicates hold and do not hold;
  - every pattern-grammar refusal;
  - the bare-directory evidence rule;
  - the entry-count completeness rule, where one rename is one entry and two paths;
  - unevaluable is never false;
  - the wrong input contract;
  - an unknown predicate.
- [ ] T023 [P] [US1] Write failing `tests/council_convening/test_resolution.py`:
  - the closed E2 shape;
  - roster composition: standing order; held seats appended; a conditional seat already standing appears once; an unbound held seat refuses; an empty roster; a duplicate seat; a reordered roster; a same-count substitution;
  - provenance against injected oracles: rule availability, authority, digest, currency under the OPEN-3 ruling, class, projection, consumed facts, unused facts, fact source, secrets via `$parts`, candidate mismatch, head moved before the recheck, head moved after the recheck, head moved at admission, head unavailable;
  - `convening_digest` known answers.
- [ ] T024 [US1] Author the `resolution` vectors in `contracts/council-convening/conformance/vectors/resolution/` with their expected outcomes before any implementation.
  - Positives: standing only; a conditional seat held; a conditional seat not held; a `rule_facts` conjunction held; a conditional seat already standing; both rename paths.
  - At least one negative per Phase 2 refusal code.
  - Shared checks carry `applies_to: [producer, consumer]`. Pre-submit drift is producer-only. Admission drift is consumer-only.
  - Regenerate `conformance/index.json`.

### Implementation

- [ ] T025 [US1] Author `contracts/council-convening/predicate-registry.schema.yaml` and the closed instance `contracts/council-convening/predicate.registry.yaml`, per data-model E3 and research R5.
- [ ] T026 [US1] Author `contracts/council-convening/council-convening.schema.yaml`, per data-model E2.
- [ ] T027 [US1] Implement `scripts/council_convening/predicates.py` from E3's written semantics only. No code is copied from codexFactory (R4).
- [ ] T028 [US1] Implement `scripts/council_convening/resolution.py`:
  - roster composition and every provenance check;
  - the injected oracle interface (R8);
  - the secret check through `importlib` of `SECRET_PATTERNS` in `scripts/validate-domain-factory.py` (R9);
  - `convening_digest`.
- [ ] T029 [US1] Register the `commission` and `admission` handlers in `scripts/council_convening/corpus.py`. Add the offline E2 rules to `check` in `scripts/validate-council-convening.py`. Add the adapter and residual-risk section to `contracts/council-convening/README.md`.
- [ ] T030 [US1] Run quickstart steps 1–4 and record them in `evidence.md` § Phase 2, including the agreement-set count. Open PR-2 as a draft.

**Checkpoint**: The MVP. Producer and consumer can each prove membership agreement against one reviewed commit, while staying dormant.

---

## Phase 3: User Story 2 (a) — Frozen assignments and exact completion (P1) (PR-3)

**Goal**: one immutable assignment per required seat, with retry identity, completion on exactly the frozen identities, and a frozen roster that later rules never change (spec US2 scenarios 3–4; FR-004, FR-005; D2).

**Independent test**: every `assignment` vector adjudicates. Same-count wrong identity, missing, duplicate and extra returns refuse, and a rule changed after freezing does not change completion.

**Unblocks**:

- 049: T012 (retry identity), T015b (the provider half of the snapshot and assignment encodings), T016b (the public assignment shape), T021/T022 (completion mapping).
- 025: FR-005–FR-007.

**Depends on**: Phase 2. OPEN-1 governs the assignment ceiling vectors, under the same withhold-then-follow-up rule as Phase 2.

### Tests first

- [ ] T031 [P] [US2] Write failing `tests/council_convening/test_assignments.py`:
  - E4 and E5 shapes;
  - one assignment per seat, in roster order: extra, missing and reordered refused;
  - duplicate `assignment_id`;
  - shared holder;
  - `convening_digest` recomputation;
  - `cross_convening_context` fields;
  - lifetime and ceiling at `evaluation_time`: not-yet-valid, and expired at the instant;
  - closed `permitted_operations`;
  - retry: identical returns the same snapshot; conflicting is `convening_conflict`;
  - completion: unlisted, duplicate, missing and same-count wrong identity;
  - a changed rule oracle after freezing, where completion still follows the snapshot.
- [ ] T032 [US2] Author the `assignment` vectors in `contracts/council-convening/conformance/vectors/assignment/` with their expected outcomes first. Regenerate the index.

### Implementation

- [ ] T033 [US2] Author `contracts/council-convening/convening-snapshot.schema.yaml` and `contracts/council-convening/seat-assignment.schema.yaml`, per data-model E4 and E5.
- [ ] T034 [US2] Implement `scripts/council_convening/assignments.py`.
- [ ] T035 [US2] Register the snapshot-at-`admission` and `completion` handlers in `scripts/council_convening/corpus.py`, and extend `check` in `scripts/validate-council-convening.py`.
- [ ] T036 [US2] Run quickstart steps 1–4, record them in `evidence.md` § Phase 3, and open PR-3 as a draft.

---

## Phase 4: User Story 2 (b) — Assignment-bound key registration and signed returns (P1) (PR-4)

**Goal**: possession proofs and returns bind protocol, convening, council, candidate, assignment, seat and digest. Wrong principals, shared keys, replay, challenge misuse, root authorization and cross-protocol bytes all refuse (spec US2 scenarios 1–2; FR-006–FR-008; D3).

**Independent test**: every `signing` vector adjudicates, with `signed_bytes` known answers matching. `generate --check` reproduces every signature byte for byte.

**Unblocks**:

- 049: T020 (signing-context strings and shapes), T017/T019 (mapping the producer-internal contexts), T025 (what the consumer's evidence must show).
- 025: FR-008–FR-010.

**Depends on**: Phase 3. OPEN-1 governs the challenge ceiling vectors, under the withhold-then-follow-up rule.

### Tests first

- [ ] T037 [P] [US2] Write failing `tests/council_convening/test_signing.py`:
  - contexts built from the frozen assignment, challenge and key, never from caller labels;
  - `signed_bytes` known answers;
  - fingerprint recomputation;
  - stdlib `ed25519.verify`;
  - registration refusals: `wrong_principal` with a valid proof, already registered, `shared_key`, cross seat, cross convening, cross protocol, proof invalid, and root-authorization members refused as `root_authorization_refused` before `registration_malformed`;
  - challenge refusals: unknown, wrong assignment, consumed, expired at the instant, lifetime above the ceiling;
  - return refusals: unregistered, key mismatch, digest mismatch, signature invalid, replay into another assignment, convening or protocol, a float payload refused as `value_not_canonicalizable`;
  - legacy v1 signed bytes never verify as replacement bytes, and the reverse.
- [ ] T038 [P] [US2] Write failing `tests/council_convening/test_corpus_regeneration.py`:
  - `generate --check` is byte-identical;
  - no corpus file carries a seed or private-key member (`seed`, `private`, `d`) or a 32-byte seed-shaped value outside `public_key` and `nonce`;
  - every corpus file is clean under the provider's `SECRET_PATTERNS`.
- [ ] T039 [US2] Generate the `signing` vectors in `contracts/council-convening/conformance/vectors/signing/` from labelled test keys, with their expected outcomes authored first. Regenerate the index.

### Implementation

- [ ] T040 [US2] Author `contracts/council-convening/registration-challenge.schema.yaml`, `contracts/council-convening/seat-key-registration.schema.yaml`, `contracts/council-convening/seat-return.schema.yaml` and `contracts/council-convening/signing-context.schema.yaml`, per data-model E6–E9.
- [ ] T041 [US2] Implement `scripts/council_convening/signing.py`:
  - reuse `canonical.serialize` and `ed25519.verify`;
  - the estate fingerprint spelling;
  - no second framing (R3).
- [ ] T042 [US2] Register the `registration` and `return` handlers in `scripts/council_convening/corpus.py`. Add signing to `scripts/council_convening/generate.py`. Make `check` verify a record's signature where the record carries one.
- [ ] T043 [US2] Run quickstart steps 1–4, record them in `evidence.md` § Phase 4, and open PR-4 as a draft.

---

## Phase 5: User Story 2 (c) — Producer identity bound to verified workflow claims (P1) (PR-5)

**Goal**: the producer's authority is bound to the current governed repository identity and to verified issuer, audience, subject and workflow claims. A workflow ref is never a subject, and an unverified broker parks activation (FR-009; D4).

**Independent test**: every `binding` vector adjudicates against the repository's own `contracts/policies/repository-identity.yaml`.

**Unblocks**:

- 049: T023, T024, T031 (the shape the owner provisions).
- 025: FR-008 (principal-authentication inputs), and H3's activation park.

**Depends on**: Phase 1. It may be authored in parallel with Phases 2–4, and it lands after Phase 2. OPEN-2 decides the instance's home; OPEN-3 decides the workflow-revision rule.

### Tests first

- [ ] T044 [P] [US2] Write failing `tests/council_convening/test_binding.py`:
  - the E10 shape;
  - repository derivation through the existing reader in `scripts/estate_inventory.py`: the former spelling and a non-canonical case variant refused as `repository_identity_former`, an unknown repository refused;
  - the issuer constant;
  - audience and subject wildcards;
  - `sub` versus `job_workflow_ref` conflation;
  - an unlisted workflow;
  - the workflow-revision rule;
  - decoded-only claims;
  - an unverified broker parks activation;
  - the `.template.yaml` stub is never accepted as live.
- [ ] T045 [US2] Author the `binding` vectors in `contracts/council-convening/conformance/vectors/binding/` with their expected outcomes first. Regenerate the index.

### Implementation

- [ ] T046 [US2] Author `contracts/council-convening/producer-binding.schema.yaml` and `contracts/council-convening/producer-binding.template.yaml`. The template carries `instantiation_stub: true` and no live audience, subject template or repository id.
- [ ] T047 [US2] Implement `scripts/council_convening/binding.py`, reusing the repository-identity reader. No second transfer map.
- [ ] T048 [US2] Register the `binding` handlers in `scripts/council_convening/corpus.py`, and add `check` support. Document the binding and the OPEN-2 outcome in `contracts/council-convening/README.md`.
- [ ] T049 [US2] Run quickstart steps 1–4, record them in `evidence.md` § Phase 5, and open PR-5 as a draft.

---

## Phase 6: User Story 3 — Activate and recover the matched pair (P2) (PR-6)

**Goal**: one explicitly selected protocol per binding, with no fallback. Legacy is recognized for warning, refusal and historical routing. Pair matching, activation evidence and the paired-rollback runbook are defined (spec US3; FR-011, FR-012; D5).

**Independent test**: every `migration` vector adjudicates. Every legacy vector carries an explicit `registry_status` override, so the corpus digest does not move when Phases 7 and 8 flip the registry.

**Unblocks**:

- 049: T027 (the selection shape), T028, T029 (the runbook its quickstart mirrors), T032 (the rehearsal-record shape).
- 025: FR-011, FR-012.

**Depends on**: Phases 2–5.

### Tests first

- [ ] T050 [P] [US3] Write failing `tests/council_convening/test_migration.py`:
  - legacy recognition: a roster-less block, legacy context strings, a root-authorized registration;
  - status-driven behavior: `in_use` accepts, `deprecated` warns (an error under `--strict`), `historical_only` refuses;
  - `--historical` classifies and never reinterprets;
  - E11 pair matching on all four members;
  - `rejected_without_fallback`;
  - `replacement_not_admission_eligible` before the major;
  - E12 completeness per act: `owner_word` required for activation and rollback, new records retained on rollback, resume only after a passing rehearsal with both sides verified.
- [ ] T051 [US3] Author the `migration` vectors in `contracts/council-convening/conformance/vectors/migration/` with their expected outcomes first. Regenerate the index.

### Implementation

- [ ] T052 [US3] Author `contracts/council-convening/protocol-selection.schema.yaml` and `contracts/council-convening/activation-evidence.schema.yaml`, per data-model E11 and E12.
- [ ] T053 [US3] Implement `scripts/council_convening/migration.py`. Add the `select` and `check --historical` modes to `scripts/validate-council-convening.py`.
- [ ] T054 [US3] Write `docs/council-convening-activation-runbook.md` with headers `Status: ratified` and `Ratified by: renew-resolved-council-protocol`. It covers, in order:
  1. pause commissioning;
  2. drain or explicitly cancel in-flight convenings;
  3. switch both selections to one E11 value set;
  4. both sides run the full corpus at the same index digest;
  5. resume only on a matched, verified pair;
  6. paired rollback that keeps new records as audit evidence.

  Each act is an owner act recorded as E12. Link the runbook from the README document index (`README.md`).
- [ ] T055 [US3] Run quickstart steps 1–4, record them in `evidence.md` § Phase 6, and open PR-6 as a draft.

**Checkpoint**: The family is complete on `main`, dormant and unregistered. Both successors can finish dormant implementations against one reviewed commit.

---

## Phase 7: Release A — the additive and deprecating minor (PR-7)

**Purpose**: publish the family, with the replacement `available` and the legacy protocol `deprecated` (R19; § Change Classes).

**Unblocks**:

- 049: T030 (the minor half); T003 and the `stack.yaml` pin on a published bundle.
- 025: FR-011 and FR-012 (a compatible published pin).

**Depends on**: Phases 1–6 merged, and OPEN-4 ruled.

- [ ] T056 Claim the contract-cut shared substrate on openxFactory's pinned "Shared substrates — claims" issue. Then fetch and merge `origin/main`. Then allocate the next available minor from `contracts/manifest.yaml` at that moment, re-checking tag availability (Bundle Realization Order step 1). Record the allocation in `evidence.md`.
- [ ] T057 [P] Write failing `tests/council_convening/test_council_convening_manifest_rows.py`:
  - every family schema, both registries and `conformance/index.json` carry a row;
  - the rows are closed in both directions;
  - each row's digest is recomputed.
- [ ] T058 [P] If OPEN-4 rules "join", write failing release-membership tests in `tests/hermes_runtime_contracts/test_council_convening_release_floor.py`:
  - below the floor, no family path is a member;
  - at or after the floor, the family, validator, package and tests are members;
  - every published inventory up to the previous tag still verifies.
- [ ] T059 In `contracts/council-convening/protocol.registry.yaml`, flip legacy to `deprecated` and write the allocated tag into the `introduced_in` and `deprecated_in` fields. No corpus vector changes (Phase 6's override rule).
- [ ] T060 Register the manifest rows in `contracts/manifest.yaml`: `canonical_openxfactory_contract`, `adapter_owner: openxFactory`, and a `consumption_rule` naming the pin recipe in contracts/provider-interface.md. Bump `contract_bundle_version` to the allocated tag.
- [ ] T061 Write the `contracts/CHANGELOG.md` entry for the additive and deprecating minor:
  - what is added;
  - what is deprecated;
  - the removal named as the next major, written concretely;
  - the migration path.

  Write the § *Deprecations Currently In Force* entry in `docs/contract-versioning-policy.md`, from the refusal list.
- [ ] T062 [P] Add the family rows to the `contracts/README.md` native contract index, and the family README and runbook rows to the `README.md` document index.
- [ ] T063 If OPEN-4 rules "join", add the `COUNCIL_CONVENING_RELEASE_FLOOR` block to `scripts/hermes_runtime_validation/release.py`, set to the allocated version, in the clearing block's form.
- [ ] T064 Build `contracts/releases/<allocated>.digests.yaml` with `scripts/validate-contract-release.py build`. Then run, against the exact candidate:
  - `verify-commit` and `verify-promotion`;
  - the release-tag gate;
  - the supported-domain regression denominator;
  - quickstart steps 1–5.

  Record everything in `evidence.md` § Phase 7.
- [ ] T065 Open PR-7 as a draft. It lands only on Brett Heap's word, on the plain gate, at the exact reviewed commit.
- [ ] T066 **OWNER**: publish the annotated tag at the landed commit (Bundle Realization Order step 5). Record `verify-tag --remote origin --tag <allocated>` from an independently refreshed checkout in `evidence.md`. The box stays unticked.

---

## Phase 8: Release B — the removal major (PR-8)

**Purpose**: refuse legacy for active selection, keep historical classification, and make the replacement admission-eligible (R19; FR-011).

**Unblocks**:

- 049: T030 (the major half); prerequisites for T033 and T034.
- 025: FR-011 (old shapes refused at the major) and FR-012.

**Depends on** all four of:

- T066 done;
- at least one full minor served;
- both successors' dormant implementations verified against the published minor (049 T013/T035 and 025 evidence, cited and not claimed);
- the owner's release act.

- [ ] T067 Record the four preconditions with citations in `evidence.md` § Phase 8. Stop if any is missing.
- [ ] T068 Claim the contract-cut substrate, merge `origin/main`, and allocate the next major from `contracts/manifest.yaml` at that moment. Record it in `evidence.md`.
- [ ] T069 [P] Write failing tests in `tests/council_convening/test_protocol_registry.py` and `tests/council_convening/test_migration.py`:
  - legacy `historical_only` refuses active legacy records;
  - `--historical` still classifies them;
  - the replacement is `admission_eligible`;
  - `removed_in` is set.
- [ ] T070 In `contracts/council-convening/protocol.registry.yaml`, flip the statuses and set `removed_in`.
- [ ] T071 Write the BREAKING `contracts/CHANGELOG.md` entry with its migration note, citing the published minor as the served deprecation window. Write the § *Deprecations Executed* entry in `docs/contract-versioning-policy.md`. Process every other § *Deprecations Currently In Force* entry that targets this major, restating each or executing it under its own pre-authorized text. Phase 8 decides none of those acts.
- [ ] T072 Re-baseline `contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml` against the actual union of supported consumers, per the policy's § Supported-Domain Regression Denominator. Bump `contract_bundle_version`. Build `contracts/releases/<allocated>.digests.yaml`. Run quickstart steps 1–5 and record them in `evidence.md` § Phase 8.
- [ ] T073 Open PR-8 as a draft. It lands only on Brett Heap's word.
- [ ] T074 **OWNER**: publish the major's annotated tag at the landed commit. Record `verify-tag` in `evidence.md`. The box stays unticked.

---

## Phase 9: Closeout (PR-9)

**Purpose**: provider realization evidence handed to the governance packet. The archive stays gated on successor and activation evidence (change tasks 3.1–3.5).

- [ ] T075 In `evidence.md`, record:
  - each phase's merged commit;
  - both releases' corpus digests;
  - the validator outputs;
  - the 049 and 025 evidence references, cited and not claimed.
- [ ] T076 Report the change's task 3.1 acceptance evidence to the change's owner lane. Leave 3.2–3.5 to their owner and archive acts. Edit nothing under `openspec/changes/renew-resolved-council-protocol/` from this feature.
- [ ] T077 Re-run `speckit-analyze` over the final artifacts, and update `analysis.md`. Under the shared-substrate claim, update this feature's sentence in the README's OpenSpec Records block in `README.md`.

---

## Dependencies and execution order

```text
Phase 1 ──► Phase 2 ──► Phase 3 ──► Phase 4 ──┐
   │                                          ├──► Phase 6 ──► Phase 7 ──► [OWNER tag] ──► Phase 8 ──► [OWNER tag] ──► Phase 9
   └──────► Phase 5 (lands after Phase 2) ────┘
```

The order within a phase:

1. tests and vectors, run red and recorded;
2. schemas;
3. the package module;
4. handlers and CLI;
5. gates and evidence;
6. the PR.

**Gates on Brett Heap's rulings**:

| Ruling | Governs |
|---|---|
| OPEN-1 | T031, T037 (the ceiling vectors) |
| OPEN-2 | T046 and T048 (the instance's home) |
| OPEN-3 | T023 and T044 (currency and the workflow revision) |
| OPEN-4 | T058 and T063 |

An unruled question withholds only its vectors and code. It never blocks the rest of its phase.

## Parallel opportunities

- **Phase 1**: T002–T009 in parallel, then T010–T020 in order (T010→T011→T012 are one invariant).
- **Phase 2**: T022 ∥ T023, then T024. T025 ∥ T026, then T027→T028→T029.
- **Phase 3**: T031, then T032, then T033→T034→T035.
- **Phase 4**: T037 ∥ T038, then T039, then T040→T041→T042.
- **Phase 5**: authored beside Phases 2–4 (T044–T048). Its corpus index is regenerated when it merges after Phase 2.
- **Phase 7**: T057 ∥ T058 ∥ T062 once T056 holds the claim.

## Implementation strategy

- **MVP**: Phases 1–2, which deliver the membership agreement. They let 049's T003 and T010 and 025's FR-001–FR-004 proceed dormant at a reviewed commit.
- **Increments**: each later phase adds one consumer-facing artifact class and its vectors, and lands alone.
- **Publication**: comes only through Phases 7 and 8. Activation stays outside this feature entirely.

## Requirement coverage

| Requirement | Tasks |
|---|---|
| FR-001 | T004, T005, T013, T014, T023, T026 |
| FR-002 | T022, T023, T025, T026, T027, T028 |
| FR-003 | T016, T023, T024, T028 |
| FR-004 | T023, T031, T034 |
| FR-005 | T031, T032, T034 |
| FR-006 | T031 (public assignment, unique holder), T037 (shared key), T040 (no secret member) |
| FR-007 | T037, T040, T041, T044 |
| FR-008 | T006, T010, T011, T037–T042 |
| FR-009 | T044–T048 |
| FR-010 | T003, T007, T009, T016–T018, T024, T032, T039, T045, T051, T057 |
| FR-011 | T005, T014, T050–T053, T059–T061, T069–T071 |
| FR-012 | T050, T052, T054, T066, T074 |
| SC-001 | T016, T024, T032, T039, T045, T051; the successors' evidence is external |
| SC-002 | T031, T032; the consumer's database evidence is external (025) |
| SC-003 | T037, T038, T039 |
| SC-004 | T052, T054; the owner's rehearsal is external |

The spec delta's seven requirements map as follows:

| Spec-delta requirement | Phase |
|---|---|
| Resolved roster | Phase 2 |
| Reproducible provenance | Phase 2 |
| Frozen assignments | Phase 3 |
| Candidate across submission and admission | Phase 2 |
| Independent signing authority | Phase 4 |
| Verified workflow binding | Phase 5 |
| Versioned coordinated migration | Phases 6–8 |
