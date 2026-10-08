# Tasks: correct-naming-families-count

Status: ratified
Ratified by: correct-naming-families-count — 2026-10-07, Brett Heap, "ratify as recommended when the PR opens" (logged RULED on the lane register at 2026-10-07T09:47:04Z), over PR #1266's opening head `3bb38c20` (record `review/ratification-2026-10-07.md`)
Kind: tasks

`code_surface: none`, `target_release: implemented`. Under
`release-realization` this packet therefore archives on LANDING plus this task
list, not on merged-plus-green realization evidence. **The doctrine edit is IN
this list (§ 5.1), so "archives on landing plus its task list" still means the
doctrine edit has to have been merged.** § 1 is the owner's acts, §§ 2-4 are
what this packet itself authored and measured, § 5 is the one realization
handoff, and § 6 is the archive.

## 1. Ratification — 1.1 and 1.2 are OWNER BOXES, and an agent never ticks them

Each is ticked only on Brett Heap's own recorded word, by whoever encodes that
word, citing it. 1.3 is the bookkeeping that follows the ratifying word and
never precedes it.

- [ ] 1.1 OWNER BOX. Brett Heap's word on the reading this packet encodes: the
  naming families are COUNT-FREE in canon (`design.md` D1); the correction also
  reaches the two further sentences that restate a property of the whole set
  (D2); and the doctrine is realized in the wording D3 proposes, with one
  informative note dated to the pin. His sentence of 2026-10-07, *"open an
  OpenSpec change for the four families heading"*, is the authority to author
  and open this packet. It is not this word.
  **NOTE 2026-10-07 — THE WORD WAS GIVEN:** Brett Heap, in session, verbatim
  *"ratify as recommended when the PR opens"*, logged RULED on the lane
  register at 2026-10-07T09:47:04Z and effective when PR #1266 opened at
  2026-10-07T10:43:48Z (record `review/ratification-2026-10-07.md`). It
  ratifies D1, D2 and D3 as written. The box is left for its owner to tick, as
  this section's heading says.
- [ ] 1.2 OWNER BOX. Brett Heap's merge word on this pull request. It is held
  for that word and is not merged by the authoring lane.
  **NOTE 2026-10-07 — THE WORD WAS GIVEN, SEPARATELY:** Brett Heap, in session,
  verbatim *"merge the naming families PR when green"*, logged RULED on the
  lane register at 2026-10-07T09:59:10Z. The merge is the coordinating lane's
  act, once every required check on the final head is green; the authoring
  lane does not merge. The box is left for its owner.
- [x] 1.3 On the ratifying word, and only then: `Status: ratified` + `Ratified:`
  in `proposal.md`, `Ratified by:` in `design.md` and this file, the
  `approved_by`/`approved_on` pair in `.openspec.yaml` ADDED BESIDE the drafting
  provenance and never substituted for it (`scripts/doc_health/proposal_origin.py`
  requires the pair the moment the status claims approval), a record under
  `review/`, and the README Records row moved with it.
  **DONE 2026-10-07 in the ratifying commit**, on the word above: all of it,
  with the record at `review/ratification-2026-10-07.md`. `kind`, `id`,
  `reason`, `proposed_by` and `proposed_on` did not move, and the spec delta
  did not move.

## 2. The packet

- [x] 2.1 `specs/project-repo-schema/spec.md`: TWO `## MODIFIED` requirements,
  titles unchanged, each built by script from canon. *The naming families are
  governed by the pinned standard, and a descendant form is a claim that needs
  a declared pin*: the count-free first sentence, one added paragraph, the
  corrected referent sentence, two `Removed from canon` markers, all three
  promoted scenarios carried, and one scenario added. *A project's repositories
  are named `<Project>`, `<Project>-spec` and `<Project>-code`*: the corrected
  CamelCase clause, one `Removed from canon` marker, and all three promoted
  scenarios carried. Seven scenarios in the file.
- [x] 2.2 `.openspec.yaml`: `kind: ad_hoc`, id
  `openxFactory:adhoc:2026-10-07-correct-naming-families-count`, the unapproved
  shape `add-drafted-proposal-origin` admits (`proposed_by`/`proposed_on`, no
  approval pair), Brett Heap's sentence verbatim with its register time,
  session `ed23f049-7e99-4601-8a6d-760b6aeb5f26`, lane `codeXfactory-5`.
  Written by hand in the block shape `scripts/proposal-support.py
  declare-adhoc` writes, because that command derives the id's repository
  segment from the checkout directory's name and this packet was authored in a
  worktree whose directory is not named `openxFactory`.
