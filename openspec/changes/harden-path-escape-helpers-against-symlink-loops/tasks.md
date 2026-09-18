# Tasks: harden-path-escape-helpers-against-symlink-loops

Status: ratified
Ratified: 2026-09-18, approximately 09:55Z by Brett Heap (openxFactory
repository owner) — verbatim "Ratify; land when green" (record
`review/ratification-2026-09-18.md`)
Kind: tasks

`code_surface: openxFactory`, `target_release: implemented`. The realization
group is § 3 and it is **NOT IN THIS PULL REQUEST**, which carries the PACKET
ONLY. The tasks are individually executable, so under `release-realization`'s
decomposition rule this packet realizes through its own task list rather than
through a feature DAG.

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in this
pull request or a measurement recorded verbatim in this packet and reproducible
from the commands named beside it. **§ 1 IS BRETT HEAP'S ACT AND IS NOT TICKED BY
THIS LANE.** § 3, § 4, § 5 and § 6 stay ENTIRELY OPEN.

## 1. Ratification — GIVEN 2026-09-18, Brett Heap's and nobody else's

- [x] 1.1 **(OPERATOR)** Ratify or refuse `proposal.md` § *The decision, put for a
      veto* (OQ-1): option (a) AS FILED (`design.md` D1 ADDED over
      `release-realization`, D2 one act across all four sites, D3 widen
      `_registry_present` too, D4 scope by containment ROLE), or (b) narrow D3, or
      (c) narrow D2 to `code_surface.py` alone, or (d) widen D4 to every
      `except OSError:` in the three modules. Ratifying (a) moves no byte of the
      delta; the packet's three lifecycle documents then take `Status: ratified`
      with one citation line each, `.openspec.yaml` gains
      `approved_by`/`approved_on` ADDED BESIDE the unmoved drafting pair, and a
      `review/ratification-<date>.md` record is written.
      **RULED (a) — Brett Heap, 2026-09-18, approximately 09:55Z, verbatim
      "Ratify; land when green"**, given in the lane's terminal as a
      multiple-choice answer to lane `openxfactory-5` (session `651195c7`); no
      GitHub comment carries this word (`review/ratification-2026-09-18.md`).
      **DONE** in this same commit: `proposal.md`, `design.md` and this file
      take `Status: ratified` with a citation line each, `.openspec.yaml`
      gains `approved_by`/`approved_on` beside the unmoved `proposed_by`/
      `proposed_on`, and `review/ratification-2026-09-18.md` records the word
      in full.
- [x] 1.2 **(OPERATOR)** The ratifying word authorizes the REALIZATION (§ 3) to be
      authored. It does not authorize the ARCHIVE (§ 5), which is a separate act
      on a separate word and on merged-plus-green evidence.
      **SATISFIED by the word itself**: `Ratify; land when green` reaches
      exactly § 3 (may now be authored, as a later pull request) and not § 5
      (stays closed behind merged-plus-green realization evidence and its own
      word). "Land when green" is a MERGE authorization over this pull
      request once its checks are green, a separate act performed by whoever
      holds it — this lane refreshes the packet and does not merge it.

## 2. Measurement (CLOSED in this pull request)

- [x] 2.1 Interpreter measured, not assumed: `.github/workflows/pytest-suite.yml:556`
      pins `python-version: "3.12"`; the measuring shell is `Python 3.12.3`.
      `Path.resolve(strict=True)` raises `RuntimeError` for a symlink loop at the
      LEAF and at a PARENT COMPONENT alike; `RuntimeError` is a subclass of
      neither `OSError` nor `ValueError`. Transcript in `design.md` D0.1.
- [x] 2.2 All four sites re-read on `c6997f12` and called directly against a real
      `a -> b -> a` loop: `code_surface._unescaped` (`:746`, clause `:777`),
      `target_release._unescaped` (`:600`, clause `:630`),
      `target_release._registry_present` (`:354`, clause `:394`),
      `proposal-support._contained` (`:341`, clause `:347`). Transcript in
      `design.md` D0.2.
