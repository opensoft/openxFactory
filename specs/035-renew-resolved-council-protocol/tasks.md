# Tasks: Neutral resolved council protocol

**Input**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [contracts/](contracts/), [quickstart.md](quickstart.md), [analysis.md](analysis.md)

**Tests are required, and they come first.** The spec's Assumptions require "deterministic corpus, race, isolation, authorization and migration verification", and SC-001 to SC-003 are measured by executed vectors. In every implementation phase:

1. The test, vector and CLI-test tasks are written first.
2. They are run red locally, with the failure count recorded in `evidence.md`. A red run is never pushed: each phase's tests and implementation are pushed together, so every pushed commit passes the validators (Principle V).
3. Only then do the implementation tasks begin.

The phase is done when the quickstart's per-phase proof passes.

**Preconditions, both of them governance order (I5 in [analysis.md](analysis.md)):**

- The governing packet, #1267, is in `main`. **Satisfied**: it landed as `80f47483` on 2026-10-08.
- This planning PR, #1268, lands on Brett Heap's word before PR-1 opens. It touches `openspec/changes/renew-resolved-council-protocol/`: under Brett Heap's N10 ruling of 2026-10-08, "Dated correction + tick 2.2 (Recommended)", it replaces the stale 2026-10-03 allocation notes there with a dated allocation record and ticks the packet's task 2.2. So it lands in its own Rule 6 window.

**One phase is one reviewed pull request.** Each phase is a new branch from current `origin/main`, named `035-<phase>` (for example `035-p1-foundation`), and lands only on Brett Heap's word. Every PR carries:

- `Lane: codexfactory-2 (codeXfactory-2)` in its body and commit trailers;
- explicit-pathspec commits;
- no Copilot review request by any route.

Phase 1 joins the template's *Setup* and *Foundational* phases, so that the first PR is self-consistent. Owner-act tasks are marked **OWNER**, stay unticked, and record dated evidence beside them.

**Brett Heap's rulings of 2026-10-08 are encoded**: the five OPEN rulings, the three follow-ups that apply OPEN-3, and N10 ([spec.md § Clarifications](spec.md#clarifications); [analysis.md § Ruled](analysis.md#ruled)). No task waits on an open question or a confirmation. Each phase's `evidence.md` cites the rulings it encodes.

| Ruling | Verbatim label | Tasks it makes concrete |
|---|---|---|
| OPEN-1 | "600 s challenge, 6 h assignment (Recommended)" | T035, T036, T038 (21600 s); T042, T044, T046 (600 s) |
| OPEN-2 | "Consumer's runtime config (Recommended)" | T052, T053, T055 |
| OPEN-3 | "History + unchanged rule file (Recommended)" | T025, T026, T031 (sources); T050, T051, T053 (workflow revision) |
| OPEN-3 follow-up 1 | "Every governed source (Recommended)" | T025, T026, T031 |
| OPEN-3 follow-up 2 | "job_workflow_ref's repo (Recommended)" | T050, T051, T053, T054 |
| OPEN-3 follow-up 3 | "At or after the frozen rev (Recommended)" | T042, T050, T051, T053 |
| OPEN-4 | "Join behind a version floor (Recommended)" | T066, T068 |
| OPEN-5 | "Keep the existing names (Recommended)" | T024, T026, T028 |
| N10 | "Dated correction + tick 2.2 (Recommended)" | T002, done in #1268 itself |

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

No task of this feature's phases edits `openspec/changes/renew-resolved-council-protocol/`, `governance/review-authority/` or `openXwallet/`. The planning PR, #1268, is the one exception, and only for the packet: under N10 it carries the dated allocation record and the tick of packet task 2.2 (T002).

---

## Phase 1: Setup and foundational (PR-1)

**Purpose**: the family skeleton and README, the shared grammar, the protocol identifiers and classification, the two digest subjects, the corpus format and its adjudicator, the validator skeleton, and the CI gate. Nothing here selects or activates anything.

**Unblocks**:

- 049: T027 and the T026→T030 binding of selectors, through the protocol identifier values; T001's follow-up dated section in 049's `contracts/interfaces.md`.
- 025: FR-001 and FR-011, the identifiers and the classification rule.

### Setup

- [x] T001 Create `specs/035-renew-resolved-council-protocol/evidence.md` and link it from this feature's entry in the `README.md` document index. Record:
  - the lane claim on `opensoft/openxFactory:openspec/changes/renew-resolved-council-protocol` (brett-wip `lanes/log/codeXfactory-2.md`);
  - Brett Heap's 2026-10-08 words: "This lane, 035 then 025 (Recommended)", the five RULED lines (19:24:21Z and 19:24:59Z), and the four RULED lines at 23:03:35Z (log lines 209–212) for the three OPEN-3 follow-ups and N10;
  - #1267 landed as `80f47483`, and #1268's merge commit;
  - the base commit and `origin/main` at start.
- [x] T002 Report change task 2.2's evidence to the change's owner lane, which is this same lane, codeXfactory-2: the Constitution Check in `specs/035-renew-resolved-council-protocol/plan.md`, the coverage tables in `specs/035-renew-resolved-council-protocol/tasks.md`, and `specs/035-renew-resolved-council-protocol/analysis.md`. **Done in #1268**, under Brett Heap's N10 ruling of 2026-10-08, "Dated correction + tick 2.2 (Recommended)": #1268 ticks 2.2 in `openspec/changes/renew-resolved-council-protocol/tasks.md` with these citations and the dated allocation record (I12; N10). T001 records #1268's merge commit as the tick's landing.
- [x] T003 [P] Create the package and test skeleton: `scripts/council_convening/__init__.py`, `tests/council_convening/__init__.py` and `tests/council_convening/conftest.py`. No empty corpus directory is created: each area directory under `contracts/council-convening/conformance/vectors/` is created together with its first vector (U11).
- [x] T004 [P] Write `contracts/council-convening/README.md` and link it, as dormant and pending realization, from the `README.md` document index and the `contracts/README.md` native contract index (Principle IV; C1). The README carries:
  - headers `Status: ratified`, `Ratified by: renew-resolved-council-protocol`, `Kind: reference`;
  - purpose and ownership boundary, from provider-interface § What stays the successors';
  - the dormancy statement;
  - the out-of-scope list (R20);
  - the adapter residual risk and its fail-closed outcome (R6);
  - "wallet trust controls outside worker registration are unchanged" (FR-010);
  - Brett Heap's rulings, cited: the five OPEN rulings and the three OPEN-3 follow-ups;
  - owner acts named, not performed.

### Tests first

