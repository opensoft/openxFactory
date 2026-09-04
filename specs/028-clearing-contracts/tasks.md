# Tasks: contracts/clearing — the neutral clearing-dispatch contract family

**Input**: Design documents from `/specs/028-clearing-contracts/`
**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/validator-cli.md](./contracts/validator-cli.md), [quickstart.md](./quickstart.md)

**Tests ARE requested.** `add-clearing-dispatch-boundary` `tasks.md` §6.7 names
`tests/clearing/` explicitly, and SC-002 makes an untested refusal an
unimplemented one.

## OUT OF SCOPE — stated here so a reviewer can check the boundary

Carried verbatim in substance from the ratified `code_surface` paragraph of
`add-clearing-dispatch-boundary`, which names each of these as NOT this surface:

- **`realize-factory-bundle-packaging`** — the codexFactory hosted packaging
  workflow that produces a conformant sealed bundle. Named successor.
- **The CODING operation** and its register entry. It arrives with the packaging
  realization that produces its bundles.
- **The HOSTED FINALIZER** for patch-returning operations. Gated on the above:
  `readiness-diagnostic` returns nothing a finalizer would validate, and a
  finalizer written against no returning operation is written against a guess.
- **Any runner, runner group, dispatch label, host, or credential.** Those are
  operator surface and already exist.