- [x] 2.3 THE THREE REACHABLE SITES DRIVEN END TO END through their shipped entry
      points, on TWO minimal trees carrying a committed-shape loop (one with the
      loop on `proposal.md`, one with it on `.openspec.yaml`), through FOUR entry
      points, ALL FOUR ending in a traceback: `scripts/validate-code-surface.py`
      and `scripts/validate-target-release.py` on the first tree, and
      `proposal-support`'s `former_identity_claimants` and
      `declared_former_ids_in_tree`, the two public readers the archive gate's
      former-identity arm is built on, on the second. A FIFTH reader was driven
      and did NOT traceback: `contained_change_dir_names` returned
      `{'a-real-change'}` on the second tree, never reaching the loop, and that
      answer is a result this packet's realization must PRESERVE and not turn
      into a drop. Transcript in `design.md` D0.3.
- [x] 2.4 Reachability measured rather than asserted: `code_surface._proposals`
      absorbs a loop at a CHANGE DIRECTORY name through its `is_dir()` filter; the
      reachable committed shapes are `<change>/proposal.md`,
      `<change>/.openspec.yaml`, and a loop at `openspec`, `openspec/changes` or
      `openspec/changes/archive`. `design.md` D0.4.
- [x] 2.5 **#1074's own text CORRECTED by measurement**: `_registry_present` is
      NOT reachable when the repository root sits behind a loop either, because
      `is_dir()` answers `False` rather than raising, so the function returns at
      `target_release.py:390`. Re-measured in ALL THREE positions the first
      requirement names, a loop at the registry LEAF, a loop at the ANCESTOR
      `contracts/`, and `repo_root` itself a loop: `False` in every one. And
      where the pre-check passes, `stat` has just resolved every component, so
      the resolution on `:392` cannot meet a loop either. THE FOURTH SITE IS A
      CLAUSE-LEVEL, RACE-ONLY CASE, not a tree state, which is the count the
      other three documents now carry. `design.md` D0.5; consequence decided at
      D3.
- [x] 2.6 Packet authored at
      `openspec/changes/harden-path-escape-helpers-against-symlink-loops/`:
      `proposal.md` (front matter `code_surface: openxFactory`,
      `target_release: implemented`, `sequenced_after: []`), `design.md`,
      `tasks.md`, `.openspec.yaml` (ad-hoc origin declared through
      `python3 scripts/proposal-support.py . declare-adhoc`, drafting provenance
      only, no approval pair claimed), and ONE `## ADDED` spec delta under
      `specs/release-realization/`.
- [x] 2.7 Sibling search taken before the root claim was written: neither ADDED
      title appears in `openspec/specs/`, in any other active change's delta, or
      in the archive, and this delta carries no `## MODIFIED` block, so no
      `sequenced_after` antecedent under *Ordered deltas and branch vocabulary*
      applies and no modified-block-currency row is opened. `sequenced_after: []`
      is a CORROBORATED root claim.
- [x] 2.8 README "OpenSpec Records → Active changes" bullet added.
- [x] 2.9 Per-change sweep-ledger row seeded from the live corpus through the
      sanctioned tool
      (`python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#<PR>'`)
      in a SECOND commit after the pull request existed, the pull request number
      being unknowable in the first.
- [x] 2.10 Gate transcripts recorded in the pull request body: `openspec validate`
      (this change `--strict`, and `--all --strict`),
      `scripts/validate-code-surface.py .`, `scripts/validate-scope-globs.py .`,
      `scripts/validate-sequenced-after.py . --ledger-diff`,
      `scripts/validate-openspec-cli-pin.py --all`, the four test packages, and
      `scripts/doc-health.py --single-repo .` diffed against the same clone at
      `origin/main`, with the pre-existing failures of `origin/main` named as such.

## 3. Realization (OPEN; a LATER pull request on the ratifying word)

**The fails-then-passes standard applies to every slice: the failing run against
the unfixed clause is recorded beside the passing run against the widened one,
and a test that passes on both sides is not the proof.**

