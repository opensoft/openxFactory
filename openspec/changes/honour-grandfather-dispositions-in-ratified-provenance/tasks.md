# Tasks: honour-grandfather-dispositions-in-ratified-provenance

Status: ratified
Ratified by: honour-grandfather-dispositions-in-ratified-provenance — 2026-09-11, Brett Heap, D1 "info row carrying the citation" / D2 "Archived-only boundary" (record `review/ratification-2026-09-11.md`)
Kind: tasks

`code_surface: openxFactory`, `target_release: implemented`. The realization
group is § 3 and it is IN THIS PULL REQUEST: the tasks are individually
executable, so under `release-realization`'s decomposition rule this packet
realizes through its own task list rather than through a feature DAG.

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in
this pull request or a measurement recorded verbatim in the pull request body
and reproducible from the commands named beside it.

**§ 1 (RATIFICATION) IS NOW TICKED AND NAMES THE WORD THAT TICKED IT**, which
is Brett Heap's act and not the authoring lane's. His earlier word of
2026-09-11, verbatim **"Commission the packet"**, commissioned the AUTHORING and
decided no wording; it stays recorded as the origin in `.openspec.yaml` and is
not read as an approval. The RATIFICATION is his separate word of
2026-09-11T10:11:50Z, recorded on PR #945 at 10:11:56Z, a MULTIPLE-CHOICE
ruling over `design.md` D1 and D2 that took **"info row carrying the
citation"** and **"Archived-only boundary"** — both the recommended and
already-encoded options, so the packet's wording stands unchanged.
`.openspec.yaml` now carries `approved_by`/`approved_on` ADDED BESIDE the
drafting provenance, which is byte-unmoved, and every document here carries
`Status: ratified` with exactly one citation line.

**§ 6 (ARCHIVE) IS ENTIRELY OPEN.** `code_surface` is non-empty, so the archive
is a separate act on merged-plus-green realization evidence and a separate word,
and openxFactory #939 closes THERE and not at this landing.

**§ 7 IS UNTICKED ON PURPOSE**: residue, measured and deliberately not taken.

**AMENDED AT THE ARCHIVE, 2026-09-11 — EXACTLY TWO CLAUSES IN THIS FILE ARE
SUPERSEDED, THEY ARE NAMED WITH THEIR LOCATIONS, AND THEY ARE QUOTED IN PLACE
RATHER THAN DELETED.** Both are PRESENT-TENSE claims that a section stood open.
These two and no others:

> **§ 6 (ARCHIVE) IS ENTIRELY OPEN.** — the paragraph above

> **§ 7 IS UNTICKED ON PURPOSE** — the paragraph above

