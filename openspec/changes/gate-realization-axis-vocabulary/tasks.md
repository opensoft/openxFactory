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
- [x] 3.5 `tests/target_release/test_target_release_gate.py` (NEW, **46 tests**,
      counted last from a collected run of the file) — the token rule (5),
      reading the declaration including a strict-loader refusal (4), release
      resolution with and without a registry (3), **the token shape-checked
      before it can become a path (6)**, the register's shape refusals (4),
      **the entry's citation enforced at the load (5)**, **the same two classes
      swept (3)**, the gate end to end (13: the refusal, `implemented`, an
      archived record, a resolving release, a release name that resolves to
      nothing, an absent declaration, an empty declaration, an unreadable
      proposal reported not crashed, a registered declaration, a stale entry, a
      token that moved, a finding and a stale entry together, a missing
      register), and three over the live corpus and the real register. **NO
      EXISTING TEST IS EDITED, RENAMED, FLIPPED OR DELETED** — the fourteen
      added by § 3.7 join the file, `_entry()` gains the citation the loader now
      requires, and `test_an_entry_missing_a_required_key_refuses` keeps its
      subject by carrying every key but the one it is about.
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
      RE-MEASURED AFTER § 3.7 AND NOT CARRIED FORWARD.** `python3 -m pytest
      tests/target_release -q` — **exit 0**, *"46 passed in 6.10s"*; the
      per-section breakdown in § 3.5 is a count of `def test_` under each
      banner in the file, taken from the file itself.

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
- [ ] 4.9 **THE PER-CHANGE SWEEP LEDGER ROW**, seeded by the sanctioned tool and
      never hand-written: `python3 scripts/validate-sequenced-after.py .
      --seed-ledger --moved-by '#<PR>'`, run after the draft pull request
      exists because the tool stamps `moved_by` with its number. Before the
      seed `--ledger-diff` reports *"per-change sweep ledger STALE (8
      finding(s))"* — one `missing row` and seven derived-total mismatches,
      each moving by exactly one.
- [ ] 4.10 **THE FULL SUITE**, `python3 -m pytest tests/ -q -m "not postgres"`,
      with the count before and after and the new-test count measured last.
- [ ] 4.11 **README `## OpenSpec Records` ACTIVE ROW**, in house style, at the
      DRAFT standing.
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
