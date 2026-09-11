# Tasks: report-stale-grandfather-dispositions

Status: draft
Kind: tasks

**WHAT IS DONE HERE AND WHAT IS OWED, KEPT APART.** § 2 through § 5 are
performed in this pull request. § 1 (ratification) and § 6 (archive) are OWED
and are Brett Heap's acts on two separate later words. § 7 is what was measured
and deliberately NOT taken.

**NOTHING IN THIS PULL REQUEST PROMOTES ANYTHING.** No file under
`openspec/specs/` is edited by it, and openxFactory
[#965](https://github.com/opensoft/openxFactory/issues/965) is closed at the
ARCHIVE pull request and nowhere else.

## 1. Ratification — OWED, NOT GIVEN

- [ ] 1.1 **BRETT HEAP RULES `design.md` D1**, put as a MULTIPLE-CHOICE
      question with the recommendation FIRST: what a stale entry IS.
      **(1) RECOMMENDED — a PRUNE PROMPT**: a new finding class at `warning`
      against the aggregation's own `health/dispositions.yaml`, naming the
      entry's target and quoting the ruling, action *"prune the entry or
      re-point it"*, so the file converges on the set the run reports.
      **(2)** the EXPECTED RESIDUE of a repair, graded `info`, no action.
      **(3)** an AGGREGATION DEFECT at `error`.
      **THE PACKET ENCODES (1).** If (2) or (3) is taken, the delta's one
      `THEN` bullet is re-authored (`warning` → `info` or `error`), the action
      string in `families._STALE_ACTION` becomes a statement rather than an
      instruction under (2), and one constant moves in the arm; every test that
      names a band is re-measured. Under (3) the row also enters the regression
      axis and `--fail-on error`, and `design.md` D1 option 3 carries what that
      costs. Nothing else in this packet moves under any of the three.
- [ ] 1.2 **THE OTHER EIGHT DECISIONS ARE CARRIED BESIDE D1 AND EACH IS
      VETOABLE — EIGHT, COUNTED RATHER THAN CHARACTERISED, SO THE PACKET TAKES
      NINE IN ALL.** D0 (the measurement), D2 (a second last pass, after the
      first; the two narrowings; the row's subject; one row per honoured
      target; the `auto-fixable` class), **D2a** (the archived-path boundary is
      the FINDING's, so an entry over a CLEAN ACTIVE path IS reported — added
      in the PR #981 bench round), **D2b** (the scope is the lifecycle scan
      set's repositories and not `ctx.repo_paths`, because the aggregation's
      anchor is admitted on `is_dir()` alone — added in the same round, and the
      one item of that round taken as a CODE change), D3 (the tests extend the
      parent's rig), D4 (`code_surface` non-empty → archive on realization
      evidence), D5 (the limit to this family alone), D6 (the sibling search
      and `sequenced_after: []`). Each stands whichever way D1 goes, except that
      D2's band sentence follows D1. **Copilot's suppressed comment on PR #981
      caught this box saying "five" over a list of six labels; the count is now
      taken from the list and `proposal.md` and `design.md` name the same
      nine.**
- [ ] 1.3 **ON RATIFICATION, AND NOT BEFORE**: `.openspec.yaml` gains
      `approved_by` / `approved_on` as a pure ADDITION beside the unmoved
      `kind`, `id`, `reason`, `proposed_by` and `proposed_on`
      (`add-drafted-proposal-origin`, issue #318); every document's
      `Status: draft` becomes `Status: ratified` with a `Ratified:` /
      `Ratified by:` citation in a sanctioned spelling; and the record is
      written at `review/ratification-<date>.md` carrying `Status: ratified`
      itself, with the gate set re-derived on the ratified tree at
      `review/verification-<date>.md`.

## 2. The measurement, taken before the design

- [x] 2.1 **THE REAL AGGREGATION DISPOSITIONS FILE WAS READ, NOT MOCKED.**
      `opensoft/xFactory` `main` **`0ecb370e8fec2c1ac78498adf8f6a4ea3ca1c9bb`**
      cloned beside this checkout, with `openxFactory` and `codexFactory`
      materialized under it at the pins that aggregation holds — `b91af6ea` and
      `2dd4e5a3` — so `corpus.discover_repos` enumerates exactly the two
      repositories the file names. **49 entries across 9 families, 18 of them
      `family: ratified-provenance`** — 15 `openxFactory`, 3 `codexFactory`,
      every one carrying a `date` and a non-empty `cite`, and every one naming a
      path under `openspec/changes/archive/`.
- [x] 2.2 **BEFORE: 35 rows, 20 `critical` + 15 `info`.** `python3
      scripts/doc-health.py --repo-root <aggregation> --family
      ratified-provenance --as-of 2026-09-11` — exit 0, *"Findings: 20 critical,
      0 error, 0 warning, 15 info"*.
- [x] 2.3 **FIFTEEN ENTRIES MATCH A LIVE FINDING AND THREE MATCH NOTHING**, the
      difference taken as a SET rather than as a count: `dispositioned AND
      reported: 15`, `dispositioned but NOT reported: 3`, `of the honoured
      eighteen, archived-path: 18, non-archived: 0`, `by repo: openxFactory 15,
      codexFactory 3`, `stale by repo: codexFactory 3`.
- [x] 2.4 **EACH OF THE THREE IS STALE BY REPAIR, READ OFF THE RECORD.** All
      three name a `review/ratification-2026-09-05.md` that EXISTS in the
      checkout and now carries `Status: ratified` with a `Ratified:` line naming
      an approver and a date, so the citation arm is satisfied and no arm of
      this family opens a finding against it:
      `openspec/changes/archive/2026-09-05-add-floor-addition-grace/review/ratification-2026-09-05.md`,
      `openspec/changes/archive/2026-09-09-adopt-openspec-cli-pin-gate/review/ratification-2026-09-05.md`,
      `openspec/changes/archive/2026-09-09-prepare-openspec-1.12-readiness/review/ratification-2026-09-05.md`.
      **ZERO are stale by a VANISHED path** today; the arm reports both shapes
      because the absence is identical and its predicate is the absence.
- [x] 2.5 **THE SPLIT IS NOT AN ARTEFACT OF A LAGGING PIN.** The aggregation's
      `openxFactory` pin is **233 commits** behind that repository's
      `origin/main` at this authoring (`git rev-list --count
      b91af6ea..origin/main`), so the rig was rebuilt with each repository at
      its own `origin/main` — `openxFactory` **`8015d45f`**, `codexFactory`
      **`dc67ad82`** — and returns the **IDENTICAL** figures: 35 rows, 20
      critical / 15 info, 15 matched, 3 unmatched, the same three paths.
      **AND RE-TAKEN AT THE ENCODE**, both repositories having moved since:
      `openxFactory` **`c521504c`** (this branch's merge base; the pin is now
      **237** commits behind it) and `codexFactory` **`c3108adc`**. **IDENTICAL
      A THIRD TIME**: 18 honoured, 15 matched, **3 unmatched**, the same three
      codexFactory paths, `by repo: openxFactory 15, codexFactory 3`, 18
      archived / 0 non-archived. The aggregation is byte-unmoved —
      `opensoft/xFactory` `main` is still `0ecb370e` at the encode — so the
      file being measured did not move under the measurement either.
- [x] 2.6 **AFTER: 38 rows, 20 `critical` + 3 `warning` + 15 `info`**, the same
      35 rows plus three. **THE WHOLE REPORT DIFF IS 12 LINES**: the three new
      rows in each of the TWO places the report renders a finding
      (`## Findings By Family` and `## Ranked Plan`), the one headline line that
      sums the bands, and the diff's own hunk markers. No existing row moves —
      not a severity, not a rule, not an action, not a resolution class.
- [x] 2.7 **`kind: ad_hoc` IS CHECKED RATHER THAN ASSUMED.**
      `ideation/staging/` enumerated (**30** topic folders) and `INDEX.md` read
      on 2026-09-11: no topic names doc-health severity policy, the disposition
      mechanism, a stale-entry rule or ratification-record rules; the only
      `grandfather` hits are the credential-escrow registry's ruling C.
      `kind: staged` would claim a staging source that does not resolve.
- [x] 2.8 **NO SIBLING WRITES THIS REQUIREMENT** (`design.md` D6, pasted there
      in full): no active change carries a `## MODIFIED` block for *Governed
      corpus membership and the lifecycle scan set*; the two active changes with
      a `specs/doc-health/` delta write different requirements; of the six open
      pull requests only #962 touches a doc-health delta and its block is
      *Currency of an active change's MODIFIED requirement blocks*. Hence
      `sequenced_after: []`, and the archived parent needs no declaration
      because its text is CANON — promoted at **`bc1f25c4`** and read at
      `origin/main` `8015d45f`.
- [x] 2.9 **THE SIBLING SEARCH WAS RE-RUN AT `origin/main` `c521504c`**, after
      this branch took that tip, because a sibling authored in parallel is
      invisible to a search taken before it existed (`design.md` D6 carries the
      re-run pasted). **STILL NO COLLISION.** Nine pull requests are open;
      #966's own packet now exists —
      [#978](https://github.com/opensoft/openxFactory/pull/978) DRAFT,
      `change/decide-disposition-reading-per-family` at `59fb2047` — and its
      `## MODIFIED` block writes *Finding severity and regression handling*
      (canon line 198), NOT this packet's *Governed corpus membership and the
      lifecycle scan set* (canon line 878). The two deltas write disjoint bytes
      and **NO `sequenced_after:` IS DECLARED EITHER WAY**: that field names a
      change that exists on `main`, and #978's packet exists only on its own
      branch at this authoring — a branch-only parent is never declared. The
      one place the two touch is a CITATION: `design.md` D1 leans on the band
      vocabulary in the requirement #978 modifies, and #978 copies that body
      paragraph byte for byte and appends one scenario, so the sentence D1
      cites is unmoved either side of that landing (`design.md` D5).

## 3. The delta

- [x] 3.1 **ONE `## MODIFIED` BLOCK, BUILT BY SLICING CANON RATHER THAN BY
      TRANSCRIPTION.** `openspec/specs/doc-health/spec.md` lines **878–945** —
      *Governed corpus membership and the lifecycle scan set* — copied byte for
      byte, `sha256
      138a0d51f42f77aa9f0418c5ec1570681f63e0409bc0a43596e8356dca06e5dd` on both
      sides, RE-MEASURED after this branch took `origin/main` `c521504c`:
      `git show origin/main:openspec/specs/doc-health/spec.md | sed -n
      '878,945p' | sha256sum` and `sed -n '5,72p'` of this delta return that
      same digest, and `diff` of canon's 878–946 against this delta's 5–73
      exits 0. The canon file is byte-unmoved between `8015d45f` and
      `c521504c` (`git diff --stat` over it is empty). With ONE
      `#### Scenario:` appended at the end. No body paragraph is
      added, edited or removed; no promoted scenario moves, is retitled or loses
      a bullet.
- [x] 3.2 **NO MARKER IS DECLARED, THERE BEING NOTHING REMOVED TO DECLARE.** The
      block adds a scenario and removes no promoted unit, so the
      `Removed from canon` machinery is not reached and `modified-block-currency`
      has no marker to check.
- [x] 3.3 **THE ADDED SCENARIO IS *A recorded disposition matches no finding***,
      and it says SIX things: an honoured entry naming no finding this run
      raised is reported at `warning` against the dispositions file's own path,
      quoting the entry's target and the recorded citation; the finding is NOT
      raised against the record the entry names; an entry naming a repository
      the run READ NO DOCUMENT FROM is not reported (`design.md` D2b: the
      lifecycle scan set's repositories, not `ctx.repo_paths`); an entry this
      family would not
      honour is not reported either; an entry over a path outside
      `openspec/changes/archive/` that names no finding IS reported, that
      boundary belonging to the FINDING the downgrade moves rather than to the
      entry (`design.md` D2a, added in the PR #981 bench round); and a run with
      no aggregation checkout reports nothing of this class.
- [x] 3.4 **SHALL/MUST ON LINE ONE.** The requirement body's first line is
      canon's own — *"The doc-health capability SHALL declare two document sets
      and SHALL keep them distinct."* — unmoved, which is what the strict parser
      reads; every bullet of the added scenario carries its own MUST.

## 4. The realization — one second last pass, in this pull request

- [x] 4.1 `scripts/doc_health/families.py`: **`fam_ratified_provenance` RETURNS
      `graded + _stale_grandfather_dispositions(ctx, graded)`** where it
      returned `_honour_grandfather_dispositions(ctx, findings)`. One line
      becomes two; no arm above it moves.
- [x] 4.2 **`_stale_grandfather_dispositions(ctx, findings)` IS THE WHOLE
      ADDITION**: `set(_grandfather_cites(ctx))` minus `{(f.repo, f.path) for f
      in findings}`, narrowed to the repositories that contributed a document
      to `_lifecycle_scope(ctx)` (D2b — NOT `ctx.repo_paths`), one
      `Finding(WARNING, "ratified-provenance", "xFactory",
      "health/dispositions.yaml", …)` per remaining entry, the rule naming the
      entry's repository and path and the action quoting the ruling through the
      existing `_cite_excerpt`. Four module constants beside it —
      `_AGGREGATION_REPO`, `_DISPOSITIONS_REL`, `_STALE_RULE_PREFIX`,
      `_STALE_ACTION` — and one docstring paragraph on the family. **Nothing
      else in the module moves**: `_grandfather_cites`,
      `_honour_grandfather_dispositions`, `_cite_excerpt` and all five arms are
      byte-unmoved.
- [x] 4.3 **THE ROW'S TARGET IS COLLAPSED TO ONE LINE AT THE EMIT SITE.**
      `report.escape_field` quotes a `"` and a `\` and does not touch a newline,
      and an entry's `repo`/`path` are whatever a hand-edited YAML string holds,
      so a double-quoted scalar carrying `\n` would split the ranked-plan row
      into two lines that match no parser (issue #474's shape at a third field).
      `" ".join(f"{repo} {path}".split())` is that row's own guard, and
      `test_a_target_spelled_across_two_lines_still_reads_back` pins it.
- [x] 4.4 **TWELVE TESTS ADDED AND TWO EXISTING TESTS MOVED, EACH MOVE NAMED.**
      `tests/doc-health/test_grandfather_dispositions.py`: **22 → 34** test
      functions at the authoring, and **23 → 39** re-measured at the tip this
      branch now carries (`grep -c '^def test_'` on this tree and on an
      `origin/main` `d4d96cca` worktree beside it, the before-figure re-read as
      **23** again at `origin/main` `0805c3bb`; § 4.6 adds three more and § 4.7
      a fourth, and `main` itself added one to this file on #980 between the
      two measurements, which is why the BEFORE figure moved once). The two
      that move HERE are this change's own behaviour rather than repairs (§ 4.7
      carries the third, which is this packet's own test re-authored):
      (a) `test_an_undispositioned_archived_record_stays_critical` keeps its own
      assertion, narrowed to the record's own row, and GAINS the stale row its
      fixture's entry now earns — the fixture names a different archived path
      from the document under test, which is precisely the class;
      (b) `test_a_run_with_no_findings_reads_no_file` is SPLIT and renamed
      `test_the_downgrade_pass_still_returns_early_on_an_empty_finding_list` —
      the downgrade pass's early return still holds and is now asserted directly
      on that function, while the family-level no-read it used to imply is
      DELIBERATELY GIVEN UP, because a clean corpus is the extreme case of this
      class (every honoured entry matches nothing) and
      `test_a_clean_corpus_makes_every_in_scope_entry_stale` pins the new
      answer. **No test the repository already had before this packet is
      edited, renamed, flipped or deleted** — § 4.7's re-authoring is of a test
      this packet itself added.
      (c) `_doc` gains a `repo=REPO` keyword so a fixture can place a document
      in a SECOND repository, which § 4.7 needs; every existing call site is
      unmoved and reads the default.
- [x] 4.6 **THREE MORE TESTS IN THE PR #981 BENCH ROUND, ONE PER SUBSTANTIVE
      SUPPRESSED COMMENT OF COPILOT'S FIRST REVIEW** (its fourth was the § 1.2
      counting defect, repaired above; its SECOND review's two are § 4.7 and a
      restatement of (b)).
      (a) `test_the_stale_rows_operator_text_is_pinned_to_its_literal_wording`
      holds the emitted `action` and `rule` as LITERAL sentences instead of
      against `_STALE_ACTION` / `_STALE_RULE_PREFIX` imported from the module
      that builds them — a rewrite of the production wording moved both sides
      at once and stayed green, and the operator instruction is the very thing
      D1 option 1 buys.
      (b) `test_two_entries_at_one_target_report_the_one_row_the_reader_admits`
      pins the duplicate-target answer: `cites.setdefault(key, cite)` is the
      parent's landed line, BYTE-UNMOVED here, so two entries at one target
      report ONE row carrying the FIRST cite. TAKEN AS A TEST AND REFUSED AS A
      CODE CHANGE — a multimap here would report a residue the downgrade half
      cannot honour (§ 7.7).
      (c) `test_an_entry_naming_a_clean_active_path_is_reported_stale` pins
      `design.md` D2a. **ALL THREE PASS**, and no line of
      `scripts/doc_health/` moved for any of the three — those three are tests
      and prose only.
- [x] 4.7 **THE ONE CODE CHANGE OF THE BENCH ROUND: D2b's SCOPE NARROWING**
      (23 → **39** test functions in that file). `in_scope` in
      `_stale_grandfather_dispositions` becomes
      `{doc.repo for doc in _lifecycle_scope(ctx)}` in place of
      `set(ctx.repo_paths)` — ONE line, plus the docstring paragraph that says
      why. **MEASURED BOTH WAYS, WHICH IS WHY IT IS A TAKE AND NOT A REFUSE**:
      `scripts/doc-health.py --repo-root <root> --family ratified-provenance`
      over the standing `health/dispositions.yaml` (`opensoft/xFactory`
      `0ecb370e`) with `openxFactory/` present as an EMPTY DIRECTORY reports
      **15** stale `warning` rows under the old reading and **0** under the new
      one; against the fully materialized aggregation both readings report the
      SAME **15 matched / 3 stale**, exit 0. `corpus.discover_repos` is NOT
      moved — its anchor admission is every fixture aggregation's route in, and
      narrowing it would change what EVERY family measures.
      (a) `test_an_unmaterialized_anchor_reports_no_entry_of_its_own_as_stale`
      is ADDED and builds the shape directly: both repositories in
      `ctx.repo_paths`, both entries admitted by `_grandfather_cites`, an empty
      `_lifecycle_scope(ctx)`, zero stale rows.
      (b) `test_an_entry_naming_a_repository_out_of_scope_is_never_stale` — a
      test this packet ADDED at the authoring — is RE-AUTHORED, not repaired:
      its in-scope half now supplies a CLEAN codexFactory document, so the two
      halves still read one file under two scopes and the scope that moves is
      the new predicate's. Raised by Copilot on PR #981 (`families.py:618`),
      TAKEN.
- [x] 4.5 **THE COMPOSITION IS ASSERTED, NOT ARGUED.**
      `test_the_second_pass_returns_only_its_own_rows` holds that the second
      pass returns ONLY the rows it builds, that every graded row reaches the
      report as the downgrade left it (`is`, not `==`), and that the same
      difference taken over the UNGRADED finding list returns the same row —
      which is the mechanical form of canon's requirement that a grandfathered
      finding keep its family, repository and path.

## 5. Verification — DONE IN THIS PULL REQUEST

**EVERY GATE BELOW WAS RUN IN THE PACKET'S OWN CLONE AFTER IT TOOK
`origin/main` `c521504c`, AND EVERY ONE THAT CAN DIFFER WAS RUN A SECOND TIME
ON A `c521504c` CONTROL WORKTREE BESIDE IT**, so a failure is either this
packet's or already on `main` and the two are told apart by measurement rather
than by assertion.

- [x] 5.1 **`openspec validate report-stale-grandfather-dispositions --strict`
      ON THE `PATH` CLI (1.2.0) → EXIT 0.** *"Change
      'report-stale-grandfather-dispositions' is valid"*.
- [x] 5.2 **AND ON THE PINNED CLI (1.12.0) → EXIT 0.** `OPENSPEC_TELEMETRY=0
      python3 scripts/validate-openspec-cli-pin.py --change
      report-stale-grandfather-dispositions --no-cache`: the artifact's content
      address verified (`integrity sha512-oFE2Lj7WVSc87nSi…`), the dependency
      closure verified (80 packages, `lockfile_integrity sha512-aw5lIN45tQq2WZll…`,
      installed with `npm ci --ignore-scripts`), *"Totals: 1 passed, 0 failed
      (1 items)"*. **BOTH CLI GENERATIONS ACCEPT THE PACKET**, which is what
      the pin gate exists to establish.
- [x] 5.3 **`--all --strict` ON THE `PATH` CLI (1.2.0) → EXIT 1 ON BOTH SIDES
      WITH THE IDENTICAL FAILURE SET.** Branch: *"Totals: 101 passed, 2 failed
      (103 items)"*. Control at `c521504c`: *"Totals: 100 passed, 2 failed (102
      items)"*. The two failures are the SAME two on both sides —
      `change/disposition-codexfactory-declared-renames` and
      `change/disposition-codexfactory-floor-relocation-retitle` — so this
      packet adds ONE passing item and no failure. **THIS IS `main`'s STANDING
      STATE ON THE OLDER CLI AND NOT THIS PACKET'S DOING.**
- [x] 5.4 **`--all` THROUGH THE PIN (1.12.0) → EXIT 0 ON BOTH SIDES.**
      *"every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS
      NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS, named above"* —
      the same two accepted exceptions on the branch and on the control
      (`add-chain-attestation` / `signed-execution-chain`, and
      `add-composed-view-authoring` / `ideation-dashboard`), each carrying its
      recorded acceptance (*"accepted by: Brett Heap, 2026-09-05, 'take exit
      2'"*). **IDENTICAL, ENTRY FOR ENTRY.**
- [x] 5.5 **`python3 scripts/proposal-support.py . verify
      report-stale-grandfather-dispositions` → EXIT 0**, *"proposal support
      verification ok"*.
- [x] 5.6 **`python3 scripts/validate-sequenced-after.py .` → EXIT 0.**
      *"sequenced_after validation passed (41 active changes, 11 declaring the
      field)"* — this packet is one of the 41 and one of the 30 NOT declaring
      it; *"archive-date agreement passed"*; *"archive-date-vs-commit agreement
      passed (… 12 disposition(s) in force, enforcement error)"*.
- [x] 5.7 **`python3 scripts/validate-scope-globs.py .` → EXIT 0**,
      *"scope_globs validation passed (all active changes conform)"*.
- [x] 5.8 **`python3 scripts/doc-health.py --single-repo .` → EXIT 0, AND THE
      SELF-GATE HEADLINE IS BYTE-IDENTICAL TO THE CONTROL'S.** Branch and
      control at `c521504c` both: *"Findings: 32 critical, 7 error, 47 warning,
      14 info. New regressions vs previous report: 0."*, and the per-severity
      row counts agree exactly (32 / 7 / 47 / 14 each side). **ZERO findings
      name this packet** — `grep -c 'report-stale-grandfather-dispositions'`
      over the report returns **0**. This is the asymmetry `design.md` D2 and
      § 7.4 pin: a `--single-repo` run has no aggregation root, so the arm this
      packet adds reports nothing in this repository's own gate, and the
      self-gate is therefore expected to be unmoved.
- [x] 5.9 **`python3 -m pytest tests/doc-health -q --tb=no` → EXIT 0, 1723
      PASSED, 0 FAILED** (7 warnings, 398s). The control at `c521504c` in a
      worktree beside it: EXIT 1, **1710 passed, 1 failed**, and **THE ONE
      FAILURE IS THE CONTROL RIG'S AND NOT `main`'s** —
      `test_modified_block_currency_self_gate.py::test_the_resolver_fails_on_a_checkout_it_cannot_confirm_and_never_walks_up`
      (*"DID NOT RAISE UnresolvedRepository"*), which fails because the control
      is a WORKTREE NESTED INSIDE the packet's clone and the test's premise is a
      directory with no enclosing repository to resolve. That same test PASSES
      on the branch, which is a top-level clone. **COLLECTED: 1723 on the
      branch against 1711 on the control — a difference of exactly the TWELVE
      tests this packet adds.**
- [x] 5.10 **THE RIG FILE ALONE: `pytest
      tests/doc-health/test_grandfather_dispositions.py -q` → EXIT 0, 34
      PASSED** (0.41s). Counted rather than characterised: `git diff
      origin/main...HEAD` over that file shows **13** `+def test_` lines and
      **1** `-def test_` line — twelve NEW subjects plus the one rename § 4.4
      names (`test_a_run_with_no_findings_reads_no_file` →
      `test_the_downgrade_pass_still_returns_early_on_an_empty_finding_list`) —
      so 22 − 1 + 13 = **34**, and `grep -c '^def test_'` returns 22 at
      `origin/main` `c521504c` and 34 here.
- [x] 5.11 **THE WHOLE CODE SURFACE IS TWO FILES.** `git diff --stat
      origin/main...HEAD -- scripts tests` → *"2 files changed, 454
      insertions(+), 20 deletions(-)"*, and `--numstat` splits it exactly:
      `scripts/doc_health/families.py` **109 added / 1 removed** (the one
      removed line is the family's old one-line `return`) and
      `tests/doc-health/test_grandfather_dispositions.py` **345 added / 19
      removed**. No other module, no other test file, no workflow, no contract,
      no schema, no path.
- [x] 5.12 **THE PACKET'S OWN SPEC DELTA IS CANON'S BYTES, VERIFIED BY `diff`
      AND BY DIGEST AFTER THE MERGE.** `git show
      origin/main:openspec/specs/doc-health/spec.md | sed -n '878,946p'`
      against this delta's lines 5–73: `diff` exits **0**. Over 878–945 and
      lines 5–72 the digest is
      `138a0d51f42f77aa9f0418c5ec1570681f63e0409bc0a43596e8356dca06e5dd` on both
      sides. The canon file is byte-unmoved between `8015d45f` and `c521504c`
      (`git diff --stat` over it is empty), so the slice this packet took before
      the merge is the slice it carries after it.

## 6. Archive — OWED, NOT GIVEN

- [ ] 6.1 **`code_surface` IS NON-EMPTY, SO THIS PACKET DOES NOT ARCHIVE ON
      LANDING.** `release-realization`'s *Realization archive gate*: *"A change
      with a non-empty code surface SHALL NOT archive until realization evidence
      exists: its code merged on the implemented target through the owning
      domain's engineering gates, and — where the surface is runnable — a green
      run of that surface."* The realization rides THIS pull request, so the
      evidence is this pull request MERGED into `main` plus a green
      `pytest-suite` run at the tree that merge carries.
- [ ] 6.2 **THE EVIDENCE IS CITED AT CANON'S GRAIN, WHICH IS THE TREE.** `main`'s
      post-merge suite run is routinely cancelled by the next landing, so the
      citable run is this pull request's own green run on `refs/pull/N/merge`
      TOGETHER WITH proof that the merge commit's tree is the tree that ran (the
      base not having moved between the run and the merge). A bare "it was green
      on the branch" is not the evidence this gate asks for.
- [ ] 6.3 **THE PROMOTION IS PART OF THE ARCHIVE ACT AND NOT OF THIS ONE.** The
      `## MODIFIED` block is applied to `openspec/specs/doc-health/spec.md`
      THERE, by `proposal-support.py`, after the ratification of § 1 and on
      Brett Heap's separate archive word. This pull request edits no file under
      `openspec/specs/`.
- [ ] 6.4 **THE ORIGIN ISSUE IS CLOSED AT THE ARCHIVE PULL REQUEST AND NOWHERE
      ELSE**, by a closing keyword written THERE against openxFactory issue 965.
      No closing keyword appears in this pull request's body or in any commit
      message on this branch, in any form, quoted or otherwise — a commit
      message auto-closes exactly as a body does, so the guard greps both.

## 7. Measured, and deliberately NOT taken here

- [ ] 7.1 **THE OTHER EIGHT FAMILIES' ENTRIES ARE NOT READ FOR STALENESS**, and
      the count is measured rather than carried: at `opensoft/xFactory` `main`
      `0ecb370e`, **31 of the 49** entries belong to the other eight families —
      `location-conformance` 10, `proposal-origin` 8, `record-immutability` 5,
      `modified-block-currency` 4, and one each of `semantic-contradiction`,
      `semantic-normative-prose`, `uncited-resolution` and `document-catalog`.
      Whether any of them should be read for staleness — and for several of
      them, whether their entries are read at all — is
      [#966](https://github.com/opensoft/openxFactory/issues/966)'s subject.
      **#966 IS NOW CLAIMED AND ITS PACKET IS OPEN** —
      `decide-disposition-reading-per-family`,
      [#978](https://github.com/opensoft/openxFactory/pull/978), DRAFT at
      `59fb2047` — and it writes a DIFFERENT requirement, so it collides with
      nothing here (`design.md` D5, `tasks.md` § 2.9). The arm here is narrow by CONSTRUCTION and
      not by convention: `_grandfather_cites` asks the shared reader for this
      family's key set alone, so an entry naming another family is not in the
      map this pass takes the complement of.
- [ ] 7.2 **THE UNRECORDED-FINDING HALF OF THE SET EQUALITY IS NOT TAKEN.** A
      finding that SHOULD be dispositioned and is not draws its own arm's
      severity and nothing says the file is missing an entry. That is the other
      direction of the same comparison, it is a question about the file's
      completeness rather than its currency, and it belongs to its own act.
      Measured at `0ecb370e` over rig A: **20** `critical` rows of this family
      carry no entry, which is the correct answer for every one of them and is
      exactly why the completeness half needs a rule before it needs an arm.
- [ ] 7.3 **AN ENTRY NAMING AN ACTIVE PATH IS NOT A SEPARATE CLASS HERE.**
      `design.md` D2 of the archived parent rules that a disposition NEVER
      downgrades a finding against an ACTIVE packet's record, so such an entry
      is inert by construction — but it still MATCHES the `critical` row that
      stands, so it is not residue and draws no stale row. Whether an entry the
      boundary can never honour deserves a class of its own is left open;
      measured at `0ecb370e`, the population is **ZERO** — all 18 entries name
      archived paths — and
      `test_an_active_path_entry_whose_finding_stands_is_not_stale` pins the
      behaviour either way. **THE OTHER HALF OF THAT SAME BOUNDARY IS NOW A
      NAMED DECISION**: an entry over an active path whose record is CLEAN
      draws no finding to match, so it IS reported stale. `design.md` D2a
      carries the alternative (filter the complement by the archive prefix)
      with its cost, and
      `test_an_entry_naming_a_clean_active_path_is_reported_stale` pins the
      encoded reading. Raised by Copilot on PR #981 (`families.py:619`).
- [ ] 7.4 **`--single-repo` IS STILL GIVEN NO ROUTE TO AN AGGREGATION
      DISPOSITIONS FILE.** A CLI surface, an argument, a contract line and a
      test matrix, for a gate whose job is to report this repository's own
      defects — left to
      [#968](https://github.com/opensoft/openxFactory/issues/968), which is
      OPEN and unclaimed at this authoring (no branch, no pull request), and
      pinned unchanged here by
      `test_a_single_repo_run_reports_no_stale_entry`.
- [ ] 7.5 **`docs/doc-health.md` IS NOT EDITED.** Its family-table row 3 still
      reads *"Every `Ratified by:` resolves to an existing OpenSpec change"*,
      which has been incomplete since the two-spelling ruling, was more
      incomplete after the grandfather pass and is more incomplete again now. A
      documentation sweep of that table is
      [#967](https://github.com/opensoft/openxFactory/issues/967)'s act, named
      by the parent's § 7.3. **THAT SWEEP IS NOW OPEN AS ITS OWN PULL
      REQUEST** — [#977](https://github.com/opensoft/openxFactory/pull/977),
      `docs/967-doc-health-family-table-currency` — and it is not this packet's
      act: this branch does not edit `docs/doc-health.md` at all, so the two do
      not touch the same bytes.
- [ ] 7.7 **A DUPLICATE TARGET IS NOT GIVEN A ROW PER LINE.** Where one
      `(repo, path)` carries two entries of this family, `_grandfather_cites`
      keeps the FIRST (`cites.setdefault(key, cite)` — the parent's landed
      line, BYTE-UNMOVED by this change), so the two downgrade one finding
      between them and are reported stale as one row between them. Reporting a
      row per LINE would require the SHARED reader to return a multimap, which
      would change what the DOWNGRADE honours — the one thing this packet
      states it does not do — and would report a residue the downgrade half
      cannot reach. **MEASURED at `opensoft/xFactory` `0ecb370e`: 49 entries,
      **49 DISTINCT** `(family, repo, path)` triples — the shape does not exist
      today, in this family or in any other.** Pinned either way by
      `test_two_entries_at_one_target_report_the_one_row_the_reader_admits`.
      Raised by Copilot on PR #981 (`families.py:621`).
- [ ] 7.6 **NO ENTRY IS PRUNED AND NO RECORD IS TOUCHED.**
      `health/dispositions.yaml` lives in `opensoft/xFactory` and this pull
      request does not edit it. The three entries this authoring measures as
      stale are reported, not removed: pruning them is the lifecycle owner's
      act in that repository, on that repository's own pull request.
- [ ] 7.8 **`corpus.discover_repos` IS NOT NARROWED, THOUGH D2b IS ABOUT ITS
      ASYMMETRY.** The aggregation's ANCHOR is admitted on `is_dir()` while
      every other pinned repository must pass `_is_materialized_repo`, and that
      laxness is what lets an unmaterialized `openxFactory` pin enumerate as a
      repository the run reads nothing of. Tightening it there would be the
      general fix — and it would change what EVERY family measures, close every
      fixture aggregation in this suite out of its own anchor (the admission's
      own docstring says that is why it is lax), and put a one-line enumerator
      change inside a packet whose declared surface is one second last pass on
      one family. **This packet narrows only what IT reports** (`design.md`
      D2b) and leaves the enumerator byte-unmoved; whether the anchor's
      admission should be tightened, and what an aggregation run should do when
      its anchor is empty, is a question for the enumerator's own change with
      its own estate-wide gate run. Measured cost of leaving it: **ZERO** rows
      in this family, the narrowing above making the anchor's laxness
      unreachable from this pass.
