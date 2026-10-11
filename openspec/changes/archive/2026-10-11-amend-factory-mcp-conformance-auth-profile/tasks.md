# Tasks: amend-factory-mcp-conformance-auth-profile

Status: ratified
Ratified by: amend-factory-mcp-conformance-auth-profile - 2026-10-08T20:2xZ, Brett Heap, "Ratify, OQs as recommended (Recommended)", RULED 2026-10-08T20:33:25Z (record `review/ratification-2026-10-08.md`)
Kind: tasks
Authored: 2026-10-08, lane `openxfactory-5` (display `openXfactory-5`).

These are governance checkpoints. The single Speckit feature created at 2.1
owns the executable implementation tasks, and this file does not duplicate
them. Boxes for acts that have not happened stay `- [ ]` until their act.
Boxes for work this change will never do carry `[~]`, in § 5.

## 0. Ratification

- [x] 0.1 Brett Heap's ratify word on this exact packet, including his answer
  to OQ-1 to OQ-6 in `design.md` ("as recommended" adopts all six). The three
  rulings of 2026-10-08 decide what the packet must say. They do not ratify
  it. **RATIFIED AS DRAFTED 2026-10-08** - Brett Heap's word at 2026-10-08T20:2xZ,
  in session to lane `openXfactory-5`, verbatim *"Ratify, OQs as recommended
  (Recommended)"*; RULED on the estate's lane register at
  2026-10-08T20:33:25Z. It adopts all six open questions at the recommended
  answer (OQ-1 admit the `issuer_assigned` binding, OQ-2 algorithms closed at
  RS256 plus optional EdDSA, OQ-3 RFC 9728 path insertion with a query
  refused, OQ-4 an `auth` evidence-or-gap concern, OQ-5 `schema_version: 1`
  first-bundled at the next minor, OQ-6 exactly one issuer), and no
  requirement or scenario text moved. It is a ratify word only: not a landing
  word, and it archives nothing. Record: `review/ratification-2026-10-08.md`.
- [x] 0.2 On the word, in one commit: `Status: ratified` plus a `Ratified:`
  line in `proposal.md`; `Status: ratified` plus `Ratified by:` here and in
  `design.md`; the `approved_by`/`approved_on` pair in `.openspec.yaml` (the
  `proposal-origin` family refuses a ratified status without it); a record
  under `review/`; and the README *Active changes* entry updated. Done in the
  one ratifying commit, which also marks each OQ RULED beside it in
  `design.md`'s table, with no requirement or scenario text touched.

## 1. This packet

- [x] 1.1 Authored: `proposal.md`, `design.md`, this file, `.openspec.yaml`,
  and one delta, `specs/factory-mcp-conformance/spec.md`, with four
  `## ADDED` requirements (16 scenarios) and one `## MODIFIED` requirement
  (3 scenarios). Every requirement has a scenario, and every body states its
  SHALL on its first line.
- [x] 1.2 The MODIFIED block is canon's block (`main` `80f47483`,
  `openspec/specs/factory-mcp-conformance/spec.md`, *Lossless results and
  explicit failures*, 15 lines) with only the narrowed words changed. `diff`
  of canon's block against the delta's reports exactly two hunks, `3c3` (the
  body paragraph: one sentence inserted, one clause qualified) and `10c10`
  (the *Unavailable dependency* WHEN bullet). The title, the THEN bullet, and
  the scenarios *Negative evaluation* and *Existing digested result* are
  byte-identical.
- [x] 1.3 Bookkeeping: one README *Active changes* bullet; the sweep-ledger
  rows in `tests/sequenced_after/corpus-ledger.yaml`, seeded by the sanctioned
  seeder with `--moved-by '#1274'`; one `_LEDGER_SUBJECTS` data row in
  `tests/doc-health/test_modified_block_currency_self_gate.py` naming this
  packet's MODIFIED block, which retires at 4.1. The seeder moved TWO rows:
  this change's new row, and `add-factory-mcp-conformance` from `sole` to
  `co-modifier`, which the ledger's own rule requires of a MODIFIED block
  over a partner's requirement. The #630 claim (comment `6066626855`) stated
  its expected movement as one new ledger row, so the partner row was outside
  its wording. **The claim was amended, to both ledger-row movements and the
  `_LEDGER_SUBJECTS` row, in #630 comment `6068473680` (2026-10-08T20:29Z),
  before the ratify word was recorded on the lane register, 2026-10-08T20:33:25Z.**
  The authoring seat posted no issue comment; the
  lane's coordinator did.