§ 6.1, § 6.2, § 7.1, § 7.2, § 7.3 and § 7.4 are now ticked, on Brett Heap's
separate word of **2026-09-11T12:08Z**, verbatim **"land each when green,
archive both when landed, claim 955 and 956"**, recorded on
[#939](https://github.com/opensoft/openxFactory/issues/939#issuecomment-5634202632)
— a word given in advance and CONDITIONALLY, and the condition is met: PR
[#945](https://github.com/opensoft/openxFactory/pull/945) merged into `main` as
**`34bb5c7158b42a45e4a4eddd2681ca9b7c3f550f`** at **2026-09-11T13:25:33Z**, and
`main`'s own `pytest-suite` run
[**34604231434**](https://github.com/opensoft/openxFactory/actions/runs/34604231434)
on that very commit concluded **`success`** at 13:51:03Z. They are ticked in the
commit BEFORE the move, because `scripts/proposal-support.py` refuses any change
whose `tasks.md` still matches `^- \[ \]` — *"change has incomplete tasks"* —
with no bypass flag; the archive pull request's number is appended to § 6.1 and
§ 6.2 in the ledger-seed commit, once the number exists.

**THREE SENTENCES A READER MIGHT TAKE FOR SUPERSEDED ARE NOT, DECLARED HERE
RATHER THAN LEFT TO BE INFERRED.** (1) ***"NOTHING IS TICKED THAT DID NOT
LAND"*** STANDS: § 6's two ticks record acts performed in the archive pull
request itself, and § 7's four record the NAMING of a successor, never its
doing. (2) *"the archive is a separate act on merged-plus-green realization
evidence and a separate word, and openxFactory #939 closes THERE and not at this
landing"* STANDS, and is exactly what this archive does — this is that separate
act, on that separate word, on that realization evidence, and the one closing
keyword is in the archive pull request's BODY and nowhere else. (3) *"residue,
measured and deliberately not taken"* in § 7's own heading and preamble STANDS:
the four residues are still not taken here, and ticking them names a successor
rather than discharging the work.

**THE FIVE OWED SUCCESSORS ARE FILED, UNCLAIMED, AND NAMED HERE.**
[#965](https://github.com/opensoft/openxFactory/issues/965) takes § 7.1 (the
stale-disposition check), [#966](https://github.com/opensoft/openxFactory/issues/966)
§ 7.2 (the other eight families' entries),
[#967](https://github.com/opensoft/openxFactory/issues/967) § 7.3 (the
`docs/doc-health.md` family-table row) and
[#968](https://github.com/opensoft/openxFactory/issues/968) § 7.4 (`design.md`
D6's `--single-repo` route). A FIFTH,
[#964](https://github.com/opensoft/openxFactory/issues/964), carries a residue
this file could not have named because it was found at the bench AFTER
ratification: Copilot's SUPPRESSED item of 2026-09-11T12:47:41Z (review
`5178781132`) that no `runner.main` end-to-end test covers § 3.9's scalar-root
FILE guard at `scripts/doc_health/runner.py:768`, landed in `5a8bba3e`. A
coverage gap on a LANDED code surface is a successor and not an archive edit:
`record-immutability` and `govern-archived-record-edits` put this packet's bytes
beyond a plain fix, so no test is added here. None of the five is claimed by
this lane.

**THE § 6 HEADING *"OWED, NOT GIVEN"* AND THE § 7 HEADING *"Measured, and
deliberately NOT taken here"* ARE RETAINED AS HISTORICAL SURFACE, NOT
SUPERSEDED** — stated at the outset rather than corrected afterwards. § 6's was
true from ratification until 2026-09-11T12:08Z; § 7's is true still.

## 1. Ratification — GIVEN 2026-09-11

- [x] 1.1 **THE PACKET IS RATIFIED.** Brett Heap (openxFactory operator
      authority) ruled on this packet itself on 2026-09-11, the word given in
      session at 10:11:50Z and recorded on PR #945 at 10:11:56Z (comment
      5632913794). `Status: ratified` with one citation line now stands on
      `proposal.md`, `design.md` and `tasks.md`, and `.openspec.yaml` carries
      `approved_by`/`approved_on` as a pure ADDITION beside a byte-unmoved
      `kind`, `id`, `reason`, `proposed_by` and `proposed_on` — the shape
      `add-drafted-proposal-origin` (issue #318) added for exactly this
      transition, and the shape the archive gate's origin-retention arm reads.
- [x] 1.2 **`design.md` D1 — THE BAND — RULED "info row carrying the
      citation".** The RECOMMENDED option, against *"Suppress, matching the
      four siblings"* on the four siblings' precedent. It was put with the
      recommendation first and the veto's cost written out: suppression would
      have been a smaller diff and would have matched four promoted
      requirements exactly, at the cost of the eighteen records' visibility, an
      uncountable grandfathered population, and a stale entry become invisible.
      **THE ENCODED OPTION WAS TAKEN, SO NOTHING MOVED**: the `THEN` bullet of
      the delta and the branch of `_honour_grandfather_dispositions` stand
      exactly as the bench reviewed them.
- [x] 1.3 **`design.md` D2 — THE BOUNDARY — RULED "Archived-only boundary".**
      The RECOMMENDED option, against *"Admit active paths too"*. A veto would
      have cost the distinction between a ruling on something nobody may repair
      and a deferral of something somebody could fix this afternoon. D1 and D2
      rest on no shared predicate and either would have stood whichever way the
      other went; both took the encoded option. **THE PREDICATE WAS NOT
      WIDENED**: `finding.path.startswith("openspec/changes/archive/")` is the
      whole test and the scenario's ACTIVE-packet bullet stands.
- [x] 1.4 **D0 AND D3 THROUGH D6 WERE CARRIED BESIDE THEM AND NONE WAS
      VETOED**, each with its alternative written out and each open to veto in
      the same ruling: D0 (the measurement), D3 (the existing file, the
      existing key, the delegated admission rule, the bounded cite excerpt),
      D4 (`doc-health` is amended and `document-lifecycle` is NOT), D5 (the
      sibling search), D6 (what is not taken). The ruling reached D1 and D2 and
      left all six standing as authored.

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
      `tests/doc-health` goes **1689 → 1711**, the whole rise being the new
      file: 22 test functions in it, counted with
      `grep -c '^def test_' tests/doc-health/test_grandfather_dispositions.py`,
      and 1689 re-measured on an `origin/main` worktree (`38c076d1`) in the
      same shell as this tree's 1711. **THAT PAIR IS THE PACKET'S ONE TEST
      COUNT**: § 3.7, this box, § 5.8, § 5.14 and the pull request body all
      state it and no other; the earlier readings (1706, 1708, 1709, 1710)
      were taken at heads before the § 5.11, § 5.12 and § 5.14 rounds added
      their tests, and are superseded.
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

- [x] 3.10 **AND THE RUNNER'S OWN READ MUST SURVIVE A MALFORMED ENTRY, NOT
      ONLY A MALFORMED FILE** (PR #945, Copilot's FIFTH round). § 3.9 stopped
      a scalar ROOT from aborting `runner.main`'s unconditional read; the
      round after it found the same read still building
      `(family, repo, path)` from the RAW entry, so a list- or dict-valued
      field in an otherwise well-formed list file makes that tuple unhashable
      and `set.add` raises `TypeError` out of the whole nightly — **MEASURED
      BOTH WAYS** at `runner.py:770`, `TypeError: unhashable type: 'list'`
      without the guard and exit 0 with it. This is the SAME defect § 5.11
      took inside `families.py`, at the OTHER reader of the same file, and it
      likewise **predates this packet**: the read is unconditional on every
      aggregation run with or without #939's arm. The guard skips only an
      entry whose key CANNOT BE HASHED, which **narrows nothing** — such a key
      could never have entered the set and could never have matched a real
      finding, whose family, repo and path are always strings — so the
      dispositioned set is identical either way and only the exception is
      gone. Pinned by
      `test_the_runners_own_read_survives_a_malformed_entry_end_to_end`,
      which goes END TO END through `runner.main` over a real aggregation
      root because that is the only path that executes the read, and which
      the § 3.7 entry tests could not have caught: they call the family
      directly and never reach the runner.

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
      style. It was seeded at the DRAFT standing — the word that commissioned
      the authoring, the two declared veto points, the measured 41/18/23
      figures, and the statement that nothing is promoted and #939 closes at
      the archive — and it MOVED TO THE RATIFIED STANDING IN THE SAME COMMIT AS
      the status flip: it now names the ratifier, the date, the two verbatim
      options and their recording on PR #945, the records' paths, the approval
      pair added beside an unmoved origin, and that § 6 stays entirely open.
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

**EVERY LINE BELOW IS A COMMAND THAT WAS RUN ON A REAL TREE**, with its exit
code and its own output quoted. § 5.1 through § 5.9 were taken on the
pre-ratification tree of 2026-09-11 — the merge of `origin/main` `f0eea7ed`,
the § 5.10 review round and the § 4.6 ledger seed. **THE TREE MOVED SIX TIMES
AFTER THAT**: three further merges from `origin/main` (`1fb6d5cd` at
`468df2ef`, `22efcbe8` at `a343f017`, `78d2c6f5` at `f281c1fa`), the § 5.11 and
§ 5.12 review rounds (`cd27180c`, `5a8bba3e`), the merge of `origin/main`
`38c076d1` at `ad6d542c`, and the ratification encode itself. So **§ 5.13
RE-DERIVES THE WHOLE GATE SET ON THE RATIFIED TREE**, and its figures — not
§ 5.1–5.9's — are the ones this packet stands on; the record of them is
`review/verification-2026-09-11.md`. The earlier readings are kept as the
record of what was measured when, which is what makes the two comparable.

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
      re-taken after the § 5.14 fix added its regression test: **1711** on this
      tree and **1689** on an `origin/main` worktree (`38c076d1`) beside it in
      the same shell, **+22** — the new file entire (22 `def test_`, counted
      rather than recalled), and nothing else. The earlier readings of this
      line (**1708**/**+19** and **1710**/**+21**) were taken before the
      § 5.11, § 5.12 and § 5.14 rounds added their tests and are SUPERSEDED by
      it; § 5.13 and § 5.14 re-derive the gate set on the ratified tree.
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

- [x] 5.13 **THE WHOLE GATE SET RE-DERIVED ON THE RATIFIED TREE**, after the
      § 5.12 fix, after the merge of `origin/main` `38c076d1` (`ad6d542c`) and
      after the ratification encode, in a fresh clone. The capture with every
      command line, exit code and control run is
      `review/verification-2026-09-11.md`; the figures are:
      `openspec validate <change> --strict` **exit 0**;
      `openspec validate --all --strict` on the 1.2.0 binary **exit 1**,
      `99 passed, 2 failed (101 items)`, the failure set IDENTICAL to
      `origin/main` `38c076d1`'s `98 passed, 2 failed (100 items)` and this
      change the one extra item, passing
      (`spec/repo-boundary-governance` has left BOTH sets since #958 archived
      `amend-repo-boundary-governance-scope-first-line` on `main`);
      `validate-openspec-cli-pin.py --all --no-cache` on the pinned 1.12.0
      **exit 0**, `99 passed, 2 failed (101 items)`, the two being the
      PRE-EXISTING accepted exceptions of 2026-09-05 *"take exit 2"*;
      `proposal-support.py . verify` **exit 0**;
      `validate-sequenced-after.py .` **exit 0** and `--ledger-diff` **exit 0**
      (200 rows, the rise from 198 being `main`'s two archives, not this
      change's row); `validate-scope-globs.py .` **exit 0**;
      `doc-health.py --single-repo .` **exit 0**,
      `32 critical, 5 error, 47 warning, 15 info`, the report
      NORMALIZED-IDENTICAL to `origin/main`'s (`diff` **0 lines**, 99 finding
      lines each), **28 `ratified-provenance` rows all `critical` and 0
      `info`** — D6 measured — **0 marker-defect findings**, and **0** findings
      naming this packet; `pytest tests/doc-health -q` **1710 passed, exit 0**
      at the head this box was taken on, re-taken as **1711** in § 5.14 after
      the fifth round's test, against the control's **1689**; and
      `pytest tests/doc-health tests/sequenced_after tests/scope_globs
      tests/proposal-support -q` **2199 passed, 66 subtests passed, exit 0**.
      **THE AGGREGATION MEASUREMENT WAS RE-TAKEN TOO** (§ 2.2–§ 2.6, § 5.9),
      against `opensoft/xFactory` `f5dba67f` with `codexFactory` `ef180510`:
      35 rows, `35 critical / 0 info` → `20 critical / 15 info`, same key
      sets, moved == the reported disposition keys, all moved paths archived,
      every moved row citing, 62 changed lines in the report diff, the Ranked
      Plan keeping all 35, `unparsed_plan_rows` `[]` and `parse_previous`
      `20` keys / `0` contested. **ONE FIGURE MOVED SINCE D0 AND THE RECORD
      SAYS SO RATHER THAN SMOOTHING IT**: eighteen entries still stand for this
      family, but codexFactory's three records have since been REPAIRED at that
      pin and draw no finding, so fifteen move and three entries are now stale
      — the § 7.1 successor's population, which that box recorded as zero when
      it was measured and which is no longer zero. Nothing in the rule depends
      on the number: it is a set equality over whatever the file records and
      whatever the run reports.

- [x] 5.14 **THE FIFTH BENCH ROUND, TAKEN ON THE RECORD, AND THE GATES
      RE-DERIVED AFTER IT.** Copilot reviewed again at 2026-09-11T12:23:01Z,
      on `5a8bba3e`, and opened two threads. (1) **THE RUNNER'S UNHASHABLE
      KEY** — § 3.10 carries the measurement and the fix. (2) **THE README
      SUMMARY STILL READ 20 TESTS** while § 3.8 read 1710: TAKEN, and it was
      already true when the comment arrived — the ratification encode
      `e60ad2ff` had moved that row to *21 new tests, 1689 → 1710* minutes
      earlier — so this round moves it again, to the final **22 / 1689 →
      1711**, which is now the one figure in the front matter, § 3.7, § 3.8,
      § 5.8, this box, the README row and the pull request body.
      **RE-MEASURED AFTER THE FIX**: `grep -c '^def test_'` on the new file
      → **22**; `python3 -m pytest tests/doc-health --collect-only -q` →
      **1711 tests collected**, against the unchanged `origin/main`
      `38c076d1` control of **1689 passed**; the whole new file alone →
      **22 passed, exit 0**, and the same directory read **1710 passed,
      exit 0** on this tree one test ago (§ 5.13), so the rise is +22 by
      collection and by sum alike;
      `openspec validate <change> --strict` → **exit 0**;
      `proposal-support.py . verify` → **exit 0**;
      `validate-sequenced-after.py .` and `--ledger-diff` → **exit 0**;
      `validate-scope-globs.py .` → **exit 0**. Every other figure in § 5.13
      is unmoved by a guard that changes no report: the capture at
      `review/verification-2026-09-11-post-bench.md` states which were re-run
      and which were not, and it is a SECOND capture at its own path because
      a committed dated run report is never rewritten.

## 6. Archive — OWED, NOT GIVEN

- [x] 6.1 **DONE IN THIS ARCHIVE PULL REQUEST — THE BLOCK IS PROMOTED INTO
      CANON AND THE PACKET IS ARCHIVED, ON BRETT HEAP'S SEPARATE WORD OF
      2026-09-11T12:08Z**, verbatim *"land each when green, archive both when
      landed, claim 955 and 956"*, recorded on
      [#939](https://github.com/opensoft/openxFactory/issues/939#issuecomment-5634202632).
      A word given in advance and CONDITIONALLY, and **the condition is met**:
      PR [#945](https://github.com/opensoft/openxFactory/pull/945) merged into
      `main` as **`34bb5c7158b42a45e4a4eddd2681ca9b7c3f550f`** at
      **2026-09-11T13:25:33Z**, and this box's own words — *"a green
      `pytest-suite` run at the tree that merge carries
      (`release-realization`'s merged-plus-green rule, at canon's grain)"* —
      are satisfied by `main`'s OWN run
      [**34604231434**](https://github.com/opensoft/openxFactory/actions/runs/34604231434),
      workflow `pytest-suite`, event `push`, head **`34bb5c71`** — the merge
      commit ITSELF, not a test-merge of it — **conclusion `success`**,
      13:25:41Z to 13:51:03Z. **NO TREE-EQUALITY ARGUMENT IS NEEDED AND NONE IS
      MADE**: the tested tree IS the merge commit's tree, because the run's head
      IS the merge commit. **THE PULL REQUEST'S OWN GREEN RUN IS NOT THE GROUND
      AND IS NAMED AS COURTESY ONLY** — run 34600369729 on head `f50b3fc8`
      tested a test-merge onto `main` as it stood at 12:43:09Z (`38c076d1`), and
      `git merge-tree --write-tree 38c076d1 f50b3fc8` is
      `086ec4429380c46fe9596203a886e2c245737d0d`, which is NOT the merge commit's
      tree `91a3675a7fc0d586abeda2210999261f04d89391`; the base moved to
      `2cdaf06a` mid-run, so that run never tested this tree and the archive does
      not rest on it. Performed with `TZ=UTC python3 scripts/proposal-support.py
      . archive honour-grandfather-dispositions-in-ratified-provenance --date
      2026-09-11 --yes` through the pinned `@fission-ai/openspec@1.12.0`
      artifact — never a bare `openspec archive` — which moved the packet to
      `openspec/changes/archive/2026-09-11-honour-grandfather-dispositions-in-ratified-provenance/`
      and wrote the `## MODIFIED` block back into
      `openspec/specs/doc-health/spec.md`. The origin-retention gate fires INSIDE
      the wrapper and passed: **ORIGIN RETAINED**, the declaration unchanged
      since the ratifying commit **`e60ad2ff`**. The byte-for-byte identity this
      box requires is MEASURED — both sides sliced programmatically and hashed —
      and recorded in the pull request body rather than asserted here. The
      ratified text follows unchanged:
      **PROMOTE THE BLOCK INTO CANON**, byte-for-byte, in a SEPARATE pull
      request on a separate word, after § 1 is ruled and after the realization
      evidence this packet's `target_release` names: this pull request merged
      into `main` and a green `pytest-suite` run at the tree that merge carries
      (`release-realization`'s merged-plus-green rule, at canon's grain).
- [x] 6.2 **DONE — THE ONE CLOSING KEYWORD IS IN THIS ARCHIVE PULL REQUEST'S
      BODY AND NOWHERE ELSE.** The closing keyword against openxFactory issue
      939 is written ONCE, on its own line, in the BODY of the archive pull
      request and in no other place on this branch — not in this file, whose
      quotation of it here is deliberately written out of the live form so that
      no carrier but that body can ever be read as closing it. openxFactory #939
      was verified OPEN
      at the moment that pull request was opened, and its
      `closingIssuesReferences` is verified to be exactly `[939]`. **AND THIS
      BOX'S CLAIM ABOUT PR #945 HELD**: no closing keyword appeared in #945's
      body or in any commit message on its branch, in any form, case or tense,
      quoted or otherwise, so #939 survived that landing and closes here. No
      commit message on THIS branch carries one either — the same grep over all
      three messages. The ratified text follows unchanged:
      **THE ORIGIN ISSUE IS CLOSED AT THE ARCHIVE PULL REQUEST AND
      NOWHERE ELSE**, by a closing keyword written THERE against openxFactory
      issue 939. No closing keyword appears in this pull request's body or in
      any commit message on this branch, in any form, quoted or otherwise — a
      commit message auto-closes exactly as a body does, so the guard greps
      both.

## 7. Measured, and deliberately NOT taken here

- [x] 7.1 **NOT TAKEN, AND NOW CARRIED BY A FILED SUCCESSOR:
      [#965](https://github.com/opensoft/openxFactory/issues/965)**, UNCLAIMED.
      This box ticks by NAMING its successor and by nothing else — no
      stale-disposition check is written here, no finding class is graded, and
      no severity is chosen. **THE POPULATION IS RE-MEASURED AT THIS ARCHIVE
      RATHER THAN CARRIED**: at `opensoft/xFactory` `main`
      **`ecb0cade4573c2b1fea3c4d779cb3ad3afff1b14`**, `health/dispositions.yaml`
      is a **49**-entry list of which **18** carry `family: ratified-provenance`
      — **15 `openxFactory`, 3 `codexFactory`** — every one of the eighteen
      carrying a `cite`, a `date`, and a path under `openspec/changes/archive/`.
      The box's own `15 reported / 3 stale` split at the § 5.13 rig is the
      figure #965 records as its starting population. The ratified text follows
      unchanged:
      **A STALE-DISPOSITION CHECK.** An entry naming a path that no longer
      exists, or a record since repaired, matches nothing and is reported
      nowhere. Measured at the § 2.1 rig (`opensoft/xFactory` `bc84d325`,
      `codexFactory` `a67fb0ae`): all 18 entries matched a live finding, so
      that successor's population was ZERO. **IT IS NO LONGER ZERO, AND THE
      RE-MEASUREMENT IS RECORDED RATHER THAN LEFT TO BE DISCOVERED**: at the
      § 5.13 rig (`opensoft/xFactory` `f5dba67f`, `codexFactory` `ef180510`)
      codexFactory's three records have been REPAIRED and now carry a
      `Ratified:` citation, so they draw no finding and their three entries
      match nothing — `dispositioned AND reported: 15`, `dispositioned but NOT
      reported: 3`. That is this successor's population as of 2026-09-11, and
      it changes nothing in this packet: the rule is a set equality over
      whatever the file records and whatever the run reports, and the arm
      honours neither a stale entry nor an unrecorded finding. It is a new
      finding class with its own severity and its own population and belongs
      to its own act.
- [x] 7.2 **NOT TAKEN, AND NOW CARRIED BY A FILED SUCCESSOR:
      [#966](https://github.com/opensoft/openxFactory/issues/966)**, UNCLAIMED.
      No other family is taught to read that file here, none is downgraded, and
      none is suppressed. **THE COUNT IS RE-MEASURED AT THIS ARCHIVE**: at
      `opensoft/xFactory` `main` **`ecb0cade`**, **31 of the 49** entries belong
      to the other EIGHT families — `location-conformance` 10, `proposal-origin`
      8, `record-immutability` 5, `modified-block-currency` 4, and one each of
      `semantic-contradiction`, `semantic-normative-prose`,
      `uncited-resolution` and `document-catalog` — where this box recorded 22
      of 40 at the § 2.1 rig and 23 of 41 at the § 5.13 rig. The file has grown
      since; the re-measured figure is the one #966 carries. The ratified text
      follows unchanged:
      **THE OTHER SEVEN FAMILIES' ENTRIES** — 22 of the 40 at the § 2.1
      rig, 23 of the 41 at the § 5.13 rig. Whether any of them should
      be downgraded rather than suppressed — or read at all, for the families
      that read nothing — is a separate question about a different subject.
- [x] 7.3 **NOT TAKEN, AND NOW CARRIED BY A FILED SUCCESSOR:
      [#967](https://github.com/opensoft/openxFactory/issues/967)**, UNCLAIMED.
      `docs/doc-health.md` IS NOT EDITED BY THIS ARCHIVE. **THE ROW IS
      RE-READ AT THIS ARCHIVE AND STILL READS AS THIS BOX SAYS** — at `main`
      `34bb5c71`, `docs/doc-health.md` line **50** is the row
      *"3 | Ratified provenance | Every Ratified by: resolves to an existing
      OpenSpec change"*, which describes ONE of that family's five arms and none
      of the pass this packet added. A
      documentation sweep of that table is #967's act, not this one's. The
      ratified text follows unchanged:
      **`docs/doc-health.md`'s FAMILY TABLE ROW 3** still reads *"Every
      `Ratified by:` resolves to an existing OpenSpec change"*, which has been
      incomplete since the two-spelling ruling and is more incomplete now. A
      documentation sweep of that table, not this packet's act.
- [x] 7.4 **NOT TAKEN, AND NOW CARRIED BY A FILED SUCCESSOR:
      [#968](https://github.com/opensoft/openxFactory/issues/968)**, UNCLAIMED.
      No CLI surface, argument, contract line or test matrix is added here, and
      `design.md` D6's question — whether a run whose job is to report THIS
      repository's own defects should consult another repository's disposition
      file at all — is left open for #968 to answer rather than answered by an
      archive. **THE ASYMMETRY IS RE-MEASURED AT THIS ARCHIVE**: `python3
      scripts/doc-health.py --single-repo .` on `main` `34bb5c71` reports **28
      `ratified-provenance` rows, all `critical`, 0 `info`**, the grandfather
      pass being unreachable with `Context.agg_root is None` — the behaviour
      `test_a_single_repo_run_has_no_aggregation_root_and_nothing_moves` pins
      deliberately. The ratified text follows unchanged:
      **A `--single-repo` ROUTE TO AN AGGREGATION DISPOSITIONS FILE.** A CLI
      surface, an argument, a contract line and a test matrix, for a gate whose
      job is to report this repository's own defects (`design.md` D6).
