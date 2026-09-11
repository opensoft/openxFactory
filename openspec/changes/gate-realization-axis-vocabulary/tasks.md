# Tasks: gate-realization-axis-vocabulary

Status: draft
Kind: tasks

`code_surface: openxFactory`, `target_release: implemented`. The realization
group is § 3 and it is IN THIS PULL REQUEST: the tasks are individually
executable, so under `release-realization`'s decomposition rule this packet
realizes through its own task list rather than through a feature DAG.

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in
this pull request or a measurement recorded verbatim in the pull request body
and reproducible from the commands named beside it.

**§ 1 (RATIFICATION) IS ENTIRELY OPEN AND IS BRETT HEAP'S ACT.** His word of
2026-09-11T12:08:24Z, verbatim **"land each when green, archive both when
landed, claim 955 and 956"**, commissioned the AUTHORING of this packet and
decided no wording; it is recorded as the origin in `.openspec.yaml` and is not
read as an approval. `.openspec.yaml` carries drafting provenance with **no
approval pair**, and every document here carries `Status: draft`.

**§ 5 (ARCHIVE) IS ENTIRELY OPEN.** `code_surface` is non-empty, so the archive
is a separate act on merged-plus-green realization evidence and a separate word,
and openxFactory #956 closes THERE and not at this landing.

**§ 6 IS UNTICKED ON PURPOSE**: residue, measured and deliberately not taken.

## 1. Ratification — OWED, NOT GIVEN

