# Tasks: adopt-codexfactory-repository-identity

**NOTHING IN THIS FILE IS PERFORMED BY THE PROPOSAL.** Every rename, re-issuance
and cut below is implementation work for a later apply step, after ratification.
The proposal declares the identity and the disposition; the tasks execute them.

**AND NOTHING IN THIS FILE PERFORMS THE TRANSFER.** The GitHub transfer, the two
visibility flips, the aggregation lockstep, the App installations, the container
namespaces and the SonarCloud rebind are an OPERATOR ceremony ordered in
`~/session-prompts/runbook-codexfactory-org-transfer.md`. Group 9 names the
handoff points; it does not own them.

**ARCHIVED 2026-09-10, AND FIFTY OF THE FIFTY-EIGHT BOXES WERE ALREADY `[x]`
BEFORE THE ACT.** **NO BOX IS TICKED BY THIS ARCHIVE.** The remaining EIGHT —
**5.7**, **8.4** and **9.1 through 9.6** — carry the house's reserved DEFERRED
marker `- [~]`, each with its own appended note naming the holder, what has and
has not happened, and why it never gated this archive. The marker is used in
preference to a tick for a stated reason:
`scripts/proposal-support.py … archive` refuses any packet whose `tasks.md`
still matches `^- \[ \]` (*"change has incomplete tasks"*) and carries **no
bypass flag**, so ticking a box whose work did not happen would buy that
refusal off with a false claim. **THE MARKER SAYS THE BOX IS OPEN AND SAYS WHY;
IT DOES NOT SAY THE WORK IS DONE.**

