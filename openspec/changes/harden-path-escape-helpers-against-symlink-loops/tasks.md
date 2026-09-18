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

- [ ] 3.1 `scripts/code_surface.py`: `_unescaped`'s clause widened to
      `except (OSError, RuntimeError):`, and its docstring amended to name
      `RuntimeError` beside `OSError` as a failure this guard closes, keeping its
      written claim that `target_release._unescaped` "is the exact shape this
      mirrors" TRUE.
- [ ] 3.2 `tests/code_surface/`: one test that builds an `a -> b -> a` loop under
      `tmp_path`, in ALL THREE exposed positions the first requirement names (the
      candidate's own leaf; a parent component above an ordinary leaf; and the
      SCANNED ROOT itself, `spec.md`'s third scenario), and asserts `_unescaped`
      returns `None` in each. In that third position the loop is reached through
      the CANDIDATE and never through a separate root read: `candidate =
      repo_root / relative` traverses the loop, so `code_surface.py:775` raises
      and the root resolution on `:776` is never executed. Measured, not assumed;
      the transcript is `design.md` D5. Recorded failing against `c6997f12`'s
      clause.
- [ ] 3.3 `scripts/target_release.py`: `_unescaped`'s clause and
      `_registry_present`'s clause both widened to `except (OSError, RuntimeError):`,
      and both docstrings amended, `_unescaped`'s keeping its claim to generalize
      `_registry_present`'s test TRUE.
- [ ] 3.4 `tests/target_release/`: TWO cases, which is why the realization is FOUR
      TEST CASES IN THREE PACKAGES and not one per module. One for `_unescaped` in
      all three positions, as 3.2; and one for `_registry_present` DECLARED AS A
      TEST OF THE CLAUSE (`design.md` D3, D0.5), since no tree state reaches it,
      with the declaration in the test's own docstring and not only in this
      packet, and driven by a seam that makes the pre-check pass while the
      resolution fails, so it still FAILS against the unfixed clause. The
      scanned-root position is no exception for that guard: measured, a root set
      to the loop returns `False` at the `is_dir()` pre-check exactly as the other
      two positions do, so it is D3's one clause test and not a fourth POSITION.
- [ ] 3.5 `scripts/proposal-support.py`: `_contained`'s clause widened to
      `except (OSError, ValueError, RuntimeError):`, the `ValueError` guarding the
      relative-path computation's own failure and STAYING; `contained_dir` and
      `contained_file` docstrings amended to name the set.
- [ ] 3.6 `tests/proposal-support/`: one test that builds the loop under `tmp_path`
      and asserts `contained_dir` and `contained_file` return `False`, in all
      three positions. `_contained` is the ONE guard of the four whose ROOT read
      is reachable on its own, because it resolves the candidate first and the
      root separately inside `relative_to`: with a real path as the candidate and
      the loop as the root, `proposal-support.py:343` succeeds and `:346` raises.
      That clean-candidate sub-case is asserted HERE and claimed nowhere else.
- [ ] 3.7 **NO SYMLINK IS ADDED TO THE TRACKED TREE.** Verified in the realization
      pull request by `git ls-files -s | awk '$1 == "120000"'` returning nothing,
      and recorded in its body.
- [ ] 3.8 **NO OTHER FILE MOVES.** No validator arm, no existing test, no
      workflow, no contract member, no schema, no report field, no promoted byte,
      and none of the ELEVEN non-containment `except OSError`-family clauses
      `design.md` D4 enumerates (`proposal-support.py:3724` among them), nor
      `proposal-support.py:3939`'s already-wider `except Exception:`.

## 4. Verification (OPEN; taken at the realization head)

- [ ] 4.1 `python3 -m pytest tests/code_surface tests/target_release tests/proposal-support -q`
      green, with the FOUR new test cases' failing runs against the unfixed
      clauses recorded beside them. FOUR, one per clause, in THREE packages: one
      in `tests/code_surface/` (§ 3.2), TWO in `tests/target_release/` (§ 3.4),
      one in `tests/proposal-support/` (§ 3.6). The count is the realization
      plan's and the same number is carried in `proposal.md`'s `code_surface:`
      front matter.
- [ ] 4.2 `python3 scripts/validate-code-surface.py .`,
      `python3 scripts/validate-target-release.py .` and
      `python3 scripts/proposal-support.py . verify` green over the live corpus,
      proving the widened clauses changed no judgment of the real tree.
- [ ] 4.3 The TWO end-to-end trees of `design.md` D0.3 re-run against the
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
- [ ] 4.4 `pytest-suite` green on the realization pull request at its merge head;
      that run is the green half of the archive evidence § 5 needs.

## 5. Archive (OPEN; a separate act on a separate word)

- [ ] 5.1 **(OPERATOR)** `code_surface` is NON-EMPTY, so under `release-realization`
      this packet SHALL NOT archive on landing. It archives on MERGED-PLUS-GREEN
      REALIZATION EVIDENCE at canon's grain: § 3's pull request merged into `main`,
      and a green `pytest-suite` run at the tree that merge carries.
- [ ] 5.2 **(OPERATOR)** Promote the `## ADDED` block onto
      `openspec/specs/release-realization/spec.md` and archive the packet to
      `openspec/changes/archive/<date>-harden-path-escape-helpers-against-symlink-loops/`
      through `python3 scripts/proposal-support.py . archive`, never a bare
      `openspec` invocation.
- [ ] 5.3 **(OPERATOR)** Close openxFactory
      [#1074](https://github.com/opensoft/openxFactory/issues/1074) in the ARCHIVE
      pull request, by a closing keyword written there and in no commit message on
      this branch or the realization branch.

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