- [ ] 1.1 **RATIFY OR REFUSE THE PACKET.** Brett Heap (openxFactory operator
      authority) rules on this packet itself. Until he does, no requirement
      here is approved, `Status: draft` stands on every document, and
      `.openspec.yaml` declares `proposed_by`/`proposed_on` with no
      `approved_by`/`approved_on` — the shape `add-drafted-proposal-origin`
      (issue #318) added for exactly this state.
- [ ] 1.2 **RULE `design.md` D1 — WHAT CANON DOES ABOUT A VALUE OUTSIDE ITS
      VOCABULARY.** Option 1, GATE the two-value vocabulary as ratified by
      ADDING one requirement plus a closed register (recommended); option 2,
      AMEND *Realization axis declaration* to admit the divergence; option 3,
      RULE the value a synonym. The cost of 2 and 3 is the same and is stated
      in D1: both are `## MODIFIED` blocks over a title the ACTIVE ratified
      `add-structured-scope-substrate` already modifies, so both owe
      `sequenced_after: [add-structured-scope-substrate]`, a pre-text taken
      from that change rather than from canon, and its archive-order hold.
      Option 3 additionally does not reach its own subject: all five active
      `none` carriers declare a NON-EMPTY `code_surface`.
- [ ] 1.3 **RULE `design.md` D2 — THE SWEEP.** Option 1, this pull request
      corrects the five `none` carriers, one value token each with every gloss
      preserved (recommended); option 2, each owning lane corrects its own and
      the gate lands ADVISORY until the last is done; option 3, correct nothing
      and register all 26. A veto of D2 option 1 reverts five one-token lines
      and adds five register entries; nothing else in the packet depends on it.
- [ ] 1.4 **RULE `design.md` D3 — HOW THE GATE RESOLVES "A NAMED RELEASE".**
      Option 1, resolve against `contracts/releases/` — the registry that
      exists (recommended); option 2, resolve literally against the aggregation
      repository, which defines no releases and carries no tags, so nothing
      resolves; option 3, accept any release-SHAPED token, which stops
      distinguishing a release from a wish.
- [ ] 1.5 **D0 AND D4 THROUGH D7 ARE CARRIED BESIDE THEM**, each with its
      alternative written out, and any of them may be vetoed in the same
      ruling: D0 (the measurement), D4 (the code surface, the three exit codes,
      and the register's home outside `contracts/`), D5 (why an OpenSpec change
      and not a patch), D6 (sequencing and the sibling search), D7 (what is not
      taken).

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
- [x] 3.4 **THE FIVE `none` CARRIERS CORRECTED** — one value token per file,
      every prose gloss preserved verbatim, five files and five lines in all:
      `add-composed-view-authoring`, `add-cpc-clearing-boundary`,
      `add-lens-document-selection`, `add-substantive-review-lane`,
      `register-gate-rules-council-seats`. The custody check is in `design.md`
      D2: `record-immutability` binds `Status: record` documents only, and
      neither *Origin retention at archive* nor *Scope retention at archive*
      reaches `target_release:`.
- [x] 3.5 `tests/target_release/test_target_release_gate.py` (NEW, **62 tests**,
      counted last from a collected run of the file) — the token rule (5),
      reading the declaration including a strict-loader refusal, **a
      repeated declaration refused rather than half-read, and an INDENTED
      gloss line that is a gloss and not a repeat** (8), release
      resolution with and without a registry, **including the estate schema's
      three-component form, the assertion that the shape IS the schema's, and
      the shape-only fallback saying so out loud** (10), **the token shape-checked
      before it can become a path (6)**, the register's shape refusals (4),
      **the entry's citation enforced at the load (5)**, **the same two classes
      swept (3)**, **the register removable and never addable (5)**, the gate
      end to end (13: the refusal, `implemented`, an
      archived record, a resolving release, a release name that resolves to
      nothing, an absent declaration, an empty declaration, an unreadable
      proposal reported not crashed, a registered declaration, a stale entry, a
      token that moved, a finding and a stale entry together, a missing
      register), and three over the live corpus and the real register. **NO
      EXISTING TEST IS EDITED, RENAMED, FLIPPED OR DELETED** — the fourteen
      added by § 3.7, the eight added by § 3.9, the five added by § 3.10 and
      the three added by § 3.11 join the file, `_entry()`
      gains the citation the loader now requires, and
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
      round's mandate is the latter only.

## 4. Verification — DONE IN THIS PULL REQUEST

**EVERY LINE BELOW IS A COMMAND THAT WAS RUN ON THIS TREE**, with its exit code
and its own output quoted.

- [x] 4.1 **THE VALIDATOR, BEFORE AND AFTER, ON THE REAL CORPUS.** Before the
      correction: **exit 1** — *"38 active proposals, 38 declaring — 9
      `implemented`, 3 a named release, 21 named by the register, 5 outside the
      vocabulary"*, the five named by path. After, RE-MEASURED ON THE TREE AS
      IT NOW STANDS (§ 3.7 landed, and this packet's own `proposal.md` is the
      39th active change and the 15th `implemented`): **exit 0** — *"39 active
      proposals, 39 declaring — 15 `implemented`, 3 a named release, 21 named
      by the register, 0 outside the vocabulary"*, with *"archive (read, never
      judged): 161 proposals, 61 of them outside the vocabulary"* on both
      sides. The before-run is the same validator pointed at an `origin/main`
      `38c076d1` checkout, so the only difference between the two runs is the
      tree.
- [x] 4.2 `OPENSPEC_TELEMETRY=0 openspec validate
      gate-realization-axis-vocabulary --strict` (PATH CLI **1.2.0**) —
      **exit 0**, *"Change 'gate-realization-axis-vocabulary' is valid"*.
- [x] 4.3 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — **exit 1**,
      `Totals: 99 passed, 2 failed (101 items)`. The failure set is IDENTICAL
      to `origin/main` `38c076d1`'s, taken in the same shell from a worktree of
      it (`Totals: 98 passed, 2 failed (100 items)`):
      `change/disposition-codexfactory-declared-renames` and
      `change/disposition-codexfactory-floor-relocation-retitle`. This change
      is in neither set and the item count moves by exactly one.
- [x] 4.4 **THROUGH THE PINNED CLI, WHICH IS THE ONE THE GATE RUNS.**
      `python3 scripts/validate-openspec-cli-pin.py --change
      gate-realization-axis-vocabulary --no-cache` — **exit 0**,
      `@fission-ai/openspec@1.12.0` verified against its content address, its
      80-package closure installed with `npm ci --ignore-scripts`,
      `Totals: 1 passed, 0 failed (1 items)`. The gate's literal
      `--all --no-cache` — **exit 0**, `Totals: 99 passed, 2 failed (101
      items)`, *"every target validated --strict with 0 UNDISPOSITIONED
      failures"*, the two being the PRE-EXISTING accepted exceptions
      `add-chain-attestation` and `add-composed-view-authoring`, neither of
      them this change.
- [x] 4.5 `python3 scripts/proposal-support.py . verify
      gate-realization-axis-vocabulary` — **exit 0**, *"proposal support
      verification ok"*.
- [x] 4.6 `python3 scripts/validate-sequenced-after.py .` — **exit 0**,
      *"39 active changes, 9 declaring the field"*, both archive-date arms
      passing.
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
      *"per-change sweep ledger consistent with the corpus (200 rows)"*, with
      *"prose `Sequenced-after:` headers: 3 (3 archived)"* and *"DEEPEST
      DECLARED CHAIN RESOLVED: 4 hop(s)"*. Re-run on the tree as it now stands
      and still **exit 0**. (Ticked on the bench's word: the work landed in
      `13ff6162` and the box was left open — Copilot round 2, thread
      `PRRT_kwDOTAvnrs6heTQZ`.)
- [ ] 4.10 **THE FULL SUITE**, `python3 -m pytest tests/ -q -m "not postgres"`,
      with the count before and after and the new-test count measured last.
- [x] 4.11 **README `## OpenSpec Records` ACTIVE ROW**, in house style, at the
      DRAFT standing. Landed in `13ff6162` at `README.md` under *Active
      changes*: the draft standing named outright (**`Status: draft` — NOT
      RATIFIED**), the commissioning word quoted, the ADDED-only shape and the
      absence of a `sequenced_after` hold, the D0 measurement, the code and its
      test count, and the three declared veto points. Its test figure was
      RE-MEASURED after § 3.7 and § 3.9 rather than carried (**54**), which is
      the only edit this round makes to it. (Ticked on the bench's word — the
      row was in the diff while the box said owed: Copilot round 2, thread
      `PRRT_kwDOTAvnrs6heTQZ`.)
- [ ] 4.12 **THE BOT BENCH**, taken and dispositioned item by item on the
      record.

## 5. Archive — OWED, NOT GIVEN

- [ ] 5.1 **PROMOTE THE ADDED REQUIREMENT INTO CANON**, byte-for-byte, in a
      SEPARATE pull request on a separate word, after § 1 is ruled and after
      the realization evidence this packet's `target_release` names: this pull
      request merged into `main` and a green `pytest-suite` run at the tree
      that merge carries — *"its code merged on the implemented target through
      the owning domain's engineering gates, and — where the surface is
      runnable — a green run of that surface"* (*Realization archive gate*).
- [ ] 5.2 **THE ORIGIN ISSUE IS CLOSED AT THE ARCHIVE PULL REQUEST AND NOWHERE
      ELSE**, by a closing keyword written THERE against openxFactory issue
      956. No closing keyword appears in this pull request's body or in any
      commit message on this branch, in any form, quoted or otherwise.

## 6. Measured, and deliberately NOT taken here

- [ ] 6.1 **WHETHER CANON ADMITS A DEFERRED ALLOCATION.** Twelve active packets
      need a spelling the two-value sentence does not have, and the versioning
      policy is why. It is a `## MODIFIED` block over the title
      `add-structured-scope-substrate` holds, with the sequencing hold that
      carries. The register's twelve `deferred-allocation` entries all retire
      on it.
- [ ] 6.2 **THE "AGGREGATION REPOSITORY" WORDING.** Canon resolves a named
      release against a repository that defines none. A wording repair is
      another MODIFIED block over the same contested title.
- [ ] 6.3 **`code_surface:` IS NOT GATED.** The other half of the same sentence
      is equally unread; it is a second population with its own classes, and
      folding it in here would widen a ruled remedy into an unruled sweep.
- [ ] 6.4 **THE ARCHIVED 61 ARE NOT TOUCHED.** Frozen record: read, counted,
      judged never.
- [ ] 6.5 **NO OTHER ESTATE REPOSITORY IS SWEPT OR REGISTERED.** The validator
      takes a `REPO_ROOT` and refuses a tree with no register rather than
      assuming an empty one; each repository's register would be its own act.