- [x] 2.3 README *Active changes*: one bullet.
- [x] 2.4 The per-change sweep ledger row, seeded by the sanctioned seeder
  (`scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#1266'`,
  this pull request): `active`, `co-modifier`, `declares: absent`. Exactly one
  row moved, this packet's own. It is `co-modifier` because both requirement
  keys it writes were also written by the archived `add-project-repo-schema`,
  whose row was already `co-modifier` and does not move.

## 3. Measurement — each re-runnable, each taken on `main` `16779816`

- [x] 3.1 CARRIAGE, two ways. By line range, with `D` the delta and `C`
  `openspec/specs/project-repo-schema/spec.md`, each of these prints nothing:
  `diff <(sed -n 28,34p D) <(sed -n 77,83p C)`, `diff <(sed -n 47,58p D)
  <(sed -n 94,105p C)`, `diff <(sed -n 60,60p D) <(sed -n 107,107p C)`,
  `diff <(sed -n 65,72p D) <(sed -n 111,118p C)`, `diff <(sed -n 84,86p D)
  <(sed -n 120,122p C)`, `diff <(sed -n 91,92p D) <(sed -n 127,128p C)` and
  `diff <(sed -n 96,108p D) <(sed -n 130,142p C)`. By unit, through
  `scripts/doc_health/modified_block_currency.py`'s own `derive_units` and
  `carried` over canon's block and the delta's: the first block leaves exactly
  ONE canon unit uncarried and the second exactly TWO, each named by a
  `Removed from canon` marker; no marker names a unit the block still carries;
  and no span a marker's reason quotes matches a canon unit. The reflowed
  paragraph's second sentence (*"A name matching no family at all is REFUSED
  …"*) is carried as a unit.
- [x] 3.2 The families, read with `git show <sha>:contracts/repository-naming.yaml`
  in openRepoShape at each pin openxFactory has held (`design.md` D1, D4):
  `deacbdc` four, `122d729b` five, `e9c4827b` five, `1a9fc537` six, each header
  saying the same number. The file is byte-identical at `3a927a2` and
  `1a9fc537` (`git diff --stat` empty), and its sha256 at `1a9fc537`,
  `a4eebad21541cbfe9a3e94a0ee667a2d5a7866c3567eea2a000d8339f6f096a4`, is the
  digest `contracts/openreposhape-pin.yaml` records.