- [x] 3.1 `scripts/code_surface.py`: `_unescaped`'s clause widened to
      `except (OSError, RuntimeError):`, and its docstring amended to name
      `RuntimeError` beside `OSError` as a failure this guard closes, keeping its
      written claim that `target_release._unescaped` "is the exact shape this
      mirrors" TRUE.
      **DONE, commit `17390262` (PR #1107)**: the clause reads
      `except (OSError, RuntimeError):` at `scripts/code_surface.py:791` (the
      docstring's own growth moves the line off the packet's `:777`
      measurement; the two resolutions it guards are unmoved). The docstring
      now reads "`Path.resolve(strict=True)` reports a missing or unreadable
      component as an `OSError` and a SYMLINK LOOP as a `RuntimeError` … A
      clause naming only `OSError` is open at exactly the loop" and still
      closes "`target_release._unescaped` is the exact shape this mirrors" —
      kept TRUE because `target_release._unescaped`'s own clause widens in the
      SAME commit (§ 3.3). `git show 17390262 --numstat --
      scripts/code_surface.py`: `15  1`.
- [x] 3.2 `tests/code_surface/`: one test that builds an `a -> b -> a` loop under
      `tmp_path`, in ALL THREE exposed positions the first requirement names (the
      candidate's own leaf; a parent component above an ordinary leaf; and the
      SCANNED ROOT itself, `spec.md`'s third scenario), and asserts `_unescaped`
      returns `None` in each. In that third position the loop is reached through
      the CANDIDATE and never through a separate root read: `candidate =
      repo_root / relative` traverses the loop, so `code_surface.py:775` raises
      and the root resolution on `:776` is never executed. Measured, not assumed;
      the transcript is `design.md` D5. Recorded failing against `c6997f12`'s
      clause.
      **DONE, commit `4892fa5f` (PR #1107)**:
      `tests/code_surface/test_code_surface_gate.py::test_a_symlink_loop_drops_the_candidate_in_all_three_positions`,
      all three positions in one test, `_unescaped(...) is None` asserted in
      each. THE PAIR OF RUNS (`python3 -m pytest … -k symlink_loop -v`,
      `Python 3.12.3`, PR #1107 body carries the full transcript): against
      `c6997f12`'s unfixed clause — `RuntimeError: Symlink loop from
      '…/leaf/openspec/changes/a-packet/proposal.md'` out of
      `code_surface.py:775`, FAILED; against this commit's widened clause —
      PASSED. The three-position, three-package run: `4 failed, 448
      deselected` then `4 passed, 448 deselected`.
- [x] 3.3 `scripts/target_release.py`: `_unescaped`'s clause and
      `_registry_present`'s clause both widened to `except (OSError, RuntimeError):`,
      and both docstrings amended, `_unescaped`'s keeping its claim to generalize
      `_registry_present`'s test TRUE.
      **DONE, commit `17390262` (PR #1107)**: `_registry_present`'s clause at
      `scripts/target_release.py:413` (packet's `:394`) and `_unescaped`'s at
      `:663` (packet's `:630`) both read `except (OSError, RuntimeError):`;
      both docstrings amended to name `RuntimeError`. `_unescaped`'s docstring
      keeps its opening claim, "THIS IS `_registry_present`'S TEST,
      GENERALIZED TO ANY PATH THIS MODULE OPENS", TRUE because both clauses
      widen together in this one commit. `git show 17390262 --numstat --
      scripts/target_release.py`: `35  2`.
- [x] 3.4 `tests/target_release/`: TWO cases, which is why the realization is FOUR
      TEST CASES IN THREE PACKAGES and not one per module. One for `_unescaped` in
      all three positions, as 3.2; and one for `_registry_present` DECLARED AS A
      TEST OF THE CLAUSE (`design.md` D3, D0.5), since no tree state reaches it,
      with the declaration in the test's own docstring and not only in this
      packet, and driven by a seam that makes the pre-check pass while the
      resolution fails, so it still FAILS against the unfixed clause. The
      scanned-root position is no exception for that guard: measured, a root set
      to the loop returns `False` at the `is_dir()` pre-check exactly as the other
      two positions do, so it is D3's one clause test and not a fourth POSITION.
      **DONE, commit `4892fa5f` (PR #1107)**: TWO cases in
      `tests/target_release/test_target_release_gate.py` —
      `test_a_symlink_loop_drops_the_candidate_in_all_three_positions` (the
      `_unescaped` case, as § 3.2) and
      `test_a_symlink_loop_at_the_registry_is_absent_and_never_raises` (the
      `_registry_present` CLAUSE test, declared as one in its own docstring,
      seamed so the `is_dir()` pre-check passes and the resolution meets a
      real loop). Against the unfixed clause: `RuntimeError` at
      `target_release.py:392` (the seamed clause test) and `:628` (the
      `_unescaped` case) — FAILED; against the widened clause — PASSED (same
      pair-of-runs transcript as § 3.2).
- [x] 3.5 `scripts/proposal-support.py`: `_contained`'s clause widened to
      `except (OSError, ValueError, RuntimeError):`, the `ValueError` guarding the
      relative-path computation's own failure and STAYING; `contained_dir` and
      `contained_file` docstrings amended to name the set.
      **DONE, commit `17390262` (PR #1107)**: `_contained`'s clause at
      `scripts/proposal-support.py:370` (packet's `:347`) reads
      `except (OSError, ValueError, RuntimeError):` — the `ValueError` kept for
      the relative-path computation's own failure, `RuntimeError` added beside
      it; `contained_dir` and `contained_file` docstrings amended to name the
      set. `git show 17390262 --numstat -- scripts/proposal-support.py`:
      `24  1`.
- [x] 3.6 `tests/proposal-support/`: one test that builds the loop under `tmp_path`
      and asserts `contained_dir` and `contained_file` return `False`, in all
      three positions. `_contained` is the ONE guard of the four whose ROOT read
      is reachable on its own, because it resolves the candidate first and the
      root separately inside `relative_to`: with a real path as the candidate and
      the loop as the root, `proposal-support.py:343` succeeds and `:346` raises.
      That clean-candidate sub-case is asserted HERE and claimed nowhere else.
      **DONE, commit `4892fa5f` (PR #1107)**:
      `tests/proposal-support/test_proposal_support.py::DeclaredFormerIdTests::test_a_symlink_loop_is_uncontained_in_all_three_positions`,
      `contained_dir`/`contained_file` both asserted `False` in all three
      positions, including the clean-candidate sub-case (a real candidate
      under an unresolvable root) claimed nowhere else. Built under
      `TemporaryDirectory()`, this package's own `tmp_path` — noted in the PR
      body as the one letter-level departure the module's pure-`unittest`
      shape (ending `unittest.main()`, no pytest fixture use anywhere in it)
      requires. Against the unfixed clause: `RuntimeError` at
      `proposal-support.py:343` — FAILED; against the widened clause —
      PASSED (same pair-of-runs transcript as § 3.2).
- [x] 3.7 **NO SYMLINK IS ADDED TO THE TRACKED TREE.** Verified in the realization
      pull request by `git ls-files -s | awk '$1 == "120000"'` returning nothing,
      and recorded in its body.
      **PROVEN, re-run at the merged head `87eb684d`** (PR #1107, the commit
      merging `origin/main` (`ebcdbc0c`, #1083's landing) into this branch):
      `git ls-files -s | awk '$1 == "120000"'` returns nothing; piped to
      `wc -l`, `0`. Every loop §§ 3.2/3.4/3.6 build lives under a test-time
      `tmp_path`/`TemporaryDirectory()` and is torn down with it; none is
      committed.
- [x] 3.8 **NO OTHER FILE MOVES.** No validator arm, no existing test, no
      workflow, no contract member, no schema, no report field, no promoted byte,
      and none of the ELEVEN non-containment `except OSError`-family clauses
      `design.md` D4 enumerates (`proposal-support.py:3724` among them), nor
      `proposal-support.py:3939`'s already-wider `except Exception:`.
      **PROVEN, re-run at the merged head `87eb684d`**: `git diff --stat
      origin/main` names exactly six files —
      `scripts/code_surface.py` (`+15/-1`), `scripts/proposal-support.py`
      (`+24/-1`), `scripts/target_release.py` (`+35/-2`), and the three test
      files (`+76`, `+95`, `+124`, each `-0`) — `6 files changed, 369
      insertions(+), 4 deletions(-)`; identical whether the diff is scoped to
      `scripts/ tests/` or left unscoped, so the merge itself carries no
      further diff against `origin/main`. `git diff -U0 origin/main --
      scripts/` removes exactly four lines, the four widened clauses
      (`except OSError:` × 3, `except (OSError, ValueError):` × 1); `git diff
      -U0 origin/main -- tests/` removes nothing — no existing test is
      edited, renamed, flipped or deleted. The eleven other clauses
      `design.md` D4 enumerates and `proposal-support.py:3939`'s
      `except Exception:` do not appear in the diff.

## 4. Verification (OPEN; taken at the realization head)

- [x] 4.1 `python3 -m pytest tests/code_surface tests/target_release tests/proposal-support -q`
      green, with the FOUR new test cases' failing runs against the unfixed
      clauses recorded beside them. FOUR, one per clause, in THREE packages: one
      in `tests/code_surface/` (§ 3.2), TWO in `tests/target_release/` (§ 3.4),
      one in `tests/proposal-support/` (§ 3.6). The count is the realization
      plan's and the same number is carried in `proposal.md`'s `code_surface:`
      front matter.
      **GREEN, re-run at the merged head `87eb684d`** (clone root, `Python
      3.12.3`): `452 passed, 297 subtests passed in 93.65s`. PR #1107's own
      body records this same command pre-merge as `452 passed, 296 subtests
      passed`; the +1 subtest is
      `DeclaredFormerIdTests::test_every_packet_in_this_corpus_reads_its_declaration_cleanly`
      (`tests/proposal-support/`) now also counting the
      `harden-path-escape-helpers-against-symlink-loops` directory the merge
      admits — the merge's other packet-directory change,
      `add-doxchat-model-intake` → `archive/2026-09-16-add-doxchat-model-intake`,
      is a pure rename this active-plus-archived sweep already counted either
      way. No file under §§ 3.2/3.4/3.6 changed. The four failing-then-passing
      cases are §§ 3.2/3.4/3.6's own transcripts: `4 failed` against
      `c6997f12`'s clauses, `4 passed` against this branch's.
- [x] 4.2 `python3 scripts/validate-code-surface.py .`,
      `python3 scripts/validate-target-release.py .` and
      `python3 scripts/proposal-support.py . verify` green over the live corpus,
      proving the widened clauses changed no judgment of the real tree.
      **GREEN, re-run at the merged head `87eb684d`** (clone root):
      `validate-code-surface.py .` → `code_surface: 48 active proposals, 48
      declaring — 7 \`none\`, 33 a repository list, 8 named by the register,
      0 outside the grammar.` … `code_surface validation passed`, exit 0;
      `validate-target-release.py .` → `target_release: 48 active proposals,
      48 declaring — 24 \`implemented\`, 2 a named release, 1
      \`deferred-allocation\`, 21 named by the register, 0 outside the
      vocabulary.` … `target_release validation passed`, exit 0;
      `proposal-support.py . verify` → `proposal support verification ok`,
      exit 0. `0 outside the grammar` / `0 outside the vocabulary` in both
      runs is what § 4.2 asks for — the widened clauses changed no judgment;
      the archive/active sub-counts differ in the low single digits from the
      PR body's pre-merge snapshot only because `origin/main` carried its own
      commits (this packet's landing among them) between that snapshot and
      this merge.
- [x] 4.3 The TWO end-to-end trees of `design.md` D0.3 re-run against the
      realization head, through the FOUR entry points that traceback today:
      `scripts/validate-code-surface.py` and `scripts/validate-target-release.py`
      on the `proposal.md` loop tree, `former_identity_claimants` and
      `declared_former_ids_in_tree` on the `.openspec.yaml` loop tree. Each of the
      four now REPORTS rather than tracebacks, and the reported judgment is the
      drop each guard's docstring promises. `contained_change_dir_names` is
      re-run beside them and MUST STILL RETURN `{'a-real-change'}`, the answer
      D0.3 already records: it never reached the loop, so the widening must not
      turn its result into a drop. An unchanged result is part of the evidence
      here and not an omission from it.
      **PROVEN, re-built and re-run at the merged head `87eb684d`.** TREE ONE
      (`<tmp>/tree_one/openspec/changes/a-real-change/proposal.md`, a
      two-link `a -> b -> a` loop, confirmed genuine —
      `Path(...).resolve(strict=True)` raises `RuntimeError: Symlink loop
      from …`): `validate-code-surface.py <tree one> --register <tree-scoped
      empty register.yaml>` → `code_surface: 0 active proposals, 0 declaring
      … validation passed`, exit 0; `validate-target-release.py <tree one>
      --register <same>` → `target_release: 0 active proposals, 0 declaring
      … validation passed`, exit 0. (The `--register` names a fresh
      `register: []` file, exactly the shape `tests/code_surface/`'s own
      `_register()` tree builder writes by default, so the run judges only
      the loop and not this repository's own register against a four-file
      fixture tree; run with no `--register` the two validators instead
      compare the fixture tree against THIS repository's real register and
      correctly report every real entry `stale` — a true finding about the
      fixture, not about § 4.3.) TREE TWO
      (`<tmp>/tree_two/openspec/changes/a-real-change/.openspec.yaml` the
      loop instead, directory itself real, also confirmed genuine):
      `former_identity_claimants(<tree two>)` →
      `{'a-real-change': ['the live packet \`openspec/changes/a-real-change\`']}`;
      `declared_former_ids_in_tree(<tree two>, 'a-real-change')` → `[]`; both
      REPORT rather than traceback. `contained_change_dir_names(<tree two>)`
      → `{'a-real-change'}` — UNCHANGED from D0.3's own record, never having
      reached the loop. All five answers match PR #1107's own body table.
- [x] 4.4 `pytest-suite` green on the realization pull request at its merge head;
      that run is the green half of the archive evidence § 5 needs.
      **LEFT OPEN, 2026-09-18.** `pytest-suite` at this branch's pushed head
      `87eb684d` — run `35354873708`
      (https://github.com/opensoft/openxFactory/actions/runs/35354873708),
      14m9s / `825.82s` — is RED: `4 failed, 7924 passed, 6 skipped, 338
      deselected, 406 subtests passed`. ALL FOUR failures are in
      `tests/sequenced_after/` and name ONE finding: `archive-date-disposition
      STALE: 2026-09-16-add-composed-view-authoring: the directory AGREES
      with the UTC date of its adding commit (2026-09-16,
      d8ff2ec2c04992ffb15d50d5b018eb65b27937e0), so there is no disagreement
      to disposition; remove the entry` — none of the four touch
      `code_surface.py`, `target_release.py`, `proposal-support.py` or their
      three test packages. **INHERITED, NOT CAUSED HERE, MEASURED RATHER THAN
      ASSUMED**: the identical 4-failure signature and the identical finding
      reproduce on a clean `git worktree` at plain `origin/main` (`ebcdbc0c`,
      no realization content at all) —
      `python3 -m pytest tests/sequenced_after -q` → `4 failed, 282 passed in
      41.46s`, the same four test ids, the same commit
      `d8ff2ec2c04992ffb15d50d5b018eb65b27937e0` named. `main` is red on this
      today (lane openxfactory-4's `2026-09-16-add-composed-view-authoring`;
      repair PR #1109 in flight) and this branch's merge of `origin/main`
      inherits exactly that red and nothing else. Left `- [ ]` rather than
      ticked, per the realization plan's own rule that a check red for a
      reason outside this packet's six files is not this packet's evidence to
      claim.
      **GREEN AT THIS HEAD, 2026-09-18.** `pytest-suite` is GREEN at PR
      #1107 head `8fb0fc99`, run `35359208240`
      (https://github.com/opensoft/openxFactory/actions/runs/35359208240);
      confirmed `gh run view 35359208240 --json conclusion` returns
      `{"conclusion":"success"}`. The tick itself is the ARCHIVE act's,
      taken from `main`'s own green run at the landed merge, because a
      tick commit always moves the head past the run it cites (the
      `add-declared-former-id` precedent).
      **TICKED AT THE ARCHIVE ACT, 2026-09-18, ON `main`'s OWN RUN.**
      `pytest-suite` GREEN on `main` at `049d54a9` (run `35372664200`,
      2026-09-18T17:09Z), containing the realization merge `c22c4fc3` (#1107).
      **CONTAINMENT MEASURED AND NOT ASSUMED**:
      `gh api repos/opensoft/openxFactory/compare/c22c4fc3...049d54a9 --jq .status`
      -> `ahead`, and `git merge-base --is-ancestor c22c4fc3 049d54a9` exits 0.
      **THE HEAD THE PARAGRAPH ABOVE NAMES IS NOT THE HEAD #1107 MERGED FROM,
      AND THAT IS CORRECTED HERE RATHER THAN LEFT TO BE FOUND.** `8fb0fc99` was
      this branch's head when that paragraph was written; ONE further commit
      followed it — `bc9ebf95`, the paragraph's own commit — and `bc9ebf95` is
      the head PR #1107 merged from (`gh pr view 1107 --json headRefOid` ->
      `bc9ebf954f9629de25c6bb61cd5485937bdaaa54`). The box is satisfied at that
      head too, measured rather than inferred from the earlier run:
      `pytest-suite` run `35362604810` at `bc9ebf95`, conclusion `success`
      (2026-09-18T15:28Z); the whole check set at that head is **15 SUCCESS and
      1 SKIPPED** (`Sourcery review`), zero failures, across 14 distinct check
      names. So BOTH readings of "at its merge head" hold, and the green half
      § 5.1 needs is taken from `main`'s own run rather than from a branch run,
      which is the stricter of the two.

## 5. Archive (PERFORMED 2026-09-18 on merged-plus-green evidence; LANDS on a separate word)

- [x] 5.1 **(OPERATOR)** `code_surface` is NON-EMPTY, so under `release-realization`
      this packet SHALL NOT archive on landing. It archives on MERGED-PLUS-GREEN
      REALIZATION EVIDENCE at canon's grain: § 3's pull request merged into `main`,
      and a green `pytest-suite` run at the tree that merge carries.
      **THE EVIDENCE HALF IS IN HAND, 2026-09-18, AND EVERY LEG IS CITED RATHER
      THAN ASSERTED.** (i) THE PACKET landed as PR
      [#1083](https://github.com/opensoft/openxFactory/pull/1083) -> merge
      `ebcdbc0c20eb7368582d4bb8103001ab48316542` on `main`,
      **2026-09-18T14:03:33Z** (`gh pr view 1083 --json mergeCommit,mergedAt`),
      on Brett Heap's ratifying word of ~09:55Z, *"Ratify; land when green"*,
      and his later *"land #1083"* of ~14:20Z. (ii) **§ 3's REALIZATION** landed
      as PR [#1107](https://github.com/opensoft/openxFactory/pull/1107) -> merge
      `c22c4fc355898d4e57eb1159f47d756b30875b66` on `main`,
      **2026-09-18T17:06:27Z**, on Brett Heap's *"land #1107 when it is
      un-drafted"* of ~14:30Z, at head `bc9ebf95` with 15 SUCCESS / 1 SKIPPED
      and `pytest-suite` run `35362604810` green. (iii) **THE GREEN HALF AT
      CANON'S GRAIN**: `pytest-suite` SUCCESS on **`main`** at `049d54a9`, run
      [`35372664200`](https://github.com/opensoft/openxFactory/actions/runs/35372664200),
      2026-09-18T17:09:27Z — and `049d54a9` CONTAINS `c22c4fc3`, measured
      (`compare/c22c4fc3...049d54a9` -> `ahead`). The chain
      `ebcdbc0c` -> `c22c4fc3` -> `049d54a9` is an ancestry chain, each leg
      checked with `git merge-base --is-ancestor`.
      **THE OPERATOR HALF IS NOT CLAIMED BY THIS TICK AND IS NOT IN THIS LANE'S
      GIFT.** Brett Heap's SEPARATE ARCHIVE WORD has not been given. This tick
      records that the evidence condition this box states is MET; the archive
      pull request it rides on is opened as a **DRAFT** and lands only on that
      word, by MERGE COMMIT.
- [x] 5.2 **(OPERATOR)** Promote the `## ADDED` block onto
      `openspec/specs/release-realization/spec.md` and archive the packet to
      `openspec/changes/archive/<date>-harden-path-escape-helpers-against-symlink-loops/`
      through `python3 scripts/proposal-support.py . archive`, never a bare
      `openspec` invocation.
      **DONE THROUGH THE GOVERNED WRAPPER, NEVER A BARE `openspec archive`**, in
      the commit that moves this directory:
      `TZ=UTC python3 scripts/proposal-support.py . archive harden-path-escape-helpers-against-symlink-loops --yes`,
      exit **0**. Its decisive lines: `ORIGIN RETAINED
      harden-path-escape-helpers-against-symlink-loops (declaration unchanged
      since the ratifying commit ebcdbc0c20eb)`; `Totals: 1 passed, 0 failed
      (1 items)`; `Task status: Complete`; `Applying changes to
      openspec/specs/release-realization/spec.md: + 2 added`; `Totals: + 2, ~ 0,
      - 0, -> 0`; `Change 'harden-path-escape-helpers-against-symlink-loops'
      archived as '2026-09-18-harden-path-escape-helpers-against-symlink-loops'`;
      `OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its
      content address and every target validated --strict clean`; `NO SUPPORTING
      DOCS ... (origin retained, nothing to package)`. The CLI is the
      content-addressed pinned 1.12.0 artifact and NOT the 1.13.1 on `PATH`;
      `--path-mode` was not used.
      **THE ARCHIVE DIRECTORY IS
      `openspec/changes/archive/2026-09-18-harden-path-escape-helpers-against-symlink-loops/`**,
      named for the UTC day of the wrapper commit, which is what
      `archive-date-vs-commit` measures.
      **THE PROMOTED TEXT IS THE RATIFIED TEXT, BYTE FOR BYTE, MEASURED ON BOTH
      SIDES.** Two `## ADDED` requirements, TEN scenarios, onto
      `openspec/specs/release-realization/spec.md` (`--numstat` **+130 -0**,
      and `-w` reads the same `130 0`, so no line is whitespace-only):
      *A containment guard answers every resolution failure and raises none*
      (six scenarios; **6,049 bytes / 82 lines**, sha256
      `e12a9d9d54f64ac0c97d9c808f03df64583943f2d75760f0d3cb723ff33ffc7a` on BOTH
      the archived delta and canon) and *A symlink-loop proof is built at test
      time and never committed* (four scenarios; **3,198 bytes / 46 lines**,
      sha256 `f98402134c0b7eb855d30c57792f8219ea4f17a5e1ade176df0381194b19d625`
      on both). `release-realization` requirement count **17 -> 19**; NO
      promoted byte is edited or removed, this delta carrying no `## MODIFIED`
      block. The transcript is `review/verification-2026-09-18-post-merge.md`.
- [x] 5.3 **(OPERATOR)** Close openxFactory
      [#1074](https://github.com/opensoft/openxFactory/issues/1074) in the ARCHIVE
      pull request, by a closing keyword written there and in no commit message on
      this branch or the realization branch.
      **THE INSTRUMENT IS PLACED, AND THE TICK RECORDS THE PLACING AND NEVER
      THAT THE ISSUE IS SHUT.** `Closes #1074` is written as its own paragraph
      in the ARCHIVE pull request's body and in NO other place; #1074 shuts on
      the MERGE of that pull request, which is the landing lane's act on Brett
      Heap's archive word, and at no earlier act.
      **AND NO COMMIT MESSAGE CARRIES A CLOSING KEYWORD, GREPPED RATHER THAN
      ASSUMED.** Over this branch,
      `git log origin/main..HEAD --format='%H%n%B'` piped through a
      case-insensitive grep for
      `(clos(e|es|ed)|fix(es|ed)?|resolv(e|es|ed))[: ]*#[0-9]` returns **0
      matches**; the realization branch was grepped the same way at its merge
      head `bc9ebf95` and also returns **0** — PR #1107's own title and body say
      `refs #1074`, never `closes`. Every other issue and pull-request number in
      this branch's commit messages and in the archive pull request's body is a
      `Refs`-style naming and closes nothing.

## 6. Measured and NOT taken (OPEN; successors, not work owed)

- [~] 6.1 **The other ELEVEN `except OSError`-family clauses in these three
      modules** (`design.md` D4, the count taken by an AST scan and including
      `proposal-support.py:3724`, the support-archive read) guard reads, writes
      and subprocesses. They are read, enumerated and deliberately left, and
      widening them is refused rather than deferred: absorbing a `RuntimeError`
      out of a YAML load or a subprocess helper would swallow a defect in this
      repository's own code. `proposal-support.py:3939`'s entrypoint
      `except Exception:` is outside that count, being already wider than the
      obligation, and is retained rather than narrowed. **`[~]`, the house's reserved
      deferred-form marker, not `- [ ]`: this box documents a successor and
      refused-not-owed work, not incomplete work, so it must not gate this
      packet's eventual archive** (`scripts/proposal-support.py`'s
      `archive_change()` refuses any literal `- [ ]` in `tasks.md`).
- [~] 6.2 **The same shape elsewhere in the estate.** `scripts/` carries other
      modules that resolve caller-supplied or tree-supplied paths
      (`scripts/pin_containment.py` among them, which `document-lifecycle`'s own
      containment requirement governs). They were NOT measured by this packet and
      no claim is made about them; a sweep across the whole `scripts/` tree is a
      successor with its own measurement. **`[~]` as § 6.1: a
      documented successor, not incomplete work.**
- [~] 6.3 **A house helper.** The four guards do NOT end up with one identical
      tuple: three read `except (OSError, RuntimeError):` and `_contained` reads
      `except (OSError, ValueError, RuntimeError):`, its `ValueError` answering a
      DIFFERENT operation and staying (§ 3.5, and the first requirement's
      retention paragraph). What the four share after § 3 is the `RuntimeError`
      COVERAGE, held equal by convention and by a docstring claim. Whether the
      estate should carry ONE resolution helper the four call, rather than four
      clauses kept equal that way, is a successor: it changes four ratified
      surfaces at once and is out of scope for a correction. **`[~]` as § 6.1: a
      documented successor, not incomplete work.**
