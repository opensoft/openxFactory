# Tasks: adopt-codexfactory-repository-identity

**NOTHING IN THIS FILE IS PERFORMED BY THE PROPOSAL.** Every rename, re-issuance
and cut below is implementation work for a later apply step, after ratification.
The proposal declares the identity and the disposition; the tasks execute them.

**AND NOTHING IN THIS FILE PERFORMS THE TRANSFER.** The GitHub transfer, the two
visibility flips, the aggregation lockstep, the App installations, the container
namespaces and the SonarCloud rebind are an OPERATOR ceremony ordered in
`~/session-prompts/runbook-codexfactory-org-transfer.md`. Group 9 names the
handoff points; it does not own them.

## 0. Ratification gate

- [x] 0.1 (2026-09-07) Convener read of `design.md` § 0 and § 8. **OQ-1, OQ-2,
      OQ-3 and OQ-5 are RULED** (add `codeXfactory` to the Opensoft GitHub
      Enterprise, VERIFIED `plan=enterprise` 2026-09-07T16:41:04Z; Apache-2.0
      for openxFactory and openXwallet, by a separate lane, landed openxFactory
      #762 / openXwallet #22; **via the ideation-split decision sheet — redact
      the two sensitive files, editorially split `treatment-options-engine`
      between openxFactory and MedxFactory, delete the stale
      `campaign-marketing` stub, and run three receiving pull requests plus one
      openxFactory removal pull request — accept publication, GATED on those
      four moves landing first**; **EXERCISE the `MIGRATION_PIN` re-point
      ceremony rather than riding GitHub's redirect**). **OQ-4 and OQ-6 remain
      OPEN and still owe a word** before any box below is ticked. Ratified
      2026-09-07T22:21:44Z, Brett Heap (convener), verbatim "accept all [A] and
      ratify 763"; record `review/ratification-2026-09-07.md`.
- [ ] 0.2 Confirm the sequencing premise still holds:
      `adopt-medxsoft-repository-identity` is still active and still authors
      `contracts/policies/repository-identity.yaml` at its task 1.1. If that
      change is archived or withdrawn before this one realizes, task 1.1 below
      changes from "add a row" to "author the file", and `sequenced_after` is
      re-derived rather than kept out of habit.
- [x] 0.3 (2026-09-07) **Ratified.** Brett Heap, convener, verbatim **"accept
      all [A] and ratify 763"**, posted 2026-09-07T22:21:44Z on
      https://github.com/opensoft/openxFactory/pull/763#issuecomment-5576174434,
      given against head `5bfdcf3c06478167bd7509f1576db3528ce4ede1`. The
      record is `review/ratification-2026-09-07.md`, a diff in this pull
      request, which is what lets this box be ticked under house practice.
      **No box in Groups 1-8 is ticked by this act** beyond 0.1's text and this
      box — OQ-4 and OQ-6 remain open and gate the rest.

## 1. The transfer mapping row

- [ ] 1.1 Add the codexFactory row to
      `contracts/policies/repository-identity.yaml` — the file
      `adopt-medxsoft-repository-identity` authors at ITS task 1.1. **Do not
      create the file here.** The row: `former: opensoft/codexFactory`,
      `current: codeXfactory/codexFactory`, `transferred_on: <the transfer
      date>`, and a `redirect` note stating that the provider redirect lapses if
      `opensoft` reuses the name — which it may, `opensoft` remaining an active
      organization that holds the aggregation repository.
      > **AMENDED 2026-09-08.** The task body above is retained as ratified
      > 2026-09-07. Brett Heap (convener), interactive walkthrough, verbatim
      > **"Amend task 1.1: this change creates the file (Recommended)"**:
      > **THIS CHANGE CREATES** `contracts/policies/repository-identity.yaml`,
      > with the schema both repositories' rows need and its own row.
      > `adopt-medxsoft-repository-identity` APPENDS its two 2026-08-26 rows to
      > `transfers:` when it realizes. The amendment was taken because the
      > exemplar is still active, `Status: draft` and UNREALIZED, so the file did
      > not exist and the premise of "Do not create the file here" had not held
      > in time; task 0.2's conditional covers only *archived or withdrawn* and
      > therefore did not fire. **The ROW CONTENT is unchanged** except
      > `transferred_on`, which is `null` with `transfer_state: pending` until
      > the transfer is CONFIRMED at runbook step 1.2 — a date recording a
      > completed act cannot be written before the act. The file-level
      > `pending_row_rule` forbids resolving `former` -> `current` for any live
      > reference while a row is `pending`, which is what makes this row safe to
      > land ahead of the transfer while groups 3-5 are held. Record:
      > `review/amendment-2026-09-08-task-1-1.md`.
- [ ] 1.2 Record on the row the TWO divergences a reader will otherwise trip on
      (OQ-6): that the owner segment is compared CASE-SENSITIVELY by this estate
      even though the provider compares it case-insensitively, and that the
      container namespace derived from this owner is LOWERCASED by GHCR to
      `codexfactory`, so `ghcr.io/codexfactory/codexfactory/...` is the same
      identity under a different spelling.
- [ ] 1.3 Record on the row the reference shapes the provider redirect does NOT
      cover: reusable-workflow `uses:` paths, container package namespaces, and
      federated-credential subject strings. This is the mapping's contribution to
      the fourth ADDED requirement and it is what makes the freeze safe: a frozen
      former identity resolves BY LOOKUP, never by a redirect that may lapse.
- [ ] 1.4 Confirm no second registration is owed: the file's
      `contracts/manifest.yaml` entry and its `consumption_rule` are created by
      the exemplar's task 1.3. Adding a row does not add an entry. Re-verify the
      per-file `sha256` moves with the row and is recomputed, not hand-edited.
      > **RE-DERIVED 2026-09-08 by the 1.1 amendment.** The task body above is
      > retained as ratified. Its premise was that the exemplar creates the file
      > and therefore its `contracts/manifest.yaml` entry. **This change now
      > creates the file, so the registration IS owed here**: the entry, its
      > `consumption_rule` and the per-file `sha256` are authored by this change.
      > The `sha256` is COMPUTED, never hand-edited — the one clause of the
      > original wording that survives verbatim and is the reason this box is
      > re-derived rather than simply reversed. The exemplar's task 1.3 then
      > RECOMPUTES that digest when its rows change the file's bytes, and
      > re-authors nothing. Record:
      > `review/amendment-2026-09-08-task-1-1.md`.

## 2. The recorded classification sweep — the evidence

- [ ] 2.1 Re-run the sweep at the realization head and file its output as
      `evidence/codexfactory-identity-sweep-<date>.md`. The command, recorded so
      the count is reproducible without this packet:

      ```sh
      git grep -ic "opensoft/codexfactory" -- .
      ```

      with the per-class totals produced by restricting the same pattern to each
      pathspec in the `design.md` § 2 table.
- [ ] 2.2 Confirm the arithmetic closes at the realization head, exactly as it
      closed at `origin/main` `64aad02e` on 2026-09-07: **281 occurrences across
      150 files = 123/60 rename + 78/54 frozen + 80/36 not swept.** A drift in
      the total is expected (the corpus moves daily); a drift that does not
      classify under the published rule is a finding and is recorded before any
      rename lands.
- [ ] 2.3 Classify every occurrence that appeared since 2026-09-07 by the
      published rule — coverage test first, then the records-and-assertions test
      — and NOT by a fresh judgment. Record each new occurrence and its class in
      the evidence file.

## 3. Rename the live machine surfaces

Group the commits so that every fixture lands with the artifact that pins it.
A split commit here is red by construction, which is the mechanism working.

- [ ] 3.1 **ONE COMMIT.**
      `contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml`:
      respell the codex entry's `repository:` to `codeXfactory/codexFactory`
      **and move that entry to its new sorted position** — the list is bytewise
      sorted by repository and `c` (0x63) sorts before `o` (0x6F), so the entry
      moves from LAST to FIRST if this change lands alone, and to SECOND if
      `adopt-medxsoft-repository-identity` has landed (`M` = 0x4D). **Derive the
      position from the tree at the realization head; do not copy either
      number.** Leave `commit`, `stack_path`, `stack_digest`, `domain_id`,
      `expected_contract_ref`, `expected_contract_schema_version` and
      `expected_result` byte-identical: the repository content did not move.
      In the same commit, respell and REORDER `PINNED_TABLE` in
      `tests/hermes_runtime_contracts/test_domain_regression.py` to match, keep
      its "bytewise sorted by repository" comment true, and confirm the
      `sorted(..., key=lambda value: value.encode("utf-8"))` assertion at
      line 259 and the value-for-value `zip` comparison both pass.
- [ ] 3.2 In the same commit as 3.1, update
      `tests/hermes_runtime_contracts/test_domain_regression.py:410`, which pins
      the `--domain-repo <canonical-repo>=<checkout>` resolver against the
      former key. The engineering domain's resolver key becomes
      `codeXfactory/codexFactory` from the next bundle forward.
- [ ] 3.3 Respell the codex `repository:` in the three negative fixtures
      `contracts/hermes-runtime/fixtures/regression/{digest-mismatch,duplicate-repository,missing-exclusion-reason}.yaml`.
      Verify each still produces EXACTLY the finding it exists to produce — the
      deliberate duplicate in `duplicate-repository.yaml` is
      `opensoft/AdxFactory` and must stay the reported one.
- [ ] 3.4 `contracts/hermes-runtime/README.md` (~line 126): respell the
      denominator enumeration and put the name in its new sorted position, so
      README order and fixture order agree.
- [ ] 3.5 **ONE COMMIT.** The review-lane decision-core pin and everything that
      asserts it: `contracts/review-lane-pin.yaml:47` (`repository:`) and its
      header line 8; `contracts/review-lane-repin-binding.template.yaml` (lines
      46, 110); `.github/workflows/review-lane-repin.yml` (`SOURCE_REPOSITORY`
      at 137, the checkout at 385); `scripts/review_lane_repin.py:62`
      (`SOURCE_REPOSITORY`); `scripts/doc_health/pin_class.py:793` (the note
      text); and the three pin tests
      `tests/review_lane_pin/test_floor_snapshot.py:74`,
      `tests/review_lane_pin/test_review_lane_caller.py:135` (both
      `PINNED_REPOSITORY`) and `tests/review_lane_pin/test_repin_lane.py`
      (lines 851, 1165).
- [ ] 3.6 `.github/workflows/merge-master-approval.yml` — TWELVE occurrences at
      108, 473, 513, 522, 533, 599, 604, 617, 623, 630, 1216, 1640: the pinned
      decision-core checkout, the App-installation diagnostics whose message text
      tells an operator which repository to grant, and two summary-table rows.
      **The diagnostic text is not decoration** — it is the instruction a human
      follows when the lane refuses, so a half-respelled message sends them to
      the wrong organization.
- [ ] 3.7 `.github/workflows/pytest-suite.yml:396` (`repository:`) and
      `.github/merge-approval-envelope.yml:3` (the schema citation).
- [ ] 3.8 The clearing corpus — SIX files, all unsigned and therefore renameable:
      `contracts/clearing/examples/single-door-attestation.example.yaml` (13, 90,
      the widening finding's `subject:`),
      `deliberation-return.example.yaml:30` (`verified_subject_pin`), and the
      four negatives under `examples/negative/`. Confirm each negative still
      fails for its own reason and no other.
- [ ] 3.9 The omnigent fixtures — SIX files under
      `contracts/omnigent/examples/`: the five negatives
      (`manifest-dual-domain-overlay`, `manifest-legacy-vocabulary`,
      `manifest-missing-effective-profiles`, `manifest-parallel-identity`,
      `manifest-semantic-duplicate-worker`) and
      `omnigent-install-manifest.example.yaml`. Confirm each negative still
      fails for its own reason and no other.
- [ ] 3.10 The hermes-domain-overlay examples — TWO files:
      `examples/hermes-subject-overlay.example.yaml` and
      `examples/negative/subject-undeclared-kind/hermes/subject/project-alfa/overlay.yaml`.
- [ ] 3.11 `contracts/clearing/examples/factory-identity-fixture/register.yaml`
      (lines 8, 17) — the FIXTURE register's header prose, which explains that
      the whole-tree sweep resolves REAL artifacts against the LIVE register.
      This is prose about the live register and it renames with it; the fixture's
      own rows are a separate fixture identity and are checked, not assumed, at
      this task.
- [ ] 3.12 `scripts/mint-factory-origin-key.py` — `TARGET_REPO` (121) and the
      two record-template lines (847, 853); and
      `tests/factory_identity/test_mint_script.py:679`, which pins the runbook's
      `gh pr merge … --repo` line the script emits.
- [ ] 3.13 `tests/factory_identity/test_validator.py` — EIGHT occurrences (107,
      366, 379, 418, 432, 479, 521, 610), the validator's default holder and the
      per-case holders. These are fixture identities inside the test and move
      with the validator's live subject.

## 4. Rename the live documents

- [ ] 4.1 `docs/architecture.md:25` — the DomainxFactory enumeration.
- [ ] 4.2 `docs/contract-versioning-policy.md:449` — the supported-domain
      regression denominator enumeration. Keep the order consistent with the
      re-sorted fixture from 3.1.
- [ ] 4.3 `docs/terminology-and-repo-topology.md:208`, and add a one-line note
      pointing at `contracts/policies/repository-identity.yaml` as the resolver
      for former identities, so the freeze rule is discoverable from the topology
      document rather than only from this packet.
- [ ] 4.4 `docs/xfactory-domain-factory-model.md` — THREE occurrences (297, 888,
      890), including the `https://github.com/opensoft/codexFactory` URL.
- [ ] 4.5 The four factory-origin and re-pin runbooks:
      `docs/factory-origin-key-mint-runbook.md` (SIX: 69, 117, 274, 303, 309,
      325 — including the `worker-credentials` environment reference and the
      mint record's table) and `docs/review-lane-repin-runbook.md` (FIVE: 109,
      110, 111, 114, 150 — four executable `gh api` lines and a permissions
      table row). **These are commands an operator pastes**; a stale line here
      fails at the terminal rather than in CI.
- [ ] 4.6 `docs/roles-and-authority.md` (237, 238, 239),
      `docs/traceability-model.md` (20, 218, 219),
      `docs/omnigent-constitution.md` (40, 41),
      `docs/dogfood-content-migration-plan.md` (5, 49).
- [ ] 4.7 The single-occurrence documents: `docs/deployment-worker-model.md:9`,
      `docs/feature-decomposition.md:9`, `docs/merge-council.md:9`,
      `docs/merge-master.md:9`, `docs/pr-admission.md:9`,
      `docs/spec-kit-stage-ownership.md:11`, `docs/workflow-contract.md:105`,
      `docs/governed-reissuance-runbook.md:61`.
- [ ] 4.8 `README.md` — EIGHT occurrences (316, 409, 530, 531, 642, 644, 1172,
      1184). Apply the records-and-assertions test PER LINE and record the
      outcome: 316 and 409 assert where engineering content lives (rename);
      530/531/642/644 are issue and pull-request citations in the OpenSpec
      Records block, which is a kept-current index (rename, and the numbers do
      not change — GitHub carries issue and pull-request numbers through a
      transfer); 1172 and 1184 narrate a completed dated act (**candidates for
      the freeze** — decide against the test, do not sweep, and record which
      way each went).

## 5. Re-issue the factory-origin identity — HUMAN-ONLY SURFACE

**Read `design.md` § 4.3 before starting.** `governance/factory-identity/` is
declared permanently human-only: no council verdict and no autonomous or
council-cleared approval path may land a change here, and the directory is
entered BY NAME in codexFactory's never-clearable floor. **The pull request
carrying this group needs a human merge word.**

- [ ] 5.1 `governance/factory-identity/register.yaml` — respell the row's
      `holder_ref` (146) and the header sentence about concurrent active rows
      (113). **One row, respelled — not a second row.** Confirm the reader still
      sees exactly one active origin row for the repository.
- [ ] 5.2 `governance/factory-identity/wallets/wal-origin-codexfactory-0001.yaml:50`
      — respell `holder_id`. **Do not touch** `key_id`, the multibase public
      half, the fingerprint, or `holder_class`.
- [ ] 5.3 `governance/factory-identity/grants/grant-origin-codexfactory-0001.yaml`
      — respell `audience.holder_ref`, the single-element `scope.objects` entry,
      and the header's "THE SCOPE IS ONE REPOSITORY" paragraph. **Do not widen
      `objects` to carry both identities**, which the grant's own header forbids
      and which would let one key speak for a repository it was not issued for.
      **Do not extend `expires_at`**, which is `issued_at` + 90 days and is a
      separate governed question.
- [ ] 5.4 The custody attestation beside them names the repository; respell it in
      the same commit and confirm `scripts/validate-factory-identity.py` reports
      no `factory-identity-tier-unattested` regression and no
      `FILL-IN-AT-MINT` sentinel reappears.
- [ ] 5.5 `tests/clearing/test_origin_signature.py` — lines 200, 204, 205, 217
      and 356 assert against the LIVE register by design. Respell in the SAME
      commit as 5.1, and `tests/clearing/test_attestation.py` (68, 75, 78) with
      it.
- [ ] 5.6 Run `scripts/validate-factory-identity.py` and
      `scripts/validate-clearing-dispatch.py` green on the re-issued tree, and
      record that the disjointness rule over key material is unaffected — no
      `key_id`, `did` or fingerprint moved.
- [ ] 5.7 **OPERATOR HANDOFF, not performed here:** verify that codexFactory's
      `worker-credentials` environment and its `FACTORY_ORIGIN_SIGNING_KEY`
      secret survived the repository transfer, and re-attest custody if they did
      not. Runbook step, recorded here so the dependency is visible from the
      packet.

## 6. Verify the freeze

- [ ] 6.1 Assert **with a diff, not by inspection**, that the 78 occurrences
      across 54 files in the frozen classes are byte-unchanged after Groups 3-5:
      `contracts/signed-execution-chain/**` (44/34),
      `openspec/changes/archive/**` (15/10), `specs/**` (18/9), and
      `docs/decisions/0002-xfactory-aggregation-repo.md` (1/1).
- [ ] 6.2 Run `scripts/validate-signed-execution-chain.py` green and record that
      `ratification_signature_verifies` and `chain_identity_recomputes` pass for
      all 34 files. **This is the check that would have caught a well-meaning
      corpus-wide sed**, and recording it green is the evidence that none was
      run.
- [ ] 6.3 Assert that the 80 occurrences across 36 files in the NOT-SWEPT classes
      — other lanes' active change packets (74/32) and `ideation/**` (6/4) — are
      byte-unchanged. A diff touching another lane's unmerged packet is a
      lane-collision and is reverted, not merged.
- [ ] 6.4 Confirm no BARE `codexFactory` name was edited anywhere. A transfer
      moves the OWNER segment only; bare member names, `--aggregate-members`
      lists, dashboard groupings, directory names and submodule paths are correct
      before and after.
- [ ] 6.5 Confirm zero remaining live occurrences of `opensoft/codexFactory`
      outside the frozen and not-swept sets.

## 7. Cut the contract bundle

- [ ] 7.1 Run the full suite and the affected validators green on the renamed
      tree BEFORE touching any release surface:
      `python3 -m pytest tests/hermes_runtime_contracts tests/clearing tests/factory_identity tests/review_lane_pin`,
      `scripts/validate-hermes-runtime-contracts.py`,
      `scripts/validate-factory-identity.py`,
      `scripts/validate-clearing-dispatch.py`,
      `scripts/validate-signed-execution-chain.py`,
      `scripts/validate-omnigent-contracts.py`,
      `scripts/validate-hermes-domain-overlay.py`.
- [ ] 7.2 Follow `docs/contract-versioning-policy.md` § Bundle Realization Order:
      rebase onto the final integration point, recheck availability, and allocate
      the next available additive minor after `contract-v3.4` THEN — no number is
      reserved by this packet, and this packet has a live ordering dependency
      besides.
- [ ] 7.3 In one atomic candidate commit: `contracts/manifest.yaml`
      (`contract_bundle_version`), `contracts/CHANGELOG.md` (one entry naming the
      transfer, the EIGHT moved members, the mapping row, the origin re-issuance,
      and the `--domain-repo` key migration note), and the realized
      `contracts/releases/<bundle-tag>.digests.yaml` built by
      `scripts/validate-contract-release.py build --tag <tag>`. **Never hand-edit
      an existing inventory to make a comparison pass.**
- [ ] 7.4 `scripts/validate-contract-release.py verify-commit --commit <sha>`
      clean at the candidate; `verify-promotion` before tagging; publish the
      annotated tag at the exact published commit and `verify-tag` from a fresh
      checkout.
- [ ] 7.5 Re-run doc-health and record `release-inventory-drift` at **0 findings**
      after the cut. Record the transient too: between Group 3 and 7.3 the family
      reports EIGHT `ERROR` findings (the eight non-editorial members), which is the
      family working and is the reason the cut is sequenced inside this change.

## 8. Corpus bookkeeping

- [ ] 8.1 Add the one-line active-change entry to the README "OpenSpec Records"
      block (done in the proposing commit) and keep the README doc index current.
- [ ] 8.2 `OPENSPEC_TELEMETRY=0 openspec validate adopt-codexfactory-repository-identity --strict`
      and `--all --strict` green. **The expected `--all` result is 98 passed /
      1 failed**, the one failure being the pre-existing deltaless disposition
      packet `disposition-codexfactory-declared-renames`, which this change
      neither causes nor repairs.
- [ ] 8.3 `python3 scripts/validate-sequenced-after.py` green, with this change
      resolving `adopt-medxsoft-repository-identity` and introducing no cycle.
- [ ] 8.4 Run `python3 openxFactory/scripts/sync-notebooklm-books.py . --apply`
      after the doc changes land, per the projection workflow.

## 9. Named follow-ons — NOT performed here

- [ ] 9.1 **The operator ceremony**, in full, is
      `~/session-prompts/runbook-codexfactory-org-transfer.md`: the Enterprise
      membership check, the transfer, the two visibility flips, the aggregation's
      lockstep commit, the App installations, the environment and secret
      inventory, the GHCR dual-publish window and prefix flip, the SonarCloud
      rebind, and the per-repository reference sweeps with their test-count
      proofs. **The openxFactory visibility flip additionally gates on OQ-3's
      ruling** (`review/ratification-2026-09-07.md`): the ideation-split
      decision sheet's four moves — redact the two sensitive files, editorially
      split `treatment-options-engine`, delete the `campaign-marketing` stub,
      and land the three receiving pull requests plus one openxFactory removal
      pull request (with the cross-reference bootstrap re-run and the
      README/INDEX pointers updated) — must land BEFORE this flip, not after
      it.
- [ ] 9.2 **`installs/hermes-install` — 181 occurrences across 84 files**,
      including `config/clients/opensoft/overlay.yaml` (5) and
      `tests/unit/test_subject_pin_guard.py` (36). A separate act in that
      repository. **This packet DECLINES the exemplar's "at its next pin bump"
      disposition for this repository** and asks that it be scheduled as a step
      of the ceremony with its own test-count proof, because at 181 occurrences
      including a live client overlay, an unbounded deferral leaves a live
      install naming a dead identity.
- [ ] 9.3 **`opensoft/xFactory` (aggregation) — 25 across 14.** No
      aggregation-level OpenSpec act is owed; the lockstep commit is a runbook
      step and a hard ordering constraint.
- [ ] 9.4 **`opensoft/OpsxFactory` — 16 across 13**, including the MCP hosting
      plan amendment. **Task 4.2 is APPROVED** (Brett Heap, `2026-09-05T23:06Z`,
      *"approve 4.2, merge #221"*, digest `4e1a4b76…`, recorded on OpsxFactory
      PR #229), so amending the plan for the new identity **REVOKES that approval
      and owes a re-approval** under the plan's requirement 2. Sequenced
      **move → amend the plan's GitHub references → Brett re-approves 4.2 over
      the new digest → 4.4/4.5 → 5.1 pin → the edge act**. See `design.md`
      § 7.2.1, which also records that this packet read the plan file's `status:`
      field and got this wrong once.
- [ ] 9.5 **`opensoft/codexFactory` itself — 532 across 211.** Its own governed
      content is its own act in its own repository.
- [ ] 9.6 **Whether a deterministic check family should verify that no live
      surface names a mapped former identity.** The exemplar left this open at
      its task 7.2. The mapping is one input such a family needs; this change's
      recorded sweep is a second. Building it here would be a second change
      riding a first.