- [x] 3.3 `git grep -n -i "four .*famil"` on `main` `16779816` (before this
  packet, whose own files quote the phrase): **146 hits, every one classified.**
  - **In scope, 3:** `openspec/specs/project-repo-schema/spec.md:108` (this
    packet's MODIFIED block); `docs/project-repo-schema.md:236` and `:248`
    (§ 5.1).
  - **Historical, 4, left as written** (`design.md` D7): `README.md:7510`,
    `contracts/CHANGELOG.md:2002`, `ideation/README.md:392`, and
    `openspec/changes/archive/2026-09-03-add-project-repo-schema/specs/project-repo-schema/spec.md:97`.
  - **Unrelated, 139.** Each names doc-health check families (the four
    lifecycle families that read the scan set, the "ruled" families,
    generator families), contract or schema families, O*NET occupational
    families, or carries "four" and "famil…" in separate clauses of one long
    line. `contracts/policies/standards-bodies.yaml:1195`, *"the four family
    listings are named here instead"*, is the O*NET case: SOC families 11, 13,
    15 and 27 for the marketing body, not naming families. The rest, by file:
    `README.md` :8978,9965,10132; `contracts/CHANGELOG.md` :2310;
    `contracts/README.md` :50,126; `contracts/review-lane-floor-snapshot.yaml`
    :51; `contracts/signed-execution-chain/README.md` :109;
    `docs/archive-record-discrepancies.md` :1340,1418,1557; `docs/doc-health.md`
    :48,49,50,51; `docs/opendox-carve-manifest.yaml` :2508,2577,2809;
    `ideation/staging/INDEX.md` :91;
    `ideation/staging/doc-health-direction-arc/doc-health-direction-arc.md` :197;
    `openspec/changes/add-chain-attestation/proposal.md` :3;
    `openspec/changes/add-per-tenant-app-manifest-provisioning/proposal.md` :2;
    `openspec/changes/add-requirement-ref-resolution-integrity/proposal.md` :2;
    `openspec/changes/create-ledgerxwallet-overlay-boundary/council-adversary-engineer.md`
    :941; `openspec/changes/settle-aging-staging-topics/proposal.md` :2;
    `openspec/specs/doc-health/spec.md` :987;
    `openspec/specs/document-lifecycle/spec.md` :1086;
    `scripts/doc_health/corpus.py` :21; `scripts/doc_health/families.py` :682;
    `scripts/doc_health/modified_block_currency.py` :1100;
    `scripts/doc_health/pin_class.py` :2550;
    `scripts/doc_health/promotion_fidelity.py` :8; under
    `openspec/changes/archive/`: `2026-07-14-add-document-cataloging/tasks.md`
    :57, `2026-08-02-add-workbench-integrated-editor-chat/tasks.md` :664,
    `2026-08-06-add-cross-factory-ideation-routing/tasks.md` :12,
    `2026-08-21-align-status-reader-to-real-lines/proposal.md` :5,
    `2026-08-22-add-doxbench-editing-phase-b/proposal.md` :4,
    `2026-08-22-add-roster-device-admission-surface/tasks.md` :364,
    `2026-08-22-sanction-ratified-record-spelling/tasks.md` :309,
    `2026-08-24-govern-openspec-corpus-membership/` (`design.md`
    :14,45,47,112,136; `proposal.md` :2,157,212,349;
    `specs/doc-health/spec.md` :122; `tasks.md`
    :31,59,81,149,173,227,293,323,335,385,591,712,726,880,939,1023,1462,1475,1722,1835,2252,2386),
    `2026-08-25-add-duplicate-packet-check/` (`proposal.md` :41,84; `tasks.md`
    :177), `2026-08-25-add-promotion-fidelity-check/specs/document-lifecycle/spec.md`
    :14, `2026-08-25-add-release-inventory-drift-check/proposal.md` :2,
    `2026-08-27-add-family-enumeration-check/` (`proposal.md` :94; `tasks.md`
    :276), `2026-08-27-govern-derived-pin-reachability/tasks.md` :22,127,605,
    `2026-08-27-supersede-lost-pin-baseline/proposal.md` :2,
    `2026-08-28-add-unclassified-finding-class/proposal.md` :2,
    `2026-08-28-declare-sentinel-pin-vocabulary/tasks.md` :719,
    `2026-08-29-clean-doc-health-floor/` (`proposal.md` :96; `tasks.md` :124),
    `2026-08-29-fix-pin-value-boundary-and-sentinel-split/proposal.md` :2,
    `2026-08-31-add-signed-execution-chain/realization-evidence.md` :393,
    `2026-09-02-govern-sibling-added-modified-deltas/proposal.md` :2,
    `2026-09-03-add-project-repo-schema/proposal.md` :3 (*"four cross-field
    rules"*, not families), `2026-09-04-add-drafted-proposal-origin/tasks.md`
    :277, `2026-09-04-add-subject-establishment/proposal.md` :3,
    `2026-09-05-add-release-tag-gate/proposal.md` :2,
    `2026-09-06-amend-marker-reason-boundary/review/verification-2026-09-06.md`
    :153, `2026-09-09-amend-marker-defect-reporting/review/verification-2026-09-09.md`
    :167, `2026-09-10-amend-marker-declaring-nothing/review/verification-2026-09-10.md`
    :216, `2026-09-10-amend-neutral-product-pin-lockfile-first-line/proposal.md`
    :2, `2026-09-11-amend-merged-into-empty-tail-standing/proposal.md` :2,
    `2026-09-11-honour-grandfather-dispositions-in-ratified-provenance/`
    (`specs/doc-health/spec.md` :54; `tasks.md` :234),
    `2026-09-11-state-header-window-budget/review/ratification-2026-09-11.md`
    :288, `2026-09-12-decide-disposition-reading-per-family/design.md` :332,
    `2026-09-12-report-stale-grandfather-dispositions/` (`proposal.md` :2;
    `specs/doc-health/spec.md` :54),
    `2026-09-15-extend-prose-tagging-target-to-pinned-capabilities/.openspec.yaml`
    :15, `2026-09-16-retire-doxbench-chat-turn-v1/proposal.md` :2,
    `2026-09-23-add-estate-repository-inventory/.openspec.yaml` :7; under
    `specs/`: `019-modified-block-currency-family/` (`contracts/family-entrypoint.md`
    :270; `research.md` :430,474; `tasks.md` :229,230),
    `020-modified-block-currency-fixtures/data-model.md` :36,
    `021-modified-block-currency-self-gate/` (`contracts/self-gate-contract.md`
    :67; `spec.md` :184; `tasks.md` :251),
    `022-modified-block-currency-reporting/` (`evidence/f4-gates.md` :275;
    `pr-body.md` :60; `research.md` :59), `026-unplaced-finding-drift/`
    (`evidence/ci-shape.md` :33; `tasks.md` :194),
    `032-govern-archived-record-edits/checklists/evidence-and-traceability.md`
    :25, `034-opendox-standalone-operation/` (`clarify-questions.md` :981;
    `tasks.md` :1078); under `tests/`:
    `doc-health/fixtures/lifecycle-historical/openxFactory/openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md`
    :4, `doc-health/fixtures/lifecycle-scan/openxFactory/openspec/changes/alpha-uncited-ratified/review/finding-2026-01-04.md`
    :9, `doc-health/test_lifecycle_scan_set.py` :13,46,310,331,440,483,
    `doc-health/test_modified_block_currency_reporting.py` :870,936,1129,
    `doc-health/test_modified_block_currency_self_gate.py` :866,1731, and
    `ideation-dashboard/test_doxbench_contracts.py` :1281.
- [x] 3.4 Ordering: the only active change with a delta on
  `project-repo-schema` is `prefer-triad-project-shape`
  (`ls -d openspec/changes/*/specs/project-repo-schema`). Its four titles and
  this packet's two are disjoint (`design.md` D5), so no `sequenced_after:` is
  owed.
- [x] 3.5 No mechanical reader and no link: the evidence in `proposal.md`'s
  `code_surface:` gloss, items (1) to (4). `git grep -n -i "naming-and-the"` is
  empty here and on `origin/main` of openRepoShape, codexFactory and the
  xFactory aggregation.
- [x] 3.6 `ideation/staging/` searched for `naming famil`, `repository-naming`,
  `four famil` and `openreposhape`: two files match (`INDEX.md`,
  `opendox-two-layer-product/`) and neither proposes this correction, so the
  origin is `ad_hoc`.

## 4. Gate

- [x] 4.1 Pinned OpenSpec CLI (`@fission-ai/openspec@1.12.0`, content address
  verified), from the worktree root. `python3 scripts/validate-openspec-cli-pin.py
  --change correct-naming-families-count --strict`: **1 passed, 0 failed**,
  exit 0. `--all --strict`: **113 passed, 1 failed (114 items), exit 0**,
  against clean `main` `16779816` at **112 passed, 1 failed (113 items), exit
  0**. Every finding line is identical on the two trees. The one failure is
  not this packet's: `add-chain-attestation`'s MODIFIED block, an ACCEPTED
  EXCEPTION that `contracts/openspec-cli-pin.yaml` `dispositions:` already
  carries.
- [x] 4.2 Each exits 0: `scripts/validate-code-surface.py .`,
  `scripts/validate-target-release.py .` (47 active proposals, 47 declaring),
  `scripts/validate-sequenced-after.py .` (47 active changes), the same with
  `--ledger-diff` ("consistent with the corpus (233 rows)"), and
  `scripts/proposal-support.py . verify correct-naming-families-count`
  ("proposal support verification ok"). `scripts/doc-health.py --single-repo .
  --as-of 2026-10-07` was run in a scratch checkout NAMED `openxFactory` with
  the submodules CI's `pytest-suite` initializes (`openXwallet`, `openXdox`,
  `openDox`, recursively), first at `main` `16779816` and then with this
  packet's files laid over it. Both report **31 critical, 26 error, 69
  warning, 19 info**, and the two reports are byte-identical. No finding names
  any file of this packet or its README bullet, in any family
  (`proposal-origin`, `modified-block-currency`, `status-validity` and
  `ratified-provenance` among them).
- [x] 4.3 pytest, `-m "not postgres"`, over every directory that reads the
  change corpus, the README, the ledger or the pins (`sequenced_after`,
  `code_surface`, `target_release`, `scope_globs`, `proposal-support`,
  `packet_reference`, `citation_remainder`, `former_id_arrival`,
  `estate_inventory`, `openspec_cli_pin`, `openreposhape_pin`,
  `intent-compliance`, `conformance-gate`, `pin_registrations`, `doc-health`),
  in the same `openxFactory`-named scratch checkout with this packet laid over
  `main`: **3872 passed, 2 skipped, 0 failed, exit 0**. In the authoring
  worktree, whose directory is not named `openxFactory` and which has no
  submodules initialized, a run over the same directories less
  `citation_remainder`, `intent-compliance`, `conformance-gate` and
  `pin_registrations` fails the same seven `doc-health` tests on clean `main`
  and on this tree alike (3327 passed and 7 failed on each). Every one
  of the seven is a checkout-name or submodule test (`test_ideation_readiness`
  three times, `test_readiness_dispatch`, `test_sentinel_vocabulary` twice,
  `test_status_reader_real_lines`), and all seven pass in the scratch
  checkout. The full suite is CI's `pytest-suite`.
- [ ] 4.4 Required checks green at the pull request's head. No review is
  requested by the authoring lane: no Copilot review by any route (Brett Heap,
  2026-10-06), and no other review request. Any thread a reviewer opens is
  answered.

**§§ 1, 4.4, 5 and 6 KEEP A LITERAL `- [ ]` DELIBERATELY.** They are acts that
have not happened, and each is ticked by the act that performs it, never by the
authoring lane.

## 5. Realization handoff — NOT performed by this packet

- [x] 5.1 **openxFactory, the doctrine.** After ratification, in its own pull
  request: `docs/project-repo-schema.md` restated as `design.md` D3 proposes.
  The heading at `:236` becomes `## Naming, and the naming families`. The
  sentence at `:240-242` says the suffixes sit apart from *"every family the
  pinned standard's naming policy spells as a CamelCase word"*. The sentence at
  `:248-251` becomes count-free, keeping the four forms it names as members.
  One INFORMATIVE note dated to the pin lists the families the pin in force
  declares and says it governs nothing. The header gains an `Amended by:
  correct-naming-families-count (ratified <date>, openxFactory PR #<n>)` line
  beside the existing one. No other sentence moves: the realization's
  `git diff` names exactly those hunks, and any other hunk is a finding against
  the edit. `docs/project-repo-schema.md` is not a registered release member,
  so no digest, inventory member or changelog entry moves. The pull request
  touches `openspec/changes/` only to tick this box, under its own Rule 6
  window.
  **DONE 2026-10-08** in openxFactory PR
  [#1270](https://github.com/opensoft/openxFactory/pull/1270) →
  `615c79c4c6c592e7a12bb8e68b639e9198ac545c`, lane `codeXfactory-5`, on Brett
  Heap's in-session word of 2026-10-08, verbatim *"do the 5.1 doctrine edit for
  naming families"*. `docs/project-repo-schema.md` gains the header line
  `Amended by: correct-naming-families-count (ratified 2026-10-07, openxFactory
  PR #1266)`; its heading becomes `## Naming, and the naming families`; the
  leg-suffix sentence says the suffixes sit apart from every family the pinned
  standard's naming policy spells as a CamelCase word; the sentence that said
  the four families are governed as DATA is count-free and keeps the four forms
  as members; and one INFORMATIVE note dated 2026-10-07 to the pin
  `1a9fc537bcce…` lists the six families that pin declares and says it governs
  nothing. The wording is `design.md` D3's, verbatim. `git diff` names those
  five places, in four git hunks because the last two are adjacent, and no
  other sentence moves: the one re-wrapped line pair keeps its words. The file
  is not a registered release member, so no digest, inventory member or
  changelog entry moves. The tick holds on `main` only through that pull
  request's merge, which waits on Brett Heap's merge word and its required
  checks.

## 6. Archive

- [ ] 6.1 Archive only after § 5.1 is merged, through the pinned CLI
  entrypoint, promoting both MODIFIED requirements into
  `openspec/specs/project-repo-schema/spec.md`, with the README OpenSpec
  Records row moved from Active to Archived. The order against
  `prefer-triad-project-shape` is free (`design.md` D5). Before archiving,
  re-read canon for both titles: if canon moved under either block, the block
  is brought forward first, as `document-lifecycle`'s currency requirement
  requires.
- [ ] 6.2 Re-run the pinned CLI (`--all --strict`), `scripts/validate-sequenced-after.py .`
  with `--ledger-diff`, and `scripts/doc-health.py --single-repo .` on the
  archived tree, and compare each with the pre-archive run.