**WHAT THIS ARCHIVE RESTS ON** is `release-realization`'s *Realization archive
gate* — merged-plus-green evidence for a NON-EMPTY `code_surface` — cited rather
than asserted. The citations are `review/archive-2026-09-10.md` and this
repository's README "OpenSpec Records" block, beside the `contract-v3.5` cut,
its annotated tag, the closure of 6.5 at zero unassigned occurrences, and the
eight open follow-ons above.

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
- [x] 0.2 Confirm the sequencing premise still holds:
      `adopt-medxsoft-repository-identity` is still active and still authors
      `contracts/policies/repository-identity.yaml` at its task 1.1. If that
      change is archived or withdrawn before this one realizes, task 1.1 below
      changes from "add a row" to "author the file", and `sequenced_after` is
      re-derived rather than kept out of habit.
      **DONE — PR #799 → `131adf11` (2026-09-08T14:32:34Z, lane
      `provenance-autonomous-merge`).** Premise held: `adopt-medxsoft-repository-identity`
      was neither archived nor withdrawn, so task 1.1's original "do not create
      the file here" stood at that reading. RE-CONFIRMED at this tick
      (2026-09-09): `openspec/changes/adopt-medxsoft-repository-identity/proposal.md`
      still carries `Status: draft`, still unarchived. The premise's conditional
      never fired; task 1.1 was instead AMENDED by Brett Heap on 2026-09-08 (PR
      #815) to create the file here regardless, because the exemplar remained
      unrealized — a distinct act from this confirmation.
- [x] 0.3 (2026-09-07) **Ratified.** Brett Heap, convener, verbatim **"accept
      all [A] and ratify 763"**, posted 2026-09-07T22:21:44Z on
      https://github.com/opensoft/openxFactory/pull/763#issuecomment-5576174434,
      given against head `5bfdcf3c06478167bd7509f1576db3528ce4ede1`. The
      record is `review/ratification-2026-09-07.md`, a diff in this pull
      request, which is what lets this box be ticked under house practice.
      **No box in Groups 1-8 is ticked by this act** beyond 0.1's text and this
      box — OQ-4 and OQ-6 remain open and gate the rest.

## 1. The transfer mapping row

- [x] 1.1 Add the codexFactory row to
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
      **DONE — PR #815 → `67405838` (2026-09-08T16:15:44Z, lane
      `provenance-autonomous-merge`, commit "Amend task 1.1 and author the
      repository-identity mapping file + row (T069)").** File created at
      `contracts/policies/repository-identity.yaml` with the single
      `transfers:` row exactly as amended: `former: opensoft/codexFactory`,
      `current: codeXfactory/codexFactory`, `transferred_on: null`,
      `transfer_state: pending`. Re-verified present at this tick's head
      (17167481) byte-identical to that commit.
- [x] 1.2 Record on the row the TWO divergences a reader will otherwise trip on
      (OQ-6): that the owner segment is compared CASE-SENSITIVELY by this estate
      even though the provider compares it case-insensitively, and that the
      container namespace derived from this owner is LOWERCASED by GHCR to
      `codexfactory`, so `ghcr.io/codexfactory/codexfactory/...` is the same
      identity under a different spelling.
      **DONE — PR #815 → `67405838`.** Both divergences are recorded on the row:
      `owner_case` (`codeXfactory` canonical per OQ-6, ruled 2026-09-08T03:51Z)
      and `derived_container_namespace`
      (`ghcr.io/codexfactory/codexfactory`).
- [x] 1.3 Record on the row the reference shapes the provider redirect does NOT
      cover: reusable-workflow `uses:` paths, container package namespaces, and
      federated-credential subject strings. This is the mapping's contribution to
      the fourth ADDED requirement and it is what makes the freeze safe: a frozen
      former identity resolves BY LOOKUP, never by a redirect that may lapse.
      **DONE — PR #815 → `67405838`.** `redirect_does_not_cover` enumerates all
      three shapes verbatim on the row.
- [x] 1.4 Confirm no second registration is owed: the file's
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
      **DONE — PR #815 → `67405838`.** `contracts/manifest.yaml` carries the
      `repository-identity` entry (`path: contracts/policies/repository-identity.yaml`,
      `sha256: 04bc5fed8827…`) with `consumption_rule` stating the former
      identity is read through this file and never through a provider redirect.
      Re-verified present at this tick's head.

## 2. The recorded classification sweep — the evidence

- [x] 2.1 Re-run the sweep at the realization head and file its output as
      `evidence/codexfactory-identity-sweep-<date>.md`. The command, recorded so
      the count is reproducible without this packet:

      ```sh
      git grep -ic "opensoft/codexfactory" -- .
      ```

      with the per-class totals produced by restricting the same pattern to each
      pathspec in the `design.md` § 2 table.
      **DONE — PR #799 → `131adf11` (2026-09-08T14:32:34Z).**
      `evidence/codexfactory-identity-sweep-2026-09-08.md` filed and kept current
      through every subsequent slice's reconciliation (§§ 1-18, 1083 lines at
      this tick): §§ 15-18 record the B1-B4 (#801/#802/#805/#806) reconciliation
      arithmetic at each branch's own merge head.
- [x] 2.2 Confirm the arithmetic closes at the realization head, exactly as it
      closed at `origin/main` `64aad02e` on 2026-09-07: **281 occurrences across
      150 files = 123/60 rename + 78/54 frozen + 80/36 not swept.** A drift in
      the total is expected (the corpus moves daily); a drift that does not
      classify under the published rule is a finding and is recorded before any
      rename lands.
      **DONE — PR #799 → `131adf11`.** Closed at the Slice-A head as 327/163 =
      124/60 RENAME + 78/54 FROZEN + 125/49 NOT SWEPT, every drift attributed by
      cause in the evidence file. Re-closed at each later reconciliation point
      through §18 (most recently 319/125 at `origin/main@111a5034`, re-verified
      unchanged at this tick's head `17167481`, one commit later, touching none
      of the classified files — see task 6.5).
- [x] 2.3 Classify every occurrence that appeared since 2026-09-07 by the
      published rule — coverage test first, then the records-and-assertions test
      — and NOT by a fresh judgment. Record each new occurrence and its class in
      the evidence file.
      **DONE — PR #799 → `131adf11`, extended through PRs #801/#802/#805/#806/#867
      and the codeXfactory/codexFactory#279 6.5 re-derivations.** Every new
      occurrence found at each reconciliation point was classified by the
      published rule (coverage test, then records-and-assertions), never by a
      fresh judgment — see e.g. #802's corrections to tasks 3.8 and 5.4, and
      #806's `docs/dogfood-content-migration-plan.md:49` and
      `docs/omniworker-naming.md` classifications.

## 3. Rename the live machine surfaces

Group the commits so that every fixture lands with the artifact that pins it.
A split commit here is red by construction, which is the mechanism working.

- [x] 3.1 **ONE COMMIT.**
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
      **DONE — PR #805 → `00d368a4` (2026-09-09T20:00:17Z).** Entry respelled
      and moved to FIRST position (re-verified at this tick's head: `repository:
      codeXfactory/codexFactory` is line 5, ahead of `opensoft/AdxFactory`);
      `PINNED_TABLE` respelled and reordered to match.
- [x] 3.2 In the same commit as 3.1, update
      `tests/hermes_runtime_contracts/test_domain_regression.py:410`, which pins
      the `--domain-repo <canonical-repo>=<checkout>` resolver against the
      former key. The engineering domain's resolver key becomes
      `codeXfactory/codexFactory` from the next bundle forward.
      **DONE — PR #805 → `00d368a4`.** Zero remaining `opensoft/codexFactory`
      hits in this file (re-verified at this tick's head).
- [x] 3.3 Respell the codex `repository:` in the three negative fixtures
      `contracts/hermes-runtime/fixtures/regression/{digest-mismatch,duplicate-repository,missing-exclusion-reason}.yaml`.
      Verify each still produces EXACTLY the finding it exists to produce — the
      deliberate duplicate in `duplicate-repository.yaml` is
      `opensoft/AdxFactory` and must stay the reported one.
      **DONE — PR #805 → `00d368a4`.** All three respelled, zero remaining hits
      (re-verified at this tick's head); 7.1's recorded `pytest
      tests/hermes_runtime_contracts` run (#866, 577 passed, every file green)
      confirms each negative still produces its own finding.
- [x] 3.4 `contracts/hermes-runtime/README.md` (~line 126): respell the
      denominator enumeration and put the name in its new sorted position, so
      README order and fixture order agree.
      **DONE — PR #805 → `00d368a4`.** Zero remaining hits (re-verified at this
      tick's head).
- [x] 3.5 **ONE COMMIT.** The review-lane decision-core pin and everything that
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
      **AMENDED 2026-09-09:** task 3.5 now also covers
      `contracts/review-lane-repin-binding.template.yaml:103`
      (`consumer.identity_namespace`), respelled to `github:codeXfactory` by
      convener ruling (Brett Heap, lane `provenance-autonomous-merge`,
      2026-09-09) — see `review/addendum-2026-09-08-token-namespace.md` and
      `review/amendment-2026-09-09-task-3-5.md`. The original wording above,
      naming only lines 46 and 110, stands unedited.
      **DONE — PR #801 → `e86eca35` (2026-09-09T15:40:56Z).** All listed files
      respelled in one commit, including the amended `identity_namespace` line
      (`"github:codeXfactory"`, verified present at line 104 at this tick's
      head). Zero remaining `opensoft/codexFactory` hits across `.github/`,
      `scripts/` and the three pin test files (re-verified at this tick's head).
- [x] 3.6 `.github/workflows/merge-master-approval.yml` — TWELVE occurrences at
      108, 473, 513, 522, 533, 599, 604, 617, 623, 630, 1216, 1640: the pinned
      decision-core checkout, the App-installation diagnostics whose message text
      tells an operator which repository to grant, and two summary-table rows.
      **The diagnostic text is not decoration** — it is the instruction a human
      follows when the lane refuses, so a half-respelled message sends them to
      the wrong organization.
      **DONE — PR #801 → `e86eca35`.** All twelve occurrences respelled in the
      same commit as 3.5, credential mints scoped to `owner: codeXfactory` per
      the fix round (`22125ea1`). Zero remaining hits (re-verified).
- [x] 3.7 `.github/workflows/pytest-suite.yml:396` (`repository:`) and
      `.github/merge-approval-envelope.yml:3` (the schema citation).
      **DONE — PR #801 → `e86eca35`.** Both respelled; zero remaining hits
      (re-verified at this tick's head).
- [x] 3.8 The clearing corpus — SIX files, all unsigned and therefore renameable:
      `contracts/clearing/examples/single-door-attestation.example.yaml` (13, 90,
      the widening finding's `subject:`),
      `deliberation-return.example.yaml:30` (`verified_subject_pin`), and the
      four negatives under `examples/negative/`. Confirm each negative still
      fails for its own reason and no other.
      **DONE — PR #802 → `20298c64` (2026-09-09T19:24:13Z).** **CORRECTED
      COUNT:** the corpus is SEVEN files, not six — a fifth negative
      (`admit-deliberation-clearing-operation`) arrived after 2026-09-07 and
      classifies RENAME by task 2.3's rule. All seven respelled (11 hits / 7
      files); `validate-clearing-dispatch.py` confirms 28 negative fixtures
      still refused, 26/26 closed refusal codes red-proven. Zero remaining hits
      (re-verified at this tick's head).
- [x] 3.9 The omnigent fixtures — SIX files under
      `contracts/omnigent/examples/`: the five negatives
      (`manifest-dual-domain-overlay`, `manifest-legacy-vocabulary`,
      `manifest-missing-effective-profiles`, `manifest-parallel-identity`,
      `manifest-semantic-duplicate-worker`) and
      `omnigent-install-manifest.example.yaml`. Confirm each negative still
      fails for its own reason and no other.
      **DONE — PR #799 → `131adf11` (2026-09-08T14:32:34Z).** All six respelled
      to `codeXfactory/codexFactory` (the only occurrences judged "safe now"
      ahead of the transfer). `validate-omnigent-contracts.py` reports all
      checks passed at this tick's head. Zero remaining `opensoft/codexFactory`
      hits (re-verified).
- [x] 3.10 The hermes-domain-overlay examples — TWO files:
      `examples/hermes-subject-overlay.example.yaml` and
      `examples/negative/subject-undeclared-kind/hermes/subject/project-alfa/overlay.yaml`.
      **DONE — PR #799 → `131adf11`.** Both respelled;
      `validate-hermes-domain-overlay.py` self-test reports 23 fixtures ok at
      this tick's head. Zero remaining hits (re-verified).
- [x] 3.11 `contracts/clearing/examples/factory-identity-fixture/register.yaml`
      (lines 8, 17) — the FIXTURE register's header prose, which explains that
      the whole-tree sweep resolves REAL artifacts against the LIVE register.
      This is prose about the live register and it renames with it; the fixture's
      own rows are a separate fixture identity and are checked, not assumed, at
      this task.
      **DONE — PR #802 → `20298c64`.** Header prose respelled at both lines
      (re-verified at this tick's head: lines now read `codeXfactory/codexFactory`
      at 8 and 17); the fixture's own rows left as their own fixture identity.
- [x] 3.12 `scripts/mint-factory-origin-key.py` — `TARGET_REPO` (121) and the
      two record-template lines (847, 853); and
      `tests/factory_identity/test_mint_script.py:679`, which pins the runbook's
      `gh pr merge … --repo` line the script emits.
      **DONE — PR #801 → `e86eca35`.** `TARGET_REPO = "codeXfactory/codexFactory"`
      and both record-template lines respelled; the pinned test line moves with
      it. Zero remaining hits (re-verified at this tick's head).
- [x] 3.13 `tests/factory_identity/test_validator.py` — EIGHT occurrences (107,
      366, 379, 418, 432, 479, 521, 610), the validator's default holder and the
      per-case holders. These are fixture identities inside the test and move
      with the validator's live subject.
      **DONE — PR #802 → `20298c64`.** All eight respelled to
      `codeXfactory/codexFactory` (re-verified count at this tick's head: 8
      occurrences of the new spelling, 0 of the former).

## 4. Rename the live documents

- [x] 4.1 `docs/architecture.md:25` — the DomainxFactory enumeration.
      **DONE — PR #806 → `95e67ab0` (2026-09-09T20:44:01Z).** Respelled; zero
      remaining hits (re-verified at this tick's head).
- [x] 4.2 `docs/contract-versioning-policy.md:449` — the supported-domain
      regression denominator enumeration. Keep the order consistent with the
      re-sorted fixture from 3.1.
      **DONE — PR #805 → `00d368a4`.** Respelled, order consistent with 3.1's
      re-sorted fixture (re-verified: zero remaining hits).
- [x] 4.3 `docs/terminology-and-repo-topology.md:208`, and add a one-line note
      pointing at `contracts/policies/repository-identity.yaml` as the resolver
      for former identities, so the freeze rule is discoverable from the topology
      document rather than only from this packet.
      **DONE — PR #805 → `00d368a4`.** Respelled; the pointer note is present
      at line 215 at this tick's head ("BY LOOKUP in
      `contracts/policies/repository-identity.yaml`").
- [x] 4.4 `docs/xfactory-domain-factory-model.md` — THREE occurrences (297, 888,
      890), including the `https://github.com/opensoft/codexFactory` URL.
      **DONE — PR #805 → `00d368a4`.** All three respelled; zero remaining hits
      (re-verified).
- [x] 4.5 The four factory-origin and re-pin runbooks:
      `docs/factory-origin-key-mint-runbook.md` (SIX: 69, 117, 274, 303, 309,
      325 — including the `worker-credentials` environment reference and the
      mint record's table) and `docs/review-lane-repin-runbook.md` (FIVE: 109,
      110, 111, 114, 150 — four executable `gh api` lines and a permissions
      table row). **These are commands an operator pastes**; a stale line here
      fails at the terminal rather than in CI.
      **DONE — PR #801 → `e86eca35`.** Both runbooks respelled in full, plus the
      operator-precondition paragraphs the fix round added (App installation is
      per-organization; the source-read mint fails closed). Zero remaining hits
      in either file (re-verified at this tick's head).
- [x] 4.6 `docs/roles-and-authority.md` (237, 238, 239),
      `docs/traceability-model.md` (20, 218, 219),
      `docs/omnigent-constitution.md` (40, 41),
      `docs/dogfood-content-migration-plan.md` (5, 49).
      **DONE — PR #806 → `95e67ab0`.** `roles-and-authority.md`,
      `traceability-model.md` and `omnigent-constitution.md` fully respelled
      (zero remaining hits). `dogfood-content-migration-plan.md:5` respelled;
      `:49` classified FROZEN per the records-and-assertions test (a dated
      "were created in" narration) and reverted to `opensoft/codexFactory` —
      the one remaining live-pathspec occurrence in this file, resolved through
      `contracts/policies/repository-identity.yaml` (see task 6.5).
- [x] 4.7 The single-occurrence documents: `docs/deployment-worker-model.md:9`,
      `docs/feature-decomposition.md:9`, `docs/merge-council.md:9`,
      `docs/merge-master.md:9`, `docs/pr-admission.md:9`,
      `docs/spec-kit-stage-ownership.md:11`, `docs/workflow-contract.md:105`,
      `docs/governed-reissuance-runbook.md:61`.
      **DONE — PR #806 → `95e67ab0`, plus PR #867 → `111a5034`
      (2026-09-09T21:48:20Z).** The eight listed documents respelled by #806;
      `docs/omniworker-naming.md` (new, arrived with #819 after #806 was cut,
      classified 4.7-by-class since the file postdates the packet) respelled by
      #867 as one of the two post-reconciliation stragglers the final 6.5
      re-derivation found unassigned. Zero remaining hits across all nine files
      (re-verified at this tick's head).
- [x] 4.8 `README.md` — EIGHT occurrences (316, 409, 530, 531, 642, 644, 1172,
      1184). Apply the records-and-assertions test PER LINE and record the
      outcome: 316 and 409 assert where engineering content lives (rename);
      530/531/642/644 are issue and pull-request citations in the OpenSpec
      Records block, which is a kept-current index (rename, and the numbers do
      not change — GitHub carries issue and pull-request numbers through a
      transfer); 1172 and 1184 narrate a completed dated act (**candidates for
      the freeze** — decide against the test, do not sweep, and record which
      way each went).
      **DONE — PR #806 → `95e67ab0`, plus PR #867 → `111a5034`.** #806 found
      NINE occurrences, not eight (README drifted between authoring and
      realization), applied the per-line test, and respelled 25 lines/froze 3
      across this slice's whole document set as recorded in its body; the two
      dated-narration lines corresponding to 1172/1184's class were frozen
      (now README `:1447`/`:1459` at this tick's head — content unchanged,
      line numbers moved with later commits). A tenth occurrence
      (`:2901`, the PR-227 citation URL) arrived after #806 was cut and was the
      other post-reconciliation straggler #867 respelled (numbers survive a
      transfer, so the URL renames). Remaining live-pathspec README hits at
      this tick's head: three, all FROZEN dated records (`:896`, a measurement
      quote; `:1447`/`:1459`, narrating the completed realization) — see task
      6.5.

## 5. Re-issue the factory-origin identity — HUMAN-ONLY SURFACE

**Read `design.md` § 4.3 before starting.** `governance/factory-identity/` is
declared permanently human-only: no council verdict and no autonomous or
council-cleared approval path may land a change here, and the directory is
entered BY NAME in codexFactory's never-clearable floor. **The pull request
carrying this group needs a human merge word.**

- [x] 5.1 `governance/factory-identity/register.yaml` — respell the row's
      `holder_ref` (146) and the header sentence about concurrent active rows
      (113). **One row, respelled — not a second row.** Confirm the reader still
      sees exactly one active origin row for the repository.
      **DONE — PR #802 → `20298c64` (Brett Heap's human merge, per the
      HUMAN-ONLY floor).** `holder_ref: codeXfactory/codexFactory` at line 146
      at this tick's head; `validate-factory-identity.py` confirms exactly one
      active origin row over one originating repository.
- [x] 5.2 `governance/factory-identity/wallets/wal-origin-codexfactory-0001.yaml:50`
      — respell `holder_id`. **Do not touch** `key_id`, the multibase public
      half, the fingerprint, or `holder_class`.
      **DONE — PR #802 → `20298c64`.** `holder_id: codeXfactory/codexFactory` at
      line 50; the diff is one line — `key_id`, the public half, fingerprint and
      `holder_class` untouched (re-verified at this tick's head).
- [x] 5.3 `governance/factory-identity/grants/grant-origin-codexfactory-0001.yaml`
      — respell `audience.holder_ref`, the single-element `scope.objects` entry,
      and the header's "THE SCOPE IS ONE REPOSITORY" paragraph. **Do not widen
      `objects` to carry both identities**, which the grant's own header forbids
      and which would let one key speak for a repository it was not issued for.
      **Do not extend `expires_at`**, which is `issued_at` + 90 days and is a
      separate governed question.
      **DONE — PR #802 → `20298c64`.** `holder_ref` and the single-element
      `objects` entry respelled (re-verified: `objects:` still one element at
      this tick's head); `expires_at` not extended (confirmed in the PR's own
      diff scope).
- [x] 5.4 The custody attestation beside them names the repository; respell it in
      the same commit and confirm `scripts/validate-factory-identity.py` reports
      no `factory-identity-tier-unattested` regression and no
      `FILL-IN-AT-MINT` sentinel reappears.
      **DONE (respell half is a NO-OP; validator half discharged) — PR #802 →
      `20298c64`.** `governance/factory-identity/attestations/custody-attest-wal-origin-codexfactory-0001.yaml`
      carries no `opensoft/` owner segment at all — only bare identifiers and
      prose (`wal-origin-codexfactory-0001`, `codexFactory's own hosted
      packaging environment`) that task 6.4 forbids editing (owner-segment-only
      rule). `validate-factory-identity.py` at this tick's head: 0 errors, no
      `FILL-IN-AT-MINT` sentinel.
- [x] 5.5 `tests/clearing/test_origin_signature.py` — lines 200, 204, 205, 217
      and 356 assert against the LIVE register by design. Respell in the SAME
      commit as 5.1, and `tests/clearing/test_attestation.py` (68, 75, 78) with
      it.
      **DONE — PR #802 → `20298c64`.** Both files respelled in the same commit
      as 5.1; `pytest tests/clearing tests/factory_identity` → 283 passed at
      that head (re-run at this tick's head as part of task 7.1's validators:
      481 passed with `tests/review_lane_pin` folded in, per PR #866).
- [x] 5.6 Run `scripts/validate-factory-identity.py` and
      `scripts/validate-clearing-dispatch.py` green on the re-issued tree, and
      record that the disjointness rule over key material is unaffected — no
      `key_id`, `did` or fingerprint moved.
      **DONE — PR #802 → `20298c64`, re-confirmed at this tick's head.**
      `validate-factory-identity.py`: 0 errors, disjointness holds (4 vs 46
      identifiers, 0 shared — the right-hand count grew only because an
      unrelated register act landed 5 seats in between, zero intersection
      either way). `validate-clearing-dispatch.py`: 0 errors, 0 warnings, 28
      negative fixtures refused, 26/26 closed refusal codes red-proven. No
      `key_id`, `did` or fingerprint moved (5.2's one-line diff).
- [~] 5.7 **OPERATOR HANDOFF, not performed here:** verify that codexFactory's
      `worker-credentials` environment and its `FACTORY_ORIGIN_SIGNING_KEY`
      secret survived the repository transfer, and re-attest custody if they did
      not. Runbook step, recorded here so the dependency is visible from the
      packet.
      **DEFERRED 2026-09-10, AT THE ARCHIVE — OPEN, OWNED, AND NOT CLAIMED.**
      **Owner: the operator**, as a step of
      `~/session-prompts/runbook-codexfactory-org-transfer.md`. It did not gate
      this archive and nothing here reads as saying the custody check happened:
      the box's OWN FIRST WORDS are *"OPERATOR HANDOFF, not performed here"*,
      authored that way at ratification. Its subject is **not readable from
      this corpus at all** — codexFactory's `worker-credentials` environment
      and the `FACTORY_ORIGIN_SIGNING_KEY` secret inside it live in the
      repository that moved (`codeXfactory/codexFactory`, private), so no
      evidence for it could be filed here even had it been performed. The
      `- [~]` marker is the house's reserved DEFERRED form
      (`openspec/changes/archive/2026-08-21-add-doxbench-editing-phase-a/tasks.md`
      § 5.3; most recently
      `archive/2026-09-09-add-openspec-cli-pin/tasks.md` § 6.2 and
      `archive/2026-09-09-pin-openspec-cli-dependency-closure/tasks.md`
      §§ 6.1/6.2) and is used in preference to a tick precisely because a tick
      would claim a custody verification this lane did not perform and cannot
      read. **THE MARKER SAYS THE BOX IS OPEN AND SAYS WHY.**

## 6. Verify the freeze

- [x] 6.1 Assert **with a diff, not by inspection**, that the 78 occurrences
      across 54 files in the frozen classes are byte-unchanged after Groups 3-5:
      `contracts/signed-execution-chain/**` (44/34),
      `openspec/changes/archive/**` (15/10), `specs/**` (18/9), and
      `docs/decisions/0002-xfactory-aggregation-repo.md` (1/1).
      **DONE — PR #799 → `131adf11`** (empty diff over every frozen pathspec at
      the Slice-A head) **and RE-ASSERTED at every later B-slice head** — #801,
      #805, #806 each report `git diff --name-only origin/main HEAD --
      contracts/signed-execution-chain/ openspec/changes/archive/ specs/
      docs/decisions/ ideation/` **EMPTY**. Re-measured at this tick's head
      (17167481, one commit past the final 6.5 re-derivation point): frozen
      subtotal is 44/34 + 17/10 + 55/17 + 1/1 = 117/62 (grown from the packet's
      78/54 baseline only because `specs/**` and `openspec/changes/archive/**`
      gained content from unrelated lanes — the classified files this change
      could touch are unchanged).
- [x] 6.2 Run `scripts/validate-signed-execution-chain.py` green and record that
      `ratification_signature_verifies` and `chain_identity_recomputes` pass for
      all 34 files. **This is the check that would have caught a well-meaning
      corpus-wide sed**, and recording it green is the evidence that none was
      run.
      **DONE — PR #799 → `131adf11`** (0 errors, 95/95 refusal codes
      red-proven) **and re-confirmed at PR #866 → `a37ae0cd`** (0 errors, 0
      warnings, 113 packaged records / 108 negative fixtures / 95/95 closed
      refusal codes red-proven, "the 34 signature-covered files are
      byte-unchanged"). Re-run at this tick's head: 0 errors, 0 warnings.
- [x] 6.3 Assert that the 80 occurrences across 36 files in the NOT-SWEPT classes
      — other lanes' active change packets (74/32) and `ideation/**` (6/4) — are
      byte-unchanged. A diff touching another lane's unmerged packet is a
      lane-collision and is reverted, not merged.
      **DONE — PR #799 → `131adf11` and re-asserted at every B-slice head**
      (same empty-diff freeze check as 6.1, covering `openspec/changes/`
      excl. `archive/` and `ideation/`). No commit in this realization ever
      touched a file outside its own declared task list. Re-measured at this
      tick's head: NOT-SWEPT subtotal 172/45 + 19/13 = 191/58, unchanged from
      the `origin/main@111a5034` final re-derivation (one commit prior).
- [x] 6.4 Confirm no BARE `codexFactory` name was edited anywhere. A transfer
      moves the OWNER segment only; bare member names, `--aggregate-members`
      lists, dashboard groupings, directory names and submodule paths are correct
      before and after.
      **DONE — PR #799 → `131adf11`.** The count-equality form of this check was
      itself wrong (false-positived on the change id's own bare substring) and
      was corrected to a multiset compare of bare occurrences removed vs added
      on diffs with removals (add-only diffs cannot have edited anything). PASS
      at the Slice-A head. Every respelling commit thereafter (#801, #802,
      #805, #806, #867) is documented as an exact `opensoft/codexFactory` →
      `codeXfactory/codexFactory` substitution with matched removed/added
      counts (e.g. #802: "37 removed, 37 added, case exact — every added
      spelling is precisely `codeXfactory/codexFactory`"); task 5.4 was left
      unedited specifically because it holds only bare forms, which is 6.4
      holding rather than being violated.
- [x] 6.5 Confirm zero remaining live occurrences of `opensoft/codexFactory`
      outside the frozen and not-swept sets.
      PRECONDITION (ruled 2026-09-09): the per-line verdict table is
      re-derived at the ceremony window, not carried forward; any new
      RENAME-class occurrence found then is assigned to a slice before #801
      merges.
      **DONE — LAST, per the ceremony merge order (lane
      `provenance-autonomous-merge`).** Final re-derivation posted at
      codeXfactory/codexFactory
      [issue #279, "6.5 FINAL re-derivation at openxFactory@111a5034
      2026-09-09T22:10Z"](https://github.com/codeXfactory/codexFactory/issues/279)
      and ruled in the immediately following comment, ["6.5 FINAL ruling
      (lane) 2026-09-09T21:58Z"](https://github.com/codeXfactory/codexFactory/issues/279)
      (posted after the re-derivation comment; timestamps as authored on the
      issue). At `origin/main@111a5034` (merge of #867, the last of the two
      post-reconciliation stragglers): whole-tree count 319 occurrences / 125
      files, closing exactly as **RENAME-pathspec remainder 11 hits / 5
      files** (all ruled FROZEN) **+ FROZEN subtotal 117/62 + NOT-SWEPT
      subtotal 191/58 = 319/125**. The 11/5 RENAME-pathspec remainder, each
      ruled FROZEN by class (dated release narration, the mapping's own lookup
      key, or a validator-rejection sentence whose meaning would invert if
      respelled) — no code change, no respell:
      `contracts/policies/repository-identity.yaml:101,106` (the mapping's own
      `former:` lookup key — permanent by construction);
      `docs/dogfood-content-migration-plan.md:49` (task 4.6's frozen line);
      `README.md:895,1446,1458` (dated realization narration, task 4.8);
      `contracts/CHANGELOG.md:16,86,123,258` (the `contract-v3.5` dated release
      entry, introduced by the bundle cut `a37ae0cd`/#866 after the
      `origin/main@95e67ab0` re-derivation — a dated changelog narrating the
      rename, the frozen mapping row quoted, a before/after CLI migration
      example, and a validator-refusal sentence); `tests/intent-compliance/test_release_boundary.py:102`
      (a docstring narrating the cut as a dated past event). **Zero unassigned
      occurrences.** RE-VERIFIED, read-only, at this tick's own head
      (`17167481`, one commit past `111a5034`, touching none of the classified
      files): identical arithmetic — 319 occurrences / 125 files, RENAME
      remainder still exactly the same 11 hits across the same 5 files (line
      numbers shifted by the intervening commit's unrelated churn; content
      byte-identical), FROZEN 117/62 and NOT-SWEPT 191/58 both unchanged.

## 7. Cut the contract bundle

- [x] 7.1 Run the full suite and the affected validators green on the renamed
      tree BEFORE touching any release surface:
      `python3 -m pytest tests/hermes_runtime_contracts tests/clearing tests/factory_identity tests/review_lane_pin`,
      `scripts/validate-hermes-runtime-contracts.py`,
      `scripts/validate-factory-identity.py`,
      `scripts/validate-clearing-dispatch.py`,
      `scripts/validate-signed-execution-chain.py`,
      `scripts/validate-omnigent-contracts.py`,
      `scripts/validate-hermes-domain-overlay.py`.
      **DONE — recorded on PR #866 → `a37ae0cd` (2026-09-09T21:47:48Z, lane
      `provenance-autonomous-merge`), run at the bundle-cut candidate on the
      fully renamed tree (after #801/#802/#805/#806 all landed):**
      `pytest tests/clearing tests/factory_identity tests/review_lane_pin` →
      **481 passed, 2 skipped, 54 subtests passed** (20.7s);
      `pytest tests/hermes_runtime_contracts` (23 files, run file by file) →
      **577 passed**, every file green;
      `pytest tests/intent-compliance tests/clearing tests/credential_contracts`
      → **739 passed** (108s, includes the release-boundary test's 13);
      `scripts/validate-hermes-runtime-contracts.py` → **pass** (51 contracts,
      32 schemas, 110 fixtures, 17 requirements, 85 scenarios, 439 tests
      collected);
      `scripts/validate-factory-identity.py` → **0 errors** (1 active origin
      row, disjointness holds 4 vs 46 identifiers, 0 shared);
      `scripts/validate-clearing-dispatch.py` → **0 errors, 0 warnings** (7
      packaged records, 28 negative fixtures refused, 26/26 closed refusal
      codes red-proven);
      `scripts/validate-signed-execution-chain.py` → **0 errors, 0 warnings**
      (113 packaged records, 108 negative fixtures, 95/95 closed refusal codes
      red-proven, 34 signature-covered files byte-unchanged);
      `scripts/validate-omnigent-contracts.py` → **all checks passed**;
      `scripts/validate-hermes-domain-overlay.py` → **self-test ok, 23
      fixtures**. RE-RUN at this tick's head (`17167481`) for the six
      single-invocation validators as a freshness check: all six pass with the
      identical readings above (`validate-hermes-runtime-contracts.py`,
      `validate-factory-identity.py`, `validate-clearing-dispatch.py`,
      `validate-signed-execution-chain.py`, `validate-omnigent-contracts.py`,
      `validate-hermes-domain-overlay.py` — no argument, self-test/repo-scan
      mode).
- [x] 7.2 Follow `docs/contract-versioning-policy.md` § Bundle Realization Order:
      rebase onto the final integration point, recheck availability, and allocate
      the next available additive minor after `contract-v3.4` THEN — no number is
      reserved by this packet, and this packet has a live ordering dependency
      besides.
      **DONE 2026-09-09 (lane `provenance-autonomous-merge`).** Integration point
      `origin/main` at `95e67ab0` — the merge of #806, the LAST of the four gated
      realization slices, committed 2026-09-09T20:44:00Z. The candidate was first
      derived at `00d368a4` (#805, 20:00:16Z) and RE-DERIVED at `95e67ab0` when
      `main` moved, per step 1; neither #806 nor #864 touches a release-inventory
      member, so the re-derivation moved no digest the first derivation had not.
      Availability RE-CHECKED at the final tip, not carried
      forward: `git ls-remote --tags origin 'refs/tags/contract-v*'` publishes
      annotated tags through `contract-v3.4` (`807a4f47`),
      `refs/tags/contract-v3.5` is ABSENT, `contracts/releases/` held inventories
      through `contract-v3.4.digests.yaml`, and there is no `Unreleased` block in
      `contracts/CHANGELOG.md`. **`contract-v3.5` allocated** — additive minor,
      no earlier bundle owing a tag, no number reused.
- [x] 7.3 In one atomic candidate commit: `contracts/manifest.yaml`
      (`contract_bundle_version`), `contracts/CHANGELOG.md` (one entry naming the
      transfer, the EIGHT moved members, the mapping row, the origin re-issuance,
      and the `--domain-repo` key migration note), and the realized
      `contracts/releases/<bundle-tag>.digests.yaml` built by
      `scripts/validate-contract-release.py build --tag <tag>`. **Never hand-edit
      an existing inventory to make a comparison pass.**
      **DONE 2026-09-09 (lane `provenance-autonomous-merge`).** One candidate
      commit on `release/contract-v3.4-bundle-cut`:
      `contracts/manifest.yaml` (`contract-v3.4` → `contract-v3.5`),
      `contracts/CHANGELOG.md` (the `contract-v3.5` entry, which names all five
      required things and adds the measured "also carried" attribution — four
      `contracts/` additions and twenty-seven modifications between the two
      cuts), `contracts/releases/contract-v3.5.digests.yaml` built by
      the tool and never hand-edited, and `tests/intent-compliance/test_release_boundary.py`
      (`FEATURE_SUCCESSOR_9`, both match arms, and the by-hand statement every
      cut past the intent-compliance floor owes — measured at ZERO
      intent-compliance paths moved). Inventory: 283 members, membership
      UNCHANGED, no `git_mode` change, TWELVE digests re-baselined. NO existing
      inventory row was touched: `contract-v3.4.digests.yaml` is byte-unchanged.
- [x] 7.4 `scripts/validate-contract-release.py verify-commit --commit <sha>`
      clean at the candidate; `verify-promotion` before tagging; publish the
      annotated tag at the exact published commit and `verify-tag` from a fresh
      checkout.
      **OPERATOR ACT — NOT the cutting lane's.** `verify-promotion` and the
      annotated tag are RELEASE SURFACES and the ceremony runbook's ownership
      legend does not cover them; row 5 of its merge order assigns them to the
      operator. The exact four-command sequence, to be run from a freshly
      refreshed openxFactory checkout AFTER the cut lands on `main`, is recorded
      in the `contract-v3.5` changelog entry § *The annotated tag is published at
      the LANDED commit, not from this branch*. `verify-commit` at the CANDIDATE
      is recorded on the cutting pull request; the re-run at the LANDED commit is
      step 1 of that sequence, because a squash merge always creates a different
      commit and skipping the re-verification is what made `contract-v3.1`
      defective.
      **DONE.** Bundle cut PR #866 landed on `main` (rebase merge, single-parent
      declaring commit) at `a37ae0cdabed0b2407b7d6b2da4d24fb12718059`,
      2026-09-09T21:47:48Z. Brett Heap, operator, 2026-09-09T22:31:05Z: ran
      `verify-commit --commit a37ae0cd` (pass), `verify-promotion --commit
      a37ae0cd --remote origin --tag contract-v3.5` (pass), then created and
      pushed the annotated tag `contract-v3.5` at that exact commit (a first
      attempt from the stale shared checkout, 912 commits behind, was refused
      by that checkout's own stale validator — an environment artifact, not a
      bundle defect; the retry from a fresh worktree succeeded). **`verify-tag`
      re-run here from an INDEPENDENTLY FRESH clone** (`git clone
      git@github.com:opensoft/openxFactory.git`, `git fetch --tags`, `git
      checkout --detach origin/main`, HEAD at `17167481`):
      ```
      python3 scripts/validate-contract-release.py verify-tag --remote origin --tag contract-v3.5
      release verify-tag: pass
      ```
      `git ls-remote --tags origin contract-v3.5` confirms the tag object
      `6c602f3cbf4796fad58263a96313132c30e26599` resolves to commit
      `a37ae0cdabed0b2407b7d6b2da4d24fb12718059`. Clone removed after
      verification.
- [x] 7.5 Re-run doc-health and record `release-inventory-drift` at **0 findings**
      after the cut. Record the transient too: between Group 3 and 7.3 the family
      reports EIGHT `ERROR` findings (the eight non-editorial members), which is the
      family working and is the reason the cut is sequenced inside this change.
      **DONE — recorded on PR #866 → `a37ae0cd`.** At the base tip `95e67ab0`,
      BEFORE the cut: `verify-commit` reports **ten** `HGR-RELEASE-DIGEST-MISMATCH`
      findings — the **EIGHT** non-editorial members graded `ERROR` (the
      predicted transient), plus `contracts/manifest.yaml` and
      `contracts/README.md`, editorial and graded `INFO`. At the candidate
      `062211b6`, AFTER the cut: `doc-health.py --single-repo . --family
      release-inventory-drift` → **`release-inventory-drift`: No findings**
      (0); `release-tag-publication` also reports no findings (the declaring
      commit is the tip).

## 8. Corpus bookkeeping

- [x] 8.1 Add the one-line active-change entry to the README "OpenSpec Records"
      block (done in the proposing commit) and keep the README doc index current.
      **DONE — in the proposing commit (PR #763, ratified 2026-09-07) and kept
      current since.** `README.md` carries the `adopt-codexfactory-repository-identity`
      entry in the OpenSpec Records block (re-verified present at this tick's
      head, e.g. lines ~700 and ~881) and its proposal/review links resolve.
- [x] 8.2 `OPENSPEC_TELEMETRY=0 openspec validate adopt-codexfactory-repository-identity --strict`
      and `--all --strict` green. **The expected `--all` result is 98 passed /
      1 failed**, the one failure being the pre-existing deltaless disposition
      packet `disposition-codexfactory-declared-renames`, which this change
      neither causes nor repairs.
      **DONE — first satisfied at PR #799 → `131adf11`; RE-RUN at this tick's
      head (`17167481`).** Single-change validate: `Change
      'adopt-codexfactory-repository-identity' is valid`. `--all --strict`:
      **97 passed / 3 failed (100 items)** — the count has moved from the
      task's authored expectation of 98/1 because the shared baseline grew two
      more pre-existing failures since (recorded on PR #866 and re-confirmed
      here): `change/disposition-codexfactory-declared-renames` (the original,
      unrelated to this change), `spec/neutral-product-pin`, and
      `spec/repo-boundary-governance` — the latter two arrived with other
      lanes' unrelated changes (#813/#828) and are neither caused nor repaired
      by this diff. The number to compare against going forward is **3**, not
      1; a fourth failure would be a real defect in a future slice.
- [x] 8.3 `python3 scripts/validate-sequenced-after.py` green, with this change
      resolving `adopt-medxsoft-repository-identity` and introducing no cycle.
      **DONE — first satisfied at PR #799 → `131adf11`; RE-RUN at this tick's
      head.** `sequenced_after validation passed (39 active changes, 9
      declaring the field)`; archive-date and archive-date-vs-commit agreement
      both passed (12 dispositions in force). No cycle introduced.
- [~] 8.4 Run `python3 openxFactory/scripts/sync-notebooklm-books.py . --apply`
      after the doc changes land, per the projection workflow.
      **NOT TICKED — no evidence found that this sync was run after this
      change's doc updates.** Left unticked rather than assumed; the
      NotebookLM projection state is external to this repository and not
      verifiable from the corpus alone.
      **DEFERRED 2026-09-10, AT THE ARCHIVE — OPEN, OWNED, AND NOT CLAIMED, on
      the reading the box already carried.** **Owner: whoever next runs the
      projection sync**; the workflow and its auth runbook are
      `docs/lifecycle-notebook-projection.md`. The archive moves the MARKER and
      nothing else: the box was authored `- [ ]` and its own body already says
      the NotebookLM projection state is *"external to this repository and not
      verifiable from the corpus alone"*. `- [~]` is used because
      `scripts/proposal-support.py … archive` refuses any packet whose
      `tasks.md` still matches `^- \[ \]` (*"change has incomplete tasks"*) and
      carries NO bypass flag — so ticking a box whose work did not happen would
      buy that refusal off with a false claim. The doc-health family that would
      measure the drift, `notebook-projection-drift`, is itself SKIPPED on every
      run of this corpus (*"nlm unauthenticated or sync unavailable; family runs
      in operator-triggered runs only"*), which is the same fact from the
      checker's side.

## 9. Named follow-ons — NOT performed here

- [~] 9.1 **The operator ceremony**, in full, is
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
      **DEFERRED 2026-09-10, AT THE ARCHIVE — OPEN, OWNED, AND NOT CLAIMED.**
      **Owner: the operator.** Group 9's own heading is *Named follow-ons — NOT
      performed here*, ratified in that form, so no box in it gated this
      archive. PARTLY PERFORMED and named as such rather than left to be found:
      the transfer itself, the two visibility flips and the lockstep commit are
      DONE (see 9.3), and the openxFactory visibility flip **still gates on
      OQ-3's four ideation-split moves landing first**, which this archive does
      not assert have landed. The remainder of the ceremony — the App
      installations, the environment and secret inventory (see 5.7), the GHCR
      dual-publish window and prefix flip (OQ-4, still UNRULED), the SonarCloud
      rebind — is the operator's, on the runbook, and is not claimed here.
- [~] 9.2 **`installs/hermes-install` — 181 occurrences across 84 files**,
      including `config/clients/opensoft/overlay.yaml` (5) and
      `tests/unit/test_subject_pin_guard.py` (36). A separate act in that
      repository. **This packet DECLINES the exemplar's "at its next pin bump"
      disposition for this repository** and asks that it be scheduled as a step
      of the ceremony with its own test-count proof, because at 181 occurrences
      including a live client overlay, an unbounded deferral leaves a live
      install naming a dead identity.
      **DEFERRED 2026-09-10, AT THE ARCHIVE — OPEN, OWNED, AND NOT CLAIMED.**
      **Owner: `installs/hermes-install`** (`opensoft/xFactory-Hermes-Install`),
      as its own act in its own repository. NOTHING HAS SWEPT IT: the 181
      occurrences across 84 files stand, `config/clients/opensoft/overlay.yaml`
      and `tests/unit/test_subject_pin_guard.py` included, and this marker says
      so rather than letting an archive imply otherwise. The box's ratified text
      DECLINES the exemplar's *"at its next pin bump"* deferral for this
      repository and asks for a scheduled ceremony step with its own test-count
      proof; that request is carried forward by this marker, unanswered.
- [~] 9.3 **`opensoft/xFactory` (aggregation) — 25 across 14.** No
      aggregation-level OpenSpec act is owed; the lockstep commit is a runbook
      step and a hard ordering constraint.
      **DEFERRED 2026-09-10, AT THE ARCHIVE — LARGELY PERFORMED, AND THE PART
      THAT IS NOT IS NAMED.** **Owner: the operator, on the runbook.** The
      lockstep commit this box calls a hard ordering constraint HAS LANDED:
      [xFactory #376](https://github.com/opensoft/xFactory/pull/376) →
      `376275c4` (2026-09-09T19:29:34Z), fifteen files in one commit —
      `.gitmodules`, the `xFactories/codexFactory` gitlink, `README.md`, seven
      council/lane workflows, `.github/merge-approval-envelope.yml`,
      `docs/council-lane-app-registration.md` and the two workflow pin tests —
      with NO sha moved, as its title states. The box stays open rather than
      ticked because it is a Group 9 follow-on whose scope is the aggregation's
      whole 25-across-14 measurement and no aggregation-side re-count was filed
      here; the marker records what landed and does not claim the residue.
- [~] 9.4 **`opensoft/OpsxFactory` — 16 across 13**, including the MCP hosting
      plan amendment. **Task 4.2 is APPROVED** (Brett Heap, `2026-09-05T23:06Z`,
      *"approve 4.2, merge #221"*, digest `4e1a4b76…`, recorded on OpsxFactory
      PR #229), so amending the plan for the new identity **REVOKES that approval
      and owes a re-approval** under the plan's requirement 2. Sequenced
      **move → amend the plan's GitHub references → Brett re-approves 4.2 over
      the new digest → 4.4/4.5 → 5.1 pin → the edge act**. See `design.md`
      § 7.2.1, which also records that this packet read the plan file's `status:`
      field and got this wrong once.
      **DEFERRED 2026-09-10, AT THE ARCHIVE — OPEN, OWNED, AND NOT CLAIMED.**
      **Owner: `opensoft/OpsxFactory`**, as its own act in its own repository.
      NOTHING HAS AMENDED THE PLAN, so the consequence this box exists to record
      has NOT been triggered: task 4.2's approval (Brett Heap,
      `2026-09-05T23:06Z`, *"approve 4.2, merge #221"*, digest `4e1a4b76…`, on
      OpsxFactory PR #229) still stands over the OLD digest, and the moment the
      plan's GitHub references are amended for the new identity that approval is
      REVOKED and a re-approval is owed under the plan's requirement 2. The
      sequence the box names — move → amend → re-approve over the new digest →
      4.4/4.5 → 5.1 pin → the edge act — is carried forward intact.
- [~] 9.5 **`opensoft/codexFactory` itself — 532 across 211.** Its own governed
      content is its own act in its own repository.
      **DEFERRED 2026-09-10, AT THE ARCHIVE — LARGELY PERFORMED, AND THE PART
      THAT IS NOT IS NAMED.** **Owner: `codeXfactory/codexFactory`**, as its own
      act in its own repository, which is what the box says. Phase 4 of the
      ceremony HAS LANDED there:
      [codexFactory #308](https://github.com/codeXfactory/codexFactory/pull/308)
      → `373410bc` (2026-09-09T19:16:31Z), *"Org move Phase 4: codexFactory
      self-references follow the repository to codeXfactory"* — 49 files,
      carrying its own 710-line sweep record
      `docs/org-move-phase4-self-reference-sweep-2026-09-09.md`, which is where
      the disposition of the residue of the 532-across-211 measurement is
      recorded. The box stays open rather than ticked because that record, not
      this packet, is the authority on what remains, and no re-count was filed
      here.
- [~] 9.6 **Whether a deterministic check family should verify that no live
      surface names a mapped former identity.** The exemplar left this open at
      its task 7.2. The mapping is one input such a family needs; this change's
      recorded sweep is a second. Building it here would be a second change
      riding a first.
      **DEFERRED 2026-09-10, AT THE ARCHIVE — UNRULED, AND DELIBERATELY NOT
      DECIDED HERE.** **Owner: a future change**, if a convener rules one is
      owed. NO SUCH CHECK FAMILY EXISTS and none was authored: the box's own
      closing words are *"Building it here would be a second change riding a
      first"*, and the exemplar `adopt-medxsoft-repository-identity` left the
      same question open at its task 7.2. The two inputs such a family would
      need are now both on record — the transfer mapping in
      `contracts/policies/repository-identity.yaml` and this change's recorded
      sweep at `evidence/codexfactory-identity-sweep-2026-09-08.md` — so the
      question is better posed after this archive than before it, which is the
      only thing this marker claims.
