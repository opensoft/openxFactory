# Tasks: gate-realization-axis-vocabulary

Status: ratified
Ratified by: gate-realization-axis-vocabulary — 2026-09-12, Brett Heap, D1 "Keep and gate" / D2 "Sweep in this PR" / D3 "Resolve against the registry that exists" (record `review/ratification-2026-09-12.md`)
Kind: tasks

`code_surface: openxFactory`, `target_release: implemented`. The realization
group is § 3 and it is IN THIS PULL REQUEST: the tasks are individually
executable, so under `release-realization`'s decomposition rule this packet
realizes through its own task list rather than through a feature DAG.

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in
this pull request or a measurement recorded verbatim in the pull request body
and reproducible from the commands named beside it.

**§ 1 (RATIFICATION) IS CLOSED: BRETT HEAP RULED ON 2026-09-12 AT 15:45Z.**
Three independent multiple-choice rulings over `design.md`'s three declared veto
points, the recommendation presented first in each — **D1 "Keep and gate"**,
**D2 "Sweep in this PR"**, **D3 "Resolve against the registry that exists"** —
recorded on openxFactory PR
[#963](https://github.com/opensoft/openxFactory/pull/963#issuecomment-5646922493)
at 2026-09-12T15:45:19Z; record `review/ratification-2026-09-12.md`. All three
are the RECOMMENDED and already-encoded options, so no wording moved on the
ruling. His earlier word of 2026-09-11T12:08:24Z, verbatim **"land each when
green, archive both when landed, claim 955 and 956"**, commissioned the
AUTHORING of this packet and decided no wording; it is recorded as the origin in
`.openspec.yaml`, is not read as an approval, and is untouched by this
ratification. `.openspec.yaml` now carries the approval pair as a pure ADDITION
beside that unmoved drafting provenance, and every document here carries
`Status: ratified`.

**§ 5 (ARCHIVE) IS ENTIRELY OPEN.** `code_surface` is non-empty, so the archive
is a separate act on merged-plus-green realization evidence and a separate word,
and openxFactory #956 closes THERE and not at this landing.

**§ 6 IS UNTICKED ON PURPOSE**: residue, measured and deliberately not taken.

## 1. Ratification — GIVEN 2026-09-12

- [x] 1.1 **THE PACKET IS RATIFIED.** Brett Heap (openxFactory operator
      authority) ruled on this packet itself on 2026-09-12 at 15:45Z, recorded
      on PR
      [#963](https://github.com/opensoft/openxFactory/pull/963#issuecomment-5646922493)
      at 2026-09-12T15:45:19Z. `.openspec.yaml` gains `approved_by` and
      `approved_on` as a pure ADDITION beside a byte-unmoved drafting
      provenance — `kind` and `id` never move — which is the shape
      `add-drafted-proposal-origin` (issue #318) defined for exactly this
      transition. Every document carries `Status: ratified` with one citation
      line naming all three ruled labels; record
      `review/ratification-2026-09-12.md`, gate set re-derived on the ratified
      tree at `review/verification-2026-09-12.md`.
- [x] 1.2 **`design.md` D1 RULED — "Keep and gate"**, the RECOMMENDED option
      (2026-09-12T15:45:19Z, PR #963), against *"Admit none"* and *"Rule none a
      synonym"*. The two-value vocabulary stays exactly as ratified and is
      GATED by ADDING one requirement plus a closed register. The options as
      put: option 1, GATE the two-value vocabulary as ratified by
      ADDING one requirement plus a closed register (recommended); option 2,
      AMEND *Realization axis declaration* to admit the divergence; option 3,
      RULE the value a synonym. The cost of 2 and 3 is the same and is stated
      in D1: both are `## MODIFIED` blocks over a title the ACTIVE ratified
      `add-structured-scope-substrate` already modifies, so both owe
      `sequenced_after: [add-structured-scope-substrate]`, a pre-text taken
      from that change rather than from canon, and its archive-order hold.
      Option 3 additionally does not reach its own subject: all five active
      `none` carriers declare a NON-EMPTY `code_surface`.
- [x] 1.3 **`design.md` D2 RULED — "Sweep in this PR"**, the RECOMMENDED
      option (2026-09-12T15:45:19Z, PR #963), against *"Each owning lane
      sweeps"* and *"Register all 26"*. The existing non-conforming spellings
      across the corpus are swept in this same pull request. The population is
      a fact about a TREE and was re-measured at the ratified head (the merge
      of `origin/main` `1f068646`): **SIX** carriers, not the five this option
      was drafted against — § 3.4, § 3.18, `design.md` D2a — and **0** outside
      the vocabulary after. The options as put: option 1, this pull request
      corrects the five `none` carriers, one value token each with every gloss
      preserved (recommended); option 2, each owning lane corrects its own and
      the gate lands ADVISORY until the last is done; option 3, correct nothing
      and register all 26.
- [x] 1.4 **`design.md` D3 RULED — "Resolve against the registry that
      exists"**, the RECOMMENDED option (2026-09-12T15:45:19Z, PR #963),
      against *"Resolve literally"* and *"Accept any release-shaped token"*.
      The gate resolves a token against the registry as it stands on the tree
      it scans — at this ratified head `contracts/releases/` carries 55 digest
      inventories — with the release-identifier SHAPE accepted, and SAID OUT
      LOUD, only where the scanned tree defines no registry at all. The options
      as put: option 1, resolve against `contracts/releases/` — the registry
      that exists (recommended); option 2, resolve literally against the
      aggregation repository, which defines no releases and carries no tags, so
      nothing resolves; option 3, accept any release-SHAPED token, which stops
      distinguishing a release from a wish.
- [x] 1.5 **D0 AND D4 THROUGH D7 WERE CARRIED BESIDE THEM AND NONE WAS
      VETOED**, each with its alternative written out and each available to be
      vetoed in the same ruling: D0 (the measurement), D4 (the code surface,
      the three exit codes, and the register's home outside `contracts/`), D5
      (why an OpenSpec change and not a patch), D6 (sequencing and the sibling
      search), D7 (what is not taken). The ruling of 2026-09-12T15:45:19Z
      reached D1, D2 and D3 and took each one's recommendation; it named none
      of the carried five, and none of them moves.

## 2. The measurement, taken before the design

- [x] 2.1 **THE CORPUS WAS RE-MEASURED, NOT QUOTED.** Fresh clone at
      `origin/main` `38c076d1`; the issue's method re-run over every
      `openspec/changes/**/proposal.md`: **199** proposals, **181** declaring
      `target_release:`, **32** declaring `none` — **5** ACTIVE and **27**
      archived. The issue's "6 active" is stale by one:
      `state-header-window-budget` archived at PR #953.
- [x] 2.2 **THE WIDER DIVERGENCE WAS FOUND BY MEASURING, AND IT MOVED THE
      DESIGN.** Of **38** ACTIVE proposals (all 38 declare the field) only
      **12** declare a value the vocabulary admits — **9** `implemented`, **3**
      a release this estate defines. **26** are outside it, in four classes:
      `none` **5**, deferred allocation **12**, realization state **4**,
      repository bootstrap **2**, answers-another-question **3**.
- [x] 2.3 **THE TWELVE ARE OBEYING ANOTHER RATIFIED RULE.**
      `docs/contract-versioning-policy.md` § Bundle Realization Order:
      *"Contract-bundle realization is serialized and allocates versions late"*.
- [x] 2.4 **NO GATE READS THE VALUE**, confirmed by the issue's own command.
      `grep -rn target_release scripts/ tests/ .github/`: four lines in
      `scripts/ideation_dashboard/generator.py` (410, 416, 571, 576) plus
      `web/views/wheel.js:767-768`, both display; nothing in `.github/`;
      fixture text only in `tests/`, in BOTH spellings
      (`tests/ideation-dashboard/test_gate_console.py` `none`;
      `tests/scope_globs/` and `tests/sequenced_after/` `implemented`). The
      snapshot schema types the field `{type: [string, "null"]}` — no enum.
- [x] 2.5 **THE AGGREGATION REPOSITORY DEFINES NO RELEASES**, which is D3's
      ground: `opensoft/xFactory` carries no `contracts/` tree and
      `GET /repos/opensoft/xFactory/tags` returns an empty list, while
      `contracts/releases/` here carries 53 digest inventories and
      `contracts/manifest.yaml` declares `contract_bundle_version:
      contract-v3.6`.
- [x] 2.6 **THE ARCHIVE WAS COUNTED AND NOT JUDGED**: 161 archived
      `proposal.md`, **61** carrying a value outside the vocabulary.
- [x] 2.7 **`kind: ad_hoc` IS CHECKED RATHER THAN ASSUMED.** `ideation/staging/`
      enumerated (31 topic folders) and `INDEX.md` read on 2026-09-11: no topic
      names the realization-axis front matter, the `target_release` vocabulary
      or a proposal front-matter validator.
- [x] 2.8 **NO SIBLING WRITES THIS REQUIREMENT** (`design.md` D6, pasted there
      in full): no open pull request touches `release-realization`,
      `target_release` or these scripts; the two active changes with a
      `specs/release-realization/` delta write different requirement titles;
      the title added here appears nowhere else in the corpus.

## 3. The realization — a house validator and a closed register, in this pull request

- [x] 3.1 `scripts/target_release.py` (NEW) — the reader and judge. Reads the
      declaration through the SHIPPED strict loader
      `frontmatter_strict.read_front_matter`, adding no second parser; extracts
      the VALUE TOKEN (first whitespace-delimited word, trailing `.,;:`
      stripped); resolves a named release against
      `contracts/releases/<token>.digests.yaml`; loads and shape-checks the
      register; scans top-level active changes and counts the archive.
- [x] 3.2 `scripts/validate-target-release.py` (NEW) — the CLI, in
      `validate-scope-globs.py`'s shape. `[REPO_ROOT]` plus `--register PATH`
      (for the tests and for a consuming tree; the gate runs it with neither).
      Exit 0 clean, 1 an off-vocabulary declaration, 2 an unusable or stale
      register; both present prints both and exits 1.
- [x] 3.3 `scripts/target-release-register.yaml` (NEW) — **21 entries in four
      classes** (deferred-allocation 12, realization-state 4,
      answers-another-question 3, non-bundle-target 2), each with its value
      token, class, reason, citation and retirement event. CLOSED: removable,
      never addable. Not under `contracts/`, deliberately (`design.md` D4).
- [x] 3.4 **THE SIX OFF-VOCABULARY CARRIERS CORRECTED** — one value token per
      file, every prose gloss preserved verbatim, six files and six lines in
      all. The five `none` carriers `design.md` D2 names:
      `add-composed-view-authoring`, `add-cpc-clearing-boundary`,
      `add-lens-document-selection`, `add-substantive-review-lane`,
      `register-gate-rules-council-seats`. And the SIXTH, which `origin/main`
      acquired after D2 was drafted and this branch took at its merge of
      `1f068646` (§ 3.18):
      `amend-kill-switch-to-declared-test-companion`, whose declaration
      carried NO leading token at all — a running sentence, so the value token
      was the article `a` — corrected to `implemented` before the author's own
      gloss, carried verbatim after an em dash (`design.md` D2a; the gloss
      itself says *"No contract bundle is cut … and NO RELEASE TAG IS OWED"*,
      which is what `implemented` means). The custody check is in `design.md`
      D2 and covers the sixth unchanged: `record-immutability` binds
      `Status: record` documents only, and neither *Origin retention at
      archive* nor *Scope retention at archive* reaches `target_release:`.
- [x] 3.5 `tests/target_release/test_target_release_gate.py` (NEW, **79 tests**,
      counted last from a collected run of the file) — the token rule (7,
      including the two § 3.18 adds: a running sentence's first word IS its
      token, and the swept form — token, em dash, gloss — reads as the token),
      reading the declaration including a strict-loader refusal, **a
      repeated declaration refused rather than half-read, and an INDENTED
      gloss line that is a gloss and not a repeat** (8), release
      resolution with and without a registry, **including the estate schema's
      three-component form, the assertion that the shape IS the schema's, and
      the shape-only fallback saying so out loud** (10), **a candidate
      inventory refused for being a symlink, including one planted outside
      the tree, beside a REGULAR inventory for a different token still
      resolving** (3), **a symlinked registry DIRECTORY treated as absent,
      its external contents (present or empty) granting no extra trust
      either way, and the gate printing the same shape-only note it prints
      for a tree with no registry at all** (3), **a symlinked ANCESTOR of the
      registry directory (`contracts/` itself) treated the same way, with
      `repo_root` itself being reached via a symlink pinned as NOT the same
      escape** (2), **the token shape-checked
      before it can become a path (6)**, the register's shape refusals (4),
      **the entry's citation enforced at the load (5)**, **the same two classes
      swept (3)**, **the register removable and never addable (5)**, the gate
      end to end (13: the refusal, `implemented`, an
      archived record, a resolving release, a release name that resolves to
      nothing, an absent declaration, an empty declaration, an unreadable
      proposal reported not crashed, a registered declaration, a stale entry, a
      token that moved, a finding and a stale entry together, a missing
      register), and three over the live corpus and the real register. **NO
      EXISTING TEST IS EDITED, FLIPPED OR DELETED (ONE RENAMED, a typo)** —
      the fourteen added by § 3.7, the eight added by § 3.9, the five added
      by § 3.10, the three added by § 3.11, the three added by § 3.14, the
      three added by § 3.15, the two added by § 3.17, the four added by
      § 3.18 and the five added by § 3.19 join the file,
      `_entry()` gains the citation the loader now requires,
      `test_a_symlinked_registry_directorys_contents_grant_no_extra_trust`
      is renamed (§ 3.17 (b), a dropped apostrophe) to
      `test_a_symlinked_registry_directory_contents_grant_no_extra_trust`, and
      `test_an_entry_missing_a_required_key_refuses` keeps its subject by
      carrying every key but the one it is about.
- [x] 3.6 **THE GATE NEEDS NO WORKFLOW EDIT**, confirmed by running it: the
      required `pytest-suite` runs `python3 -m pytest tests/ -q -m "not
      postgres"`, which collects `tests/target_release` with no registration
      anywhere.
- [x] 3.7 **THE BENCH'S TWO CODE FINDINGS TAKEN, AND THE SWEEP FOR THEIR TWO
      CLASSES** (Copilot round 1 on the draft pull request, both threads TAKEN
      IN FULL; `design.md` D8). (a) **NOTHING AUTHOR-CONTROLLED BECOMES A PATH
      BEFORE IT IS SHAPE-CHECKED.** `resolves_as_release` matched
      `RELEASE_ID_RE` only on the NO-REGISTRY branch, so with a registry present
      the value token went straight into the lookup: measured on a built tree,
      `target_release: ../elsewhere` RESOLVED against a planted
      `contracts/elsewhere.digests.yaml` and the scan reported **0 findings, 1 a
      named release** — the registry boundary was not holding. The shape is now
      the FIRST test in EVERY branch and a non-matching token never becomes a
      path component; the same tree now reports the declaration as a finding.
      (b) **EVERY FIELD THE REQUIREMENT NAMES IS ENFORCED AT THE LOAD.** The
      ADDED requirement has each standing entry carry "the value token as it
      stands, the class of divergence, the reason, a citation, and the event
      that retires the entry", but `_REQUIRED_ENTRY_KEYS` omitted `cited_to`
      entirely and only a test over THIS repository's register asked for it:
      measured, `load_register` ACCEPTED an entry with no citation at all. It is
      now a required key, shape-checked as a non-empty list of non-empty
      strings. **SWEPT FOR THE SAME TWO CLASSES**, and two more found: a
      register entry's `change:` is resolved under `openspec/changes/` by every
      consumer, so it is shape-checked as one directory segment
      (`CHANGE_ID_RE`) before the loader returns it; and the CLOSED class set
      the requirement makes a specification act lived only in a corpus test, so
      it is now `REGISTER_CLASSES` beside the loader, enforced for every tree,
      and the corpus test reads the module's set instead of a second copy.
      **MEASURED AND NOT TAKEN:** the register's own `schema_version:`/`kind:`
      are not enforced by the loader — the requirement does not name them, and
      refusing a consuming tree's register for a field the requirement never
      asks for would exceed it.
- [x] 3.8 **THE TEST FIGURE IN § 3.5 AND IN `proposal.md`'s `code_surface:` WAS
      RE-MEASURED AFTER § 3.7, § 3.9, § 3.10 AND § 3.11 AND NOT CARRIED
      FORWARD.** `python3 -m
      pytest tests/target_release -q` — **exit 0**, *"62 passed in 2.92s"*; the
      per-section breakdown in § 3.5 is a count of `def test_` under each
      banner in the file, taken from the file itself.

- [x] 3.9 **THE BENCH'S SECOND ROUND, FOUR THREADS, ALL FOUR TAKEN** (Copilot
      round 2; `design.md` D8). (a) **A REPEATED DECLARATION WAS HALF-READ.**
      `target_release:` is a PROSE header, so the shared loader JOINS a repeat
      instead of refusing it as the duplicate key a STRUCTURED field's repeat
      would be. Measured: a block declaring `target_release: implemented (the
      main line)` and then `target_release: none` came back as
      `'implemented (the main line)\ntarget_release: none'` and tokenized as
      `implemented` — two declarations shown, the first authorized.
      `declaration` now refuses the repeat BY NAME, on the value the loader
      returned and without writing a second front-matter parser; the
      requirement gains the sentence and a scenario. (b) **THE CLOSED REGISTER
      WAS NOT CLOSED** (two threads, the requirement's text and the loader's
      code, one defect). The requirement SHALLs a register that is removable
      and never addable, and the register file's own header says so, but every
      new `(change, token)` pair was accepted — a later pull request could have
      appended an exception and kept the gate green with no change to the
      specification. `CLOSED_REGISTER` now records the 21 pairs the register
      holds at this gate's landing and `load_register` REFUSES an entry the
      baseline does not carry, so granting an exception takes a second,
      deliberate edit in the module beside the refusal. A baseline may be a
      strict SUPERSET, because removal is the one lawful direction. It binds
      the HOUSE register only: `--register PATH` serves the tests and a
      consuming tree, whose closure is that repository's own record. The
      requirement gains the enforcement sentence and a scenario. (c) **§ 4.9
      AND § 4.11 WERE DONE AND LEFT UNTICKED** — the bookkeeping defect is
      real and is corrected below, with the output each was ticked on.
- [x] 3.10 **THE BENCH'S THIRD ROUND, TWO THREADS, BOTH TAKEN, AND ONE OF THEM
      A REGRESSION § 3.7 INTRODUCED** (`design.md` D8c). (a) **THE RELEASE-ID
      SHAPE WAS NARROWER THAN THE ESTATE'S OWN.**
      `contracts/releases/release-digest-inventory.schema.yaml`
      `$defs.bundle_tag` defines a release tag as
      `^contract-v[0-9]+(?:\.[0-9]+){1,2}$` — two OR three components — and
      `RELEASE_ID_RE` admitted two only. While the shape was consulted only on
      the NO-REGISTRY branch this was latent; § 3.7 made the shape the first
      test in EVERY branch, so from that commit a three-component release with
      an inventory ON DISK would have been REFUSED by the gate. Measured: no
      three-component inventory exists today (**53** two-component inventories
      under `contracts/releases/`, counted with
      `ls contracts/releases/*.digests.yaml | wc -l` and agreeing with § 2's
      own 53), so the defect was latent and not standing —
      the next such cut would have found it at the gate. `RELEASE_ID_RE` is now
      the schema's pattern, restated rather than imported (the module must
      judge a tree with no `contracts/`), and
      `test_the_release_id_shape_is_the_estates_own` READS the schema and
      asserts the two are equal, so a drift is a test failure rather than a
      release refused. Four more cases: a three-component release resolving
      against a registry, its shape accepted with no registry, a
      FOUR-component name still refused, and a three-component declaration
      passing end to end. (b) **THE README ROW'S TEST FIGURE WAS STALE** — it
      still said 32 while `proposal.md` and § 3.5 had been re-measured to 46.
      Already corrected in `989c7059` and re-measured again here; the figure
      now moves in all three places in the same commit, every time, which is
      § 3.8's whole point.
- [x] 3.11 **THE BENCH'S FOURTH ROUND, FIVE THREADS, ALL FIVE TAKEN**
      (`design.md` D8d). (a) **THE SHAPE-ONLY FALLBACK CONTRADICTED THE
      REQUIREMENT'S OWN MUST** (two threads, the scenario and the code). The
      scenario said a release-shaped name the registry does not carry MUST be
      refused, while `resolves_as_release` accepts the SHAPE where the tree
      carries no registry at all — a deliberate, reasoned choice the module has
      always documented (a gate that refused every release name in a tree that
      cannot define one is unusable outside the repository that defines them)
      and one CANON DID NOT SAY. Of the bench's two options — fail closed, or
      encode the fallback — the fallback is ENCODED: the requirement gains the
      paragraph and the scenario *The scanned tree defines no release registry
      at all*, the existing scenario's MUST is qualified to a tree that HAS a
      registry, and the weaker judgment is required to be LOUD (the run already
      printed the note; two tests now pin that it prints with no registry and
      does NOT print with one). (b) **THE REPEAT GUARD WAS OVER-BROAD.**
      `_REPEATED_HEADER_RE` allowed leading whitespace, so an INDENTED gloss
      line reading `  target_release: the main line` — a CONTINUATION, not a
      declaration — was refused, contradicting "judge the token and never the
      gloss". Measured: that gloss WAS refused. The pattern is now anchored at
      column 0, which is the loader's own notion of a header line
      (`frontmatter_strict._TOP_LEVEL`), with a test for the indented gloss.
      (c) **THE PROPOSAL'S SCENARIO INVENTORY AND THE PULL-REQUEST DESCRIPTION
      WERE STALE** (two threads) — the proposal still said seven scenarios and
      the description still said 32 tests and seven scenarios. The description
      had already been rewritten before the threads were read; the proposal's
      inventory now names all TEN and marks which the bench added.
- [x] 3.12 **THE BENCH'S FIFTH ROUND, THREE THREADS, ALL THREE TAKEN, AND ONE OF
      THEM A FIGURE THIS BENCH ITSELF INVENTED** (`design.md` D8e). (a)
      **"47 INVENTORIES" WAS A NUMBER NOBODY COUNTED.** § 3.10's own account of
      the release-id fix asserted 47 two-component inventories under
      `contracts/releases/`. There are **53**, which is what § 2 and D3 had
      counted all along — the bench's own evidence line contradicted the
      packet's own measurement, in the very paragraph arguing that an
      unchecked restatement is a defect. Recounted here,
      `ls contracts/releases/*.digests.yaml | wc -l` → **53**. The conclusion
      is unchanged (all 53 are two-component, so the narrower regex refused
      nothing standing), which is exactly why the error survived a read: a
      number that does not change the conclusion is the easiest kind to get
      wrong and the least likely to be re-derived. (b) **THE PROPOSAL'S
      BEFORE/AFTER TABLE WAS NOT REPRODUCIBLE FROM ITS OWN COMMAND.** It read
      `before (this tree, pre-correction) 38 / 9` and `after 38 / 14` under
      `validate-target-release.py .`, but running that command HERE gave a
      different pair, because this packet's own `proposal.md` is an active
      change declaring `target_release: implemented` and is judged by its own
      gate like every other file. The rows are now labelled by TREE
      (`origin/main` vs THIS tree), so the `+1`/`+1` is explained as the
      packet's own proposal rather than silently absorbed, and the table says
      the two rows are the same validator pointed at two trees. (c) **A
      MISSING NEWLINE HID A TASK.** `- [x] 3.10` ran on from the end of
      § 3.9's paragraph above, so Markdown rendered the third bench round as
      prose inside the second rather than as its own checklist item —
      invisible to anyone reading the completion ledger as a list, which is
      how it is meant to be read. Split. Small, and worth recording: in a
      packet whose method is that the task list IS the record, a task that
      does not render as a task is a task that is not in the record.
- [x] 3.13 **A POST-FREEZE COPILOT PASS SUPPRESSED FIVE COMMENTS (0 NEW
      THREADS) AND ONE OF THEM WAS REAL: "FOUR" WAS ITSELF A MISCOUNT.**
      `proposal.md` and `design.md` D8d (j) both said the bot bench added
      FOUR scenarios to the inventory of TEN. Only THREE are actually marked
      in bold in `proposal.md`'s own inventory — *a tree that defines no
      release registry at all* (D8d), *a repeated declaration* (D8b) and
      *an entry appended to the closed register* (D8b) — because *a stale
      entry* (a register entry matches nothing) was part of the ORIGINAL
      seven, not bench-added. Both files corrected from FOUR to THREE, and
      the citation narrowed from `D8b/D8c/D8d` to `D8b/D8d` (D8c added no
      scenario). The pull-request description carried the same
      miscount and is corrected with it. **Not taken from this same pass:**
      a symlink-handling comment on `scripts/target_release.py:344`
      (`resolves_as_release`'s `Path.is_file()` follows symlinks, so a
      committed symlinked digest inventory would be treated as defined,
      unlike `scripts/hermes_runtime_validation/release.py:418-426`'s
      deliberate exclusion) — real, verified by reading the code, and left
      OPEN for a dedicated round: it is a code change with its own test and
      its own bench-round citation, not a count or a ledger entry, and this
      round's mandate is the latter only. (It did not stay open: the same
      finding reopened as a formal thread on the very next push and is TAKEN
      in § 3.14.)
- [x] 3.14 **THE BENCH'S SIXTH ROUND, ONE THREAD, TAKEN** (`design.md` D8f).
      The symlink-handling finding § 3.13 disclosed and declined to take
      reopened as a formal, unresolved thread (`PRRT_kwDOTAvnrs6hgEM5`) on
      push `378eb3c3`, which carried only the § 3.13 scenario-count fix — a
      real finding does not stop being real for having been named once
      already. `resolves_as_release` now refuses a candidate inventory that
      is a symlink, restating `scripts/hermes_runtime_validation/release.py`'s
      own guard (`target.is_file() and not target.is_symlink()`) rather than
      importing it or inventing a new one. THREE tests: a symlinked inventory
      does not resolve; one planted in a sibling tmpdir (pointing OUTSIDE the
      tree) does not resolve either; a REGULAR inventory beside a symlinked
      one for a DIFFERENT token still resolves (the refusal is per-candidate).
      Measured: with the fix stashed, all three FAIL against the code as it
      stood; restored, `pytest tests/target_release -q` — **65 passed**
      (62 → 65).
- [x] 3.15 **THE BENCH'S SEVENTH ROUND, ONE THREAD, TAKEN** (`design.md` D8g).
      `resolves_as_release` checked only the CANDIDATE FILE for symlink-ness
      (§ 3.14); it never checked the REGISTRY DIRECTORY itself, and
      `Path.is_dir()` follows symlinks the same way `Path.is_file()` does — so
      a committed `contracts/releases` DIRECTORY symlink, pointing anywhere
      outside this tree, resolved as a PRESENT registry, and a REGULAR file
      reached only THROUGH that symlinked parent is never itself a symlink,
      so the file-level guard § 3.14 added never saw anything to refuse. A
      new `_registry_present` helper checks the directory for symlink-ness
      once, and BOTH call sites that ask whether the registry is present
      (`resolves_as_release` and `scan`'s `Report.registry_present`) now use
      it, so the report can never say "present" where resolution itself
      treated the registry as absent. A symlinked directory is now treated
      exactly as a MISSING registry is: the shape-only fallback governs, and
      an inventory sitting behind the symlink — whether one is there or not —
      changes nothing. THREE tests: a symlinked registry directory resolves a
      release-shaped token on shape alone (`registry_present` False); an
      EMPTY symlinked directory and one holding a genuine, matching inventory
      resolve IDENTICALLY, proving the external file grants no extra trust;
      and the gate prints the same "accepted on its SHAPE alone" note for a
      symlinked directory that it prints for a tree with no registry at all.
      Measured: with the fix stashed, all three FAIL against the code as it
      stood; restored, `pytest tests/target_release -q` — **68 passed**
      (65 → 68). Validator re-run: this tree exit 0 (41 active, 17
      `implemented`, 3 release, 21 registered, 0 outside); `origin/main
      ac688c40` exit 1 (40 active, 5 outside, the same five carriers named).
- [x] 3.16 **THE BENCH'S EIGHTH ROUND, ON THE § 3.15 FIX'S OWN PUSH, TWO
      THREADS, BOTH TAKEN** (`design.md` D8h). Neither reopens D1/D2/D3's
      recommended option; both are stale prose. (a) **D3 STILL QUOTED THE
      PRE-D8c RELEASE-ID SHAPE** — `^contract-v\d+\.\d+$`, two components
      only — three rounds after D8c (§ 3.10) widened `RELEASE_ID_RE` to two OR
      three. D3 now quotes `^contract-v[0-9]+(?:\.[0-9]+){1,2}$`, names it
      `RELEASE_ID_RE`, and cites D8c. (b) **§ 4.1 AND `proposal.md`'S OWN
      BEFORE/AFTER TABLE HAD STOPPED MOVING**, pinned to `origin/main`
      `38c076d1` and a count several rounds stale, while `origin/main` itself
      had since moved twice more. Re-measured against a FRESH `origin/main
      ac688c40`: 40 active / 11 `implemented` / 5 outside there, 41 active /
      17 `implemented` / 0 outside on this tree. Both tables corrected, with
      the delta now explained IN FULL — `+1` active (this packet's own
      `proposal.md`) and `+6` `implemented` (that same `+1`, plus `+5` from
      the D2 sweep, which `origin/main` has not received). **The previous
      freeze's own prose (carried from D8e) is ALSO corrected in passing**:
      it described its own table's delta as "`+1`/`+1`" while the table it
      sat beside read 10 → 16 `implemented` — a `+6`, the same unnamed sweep
      contribution. Not a thread on this round; found while re-deriving the
      explanation this round's own correctness now requires. Neither item
      touches code, the register or a test; `pytest tests/target_release -q`
      unaffected (68 passed). `openspec validate
      gate-realization-axis-vocabulary --strict` exit 0;
      `validate-sequenced-after.py . --ledger-diff` exit 0 (202 rows).
- [x] 3.17 **THE BENCH'S NINTH ROUND, ON THE § 3.16 FIX'S OWN PUSH, TWO
      THREADS, BOTH TAKEN** (`design.md` D8i). (a) **THE LEAF-DIRECTORY GUARD
      § 3.15 ADDED CLOSED THE ESCAPE AT ONE COMPONENT AND LEFT EVERY ANCESTOR
      OPEN** — a committed `contracts/` symlink (one level above the registry
      directory itself) reaches the same escape through a `contracts/releases`
      that is a perfectly ordinary, unsymlinked path. `_registry_present` now
      compares the registry's fully RESOLVED real path against `repo_root`'s
      own resolved real path with the literal `contracts/releases` suffix
      appended — a per-path check that SUBSUMES the leaf-only check rather
      than sitting beside it, and catches a symlink at any component in
      between. `repo_root` itself is resolved on both sides, so its own
      symlink-ness is NOT mistaken for the escape (a test pins this boundary
      explicitly). THREE tests: a symlinked `contracts/` ancestor treated as
      absent; `repo_root` itself symlinked still resolves (not the escape);
      the two § 3.15 tests unchanged and still passing. Measured with the fix
      stashed: the ancestor test FAILS (`(True, True)`, the same
      over-trusting result one level down); restored, `pytest
      tests/target_release -q` — **70 passed** (68 → 70). (b) **A NEW TEST
      NAME CARRIED A TYPO** —
      `test_a_symlinked_registry_directorys_contents_grant_no_extra_trust` —
      renamed to
      `test_a_symlinked_registry_directory_contents_grant_no_extra_trust`; no
      other file cited the old name. `openspec validate
      gate-realization-axis-vocabulary --strict` exit 0;
      `validate-sequenced-after.py . --ledger-diff` exit 0 (202 rows);
      `validate-target-release.py .` exit 0 (41 active, 0 outside);
      `origin/main ac688c40` exit 1 (40 active, 5 outside, the same five
      carriers).

- [x] 3.18 **THE MERGE OF `origin/main` `1f068646`, AND THE SIXTH CARRIER IT
      BROUGHT WITH IT — D2's RULED SWEEP, MEASURED AT THE HEAD IT LANDS ON**
      (`design.md` D2a). The branch was CONFLICTING against `main` at the
      ruling; merged at `fb55c9e9`, README `## OpenSpec Records` resolved by
      hand (this packet's row kept at the head of Active changes, `main`'s
      `amend-kill-switch-to-declared-test-companion` row kept beneath it
      verbatim, no other row touched), the sequenced-after corpus ledger
      auto-merged with both sides' rows intact (204 rows, `--ledger-diff` exit 0). **The merge made
      the gate RED, which is the gate working:**
      `python3 scripts/validate-target-release.py .` exit 1 —
      *"41 active proposals, 41 declaring — 16 `implemented`, 3 a named
      release, 21 named by the register, 1 outside the vocabulary"*, naming
      the path
      `openspec/changes/amend-kill-switch-to-declared-test-companion/proposal.md`
      and the value `a` it carries, and
      `test_corpus_target_release_validates` failed with it (**1 failed, 69
      passed**). That packet landed on `main` with pull request #959 at
      2026-09-11T17:19:09Z, AFTER D2 was drafted against a corpus that did not
      contain it. Brett Heap's D2 ruling is **"Sweep in this PR"** — the
      corpus as it stands — so the sixth was swept here by the same one-token
      correction, `a` → `implemented` before the author's own gloss, carried
      verbatim after an em dash. Registering it instead was not available: the
      register is CLOSED by D1's ruled option ("Keep and gate"), an entry may
      be removed and never added. RE-MEASURED after: **exit 0** — *"41 active
      proposals, 41 declaring — 17 `implemented`, 3 a named release, 21 named
      by the register, 0 outside the vocabulary"*. FOUR tests added for the
      class the merge exposed (§ 3.5; `pytest tests/target_release -q` —
      **74 passed**, 70 → 74): the value token of a running sentence IS its
      first word (the article), the swept form reads as `implemented`, and the
      same two end to end — the prose declaration refused with the article
      named in the finding, its corrected form exit 0. The race is disclosed
      rather than closed (`design.md` D2a): a proposal landing on `main`
      before this packet merges can add a seventh, and the remedy is the same
      one-token correction, re-measured at that head.
- [x] 3.19 **THE BENCH'S TENTH ROUND, ONE MINUTE AFTER THE FREEZE AND
      ANSWERED ON THE RATIFIED HEAD: FOUR THREADS, ALL FOUR TAKEN**
      (`design.md` D8j). None reopens D1, D2 or D3. (a) and (b) were already
      answered by the ratification's own re-measurement and are named rather
      than quietly ticked: § 4.6's stale `39 active / 9 declaring` now reads
      **41 / 11**, and § 4.9's stale **200** rows now reads **204**, the figure
      `--ledger-diff` prints, with the seed's 200 named as the seed's.
      (c) **A REAL CODE ESCALATION, THE THIRD IN ITS FAMILY** — `_proposals`
      found active declarations with a bare `Path.is_file()`, which FOLLOWS
      SYMLINKS, so a committed `openspec/changes/<id>/proposal.md` symlink, an
      ordinary proposal inside a symlinked CHANGE DIRECTORY, or one under a
      symlinked `openspec/` was read, judged and counted as the scanned tree's
      own, with `declaration()` opening bytes outside `repo_root`; a DANGLING
      link removed a proposal from the corpus instead. D8g closed this for the
      registry's leaf and D8i at every ancestor; the discovery walk was the
      same surface, untested. A new `_unescaped` helper is D8i's test
      generalized — a path counts only when resolving every symlink between
      `repo_root` and it lands where a symlink-free tree would have put it,
      `repo_root` resolved on both sides — and `_proposals` takes EVERY path,
      active and archived, through it. FIVE tests (74 -> **79**); THREE
      measured FAILING with the fix stashed and passing restored (symlinked
      active proposal, regular proposal inside a symlinked change directory,
      symlinked ARCHIVED proposal), TWO pinned as BOUNDARIES that pass either
      way (a dangling link is skipped without crashing; a `repo_root` reached
      through a symlink still finds its proposals). On the real corpus the fix
      moves nothing — 41 active and 163 archived before and after — which is
      the point. (d) **THE PULL REQUEST DESCRIPTION** still reported 68 tests
      and stopped the bench at round 8; rebuilt on the ratified head with the
      ruling, the six-carrier sweep, this round and the re-measured counts,
      `refs #956, refs #931` kept and `closingIssuesReferences` re-verified
      `[]`. Re-validated at this fix: `openspec validate
      gate-realization-axis-vocabulary --strict` exit 0;
      `validate-target-release.py .` exit 0 (41 active, 17 `implemented`, 3 a
      named release, 21 registered, 0 outside); `pytest tests/target_release
      -q` **79 passed**; `validate-sequenced-after.py . --ledger-diff` exit 0
      (204 rows); `validate-scope-globs.py .` exit 0; `doc-health.py
      --single-repo .` exit 0.
- [x] 3.20 **THE SECOND MERGE OF `origin/main` (`5972c8f3`, pull request
      #1004), AND D2's SWEEP RE-MEASURED AT IT.** The branch went DIRTY again
      against `main` on the same one file as before — README `## OpenSpec
      Records`, where `main` added the
      `disposition-codexfactory-regular-pr-council-clearance-archive` row at
      the head of *Active changes*. Resolved by keeping BOTH rows, `main`'s
      FIRST and this packet's immediately after it, no other row touched and no
      reflow; the corpus ledger auto-merged to **205** rows. **D2's ruled
      sweep has NO SEVENTH CARRIER at this head**, and that is measured rather
      than assumed: the change `main` brought in declares `implemented`, so
      `validate-target-release.py .` reads **exit 0 — 42 active proposals, 42
      declaring, 18 `implemented`, 3 a named release, 21 named by the register,
      0 outside the vocabulary**, against **exit 1** on a fresh `origin/main`
      `5972c8f3` worktree (41 active, 11 `implemented`, 6 outside, the same six
      D2 corrects). Everything § 4 states was re-taken here: `openspec validate
      <change> --strict` exit 0; `--all --strict` exit 1 `101 passed, 3 failed
      (104)` against the control's `100 passed, 3 failed (103)`, the failure set
      IDENTICAL on both trees and its THIRD member arriving with this very merge
      (`disposition-codexfactory-regular-pr-council-clearance-archive`, which
      fails on `main` too and is not this packet's);
      `validate-sequenced-after.py .` exit 0 (42 active, 12 declaring) and
      `--ledger-diff` exit 0 (205 rows); `validate-scope-globs.py .` exit 0;
      `doc-health.py --single-repo .` exit 0; `proposal-support.py . verify`
      exit 0; `pytest tests/target_release -q` **79 passed**;
      `validate-openspec-cli-pin.py` both forms exit 0 (`1 passed, 0 failed`
      and, through the pinned 1.12.0, `102 passed, 2 failed (104)` — one item
      passing there that PATH 1.2.0 fails, a CLI-version difference and not a
      tree difference).
      `review/verification-2026-09-12.md` is the DATED capture of the ratified
      tree one merge earlier and is deliberately not rewritten for this; it
      points here instead.
- [x] 3.21 **THE BENCH'S TWELFTH ROUND, ON THE FREEZE PUSH (16:45Z): ONE
      THREAD, TAKEN** (`design.md` D8k). Does not reopen D1, D2 or D3.
      **A FOURTH MEMBER OF THE SAME SYMLINK-ESCAPE FAMILY** (Copilot thread
      `PRRT_kwDOTAvnrs6hx2WG`) — `load_register` read the register through a
      bare `path.is_file()` / `path.read_text()`, which FOLLOW SYMLINKS, so a
      committed symlink at the register path (the default beside this module,
      or one named on `--register`) would be read instead of refused. D8g,
      D8i and D8j each closed this for a different reader
      (`resolves_as_release`, `_registry_present`, `_proposals`); the register
      was the one left open. Fixed with a leaf-level `path.is_symlink()`
      guard, checked before `is_file()` / `read_text()` and unconditional on
      `path`, so the default argument and a caller-supplied one take the same
      guard. FIVE tests (79 -> **84**), all measured FAILING with the fix
      stashed and passing restored: a symlinked register; one pointing
      outside the tree; a dangling register symlink (refuses as a symlink,
      not a crash); the DEFAULT path specifically, via a
      `load_register.__defaults__` patch (a function default binds at
      definition time, so patching the module attribute alone would not
      reach a bare `load_register()` call); and the CLI (`--register`)
      surface, `exit 2`. On the real corpus the fix moves nothing —
      `validate-target-release.py .` still reads 42 active, 18
      `implemented`, 3 a named release, 21 registered, 0 outside — the house
      register is a regular file. Re-validated: `openspec validate
      gate-realization-axis-vocabulary --strict` exit 0; `pytest
      tests/target_release -q` **84 passed**; `validate-sequenced-after.py .
      --ledger-diff` exit 0 (205 rows); `validate-scope-globs.py .` exit 0;
      `doc-health.py --single-repo .` exit 0; `proposal-support.py . verify`
      exit 0; `validate-openspec-cli-pin.py --change
      gate-realization-axis-vocabulary` exit 0 (1 passed, 0 failed);
      `validate-openspec-cli-pin.py --all --no-cache` exit 0 (102 passed, 2
      failed (104), unchanged); PATH 1.2.0 `--all --strict` 101 passed, 3
      failed (104), unchanged; `pytest tests/doc-health -q` **7 failed, 1717
      passed, 1 skipped** — the same local-only, pre-existing set § 3.19
      measured, unmoved.
- [x] 3.22 **THE BENCH'S THIRTEENTH ROUND, ON THE § 3.21 PUSH (343af525): ONE
      THREAD, TAKEN** (`design.md` D8l). Does not reopen D1, D2 or D3. Copilot
      thread `PRRT_kwDOTAvnrs6hyDwH` (on `proposal.md`): § 3.21's own fix grew
      `tests/target_release/test_target_release_gate.py` from 79 to 84, but
      `proposal.md`'s `code_surface:` line still read **79 tests** — the
      summary was one round behind the code it describes. Measured on the
      flagged head: `grep -c '^def test_'` = 84; `pytest --collect-only`
      collects 84. Two places stated the stale total as a CURRENT figure and
      are corrected to 84: `proposal.md`'s `code_surface:` line (this
      thread's own anchor) and the README `## OpenSpec Records` row's own
      restatement of the same code surface. Left alone, deliberately: § 3.5,
      § 3.19, § 3.20 here and `design.md`'s D8j/D8k narrative all state a
      count as a DATED CHECKPOINT of what a specific round measured (74, then
      79, then 84) and are each true of their own moment, not a claim about
      the file's current total; `review/verification-2026-09-12.md` is the
      dated capture § 3.20 already says is deliberately not rewritten.
      Fix committed `34bc8cad`. `origin/main` moved twice while this round
      was answered — `a72f0a76` (#978, #998, #1005) then `177ba819` (#981) —
      and both were merged in ordinary bookkeeping merges (`db208513`,
      `32e57bd7`), README's `## OpenSpec Records` conflicting the same way
      each time: the newer active row kept FIRST, this packet's row
      immediately after, no reflow. Re-validated at each head: `openspec
      validate gate-realization-axis-vocabulary --strict` exit 0; `pytest
      tests/target_release -q` 84 passed throughout (prose-only, and then a
      merge-only change); `validate-target-release.py .` exit 0, growing
      from 42/18/0-outside to 45/21/0-outside as main's own admitted changes
      landed; `doc-health.py --single-repo .` exit 0.
- [x] 3.23 **THE BENCH'S FOURTEENTH ROUND, ON THE § 3.22 PUSH (32e57bd7): TWO
      THREADS, BOTH TAKEN** (`design.md` D8m). Does not reopen D1, D2 or D3.
      (a) **A FIFTH MEMBER OF THE SAME SYMLINK-ESCAPE FAMILY, AND THE FIRST
      IN THE ANCESTOR DIMENSION FOR THE REGISTER** (Copilot thread
      `PRRT_kwDOTAvnrs6hyYeC`, on `scripts/target_release.py`): § 3.21's
      leaf-level `path.is_symlink()` guard covers only `load_register`'s own
      name. `linkdir/register.yaml`, where `linkdir` is a symlink to an
      external directory, has an entirely ORDINARY leaf, so the guard passed
      it and `read_text()` still followed `linkdir`. A new
      `_has_symlinked_ancestor` helper climbs `path`'s own ancestors —
      without a `repo_root` to anchor it the way `_unescaped` has one,
      because a register named on `--register` is deliberately allowed to
      live anywhere (`load_register`'s own docstring) — and `load_register`
      now refuses on `path.is_symlink() or _has_symlinked_ancestor(path)`.
      TWO tests (84 -> **86**), both measured FAILING with the fix stashed
      and passing restored: the direct call, and the CLI (`--register`) end
      to end. On the real corpus the fix moves nothing — the house register
      sits directly beside this module with no symlinked ancestor either.
      (b) **THE PULL REQUEST'S OWN DESCRIPTION, A THIRD TIME** (Copilot
      thread `PRRT_kwDOTAvnrs6hybFv`, on `README.md`, but naming the PR body
      directly): the live description still reported 70 tests in its
      implementation summary and 79 passed in later verification, both
      behind the committed 86. Rebuilt on this head with the current
      figures; `refs #956` kept, `closingIssuesReferences` re-verified `[]`.
      Re-validated: `openspec validate gate-realization-axis-vocabulary
      --strict` exit 0; `pytest tests/target_release -q` **86 passed**;
      `validate-target-release.py .` exit 0 (45 active, 45 declaring, 21
      `implemented`, 3 a named release, 21 registered, 0 outside, unchanged —
      an I/O-boundary-only fix); `validate-sequenced-after.py . --ledger-diff`
      exit 0 (208 rows); `validate-scope-globs.py .` exit 0; `doc-health.py
      --single-repo .` exit 0; `proposal-support.py . verify` exit 0;
      `validate-openspec-cli-pin.py --change gate-realization-axis-vocabulary`
      exit 0 (1 passed, 0 failed); `--all --no-cache` exit 0 (102 passed, 2
      failed (104), the two known `disposition-codexfactory-*` exceptions,
      unchanged).

## 4. Verification — DONE IN THIS PULL REQUEST

**EVERY LINE BELOW IS A COMMAND THAT WAS RUN ON THIS TREE**, with its exit code
and its own output quoted.

- [x] 4.1 **THE VALIDATOR, BEFORE AND AFTER, ON THE REAL CORPUS — RE-RECORDED
      AGAINST THE TREE AS IT NOW STANDS (Copilot round 7, thread
      `PRRT_kwDOTAvnrs6hhb5a`; a prior version of this task pinned the
      "before" tree to `origin/main` `38c076d1` and the "after" figures to an
      earlier commit's count, both stale the moment either tree moved — the
      REMEDY IS NOT TO FREEZE A SHA HERE BUT TO RE-MEASURE AT EACH
      RE-RECORDING, which this entry now does).** RE-MEASURED AT THE CURRENT
      HEAD, on the merge of `origin/main` `5972c8f3` (§ 3.20). Before: **exit 1**
      against a fresh `origin/main` `5972c8f3` worktree — *"41 active
      proposals, 41 declaring — 11 `implemented`, 3 a named release, 21 named
      by the register, 6 outside the vocabulary"*, the six named by path (the
      same six D2 corrects, `design.md` D2a). After, on THIS tree at its own
      head: **exit 0** — *"42 active proposals, 42 declaring — 18
      `implemented`, 3 a named release, 21 named by the register, 0 outside
      the vocabulary"*, with *"archive (read, never judged): 163 proposals, 61
      of them outside the vocabulary"* on both sides. Both runs are the SAME
      validator pointed at two trees, so the only difference between them is
      the tree. The `+1` active is this packet's own `proposal.md`
      (`implemented`); the `+7` `implemented` is that same `+1` plus the `+6`
      from the sweep (D2, D2a) — `origin/main` never received it, so the six
      carriers still count `refused` there. The earlier capture in
      `review/verification-2026-09-12.md` § 4 is the same pair taken one merge
      earlier (`1f068646`: 40/10/6 there, 41/17/0 here) and is left as the
      dated capture it is.
- [x] 4.2 `OPENSPEC_TELEMETRY=0 openspec validate
      gate-realization-axis-vocabulary --strict` (PATH CLI **1.2.0**) —
      **exit 0**, *"Change 'gate-realization-axis-vocabulary' is valid"*.
- [x] 4.3 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — **exit 1**,
      `Totals: 101 passed, 3 failed (104 items)`. The failure set is IDENTICAL
      to `origin/main` `5972c8f3`'s, taken in the same shell from a worktree of
      it (`Totals: 100 passed, 3 failed (103 items)`):
      `change/disposition-codexfactory-declared-renames`,
      `change/disposition-codexfactory-floor-relocation-retitle` and
      `change/disposition-codexfactory-regular-pr-council-clearance-archive`,
      the third arriving with the merge of `5972c8f3` (§ 3.20) and failing on
      BOTH trees alike. This change is in neither set and the item count moves
      by exactly one.
- [x] 4.4 **THROUGH THE PINNED CLI, WHICH IS THE ONE THE GATE RUNS.**
      `python3 scripts/validate-openspec-cli-pin.py --change
      gate-realization-axis-vocabulary --no-cache` — **exit 0**,
      `@fission-ai/openspec@1.12.0` verified against its content address, its
      80-package closure installed with `npm ci --ignore-scripts`,
      `Totals: 1 passed, 0 failed (1 items)`. The gate's literal
      `--all --no-cache` — **exit 0**, `Totals: 102 passed, 2 failed (104
      items)` — the PINNED 1.12.0's own reading, which differs from the PATH
      1.2.0 run in § 4.3 by one item passing rather than failing, and the
      difference is the CLI VERSION and not the tree — *"every target validated
      --strict with 0 UNDISPOSITIONED
      failures"*, the two being the PRE-EXISTING accepted exceptions
      `add-chain-attestation` and `add-composed-view-authoring`, neither of
      them this change.
- [x] 4.5 `python3 scripts/proposal-support.py . verify
      gate-realization-axis-vocabulary` — **exit 0**, *"proposal support
      verification ok"*.
- [x] 4.6 `python3 scripts/validate-sequenced-after.py .` — **exit 0**,
      *"42 active changes, 12 declaring the field"*, both archive-date arms
      passing (re-measured at the current head, § 3.20).
- [x] 4.7 `python3 scripts/validate-scope-globs.py .` — **exit 0**,
      *"scope_globs validation passed (all active changes conform)"*.
- [x] 4.8 `python3 scripts/doc-health.py --single-repo .` — **exit 0** on this
      tree and on the `origin/main` worktree alike.
- [x] 4.9 **THE PER-CHANGE SWEEP LEDGER ROW**, seeded by the sanctioned tool and
      never hand-written: `python3 scripts/validate-sequenced-after.py .
      --seed-ledger --moved-by '#<PR>'`, run after the draft pull request
      exists because the tool stamps `moved_by` with its number. Before the
      seed `--ledger-diff` reports *"per-change sweep ledger STALE (8
      finding(s))"* — one `missing row` and seven derived-total mismatches,
      each moving by exactly one. SEEDED in `13ff6162` with
      `--seed-ledger --moved-by '#963'`; after it, `python3
      scripts/validate-sequenced-after.py . --ledger-diff` — **exit 0**,
      *"per-change sweep ledger consistent with the corpus (205 rows)"* at the
      current head (200 at the seed; the merges of `origin/main` `1f068646` and
      `5972c8f3` brought the rest), with
      *"prose `Sequenced-after:` headers: 3 (3 archived)"* and *"DEEPEST
      DECLARED CHAIN RESOLVED: 4 hop(s)"*. Re-run on the tree as it now stands
      and still **exit 0**. (Ticked on the bench's word: the work landed in
      `13ff6162` and the box was left open — Copilot round 2, thread
      `PRRT_kwDOTAvnrs6heTQZ`.)
- [x] 4.10 **THE FULL SUITE — DONE AND LEFT UNTICKED AT RATIFICATION, THE SAME
      BOOKKEEPING DEFECT § 3.9(c) NAMES FOR § 4.9 AND § 4.11, CORRECTED HERE ON
      THE RECORD (tick-on-the-recording, Brett Heap's ruling of 2026-09-06T23:10Z)
      RATHER THAN RE-RUN, BECAUSE THE REQUIRED GATE ALREADY RAN IT ON EXACTLY
      THESE TWO TREES.** BEFORE — `main` at `f663b379` (this packet's branch's
      merge-base, the tip immediately preceding the merge below), required
      `pytest-suite` run
      [34711691612](https://github.com/opensoft/openxFactory/actions/runs/34711691612),
      **success**: *"7009 passed, 6 skipped, 338 deselected, 9 warnings, 175
      subtests passed"* (`selected=7190 passed=7184 skipped=6 failures=0
      errors=0`). AFTER — `main` at the merge itself, `68ff88b4`, required
      `pytest-suite` run
      [34713047890](https://github.com/opensoft/openxFactory/actions/runs/34713047890)
      (the same run § 5.1 cites as realization evidence), **success**: *"7095
      passed, 6 skipped, 338 deselected, 9 warnings, 176 subtests passed"*
      (`selected=7277 passed=7271 skipped=6 failures=0 errors=0`). **THE
      DELTA IS THIS PACKET'S OWN NET ADDITION**, since `f663b379` is the
      merge's own first parent: **+87** selected, **+87** passed, **+1**
      subtest, **0** new skips, **0** failures either side. THE NEW-TEST COUNT
      MEASURED LAST, directly on this packet's own file: `pytest --collect-only
      -q tests/target_release` on this archive tree collects **86** tests
      (`grep -c '^def test_' tests/target_release/test_target_release_gate.py`
      agrees), the figure `design.md` D8m and this pull request's own body
      already carry; the one-test difference between that figure and the
      repo-wide +87 delta is not reconciled further here (a repo-wide count
      also reflects fixture/parametrization shifts outside this packet's own
      file, and the required gate's PASS is the fact this box asks for, not a
      line-by-line reconciliation of two different counting grains).
- [x] 4.11 **README `## OpenSpec Records` ACTIVE ROW**, in house style, MOVED
      TO THE RATIFIED STANDING BY THIS RATIFICATION (all three ruled labels
      verbatim, the recording comment linked, the sweep's six carriers, and the
      archive named as the separate act where #956 closes). It first landed in
      `13ff6162` at `README.md` under *Active
      changes* at the draft standing: the draft standing named outright
      (**`Status: draft` — NOT RATIFIED**), the commissioning word quoted, the ADDED-only shape and the
      absence of a `sequenced_after` hold, the D0 measurement, the code and its
      test count, and the three declared veto points. Its test figure was
      RE-MEASURED after § 3.7 and § 3.9 rather than carried (**54**), which is
      the only edit this round makes to it. (Ticked on the bench's word — the
      row was in the diff while the box said owed: Copilot round 2, thread
      `PRRT_kwDOTAvnrs6heTQZ`.)
- [x] 4.12 **THE BOT BENCH — DONE AND LEFT UNTICKED AT RATIFICATION, THE SAME
      BOOKKEEPING DEFECT AS § 4.10, CORRECTED HERE ON THE RECORD.** Taken and
      dispositioned item by item across eleven rounds (`design.md` D8 through
      D8m; `tasks.md` § 3.7–§ 3.23), all Copilot — Codex was requested once
      (2026-09-11T12:43:28Z, PR #963 comment `5634604106`) and replied ABSENCE
      (usage limit) eight seconds later, recorded verbatim in
      `review/ratification-2026-09-12.md` § 7, no second request made. FROZEN
      at head `1d08089a` with **36 threads total, 0 unresolved**: FREEZE
      comment
      [issuecomment-5648023802](https://github.com/opensoft/openxFactory/pull/963#issuecomment-5648023802),
      re-verified through GraphQL immediately before that FREEZE and not
      contradicted by anything after it (this packet's ratification pull
      request merged **2 minutes 18 seconds** later, 19:01:29Z to
      2026-09-12T19:03:47Z, at unchanged head `1d08089a` as `68ff88b4`).

## 5. Archive — OWED, NOT GIVEN

**DISPOSITION 2026-09-12 — THE HEADING ABOVE IS RETAINED AS HISTORICAL SURFACE,
NOT SUPERSEDED.** *"OWED, NOT GIVEN"* was true from ratification
(2026-09-12T15:45:19Z) until **2026-09-12T22:25:43Z**, when Brett Heap gave the
separate word this section waits on, verbatim **"archive both"** (this packet
and `report-stale-grandfather-dispositions`), recorded on PR #963 at
[issuecomment-5649094500](https://github.com/opensoft/openxFactory/pull/963#issuecomment-5649094500)
and mirrored on this issue (openxFactory #956) at
[issuecomment-5649094591](https://github.com/opensoft/openxFactory/issues/956#issuecomment-5649094591).
The word was given AFTER the realization evidence already existed (the reverse
order from the `amend-merged-into-empty-tail-standing` sibling's own archive,
where the word came first and the landing followed four hours later) — this
packet's own ratification pull request #963 had already merged and its own
`pytest-suite` run had already gone green seven hours before Brett Heap spoke.

- [x] 5.1 **PROMOTE THE ADDED REQUIREMENT INTO CANON**, byte-for-byte, DONE IN
      ARCHIVE PULL REQUEST [#1014](https://github.com/opensoft/openxFactory/pull/1014),
      on the separate archive word above.
      **REALIZATION EVIDENCE (*Realization archive gate*, a NON-EMPTY code
      surface — this packet is a house validator and a closed register, not a
      doc-only change):** this packet's OWN ratification pull request
      [#963](https://github.com/opensoft/openxFactory/pull/963) merged into
      `main` as **`68ff88b4091ece46f0ad269643aa316924aa8c65`** at
      **2026-09-12T19:03:47Z** (LANDED comment
      [issuecomment-5648037759](https://github.com/opensoft/openxFactory/pull/963#issuecomment-5648037759)),
      and `main`'s OWN `pytest-suite` run AT THAT EXACT TREE — run
      [34713047890](https://github.com/opensoft/openxFactory/actions/runs/34713047890),
      `headSha` **`68ff88b4091ece46f0ad269643aa316924aa8c65`** (byte-identical
      to the merge commit itself — **a DECIDED run at the tree the merge
      carries, so no tree-equality argument is owed**), `conclusion`
      **success**, created 2026-09-12T19:03:52Z, completed 2026-09-12T19:23:11Z.
      Performed with `TZ=UTC python3 scripts/proposal-support.py . archive
      gate-realization-axis-vocabulary --date <UTC day of the act> --yes`
      through the pinned `@fission-ai/openspec@1.12.0` artifact — never a bare
      `openspec archive` — moving the packet to
      `openspec/changes/archive/<date>-gate-realization-axis-vocabulary/` and
      writing the `## ADDED Requirements` block (*Realization axis vocabulary
      is gated*) into `openspec/specs/release-realization/spec.md`. The
      origin-retention gate fires INSIDE the wrapper; its output, the
      byte-identity of the promoted block against this delta (sizes, sha256
      both sides), and the rename-purity proof are measured and recorded in
      the archive pull request's own body rather than repeated here.
      **THE RATIFIED BODY OF THIS BOX, CARRIED VERBATIM:**
      **PROMOTE THE ADDED REQUIREMENT INTO CANON**, byte-for-byte, in a
      SEPARATE pull request on a separate word, after § 1 is ruled and after
      the realization evidence this packet's `target_release` names: this pull
      request merged into `main` and a green `pytest-suite` run at the tree
      that merge carries — *"its code merged on the implemented target through
      the owning domain's engineering gates, and — where the surface is
      runnable — a green run of that surface"* (*Realization archive gate*).
- [x] 5.2 **THE ORIGIN ISSUE IS CLOSED AT THE ARCHIVE PULL REQUEST AND NOWHERE
      ELSE.** This packet's own ratification pull request (#963)'s
      `closingIssuesReferences` was `[]` throughout and at merge (recorded
      `review/ratification-2026-09-12.md` § 6 and re-verified before this
      archive branch was cut); THIS archive pull request,
      [#1014](https://github.com/opensoft/openxFactory/pull/1014), carries the
      single `Closes #956` line in its body and its `closingIssuesReferences`
      is verified through GraphQL to be exactly `[956]`. **NO COMMIT MESSAGE ON THIS ARCHIVE BRANCH CARRIES A CLOSING
      KEYWORD IN ANY FORM** — not `Closes`, `Fixes` or `Resolves`, in any case
      or tense, quoted or unquoted — checked with a compound regex over every
      commit message on the branch and recorded in the pull request body.
      **THE RATIFIED BODY OF THIS BOX, CARRIED VERBATIM:**
      **THE ORIGIN ISSUE IS CLOSED AT THE ARCHIVE PULL REQUEST AND NOWHERE
      ELSE**, by a closing keyword written THERE against openxFactory issue
      956. No closing keyword appears in this pull request's body or in any
      commit message on this branch, in any form, quoted or otherwise.

## 6. Measured, and deliberately NOT taken here

**DISPOSITION 2026-09-12 — THE HEADING ABOVE IS RETAINED AND NOTHING IN THIS
SECTION IS TAKEN AT THIS ARCHIVE.** All five boxes tick, on Brett Heap's ruling
of 2026-09-06T23:10Z, option labelled verbatim *"Tick on the recording"* (his
#900 ruling on a conditional tick trigger): each tick records either a
MEASUREMENT RE-TAKEN on the archive tree, with any figure that moved
disclosed at the box, or the NAMING of a successor and never its doing.
**TWO SUCCESSORS ARE OWED. ONE IS ALREADY NAMED IN THIS PACKET'S OWN RATIFIED
RECORD** (`add-structured-scope-substrate`, for § 6.1 and § 6.2, both
amendments to the SAME ratified requirement title and therefore the same
sequencing slot); **ONE HAS NO EXISTING NAME AND IS FILED HERE, UNCLAIMED:**
openxFactory [#1013](https://github.com/opensoft/openxFactory/issues/1013)
for § 6.3, filed after a sibling search (by title/body over open and closed
issues, and by grep over the active and archived corpus) found no existing
issue or packet proposing to gate `code_surface:`. § 6.4 and § 6.5 owe no
successor and none is filed for them — each is a boundary the box's own
ratified text already draws (a frozen record; another repository's own act).

- [x] 6.1 **NOT TAKEN — A SUCCESSOR IS ALREADY NAMED IN THIS PACKET'S OWN
      RATIFIED RECORD, AND NOTHING IS EDITED.** `openspec/changes/add-structured-scope-substrate/`
      is ACTIVE (not archived) and `Status: ratified`, unchanged since this
      packet's own `.openspec.yaml` `related:` block named it at ratification
      as the change that *"Holds the `## MODIFIED` block over Realization axis
      declaration that an amending design would have to sequence after"* — this
      is re-verified on the archive tree rather than carried: `git log -1
      --format=%h -- openspec/changes/add-structured-scope-substrate/proposal.md`
      confirms it has not moved to `archive/`, and its own
      `specs/release-realization/spec.md` still opens *"code_surface: and
      target_release: are UNCHANGED"* and restates the promoted two-value
      sentence verbatim — it holds the sequencing slot and does NOT itself
      answer § 6.1, exactly as this packet's design.md D7 and ratification
      record § 8.4 already say. **THE REGISTER'S DEFERRED-ALLOCATION COUNT IS
      RE-MEASURED, NOT CARRIED:** `grep -c "class: deferred-allocation"
      scripts/target-release-register.yaml` still returns **12** on the
      archive tree — unchanged from ratification. Answering § 6.1 remains a
      `## MODIFIED` block over *Realization axis declaration*, sequenced after
      `add-structured-scope-substrate`, and it is not authored here.
      **THE RATIFIED BODY OF THIS BOX, CARRIED VERBATIM:**
      **WHETHER CANON ADMITS A DEFERRED ALLOCATION.** Twelve active packets
      need a spelling the two-value sentence does not have, and the versioning
      policy is why. It is a `## MODIFIED` block over the title
      `add-structured-scope-substrate` holds, with the sequencing hold that
      carries. The register's twelve `deferred-allocation` entries all retire
      on it.
- [x] 6.2 **NOT TAKEN — THE SAME NAMED SUCCESSOR, RE-CONFIRMED.** Same target
      as § 6.1 (`add-structured-scope-substrate`, re-verified ACTIVE and
      ratified above, holding the same `## MODIFIED` block over the same
      contested title) — a wording repair to the *"aggregation repository"*
      phrase is another amendment to that same requirement, and would
      naturally land in the SAME future `## MODIFIED` block as § 6.1's remedy
      rather than a second one, since both correct the identical sentence.
      Not repaired here: this archive pull request edits no prose under
      `openspec/specs/release-realization/spec.md` except to ADD the new
      requirement this packet's own § 1 ratified; the existing *"Realization
      axis declaration"* requirement is untouched.
      **THE RATIFIED BODY OF THIS BOX, CARRIED VERBATIM:**
      **THE "AGGREGATION REPOSITORY" WORDING.** Canon resolves a named release
      against a repository that defines none. A wording repair is another
      MODIFIED block over the same contested title.
- [x] 6.3 **NOT TAKEN — NO SUCCESSOR WAS NAMED ANYWHERE IN THIS PACKET, SO ONE
      IS FILED HERE, UNCLAIMED.** openxFactory
      [#1013](https://github.com/opensoft/openxFactory/issues/1013), filed for
      this archive pull request, naming the gap and a re-measurement taken on
      this archive tree (method: a `^code_surface:` front-matter line over
      every `openspec/changes/*/proposal.md`, so it reproduces): **45** active
      proposals, **45** declaring `code_surface:` — **5** `none`, **40** a
      non-`none` value (free prose, no enumerable schema) — and no validator
      anywhere checks its shape or vocabulary. A sibling search preceded the
      filing: by title and body over every open and closed issue for
      `code_surface`, and by grep over the active and archived corpus for a
      packet proposing to gate it; neither returned an existing name, which is
      why a new issue and not an existing one is cited.
      **THE RATIFIED BODY OF THIS BOX, CARRIED VERBATIM:**
      **`code_surface:` IS NOT GATED.** The other half of the same sentence is
      equally unread; it is a second population with its own classes, and
      folding it in here would widen a ruled remedy into an unruled sweep.
- [x] 6.4 **NOT TAKEN, AND NOT OWED — RE-MEASURED ON THE ARCHIVE TREE.**
      `python3 scripts/validate-target-release.py .` reports *"archive (read,
      never judged): 164 proposals, 61 of them outside the vocabulary"* at
      this archive's tree — the ARCHIVED TOTAL has grown from the count at
      ratification (more packets archived in the interval), but the
      OFF-VOCABULARY COUNT is still exactly **61**: no packet archived since
      this one's ratification added a new off-vocabulary `target_release`
      declaration to the frozen record. The validator's own closed-register
      design reads and reports the archived population without judging it, and
      this archive pull request touches no file under `openspec/changes/archive/`
      other than this packet's own move.
      **THE RATIFIED BODY OF THIS BOX, CARRIED VERBATIM:**
      **THE ARCHIVED 61 ARE NOT TOUCHED.** Frozen record: read, counted, judged
      never.
- [x] 6.5 **NOT TAKEN, AND NOT OWED — NO ESTATE REPOSITORY OTHER THAN THIS ONE
      IS TOUCHED BY THIS ARCHIVE.** `scripts/target_release.py` and
      `scripts/validate-target-release.py` take a `REPO_ROOT` (default `.`)
      and this archive pull request runs and gates them only against
      `opensoft/openXFactory`; no other governed repository's corpus,
      register or CI is read, written or referenced by this act.
      **THE RATIFIED BODY OF THIS BOX, CARRIED VERBATIM:**
      **NO OTHER ESTATE REPOSITORY IS SWEPT OR REGISTERED.** The validator
      takes a `REPO_ROOT` and refuses a tree with no register rather than
      assuming an empty one; each repository's register would be its own act.
