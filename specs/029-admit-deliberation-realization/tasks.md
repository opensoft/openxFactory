# Tasks: `deliberation` — register entry two and its neutral return schema

**Input**: Design documents from `/specs/029-admit-deliberation-realization/`
**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/deliberation-return.md](./contracts/deliberation-return.md), [quickstart.md](./quickstart.md)

**Lane**: `hermes-wallet-exercise`

**Tests ARE requested.** The ratified `tasks.md` Phase 2 names the assertion each
item must satisfy, and this family's own rule is that a refusal with no fixture
and no test is not implemented.

**Mapping.** Each task below names the ratified Phase 2 item it discharges. The
ratified `tasks.md` is the governance record and is ticked with the sha that
realized it; THIS file is the executable list. Neither restates the other.

## OUT OF SCOPE

See [spec.md](./spec.md) § Out of Scope: no `opensoft/xFactory` byte, no
`opensoft/codexFactory` byte, no host job, no route retirement, no attestation
fixture refresh, no annotated tag, no archive.

---

## Phase 1: Packet

- [X] T001 Author `specs/029-admit-deliberation-realization/` — spec, plan,
      research (with OPEN POINTS), data-model, the contract note, quickstart,
      this file, and the quality checklist.
- [X] T002 Open the pull request as a DRAFT with `Lane: hermes-wallet-exercise`
      as the first line of the body, the authority, the claim link, the allocated
      minor, and the statement that the tag is the owner's act.

## Phase 2: The five frozen copies and the fixture re-point — ONE diff (ratified 2.1, 2.3, 2.4, 2.7)

- [ ] T003 `contracts/clearing/permitted-operations.registry.yaml`: ENTRY NUMBER
      TWO with every fact of [data-model.md](./data-model.md) § 1; advance
      `registry_version` 1 → 2; REWRITE the header comment — the "EXACTLY ONE
      MEMBER TODAY" and "`deliberation` IS NOT HERE ON PURPOSE" paragraphs become
      the record of when and by what it arrived, `coding` is named as the
      deliberately-absent later member, and the HONEST LIMIT paragraph is
      retained. *(ratified 2.1, copy 3 of 5)*
- [ ] T004 `scripts/validate-clearing-dispatch.py`:
      `RATIFIED_OPERATIONS = frozenset({"readiness-diagnostic", "deliberation"})`
      and the constant's comment rewritten. *(copy 1 of 5)*
- [ ] T005 `tests/clearing/test_register_closure.py`: the INDEPENDENT `RATIFIED`
      copy gains the member — **not** imported from the validator; the
      independence is the control. *(copy 2 of 5)*
- [ ] T006 `.github/workflows/clearing-dispatch-gate.yml`: the literal grep
      `\(1 registered operation\)` → `\(2 registered operations\)`, and the
      comment above it rewritten to say what moved it. *(copy 4 of 5)*
- [ ] T007 `tests/clearing/test_clearing_gate_wiring.py::test_the_assertion_pins_the_registers_literal_member_count`:
      the pinned literal moves with T006. *(copy 5 of 5)*
- [ ] T008 The validator's register-read note pluralizes correctly so the gate's
      new literal is the one the reader actually prints.
- [ ] T009 [P] `tests/clearing/test_register_closure.py`: entry-two twins of
      `test_the_entry_declares_every_ratified_fact` and of the lanes test (ONE
      lane; `token_scopes == ["actions:read"]`; the new `output_schema_ref`;
      `data_handling == "internal-governance"`), and an assertion that
      `registry_version == 2`. *(ratified 2.1)*
- [ ] T010 [P] `examples/negative/register-carrying-an-unratified-operation.yaml`
      → `coding`, comments rewritten to argue about `coding`. *(ratified 2.4)*
- [ ] T011 [P] `examples/negative/manifest-naming-an-unregistered-operation.yaml`
      → `coding`, comments rewritten. *(ratified 2.4)*
- [ ] T012 `tests/clearing/test_register_closure.py::test_deliberation_is_refused_by_name`
      RENAMED `test_coding_is_refused_by_name` and re-pointed, docstring argument
      intact. *(ratified 2.4)*
- [ ] T013 [P] `examples/dispatch-record-refused.example.yaml` → a refused claim
      of `coding`, comments rewritten; and
      `tests/clearing/test_dispatch_record.py::test_a_refusal_records_what_was_asked_for`
      moves in the same commit. *(ratified 2.7)*
- [ ] T014 RUN, do not read:
      `examples/negative/dispatch-record-with-a-free-text-refusal-ground.yaml`
      still fires `clearing-record-refusal-ground-unknown`. *(ratified 2.4's
      "expecting NO change")*

## Phase 3: The new neutral schema, its routing, and the verdict scan (ratified 2.2, 2.5)

- [ ] T015 Author `contracts/clearing/deliberation-return.schema.yaml` per
      [data-model.md](./data-model.md) § 2 and
      [contracts/deliberation-return.md](./contracts/deliberation-return.md).
