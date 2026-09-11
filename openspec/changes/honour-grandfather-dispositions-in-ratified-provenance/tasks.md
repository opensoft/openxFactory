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
      `all moved paths archived: True`. The only other line of the report that
      moves is the headline that sums the bands.
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
      **THE RE-READ APPLIES TWO PREDICATES OF ITS OWN AND BOTH ONLY NARROW**
      (added in the § 5.10 review round, and each with its own test): the
      entry must name THIS family — a finding carries `(repo, path)` and no
      third coordinate, so a `(repo, path)`-only lookup would let a
      NEIGHBOURING family's entry at the same path supply the citation, which
      is a shape the standing file HAS (`location-conformance` and
      `document-catalog` over one `ideation/staging/` path) — and it must carry
      the `date` § 4.3's scenario asks for, which the shared reader has never
      tested. Neither predicate honours an entry that reader would refuse.
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
- [x] 3.6 **NOTHING ELSE MOVES**: no arm, no document scope, no threshold, no
      resolution class, no other family, no report field, no workflow, no
      contract member, no schema, no path. `INFO` was already imported by this
      module and already spent by four families; the only import added is
      `dataclasses.replace`.
- [x] 3.7 `tests/doc-health/test_grandfather_dispositions.py` (**NEW, 19
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
      pinned EQUAL to the shared reader's over a five-entry file; the excerpt's
      one-line and bounded properties; and the downgraded row rendered by
      `report.plan_line(strict=True)` and read back by `report.PLAN_RE`,
      `report.unparsed_plan_rows` and `report.parse_previous`.
- [x] 3.8 **NO EXISTING TEST IS EDITED, RENAMED, FLIPPED OR DELETED.**
      `tests/doc-health` goes **1689 → 1708**, the whole rise being the new
      file. `test_ratification_record_subject.py`'s real-tree measurements are
      untouched by construction: they build their `Context` with
      `agg_root=None`, which is the scope this arm does nothing in.

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

- [ ] 5.1 `OPENSPEC_TELEMETRY=0 openspec validate
      honour-grandfather-dispositions-in-ratified-provenance --strict`.
- [ ] 5.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`, with the
      failure set compared against `origin/main`'s and the item count moving by
      exactly one.
- [ ] 5.3 **THROUGH THE PINNED CLI, WHICH IS THE ONE THE GATE RUNS**:
      `python3 scripts/validate-openspec-cli-pin.py --change … --no-cache` and
      the gate's literal `--all --no-cache`.
- [ ] 5.4 `python3 scripts/proposal-support.py . verify
      honour-grandfather-dispositions-in-ratified-provenance`.
- [ ] 5.5 `python3 scripts/validate-sequenced-after.py .` and `--ledger-diff`,
      the latter after the seed of § 4.6.
- [ ] 5.6 `python3 scripts/validate-scope-globs.py .`.
- [ ] 5.7 `python3 scripts/doc-health.py --single-repo .`, with the finding set
      compared LINE FOR LINE against `origin/main`'s — this arm does nothing in
      a single-repo scope, so the two must be identical.
- [ ] 5.8 `python3 -m pytest tests/doc-health tests/sequenced_after
      tests/scope_globs tests/proposal-support -q`, with the
      `tests/doc-health` count taken on this tree and on `origin/main` in the
      same shell.
- [ ] 5.9 **THE AGGREGATION MEASUREMENT RE-RUN ON THE FINAL TREE**, § 2.2
      through § 2.6 repeated after the last commit, so the figures in the pull
      request body describe the tree that merges rather than the tree they were
      first taken on.
- [ ] 5.10 **THE BOT BENCH, TAKEN AND ANSWERED ON THE RECORD.** Every thread
      is disposed with a reason, TAKEN or REFUSED, and a taken one is answered
      by a commit rather than by a reply.

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
