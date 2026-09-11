# Tasks: honour-grandfather-dispositions-in-ratified-provenance

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
2026-09-11, verbatim **"Commission the packet"**, commissioned the AUTHORING and
decided no wording; it is recorded as the origin in `.openspec.yaml` and is not
read as an approval. `.openspec.yaml` carries drafting provenance with **no
approval pair**, and every document here carries `Status: draft`.

**§ 6 (ARCHIVE) IS ENTIRELY OPEN.** `code_surface` is non-empty, so the archive
is a separate act on merged-plus-green realization evidence and a separate word,
and openxFactory #939 closes THERE and not at this landing.

**§ 7 IS UNTICKED ON PURPOSE**: residue, measured and deliberately not taken.

## 1. Ratification — OWED, NOT GIVEN

- [ ] 1.1 **RATIFY OR REFUSE THE PACKET.** Brett Heap (openxFactory operator
      authority) rules on this packet itself. Until he does, no requirement
      here is approved, `Status: draft` stands on every document, and
      `.openspec.yaml` declares `proposed_by`/`proposed_on` with no
      `approved_by`/`approved_on` — the shape `add-drafted-proposal-origin`
      (issue #318) added for exactly this state. Approval, when it comes, is a
      pure ADDITION beside a fixed `kind` and `id`.
- [ ] 1.2 **RULE `design.md` D1 — THE BAND.** `info` row carrying the citation
      (recommended) against SILENCE on the four siblings' precedent. Put with
      the recommendation first and the veto's cost written out: suppression is
      a smaller diff and matches four promoted requirements exactly; it costs
      the eighteen records their visibility, makes the grandfathered population
      uncountable from the report, and turns a stale entry into an invisible
      one. A veto of D1 moves ONE `THEN` bullet of the delta and one branch of
      `_honour_grandfather_dispositions`; nothing else in the packet depends
      on it.
- [ ] 1.3 **RULE `design.md` D2 — THE BOUNDARY.** ARCHIVED-only (recommended)
      against admitting an entry over an ACTIVE packet's record. A veto of D2
      costs the distinction between a ruling on something nobody may repair and
      a deferral of something somebody could fix this afternoon. D1 and D2 rest
      on no shared predicate; either stands whichever way the other goes.
- [ ] 1.4 **D0 AND D3 THROUGH D6 ARE CARRIED BESIDE THEM**, each with its
      alternative written out, and any of them may be vetoed in the same
      ruling: D0 (the measurement), D3 (the existing file, the existing key,
      the delegated admission rule, the bounded cite excerpt), D4 (`doc-health`
      is amended and `document-lifecycle` is NOT), D5 (the sibling search), D6
      (what is not taken).

## 2. The measurement, taken before the design

- [x] 2.1 **THE REAL AGGREGATION DISPOSITIONS FILE WAS READ, NOT MOCKED.**
      `opensoft/xFactory` @ `bc84d325` cloned beside this checkout, with
      `openxFactory` @ `96b4835b` and `codexFactory` @ `a67fb0ae` materialized
      under it so `corpus.discover_repos` enumerates exactly the two
      repositories the file names. **40 entries, 8 families, 18 of them
      `family: ratified-provenance`** — 15 `openxFactory`, 3 `codexFactory`,
      every one carrying a `date` and a non-empty `cite`, and every one naming a
      path under `openspec/changes/archive/`.
- [x] 2.2 **BEFORE: 41 rows, ALL `critical`.** `python3 scripts/doc-health.py
      --repo-root <aggregation> --family ratified-provenance --as-of 2026-09-10`
      — exit 0, *"Findings: 41 critical, 0 error, 0 warning, 0 info"*.
- [x] 2.3 **ALL EIGHTEEN DISPOSITION KEYS ARE LIVE ROWS TODAY**, so the
      remedy's population is eighteen and not fewer: `dispositioned AND
      currently reported: 18`, `dispositioned but NOT reported: 0`, and `of the
      hits, archived-path: 18, non-archived: 0`.
- [x] 2.4 **AFTER: 41 rows, 23 `critical` + 18 `info`**, the SAME 41
      `(repo, path)` keys. `rows whose severity moved: 18`; `rows byte-identical
      (severity+rule+action+class): 23`; `moved == disposition key set: True`;
      `all moved paths archived: True`. **THE WHOLE REPORT DIFF IS 74 LINES**:
      the eighteen findings in each of the TWO places the report renders them
      (`## Findings By Family` and `## Ranked Plan`, 36 lines a side) and the
      one headline that sums the bands. Nothing else moves, and the Ranked Plan
      keeps all 41 rows — an `info` row is re-banded there, not dropped.
- [x] 2.5 **THE SPLIT ACROSS THE FAMILY'S ARMS IS MEASURED**, which is why § 3
      is a LAST PASS rather than a branch inside one arm: 15 of the moved rows
      carry the SUBJECT-arm rule (#878's shape, all fifteen openxFactory) and 3
      carry *"ratified header carries no citation in either sanctioned
      spelling"* (all three codexFactory).
- [x] 2.6 **THE DOWNGRADED ROW SURVIVES THE REPORT GRAMMAR.**
      `report.unparsed_plan_rows` over the after-report returns `[]`, and
      `report.parse_previous` returns `23` keys and `0` contested — the eighteen
      leaving the regression axis (only `critical`/`error` rows enter `keys`)
      and entering no other (`uncited_resolutions` reads the `contested` set,
      which this `auto-fixable` family is never in).
- [x] 2.7 **`kind: ad_hoc` IS CHECKED RATHER THAN ASSUMED.**
      `ideation/staging/` enumerated (30 topic folders) and `INDEX.md` read on
      2026-09-11: no topic names doc-health severity policy, the disposition
      mechanism or ratification-record rules. `kind: staged` would claim a
      staging source that does not resolve.
- [x] 2.8 **NO SIBLING WRITES THIS REQUIREMENT** (`design.md` D5, pasted there
      in full): no open pull request touches `scripts/doc_health/` or
      `openspec/specs/doc-health/`; no active change other than this one carries
      a `## MODIFIED` block for *Governed corpus membership and the lifecycle
      scan set*; the two other active changes with a `specs/doc-health/` delta
      write different requirements.

## 3. The realization — one last pass, in this pull request

- [x] 3.1 `scripts/doc_health/families.py`: **`fam_ratified_provenance` RETURNS
      `_honour_grandfather_dispositions(ctx, findings)`.** That is the ONLY
      edit to the function's body — one `return` expression — so the five arms
      above it are byte-unmoved and every finding they build is unchanged unless
      it is one of the dispositioned archived rows.
- [x] 3.2 **THE ADMISSION RULE IS DELEGATED, NOT COPIED** (`design.md` D3).
      `_grandfather_cites` calls
      `promotion_fidelity.load_dispositions(ctx, _RATIFIED_PROVENANCE)` — the
      one reader promotion fidelity, duplicate packet and modified-block
      currency already share — for the key set, and re-reads the file only for
      the citation TEXT that reader does not return. `families.py` already
      imports `promotion_fidelity`; `promotion_fidelity` imports nothing from
      `families`, so no dependency is added and no cycle is created.
      **THE RE-READ APPLIES THREE PREDICATES OF ITS OWN AND ALL THREE ONLY
      NARROW** (two added in the § 5.10 review round and one in § 5.11, each
      with its own test): the entry must name THIS family — a finding carries
      `(repo, path)` and no third coordinate, so a `(repo, path)`-only lookup
      would let a NEIGHBOURING family's entry at the same path supply the
      citation, which is a shape the standing file HAS
      (`location-conformance` and `document-catalog` over one
      `ideation/staging/` path); it must carry the `date` § 4.3's scenario
      asks for, which the shared reader has never tested; and its `cite` must
      be TEXT THAT SAYS SOMETHING, `cite: '   '` being truthy enough to pass
      that reader and to emit a row reading `Cite: ` with no ruling after it.
      No predicate honours an entry that reader would refuse.
      **AND A THIRD ROUND ADDED A TYPE GUARD THAT IS NOT A PREDICATE AT ALL**
      (§ 5.11): the shared reader already refuses an entry whose `repo` or
      `path` is not a string, so such an entry was never admitted and the
      honoured set is identical either way — but the citation pass built its
      lookup key from the RAW entry, and a list- or dict-valued `repo` makes
      that key UNHASHABLE, so `key in admitted` raised `TypeError` out of the
      family and out of the whole run. The guard is that reader's own refusal
      taken early, before the key is built.
- [x] 3.3 **THE BOUNDARY IS ONE PREDICATE IN ONE PLACE**:
      `finding.path.startswith(_ARCHIVED_PACKET_PREFIX)`, evaluated at the
      downgrade site rather than in the loader — the loader answers *which
      entries are recorded*, and the archive rule is about *what a recorded
      entry may reach*.
- [x] 3.4 **THE CITE IS BOUNDED TO ONE LINE.** `_cite_excerpt` collapses every
      whitespace run first (a literal-block `|-` entry would otherwise split the
      ranked-plan row into two lines that match no parser — issue #474's shape at
      a different field), cuts at a word boundary at `_CITE_EXCERPT_CHARS = 240`
      and appends an ellipsis. A short cite is quoted whole with no ellipsis.
- [x] 3.5 **THE DOWNGRADED FINDING KEEPS ITS IDENTITY AND NAMES THE DEFECT IN
      FULL.** `dataclasses.replace` on the finding the arm built: same family,
      repo, path and resolution class; `severity` → `INFO`; `rule` → the arm's
      own rule behind `"GRANDFATHERED by a recorded disposition — "`; `action` →
      the no-repair-is-owed text plus the excerpt. Every untouched finding is
      returned BY IDENTITY, not rebuilt.
- [x] 3.6 **NOTHING ELSE MOVES IN THIS MODULE**: no arm, no document scope, no
      threshold, no resolution class, no other family, no report field, no
      workflow, no contract member, no schema, no path. `INFO` was already
      imported by this module and already spent by four families; the only
      import added is `dataclasses.replace`. The one edit OUTSIDE `families.py`
      is § 3.9's pair of guards, which change what no run REPORTS and only
      whether a malformed FILE aborts it.
- [x] 3.7 `tests/doc-health/test_grandfather_dispositions.py` (**NEW, 21
      tests**): the downgrade on BOTH covered arms; an undispositioned archived
      record unchanged; the ACTIVE/ARCHIVED boundary asserted in ONE run over
      the same record text at two paths; a missing `cite`, an empty `cite`, a
      missing `date`, an empty `date`, another family, another repository, and
      **another family's entry at the SAME path** — each ignored, the last
      asserted on the CITATION it must not supply; a `requirement:` narrowing
      not stopping the downgrade; `agg_root=None` (the `--single-repo`
      self-gate) unchanged; a missing dispositions file unchanged; a clean
      corpus never opening the file; every other finding returned as its arm
      built it **by `is`, over the arms' own list**; the admission key set
      pinned EQUAL to the shared reader's over a five-entry file; **a
      malformed entry — a list-valued `repo`, a dict-valued `path` — IGNORED
      RATHER THAN ABORTING THE RUN**, asserted both beside a valid entry and
      alone, and asserted on the shared reader's admitted set to show the
      guard honours nothing differently; a whitespace-only `cite` and a
      non-string `cite` each ignored, the first asserted against the shared
      reader's admitted set so the narrowing is visible as this arm's own act;
      the early return proved by a MONKEYPATCHED reader that RAISES, so the
      no-read is observed rather than inferred from an empty result, with the
      dirty corpus asserted to raise so the probe is known live; the excerpt's
      one-line and bounded properties; and the downgraded row rendered by
      `report.plan_line(strict=True)` and read back by `report.PLAN_RE`,
      `report.unparsed_plan_rows` and `report.parse_previous`; and a
      **malformed dispositions FILE — a scalar root — IGNORED RATHER THAN
      ABORTING THE RUN** (§ 3.9), asserted for this arm, for the two families
      that have read the file since the shared reader was written, and for
      every other non-list root, with a list root still read exactly as before.

- [x] 3.8 **NO EXISTING TEST IS EDITED, RENAMED, FLIPPED OR DELETED.**
      `tests/doc-health` goes **1689 → 1710**, the whole rise being the new
      file: 21 test functions in it, counted with
      `grep -c '^def test_' tests/doc-health/test_grandfather_dispositions.py`,
      and 1689 re-measured on an `origin/main` worktree (`38c076d1`) in the
      same shell as this tree's 1710. **THAT PAIR IS THE PACKET'S ONE TEST
      COUNT**: § 3.7, this box, § 5.8, § 5.13 and the pull request body all
      state it and no other.
      `test_ratification_record_subject.py`'s real-tree measurements are
      untouched by construction: they build their `Context` with
      `agg_root=None`, which is the scope this arm does nothing in.

- [x] 3.9 **A MALFORMED dispositions FILE MUST NOT ABORT THE NIGHTLY EITHER,
      AND THE ABORT IS OLDER THAN THIS PACKET** (PR #945, Copilot's fourth
      round). `yaml.safe_load` returns whatever the document holds, so a SCALAR
      root (`42`) is well-formed YAML that reaches `for entry in entries` and
      raises `TypeError`. **MEASURED BOTH WAYS, END TO END, BEFORE ANYTHING WAS
      CHANGED**, over an aggregation carrying such a file:
      `doc-health.py --repo-root <aggregation>` exits **1** on `origin/main` at
      `runner.py:758` — the runner's own unconditional read of the same file,
      which fires on every aggregation run with or without this packet — and
      exited **1** one frame earlier on this branch, at `families.py:419` into
      `promotion_fidelity.py:757`. **SO THE GUARD IS IN BOTH READERS OR IT BUYS
      NOTHING**: repairing only the shared reader would have moved the abort
      back to the runner's line rather than removed it. Both are the refusal
      each loop already applies to an ENTRY that is not a mapping, taken one
      level up — a malformed FILE ignored exactly as a malformed ENTRY is —
      and **NEITHER NARROWS WHAT COUNTS AS RECORDED**: every non-list root they
      now refuse already yielded an empty set by iteration (a mapping root
      iterates keys, a string root characters, neither being a mapping), which
      § 3.7's test asserts shape by shape. After the fix the same run exits
      **0** and reports every row at `critical` — the file records nothing, so
      nothing is honoured. **RE-MEASURED ON THE RATIFIED TREE** against the
      aggregation § 5.13 names: `origin/main` `38c076d1` **exit 1** with
      `TypeError: 'int' object is not iterable` at
      `scripts/doc_health/runner.py:758`; this tree **exit 0**, `Findings: 35
      critical, 0 error, 0 warning, 0 info`; and over the REAL file the report
      is **byte-identical** to the one taken without the guards (§ 5.13).

## 4. The delta

- [x] 4.1 **ONE `## MODIFIED` REQUIREMENT, WRITTEN OVER CANON**, byte-faithful
      by CONSTRUCTION rather than by transcription: the block was GENERATED by
      slicing `openspec/specs/doc-health/spec.md` lines **878–936** with the
      bounds ASSERTED in the generator (its first line is the requirement
      header, its last is the final scenario's `THEN`, and the line after it is
      the next requirement), then appending ONE `#### Scenario:`. The slice is
      byte-identical to canon: `sha256
      d32aaa43dc6ad118af3a57d58a2a3ffcb80c66ae128ca36b2921224a30bfdbe3` on both
      sides, `diff` empty.
- [x] 4.2 **NO PROMOTED BYTE IS EDITED, SO NO MARKER IS OWED.** No body
      paragraph is added, replaced or removed; no promoted scenario moves, is
      retitled, or loses a bullet; nothing is removed, so there is nothing for a
      `Removed from canon` marker to declare and none is written. Verified by
      the family's own derivation (`modified_block_currency.derive_units` over
      both blocks): **29 canon units, 0 uncarried, 5 of 5 promoted scenario
      titles carried, 8 units added, 0 markers on either side**.
- [x] 4.3 **THE ADDED SCENARIO IS *A finding is grandfathered by a recorded
      disposition***, at the END of the block, in the shape its four siblings
      use and departing from them in ONE bullet — `info` rather than suppressed
      (`design.md` D1). Its seven bullets carry: the WHEN (an archived path, a
      dated cited entry for this family); the `info` band with the citation
      quoted, and WHY; the identity the finding keeps; the MAY that leaves the
      excerpt's bound to the implementation; the ACTIVE-packet refusal; the
      no-`cite` no-op; and the no-aggregation-checkout no-op.
- [x] 4.4 **THE REQUIREMENT'S FIRST BODY LINE IS UNMOVED AND STILL CARRIES
      `SHALL`** — *"The doc-health capability SHALL declare two document sets
      and SHALL keep them distinct."* — which is what the strict parser reads.
- [x] 4.5 **README `## OpenSpec Records` CARRIES THE ACTIVE ROW**, in house
      style, at the DRAFT standing: the word that commissioned the authoring,
      the two declared veto points, the measured 41/18/23 figures, and the
      statement that nothing is promoted and #939 closes at the archive.
- [x] 4.6 **THE PER-CHANGE SWEEP LEDGER ROW IS SEEDED BY THE SANCTIONED TOOL**,
      never hand-written: `python3 scripts/validate-sequenced-after.py .
      --seed-ledger --moved-by '#945'` — *"wrote
      tests/sequenced_after/corpus-ledger.yaml (198 rows, 1 moved by #945)"*,
      run after the draft pull request existed because the tool stamps
      `moved_by` with its number. **THE DIFF IS ONE LINE**, which is the claim
      measured rather than asserted:
      `honour-grandfather-dispositions-in-ratified-provenance: {state: active,
      class: co-modifier, declares: [], depth: 0, prose: false, moved_by:
      "#945", moved_on: "2026-09-11"}`. NO other row's provenance moves: the
      change classes `co-modifier` on ARCHIVED partners only — the archived
      changes that carry a `## MODIFIED` block for this requirement — so no
      partner flips and no MOVEMENT LOG entry is owed.

## 5. Verification — DONE IN THIS PULL REQUEST

**EVERY LINE BELOW IS A COMMAND THAT WAS RUN ON THE FINAL TREE** — the merge of
`origin/main` `f0eea7ed`, the § 5.10 review round and the § 4.6 ledger seed —
with its exit code and its own output quoted.

- [x] 5.1 `OPENSPEC_TELEMETRY=0 openspec validate
      honour-grandfather-dispositions-in-ratified-provenance --strict` —
      **exit 0**, *"Change 'honour-grandfather-dispositions-in-ratified-provenance'
      is valid"*.
- [x] 5.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — **exit 1**,
      `Totals: 98 passed, 3 failed (101 items)`. The failure set is
      BYTE-IDENTICAL to `origin/main` `f0eea7ed`'s, taken in the same shell from
      a worktree of it (`97 passed, 3 failed (100 items)`):
      `change/disposition-codexfactory-declared-renames`,
      `change/disposition-codexfactory-floor-relocation-retitle`,
      `spec/repo-boundary-governance`. This change is in NEITHER set and the
      item count moves by exactly one.
- [x] 5.3 **THROUGH THE PINNED CLI, WHICH IS THE ONE THE GATE RUNS.**
      `python3 scripts/validate-openspec-cli-pin.py --change … --no-cache` —
      **exit 0**, `@fission-ai/openspec@1.12.0` verified against its content
      address, its 80-package closure installed with `npm ci --ignore-scripts`
      and its `lockfile_integrity` verified, `Totals: 1 passed, 0 failed (1
      items)`. The gate's literal `--all --no-cache` — **exit 0**,
      `Totals: 99 passed, 2 failed (101 items)`, *"every target validated
      --strict with 0 UNDISPOSITIONED failures"*, the two failures being the
      PRE-EXISTING accepted exceptions `add-chain-attestation` and
      `add-composed-view-authoring`, neither of them this change.
- [x] 5.4 `python3 scripts/proposal-support.py . verify
      honour-grandfather-dispositions-in-ratified-provenance` — **exit 0**,
      *"proposal support verification ok"*.
- [x] 5.5 `python3 scripts/validate-sequenced-after.py .` — **exit 0**, *"39
      active changes, 9 declaring the field"*, both archive-date arms passing.
      `--ledger-diff` — **exit 0**, *"per-change sweep ledger consistent with
      the corpus (198 rows)"*, taken after the § 4.6 seed (before it: exit 1,
      8 findings, `missing row` and seven derived-total mismatches).
- [x] 5.6 `python3 scripts/validate-scope-globs.py .` — **exit 0**,
      *"scope_globs validation passed (all active changes conform)"*.
- [x] 5.7 `python3 scripts/doc-health.py --single-repo .` — **exit 0**, and the
      report is **IDENTICAL LINE FOR LINE** to `origin/main` `f0eea7ed`'s, 349
      lines each, `diff` empty once the checkout DIRECTORY NAME is normalised
      (the only token that differs, the two runs being rooted at differently
      named clones). That is the claim of `design.md` D6's last bullet
      measured: `health/dispositions.yaml` lives at the aggregation root, a
      self-gate run has `agg_root is None`, and this arm does nothing at all in
      that scope — and it is also proof that the packet's own new documents add
      no finding of their own.
- [x] 5.8 `python3 -m pytest tests/doc-health tests/sequenced_after
      tests/scope_globs tests/proposal-support -q` — **exit 0**, **2197 passed,
      66 subtests passed**, taken on the § 5 tree named above. **THE
      `tests/doc-health` COUNT IS ONE MEASUREMENT AND IT IS THE LAST ONE**,
      re-taken after the § 5.12 fix added its regression test: **1710** on this
      tree and **1689** on an `origin/main` worktree (`38c076d1`) beside it in
      the same shell, **+21** — the new file entire (21 `def test_`, counted
      rather than recalled), and nothing else. The earlier readings of this
      line (**1708**, **+19**) were taken before the § 5.11 and § 5.12 rounds
      added their tests and are SUPERSEDED by it; § 5.13 re-derives the whole
      gate set, this suite included, on the ratified tree.
- [x] 5.9 **THE AGGREGATION MEASUREMENT RE-RUN ON THE FINAL TREE**, § 2.2
      through § 2.6 repeated after the last commit against an aggregation
      assembled TODAY: `opensoft/xFactory` @ `5fc9bc53` with `openxFactory`
      checked out at each side of the comparison and `codexFactory` @
      `eb093294` (the pin that aggregation head carries) materialized under
      `xFactories/`. **The dispositions file is the same file D0 measured**:
      blob `414ed86e` at `bc84d325`, at `5fc9bc53` and in the checkout, so the
      two measurements read identical bytes. BEFORE (`openxFactory` @
      `f0eea7ed`): `Findings: 41 critical, 0 error, 0 warning, 0 info`. AFTER
      (this tree): `Findings: 23 critical, 0 error, 0 warning, 18 info`, 41
      rows, `SAME KEY SETS: True`, `moved: 18`, `byte-identical: 23`,
      `MOVED == DISPOSITION KEY SET: True`, `all moved paths archived: True`,
      `dispositioned but NOT reported: 0`, the arm split `15` SUBJECT-arm
      (openxFactory) and `3` citation-arm (codexFactory), every moved row
      keeping its family, repo, path and resolution class and carrying the
      `GRANDFATHERED by a recorded disposition — ` prefix in front of its own
      arm's rule. `report.unparsed_plan_rows` → `[]`;
      `report.parse_previous` → **23** keys, **0** contested, against **41**
      and **0** before.
- [x] 5.10 **THE BOT BENCH, TAKEN AND ANSWERED ON THE RECORD.** Copilot's two
      threads were both **TAKEN** and answered by a commit rather than by a
      reply. (1) `_grandfather_cites`' citation lookup keyed `(repo, path)`
      alone, so a NEIGHBOURING family's entry at the same path could supply the
      text — a shape the standing `health/dispositions.yaml` HAS, carrying
      `location-conformance` and `document-catalog` over one `ideation/staging/`
      path — and it honoured an UNDATED entry although § 4.3's scenario asks
      for a date. Both predicates are now applied in that pass, and both only
      NARROW what a recorded entry may reach; `design.md` D3's delegation is
      untouched, the shared reader still answering alone which entries are
      RECORDED. (2) the pass-through-BY-IDENTITY invariant was documented and
      uncovered: the test compared findings from two separate runs, which can
      only compare VALUES. The arms now run once and the pass is called on
      their own list, with `is` on every untouched row. **MEASURED BOTH WAYS**:
      against the pre-fix module the two new tests FAIL and the rewritten
      identity test passes; against a probe build whose pass rebuilds every
      untouched finding, the RETIRED two-run form PASSES and the rewritten one
      FAILS on the first untouched row. The eighteen figures do not move —
      every standing entry for this family carries a `date`, and none shares a
      path with another family's entry.

- [x] 5.11 **THE THIRD BENCH ROUND, TAKEN AND REFUSED ON THE RECORD.** Copilot
      reviewed again at 2026-09-11T10:18:18Z and its round is dispositioned
      item by item rather than in aggregate. **FOUR TAKEN.** (1) **A CRASH**,
      and the only comment it posted as a thread: the citation pass built its
      lookup key from the RAW entry, so a same-family entry with a list- or
      dict-valued `repo` or `path` made `(repo, path)` UNHASHABLE and
      `key in admitted` raised `TypeError` out of the family and out of the
      whole run — reproduced first at `families.py:451`, then guarded with the
      shared reader's own `isinstance` test taken before the key is built, and
      pinned by a test asserted BOTH WAYS (it fails on the pre-fix module with
      that exact `TypeError` and passes on the fix). The guard is not a
      predicate: an entry it drops is one `load_dispositions` never admitted,
      so the honoured set is identical either way. (2) A truthy but EMPTY
      citation — `cite: '   '` passes the shared reader and would emit an
      `info` row reading `Cite: ` with no ruling after it, which is this arm's
      own defect in miniature; a non-blank STRING is now required and a
      non-string `cite` is refused rather than coerced (`str(5)` is not a
      citation). (3) `_RATIFIED_PROVENANCE`'s comment claimed the family id was
      *"spelled once"* while the five arms and the `FAMILIES` registration
      still spell the literal; the CLAIM is corrected rather than the arms
      rewritten, because § 3.1 leaves them byte-unmoved. (4) The early-return
      test proved only its own result — a valid file and an empty list pass
      whether or not the file was opened — so the reader is now monkeypatched
      to RAISE and the clean run must still return `[]`, with the dirty corpus
      asserted to raise so the probe is known live. **TWO REFUSED, WITH THE
      REASON RECORDED RATHER THAN THE COMMENT DROPPED.** (a) That the added
      scenario CONTRADICTS *A proposal carries an uncited ratified header* and
      that the older bullet should be amended: REFUSED on custody first — that
      bullet is PROMOTED CANON carried here byte-faithfully as the `##
      MODIFIED` block's pre-text (`sha256 d32aaa43…` on both sides, § 4.1), so
      amending it would edit promoted text, break the carriage proof and owe a
      marker § 4.2 measures as not owed; and the word of 2026-09-11T10:11:50Z
      landed on this text with the comment already six hours on the record. On
      the merits it is also not a contradiction: the older bullet asserts
      PARITY between the lifecycle scan set and the governed corpus (*"the same
      severity it would carry for a governed-corpus document"*), and this pass
      is scope-blind — it keys on `(family, repo, path)` and an archived path
      and would downgrade a governed-corpus document identically — so the
      parity it exists to protect is exactly preserved, the newer scenario
      being the more specific rule over a strictly narrower subject. The four
      sibling *A finding is dispositioned* scenarios already sit beside their
      own families' severity rules with no exception clause, and they SUPPRESS,
      which departs further. (b) That the downgraded row should carry
      `CONTESTED` rather than the family's `auto-fixable` class: REFUSED as a
      re-decision rather than a fix. § 3.5 keeps the resolution class on
      purpose, the proposal's *What this proposal does NOT do* says so, and
      § 2.6 MEASURES the consequence — the eighteen leave the regression axis
      and enter no other, `report.parse_previous` returning 0 contested.
      `CONTESTED` would route them into `report.uncited_resolutions`, the arm
      the proposal's *Why* shows adjudicates a DISAPPEARED finding and never a
      standing one. It is a successor's question, beside § 7's residue, and it
      needs its own word.

- [x] 5.12 **THE FOURTH BENCH ROUND, BOTH ITEMS TAKEN ON THE RECORD.** Copilot
      reviewed again at 2026-09-11T11:01Z, on `cd27180c`. (1) **A SECOND
      CRASH, ONE LEVEL UP AND OLDER THAN THIS PACKET**: a dispositions file
      whose top-level value is a SCALAR reaches `load_dispositions`'
      `for entry in entries` and raises `TypeError`, and this family did not
      read that file before this change. TAKEN, and taken WIDER than the thread
      asked because the narrow fix would have been cosmetic: measured end to
      end first, `origin/main` ALREADY exits 1 over such a file at
      `runner.py:758`, its own unconditional read, so a guard in the shared
      reader alone would have moved the abort rather than removed it. Both
      readers now refuse a non-list root, the repair is pinned by a test
      asserted BOTH WAYS (it fails on the pre-fix module with that exact
      `TypeError`), and the full run over the real file is byte-identical to
      the one taken without the guards — § 3.9 carries the measurement.
      (2) **THE VERIFICATION COUNTS WERE INCONSISTENT** — § 3.8 read
      1689 → 1709, § 5.8 read 1708 (+19) and the pull request body read 17
      tests / 1706, the three having been written at three different heads.
      TAKEN: every count in this packet and in the pull request body is now the
      SAME measurement, re-taken on the final tree and against the `origin/main`
      worktree named in § 5.8, and the new file's test functions are counted
      rather than recalled.

## 6. Archive — OWED, NOT GIVEN

- [ ] 6.1 **PROMOTE THE BLOCK INTO CANON**, byte-for-byte, in a SEPARATE pull
      request on a separate word, after § 1 is ruled and after the realization
      evidence this packet's `target_release` names: this pull request merged
      into `main` and a green `pytest-suite` run at the tree that merge carries
      (`release-realization`'s merged-plus-green rule, at canon's grain).
- [ ] 6.2 **THE ORIGIN ISSUE IS CLOSED AT THE ARCHIVE PULL REQUEST AND
      NOWHERE ELSE**, by a closing keyword written THERE against openxFactory
      issue 939. No closing keyword appears in this pull request's body or in
      any commit message on this branch, in any form, quoted or otherwise — a
      commit message auto-closes exactly as a body does, so the guard greps
      both.

## 7. Measured, and deliberately NOT taken here

- [ ] 7.1 **A STALE-DISPOSITION CHECK.** An entry naming a path that no longer
      exists, or a record since repaired, matches nothing and is reported
      nowhere. Measured today: all 18 entries match a live finding, so that
      successor's population is ZERO. It is a new finding class with its own
      severity and its own population and belongs to its own act.
- [ ] 7.2 **THE OTHER SEVEN FAMILIES' 22 ENTRIES.** Whether any of them should
      be downgraded rather than suppressed — or read at all, for the families
      that read nothing — is a separate question about a different subject.
- [ ] 7.3 **`docs/doc-health.md`'s FAMILY TABLE ROW 3** still reads *"Every
      `Ratified by:` resolves to an existing OpenSpec change"*, which has been
      incomplete since the two-spelling ruling and is more incomplete now. A
      documentation sweep of that table, not this packet's act.
- [ ] 7.4 **A `--single-repo` ROUTE TO AN AGGREGATION DISPOSITIONS FILE.** A CLI
      surface, an argument, a contract line and a test matrix, for a gate whose
      job is to report this repository's own defects (`design.md` D6).
