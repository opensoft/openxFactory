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
- [x] 1.5 **(OPERATOR — THREE FURTHER WORDS OF 2026-09-18, PLUS A FOURTH OF
      2026-09-21, ON GAPS THE BARE WORD DID NOT REACH.)** Copilot's review of PR
      #1101 found three gaps in the ratified text on 2026-09-18. Each was put to
      Brett Heap as a multiple choice and each was answered on 2026-09-18 at
      approximately 15:40Z in the lane's terminal to lane `openxfactory-5`,
      recorded as `RULED` entries in `opensoft/brett-wip`
      `lanes/log/openXfactory-5.md`. **ALL THREE WERE ENCODED AS RATIFIED TEXT IN
      ONE COMMIT (`089b02e0`)**, verbatim:
      **(a) "Bind the carrier identity"** — a working tree supplied for a
      `gitlink` row's re-check MUST be verified as a checkout of the CARRIER the
      row names, by the tree's own origin URL or by its record in
      `contracts/policies/repository-identity.yaml`, before its `.gitmodules`
      evidence is trusted; a tree that fails leaves the row NOT RE-CHECKED —
      counted, neither passed nor failed. Encoded in the enumeration
      requirement's re-check paragraph, in the scenario *A gitlink row is
      re-checked only against a supplied tree*, in the membership arm's bound
      sentence and its scenario *An inventory row nothing names*; mirrored at
      `design.md` D1.2 and at § 3.2, § 3.3 and § 3.4 below.
      **(b) "#1101 declares #1108 and folds its text"** —
      `sequenced_after: [amend-code-surface-grammar-comma-and]` is declared and
      the `## MODIFIED` block is written over THAT packet's outcome, carrying its
      ratified wording byte-for-byte with this packet's membership change on top.
      Promotion order #1108 then #1101; **#1108 is not touched.** Mirrored at
      `design.md` D6 and D3, and in the delta's preamble.
      **(c) "MAY becomes MUST"** — the inventory MUST carry the PROVISIONAL row a
      repository-creating ratified change opens; the membership arm stays
      UNCONDITIONAL and fails closed. Mirrored at `design.md` D1.1.
      **(d) "Drop the pin admission on row 3"** — a LATER word answering a LATER
      gap, given 2026-09-21 approximately 20:30Z in the lane's terminal, recorded
      as a `RULED` entry in `opensoft/brett-wip` `lanes/log/openXfactory-5.md`,
      over a gap Copilot's review of the REALIZATION pull request **#1119**
      found (not #1101, already merged by then, and encoded in a SEPARATE, LATER
      commit than (a)-(c)): `design.md` D0.2 row 3 admitted `codeXfactory/codexFactory`
      by `pin (review-lane-pin.yaml)` among others, and that file is `kind:
      pinned_workflow`, a commit-only pin of governance code with no digest
      set — satisfying neither half of the delta's own `pin` kind definition.
      Row 3 loses the `pin` admission and keeps `gitlink (opensoft/xFactory)`
      and `workflow`; the `pin` kind's definition is UNCHANGED. TWO REMEDIES
      WERE PUT AND DECLINED — widening the kind's definition, and adding a
      sixth admission kind — because row 3 is already admitted without either.
      Mirrored at `design.md` D0.1, D0.2; full record at
      `review/ratification-2026-09-18.md` § 7.
      **NO WORD OF BRETT HEAP'S IS PARAPHRASED HERE**: all four quoted strings
      are the option texts as given, and the encoding is what this lane did with
      them.

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
      DECLARED.** At drafting no active change wrote `(release-realization,
      Code-surface declaration grammar is gated)`, so the block was SOLE and owed
      no `sequenced_after:`. **THAT CHANGED ON 2026-09-18**, when
      `amend-code-surface-grammar-comma-and` landed at `60d281a8` with a block
      over the same key: the ordering is now DECLARED, the block is written over
      that packet's outcome, and the family resolves the pair and reports
      nothing (§ 1.5 (b), `design.md` D6). The three superseded sentences are named
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