- **The `deliberation` register member** (codexFactory #165). A LATER governed
  change; T018's refusal is what keeps it out of this cut.
- **Any `opensoft/xFactory` workflow change** — the clearing lane, the
  grandfather enumeration, the L4 authoring-time guard, the L5 attestation
  IMPLEMENTATION. This feature ships the attestation RECORD SHAPE only.
- **The `sealed_return` digest subject** named in `add-cpc-clearing-boundary`
  `tasks.md` §2.9. Nothing here computes a digest over a sealed return; see
  research.md R4.
- **Any spec delta.** This is a realization. It authors no requirement, adds no
  `## MODIFIED Requirements` block, and therefore should move no `sequenced_after`
  sweep pin.
- **The annotated `contract-v3.3` tag.** Bundle Realization Order step 5, at the
  LANDED commit, after `verify-commit` is re-run there.

---

## Phase 1: Setup

- [X] T001 Initialize the pinned key decoders with `git submodule update --init openXwallet` from the repo root, and confirm `openXwallet/scripts/validate-openxwallet.py` exists — the validator REFUSES without it and never falls back.
- [X] T002 [P] Create the family directory skeleton `contracts/clearing/` and `contracts/clearing/examples/negative/` in the repository root.
- [X] T003 [P] Create the test package directory `tests/clearing/` in the repository root.

---

## Phase 2: Foundational (blocking prerequisites)

**⚠️ Every user story below depends on these. The manifest schema cannot cite a
digest subject that does not exist, and no shape can be validated before the
family's header conventions are fixed.**

- [X] T004 Widen `$defs/digest_subject` in `contracts/signed-execution-chain/digest-construction.schema.yaml` by exactly one member, `sealed_bundle_manifest`, with a tranche-3 comment in the file's own established style naming `add-cpc-clearing-boundary`'s requirement as the basis — SUBJECTS widen, `construction_name` is untouched, and no second construction is declared.
- [X] T005 Add `"sealed_bundle_manifest"` to the `SUBJECTS` frozenset in `scripts/signed_execution_chain/canonical.py` with the same tranche comment, so the reader's frozen copy admits what the contract admits.
- [X] T006 [P] Write `contracts/clearing/README.md` carrying `Status: ratified` + `Ratified by: add-clearing-dispatch-boundary` (the `contracts/worker-enrollment/README.md` header form), the family's purpose, the closed-register governance statement ("adding an operation is a governed contract change, not a workflow edit"), the HONEST LIMIT of the closure tripwire, and the out-of-scope list above.

---

## Phase 3: User Story 1 — A clearing implementation can validate a sealed bundle manifest (Priority: P1) 🎯 MVP

**Goal**: the ten declared fields become a schema, the register becomes something
the manifest can be resolved against, and the canonical validator turns "the
boundary refuses X" into a command that exits non-zero and names X.

**Independent test**: `python3 scripts/validate-clearing-dispatch.py` exits `0` on
the packaged positives and each negative fixture fails for its declared code.

### Schemas

- [X] T007 [P] [US1] Author `contracts/clearing/sealed-bundle-manifest.schema.yaml` — the ten declared fields per data-model.md §1, `additionalProperties: false`, `expires_at` required, `selected_files` requiring a byte-tagged `content_hash` per file, and field (10) as the two-variant tagged union whose `origin_signature` variant carries `manifest_digest` with `construction: xfc-jcs-sha256-1` and `subject: sealed_bundle_manifest` and a `covered_fields` array of the ten field tokens.
- [X] T008 [P] [US1] Author `contracts/clearing/permitted-operations.schema.yaml` — `registry_id` const `clearing-permitted-operations`, `registry_version`, and the operation-entry shape of data-model.md §2 with every declaration the ratified entry list names.
- [X] T009 [US1] Author the CLOSED instance `contracts/clearing/permitted-operations.registry.yaml` with EXACTLY ONE member, `readiness-diagnostic`, populated from the ratified text and the live realization constants (worker profile, two lanes with their literal groups/labels/expected runners, class constraints `no checkout / no writes / no secrets / no token scopes / 5-minute timeout`, `output_schema_ref`, `data_handling: public_log_only`, `repository_affecting_output: false`), with a file header stating that a second member is a governed contract change.

### Validator

- [X] T010 [US1] Create `scripts/validate-clearing-dispatch.py` with the house skeleton: module docstring naming the ratified basis, `Findings` dataclass emitting `ERROR [code]` / `WARN  [code]` / `note  `, `build_registry()` over the family schemas using `Draft202012Validator` + `FormatChecker` + `referencing.Registry`, `argparse` CLI (`path` optional, `--strict`), `report()`, and exit codes `0/1/2` per contracts/validator-cli.md.
- [X] T011 [US1] In `scripts/validate-clearing-dispatch.py`, add the reuse imports and their refusals: `from scripts.signed_execution_chain import canonical, ed25519` after pushing `ROOT` onto `sys.path`, and `load_pinned_reader()` importing `openXwallet/scripts/validate-openxwallet.py` by `importlib.util.spec_from_file_location` and exiting `2` with the `git submodule update --init openXwallet` remedy when absent.
- [X] T012 [US1] In `scripts/validate-clearing-dispatch.py`, implement the register reader: load the instance, assert its members are a subset of the frozen ratified set (`clearing-register-member-unratified`), assert each entry is complete (`clearing-register-entry-incomplete`), refuse a `repository_affecting_output: false` entry that declares a repository effect (`clearing-readonly-entry-claims-effect`), and emit the positive note naming the file and the registered-operation count.
- [X] T013 [US1] In `scripts/validate-clearing-dispatch.py`, implement the manifest cross-shape rules: ten-field completeness naming the missing field, per-file hash presence, byte-tagged-not-JCS hash refusal, expiry against a declared evaluation instant, digest construction/subject, unknown operation, lane not permitted by the entry, and bundle-versus-register disagreement on worker profile / lane / output schema / handling — the register GOVERNS and the dispatch proceeds on neither value.
- [X] T014 [US1] In `scripts/validate-clearing-dispatch.py`, implement origin-signature resolution against `governance/factory-identity/` (path overridable for fixtures): resolve the originating repository's active row, refuse hosted-provenance-alone for a registered producer (`clearing-origin-signature-missing`), accept it for an unregistered one, verify the signature over `canonical.digest` of the signable subject with `ed25519.verify` against the key decoded by the PINNED decoder (`clearing-origin-signature-invalid`), and refuse a `covered_fields` short of ten (`clearing-origin-signature-partial`).

### Examples

- [X] T015 [P] [US1] Author `contracts/clearing/examples/sealed-bundle-manifest-registered-producer.example.yaml` (origin-signature variant, a REAL verifying signature from an ephemeral key whose private half is never written to the repository) and `contracts/clearing/examples/sealed-bundle-manifest-unregistered-producer.example.yaml` (hosted-provenance variant).
- [X] T016 [P] [US1] Author `contracts/clearing/examples/permitted-operations-registry.example.yaml` — the fixture register the self-test resolves against, plus `contracts/clearing/examples/factory-identity-fixture/` holding the fixture origin register and wallet for the packaged signature, so the LIVE `governance/factory-identity/` tree is never a self-test dependency.
- [X] T017 [US1] Author the negative fixtures for US1's refusals, one file per code, each with a `# expected_failure: <code>` header and a comment naming the ratified scenario it discharges, under `contracts/clearing/examples/negative/`: missing field, missing per-file hash, JCS-tagged file hash, expired handle, wrong digest construction, unregistered operation, lane not permitted, bundle-disagrees-with-register, origin signature missing, origin signature invalid, origin signature partial.
- [X] T018 [US1] Author `contracts/clearing/examples/negative/register-carrying-an-unratified-operation.yaml` (`# expected_failure: clearing-register-member-unratified`) using `deliberation` as its unratified member, with a comment naming codexFactory #165 as the LATER governed change this refusal keeps out.

### Tests

- [X] T019 [P] [US1] Write `tests/clearing/test_schemas.py` — every family schema is meta-valid Draft 2020-12, declares `$schema` and an absolute `$id`, and every packaged positive example validates against the schema its `kind` names.
- [X] T020 [P] [US1] Write `tests/clearing/test_register_closure.py` — the shipped instance holds exactly one member; a copy with `deliberation` added is refused with `clearing-register-member-unratified`; a copy with a member removed still passes (closure shrinks, never grows).
- [X] T021 [US1] Write `tests/clearing/test_validator_refusals.py` — load the validator by `importlib`, assert every negative fixture fails for its declared code, and assert every member of the validator's closed `REFUSAL_CODES` is red-proven by at least one fixture.
- [X] T022 [P] [US1] Write `tests/clearing/test_digest_by_reference.py` — `sealed_bundle_manifest` is a member of BOTH the chain schema's `digest_subject` enum and `canonical.SUBJECTS`; the manifest schema's digest members match the chain's `$defs/digest` structurally; no file under `contracts/clearing/` declares a `construction_name`.
- [X] T023 [US1] Write `tests/clearing/test_origin_signature.py` — a registered producer with a verifying signature passes; hosted provenance alone from a registered producer is refused by name; hosted provenance from an unregistered producer passes; fixture keys are derived from labelled sha256 digests except the one ephemeral verifying key, and no test skips under any condition.

**Checkpoint**: US1 is independently shippable — the manifest, the closed register
and the validator together make the boundary machine-checkable.

---

## Phase 4: User Story 2 — The register reads as closed to a reviewer (Priority: P1)

**Goal**: a reviewer can determine from the tree alone that one operation is
registered and that adding a second is refused mechanically.

**Independent test**: read `contracts/clearing/README.md` and
`permitted-operations.registry.yaml`; run the T020 closure test.

- [X] T024 [US2] Extend `contracts/clearing/README.md` with the register's own section: the one member, each declaration it carries and the ratified sentence requiring it, the governed-change rule for adding a member, and the TRIPWIRE-NOT-UNFORGEABLE honesty statement the ratified L4 requirement demands of the equivalent mechanism.
- [X] T025 [US2] Add the entry-completeness probe to `tests/clearing/test_register_closure.py`: the shipped `readiness-diagnostic` entry declares operation id, may/may-not semantics, all five class constraints, worker profile, at least one lane with a literal group and label, an output schema ref, a data-handling class, and `repository_affecting_output: false`.

---

## Phase 5: User Story 3 — Dispatches and refusals share one record shape (Priority: P2)

**Goal**: one ledger shape for admissions and refusals, resolved beside claimed,
grounds from a closed enumeration, disposal evidence as a field.

**Independent test**: validate the cleared and refused positive examples, then the
free-text-ground and empty-disposal negatives.

- [X] T026 [US3] Author `contracts/clearing/dispatch-record.schema.yaml` per data-model.md §4, with the three DISJOINT verification groups (`provider_verified`, `policy_checked`, `origin_signature`), `lane_declarations` whose member names carry DECLARED, `refusal.ground` as a snake_case enum seeded with EXACTLY `unregistered_operation` and `unknown_lane_selector`, a REQUIRED non-empty `workspace_disposal`, a nullable `chain_ref`, and a description naming `contracts/schemas/dispatch-record.schema.yaml` as the different record it is not.
- [X] T027 [US3] Extend `scripts/validate-clearing-dispatch.py` with the ledger cross-shape rules: `clearing-record-refusal-ground-unknown`, `clearing-record-cleared-with-refusal`, `clearing-record-disposal-unattested`, and `clearing-record-policy-field-reported-verified`.
- [X] T028 [P] [US3] Author `contracts/clearing/examples/dispatch-record-cleared.example.yaml` and `contracts/clearing/examples/dispatch-record-refused.example.yaml`, the second carrying `unregistered_operation` and the claimed operation recorded AS CLAIMED.
- [X] T029 [P] [US3] Author the US3 negative fixtures under `contracts/clearing/examples/negative/`: a free-text refusal ground, a cleared record carrying a refusal, an empty `workspace_disposal`, and a record reporting a policy-checked field inside the provider-verified set.
- [X] T030 [US3] Add `tests/clearing/test_dispatch_record.py` — the refusal-ground enum holds exactly the two seeded members; a bundle-less record types group, label and handling as declared and offers no observed counterpart; the four US3 refusals fire by name.

---

## Phase 6: User Story 4 — The single door is attestable, and the three findings stay distinct (Priority: P2)

**Goal**: a record shape that can express a widening, a dark lane and
not-yet-converged without conflating them.

**Independent test**: validate the positive attestation carrying all three finding
classes; validate the dark-lane-as-breach negative.

- [X] T031 [US4] Author `contracts/clearing/single-door-attestation.schema.yaml` per data-model.md §5 — the expected set as a PER-GROUP member with no estate-wide counterpart, `finding_class` a closed three-member enum, and `completeness_claim.strength` distinguishing the pre- and post-admission claims.
- [X] T032 [US4] Extend `scripts/validate-clearing-dispatch.py` with `clearing-attestation-expected-set-not-per-group`, `clearing-attestation-dark-lane-as-breach` and `clearing-attestation-overclaims-completeness`.
- [X] T033 [P] [US4] Author `contracts/clearing/examples/single-door-attestation.example.yaml` carrying one widening, one dark lane and one not-yet-converged finding across the two governed groups, and the US4 negative fixtures (dark lane filed as a widening; an estate-wide expected set; `full_post_admission` claimed while a convergence finding stands).
- [X] T034 [US4] Add `tests/clearing/test_attestation.py` asserting the three finding classes are exactly the enum, and that each US4 refusal fires by name.

---

## Phase 7: User Story 5 — The operation report is composed evidence, never a verdict (Priority: P2)

**Goal**: one composed report of record per dispatch, per-lane facts as a keyed
collection, group and label typed as DECLARED, and no eligibility verdict.

**Independent test**: validate the composed positive report; validate the verdict
and environment-dump negatives.

- [X] T035 [US5] Author `contracts/clearing/operation-report.schema.yaml` per data-model.md §3, with `lanes` a keyed collection, `declared` naming group/label/expected runner, `environment` restricted by `propertyNames` to the ratified NAME ALLOWLIST, `compute` carrying both the computed and expected digests, and a description refusing any member that would make it the awaited infrastructure-readiness result.
- [X] T036 [US5] Extend `scripts/validate-clearing-dispatch.py` with `clearing-report-carries-a-verdict`, `clearing-report-environment-not-allowlisted` and `clearing-report-lane-reported-as-observed`.
- [X] T037 [P] [US5] Author `contracts/clearing/examples/operation-report-both-lanes.example.yaml` built from the names the live clearing lane emits, plus the US5 negative fixtures (a verdict member, an unallowlisted environment name, an observed-group member).
- [X] T038 [US5] Add `tests/clearing/test_operation_report.py` asserting the report is one composed record across two lanes, that the allowlist is exactly the ratified nine names, and that each US5 refusal fires by name.

---

## Phase 8: User Story 6 — A consumer can pin the family at a numbered release (Priority: P3)

**Goal**: registration on all three surfaces at `contract-v3.3`.

**Independent test**: `scripts/validate-manifest-digests.py` and the per-family
digest test pass; `validate-contract-release.py verify-commit` verifies the new
inventory at HEAD.

- [X] T039 [US6] RE-MEASURE the next available minor at the branch tip before writing any number (`contracts/manifest.yaml:contract_bundle_version`, `ls contracts/releases/`, `git ls-remote --tags origin`, open PRs) and record the measurement in the CHANGELOG entry; allocate `contract-v3.3` only if it is still free.
- [X] T040 [US6] Register every `contracts/clearing/*.schema.yaml` with `type: schema` and `contracts/clearing/permitted-operations.registry.yaml` with `type: registry` in `contracts/manifest.yaml`, each row carrying `id`, `path`, `source_path`, `schema_version`, a recomputed `sha256`, `compatibility: canonical_openxfactory_contract`, `adapter_owner: openxFactory` and a `consumption_rule`, under a family header comment stating that the validator, README and examples are content-addressed by commit; bump `contract_bundle_version` to the allocated minor.
- [X] T041 [US6] Add the two `contracts/README.md` "Native Contract Index" rows — one for the family's schemas, one for the validator + examples + tests bundle — in the shape the `signed-execution-chain` rows use.
- [X] T042 [US6] Write the `contracts/CHANGELOG.md` entry for the allocated minor on the `contract-v2.5` new-family template: attribution to both ratified changes with their PR/squash, a MEASURED additive-class justification, the added-artifact inventory, what the release does NOT confer (registration is not enforcement; the release-inventory membership asymmetry), the FRESH-COUNTED bundle-number evidence from T039, and the statement that the annotated tag is published at the LANDED commit per Bundle Realization Order step 5.
- [X] T043 [US6] Build the inventory with `python3 scripts/validate-contract-release.py build --tag contract-v3.3 --output contracts/releases/contract-v3.3.digests.yaml`, then verify it with `verify-commit --commit $(git rev-parse HEAD)`.
- [X] T044 [US6] Write `tests/clearing/test_clearing_manifest_rows.py` (named for the family because `tests/signed_execution_chain/` already claims the bare basename, and neither directory is a package) closed in BOTH directions — an `EXPECTED_ROWS` map of every family schema plus the registry instance, an assertion that the manifest's clearing rows equal that set, an assertion that every `contracts/clearing/**/*.schema.yaml` and the `.registry.yaml` on disk carries a row, and a parametrized per-row `sha256` recomputation compared as `str()`.

---

## Phase 9: CI wiring

- [X] T045 Add `.github/workflows/clearing-dispatch-gate.yml` in the `signed-execution-chain-gate.yml` pattern — job id `clearing-dispatch-gate` with NO `name:` key, `pull_request`/`push` on `main`, `permissions: {contents: read}`, the App-token mint + ssh-URL rewrite + checkout + scoped `git submodule update --init openXwallet` preamble, `setup-python` 3.12, `pip install pyyaml jsonschema rfc3339-validator`, `python3 scripts/verify-openxwallet-pin.py`, then the validator over `.` piped through `tee clearing-gate.log`.
- [X] T046 Add the POSITIVE assertion step to `.github/workflows/clearing-dispatch-gate.yml`: grep the log for the pinned-decoder note, the register-read note with its literal count, the self-test note, the `K/K closed refusal codes red-proven` line and the repo-scan note, and assert no `ERROR [` line survives — a green check that opened nothing is a vacuous pass.
- [X] T047 [P] Write `tests/clearing/test_clearing_gate_wiring.py` (family-named for the same collision reason as T044) pinning the workflow's job id and the exact validator `run:` string, in the shape `tests/openxwallet_consumer_gate/test_gate_invocation.py` uses.

---

## Phase 10: Governance bookkeeping and polish

- [X] T048 Tick `openspec/changes/add-clearing-dispatch-boundary/tasks.md` §6.1–6.8 for exactly what this realization lands, each tick carrying the realization reference (PR + branch) in the house `**DONE <date>** —` inline form, and leave §7 (the L5 attestation implementation) and §8 (successors) untouched.
- [X] T049 Add a dated realization note to `openspec/changes/add-clearing-dispatch-boundary/proposal.md` recording that the neutral half is realized by this PR, in the same filed-forward correction style the packet already uses — the front matter's `target_release` line is NOT rewritten, it is annotated.
- [X] T050 [P] Add the family to the `contracts/README.md` doc index / repository README linkage wherever the house links a new family, and confirm no other index goes stale. **NO ROOT-README ROW, and the precedent is measured rather than assumed:** the root `README.md` doc index lists SOME families (`omnigent`, `worker-enrollment`, `memory-gateway`) and not others — `signed-execution-chain`, the most recent comparable family, has no row there and is referenced from the narrative instead. The authoritative family index is `contracts/README.md`'s "Native Contract Index And Pending Realization" table, which gains BOTH house rows (the family, and the validator + corpus + tests bundle). No other index went stale; the seven doc-health families report no new finding.
- [X] T051 Run the gates: `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`, `python3 scripts/proposal-support.py . verify`, `python3 scripts/validate-clearing-dispatch.py .`, `python3 scripts/validate-manifest-digests.py`, and the doc-health families prior work uses (proposal-origin, status-validity, location-conformance, modified-block-currency, promotion-fidelity, standard-backing, document-catalog).
- [X] T052 Run `python3 -m pytest tests/ -q -m "not postgres"` in the FOREGROUND once at the end (~20 min) and confirm no new failure and NO new skip — `pytest-suite.yml` pins the skipped count exactly while selected/passed are floors.
- [X] T053 Confirm the `sequenced_after` sweep pin did NOT move: this realization adds no `## MODIFIED Requirements` block. If a pin moved anyway, re-derive it in the house style with a dated reason rather than reverting it.

---

## Dependencies & Execution Order

- **Setup (T001–T003)** → everything.
- **Foundational (T004–T006)** → every user story. T004/T005 are ONE logical
  change in two files and must land together; T007 cites the subject they add.
- **US1 (T007–T023)** is the MVP and blocks nothing else structurally, but T010's
  validator skeleton is extended by T027, T032 and T036, so US1's validator tasks
  precede those.
- **US2 (T024–T025)** depends on T009 and T020.
- **US3 (T026–T030)**, **US4 (T031–T034)** and **US5 (T035–T038)** are mutually
  independent once T010 exists, and may be worked in any order.
- **US6 (T039–T044)** depends on EVERY contract file being final: a `sha256` row
  is only correct once its file stops moving.
- **CI (T045–T047)** depends on the validator being complete.
- **Polish (T048–T053)** last.

## Parallel Opportunities

- T002 ‖ T003.
- T007 ‖ T008 (different files, no shared members).
- T019 ‖ T022 (independent test files).
- T028 ‖ T029; T033 alone; T037 alone — each story's examples are independent of
  the others'.
- T047 ‖ T050.

Nothing in Phase 8 is parallel: the manifest, README, CHANGELOG and inventory are
one atomic release surface per `docs/contract-versioning-policy.md` step 2.

## Implementation Strategy

**MVP = US1.** The manifest schema, the closed register and the canonical
validator are what turn the ratified boundary into something a machine refuses.
Everything after it adds a record shape the boundary will need when an
implementation writes one, and none of it changes what US1 already enforces.

**Increment order**: US1 → US2 (documentation of what US1 built) → US3/US4/US5 in
any order → US6 (registration, once nothing moves) → CI → bookkeeping.
