# Tasks: add-estate-repository-inventory

Status: ratified
Ratified by: Brett Heap, 2026-09-18, approximately 12:55Z — verbatim
"ratify #1101", given in the lane's terminal (no GitHub comment carries it;
RULED entry against `opensoft/openxFactory#1101` in
`lanes/log/openXfactory-5.md`)

Lane: openxfactory-5 (openXfactory-5)
For: openxFactory [#1087](https://github.com/opensoft/openxFactory/issues/1087)

**WHAT IS OPEN AND WHAT IS CLOSED.** § 2 is CLOSED and was done in this pull
request. **§ 1 IS NOW CLOSED TOO, by Brett Heap's word of 2026-09-18 and by no
lane's decision.** §§ 3, 4, 5 and 6 stay OPEN. § 3 is a LATER pull request,
which that word authorizes to be authored. § 5 is a SEPARATE act on a SEPARATE
word.

## 1. Ratification — GIVEN 2026-09-18, Brett Heap's and nobody else's

- [x] 1.1 **(OPERATOR)** Ratify or refuse `proposal.md` § *The decision, put for a
      veto*, which puts FOUR decisions with the recommendation first: **D2** where
      the inventory lives (`scripts/` beside the register, `target_release:
      implemented`; against `contracts/policies/`, which owes an additive minor
      per correction against a fact that moves every four days; against no file
      at all); **D3** one `## MODIFIED` block over the promoted grammar
      requirement (against ADDED-only, which leaves a contradiction standing);
      **D4** the authority question: FIVE admission-evidence kinds (`gitlink`,
      `pin`, `workflow`, `root`, `change`, with `gitlink` reaching ANY governed
      estate repository's `.gitmodules` and its evidence naming the carrier) and
      three governance classes, the inventory RECORDING an admission and
      PERFORMING none (against a flat membership list); **D5** a former address in
      an active head REPORTS rather than refuses. A BARE RATIFYING WORD takes the
      packet as encoded, which is the recommendation in all four.
      **RULED AS ENCODED — Brett Heap, 2026-09-18, approximately 12:55Z,
      verbatim "ratify #1101"**, given in the lane's terminal to lane
      `openxfactory-5` (session `651195c7`); no GitHub comment carries the
      word, and the lane recorded it as a RULED entry against
      `opensoft/openxFactory#1101` in `lanes/log/openXfactory-5.md`. **THE WORD
      IS BARE AND NAMES NO ALTERNATIVE**, so D2, D3, D4 and D5 each take the
      recommended option above, which is what this task's own last sentence
      says a bare word does. **THE WORD TOOK THE OPTION THIS PACKET HAD ALREADY
      ENCODED, SO THE DELTA'S WORDING STANDS UNCHANGED**: not one byte of
      `specs/release-realization/spec.md` moved by this ratification.
      **DONE** in this same commit: `proposal.md`, `design.md` and this file
      take `Status: ratified` with a citation line each, and `.openspec.yaml`
      gains `approved_by`/`approved_on` ADDED BESIDE the unmoved
      `proposed_by`/`proposed_on` (`git diff --numstat` on that file = `50 0`,
      additions only).
- [x] 1.2 **(OPERATOR)** The ratifying word authorizes the REALIZATION (§ 3) to be
      authored as a later pull request. It does not authorize the archive, which
      § 5 governs and which owes its own word on merged-plus-green evidence.
      **SATISFIED BY THE WORD ITSELF.** "ratify #1101" reaches exactly § 3 (may
      now be authored, as a later pull request) and not § 5, which stays closed
      behind merged-plus-green realization evidence and its own word. No merge
      word is quoted here either: the verbatim word is "ratify #1101" and
      nothing further, and the merge of this pull request is a separate act
      performed by whoever holds it, never by this lane alone.
- [x] 1.3 **(OPERATOR)** If D2 is vetoed to `contracts/policies/`, `target_release:`
      moves with it to "next additive contract bundle (allocated at realization)"
      and § 3.1 gains the `contracts/manifest.yaml` entry with a recomputed
      `sha256`. Nothing else in the packet changes, and `design.md` D2 states it
      so the veto is takeable without a re-author.
      **NOT TRIGGERED.** D2 was not vetoed: the word is bare and takes the
      recommended option, so `target_release:` stays `implemented`, the
      inventory stays at `scripts/estate-repository-inventory.yaml`, and § 3.1
      gains no `contracts/manifest.yaml` entry. Nothing in the packet moved
      under this clause.
- [x] 1.4 **(OPERATOR — NOT A FIFTH DECISION, A DISCLOSURE.)** Two things moved
      after the first filing, at the review of PR #1101, and a ratifying word
      takes them with the rest: `gitlink` was WIDENED from the aggregation's
      `.gitmodules` to any governed estate repository's, without which the
      `change` kind's provisional row could never be discharged (`design.md`
      D1.1), which re-measured the candidate from 27 rows to **33**; and the
      reverse arm's evidence re-check was BOUNDED to the four in-tree kinds, with
      `gitlink` re-checked only against a working tree supplied as a path and
      otherwise reported as NOT RE-CHECKED (`design.md` D1.2), without which the
      validator could not be both deterministic and network-free as § 3.2 says it
      is. Neither is put separately for a veto; both are recorded here so the word
      is given over what the packet now says.
      **TAKEN WITH THE REST.** The word of 2026-09-18 was given over the packet
      AS IT NOW STANDS, both disclosures inside it, and named neither
      separately — which is the outcome this task was written to produce, not a
      fifth decision taken by silence.

## 2. Measurement (CLOSED in this pull request)

- [x] 2.1 The FIVE naming sites enumerated with the commands recorded at
      `design.md` D0.1: the aggregation's `.gitmodules` via
      `gh api repos/opensoft/xFactory/contents/.gitmodules` (23 submodules), this
      repository's `contracts/*-pin.yaml` (7 pins, 6 distinct repositories, 2 of
      them no submodule), `.github/workflows/` (1, already a submodule), the
      aggregation root itself (1, which no `.gitmodules` can carry), and a
      GOVERNED DomainxFactory's own `.gitmodules` where the estate nested rather
      than sibling-linked (11 nested gitlinks in 6 repositories, naming 7 no
      other site names). The first four were taken on `origin/main` `ad089e8a`;
      **the fifth was taken on 2026-09-18 at the review of PR #1101**, which is
      where the kind was widened, and `design.md` D0.1 records why rather than
      presenting five sites as if four had never been claimed.