Record note 2026-09-23 (landing prep, PR #1119): this sentence describes the
CODE SURFACE. The landing-prep tick commit moves this tasks.md file itself, the
packet's lifecycle record, exactly as PR #1107 did for its packet; the
code-surface diff stays five files, and tasks.md is the sixth file in the
branch diff.

- [x] 3.1 `scripts/estate-repository-inventory.yaml` (NEW): the 33 candidate rows
      of `design.md` D0.2, `schema_version` and `kind` at the head (CLAUDE.md
      rule 4), a header stating why the file is not under `contracts/` and what a
      row means, and per row `repository:`, `name:`, `role:`, `governance:`,
      `admitted_by:` (one or more of the five kinds with its site, and for a
      `gitlink` THE REPOSITORY THAT CARRIES IT, which is the aggregation for 23
      rows and a governed DomainxFactory for 7) and, for a `change`-admitted row,
      `provisional: true` with the change id. **THE `change`-ADMITTED ROW IS
      OWED, NOT OPTIONAL** (ruling "MAY becomes MUST", § 1.5 (c)): row 27 is
      written because `create-ledgerxwallet-overlay-boundary` is ratified and
      creates the repository, and omitting it would refuse that packet's lawful
      declaration at the membership arm.
      **DONE, commit `eee585c3` (PR #1119).** Amended twice on the SAME ratified
      shape, both disclosed rather than silent: row 3 (`codeXfactory/codexFactory`)
      dropped its unlawful `pin` admission at `728b8770` (Brett Heap's ruling,
      verbatim "Drop the pin admission on row 3", RULED at `opensoft/brett-wip`
      `lanes/log/openXfactory-5.md`, matching the same-word amendment landed into
      `design.md` D0.2 on `main` by PR #1130 `0f23341f`); the header's nested-gitlinks
      re-measurement note was corrected from "11 in 6" to "12 in 7" at `5e08ff1d`
      (round 4). Unchanged since (`git diff 5e08ff1d..c2d4309b --stat -- scripts/estate-repository-inventory.yaml`
      is empty).
- [x] 3.2 `scripts/estate_inventory.py` (NEW): the reader and the row-level judge,
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
      (`design.md` D1.2). It also carries the CARRIER-IDENTITY CHECK that mode
      uses — given a path, read the tree's own origin URL and normalize it, and
      resolve a FORMER carrier address through
      `contracts/policies/repository-identity.yaml` — returning verified /
      unverified rather than raising, so § 3.3 can report an unverified tree as
      NOT RE-CHECKED instead of failing the run (ruling "Bind the carrier
      identity", § 1.5 (a)).
      **DONE, commit `92bb8eb7` (PR #1119), hardened across seven Copilot review
      rounds — each fix disclosed with its own fails-then-passes case in the PR
      body, none changing this task's own shape:** a sanitized git environment for
      the carrier read (`b747daad`, `247ca3dc` — `GIT_CONFIG` added to
      `_SCRUBBED_GIT_ENVIRONMENT`, measured inert on this git and scrubbed anyway);
      the WORK-TREE ROOT bound rather than any path git will answer for, refusing a
      bare repository or an imprecise subdirectory (`b747daad`); a `gitlink`
      carrier required to resolve to a `governed` row (round 1); a `root` row
      required to declare `governance: governed` (`247ca3dc`); a `pin` admission on
      a `governance: governed` row refused at load (`b626316b`, round 6 — the same
      defect class the row-3 ruling closed on one row, generalized to every row);
      `pin`/`workflow` admissions named by their STRUCTURAL field only, never by
      prose elsewhere in the file (`a961d92c`, round 4), extended to the JOB-LEVEL
      `jobs.<job_id>.uses:` reusable-workflow site (`81a01b3c`, round 5);
      `load_transfers` holding a `complete` row to its own field-agreement shape —
      `transferred_on` a real date (`type(...) is datetime.date` exactly, not
      `isinstance`, which a `datetime.datetime` subclass would pass — round 7,
      `c2d4309b`), both addresses `<owner>/<name>`-shaped, PyYAML's `ValueError` on
      an impossible calendar date caught and reported as a finding rather than
      raised (round 7, `c2d4309b`), and two `complete` rows naming the same
      `former` refusing the whole file rather than silently overwriting (round 7,
      `c2d4309b`). `python3 -m pytest tests/estate_inventory tests/code_surface
      tests/scope_globs -q` — 317 passed at `c2d4309b` (52 at `729448f2`, the
      original § 3.5 delivery).
- [x] 3.3 `scripts/validate-estate-inventory.py` (NEW): the house validator CLI in
      the shape every other `scripts/validate-*.py` uses. The DEFAULT run judges
      the inventory file's SHAPE and its in-tree evidence and makes no network
      call: refuses a duplicate bare name, a row whose in-tree `admitted_by:`
      evidence names nothing, and a still-provisional row whose change has
      archived; REPORTS a row at a FORMER address, naming the current address the
      transfer map resolves (`design.md` D5: RECOMMENDED REPORT, ALTERNATIVE
      refuse DECLINED); and REPORTS the `gitlink` rows as NOT
      RE-CHECKED, with their count. A repeatable `--estate-tree <repo>=<path>`
      supplies a carrying repository's working tree, and **THE TREE IS VERIFIED
      AS THAT CARRIER BEFORE IT IS READ** — by its own origin URL or by the
      carrier's record in `contracts/policies/repository-identity.yaml` — and
      only then is that repository's `.gitmodules` evidence re-checked, an
      absence being a finding against the row. A supplied tree that does NOT
      verify leaves the row reported NOT RE-CHECKED and counted, neither passed
      nor failed, the report naming the carrier the row expects and what the tree
      actually is (ruling "Bind the carrier identity", § 1.5 (a); a path is an
      assertion and not an identity). No mode fetches a tree: the input is a path
      a caller already has.
      **DONE, commit `ed6160c7` (PR #1119).** Extended at `81a01b3c` (round 5) to
      thread `load_transfers`'s second return value (`transfer_findings`) through
      to a FAILED report block and the exit-code check, so a malformed transfer
      row is fail-closed here too, not only at the membership arm. `python3
      scripts/validate-estate-inventory.py .` — exit 0 at `c2d4309b`; `33
      repositories — 26 governed, 6 pinned, 1 external; 1 provisional`, `8 named, 0
      gone`, `30 NOT RE-CHECKED` (no tree supplied).
- [x] 3.4 ONE MEMBERSHIP ARM added to `scripts/validate-code-surface.py`, so the
      grammar scan and the membership scan report in one run. FAILS CLOSED on an
      identifier no row carries; REFUSES an `external` row naming the class;
      REPORTS a former address with the current one; does NOT judge a REGISTERED
      declaration and does NOT fall back; REPORTS a row whose IN-TREE evidence
      nothing names, and reports a `gitlink` row as NOT RE-CHECKED — whether no
      tree was supplied for its carrier or the supplied tree does not verify as
      that carrier — rather than as named or as stale; reads the archive and
      judges none of it. It takes NO EXCEPTION for the forward-looking window:
      the `change`-admitted PROVISIONAL row is OWED by § 3.1, so the window is
      answered by a row that resolves and the arm stays unconditional (ruling
      "MAY becomes MUST", § 1.5 (c)). The arm takes no tree argument and makes no
      network call, so the required check's verdict is the same on every
      machine.
      **DONE, commit `82ae4f1a` (PR #1119).** Extended at `81a01b3c` (round 5) the
      same way as § 3.3: `MembershipReport` gains `transfer_findings`, both its
      real and its `membership is None` fallback construction, the summary line,
      a FAILED block, and the exit-code check. `python3
      scripts/validate-code-surface.py .` — exit 0 at `c2d4309b`; `46 active
      proposals, 46 declaring — 9 \`none\`, 30 a repository list, 7 named by the
      register, 0 outside the grammar`; `membership: 30 readable heads naming 6
      distinct identifiers — 6 carried, 0 refused, 0 at a former address
      (reported), 7 registered and not judged, 0 transfer-map rows malformed`.
- [x] 3.5 `tests/estate_inventory/` (NEW): one case per scenario class of both
      ADDED requirements and of the MODIFIED paragraph, each FAILING against the
      tree without § 3.1–§ 3.4 and passing with them, plus a LIVE-CORPUS case that
      reds `pytest-suite` when a declaration names a repository no row carries.
      **TWO CASES ARE NAMED HERE BECAUSE THE RULINGS OF § 1.5 CREATED THEM**: a
      `gitlink` row handed a tree that is a checkout of a DIFFERENT repository
      reports NOT RE-CHECKED and is counted, neither passed nor failed (and a
      tree at the carrier's FORMER address, resolved through the transfer map,
      VERIFIES); and an inventory missing the `change`-admitted row for a ratified
      repository-creating change fails § 3.1's own shape check rather than being
      excused by the membership arm.
      **DONE, commit `729448f2` (PR #1119), 52 cases, one per scenario class of
      both ADDED requirements and the MODIFIED paragraph plus the two rulings'
      cases (§ 1.5's `gitlink`-at-a-different-repository and
      missing-`change`-row cases) — full list in the PR body's § 3.5 section and
      in the file itself. GROWN by every review round since, each new case named
      in the PR body's per-round table and every one shown failing against the
      pre-fix reader before the fix that closes it: round 1 (ten cases, `277c028e`);
      round 2, the carrier read (two cases, `b747daad`); round 3, `GIT_CONFIG` and
      the `root` governance check (two cases, `247ca3dc`); the row-3 ruling (one
      case, `728b8770`); round 4, structural-field-only reading and the 115KB
      workflow file (three cases, `a961d92c`); round 5, the transfer-row shape and
      the job-level `uses:` site (two cases, `81a01b3c`); round 6, `pin` on a
      `governed` row (one case, `b626316b`); round 7, the impossible date, the
      timestamp subclass, and the duplicate `former` (three cases, `c2d4309b`).
      `python3 -m pytest tests/estate_inventory -q` — **64 passed** at `c2d4309b`,
      measured directly rather than summed from the per-round additions above
      (which do not net to this figure one for one — later rounds' fixture
      changes and the file's own reorganization move individual case counts
      within a function as well as adding whole new ones; the per-round table in
      the PR body names every added or changed case by its actual test id). The
      LIVE-CORPUS case this section also owes is
      `test_every_live_declared_identifier_is_CARRIED_by_the_inventory`, in this
      same 64.
- [x] 3.6 **NO OTHER FILE MOVES.** `scripts/code_surface.py`'s grammar,
      `scripts/scope_globs.py`'s derivation, the closed register, every existing
      test, every workflow, every contract member and every promoted byte are
      untouched. Verified in the realization pull request by its own diff.
      **HELD, first taken at commit `8407e157`, RE-VERIFIED at `c2d4309b` across
      seven review rounds of further commits to the same five files**: `git diff
      origin/main..c2d4309b --stat` names exactly `scripts/estate-repository-inventory.yaml`,
      `scripts/estate_inventory.py`, `scripts/validate-code-surface.py`,
      `scripts/validate-estate-inventory.py` and
      `tests/estate_inventory/test_estate_inventory.py` — five files, nothing
      else, both at the original delivery and at every round since.
      Precisely: exactly five code-surface files (plus this tasks.md record,
      ticked at landing prep) — the code-surface diff has not grown a sixth
      member; `tasks.md` becomes the branch's sixth changed file only as the
      packet's own lifecycle record, per the § 3 boundary note above.

## 4. Verification (OPEN; taken at the realization head)

- [x] 4.1 `python3 -m pytest tests/estate_inventory tests/code_surface tests/scope_globs -q`
      green, with the fails-then-passes evidence for § 3.5 pasted in the
      realization pull request body.
      **GREEN at `c2d4309b`: `317 passed in 26.09s`.** The fails-then-passes
      evidence for every § 3.5 case, across all seven review rounds and the
      original 52, is in the PR body (a dedicated section per round, each
      reverting the reader to its pre-fix parent commit, showing the genuine
      failure, then restoring the fix).
- [x] 4.2 `python3 scripts/validate-estate-inventory.py .` and
      `python3 scripts/validate-code-surface.py .` both exit 0, the second now
      reporting the membership counts beside the grammar counts.
      **GREEN at `c2d4309b`, both exit 0** — transcripts and counts under §§ 3.3
      and 3.4 above (`0 transfer-map rows malformed` in the second, a field round
      5 added and round 7 exercised further).
- [x] 4.3 The 33 rows RE-MEASURED at the realization head rather than carried from
      this drafting, by the FIVE D0.1 commands, with any row that moved DISCLOSED
      at this box. The corpus moves between drafting and landing; the register's
      own requirement says so and this packet is bound by it. The re-measurement
      also settles the governance class of rows 28-33, which D0.2 states only as
      far as the openxFactory sites reach: whether the NESTING repository pins
      rather than authors any of the six is a fact in that repository's tree.
      **RE-MEASURED, full five-command sequence taken at `5e08ff1d` (round 4;
      transcripts and the two disclosed figure-moves — 12 nested gitlinks in 7
      repositories where D0.1 measured 11 in 6, and the corpus's ordinary drift —
      are in the PR body's § 4.3 section). NO ROW MOVED. Unchanged since:
      `scripts/estate-repository-inventory.yaml` carries no byte of diff between
      `5e08ff1d` and `c2d4309b` (§ 3.1 above), and rounds 5-7 touched neither the
      `.gitmodules` sites, the `contracts/` pins, nor the workflow `uses:` sites
      commands 1-4 read. Command 5 (the declared population, through the shipped
      reader) DOES move on its own — the corpus is read live, not frozen — and
      was RE-CONFIRMED FRESH at `c2d4309b` in this same pull request's final body
      update: still the same six distinct identifiers (`openxFactory`,
      `xFactory`, `openAvatar`, `opensoft/LedgerxWallet`,
      `opensoft/Keycloak-Install`, `opensoft/OpenXPKI-Install`), all six still
      resolving, zero refused, governance class of rows 28-33 unchanged. The
      governance-class settlement itself (pins vs. authors, per repository) is a
      fact of those repositories' own trees and does not move with the corpus
      count.
      **RE-MEASURED AGAIN, THE FULL FIVE-COMMAND SEQUENCE ACTUALLY RE-RUN — not
      reasoned from an unchanged-files argument — at `2858747b` on 2026-09-23,
      SUPERSEDING the PR body's round-7 note that this sequence was still owed
      at landing prep:** (1) re-measured at `2858747b` on 2026-09-23: `gh api
      repos/opensoft/xFactory/contents/.gitmodules -q .content | base64 -d |
      grep -oP 'github\.com[:/]\K[^ ]+' | sed 's/\.git$//' | sort` → 23
      addresses, set difference against the inventory's 23 `carrier:
      opensoft/xFactory` gitlink rows EMPTY both ways, matching `5e08ff1d`; (2)
      re-measured at `2858747b` on 2026-09-23: the same scan over the 25
      governed non-root rows the live inventory's own governance column now
      names → 12 nested gitlinks in 7 carriers (openxFactory 4, MedxEHR 2,
      LedgerxFactory 2, MedxFactory 1, MedxChart 1, MedxPractice 1,
      LedgerxAvatar 1), the identical distribution `5e08ff1d` recorded; (3)
      re-measured at `2858747b` on 2026-09-23: `grep -rn
      'source_repository\|^repository:' contracts/*.yaml` → 8 hits (7
      declaration lines, one the empty
      `review-lane-repin-binding.template.yaml` stub, one commented in
      `review-lane-floor-snapshot.yaml`), 6 distinct repositories, unchanged;
      (4) re-measured at `2858747b` on 2026-09-23: `grep -rhoP
      'uses:\s*\K[A-Za-z0-9._-]+/[A-Za-z0-9._-]+' .github/workflows/ | sort -u`
      plus `grep -rln 'codeXfactory/codexFactory' .github/workflows/` →
      `actions/*` and `codeXfactory/codexFactory`, ONE estate repository across
      the same four files (`doc-health-reusable.yml`,
      `merge-master-approval.yml`, `pytest-suite.yml`,
      `review-lane-repin.yml`), unchanged; (5) re-measured at `2858747b` on
      2026-09-23: `python3 scripts/validate-code-surface.py .` → exit 0, `46
      active proposals, 46 declaring — 9 \`none\`, 30 a repository list, 7
      named by the register, 0 outside the grammar`, archive `180 proposals,
      134 declaring, 4 outside the grammar`, `membership: 30 readable heads
      naming 6 distinct identifiers — 6 carried, 0 refused`, the same six
      identifiers as before (`openxFactory`, `xFactory`, `openAvatar`,
      `opensoft/LedgerxWallet`, `opensoft/Keycloak-Install`,
      `opensoft/OpenXPKI-Install`), matching the round 5-7 re-confirmation
      already cited at § 3.4. **NO ROW MOVED — confirmed this time by direct
      re-run of all five commands at the landing head, not by an argument about
      which files changed since `5e08ff1d`.**
- [x] 4.4 `pytest-suite` green on the realization pull request at its merge head.
      **NOTED, 2026-09-23, left `- [ ]` rather than ticked**: `pytest-suite` is
      GREEN on this pull request's own head `c2d4309b` — run `35896651067`
      (https://github.com/opensoft/openxFactory/actions/runs/35896651067),
      22m31s — `317 passed` among the other packages this workflow also runs.
      This box's own words ask for green "at its MERGE head", which is main's
      head after the landing squash and not this branch's own pre-merge head;
      the tick is the archive act's, from main's green run at the landed merge,
      per the coordinator's standing instruction for this box.
      **TICKED AT THE ARCHIVE ACT, 2026-09-23, ON `main`'s OWN RUN AT THE MERGE
      HEAD.** `pytest-suite` is GREEN on `main` at
      `5e122388d489378ea3e768de7f1de678f97e62e6` — run `35907128216`
      (https://github.com/opensoft/openxFactory/actions/runs/35907128216), event
      `push`, `completed` / `success`, 2026-09-23T19:06:54Z → 19:29:29Z,
      re-read with `gh run view 35907128216 --json
      headSha,conclusion,status,url` rather than carried. **THAT COMMIT IS THE
      MERGE HEAD ITSELF, NOT A DESCENDANT OF IT**: PR #1119 landed by SQUASH as
      `5e122388` (`gh pr view 1119 --json mergeCommit` →
      `5e122388d489…`, merged 2026-09-23T19:06:49Z), so the run decided exactly
      the tree the landing produced and no containment leg is owed. **THE HEAD
      THE NOTE ABOVE NAMES IS NOT THE HEAD #1119 MERGED FROM, AND THAT IS
      CORRECTED HERE RATHER THAN LEFT TO BE FOUND**: `c2d4309b` was followed
      by two `tasks.md`-only commits, `2858747b` and `5d44003c`, and
      `5d44003c` is the head the squash took (`gh pr view 1119 --json
      headRefOid` → `5d44003cc35d…`). `pytest-suite` is green there too — run
      `35904638873` (https://github.com/opensoft/openxFactory/actions/runs/35904638873),
      `success`, 2026-09-23T18:45:12Z → 19:03:50Z — beside every other check
      run at that head (`success`, `Sourcery review` `skipped`). Both readings
      of "at its merge head" hold, and the tick is taken from `main`'s own
      run, the stricter of the two.

## 5. Archive (PERFORMED 2026-09-23 on merged-plus-green evidence, on Brett Heap's archive word)

- [x] 5.1 **(OPERATOR)** `code_surface` is NON-EMPTY, so under `release-realization`
      this packet archives on MERGED-PLUS-GREEN REALIZATION EVIDENCE and not on
      this landing. The archive is a separate pull request on a separate word.
      **THE EVIDENCE IS IN HAND, 2026-09-23, AND EVERY LEG IS CITED RATHER THAN
      ASSERTED.** (i) THE PACKET landed as PR
      [#1101](https://github.com/opensoft/openxFactory/pull/1101) →
      `344ad3c7bc0b662a99590c836e4c91edcc77b3cf` on `main`,
      2026-09-18T18:51:59Z, on Brett Heap's *"ratify #1101"*, and the row-3
      amendment as PR [#1130](https://github.com/opensoft/openxFactory/pull/1130)
      → `0f23341fcf8c04ea234a57632c5ff321bc47c0f8`, 2026-09-21T22:01:50Z, on
      his *"Drop the pin admission on row 3"*. (ii) **§ 3's REALIZATION**
      landed as PR [#1119](https://github.com/opensoft/openxFactory/pull/1119)
      → `5e122388d489378ea3e768de7f1de678f97e62e6` on `main`,
      2026-09-23T19:06:49Z, by SQUASH from head `5d44003c`, on his *"land
      #1119"* (RULED in `opensoft/brett-wip` `lanes/log/openXfactory-5.md` at
      2026-09-23T16:34:17Z). (iii) **THE GREEN HALF AT CANON'S GRAIN**:
      `pytest-suite` SUCCESS on `main` AT `5e122388` itself, run
      [`35907128216`](https://github.com/opensoft/openxFactory/actions/runs/35907128216),
      2026-09-23T19:29:29Z (§ 4.4). `344ad3c7` → `0f23341f` → `5e122388` is
      an ancestry chain, each leg checked with `git merge-base --is-ancestor`.
      **THE OPERATOR HALF IS GIVEN, AND IT IS BRETT HEAP'S WORD, NOT THIS
      LANE'S DECISION**: verbatim *"archive it when the draft is up"*, given in
      the lane's terminal on 2026-09-23 — before the 20:58:43Z pause and
      repeated at the 21:03Z resume — and RULED in `opensoft/brett-wip`
      `lanes/log/openXfactory-5.md` at 2026-09-23T21:04:55Z against openxFactory
      #1087 (brett-wip commit `837f44cf`; the NOTED correction of that line's
      clock at 21:05:39Z, commit `3d01aa9b`). The archive pull request is
      opened as a DRAFT and lands by MERGE COMMIT, never squash, once it is
      green and Copilot-clean, so this directory's date keeps matching its
      adding commit.
- [x] 5.2 **(OPERATOR)** Promote the `## MODIFIED` block and the two `## ADDED`
      requirements onto `openspec/specs/release-realization/spec.md` at that
      archive, and at that archive only.
      **DONE THROUGH THE GOVERNED WRAPPER, NEVER A BARE `openspec archive`**, in
      the commit that moves this directory:
      `TZ=UTC python3 scripts/proposal-support.py . archive add-estate-repository-inventory --yes`,
      exit **0**. Its decisive lines: `ORIGIN RETAINED
      add-estate-repository-inventory (declaration unchanged since the ACCEPTED
      mutation 0f23341fcf8c, dispositioned accept by Brett Heap (openxFactory
      repository owner) on 2026-09-21; ratifying commit 344ad3c7bc0b)`;
      `Totals: 1 passed, 0 failed (1 items)`; `Task status: Complete`;
      `Applying changes to openspec/specs/release-realization/spec.md: + 2
      added, ~ 1 modified`; `Totals: + 2, ~ 1, - 0, -> 0`; `Change
      'add-estate-repository-inventory' archived as
      '2026-09-23-add-estate-repository-inventory'`; `OK openspec-cli-pin:
      @fission-ai/openspec@1.12.0 verified against its content address and
      every target validated --strict clean`; `NO SUPPORTING DOCS ... (origin
      retained, nothing to package)`. The CLI is the content-addressed pinned
      1.12.0 artifact and NOT the 1.13.1 on `PATH`; `--path-mode` was not used;
      `--date` was not passed, so the wrapper took today in UTC.
      **THE ARCHIVE DIRECTORY IS
      `openspec/changes/archive/2026-09-23-add-estate-repository-inventory/`**,
      named for the UTC day of the wrapper run and of the commit that adds it,
      which is what `archive-date-vs-commit` measures.
      **ORIGIN RETAINED THROUGH A RECORDED ACCEPTANCE, WHICH IS STATED HERE
      RATHER THAN LEFT TO A READER OF THE WRAPPER'S OUTPUT.** Without it the
      gate REFUSES: the `origin:` block differs from the one at the ratifying
      commit `344ad3c7` in exactly one key, `approved_by`, to which PR #1130
      (`0f23341f`) APPENDED the ten-line paragraph recording Brett Heap's fifth
      word, *"Drop the pin admission on row 3"* — a pure addition, no line of
      the block moved. RESTORING the ratified bytes would delete that record,
      so the archive act adds ONE `accept` entry to
      `openspec/origin-dispositions.yaml`, in the shape of that file's first
      entry (whose accepted declaration is likewise the ratifier's own later
      word): both commits in full, `changed_keys: [approved_by]`, the verbatim
      word and its citations.
      **THE PROMOTED TEXT IS THE DELTA AS WRITTEN, MEASURED ON BOTH SIDES AND
      NOT EYEBALLED**, each block extracted programmatically by its
      `### Requirement:` heading from the archived delta and from canon and
      hashed. `openspec/specs/release-realization/spec.md` is the ONLY
      capability this delta touches:
      the `## MODIFIED` block *Code-surface declaration grammar is gated*
      REPLACES canon's block — before 15,665 bytes / 184 lines / 11 scenarios
      (sha256 `e8477c2a5d7e74b0…`), after **15,971 bytes / 207 lines / 11
      scenarios, sha256 `2b9a75d6bf836c8e…` on BOTH the archived delta and
      canon**; *The estate's repositories are enumerated in a governed
      inventory* is ADDED — **8 scenarios, 12,297 bytes / 160 lines, sha256
      `3020c2c916df22bb…` on both**; *A declared repository is judged for
      membership against the estate inventory* is ADDED — **9 scenarios, 7,712
      bytes / 108 lines, sha256 `8189458612a21dcb…` on both**.
      `release-realization` requirement count **19 -> 21** and scenario count
      **105 -> 122** (-11 +11 +8 +9, re-taken with `grep -c` from canon rather
      than copied forward); the other EIGHTEEN requirement blocks are
      byte-identical before and after, hashed one by one; `--numstat` **+312
      -19**, and `-w` reads the same, so no changed line is whitespace-only.
      THE CLI DID NOT DIVERGE FROM THE DELTA and no block was corrected by hand.
      **ONE CONSEQUENCE OF "THE DELTA AS WRITTEN" IS STATED RATHER THAN LEFT TO
      BE FOUND.** Canon's `**AMENDED BY**` paragraph for
      `amend-code-surface-grammar-comma-and` was QUALIFIED in canon after this
      block was ratified (PR #1112's round-3 fix, `35afdc3f`, 2026-09-21); this
      block carries that paragraph as #1108's RATIFIED delta states it,
      byte-for-byte, on the ruling *"#1101 declares #1108 and folds its text"*,
      so the promotion restores the ratified wording and canon no longer
      carries the round-3 qualification. That paragraph is the one unit the
      `modified-block-currency` arm reported as uncarried by this ACTIVE block
      (1 of 66, `info`), and its `_LEDGER_SUBJECTS` row in
      `tests/doc-health/test_modified_block_currency_self_gate.py` retires at
      this archive on its own stated condition. Re-applying the qualification
      would edit ratified text after the word, which is not this act's to do;
      it is named in the archive pull request for the ratifier.
- [x] 5.3 **(OPERATOR)** Close openxFactory #1087 THERE, by a closing keyword
      written in the archive pull request and in no commit message on this branch.
      **THE INSTRUMENT IS PLACED, AND THE TICK RECORDS THE PLACING AND NEVER
      THAT THE ISSUE IS SHUT.** The closing keyword naming openxFactory #1087 is
      written as its own line in the BODY of the archive pull request that
      carries this commit, and in NO other place; #1087 shuts on the MERGE of
      that pull request — the landing lane's act on Brett Heap's archive word,
      RULED in `opensoft/brett-wip` `lanes/log/openXfactory-5.md` at
      2026-09-23T21:04:55Z against #1087 — and at no earlier act. **AND NO
      COMMIT MESSAGE CARRIES A CLOSING KEYWORD, SCANNED RATHER THAN ASSUMED**:
      a case-insensitive Python `re` scan for any of `close`, `closes`,
      `closed`, `fix`, `fixes`, `fixed`, `resolve`, `resolves`, `resolved`
      followed by an optional colon and an issue reference returns **0**
      matches over this branch's commit messages, over the 22 commits of the
      realization pull request #1119, and over its squash commit `5e122388`.
      Every other issue and pull-request number in those messages and in the
      archive pull request's body is a `Refs`-style naming and shuts nothing.

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