- [ ] T016 `scripts/validate-clearing-dispatch.py`: add the file to
      `SCHEMA_FILENAMES` and the kind
      `xfactory_clearing_deliberation_return` to `KIND_TO_SCHEMA`. **This row is
      what makes the shape check exist at all.**
- [ ] T017 EXTRACT the `VERDICT_WORDS` name scan into one shared function and
      call it from both the operation-report path and a new
      `check_deliberation_return`; dispatch the new kind in `validate_record`.
      **NO new finding code** — the refusal is the existing
      `clearing-report-carries-a-verdict`.
- [ ] T018 [P] `contracts/clearing/examples/deliberation-return.example.yaml` —
      the positive, validating clean.
- [ ] T019 [P] `examples/negative/deliberation-return-that-does-not-match-its-shape.yaml`
      declaring `# expected_failure: schema`.
- [ ] T020 [P] `examples/negative/deliberation-return-carrying-a-verdict.yaml`
      declaring `# expected_failure: clearing-report-carries-a-verdict`.
- [ ] T021 `tests/clearing/test_schemas.py`: `test_the_family_ships_five_schemas`
      → SIX, renamed, with the new filename in the exact list; and
      `test_the_corpus_covers_every_shipped_kind` gains the new kind.
- [ ] T022 [P] `tests/clearing/` gains assertions for the new shape: the binding
      triple is required, the root and every nested object are closed, a
      verdict-named member at depth is refused, and the schema is meta-valid and
      self-identifying (the parametrized suites cover the last one for free).

## Phase 4: The three refusal grounds (ratified 2.9)

- [ ] T023 `contracts/clearing/dispatch-record.schema.yaml`:
      `$defs.refusal_ground.enum` 2 → 5, with the `$defs` description and the
      schema header paragraph rewritten — "two members today" becomes five, the
      nine-awaited list shrinks to six, each new member names the change that
      admitted it, and THE RENDERING RULE is written down.
- [ ] T024 `tests/clearing/test_dispatch_record.py::test_the_refusal_grounds_are_exactly_the_two_the_realization_emits`
      → the five, renamed, with the docstring's argument carried forward.
- [ ] T025 [P] A packaged record naming each new ground validates clean — proven
      by test rather than by three more example files.

## Phase 5: Bookkeeping that moves with the bytes (ratified 2.10, and Phase 3's 3.2/3.3)

- [ ] T026 `contracts/manifest.yaml`: the new row `clearing-deliberation-return`
      with its digest; the register instance's and the dispatch-record schema's
      row digests recomputed; the clearing-family header comment's corpus counts
      corrected to the MEASURED values; `contract_bundle_version` →
      `contract-v3.4`.
- [ ] T027 `tests/clearing/test_clearing_manifest_rows.py`: `EXPECTED_ROWS` 6 → 7,
      the count test renamed, the per-row registration assertion re-expressed so
      each row records the release that registered IT.
- [ ] T028 `contracts/releases/contract-v3.4.digests.yaml`, MACHINE-WRITTEN by
      `python3 scripts/validate-contract-release.py build --tag contract-v3.4`
      and re-derived at the integration point. **Never hand-edited.**
- [ ] T029 [P] `contracts/clearing/README.md`: the register section stops saying
      "exactly one member" and stops saying `deliberation` is deliberately
      absent; the shape table gains the return schema; the corpus counts move;
      the honest-limit paragraph is retained and extended to name the gate's grep
      AND the test that pins it as copies four and five.
- [ ] T030 [P] `contracts/README.md`: the two clearing index rows move.
- [ ] T031 [P] `contracts/CHANGELOG.md`: one entry, class **ADDITIVE (minor)**,
      written from a MEASURED diff against `contract-v3.3`, naming anything that
      moved on `main` between the tag and this base so a reader does not
      attribute it to this cut.
- [ ] T032 `tests/intent-compliance/test_release_boundary.py`: `ReleaseState`
      gains `FEATURE_SUCCESSOR_8 = "contract-v3.4"` with the by-hand paragraph
      every previous cut added.

## Phase 6: Proof and ticks

- [ ] T033 Prove each of the FIVE frozen copies fails ALONE — revert exactly one,
      five times, observe red, restore. *(ratified 2.6)*
- [ ] T034 Prove each of the THREE pinned numerals fails alone — the schema list,
      the manifest row count, the row digests. *(ratified 2.6)*
- [ ] T035 Green: `python3 scripts/validate-clearing-dispatch.py .` (0/0, 2
      registered operations, 26/26 red-proven);
      `python3 -m pytest tests/ -q -m "not postgres"`;
      `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`; the doc-health
      single-repo run. *(ratified 2.11)*
- [ ] T036 Tick `openspec/changes/admit-deliberation-clearing-operation/tasks.md`
      Phase 2 items 2.1–2.11, each with the sha that realized it. **Phase 3's tag
      and Phase 4's downstream items are NOT ticked here.**
- [ ] T037 `gh pr ready`, then watch the checks.