- [x] T005 [P] Write failing `tests/council_convening/test_shared_definitions.py`, covering every grammar in data-model § Shared definitions:
  - whole-string matching, including a trailing-newline refusal;
  - `full_sha` refusing an abbreviated id, an uppercase id and a branch;
  - `pull_number` bounds, with a boolean refused;
  - every `relative_path` refusal, a 4097-byte path refused, and a path with `\` or a C1 character accepted;
  - `head_ref` and `decimal_string`, including `-0`, an exponent and a trailing fractional zero refused;
  - `utc_instant` calendar validity;
  - base64url lengths;
  - closed `candidate`, with and without `subject_path`;
  - closed `principal_kind`, `refusal_code` and `finding_code`, each holding exactly the Phase 1 members.
- [x] T006 [P] Write failing `tests/council_convening/test_protocol_registry.py`:
  - exactly two entries;
  - identifiers, roles, signing contexts and recognition rules per data-model E1;
  - statuses `available` and `in_use`, and the schema's status enumeration holding all five statuses;
  - tag fields `null`;
  - an added, removed or renamed entry is refused (`council-convening-registry-closure`);
  - classification in its order: a replacement record carrying root-authorization members classifies as replacement (I3); a roster-less block, a legacy context string and a root-authorized registration with no `protocol` classify as legacy; an unknown `protocol` is `protocol_unknown`;
  - the selection-dependent effects of the Phase 1 rows: a legacy record under a replacement selection is `legacy_protocol_refused`; a replacement record under a legacy selection is `protocol_not_selected`; a legacy record under a legacy selection or offline is routed (I4, C3).
- [x] T007 [P] Write failing `tests/council_convening/test_digest_subjects.py`:
  - `council_convening` and `council_seat_return_payload` are present in both `contracts/signed-execution-chain/digest-construction.schema.yaml` `$defs/digest_subject` and `scripts/signed_execution_chain/canonical.py` `SUBJECTS`;
  - in the YAML enumeration they are appended after `daily_batch_root`, with no member reordered (`SUBJECTS` is a frozenset, so order is tested in the YAML only);
  - `construction_name` is unchanged;
  - `canonical.serialize` refuses a float, an integer above 2^53 − 1 and a lone surrogate;
  - one hand-authored known answer from RFC 8785: the RFC's example object with its `numbers` member removed, whose canonical bytes are copied from the RFC text (U12).
- [x] T008 [P] Write failing `tests/council_convening/test_corpus_index.py`:
  - index closure in both directions;
  - raw-byte `sha256` rows;
  - bytewise path order;
  - `case_id` equals the basename;
  - `$parts` join, with an object leaf anywhere else refused;
  - `evaluation_time` required;
  - unknown members refused;
  - JSON byte form: no byte-order mark, LF, one trailing newline;
  - coverage at the commit: every `refusal_code` and `finding_code` member probed, and every `coverage_floor` requirement cited;
  - a vector whose outcome reads a registry status without `registry_status` is refused (`council-convening-vector-registry-status-missing`; U4);
  - `derived_origin` is `hand` or `generated`.
- [x] T009 [P] Author the `foundation` vectors, creating `contracts/council-convening/conformance/vectors/foundation/` with the first of them, before any implementation:
  - boundary `definition`: each grammar's accept and refusal (`value_malformed`), the trailing newline, the 4097-byte path, `\` and C1 paths accepted, and non-canonicalizable values (`value_not_canonicalizable`);
  - boundary `classification`: every row of the Phase 1 classification and effects rules, including the I3 case and the `route` outcome with finding `legacy_protocol_routed`;
  - each vector carries `applies_to: [producer, consumer]`, and the known answers carry `derived_origin: hand`.
- [x] T010 [P] Write failing `tests/council_convening/test_validator_cli.py`:
  - exits 0, 1, 2 and 3, where 3 is a routed record and never a pass;
  - the finding-line format;
  - every Phase 1 proof-of-work note in contracts/validator-cli.md;
  - `corpus --json` shape;
  - `check` on a legacy record exits 3 with `council-convening-legacy-protocol-routed`, and on a replacement record of a kind not landed yet exits 1 with `council-convening-kind-unknown`;
  - `check` judges the registry instances by their `kind` and never classifies them (N7);
  - the self-test exits 0 when every route vector's route matches its `expected`.
- [x] T011 [P] Write failing `tests/council_convening/test_gate_wiring.py` against `.github/workflows/council-convening-gate.yml`:
  - job id `council-convening-gate` with no `name:` key;
  - `pull_request` and `push` triggers on `main`;
  - installs `requirements/hermes-runtime-contracts.lock` with `--require-hashes`;
  - runs the validator;
  - a positive assertion step requiring every Phase 1 proof-of-work note;
  - no `secrets` context and no `id-token`.

### Implementation

- [x] T012 Widen `$defs/digest_subject` in `contracts/signed-execution-chain/digest-construction.schema.yaml`:
  - append exactly `council_convening` and `council_seat_return_payload`;
  - add a comment in the file's tranche style naming `renew-resolved-council-protocol` D1/D3 and what each subject is taken over;
  - subjects are added; no construction is added (R3).
- [x] T013 Mirror both subjects in `scripts/signed_execution_chain/canonical.py` `SUBJECTS`, with the same comment.
- [x] T014 Refresh the `signed-execution-chain-digest-construction` row `sha256` in `contracts/manifest.yaml` to the new bytes:
  - add a row comment;
  - make no version and no CHANGELOG change. A row moves with its bytes, and the version is the cutting session's act, as the row's own comment already records.
  - Update the one existing test that pins the enumeration, `tests/signed_execution_chain/test_anchor_event_settlement.py` (`test_the_anchoring_digest_subjects_are_enumerated_once`, lines 490–495). It asserts `subjects[28:]` is the six daily-batch subjects and the length is 34. It becomes `subjects[28:34] ==` those six, `subjects[34:] == ["council_convening", "council_seat_return_payload"]`, and a length of 36. No other test pins the count (`grep -rn "== 34" tests scripts` finds only an unrelated trust-anchor positives count).
  - Then run, green: `python3 -m pytest tests/signed_execution_chain tests/clearing tests/code_surface tests/intent-compliance tests/manifest_digests -q`, `python3 scripts/validate-signed-execution-chain.py` and `python3 scripts/validate-clearing-dispatch.py` (G5).
- [x] T015 Author `contracts/council-convening/shared-definitions.schema.yaml`:
  - house header: `schema_version`, `kind: openxfactory-council-convening-contract-schema`, `name`, `$schema`, and an `$id` under `https://xforge.us/schemas/openxfactory/council-convening/v1/`;
  - `contract_id`, `contract_schema_version: 1`, `title`, `description`;
  - every definition in data-model § Shared definitions, with `digest` taken by `$ref` to the construction file;
  - `refusal_code` holding the five Phase 1 codes, and `finding_code` holding `legacy_protocol_routed`.
- [x] T016 Author `contracts/council-convening/protocol-registry.schema.yaml` and the closed instance `contracts/council-convening/protocol.registry.yaml`, per data-model E1 and research R10. The legacy entry has status `in_use`, the replacement has status `available`, and every tag field is `null`.
- [x] T017 Implement `scripts/council_convening/records.py`:
  - the schema registry, using `Draft202012Validator`, `FormatChecker` and `referencing.Registry`;
  - whole-match identifier enforcement;
  - the canonicalizability pre-check through `canonical.serialize`;
  - a `Refused(code, member)` exception whose messages never echo values.