- [x] 1.4 Gates at the LANDING head, the exact head the landing word names
  (it carries every commit made after the ratifying commit, so evidence from
  an earlier head is not enough), in a full clone named
  `openxFactory` with the three gitlinks initialized as CI initializes them:
  the pinned OpenSpec CLI (`scripts/validate-openspec-cli-pin.py --all
  --strict`, and `--change`), `scripts/proposal-support.py . verify`,
  `scripts/validate-sequenced-after.py .` (plain and `--ledger-diff`),
  `scripts/validate-code-surface.py .`, `scripts/validate-target-release.py .`,
  doc-health `--single-repo .`, the pytest modules CI runs for these surfaces
  and the required `pytest-suite` check, `git diff --check`, and a
  closing-keyword scan of every commit and the pull request body. Until then
  the pull request body records each run against the head it ran at. Every
  red is compared with `main` in the same clone kind.
  **Done at the landing head, and recorded on the pull request as this box
  asks.** Verified 2026-10-11, at the archive, by lane `openxfactory-5`
  (display `openXfactory-5`) from the pull request and its check runs, not
  from a handoff. The landing head is
  [#1274](https://github.com/opensoft/openxFactory/pull/1274)'s final head
  `8e56ac5814f38d9a54b2f5bf76dfd77b8a511425`, the head the land word of 3.1
  landed. The body's table *Gates at the pushed head `8e56ac58`* records, at
  that head, in a full clone named `openxFactory` with the three gitlinks
  initialized: the pinned CLI with `--change` (rc 0) and `--all --strict` (rc
  0, 114 passed plus the accepted `add-chain-attestation` exception);
  `proposal-support.py . verify` (ok); `validate-sequenced-after.py .` and
  `--ledger-diff` (rc 0, 237 rows); `validate-code-surface.py .` and
  `validate-target-release.py .` (rc 0); doc-health `--single-repo .` (rc 0,
  with exactly one added finding, the INFO `modified-block-currency` finding
  that 1.3's `_LEDGER_SUBJECTS` row names); `git diff --check` (clean); and
  the closing-keyword scan of its 14 commits and the body (no hit). Each red
  is compared there with `main` in the same clone kind. Some of the body's
  local pytest runs were made at earlier heads, which it names:
  `tests/doc-health` and `tests/proposal-support` at `89506b51`, and six
  further directories on the ratifying tree. At the landing head itself every
  pytest module ran inside the required `pytest-suite` check, run
  [37869532651](https://github.com/opensoft/openxFactory/actions/runs/37869532651)
  (`selected=9839 passed=9833 skipped=6 failures=0 errors=0`), and of the 17
  check runs at `8e56ac58`, 16 concluded success and Sourcery's was skipped.

## 2. Realization (one Speckit feature, after 0.1 and never before it)

- [x] 2.1 Create the Speckit feature from the ratified packet. Its spec and
  plan trace to this delta, and it runs clarify, plan, checklists, tasks and
  analyze.
  **Done** in Speckit feature 039, `specs/039-factory-mcp-auth-profile/`,
  created from the ratified packet at `main` `93d13d6c` (#1274's landing). Its
  `spec.md` and `plan.md` trace to this delta. It ran clarify (no question:
  the ratified packet decides every material question), plan, seven domain
  checklists at maximum coverage (97 items), tasks T001 to T028, and analyze,
  whose round 1 findings were each fixed or kept with a reason, leaving no
  CRITICAL finding (`verification.md` § 2).
- [x] 2.2 Tests in `tests/factory-mcp/`. Red-first for every NEW refusal,
  committed before any schema or validator change and shown failing against the
  validator on `main`; characterization for what `main` already does:
  - one red-first test per new code in `design.md` D7, and per existing code at
    its new `/service/auth/...` location (`main` has no block to inspect, so
    each fails there);
  - characterization tests, which pass on `main` and must keep passing: a
    not-deployed service carrying `auth` is refused with `schema_oneOf` at
    `/service` (the closed branch rejects it today), and a stdio-only
    declaration that needs no block validates;
  - structure: a block that breaks its closed shape (an unknown field, a
    repeated algorithm, a `binding` outside the closed set, and an `issuer`
    given as a list or as more than one issuer, which pins OQ-6's exactly one
    issuer) is refused with
    `schema_oneOf` at `/service`, the structure pass not descending into the
    `oneOf` branches (`design.md` D7), beside a valid-block test that is red on
    `main`;
  - the scenarios of the four ADDED requirements, including a hosted
    declaration without the block, an algorithm list without RS256, `none`
    and each HMAC name in more than one letter case, an audience bound to
    another resource, an issuer carrying userinfo, a hosted canonical
    resource URI carrying a query, and a dangling id and a repeated id in the
    block's `evidence_ids` and in its `gap_ids`;
  - M5: an error-inventory dependency code mapped as a completed evaluation is
    refused, and a result status mapped as an execution failure is refused.
    The enforcement exists already, so these are shown red against a mutant
    of `main`'s validator with the classification comparison removed, and
    green against `main`'s own (`design.md` D8).
  Synthetic identifiers only: no real issuer, tenant, host or domain schema.
  **Done, red first.** The tests were committed alone at `bd76faf4`, before
  any schema, example or validator byte. Run there, against `main`'s
  validator: 93 failed, 97 passed, 176 subtests passed. Every new refusal and
  both amended tests failed, and the six characterization tests passed
  (`verification.md` § 3). The M5 pair failed against a mutant of `main`'s
  validator with the classification comparison removed (`failures=4`) and
  passed against `main`'s own (`verification.md` § 4). Synthetic identifiers
  only.
- [x] 2.3 Schema: the `auth` property of the `deployed` service branch, closed
  as `design.md` D1 gives it, and the `auth` key in the evidence and gap
  concern vocabulary. A deployed synthetic example sits beside the existing
  not-deployed one.
  **Done** in `bcdf2235`: the closed `auth` property of the `deployed` branch,
  the `auth` concern key, and the deployed synthetic example
  `contracts/factory-mcp/examples/declaration-deployed.example.json`
  (`verification.md` § 5).
- [x] 2.4 Validator: the checks and stable codes of `design.md` D7, in the
  semantic pass, with the existing ordering and dimensions.
  **Done** in `3245c0c3`: the D7 checks and stable codes, in the semantic
  pass. After it, `tests/factory-mcp/` reads 108 passed, 300 subtests passed
  (`verification.md` § 5).
- [x] 2.5 Runbook: `docs/factory-mcp-conformance.md` gains the block, its
  codes, the stdio rule, the narrowed M5 reading and the per-domain
  vocabulary statement. The "unbundled and unreleased" paragraph moves to the
  release the cut allocates.
  **Done** in `3335da43`, and the release paragraph moved to `contract-v4.1`
  in the cut commit (`verification.md` §§ 5 and 6).
- [x] 2.6 Contract cut, under `docs/contract-versioning-policy.md` § Bundle
  Realization Order. First claim the version number as row 4 on #630. Then,
  in one candidate commit with the schema, add the declaration's manifest row
  with its digest, the `contracts/CHANGELOG.md` entry and
  `contracts/releases/<version>.digests.yaml`. Run `release-tag-gate`, and
  publish the annotated tag after landing.
  **Done.** Row 4 was claimed on #630 before the cut (comment `6086467830`,
  2026-10-09T18:02:11Z). The candidate `38c78817` was re-cut forward-only as
  `6300772b` after #1284 moved two inventory members, and `release-tag-gate`
  found no error and no warning on the emulated merge tree, only the owed-tag
  notice (`verification.md` § 6). It landed in #1289 as `b27ae7a2`. At that
  merge commit `verify-commit`, `release-tag-gate` and `verify-promotion`
  passed, and the annotated tag `contract-v4.1` (tag object `b30b65be`) was
  published on it on Brett Heap's word *"This lane, after landing
  (Recommended)"* (RULED on the lane register at 2026-10-10T23:30:38Z).
  `verify-tag` passed from a refetched checkout. Record: [#630 comment
  6104587382](https://github.com/opensoft/openxFactory/issues/630#issuecomment-6104587382),
  which also discharged the row-4 claim.
- [x] 2.7 Verification record in the feature: every gate and the full suite at
  the head that lands, and an out-of-tree check by a reviewer with access to
  the engineering domain (`--snapshot`, never vendoring its bytes). That check
  confirms that its hosted declaration reports `hosted_auth_missing` until its
  own slice declares a block (and `auth_rs256_missing` if it declares one that
  lists EdDSA alone), and that its stdio declaration validates as before.
  **Done** (`verification.md` §§ 7 to 11): every gate on the branch and on
  `main` in the same clone kind; `tests/factory-mcp/` at 108 passed, 300
  subtests passed; the full suite under `setsid` (§ 8); and the out-of-tree
  engineering check by `--snapshot` against `codeXfactory/codexFactory` at
  `33b916c1` (§ 9). That check found the not-deployed declaration
  `valid-with-gaps`, the deployed one without a block `hosted_auth_missing`,
  an EdDSA-only block `auth_rs256_missing`, and an RS256-and-EdDSA block
  `valid-with-gaps`, and no codexFactory byte entered this repository. § 11
  records the landing round at each merge of `main`. The full suite at the
  head that lands is CI's required `pytest-suite` at `aed40d2d`, run
  [38102924018](https://github.com/opensoft/openxFactory/actions/runs/38102924018)
  (`selected=11063 passed=11057 skipped=6 failures=0 errors=0`).

## 3. Landing

- [x] 3.1 This packet lands on Brett Heap's landing word, after 0.1, under the
  Rule 6 landing window, with every required check green and Copilot's review
  read at the exact head. **The landing word is given**: 2026-10-08T23:0xZ, in
  session to lane `openXfactory-5`, verbatim *"Land all three, waive Codex
  (Recommended)"*, RULED on the estate's lane register at 2026-10-08T23:00:44Z.
  It WAIVES the Codex review, the connector having answered every trigger with
  a usage-limit notice since about 19:49Z, so no Codex review is required of
  the landing head. The packet stays ACTIVE after it lands: it is not archived
  until it is implemented through Speckit (§ 2 and § 4). Record:
  `review/ratification-2026-10-08.md` § 6.
  **Landed.** [#1274](https://github.com/opensoft/openxFactory/pull/1274)
  merged into `main` by squash at 2026-10-09T01:51:24Z as
  `93d13d6c8e14008c0b66adea65756d106fef6227`, from head `8e56ac58`, on the
  land word above, inside the Rule 6 window (LANDING comment `6072619051`,
  LANDED comment `6072622734`). Of the 17 check runs at `8e56ac58`, 16
  concluded success, `pytest-suite` among them, and Sourcery's was skipped.
  Copilot's review `5464733462` at that exact head reports 0 open findings,
  and all 17 review threads are resolved. This packet directory's tree
  (`999ae78b`) is the same at `8e56ac58`, at `93d13d6c` and at `main`
  `b27ae7a2`, and the delta blob is still the ratified `51fc770d`.
- [x] 3.2 The realization lands on its own word, merged and green.
  **Done.** Brett Heap gave the realization word on 2026-10-10 at 23:2xZ, in
  session to lane `openXfactory-5`, as a multiple-choice answer whose verbatim
  option label is *"Land when green, waive Codex (Recommended)"*. It is RULED
  on the lane register at 2026-10-10T23:30:24Z, and it waives Codex: the one
  trigger, on #1289 at 2026-10-09T21:34:58Z, drew the usage-limit notice. Pull
  request [#1289](https://github.com/opensoft/openxFactory/pull/1289) merged
  into `main` by merge commit at 2026-10-11T02:17:36Z as
  `b27ae7a25705e52147f59e05f30a17533d7af367` (parents `main` `978e9cbc` and
  head `aed40d2d`), between LANDING comment `6104542950` and LANDED comment
  `6104545275`. Of the 17 check runs at `aed40d2d`, 16 concluded success and
  Sourcery's was skipped. Copilot's review `5481531243` at that exact head
  reports 0 open findings, and its one review thread is resolved.
  `pytest-suite` also ran green on `main` at `b27ae7a2` itself, on push, run
  [38104679302](https://github.com/opensoft/openxFactory/actions/runs/38104679302),
  with the same counts line as at the head.

## 4. Archive

- [x] 4.1 After merged, green realization evidence exists (the code surface is
  not empty), and on its own word: archive with `python3
  scripts/proposal-support.py . archive amend-factory-mcp-conformance-auth-profile`
  (never a bare `openspec archive`), landed by merge commit and never by
  squash. Before the archive command, resolve this packet's
  `target_release: deferred-allocation`: replace it in `proposal.md` with the
  literal contract release the cut allocated (or `implemented` if no bundle
  was cut), in a pull request that names the bundle version it observed and
  the release surface carrying it. A change whose declaration is still
  deferred MUST NOT archive (`release-realization`, scenarios *A change tries
  to archive while its target release is deferred* and *The resolving pull
  request swaps the token and cites nothing*, ratified by
  `add-target-release-deferred-allocation`). Retire this packet's
  `_LEDGER_SUBJECTS` row, and move the README entry to the archive record.
  Canon then holds twelve requirements.
  **Ticked before the run, because the archive wrapper refuses an open box**
  (`change has incomplete tasks` while any `- [ ]` line remains). The
  conditions this item names are met: merged, green realization evidence
  exists (2.1 to 2.7 and 3.2), and the archive has its own word.
  - **The word.** Brett Heap gave it on 2026-10-11 at 15:5xZ, in session to
    lane `openXfactory-5`, as a multiple-choice answer whose verbatim option
    label is *"Archive, land when green (Recommended)"*. The option read: *"a
    seat writes the openxFactory archive PR, which lands by merge commit under
    Rule 6 once CI is green and Copilot has reviewed the head, Codex waived as
    for #1289."* It is RULED on the lane register (`opensoft/brett-wip`
    `lanes/log/openXfactory-5.md`) at 2026-10-11T16:03:19Z, commit `d74bd6f2`,
    against this change path. No GitHub comment carries the word; the register
    entry and this citation are its record.
  - **The release.** `contract-v4.1`. The annotated tag `contract-v4.1` (tag
    object `b30b65bed6991e05dadb7eaab7d56903ed567757`) dereferences to
    `b27ae7a25705e52147f59e05f30a17533d7af367`, #1289's merge commit, which is
    the cut (2.6 and 3.2).
  - **`target_release` resolved before the archive command**, in this
    archive's own pull request and in its own commit, `cea58658`: the token
    `deferred-allocation` became the literal `contract-v4.1`. The new
    declaration names the bundle version it observed and the release surface
    carrying it: `contracts/manifest.yaml`,
    `contracts/releases/contract-v4.1.digests.yaml` and
    `contracts/CHANGELOG.md`.
  - The wrapper's run, the promotion measured by content, the retirement of
    the `_LEDGER_SUBJECTS` row and the README record are recorded under this
    item in the commit after the move.

## 5. Downstream acts this change does NOT perform

- [~] 5.1 **codexFactory's RS256 slice**, lane `openXfactory-5`, as its own
  governed change in that repository. Two notes ride to it from `design.md`.
  The audience binding: its adapter compares `aud` with its canonical resource
  URI, while the estate issuer's tokens carry a client identifier (D3). The
  metadata location: it appends the well-known suffix to the resource URI (D4).
- [~] 5.2 **OpsxFactory's hosting-plan `issuer` correction**: a material
  amendment of the approved hosting plan, with a fresh task 4.2 approval. This
  change supplies the issuer rule that correction meets (`design.md` D4).
- [~] 5.3 **The Ops gateway's intake alignment**, lane `opsXfactory-4`, at
  gateway base task 3.1.
- [~] 5.4 **No shared transport package, server, token minting or client
  registration.** The shared-transport trigger is untouched.
