# Tasks: repository identity — `opensoft/codexFactory` becomes `codeXfactory/codexFactory` in governed content

**Input**: Design documents from `/specs/030-realize-codexfactory-identity/`
**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/](./contracts/), [quickstart.md](./quickstart.md)

**Lane**: `provenance-autonomous-merge`
**Governing change**: `adopt-codexfactory-repository-identity` (ratified 2026-09-07, merged PR #763 `eb30db7a`)
**Runbook**: `~/session-prompts/runbook-codexfactory-org-transfer.md` step **10.2**

**Tests**: this feature ships no new tests. It moves existing pinning
assertions (`PINNED_TABLE`, two `PINNED_REPOSITORY` constants, the live-register
assertions) in the same commit as the artifact each pins, which is the packet's
own red-by-construction mechanism. Every task is proved by a validator or an
existing suite, per constitution principle V.

**THIS LANE MERGES NOTHING.** Every task below completes at *pull request
opened, checks recorded*. The packet's own `tasks.md` boxes stay unticked where
the act completes at merge, and § Packet ledger names the pull request that will
tick each.

---

## The cross-repository ledger

The single place that names every pull request this realization owes, per the
launch instruction that this file is that ledger.

| PR | repo | slice | packet tasks | gate | state |
| --- | --- | --- | --- | --- | --- |
| **[#799](https://github.com/opensoft/openxFactory/pull/799)** | openxFactory | A — feature artifacts, sweep evidence, the eight safe-now example fixtures, the freeze proof, bookkeeping records | 0.2, 2.1–2.3, 3.9, 3.10, 6.1–6.4, 8.2, 8.3 | **safe now** | **OPEN, all checks green** |
| **[#801](https://github.com/opensoft/openxFactory/pull/801)** | openxFactory | B1 — decision-core pin, workflows, operator tools and their runbooks (41/15) | 3.5, 3.6, 3.7, 3.12, 4.5 | **GATED — runbook 1.2** | **DRAFT** |
| **[#802](https://github.com/opensoft/openxFactory/pull/802)** | openxFactory | B2 — origin identity re-issuance + clearing corpus (35/14) | 5.1–5.6, 3.8, 3.11, 3.13 | **GATED — runbook 1.2**, and **HUMAN MERGE WORD ONLY** | **DRAFT** |
| **[#805](https://github.com/opensoft/openxFactory/pull/805)** | openxFactory | B3 — the eight `contract-v3.4` inventoried members, denominator re-sorted (12/9) | 3.1, 3.2, 3.3, 3.4, 4.2, 4.3, 4.4 | **GATED — runbook 1.2** | **DRAFT** |
| **[#806](https://github.com/opensoft/openxFactory/pull/806)** | openxFactory | B4 — remaining live prose and `README.md` per line (28/14; 25 respelled, 3 frozen) | 4.1, 4.6, 4.7, 4.8 | **GATED — runbook 1.2** | **DRAFT** |
| **P6** | openxFactory | B5 — **the mapping FILE and its row** (task 1.1 **AMENDED 2026-09-08**: this change creates the file) | 1.1, 1.2, 1.3, **1.4 re-derived** | **SAFE NOW** — `transferred_on: null` + `transfer_state: pending`, and the file-level `pending_row_rule` forbids resolving a pending row, so nothing live resolves it | **OPEN** |
| **P7** | openxFactory | the bundle cut | 7.1–7.5 | **owed the moment #805 merges**; the minor is allocated at that point, never reserved | **NOT OPENED** |

**No pull request in codexFactory, `opensoft/xFactory`, `installs/hermes-install`
or `opensoft/OpsxFactory`.** Those are packet group **9.2–9.5** and the runbook's
Phases 2, 4, 8 and 9 — explicitly *"NOT performed here"*.

---

## Phase 1: Setup

- [X] T001 Create the feature worktree `openxFactory-worktrees/030-realize-codexfactory-identity` on branch `030-realize-codexfactory-repository-identity` from `origin/main`, per the constitution's worktree-checkout-mode constraint
- [X] T002 Record the realization head every count is taken at — `e8021fed` — in `specs/030-realize-codexfactory-identity/plan.md` and `quickstart.md`
- [X] T003 Author the Speckit artifacts `spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/repository-identity-row.md` and `checklists/requirements.md` under `specs/030-realize-codexfactory-identity/`

---

## Phase 2: Foundational — blocking prerequisites for every slice

**These gate everything. A rename that lands before T004–T009 is unreviewable,
and a rename that lands before T007 may be a lane collision.**

- [X] T004 Confirm the sequencing premise of packet task **0.2**: check whether `adopt-medxsoft-repository-identity` is still active and still authors `contracts/policies/repository-identity.yaml` at its task 1.1 — `git ls-tree origin/main -- openspec/changes/adopt-medxsoft-repository-identity/` and `-- contracts/policies/repository-identity.yaml` — and record the result in `research.md` R-5
- [X] T005 Measure the transfer state that the whole gating rule rests on: `gh api repos/codeXfactory/codexFactory` (expect HTTP 404) and `gh api repos/opensoft/codexFactory --jq '{full_name,private,visibility}'`; record in `research.md` R-1
- [X] T006 Re-run the recorded sweep at the realization head and produce the per-class table (packet **2.1**), using `git grep -ic` and NOT `-Ic`, per `quickstart.md` § 1
- [X] T007 Close the arithmetic against the 2026-09-07 baseline of 281/150 = 123/60 + 78/54 + 80/36 and attribute every drift to a named cause (packet **2.2**); record in `data-model.md` § Path class
- [X] T008 Classify every occurrence that appeared since 2026-09-07 by the published rule and not by fresh judgment (packet **2.3**) — the fifth clearing negative, this packet's own four files, the README Records line, the `ideation/` split
- [X] T009 Re-verify the release-surface arithmetic of `design.md` § 5 at this head: all eight named members present in `contracts/releases/contract-v3.4.digests.yaml` (283 entries) and none of the other 52 renamed files present, per `quickstart.md` § 4
- [X] T010 Derive the regression denominator's new sorted position from the tree, never copied from the packet (packet **3.1**); record the derivation in `research.md` R-4
- [X] T011 Apply the records-and-assertions test PER LINE to all nine `README.md` occurrences and record which way each went (packet **4.8**); record in `research.md` R-8
- [X] T012 Post the plan comment on codexFactory issue **#279** carrying the lane line, the (a)/(b) counts, the intended pull requests with their gating, and every ambiguity found in the packet

---

## Phase 3: User Story 1 — the recorded sweep (Priority: P1) → PR **#799**

**Goal**: the disposition becomes reviewable against the tree rather than against
a hand list, at any commit, by anyone.

**Independent test**: run `quickstart.md` § 1 at the feature head; the totals and
the per-class split reproduce the evidence file exactly.

- [X] T013 [US1] File the sweep as `openspec/changes/adopt-codexfactory-repository-identity/evidence/codexfactory-identity-sweep-2026-09-08.md` carrying the verbatim reproducing command, the pathspec and count per class, and the closed arithmetic (packet **2.1, 2.2**)
- [X] T014 [US1] In the same evidence file, record each occurrence that appeared since the baseline with its class and the rule that placed it (packet **2.3**)
- [X] T015 [US1] In the same evidence file, state the file's own self-referential contribution to the `active-packets` class, so a later re-run reads a known delta rather than an unexplained one
- [X] T016 [US1] In the same evidence file, record the second axis this feature adds — the gating class per RENAME file — and assert that the two gating subtotals sum to the RENAME subtotal in both hits and files

---

## Phase 4: User Story 2 — the declarative renames (Priority: P1) → PR **#799**

**Goal**: respell everything that is correct today, and nothing that is not.

**Independent test**: `scripts/validate-omnigent-contracts.py` and
`scripts/validate-hermes-domain-overlay.py` green; each negative fixture still
produces exactly its own finding; no workflow, pin, register, inventoried member
or operator runbook appears in the diff.

- [X] T017 [P] [US2] Respell `repository:` in the five omnigent negative fixtures `contracts/omnigent/examples/fixtures/negative/manifest-{dual-domain-overlay,legacy-vocabulary,missing-effective-profiles,parallel-identity,semantic-duplicate-worker}.yaml` (packet **3.9**)
- [X] T018 [P] [US2] Respell `repository:` in `contracts/omnigent/examples/omnigent-install-manifest.example.yaml` (packet **3.9**)
- [X] T019 [P] [US2] Respell `repository:` in `contracts/hermes-domain-overlay/examples/hermes-subject-overlay.example.yaml` and `contracts/hermes-domain-overlay/examples/negative/subject-undeclared-kind/hermes/subject/project-alfa/overlay.yaml` (packet **3.10**)
- [X] T020 [US2] Confirm each of the six omnigent fixtures still fails for its own reason and no other: `python3 scripts/validate-omnigent-contracts.py .` (packet **3.9**)
- [X] T021 [US2] Confirm the two hermes-domain-overlay examples still validate and the negative still fails for the undeclared-kind reason: `python3 scripts/validate-hermes-domain-overlay.py .` (packet **3.10**)
- [X] T022 [US2] Record in the evidence file that the remaining RENAME occurrences are GATED, with the runbook step and the pull request that carries each — the deliberate reason this story lands 8 of 124 rather than all of them

---

## Phase 5: User Story 5 — the freeze, verified by diff (Priority: P1) → PR **#799**

**Goal**: prove that the 78 frozen and 125 not-swept occurrences are
byte-unchanged, and that no corpus-wide substitution was run.

**Independent test**: the pathspec-restricted diffs of `quickstart.md` § 5 are
empty and `scripts/validate-signed-execution-chain.py` exits 0.

- [X] T023 [US5] Assert by diff, not by inspection, that `contracts/signed-execution-chain/**` (44/34), `openspec/changes/archive/**` (15/10), `specs/**` outside this feature's own directory (18/9) and `docs/decisions/0002-xfactory-aggregation-repo.md` (1/1) are byte-unchanged (packet **6.1**)
- [X] T024 [US5] Run `python3 scripts/validate-signed-execution-chain.py .` and record `ratification_signature_verifies` and `chain_identity_recomputes` passing for all 34 files — the check that would have caught a well-meaning corpus-wide `sed` (packet **6.2**)
- [X] T025 [US5] Assert by diff that the NOT-SWEPT set is byte-unchanged: other lanes' active change packets (77/32 excluding this packet's own directory) and `ideation/**` (19/13) (packet **6.3**)
- [X] T026 [US5] Assert that no BARE `codexFactory` name was edited anywhere — prose, `--aggregate-members` lists, dashboard groupings, directory names, submodule paths, and the wallet, grant and attestation FILENAMES — per `quickstart.md` § 6 (packet **6.4**)
- [X] T027 [US5] Record the refinement packet task **6.5** needs: after every slice lands, `README.md` retains **three** frozen occurrences (lines 629, 1335, 1347), so the frozen total for the zero-remaining check is **81**, not 78 — stated here rather than left for a later reader to find as unexplained hits

---

## Phase 6: Bookkeeping and validator records (Priority: P1) → PR **#799**

- [X] T028 Run `OPENSPEC_TELEMETRY=0 openspec validate adopt-codexfactory-repository-identity --strict` and record the result (packet **8.2**)
- [X] T029 Run `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` and record the result, expecting exactly one pre-existing failure, `disposition-codexfactory-declared-renames` (packet **8.2**)
- [X] T030 Read `disposition-codexfactory-declared-renames` and record what it actually is, since the name collides with this work: a deltaless packet disposing of OpenSpec CLI 1.12.0 scenario-currency findings over declared SCENARIO retitles — **not** the sweep-record mechanism for group 2, and neither caused nor repaired here (`research.md` R-11)
- [X] T031 Run `python3 scripts/validate-sequenced-after.py . --ledger-diff` and record it green, with this change resolving `adopt-medxsoft-repository-identity` and introducing no cycle (packet **8.3**)
- [X] T032 Confirm packet task **8.1**'s README OpenSpec Records entry is already present from the proposing commit and needs no further edit — and note that its measured-count sentence is one of the three frozen `README.md` lines
- [X] T033 Record packet task **8.4** as OWED, not run: `scripts/sync-notebooklm-books.py --apply` writes to a live external service and is scheduled for after the doc changes land (`research.md` R-14)
- [X] T034 Open **#799** as a normal pull request whose body carries the lane line, the packet task ids, the safe-now declaration, "Not for merge without Brett's word", and the Rule 6 LANDING/LANDED line because it touches `openspec/changes/`

---

## Phase 7: User Story 3 — the live machine surfaces (Priority: P2) → PR **#801**, DRAFT

**Goal**: the transfer window spends minutes merging a reviewed diff instead of
hours writing one.

**Independent test**: the pull request is a draft, names runbook step 1.2, and its
diff touches exactly the B1 files.

- [X] T035 [US3] **ONE COMMIT.** Respell the decision-core pin and everything that asserts it: `contracts/review-lane-pin.yaml` (`repository:` at 47 and the header at 8), `contracts/review-lane-repin-binding.template.yaml`, `.github/workflows/review-lane-repin.yml` (`SOURCE_REPOSITORY` and the checkout), `scripts/review_lane_repin.py` (`SOURCE_REPOSITORY`), `scripts/doc_health/pin_class.py` (the note text), and the three pin tests `tests/review_lane_pin/test_{floor_snapshot,review_lane_caller,repin_lane}.py` (packet **3.5**)
- [X] T036 [US3] Respell all TWELVE occurrences in `.github/workflows/merge-master-approval.yml` together — the pinned decision-core checkout, the App-installation diagnostics whose text tells a human which repository to grant, and the two summary-table rows (packet **3.6**)
- [X] T037 [US3] Respell `.github/workflows/pytest-suite.yml`'s `repository:` and `.github/merge-approval-envelope.yml`'s schema citation (packet **3.7**)
- [X] T038 [US3] Respell `scripts/mint-factory-origin-key.py`'s `TARGET_REPO` and its two record-template lines, and `tests/factory_identity/test_mint_script.py`'s pin of the `gh pr merge … --repo` line the script emits, in the same commit (packet **3.12**)
- [X] T039 [P] [US3] Respell `docs/factory-origin-key-mint-runbook.md` (six, including the `worker-credentials` environment reference and the mint record's table) and `docs/review-lane-repin-runbook.md` (five, four executable `gh api` lines and a permissions-table row) — commands an operator pastes (packet **4.5**)
- [X] T040 [US3] Run `python3 -m pytest tests/review_lane_pin tests/factory_identity/test_mint_script.py -q` green on the respelled tree, proving the one-commit rule held
- [X] T041 [US3] Open **#801** as a DRAFT pull request stating **GATED — lands at runbook step 1.2**, why each file is a live reference (the two required checks that resolve `opensoft/codexFactory` by `actions/checkout` today), and "Not for merge without Brett's word"

---

## Phase 8: User Story 4 — the origin identity, human-only (Priority: P2) → PR **#802**, DRAFT

**Goal**: the transfer stops revoking codexFactory's clearing lane the moment it
completes.

**Independent test**: `scripts/validate-factory-identity.py` and
`scripts/validate-clearing-dispatch.py` green; a diff shows no key material,
no `expires_at` and no `objects` cardinality moved.

- [X] T042 [US4] **ONE COMMIT with T043–T047.** Respell `governance/factory-identity/register.yaml`'s row `holder_ref` and the header sentence about concurrent active rows — **one row respelled, not a second row** — and confirm the reader still sees exactly one active origin row for the repository (packet **5.1**)
- [X] T043 [US4] Respell `holder_id` in `governance/factory-identity/wallets/wal-origin-codexfactory-0001.yaml`, leaving `key_id`, the multibase public half, the fingerprint and `holder_class` untouched (packet **5.2**)
- [X] T044 [US4] Respell `audience.holder_ref`, the single-element `scope.objects` entry and the "THE SCOPE IS ONE REPOSITORY" paragraph in `governance/factory-identity/grants/grant-origin-codexfactory-0001.yaml`, **without widening `objects`** and **without extending `expires_at`** (packet **5.3**)
- [X] T045 [US4] Record that packet task **5.4**'s respell half is a NO-OP: `governance/factory-identity/attestations/custody-attest-wal-origin-codexfactory-0001.yaml` carries no owner segment, only bare names, so editing it would violate packet task 6.4 (`research.md` R-10)
- [X] T046 [US4] Respell `tests/clearing/test_origin_signature.py` (lines 200, 204, 205, 217, 356 — the live-register assertions) and `tests/clearing/test_attestation.py` (68, 75, 78) in the SAME commit as T042 (packet **5.5**)
- [X] T047 [US4] Respell the eight clearing example files — `single-door-attestation.example.yaml`, `deliberation-return.example.yaml` and the **five** negatives under `examples/negative/`, which is one more than packet task 3.8 names (`research.md` R-9) — plus `contracts/clearing/examples/factory-identity-fixture/register.yaml`'s header prose about the live register (packet **3.8, 3.11**)
- [X] T048 [US4] Respell the eight occurrences in `tests/factory_identity/test_validator.py` — the validator's default holder and the per-case holders, which move with the validator's live subject (packet **3.13**)
- [X] T049 [US4] Run `python3 scripts/validate-factory-identity.py .` and `python3 scripts/validate-clearing-dispatch.py .` green on the re-issued tree and record that the disjointness rule over key material is unaffected — no `key_id`, `did` or fingerprint moved, no `FILL-IN-AT-MINT` sentinel reappeared (packet **5.6**)
- [X] T050 [US4] Run `python3 -m pytest tests/clearing tests/factory_identity -q` green
- [X] T051 [US4] Record packet task **5.7** as an OPERATOR HANDOFF, not performed: verify codexFactory's `worker-credentials` environment and its `FACTORY_ORIGIN_SIGNING_KEY` secret survived the transfer, and re-attest custody if not (runbook 10.4)
- [X] T052 [US4] Open **#802** as a DRAFT pull request stating **GATED — lands at runbook step 1.2** and, **in bold**, that `governance/factory-identity/` is permanently human-only, is entered BY NAME in codexFactory's never-clearable floor, needs Brett Heap's HUMAN merge word, and may be landed by no council verdict and no autonomous or council-cleared path

---

## Phase 9: The eight inventoried members (Priority: P2) → PR **#805**, DRAFT

**Goal**: move all eight together so the `release-inventory-drift` transient is
bounded and repairable by one cut.

**Independent test**: `python3 -m pytest tests/hermes_runtime_contracts -q` and
`scripts/validate-hermes-runtime-contracts.py` green; doc-health reports exactly
eight `release-inventory-drift` findings, naming these members and no others.

- [X] T053 **ONE COMMIT with T054.** Respell the codex entry's `repository:` in `contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml` and move it to position **1** as derived in `research.md` R-4, leaving `commit`, `stack_path`, `stack_digest`, `domain_id`, `expected_contract_ref`, `expected_contract_schema_version` and `expected_result` byte-identical (packet **3.1**)
- [X] T054 Respell and REORDER `PINNED_TABLE` in `tests/hermes_runtime_contracts/test_domain_regression.py` to match, keep its "bytewise sorted by repository" comment true, and confirm the `sorted(..., key=lambda value: value.encode("utf-8"))` assertion and the value-for-value `zip` both pass (packet **3.1**)
- [X] T055 Respell `tests/hermes_runtime_contracts/test_domain_regression.py`'s resolver pin at line 410, including the bare-mirror fixture's own path segments, so the engineering domain's `--domain-repo` resolver key becomes `codeXfactory/codexFactory` (packet **3.2**)
- [X] T056 [P] Respell the codex `repository:` in `contracts/hermes-runtime/fixtures/regression/{digest-mismatch,duplicate-repository,missing-exclusion-reason}.yaml` and verify each still produces EXACTLY its own finding, with `duplicate-repository.yaml`'s deliberate duplicate remaining `opensoft/AdxFactory` (packet **3.3**)
- [X] T057 [P] Respell `contracts/hermes-runtime/README.md`'s denominator enumeration and put the name in its new sorted position so README order and fixture order agree (packet **3.4**)
- [X] T058 [P] Respell `docs/contract-versioning-policy.md`'s denominator enumeration, keeping the order consistent with the re-sorted fixture (packet **4.2**)
- [X] T059 [P] Respell `docs/terminology-and-repo-topology.md` and add a one-line note pointing at `contracts/policies/repository-identity.yaml` as the resolver for former identities, so the freeze rule is discoverable from the topology document (packet **4.3**)
- [X] T060 [P] Respell the three occurrences in `docs/xfactory-domain-factory-model.md`, including the `https://github.com/opensoft/codexFactory` URL (packet **4.4**)
- [X] T061 Run `python3 -m pytest tests/hermes_runtime_contracts -q` and `python3 scripts/validate-hermes-runtime-contracts.py .` green (packet **7.1**)
- [X] T062 Record the predicted transient: doc-health will report EIGHT `ERROR`-severity `release-inventory-drift` findings from the moment this slice lands until the cut, one per inventoried member, none in the `EDITORIAL` set (packet **7.5**)
- [X] T063 Open **#805** as a DRAFT pull request stating **GATED — lands at runbook step 1.2**, naming the eight inventoried members, and stating that the cut (**P7**) is owed immediately on its merge

---

## Phase 10: The remaining live prose (Priority: P3) → PR **#806**, DRAFT

- [X] T064 [P] Respell `docs/architecture.md`'s DomainxFactory enumeration (packet **4.1**)
- [X] T065 [P] Respell `docs/roles-and-authority.md` (3), `docs/traceability-model.md` (3), `docs/omnigent-constitution.md` (2) and `docs/dogfood-content-migration-plan.md` (2) (packet **4.6**)
- [X] T066 [P] Respell the eight single-occurrence documents `docs/{deployment-worker-model,feature-decomposition,merge-council,merge-master,pr-admission,spec-kit-stage-ownership,workflow-contract,governed-reissuance-runbook}.md` (packet **4.7**)
- [X] T067 Respell the SIX `README.md` lines the per-line test sent to RENAME (316, 409, 678, 679, 790, 792) and leave the THREE it sent to the freeze (629, 1335, 1347) byte-unchanged, recording the verdict per line in the pull request body (packet **4.8**, `research.md` R-8)
- [X] T068 Open **#806** as a DRAFT pull request stating **GATED — lands at runbook step 1.2** and carrying the per-line `README.md` verdict table

---

## Phase 11: Blocked and owed — recorded, not performed

- [X] T069 **DONE — task 1.1 AMENDED 2026-09-08, then realized.** Brett Heap (convener), interactive walkthrough, verbatim **"Amend task 1.1: this change creates the file (Recommended)"**. Authored `contracts/policies/repository-identity.yaml` (schema for both repositories' rows + the codexFactory row, `transferred_on: null` with `transfer_state: pending` and a file-level `pending_row_rule` forbidding live resolution of a pending row), realized tasks **1.2** and **1.3** on the row, and **RE-DERIVED task 1.4** — the `contracts/manifest.yaml` entry, its `consumption_rule` and the computed per-file `sha256` are owed here, not by the exemplar. Record: `openspec/changes/adopt-codexfactory-repository-identity/review/amendment-2026-09-08-task-1-1.md`; evidence addendum § 15. Carried by the pull request from branch `030-mapping-row-amendment`.
- [ ] T070 **OWED after #805 merges.** Cut the contract bundle (packet **7.1–7.5**): run the full affected suite and validators green on the renamed tree; follow `docs/contract-versioning-policy.md` § Bundle Realization Order to allocate the next additive minor after `contract-v3.4` at that point and not before; in one atomic candidate commit move `contracts/manifest.yaml`'s `contract_bundle_version`, one `contracts/CHANGELOG.md` entry naming the transfer, the eight moved members, the mapping row, the origin re-issuance and the `--domain-repo` key migration, plus the realized `contracts/releases/<tag>.digests.yaml` built by `scripts/validate-contract-release.py build --tag <tag>`; then `verify-commit` clean, `verify-promotion` before tagging, the annotated tag at the exact published commit, and `verify-tag` from a fresh checkout. Re-run doc-health and record `release-inventory-drift` at **0**.
- [ ] T071 **OWED after the doc changes land.** Run `python3 openxFactory/scripts/sync-notebooklm-books.py . --apply` per the projection workflow (packet **8.4**). Not run here: it writes to a live external service and this feature's doc changes are unmerged.
- [ ] T072 **OPERATOR, not this lane.** Runbook **10.3** — the human merge word for **#802**; **10.4** — verify `worker-credentials` / `FACTORY_ORIGIN_SIGNING_KEY` survived the transfer; **10.5** — prove the clearing lane end to end with a sealed request from `codeXfactory/codexFactory` accepted by `scripts/validate-clearing-dispatch.py`.
- [ ] T073 **GATE REFINEMENT, recorded 2026-09-08 after the gate fired.** Slice B1 (#801) reds `pytest-suite` before the transfer with `failures=0 errors=0` and `skipped=23` against a pinned `EXPECT_SKIPPED: 21` — the cross-repository checkout of `codeXfactory/codexFactory` is `continue-on-error`, so the freshness verifier and the vector replay SKIP instead of passing. The slice therefore needs runbook step **1.6** (reinstall the Apps on `codeXfactory` and re-grant repository access — App installations are per organization and do NOT travel with a transfer) in addition to **1.2**. Read "lands at runbook step 1.2" on every gated pull request as **"lands when Phase 1 is complete, 1.6 included"**. At merge time the number that proves it is `skipped=21` with both named verifiers `passed`. Recorded in `evidence/codexfactory-identity-sweep-2026-09-08.md` § 14 and on #801; the runbook itself is the operator's document and is not edited by this lane.
- [ ] T074 **NEW OCCURRENCE, classified and DEFERRED — not this lane's to edit.** Discharging task **2.3** at `131adf11` found `governance/review-authority/grants/grant-grc-0001.yaml` (2 hits), absent at `e8021fed`, added by `4719f07f` — the `register-gate-rules-council-seats` mint-and-register ceremony. `governance/**` → **RENAME** by the published rule; both occurrences are COUNTERFACTUAL, in a header comment explaining why `objects:` is `opensoft/openxFactory` and deliberately NOT `opensoft/codexFactory`, and the sentence is present-tense so it respells at the transfer to stay true. **Not edited here**: it is another lane's live ceremony artifact mid-construction with unfilled `@@…@@` operator placeholders, it is a review-authority (key-custody) grant, and the four rename slices are already under review. Deferred to that lane's next touch or to a fifth slice after the ceremony completes. Recorded in evidence § 15.2 and on codexFactory issue #279. The RENAME subtotal rises 124 → 126.

---

## Packet ledger — which `tasks.md` box each pull request will tick

**This feature ticks NOTHING in the packet.** A tick claims an act is done, and
for a rename the act completes at merge. Recorded here so the next lane ticks
from the ledger rather than from the tree.

| packet task | ticked by | why not yet |
| --- | --- | --- |
| 0.2 | **#799** | the premise was confirmed and recorded in `research.md` R-5; the box ticks when that record is on `main` |
| 1.1, 1.2, 1.3, 1.4 | **P6** | 1.1 AMENDED 2026-09-08 and realized; ticks on P6's merge. 1.4 re-derived: the manifest registration is owed here |
| 2.1, 2.2, 2.3 | **#799** | the evidence file is a diff in #799 |
| 3.1, 3.2, 3.3, 3.4 | **#805** | gated at runbook 1.2 |
| 3.5, 3.6, 3.7, 3.12 | **#801** | gated at runbook 1.2 |
| 3.8, 3.11, 3.13 | **#802** | gated at runbook 1.2 + human merge word |
| 3.9, 3.10 | **#799** | safe now; ticks on #799's merge |
| 4.1, 4.6, 4.7, 4.8 | **#806** | gated at runbook 1.2 |
| 4.2, 4.3, 4.4 | **#805** | gated at runbook 1.2 |
| 4.5 | **#801** | gated at runbook 1.2 |
| 5.1–5.6 | **#802** | gated at runbook 1.2 + **human merge word** |
| 5.7 | operator | runbook 10.4 |
| 6.1, 6.2, 6.3, 6.4 | **#799** | the diff evidence is in #799; 6.1/6.3 are re-asserted on every later slice |
| 6.5 | **#806** (the last rename slice) | only true once every rename has landed; refined to **81** frozen, not 78 (T027) |
| 7.1–7.5 | **P7** | the minor is allocated after the final integration point |
| 8.1 | already done in the proposing commit | — |
| 8.2, 8.3 | **#799** | the recorded runs are in #799, and were re-run at the merged head after #783 landed: `100 passed, 1 failed`, ledger 184 rows |
| 8.4 | **P7** or later | writes to a live external service |
| 9.1–9.6 | **NOT performed** | group 9 |

---

## Dependencies and slice order

```text
Phase 1 (setup) ──> Phase 2 (foundational: sweep, arithmetic, derivations)
                        │
                        ├──> Phase 3 US1  ┐
                        ├──> Phase 4 US2  ├─> PR #799 ── safe now, all checks green
                        ├──> Phase 5 US5  │
                        └──> Phase 6      ┘
                        │
                        ├──> Phase 7 US3 ──> PR #801 ┐
                        ├──> Phase 8 US4 ──> PR #802 ├─ all GATED at runbook step 1.2
                        ├──> Phase 9     ──> PR #805 │  (the transfer, Phase 1 of the ceremony)
                        └──> Phase 10    ──> PR #806 ┘
                                                     │
                        Phase 11: P6 (blocked) ; P7 owed after #805 merges
```

- **#799 depends on nothing.** It is the MVP: the estate gains a reproducible,
  reviewable disposition record plus the eight renames that are true today.
- **#801, #802, #805, #806 are mutually independent** — disjoint file sets, verified by
  the slice tables in [plan.md](./plan.md) — and share exactly one gate, the
  transfer. They may merge in any order once it lifts.
- **#805 → P7** is the only hard intra-feature ordering: the cut needs the eight
  members on `main`.
- **P6** has two gates and only one of them is the transfer.

## Parallel execution

Within #799: T017, T018, T019 touch disjoint files and run in parallel; T023–T026
are independent read-only assertions.

Within #805: T056, T057, T058, T059, T060 touch disjoint files. T053+T054 are ONE
commit and never parallel.

Within #806: T064, T065, T066 touch disjoint files.

Across slices: #801, #802, #805, #806 can be authored in parallel; they were.

## Implementation strategy

**MVP is #799 alone** — the sweep evidence, the eight safe-now renames, the freeze
proof and the recorded validator runs. It delivers the packet's central claim
(*a disposition by rule plus a recorded machine sweep*) with no dependency on the
operator ceremony, and it is the only slice that can be merged today.

**Everything else is authored now and held**, so the transfer window is spent
reviewing and merging rather than writing. That is the whole ordering argument:
the ceremony's Phase 3 already runs three gates inside the window, and adding
diff authorship to that window is the cost this split avoids.