- [x] 2.2 **THE CANDIDATE INVENTORY BUILT AND PUT IN `design.md` D0.2**, 33 rows,
      each with its `<owner>/<name>`, its role in the layer model, its governance
      class and its admission evidence. The last six (`openChart`,
      `openPractice`, `MedxAvatar`, `LedgerxAvatar`, `MedxEHR-spec`,
      `MedxEHR-code`) are the members the fifth site added; the governance class
      of those six is stated only as far as the openxFactory sites measure it and
      is re-measured at § 4.3.
- [x] 2.3 The declared population measured through the SHIPPED reader
      (`scripts/code_surface.py` `declaration` then `parse_head`) and never by a
      private scan: 49 active proposals, 49 declaring, 7 `none`, 8 named by the
      closed register, 34 a readable repository list, and those 34 heads naming
      **SIX** distinct identifiers.
- [x] 2.4 **EVERY ONE OF THE SIX CHECKED AGAINST THE CANDIDATE**, `design.md`
      D0.3: all six resolve, so the membership arm refuses NOTHING on the day it
      lands. This is the measurement that falsifies the predecessor's stated
      fatal cost for membership resolution.
- [x] 2.5 **THE FIFTH ADMISSION KIND MEASURED INTO EXISTENCE, NOT DESIGNED IN,
      AND ITS DISCHARGE MEASURED TOO.** `opensoft/LedgerxWallet` is named by no
      AGGREGATION gitlink, no openxFactory pin and no openxFactory workflow; it
      was declared by the RATIFIED `create-ledgerxwallet-overlay-boundary` on
      2026-08-27, one day before that realization created and nested it.
      `design.md` D1.1 records the case, the PROVISIONAL row it forced, and —
      added at the review of PR #1101 — the DISCHARGE the first filing lacked:
      `ledgerXfactory/LedgerxFactory`'s `.gitmodules` has carried
      `[submodule "LedgerxWallet"]` since 2026-08-28 (that packet's § 5.1,
      LedgerxFactory PR #31, commit `2c96b0b`), verified live on 2026-09-18. A
      `gitlink` read as the aggregation's alone would have left the row expiring
      into a finding no kind could close.
- [x] 2.6 **THE DEFECT MEASURED AS STANDING, not asserted** (`design.md` D0.5):
      `contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml` names
      `opensoft/LegalxFactory`, a provider 404 carried by no gitlink and no pin,
      and two more addresses that live only through a provider redirect, while
      `contracts/policies/repository-identity.yaml` carries ONE transfer row.
- [x] 2.7 The churn rate measured (`design.md` D0.6): 19 commits to the
      aggregation's `.gitmodules` between 2026-07-01 and 2026-09-12, nineteen of
      nineteen moving an inventory row. This is what decides D2 and it is a
      measurement rather than the register header's assertion.
- [x] 2.8 **DELTA KIND DECIDED AGAINST THE PROMOTED TEXT AND NOT BY HABIT**
      (`design.md` D3): the promoted `SHALL NOT judge its MEMBERSHIP` is
      unconditional, so ADDED-only would leave canon self-contradictory. ONE
      `## MODIFIED` block, restating canon verbatim but for the one paragraph
      whose own stated reason this packet removes.
- [x] 2.9 **THE MODIFIED-BLOCK SELF-GATE CHECKED, NOT ASSUMED, AND THE DELETION
      DECLARED.** No active change writes `(release-realization, code-surface
      declaration grammar is gated)`, so this block is SOLE and no
      `sequenced_after:` is owed on it. The three superseded sentences are named
      as code spans in a reserved `Removed from canon by` marker carried inside
      the block, in the form the promoted marker-hygiene family defines; without
      it the `modified-block-currency` arm reported three findings against this
      block, and with it the whole checker reports the SAME total at this head and
      at a clean `origin/main` checkout in the same clone, ZERO NEW and ZERO GONE —
      RE-MEASURED 2026-09-18 at this branch's `b3bf9cf5` and `origin/main`
      `dc242f3a`: 92 findings at both (31 critical, 11 error, 28 warning, 22 info),
      superseding the stale 97 this line previously stated.
- [x] 2.10 Sibling search taken before the claim was written (`design.md` D6):
      no active or archived change enumerates the estate's repositories, and the
      change id collides with nothing under `openspec/changes/` or its archive.
- [x] 2.11 README "OpenSpec Records → Active changes" bullet added.
- [x] 2.12 Per-change sweep-ledger row seeded from the live corpus through the
      sanctioned command, never hand-written:
      `python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#<PR>'`,
      the diff read as the list of rows this change moved.
- [x] 2.13 Gate transcripts recorded in the pull request body.

## 3. Realization (OPEN; a LATER pull request on the ratifying word)

**NOT ONE BYTE OF § 3 MOVES IN THIS PULL REQUEST.** Each slice states the
FAILS-THEN-PASSES obligation: every test is written to FAIL against the tree
without its arm, and is shown failing before it is shown passing.

- [ ] 3.1 `scripts/estate-repository-inventory.yaml` (NEW): the 33 candidate rows
      of `design.md` D0.2, `schema_version` and `kind` at the head (CLAUDE.md
      rule 4), a header stating why the file is not under `contracts/` and what a
      row means, and per row `repository:`, `name:`, `role:`, `governance:`,
      `admitted_by:` (one or more of the five kinds with its site, and for a
      `gitlink` THE REPOSITORY THAT CARRIES IT, which is the aggregation for 23
      rows and a governed DomainxFactory for 7) and, for a `change`-admitted row,
      `provisional: true` with the change id.
- [ ] 3.2 `scripts/estate_inventory.py` (NEW): the reader and the row-level judge,
      in the shape `scripts/code_surface.py` uses: read through the shipped
      strict loader, no second parser, no path reached through a symlink at leaf
      or ancestor, deterministic, no network. Public: load the inventory, resolve
      an identifier (address, bare name, or former address through
      `contracts/policies/repository-identity.yaml`), and report the row-level
      findings § 3.4 gates. **IT RE-CHECKS THE FOUR IN-TREE KINDS ONLY** (`pin`
      under `contracts/`, `workflow` under `.github/workflows/`, `change` under
      `openspec/changes/`, `root` a constant naming no file), which is what makes
      "deterministic, no network" a statement it can keep; `gitlink` evidence
      lives in another repository's tree and is § 3.3's separately invoked mode
      (`design.md` D1.2).
- [ ] 3.3 `scripts/validate-estate-inventory.py` (NEW): the house validator CLI in
      the shape every other `scripts/validate-*.py` uses. The DEFAULT run judges
      the inventory file's SHAPE and its in-tree evidence and makes no network
      call: refuses a duplicate bare name, a row whose in-tree `admitted_by:`
      evidence names nothing, and a still-provisional row whose change has
      archived; REPORTS a row at a FORMER address, naming the current address the
      transfer map resolves (`design.md` D5: RECOMMENDED REPORT, ALTERNATIVE
      refuse DECLINED); and REPORTS the `gitlink` rows as NOT
      RE-CHECKED, with their count. A repeatable `--estate-tree <repo>=<path>`
      supplies a carrying repository's working tree, and only then is that
      repository's `.gitmodules` evidence re-checked, an absence being a finding.
      No mode fetches a tree: the input is a path a caller already has.
- [ ] 3.4 ONE MEMBERSHIP ARM added to `scripts/validate-code-surface.py`, so the
      grammar scan and the membership scan report in one run. FAILS CLOSED on an
      identifier no row carries; REFUSES an `external` row naming the class;
      REPORTS a former address with the current one; does NOT judge a REGISTERED
      declaration and does NOT fall back; REPORTS a row whose IN-TREE evidence
      nothing names, and reports a `gitlink` row as NOT RE-CHECKED rather than as
      named or as stale; reads the archive and judges none of it. The arm takes no
      tree argument and makes no network call, so the required check's verdict is
      the same on every machine.
- [ ] 3.5 `tests/estate_inventory/` (NEW): one case per scenario class of both
      ADDED requirements and of the MODIFIED paragraph, each FAILING against the
      tree without § 3.1–§ 3.4 and passing with them, plus a LIVE-CORPUS case that
      reds `pytest-suite` when a declaration names a repository no row carries.
- [ ] 3.6 **NO OTHER FILE MOVES.** `scripts/code_surface.py`'s grammar,
      `scripts/scope_globs.py`'s derivation, the closed register, every existing
      test, every workflow, every contract member and every promoted byte are
      untouched. Verified in the realization pull request by its own diff.

## 4. Verification (OPEN; taken at the realization head)

- [ ] 4.1 `python3 -m pytest tests/estate_inventory tests/code_surface tests/scope_globs -q`
      green, with the fails-then-passes evidence for § 3.5 pasted in the
      realization pull request body.
- [ ] 4.2 `python3 scripts/validate-estate-inventory.py .` and
      `python3 scripts/validate-code-surface.py .` both exit 0, the second now
      reporting the membership counts beside the grammar counts.
- [ ] 4.3 The 33 rows RE-MEASURED at the realization head rather than carried from
      this drafting, by the FIVE D0.1 commands, with any row that moved DISCLOSED
      at this box. The corpus moves between drafting and landing; the register's
      own requirement says so and this packet is bound by it. The re-measurement
      also settles the governance class of rows 28-33, which D0.2 states only as
      far as the openxFactory sites reach: whether the NESTING repository pins
      rather than authors any of the six is a fact in that repository's tree.
- [ ] 4.4 `pytest-suite` green on the realization pull request at its merge head.

## 5. Archive (OPEN; a separate act on a separate word)

- [ ] 5.1 **(OPERATOR)** `code_surface` is NON-EMPTY, so under `release-realization`
      this packet archives on MERGED-PLUS-GREEN REALIZATION EVIDENCE and not on
      this landing. The archive is a separate pull request on a separate word.
- [ ] 5.2 **(OPERATOR)** Promote the `## MODIFIED` block and the two `## ADDED`
      requirements onto `openspec/specs/release-realization/spec.md` at that
      archive, and at that archive only.
- [ ] 5.3 **(OPERATOR)** Close openxFactory #1087 THERE, by a closing keyword
      written in the archive pull request and in no commit message on this branch.

## 6. Measured and NOT taken (OPEN; successors, not work owed)

- [~] 6.1 **THE THREE DIVERGENT FIXTURE ROWS ARE NOT CORRECTED HERE.**
      `contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml` names
      `opensoft/LegalxFactory` (404), `opensoft/LedgerxFactory` and
      `opensoft/MedxFactory` (both redirect-only). It is a CONTRACT MEMBER whose
      correction owes a manifest entry and a bundle, and the Medx row is the
      subject of the ACTIVE draft `adopt-medxsoft-repository-identity`. Correcting
      it here would reach into another lane's packet and spend a bundle this
      packet declares it does not spend. The inventory REPORTS the divergence;
      the correction is a successor.
- [~] 6.2 **THE TRANSFER MAP IS NOT EXTENDED.** It carries ONE row and the estate
      has taken at least three transfers. Extending it is
      `adopt-medxsoft-repository-identity`'s act for the Medx half and an
      unclaimed act for the Ledger half; this packet READS the map and adds no row
      to it.
- [~] 6.3 **THE GLOSS IS STILL NEVER JUDGED, AND ONE CONSEQUENCE IS MEASURED
      HERE.** `create-ledgerxwallet-overlay-boundary` writes
      `opensoft/LedgerxWallet (new), LedgerxFactory, openxFactory — THREE
      repositories`, so its `(` opens the gloss and the grammar reads a
      ONE-repository head where the author meant three. Whether a head may carry
      a parenthetical before its list is a question about the GRAMMAR, which is
      the predecessor's ratified surface and not this packet's. Named, not taken.
- [~] 6.4 **NO OTHER ESTATE REPOSITORY IS SWEPT.** The inventory is authored in
      openxFactory and read by openxFactory's validators. Whether the aggregation
      or a DomainxFactory should consume it, and if so, pinned by commit and
      digest per CLAUDE.md rule 1, which would move the file under `contracts/`
      after all, is a successor with its own authority question.
- [~] 6.5 **THE PROVIDER IS NEVER ASKED AT THE GATE.** Existence was checked once,
      at the measurement (`design.md` D0.4), to establish that the six declared
      identifiers are real and that the estate already writes one that is not. A
      gate that re-checked would make a required check depend on a token and on
      read access to a private repository. Named as the bound, not as work owed.