- [x] T018 Implement `scripts/council_convening/classification.py`: classification and the selection-dependent effects of data-model E1, from the written rules only.
- [x] T019 Implement `scripts/council_convening/corpus.py`:
  - index loading, closure and raw-byte digests;
  - `$parts` join;
  - a dispatch table by `boundary`, with the `definition` and `classification` handlers registered here and later handlers registered by later modules;
  - exact outcome, refusal, finding and `derived` comparison;
  - coverage at the commit, and the `registry_status` rule.
- [x] T020 Implement `scripts/council_convening/generate.py`:
  - deterministic JSON writing: sorted keys, 2-space indent, LF, one trailing newline;
  - labelled test-key derivation, a SHA-256 of a fixed public phrase plus a label, used as the Ed25519 seed, with signing through `cryptography`;
  - no seed or private key is ever written;
  - writing `contracts/council-convening/conformance/index.json` from the vectors, with `coverage_floor` set to FR-001 and FR-011;
  - `--check`, which regenerates into a temporary tree and byte-compares (R18).
- [x] T021 Implement `scripts/validate-council-convening.py`:
  - a thin CLI over the package, with the self-test, `check` and `corpus` modes;
  - finding format, notes and exit codes per contracts/validator-cli.md, including exit 3 for a routed record;
  - `select` and `--historical` are added in Phase 6, and an unknown subcommand is argparse's exit 2.
- [x] T022 Add `.github/workflows/council-convening-gate.yml` per R17, with a header stating that the gate reports and does not gate until the owner requires it.
- [x] T023 Run quickstart steps 1–5. Record base and head runs in `evidence.md` § Phase 1: the red counts, the green counts, the validator notes, the OpenSpec totals, the doc-health diff, the pytest selected, passed and skipped counts, and the empty PR-scope diff. Open PR-1 as a draft, stating the unblocks above.

**Checkpoint**: The validator self-test passes on the foundation corpus. Successors can read the protocol identifiers and the classification rule at a reviewed commit.

---

## Phase 2: User Story 1 — Agree on membership before work (P1) — MVP (PR-2)

**Goal**: the commission record and its provenance reproduce identically in independent implementations, and every refusal happens before work or assignment (spec US1; FR-001–FR-004; D1, D2).

**Independent test**: `python3 scripts/validate-council-convening.py` adjudicates every `resolution` vector. Every positive yields the expected `required_seats` and `convening_digest`, and every negative yields exactly its code, in the normative order.

**Unblocks**:

- 049: T003 (a corpus to pin), T010 (payload shape, refusal mapping and order), T011 (the gate-rules candidate as `subject_path`), T011b (the POST body's provider half, with 025), T012 (the head-race half), T013.
- 025: FR-001–FR-004.

**Depends on**: Phase 1.

### Tests first

- [x] T024 [P] [US1] Write failing `tests/council_convening/test_predicates.py`:
  - `changed_paths_intersect` and `rule_touches_security_posture`, by those identifiers (OPEN-5), each holding and not holding;
  - every pattern-grammar refusal;
  - the bare-directory evidence rule;
  - the entry-count completeness rule, where one rename is one entry and two paths, and a declared total above 3000 is unevaluable;
  - unevaluable is never false;
  - the wrong input contract;
  - an unknown predicate.
- [x] T025 [P] [US1] Write failing `tests/council_convening/test_resolution.py`:
  - the closed E2 shape, and classification before shape;
  - the data-model E2 evaluation order, with multi-defect records that pin each adjacent pair of steps;
  - class selection from `class_inputs`: exact and glob head refs, each glob rule, first match wins, and a declared but unselected class refused as `class_mismatch` (U1);
  - `class_inputs.head_ref` that differs from `environment.head_refs` refused as `candidate_mismatch` (N1);
  - an unclassed council (the gate-rules shape) with no class inputs accepted, and class inputs on an unclassed council, or none on a classed one, refused as `class_mismatch` (N4);
  - the source set: an omitted source and an extra source, each refused as `governed_sources_mismatch` (R4-H3);
  - governed sources under the OPEN-3 ruling and follow-up 1: a `governed.repository` that is not allowlisted, including a former spelling, refused as `rule_unauthorized` before any `governed_history` read (the oracle records no read); a revision off the first-parent history (`rule_revision_ungoverned`); at admission, a file changed at the tip, and a listing whose entry set changed at the tip (`rule_superseded`), including a source that is not the rule file (U2; N3); an unrelated, non-listed file changed at the tip, accepted; and no `rule_superseded` outcome at commission, where it is a non-normative producer pre-check;
  - roster composition: standing order; held seats appended; a conditional seat already standing appears once; an unbound held seat refuses; an empty roster; a duplicate seat; a reordered roster; a same-count substitution;
  - fact sources, including a gate-rules shape whose `rule_facts` come from `candidate.subject_path` at `candidate.head_sha` (I1);
  - consumed, unused and absent facts; secrets via `$parts`, before any oracle is queried with a free-text value of the record;
  - candidate identity against `inputs.expected_candidate` and `environment.resolved_candidate`;
  - head moved before the recheck, after the recheck, and at admission; head unavailable;
  - `convening_digest` known answers.
- [x] T026 [US1] Author the `resolution` vectors, creating `contracts/council-convening/conformance/vectors/resolution/` with the first of them, with their expected outcomes before any implementation.
  - Positives: standing only; a conditional seat held; a conditional seat not held; an unclassed gate-rules council with a `rule_facts` conjunction held; a conditional seat already standing; both rename paths; a class selected by glob.
  - At least one negative per Phase 2 refusal code, and the multi-defect order vectors.
  - Shared resolution checks use boundary `commission` and carry `applies_to: [producer, consumer]`. A consumer runs one through its admission resolution with no binding step: each shared commission vector carries both `inputs.expected_candidate` and an `environment.resolved_candidate` consistent with it, a single-entry `live_heads`, and no binding (contracts/conformance-corpus.md § How each side runs a shared vector). A vector whose `live_heads` gives more than one read, to model drift between the producer's reads, is producer-only. Shared commission vectors carry no `rule_superseded` case.
  - Admission vectors are `applies_to: [consumer]`, because from Phase 5 admission also runs the consumer's binding checks. Pre-submit drift is producer-only. Admission drift is consumer-only. No vector's `expected` depends on 025's guards at E2 steps A2 and A5, which run as passing seams in a corpus run (data-model E2), and no multi-defect vector pairs one of them with another defect.
  - Raise `coverage_floor` to add FR-002–FR-004 and SC-001, keeping Phase 1's FR-001 and FR-011, and regenerate `conformance/index.json`.
- [x] T027 [P] [US1] Extend `tests/council_convening/test_validator_cli.py`: `check` runs the offline E2 rules, reports each oracle-dependent rule as not offline-checkable, and the self-test prints the predicate-registry note.

### Implementation

- [x] T028 [US1] Author `contracts/council-convening/predicate-registry.schema.yaml` and the closed instance `contracts/council-convening/predicate.registry.yaml`, per data-model E3 and research R5, with the ruled identifiers. Extend `refusal_code` in `contracts/council-convening/shared-definitions.schema.yaml` with the Phase 2 codes (G1).
- [x] T029 [US1] Author `contracts/council-convening/council-convening.schema.yaml`, per data-model E2.
- [x] T030 [US1] Implement `scripts/council_convening/predicates.py` from E3's written semantics only. No code is copied from codexFactory (R4).
- [x] T031 [US1] Implement `scripts/council_convening/resolution.py`:
  - the E2 evaluation order, every provenance check and roster composition;
  - the injected oracle interface (R8);
  - the secret check through `importlib` of `SECRET_PATTERNS` in `scripts/validate-domain-factory.py` (R9);
  - `convening_digest`.
- [x] T032 [US1] Register the `commission` and `admission` handlers in `scripts/council_convening/corpus.py`. Add the offline E2 rules to `check` in `scripts/validate-council-convening.py`. Add the predicate-registry note to the gate's assertion in `.github/workflows/council-convening-gate.yml` and its test.
- [x] T033 [US1] Measure the secret floor gap (I13). Run the four patterns 049 detects and the floor lacks over every tracked file, and record the hits in `evidence.md` § Phase 2. File the floor widening as its own follow-up issue on opensoft/openxFactory, citing R9. Do not widen `SECRET_PATTERNS` in this PR.
- [x] T034 [US1] Run quickstart steps 1–5 and record them in `evidence.md` § Phase 2, including the agreement-set count, and cite follow-up 1, "Every governed source (Recommended)", as the ruling the source-currency vectors encode. Open PR-2 as a draft.

**Checkpoint**: The MVP. Producer and consumer can each prove membership agreement against one reviewed commit, while staying dormant.

---

## Phase 3: User Story 2 (a) — Frozen assignments and retry identity (P1) (PR-3)

**Goal**: one immutable assignment per required seat, in roster order, with retry identity and a frozen roster (the frozen-roster half of spec US2 scenario 4; US1 scenario 4's retry; FR-004, FR-005; D2). Completion over the frozen identities (US2 scenario 3, and the completion half of scenario 4) reads signed returns, whose schema is Phase 4's, so it lands there.

**Independent test**: every `assignment` vector adjudicates. Extra, missing, reordered and same-count wrong assignments refuse; an identical retry returns the same snapshot even after the governed tip or the live head moved; a different record for the same key is `convening_conflict`.

**Unblocks**:

- 049: T012 (retry identity), T015b (the provider half of the snapshot and assignment encodings), T016b (the public assignment shape).
- 025: FR-005–FR-007.

**Depends on**: Phase 2.

### Tests first

- [x] T035 [P] [US2] Write failing `tests/council_convening/test_assignments.py`:
  - E4 and E5 shapes, and the E4 order;
  - one assignment per seat, in roster order: extra, missing and reordered refused as `assignment_set_mismatch`, as is an assignment whose convening members differ from the snapshot's;
  - duplicate `assignment_id`;
  - shared holder;
  - `convening_digest` recomputation (`digest_construction_mismatch`);
  - the ruled ceiling (OPEN-1): an assignment lifetime of exactly 21600 seconds accepted; 21601 seconds, zero and a negative lifetime refused as `assignment_malformed`;
  - `permitted_operations`: a non-empty, duplicate-free subset of `[seat_key_registration, seat_return]` in that order; an empty, repeated, reordered or unknown list refused as `assignment_malformed`;
  - retry, as E2 step A3 over `environment.issued.live_snapshots`: an identical E2 returns the same snapshot; a different one is `convening_conflict`, keyed on `(protocol, council_id, subject_pin)` (025's once-per-pin key), including a record that differs only in `candidate.pull_number` or `candidate.subject_path`, while a record for the same council at another pin is not a conflict; an identical E2 resent after a governed source changed at the tip, or after the live head moved, still returns the same snapshot, because retry identity runs before every drift check (US1 scenario 4; 025 FR-006); and once-per-pin never pre-empts an identical retry;
  - `assignment_malformed` at its E4 position, before the digest and set checks.
- [x] T036 [US2] Author the `assignment` vectors, creating `contracts/council-convening/conformance/vectors/assignment/` with the first of them, with their expected outcomes first, including the four ceiling vectors. Raise `coverage_floor` to add FR-005, FR-006 and SC-002, and regenerate the index.
- [x] T037 [P] [US2] Extend `tests/council_convening/test_validator_cli.py`: `check` on a snapshot recomputes its digest and its assignment set.

### Implementation

- [x] T038 [US2] Author `contracts/council-convening/convening-snapshot.schema.yaml` and `contracts/council-convening/seat-assignment.schema.yaml`, per data-model E4 and E5, with the assignment lifetime ceiling of 21600 seconds. Extend `refusal_code` in `contracts/council-convening/shared-definitions.schema.yaml` with the Phase 3 codes.
- [x] T039 [US2] Implement `scripts/council_convening/assignments.py`, including retry identity and once-per-pin (E2 step A3).
- [x] T040 [US2] Register the snapshot-at-`admission` handler in `scripts/council_convening/corpus.py`, insert retry identity (E2 step A3) into the Phase 2 `admission` handler (T032) right after E2 step 2, and extend `check` in `scripts/validate-council-convening.py`. From Phase 5, T055 puts binding (A1) before it. The `completion` handler is Phase 4's (T048).
- [x] T041 [US2] Run quickstart steps 1–5, record them in `evidence.md` § Phase 3, and open PR-3 as a draft.

---

## Phase 4: User Story 2 (b) — Assignment-bound key registration and signed returns (P1) (PR-4)

**Goal**: possession proofs and returns bind protocol, convening, council, candidate, assignment, seat and digest. Wrong principals, shared keys, replay, challenge misuse, root authorization and cross-protocol bytes all refuse, and completion runs on exactly the frozen identities (spec US2 scenarios 1–3, and the completion half of scenario 4; FR-005–FR-008; D3).

**Independent test**: every `signing` vector adjudicates, with `signed_bytes` known answers matching. `generate --check` reproduces every signature byte for byte.

**Unblocks**:

- 049: T020 (signing-context strings and shapes, and the decimal-string payload), T017/T019 (mapping the producer-internal contexts), T021/T022 (completion mapping), T025 (what the consumer's evidence must show).
- 025: FR-008–FR-010.

**Depends on**: Phases 3 and 5. Phase 5 lands first, because registration checks a seat job's claims against its holder's binding (data-model E7 step 5).

### Tests first

- [ ] T042 [P] [US2] Write failing `tests/council_convening/test_signing.py`:
  - contexts rebuilt from the frozen assignment, challenge and key, compared member by member with the presented context, never trusting its labels;
  - the E7 and E8 orders, with multi-defect records;
  - `signed_bytes` known answers, including one registration and one return context whose signed bytes are hand-authored (`derived_origin: hand`), so the generator is not checked only against itself (N9);
  - fingerprint recomputation, and the challenge's `key_fingerprint`;
  - stdlib `ed25519.verify`;
  - registration refusals: `root_authorization_refused` before `registration_malformed`; the seat job's claims checked against its holder's binding at E7 step 5: a `binding_ref` that resolves to nothing (`binding_unresolved`), a `governed_broker_job` holder (`broker_capability_insufficient`), a stub binding (`binding_malformed`), `claims_unverified`, `claims_expired`, `audience_mismatch`, and a seat workflow commit before the frozen revision or off the governed history (`workflow_revision_ungoverned`, follow-up 3) (R4-H1; R4-M3); `wrong_principal` with a valid proof; already registered; `shared_key`; cross seat, cross convening and cross protocol, each told apart by the presented context; proof invalid;
  - challenge refusals, over `environment.issued.challenges` and in the E7 order: unknown, malformed, wrong assignment, consumed, expired at the instant;
  - key transport (spec delta, "key transport MUST refuse"): a registration or a return carrying a member named `private_key`, `secret_key`, `seed`, `sk` or `d`, or a PEM private-key block, refused as `registration_malformed` or `return_malformed` (N18);
  - a return context whose `key_fingerprint` differs, refused as `return_key_mismatch` (N16);
  - a `payload` above 1 MiB of canonical bytes, refused as `return_malformed`;
  - the ruled ceiling (OPEN-1): a challenge lifetime of exactly 600 seconds accepted; 601 seconds, zero and a negative lifetime refused as `challenge_malformed`;
  - assignment use: not yet valid, expired at the instant, and operation not permitted, shown with a one-operation assignment (a registration against `[seat_return]`, a return against `[seat_key_registration]`);
  - return refusals: unregistered, key mismatch, digest mismatch, signature invalid, replay into another assignment, convening or protocol, and a float in the payload refused as `value_not_canonicalizable` while a `decimal_string` is accepted;
  - legacy v1 signed bytes never verify as replacement bytes, and the reverse;
  - completion, moved here from Phase 3 because it reads E8 returns: unlisted, duplicate, missing and same-count wrong identity, in the E8 completion order; and a changed rule oracle after freezing, where completion still follows the snapshot.
- [ ] T043 [P] [US2] Write failing `tests/council_convening/test_corpus_regeneration.py`:
  - `generate --check` is byte-identical;
  - no corpus member at any depth is named `seed`, `private_key`, `secret_key`, `sk` or `d` (U10: keyed by member name, because every SHA-256 is also 32 bytes);
  - every corpus file is clean under the provider's `SECRET_PATTERNS`.
- [ ] T044 [US2] Generate the `signing` vectors with the T020 generator, which already derives the labelled test keys and signs, creating `contracts/council-convening/conformance/vectors/signing/` with the first of them, with their expected outcomes authored first. Include the four challenge-ceiling vectors, which carry `applies_to: [consumer]` because the consumer issues challenges (N23), and the hand-authored signed-bytes answers. The ceiling vectors are at the contract ceiling: a consumer's tighter configured value applies when it issues a challenge, and never changes a vector's outcome (R12). Include the `completion` vectors. Raise `coverage_floor` to add FR-007, FR-008 and SC-003, and regenerate the index.
- [ ] T045 [P] [US2] Extend `tests/council_convening/test_validator_cli.py`: `check` verifies a record's signature where the record carries one, and reports registration-state rules as not offline-checkable.

### Implementation

- [ ] T046 [US2] Author `contracts/council-convening/registration-challenge.schema.yaml` (challenge lifetime ceiling 600 seconds), `contracts/council-convening/seat-key-registration.schema.yaml`, `contracts/council-convening/seat-return.schema.yaml` and `contracts/council-convening/signing-context.schema.yaml`, per data-model E6–E9. Extend `refusal_code` in `contracts/council-convening/shared-definitions.schema.yaml` with the Phase 4 codes, which include the completion codes and `binding_unresolved` and `broker_capability_insufficient` (data-model § Refusal vocabulary).
- [ ] T047 [US2] Implement `scripts/council_convening/signing.py`:
  - reuse `canonical.serialize` and `ed25519.verify`;
  - the estate fingerprint spelling;
  - no second framing (R3).
- [ ] T048 [US2] Register the `registration`, `return` and `completion` handlers in `scripts/council_convening/corpus.py`. Make `check` in `scripts/validate-council-convening.py` verify a record's signature where the record carries one.
- [ ] T049 [US2] Run quickstart steps 1–5, record them in `evidence.md` § Phase 4, citing follow-up 3, "At or after the frozen rev (Recommended)", for the seat-rule vectors, and open PR-4 as a draft.

---

## Phase 5: User Story 2 (c) — Producer identity bound to verified workflow claims (P1) (PR-5)

**Goal**: the producer's authority is bound to the current governed repository identity and to verified issuer, audience, subject and workflow claims. A workflow ref is never a subject, and an unverified broker parks activation (FR-009; D4).

**Independent test**: every `binding` vector adjudicates against the identity map it carries in its `repository_identity` oracle: the corpus's frozen identity fixture, never the live `contracts/policies/repository-identity.yaml`, so an edit to the live map moves no vector and fails no `generate --check` (R8; R7-M1).

**Unblocks**:

- 049: T023, T024, T031 (the shape the owner provisions into the consumer's runtime configuration, under OPEN-2).
- 025: FR-008 (principal-authentication inputs), and H3's activation park.

**Depends on**: Phases 2 and 3 for landing; it may be authored in parallel from Phase 1. It lands after Phase 3, because binding runs inside admission and T051 re-authors every admission vector at that commit, and before Phase 4, which uses its claim checks.

### Tests first

- [ ] T050 [P] [US2] Write failing `tests/council_convening/test_binding.py`:
  - the E10 shape and the E10 binding order, with its offline half (steps 1–6) and its claim half (steps 7–14);
  - the verified claims against the binding (R3-H2; D3 "signed issuer/audience/expiry"): another `iss` refused as `issuer_mismatch`, another `aud` as `audience_mismatch`, an `exp` at or before `evaluation_time` or an `nbf` after it as `claims_expired`, and another `sub` as `subject_template_mismatch`;
  - a former spelling in a permitted `job_workflow_ref` refused as `repository_identity_former` (R3-L9);
  - repository derivation through `load_transfers` in `scripts/estate_inventory.py`, for `caller_repository`: an absent map, an unreadable map, and a map with a malformed row each refused as `repository_identity_unavailable`, because `load_transfers` itself returns an empty map for the first two; the former spelling refused as `repository_identity_former`; a non-canonical case variant, defined as equal to a listed spelling ignoring ASCII case but not byte-equal, refused as `repository_identity_former`; a spelling the map does not list accepted as current; a verified `repository` or `repository_id` claim that differs from the binding refused as `repository_identity_mismatch` (N11);
  - the issuer: the standard URL and an enterprise-slug URL accepted, anything else refused (I6);
  - audience and subject wildcards;
  - a subject template customized with the `job_workflow_ref` and `repository_id` claim keys accepted; a bare workflow reference as the template (the `<owner>/<repo>/.github/workflows/<file>@<ref>` shape with no `key:` element) refused as `subject_workflow_conflation`, which runs before the parse check; any other template that does not parse refused as `subject_template_mismatch` (I6; N15; R3-H1);
  - an unlisted workflow, and a `sub` that contains a permitted workflow reference while the verified `job_workflow_ref` names an unlisted one, both refused as `workflow_not_permitted` (N15);
  - the seat rule (follow-up 3, "At or after the frozen rev (Recommended)"): a seat job's `job_workflow_sha` at or after the frozen revision on the governed history accepted, one before it or off that history refused as `workflow_revision_ungoverned`, and a commission entry paired with the seat rule refused as `binding_malformed` (R4-H1);
  - the ruled workflow-revision rule (OPEN-3 and follow-up 2, "job_workflow_ref's repo (Recommended)"): the estate's calling pattern, a caller repository running the governed repository's reusable workflow at `governed.revision`, accepted; an unequal `job_workflow_sha`, and a permitted workflow whose repository is not the governed repository, refused as `workflow_revision_ungoverned` (N2);
  - decoded-only claims;
  - a binding whose `broker.capability_verified` is `false` is accepted at binding, which records it; it is refused only at `activation` and `resume` (Phase 6, E12);
  - the `.template.yaml` stub is never accepted as live;
  - the corpus index check: a `binding`, `registration` or Phase-5 `admission` vector without the `repository_identity` oracle refused as `council-convening-vector-identity-map-missing`, failing first (R7-L1), like T008's `registry_status` rule;
  - the frozen identity fixture: `conformance/fixtures/repository-identity.json` is an index `fixtures` row with a matching digest, every map-reading vector's `text` equals the fixture's, and `generate --check` passes unchanged when `contracts/policies/repository-identity.yaml` is removed or edited in a temporary copy of the tree, because it never reads the live map (R7-M1).
- [ ] T051 [US2] Author the `binding` vectors, creating `contracts/council-convening/conformance/vectors/binding/` with the first of them, with their expected outcomes first. Because binding now runs inside admission (data-model E2), re-author every admission vector at that commit, Phase 2's and Phase 3's, to carry a passing binding and verified claims, and add admission vectors that pin the interleaved order: a binding defect with a step-3 defect; a workflow-revision defect with a step-5 defect (R3-M4; R4-M1; R4-H2); and an identical retry whose commission token fails binding, which refuses with the binding code and does not return the snapshot (A1 before A3). Author the frozen identity fixture `contracts/council-convening/conformance/fixtures/repository-identity.json` first, with one complete transfer row and one `pending` row, and register it in the index's `fixtures`. Author the three `repository_identity_unavailable` vectors with the `repository_identity` oracle's `absent` and `unreadable` states and a `text` with a malformed row. Every other vector that reads the map, the re-authored admission vectors included, carries the fixture's text, as generated. Raise `coverage_floor` to add FR-009, and regenerate the index.
- [ ] T052 [P] [US2] Extend `tests/council_convening/test_validator_cli.py`: `check` validates a binding instance offline against `repository-identity.yaml`, refuses the stub as live, and reports the claim-verification rules as not offline-checkable.

### Implementation

- [ ] T053 [US2] Author `contracts/council-convening/producer-binding.schema.yaml` and `contracts/council-convening/producer-binding.template.yaml`. `workflow_revision_rule` is the closed enumeration `[equals_governed_revision, on_governed_history_since_revision]`, the first for `commission` and the second for `seat_execution`, any other pairing being `binding_malformed` (OPEN-3; follow-up 3). The closed set of subject claim keys is enumerated from GitHub's OIDC reference, which the schema's description cites. The template carries `instantiation_stub: true` and no live audience, subject template or repository id. Extend `refusal_code` in `contracts/council-convening/shared-definitions.schema.yaml` with the Phase 5 codes.
- [ ] T054 [US2] Implement `scripts/council_convening/binding.py`, reusing `load_transfers`. No second transfer map. Add the fail-closed check `load_transfers` lacks: before calling it, confirm the map exists and reads and parses under the same strict loader, so an absent or unreadable map is `repository_identity_unavailable` and is never taken for a valid empty one; and any malformed row it reports is `repository_identity_unavailable` too. A well-formed map with no transfer rows is valid. The corpus adapter honours the `repository_identity` oracle's overrides by materializing them under a temporary root.
- [ ] T055 [US2] Register the `binding` handler in `scripts/council_convening/corpus.py`, and run binding inside the `admission` handler: E10 steps 1 to 13 as E2 step A1, after shape, and step 14 as E2 step A4, after E2 step 5 has checked `governed` (R3-M4; R4-M1). Add the identity-map rule and the `fixtures` closure to the corpus index check (`council-convening-vector-identity-map-missing`; contracts/validator-cli.md), make the generator read the identity fixture and never the live map, and `check` support for the offline half. Document the binding in `contracts/council-convening/README.md`, including the OPEN-2 ruling: the concrete instance lives in the consumer's governed runtime configuration, written at the provisioning act and validated at the consumer's pin.
- [ ] T056 [US2] Run quickstart steps 1–5, record them in `evidence.md` § Phase 5, citing follow-ups 2 and 3 for the workflow-revision vectors, and open PR-5 as a draft.

---

## Phase 6: User Story 3 — Activate and recover the matched pair (P2) (PR-6)

**Goal**: one explicitly selected protocol per binding, with no fallback. Legacy is recognized for refusal and routing. Pair matching, activation evidence and the paired-rollback runbook are defined (spec US3; FR-011, FR-012; D5).

**Independent test**: every `migration` vector adjudicates. Every vector whose outcome reads a registry status carries a `registry_status` override, so the corpus digest does not move when Phases 7 and 8 flip the registry.

**Unblocks**:

- 049: T027 (the selection shape), T028, T029 (the runbook its quickstart mirrors), T032 (the rehearsal-record shape).
- 025: FR-011, FR-012.

**Depends on**: Phases 2–5.

### Tests first

- [ ] T057 [P] [US3] Write failing `tests/council_convening/test_migration.py`:
  - every row of the data-model E1 effects table, under each registry status, by override;
  - `deprecated` routes with the findings `[legacy_protocol_routed, legacy_protocol_deprecated]`, an error under `--strict`; `historical_only` refuses any legacy selection, in either mode (N6; N17);
  - `--historical` classifies and never reinterprets: a legacy record routes (exit 3), and a replacement record verifies;
  - E11: `mode`, a `null` bundle only in rehearsal, pair matching on all five members, `replacement_not_admission_eligible` before the major;
  - `rejected_without_fallback`, from `inputs.rejected_under` and a later `inputs.selection_attempt` that names another protocol;
  - E12 per act, in the activation order: `activation_evidence_malformed`; each act's required members (`activation_evidence_incomplete`); then, for an activation or resume, `binding_refs` equal to the configured binding set in `inputs.bindings` (one omitted is `activation_evidence_incomplete`), each entry resolved against it (`binding_unresolved`) and its binding's `broker` member read as the one source of broker capability (`broker_capability_insufficient` when `capability_verified` is not `true` or `evidence_ref` is `null`), before the pair comparison; an activation record carries no broker state of its own; activation and resume need a passing matched rehearsal, found through `rehearsal_ref` in `inputs.rehearsal`; the two sides' selections compared on the five matched values; `rehearsal_ref` hashed over the exact text of `inputs.rehearsal`; a passing rehearsal whose provider or matched values differ from the activation's refused as `activation_evidence_incomplete` (R4-M5); a rollback with no `binding_refs` accepted; a rollback with `new_records_retained: false` refused as `activation_evidence_incomplete`, and one whose `new_records_protocol` is not the replacement refused as `historical_reinterpretation_refused` (N5; N19; R3-M2; R3-M6).
- [ ] T058 [US3] Author the `migration` vectors, creating `contracts/council-convening/conformance/vectors/migration/` with the first of them, with their expected outcomes first. Raise `coverage_floor` to the full FR-001–FR-012 and SC-001–SC-003, and regenerate the index.
- [ ] T059 [P] [US3] Extend `tests/council_convening/test_validator_cli.py`: `select` exits and findings; `check --historical` exits 0 on a replacement record and 3 on a legacy one; and the full-coverage note.

### Implementation

- [ ] T060 [US3] Author `contracts/council-convening/protocol-selection.schema.yaml` and `contracts/council-convening/activation-evidence.schema.yaml`, per data-model E11 and E12. Extend `refusal_code` with the Phase 6 codes and `finding_code` with `legacy_protocol_deprecated` in `contracts/council-convening/shared-definitions.schema.yaml`.
- [ ] T061 [US3] Implement `scripts/council_convening/migration.py`. Add the `select` and `check --historical` modes to `scripts/validate-council-convening.py`.
- [ ] T062 [US3] Write `docs/council-convening-activation-runbook.md` with headers `Status: ratified` and `Ratified by: renew-resolved-council-protocol`, and link it from the `README.md` document index. This is the runbook's one index link. It covers, in order:
  1. pause commissioning;
  2. drain or explicitly cancel in-flight convenings;
  3. switch both selections to one E11 value set;
  4. both sides run the full corpus at the same index digest, in a matched rehearsal;
  5. activate or resume only on a matched, verified pair;
  6. paired rollback that keeps new records as audit evidence.

  Each act is an owner act, recorded as an E12 record of its own `act`.
- [ ] T063 [US3] Run quickstart steps 1–5, record them in `evidence.md` § Phase 6, and open PR-6 as a draft.

**Checkpoint**: The family is complete on `main`, dormant and unregistered. Both successors can finish dormant implementations against one reviewed commit.

---

## Phase 7: Release A — the additive and deprecating minor (PR-7)

**Purpose**: publish the family, with the replacement `available`, the legacy protocol `deprecated`, and the family inside the release inventory behind its floor (R15, R19; § Change Classes).

**Unblocks**:

- 049: T030 (the minor half); T003 and the `stack.yaml` pin on a published bundle.
- 025: FR-011 and FR-012 (a compatible published pin).

**Depends on**: Phases 1–6 merged.

- [ ] T064 Claim the contract-cut shared substrate on openxFactory's pinned "Shared substrates — claims" issue. Then fetch and merge `origin/main`. Then allocate the next available minor from `contracts/manifest.yaml` at that moment, re-checking tag availability (Bundle Realization Order step 1). Record the allocation in `evidence.md`.

### Tests first

- [ ] T065 [P] Write failing `tests/council_convening/test_council_convening_manifest_rows.py`:
  - every family schema, both registries and `conformance/index.json` carry a row;
  - the rows are closed in both directions;
  - each row's digest is recomputed.
- [ ] T066 [P] Write failing `tests/hermes_runtime_contracts/test_council_convening_release_floor.py`, under the OPEN-4 ruling:
  - below `COUNCIL_CONVENING_RELEASE_FLOOR`, no family path is a member;
  - at or after the floor, the family, validator, package and tests are members;
  - every published inventory up to the previous tag still verifies.
- [ ] T067 [P] Update `tests/council_convening/test_protocol_registry.py` to the minor, failing first: legacy `deprecated`; `introduced_in` and `deprecated_in` naming the allocated tag; `removed_in` still `null` (G2).

### Implementation

- [ ] T068 Add the `COUNCIL_CONVENING_RELEASE_FLOOR` block to `scripts/hermes_runtime_validation/release.py`, set to the allocated version, in the clearing block's form.
- [ ] T069 In `contracts/council-convening/protocol.registry.yaml`, flip legacy to `deprecated` and write the allocated tag into the `introduced_in` and `deprecated_in` fields. No corpus vector changes, because of the `registry_status` rule.
- [ ] T070 Register the manifest rows in `contracts/manifest.yaml`: `canonical_openxfactory_contract`, `adapter_owner: openxFactory`, and a `consumption_rule` naming the pin recipe in contracts/provider-interface.md. Bump `contract_bundle_version` to the allocated tag.
- [ ] T071 Write the `contracts/CHANGELOG.md` entry for the additive and deprecating minor:
  - what is added;
  - what is deprecated;
  - the removal named as the next major, written concretely;
  - the migration path.

  Write the § *Deprecations Currently In Force* entry in `docs/contract-versioning-policy.md`, from the refusal list.
- [ ] T072 [P] Change the family's rows in the `contracts/README.md` native contract index and the family README's row in the `README.md` document index from "pending realization" to registered at the allocated tag. Add no second runbook link.
- [ ] T073 Build `contracts/releases/<allocated>.digests.yaml` with `scripts/validate-contract-release.py build`. Then run, against the exact candidate:
  - `verify-commit` and `verify-promotion`;
  - the release-tag gate;
  - the supported-domain regression denominator;
  - quickstart steps 1–6.

  Record everything in `evidence.md` § Phase 7.
- [ ] T074 Open PR-7 as a draft into `main`. It carries exactly `scripts/hermes_runtime_validation/release.py`, `contracts/council-convening/protocol.registry.yaml`, `contracts/manifest.yaml`, `contracts/CHANGELOG.md`, `docs/contract-versioning-policy.md`, `contracts/README.md`, `README.md`, `contracts/releases/<allocated>.digests.yaml`, `tests/council_convening/test_council_convening_manifest_rows.py`, `tests/council_convening/test_protocol_registry.py`, `tests/hermes_runtime_contracts/test_council_convening_release_floor.py` and `specs/035-renew-resolved-council-protocol/evidence.md`. It lands only on Brett Heap's word, on the plain gate, at the exact reviewed commit.
- [ ] T075 **OWNER**: publish the annotated tag at the landed commit (Bundle Realization Order step 5). Record `verify-tag --remote origin --tag <allocated>` from an independently refreshed checkout in `evidence.md`. The box stays unticked.

---

## Phase 8: Release B — the removal major (PR-8)

**Purpose**: refuse legacy for active selection, keep historical classification, and make the replacement admission-eligible (R19; FR-011).

**Unblocks**:

- 049: T030 (the major half); prerequisites for T033 and T034.
- 025: FR-011 (old shapes refused at the major) and FR-012.

**Depends on** all four of:

- T075's dated evidence recorded;
- at least one full minor served;
- both successors' dormant implementations verified against the published minor (049 T013/T035 and 025 evidence, cited and not claimed);
- the owner's release act.

- [ ] T076 Record the four preconditions with citations in `evidence.md` § Phase 8. Stop if any is missing.
- [ ] T077 Claim the contract-cut substrate, merge `origin/main`, and allocate the next major from `contracts/manifest.yaml` at that moment. Record it in `evidence.md`.

### Tests first

- [ ] T078 [P] Update `tests/council_convening/test_protocol_registry.py` and `tests/council_convening/test_migration.py`, failing first:
  - legacy `historical_only`, and an active legacy selection refused;
  - `--historical` still classifies legacy records and routes them;
  - the replacement is `admission_eligible`;
  - `removed_in` names the allocated major;
  - every family file's `contract_schema_version` is still `1` (G3; R19).

### Implementation

- [ ] T079 In `contracts/council-convening/protocol.registry.yaml`, flip the statuses and set `removed_in`.
- [ ] T080 Write the BREAKING `contracts/CHANGELOG.md` entry with its migration note, citing the published minor as the served deprecation window. Write the § *Deprecations Executed* entry in `docs/contract-versioning-policy.md`. Process every other § *Deprecations Currently In Force* entry that targets this major (three target `contract-v5.0` today: the flat `hermes` keys, the credential `consumer:` block, and the unresolvable `requirement_ref`), restating each or executing it under its own pre-authorized text. Phase 8 decides none of those acts.
- [ ] T081 Re-baseline `contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml` against the actual union of supported consumers, per the policy's § Supported-Domain Regression Denominator.
- [ ] T082 Last, after every other Phase 8 edit: refresh the `sha256` of every `contracts/manifest.yaml` row whose file Phase 8 changed, at least `contracts/council-convening/protocol.registry.yaml` (G3). The regression inventory has no manifest row; its identity travels in the release inventory (N13). Bump `contract_bundle_version` to the allocated major. Build `contracts/releases/<allocated>.digests.yaml`. Run quickstart steps 1–6 and record them in `evidence.md` § Phase 8.
- [ ] T083 Open PR-8 as a draft into `main`. It carries exactly `contracts/council-convening/protocol.registry.yaml`, `contracts/manifest.yaml`, `contracts/CHANGELOG.md`, `docs/contract-versioning-policy.md`, `contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml`, `contracts/releases/<allocated>.digests.yaml`, `tests/council_convening/test_protocol_registry.py`, `tests/council_convening/test_migration.py` and `specs/035-renew-resolved-council-protocol/evidence.md`, plus any file a restated or executed deprecation entry names. It lands only on Brett Heap's word.
- [ ] T084 **OWNER**: publish the major's annotated tag at the landed commit. Record `verify-tag` in `evidence.md`. The box stays unticked.

---

## Phase 9: Closeout (PR-9)

**Purpose**: provider realization evidence handed to the governance packet. The archive stays gated on successor and activation evidence (change tasks 3.1–3.5).

- [ ] T085 In `specs/035-renew-resolved-council-protocol/evidence.md`, record:
  - each phase's merged commit;
  - both releases' corpus digests;
  - the validator outputs;
  - the 049 and 025 evidence references, cited and not claimed.
- [ ] T086 Report the change's task 3.1 acceptance evidence to the change's owner lane. Leave 3.2–3.5 to their owner and archive acts. No implementation phase edits anything under `openspec/changes/renew-resolved-council-protocol/`; ticking 3.1 is the owner lane's act, as #1268's tick of 2.2 was (N10).
- [ ] T087 Re-run `speckit-analyze` over the final artifacts, and update `specs/035-renew-resolved-council-protocol/analysis.md`. In the README's OpenSpec Records block in `README.md`, update this feature's own sentence, inside a Rule 6 window.

---

## Dependencies and execution order

```text
#1267 landed (80f47483) ──► #1268 (this plan) lands ──► Phase 1 ──► Phase 2 ──► Phase 3 ──┐
                                                                         │                ├──► Phase 4 ──► Phase 6 ──► Phase 7 ──► [OWNER tag] ──► Phase 8 ──► [OWNER tag] ──► Phase 9
                                                                         └──► Phase 5 ────┘
Landing order: 1, 2, 3, 5, 4, 6, 7, 8, 9. Phase 5 is authored beside Phases 2–3, lands after Phase 3, and lands before Phase 4.
```

The order within a phase:

1. tests, vectors and CLI tests, run red and recorded;
2. schemas, with the `refusal_code` extension;
3. the package module;
4. handlers and CLI;
5. gates and evidence;
6. the PR.

## Parallel opportunities

- **Phase 1**: T003–T011 in parallel, then T012–T022 in order (T012→T013→T014 are one invariant).
- **Phase 2**: T024 ∥ T025 ∥ T027, then T026. T028 ∥ T029, then T030→T031→T032. T033 beside them.
- **Phase 3**: T035 ∥ T037, then T036, then T038→T039→T040.
- **Phase 4**: T042 ∥ T043 ∥ T045, then T044, then T046→T047→T048.
- **Phase 5**: authored beside Phases 2–3 (T050–T055). Its corpus index is regenerated when it merges after Phase 3, and it lands before Phase 4.
- **Phase 7**: T065 ∥ T066 ∥ T067 ∥ T072 once T064 holds the claim.

## Implementation strategy

- **MVP**: Phases 1–2, which deliver the membership agreement. They let 049's T003 and T010 and 025's FR-001–FR-004 proceed dormant at a reviewed commit.
- **Increments**: each later phase adds one consumer-facing artifact class and its vectors, and lands alone.
- **Publication**: comes only through Phases 7 and 8. Activation stays outside this feature entirely.

## Requirement coverage

| Requirement | Tasks |
|---|---|
| FR-001 | T005, T006, T009, T015, T016, T025, T029 |
| FR-002 | T024, T025, T026, T028, T029, T030, T031 |
| FR-003 | T019, T025, T026, T031, T033 |
| FR-004 | T025, T035, T036, T039 |
| FR-005 | T035, T036, T039 (frozen assignments); T042, T044, T048 (completion) |
| FR-006 | T035 (public assignment, unique holder), T042 (shared key), T046 (no secret member) |
| FR-007 | T035, T038, T042, T046, T047, T050 |
| FR-008 | T007, T012, T013, T042–T048 |
| FR-009 | T050–T055 |
| FR-010 | T004, T008, T009, T011, T019–T022, T026, T036, T044, T051, T058, T065 |
| FR-011 | T006, T009, T016, T018, T057–T061, T066–T071, T078–T081 |
| FR-012 | T057, T060, T062, T075, T084 |
| SC-001 | T019, T026, T036, T044, T051, T058; the successors' evidence is external |
| SC-002 | T035, T036; the consumer's database evidence is external (025) |
| SC-003 | T042, T043, T044 |
| SC-004 | T060, T062; the owner's rehearsal is external |

The spec delta's seven requirements map as follows:

| Spec-delta requirement | Phase |
|---|---|
| Resolved roster | Phase 2 |
| Reproducible provenance | Phase 2 |
| Frozen assignments | Phase 3 |
| Candidate across submission and admission | Phase 2 |
| Independent signing authority | Phase 4 |
| Verified workflow binding | Phase 5 |
| Versioned coordinated migration | Phases 1 and 6–8 |
