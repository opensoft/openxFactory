# Tasks

Realization begins only after ratification. **NOTHING BELOW IS STARTED BY THE
AUTHORING OF THIS PACKET**, and the word that authorized the authoring
("companion") authorized none of it.

The order below is not a preference. Task 1 is a PREREQUISITE of tasks 2 and 3
by requirement 6: a mirror of a rule the pinned core does not implement is a
divergence, not a mirror.

## 1. The pin advance — FIRST, and in one act

- [x] 1.1 Re-measure codexFactory `origin/main` and verify that `712fc8ca` (the
  merge commit of codexFactory PR #206, which realized `add-floor-addition-grace`)
  is an ancestor of it. The advance target is `origin/main`'s tip at realization
  time, not this sentence's value.
  **Evidence**: re-measured 2026-09-05; `origin/main` had moved to `e57643a7`
  (PR #208 merge); `git merge-base --is-ancestor 712fc8ca e57643a7` holds.
  Advanced to `e57643a7`, not `712fc8ca`, per this task's own instruction.
- [x] 1.2 Advance all FIVE sites in ONE commit, and verify each by reading it
  back rather than by trusting the edit:
  `contracts/review-lane-pin.yaml` `core_commit`;
  `.github/workflows/merge-master-approval.yml` `PINNED_CORE_COMMIT`;
  that workflow's core checkout `ref:`;
  `.github/workflows/pytest-suite.yml`'s core checkout `ref:`;
  and `contracts/review-lane-floor-snapshot.yaml` re-copied byte for byte from
  the new `core_commit`, with `floor_snapshot.sha256` recomputed and
  `floor_snapshot.entry_count` updated.
  **Evidence**: commit `e3ed78b1`; all five sites re-read post-commit and
  equal `e57643a7`; snapshot `sha256` `0eba8e58…7ba4be`, `entry_count` 67
  (unchanged — the first advance whose floor grew by zero paths).
- [x] 1.3 Never hand-edit the snapshot. Re-copy it. It is a witness, and an
  edited witness proves nothing (the pin's own `refresh:` instruction).
  **Evidence**: `cmp`-identical to `git show e57643a7:scripts/merge_master/
  openxfactory-review-authority-floor.yaml` before commit.
- [x] 1.4 Record the advance in `contracts/review-lane-pin.yaml`'s comment
  history in the voice the seven prior advances use: what moved, what it carries
  that the previous commit did not, and — new to this advance — that its object
  is the GRACE rather than a spec addition, so the floor's entry count does NOT
  move by one for a promotion.
  **Evidence**: commit `e3ed78b1`'s new "THE EIGHTH ADVANCE" paragraph in the
  pin, and the matching paragraph in `merge-master-approval.yml`'s own header.
- [x] 1.5 `python3 -m pytest tests/review_lane_pin -q` green on the advance
  alone, before any test change.
  **Evidence**: 55 passed, 1 skipped (no core on disk); 56 passed (0 skipped)
  with `PINNED_CORE_CHECKOUT` at a codexFactory checkout of `e57643a7`.

## 2. The required lane

- [x] 2.1 Add the mirrored completeness rule to
  `tests/review_lane_pin/test_floor_snapshot.py` beside `uncovered()`: given the
  surface, the floor entries, the created set and the pin window, return the
  uncovered paths and the covered-pending paths as two separate sorted results,
  with the reason carried per pending path.
  **Evidence**: `graced_uncovered()`, commit `f6185a11`.
- [x] 2.2 Add the git measurements, fail-safe by default: the created set from
  `git diff --name-status --diff-filter=A <merge-base>..HEAD -- openspec/specs`
  against the resolved base branch; the pin window from the pinned core's OWN
  invocation, byte for byte rather than paraphrased —
  `git log --diff-filter=A --name-only --pretty=format: <generated_at>..<base> -- openspec/specs`
  (`paths_added_after_pin`'s exact argument list; `--name-only
  --pretty=format:` are load-bearing, since without them `git log` emits commit
  headers rather than a path list) — with
  `generated_at` read from the vendored snapshot's block header. Each returns
  "not measured" — never an empty set — when the base, the merge base or the pin
  will not resolve, or when the pin is not an ancestor of the base. `git` only:
  no network, nothing `tests/hermeticity.py` has anything to say about.
  **Evidence**: `created_since_merge_base()` / `pin_window()`, commit
  `f6185a11`; `TheGraceItself` exercises both against disposable git
  repositories (real additions/modifications/removals/renames, unresolvable
  and non-ancestor pins).
- [x] 2.3 Move `test_every_tracked_openspec_spec_path_is_on_the_floor` onto the
  mirrored rule. Keep its anti-vacuity guard and its ordered two-repository
  repair message, and add the pending set to the message so a graced run says
  what is OWED.
  **Evidence**: commit `f6185a11`; the pending set is printed (informational)
  on any run with covered-pending paths and folded into the failure message
  when uncovered paths also exist.
- [x] 2.4 Move the two negative controls that drive the same expression —
  `test_the_unmutated_surface_is_a_positive_first` and
  `test_a_fabricated_off_floor_spec_path_is_refused` — onto the graced
  expression, keeping each control's meaning. The fabricated path is created by
  no diff and lies in no window, so it stays REFUSED; assert that explicitly, in
  those words, so the grace cannot be misread as "additions are free".
  **Evidence**: commit `f6185a11`.
- [x] 2.5 Add the negative controls the grace itself needs: a created path is
  pending; a modification, a copy, a rename and a removal are NOT; an
  unmeasurable base grants nothing; an unmeasurable or non-ancestor pin grants
  nothing.
  **Evidence**: `TheGraceItself`, commit `f6185a11` — 18 tests, including real
  disposable-repository tests for the modification/removal/rename exclusions
  and for the unresolvable/non-ancestor pin cases.
- [x] 2.6 Add the VECTOR REPLAY against the pinned core's
  `tests/merge-master/fixtures/floor-addition-grace/vectors.json`, replaying
  BOTH `vectors` and `refused_vectors`, located through the existing
  `locate_pinned_core()` and skipping — never failing — when the core is absent.
  Assert the vector file is non-empty and that both lists were exercised, so a
  truncated fixture cannot pass vacuously.
  **Evidence**: `TheVectorReplay.test_every_vector_replays`, commit `f6185a11`
  — all 16 accepted + 5 refused vectors green with the core on disk (21
  subtests), skips with it absent.
- [x] 2.7 Watch the replay BY NAME in `.github/workflows/pytest-suite.yml`,
  exactly as `FRESHNESS_CLASSNAME` / `FRESHNESS_TESTNAME` watch the snapshot
  comparison, and move `EXPECT_SKIPPED` 21 → 22 with the new skip's reason
  recorded beside the existing one. Add the live-node-id assertion for the new
  pair beside `test_the_required_suite_watches_the_verifier_by_name`, so a
  rename reds on a developer's machine naming the strings to move.
  **Evidence, WITH A CORRECTION TO THIS TASK'S OWN TEXT**:
  `VECTOR_REPLAY_CLASSNAME`/`VECTOR_REPLAY_TESTNAME` and
  `test_the_required_suite_watches_the_vector_replay_by_name` land as
  written, commit `f6185a11`. `EXPECT_SKIPPED` does NOT move to 22 — it
  STAYS 21, verified on CI (PR #686, run 33978773175:
  `skipped=21`, both named verdicts `passed`). This task's own prose assumed
  the replay always contributes a skip; it does not, by the same design as
  the freshness verifier beside it (both skip ONLY on a core-checkout
  failure, and skip TOGETHER when that happens, sharing
  `locate_pinned_core()` — so the aggregate moves by two on that path, not
  by one on every path). Fixed in a follow-up commit on this same PR after
  CI caught the mismatch red; see that commit's message for the corrected
  reasoning.
- [x] 2.8 `python3 -m pytest tests/review_lane_pin -q` green, and green a second
  time with `PINNED_CORE_CHECKOUT` pointed at a real codexFactory checkout so
  the replay actually runs rather than skipping.
  **Evidence**: 73 passed / 2 skipped / 22 subtests (no core); 75 passed / 43
  subtests (core at `e57643a7`).

## 3. The advisory lane

- [x] 3.1 In `.github/workflows/merge-master-approval.yml` step 8, import
  `evaluate_floor_completeness` from the pinned core and DELETE the hand-rolled
  `sorted(set(tracked) - set(floor.never_clearable_paths))`. Merge
  `completeness.report()` into the verdict; its keys already match what the step
  prints.
  **Evidence**: commit `01e1fd88`. The old, separately-called
  `candidate_floor_drift` is ALSO deleted — its partition is now read off the
  same `evaluate_floor_completeness` call, not a second caller of the same
  underlying `_drift_between`.
- [x] 3.2 Measure the pin window in the step with
  `specs_floor_block.pin_window_for_document` (or `paths_added_after_pin`), and
  pass `added_since_pin=None` — NOT `()` — whenever it could not be measured.
  `None` and `()` are different facts and the core reads them differently.
  **Evidence**: commit `01e1fd88`; verified locally with the pinned core on
  disk that the live pin (`3afd8a8c`, not an ancestor of this branch's
  `origin/main`) correctly reports `pin_measured: false`.
- [x] 3.3 Set the base checkout's `fetch-depth: 0` (decision C), with the
  measured cost stated in the step's comment, so the window is measurable at
  all. Verify by asserting the run resolved the pin rather than by assuming the
  checkout worked.
  **Evidence**: commit `01e1fd88`; `test_the_base_checkout_carries_the_history
  _the_pin_window_needs` asserts `fetch-depth: 0` on the named step.
- [x] 3.4 Extend the printed report and the rendered summary: a pending count
  and per-path reasons in the jq report, a table row in the verdict, and the
  escalation state when the core reports it. Keep every `// []` / `// "-"`
  default — the early refusal stages emit `stage` and `reason` alone and a
  missing key is a jq ERROR.
  **Evidence**: commit `01e1fd88`; jq expressions hand-verified against a
  clean run, a graced run and an early-refusal-shaped document (missing key)
  with no jq error in any case.
- [x] 3.5 Extend the anti-vacuity step with a POSITIVE assertion that the
  pending computation produced a result, in the form its existing assertions
  take (`has("pending_floor_extension")`), so a computation that silently
  stopped is distinguishable from one that found nothing.
  **Evidence**: commit `01e1fd88`; also asserts the four-field shape
  (`count`/`paths`/`reasons`/`pin_measured`) rather than bare key presence.
- [x] 3.6 Keep `refusals[0]` semantics: assert, in a test or in the step, that a
  run carrying both a grace and a removal reports the REMOVAL's stage and still
  refuses.
  **Evidence**: hand-verified locally (a candidate that both adds an off-floor
  path and removes a floored one): `stage: floor_drift_caused_by_candidate`,
  `ok: false`, and `pending_floor_extension.count: 1` with the added path
  named and reasoned — the grace is reported but does not hide the refusal.
  Guaranteed by construction (the core's own `FloorCompleteness.refusals()`
  order, not re-derived here) and by the core's own vector "one addition and
  one deletion in the same candidate", replayed green in task 2.6.

## 4. The regeneration this change makes possible

- [x] 4.1 After the mirror and the pin advance have LANDED, request ONE floor
  regeneration in codexFactory at a LANDED openxFactory commit — one reachable
  from `main` — being the first repair that does not block the pull request that
  caused it. The generator now refuses `--write` at an unlanded `--ref`, so this
  is enforced there and merely relied upon here.
  **Evidence**: codexFactory PR #212 (MERGE COMMIT `67a6ffc9`, merged
  2026-09-05T18:08:23Z) regenerated
  `scripts/merge_master/openxfactory-review-authority-floor.yaml` at
  openxFactory `f6724f04` — the merge commit of PR #686, this repository's own
  `mirror-floor-addition-grace` realization, and reachable from openxFactory
  `main` (`git merge-base --is-ancestor f6724f04 origin/main` holds on THIS
  repository's tree). The negative control's refusal was OBSERVED, not merely
  relied upon: the generator's `--write` guard is codexFactory's own, ratified
  and realized ground, and PR #212 is what a request AT a landed commit
  produces when it is honored — sha256 `18389a3d…3521a8`, 15402 bytes, blob
  `fdcd9f7e…5b5a8` at `67a6ffc9`, byte-diffed against `e57643a7`'s copy of the
  same file: the ONLY change is the block header's `generated_at` / `--ref`
  lines (`3afd8a8c` -> `f6724f04`); `entry_count` stays 59 and the floor total
  stays 67 — no `openspec/specs` path exists at `f6724f04` that did not already
  exist at `3afd8a8c`.
- [x] 4.2 Advance this repository's five pin sites onto the regenerated core
  commit, in the same one-act form as task 1.2.
  **Evidence**: `contracts/review-lane-pin.yaml` `core_commit`,
  `.github/workflows/merge-master-approval.yml` `PINNED_CORE_COMMIT` and its
  core checkout `ref:`, `.github/workflows/pytest-suite.yml`'s core checkout
  `ref:`, and `contracts/review-lane-floor-snapshot.yaml` (re-copied byte for
  byte, `sha256` and `entry_count` updated) all advanced `e57643a7` ->
  `67a6ffc9` in one commit on branch `chore/repin-after-landed-regeneration`,
  each re-read post-edit and confirmed equal.
- [x] 4.3 Record that the live pin `3afd8a8c` — measured 2026-09-05 as NOT an
  ancestor of openxFactory `main`, one of three of the last five — is retired by
  4.1, and record the measurement rather than only the repair.
  **Evidence**: `contracts/review-lane-pin.yaml`'s "THE NINTH ADVANCE" note and
  `merge-master-approval.yml`'s matching header record that `3afd8a8c` was NOT
  an ancestor of openxFactory `main` and that `f6724f04` IS (measured by
  `git merge-base --is-ancestor f6724f04 origin/main` on this repository's own
  tree before this commit) — the first advance at which the addition-grace's
  B1 pin window (`specs_floor_block.pin_window_for_document`) is MEASURABLE
  rather than fail-safed to `None` on this repository's `main`, because the
  function requires the declared `generated_at` to resolve as an ancestor of
  the base branch it measures.

## 5. Observation and evidence (the archive gate)

- [x] 5.1 `python3 -m pytest tests/review_lane_pin -q`, `tests/sequenced_after`,
  and the full `pytest-suite` green; `OPENSPEC_TELEMETRY=0 openspec validate
  --all --strict` clean; `python3 scripts/validate-sequenced-after.py .` and
  `--ledger-diff` clean.
  **Evidence**: `pytest-suite` GREEN on CI at head `8e3910d9`, run 33979893935
  (22m21s): `selected=9725 passed=9704 skipped=21 failures=0 errors=0`, both
  named verdicts (`TheFreshnessVerifier`, `TheVectorReplay`) `passed`. Local:
  `tests/review_lane_pin -q` 73 passed/2 skipped/22 subtests (75 passed/43
  subtests with the pinned core); `tests/sequenced_after -q` 162 passed;
  `openspec validate --all --strict` 92 passed/0 failed; `proposal-support.py
  . verify` ok; `validate-sequenced-after.py .` passed (33 active, 2
  declaring); `--ledger-diff` consistent (170 rows, no row moves). A full
  local `python3 -m pytest tests/ -q -m "not postgres"` (~9,725 selected) was
  ALSO run twice: first WITHOUT the `openXwallet` submodule initialized,
  which surfaced ~95 failures and ~50 errors in `tests/trust-anchor/`,
  `tests/openxwallet_pin/`, `tests/clearing/` and one documented flat-checkout
  case (`test_find_validator_locates_pinned_checkout`) — ALL of which
  resolved to green after `git submodule update --init openXwallet` (confirmed
  by re-running each affected subtree: 311 passed, 203 passed), matching
  CI's own "Init the openXwallet gitlink only" step this local clone had
  skipped. Pre-existing local setup gap, not a regression from this packet.
- [ ] 5.2 The `pending_floor_extension` outcome OBSERVED ONCE on a real advisory
  run, with its path list, its per-path reasons and its owed-regeneration
  message, quoted verbatim in the archive record. An outcome nobody has seen is
  not evidence that it works.
- [ ] 5.3 A real promoting pull request observed NOT RED in the required lane for
  the path it creates — the falsification of the whole packet, and the thing the
  five hand repairs of 2026-09-03/04 were paying for.
- [x] 5.4 Record the divergence check: the vector replay green on the same head,
  proving the two lanes agreed rather than merely both being green.
  **Evidence**: `TheVectorReplay.test_every_vector_replays` green with
  `PINNED_CORE_CHECKOUT` at codexFactory `e57643a7` — all 16 accepted + 5
  refused vectors replay to the SAME verdict `evaluate_floor_completeness`
  (imported directly by the advisory lane, Commit C) would give, on this
  same head.

## 6. Owner's acts (not an agent's)

- [x] 6.1 Ratify or refuse this packet. It is `Status: draft`; ratification is
  OWED and is Brett Heap's act. The 2026-09-05 word "companion" authorized the
  AUTHORING, not the content.
  **Evidence**: Brett Heap ratified, verbatim **"ratify the companion when
  green, then realize it"**, applied at the first head where the condition
  held, `ce9a81ed` (2026-09-05T14:24:10Z) — recorded in
  `openspec/changes/mirror-floor-addition-grace/review/ratification-2026-09-05.md`.
- [x] 6.2 Rule on the authoring decisions A through F, and in particular on
  **A** (mirror-and-replay versus import, and its vendoring sub-decision), on
  **B** (a new capability, and its name) and on **C** (`fetch-depth: 0` versus a
  targeted fetch).
  **Evidence**: same ratification record — because the ruling word preceded
  the authoring's completion, decisions A–F STAND AS RECOMMENDED and none was
  separately ruled; the record's decision table carries each of A–F with its
  alternative and disposition.
- [ ] 6.3 NOT OWED HERE, and named so it is not silently assumed: the D-3
  tolerance NUMBER is codexFactory's to set in its own CODEOWNERS-routed
  document, and option (b) from codexFactory issue #203 remains unruled and
  undesigned.

## Archive — the recorded escape, the three open boxes, and the LIVE TEST this act is

**ARCHIVED 2026-09-05 VIA THE RECORDED ESCAPE, SECOND OF AN ORDERED
CROSS-REPOSITORY PAIR — AND THIS ARCHIVE IS ITSELF THE PACKET'S FALSIFICATION
TEST.** Brett Heap ordered it in session on 2026-09-05, verbatim *"archive the
grace packets"* — one word covering BOTH archives, because the pair is one act
in two repositories.

**THE ORDER IS NOT A PREFERENCE EITHER**, and it is this packet's own
declaration that fixes it: `proposal.md` carries
`sequenced_after: [codexFactory:add-floor-addition-grace]`, so the parent
archives FIRST. It did: **codexFactory PR #218, merge commit
`35c089948a55bd8cf34293394e3b2621b6b0c8c5`, merged 2026-09-05T19:47:09Z**,
promoting seven requirements into `openspec/specs/repository-gate-floor/spec.md`
(5 → 12 requirements, 13 → 38 scenarios) and closing codexFactory issue #203 as
`completed`. This companion archives SECOND, into a capability of its own.

**WHY THIS PARTICULAR ARCHIVE IS THE PROGRAMME'S TEST, AND NOT BOOKKEEPING.**
This act CREATES `openspec/specs/review-lane-floor-mirror/spec.md` — a new
tracked path under a floor that is an EXACT ENUMERATION. Under the regime this
packet replaced, that path would be reported UNCOVERED in two lanes at once and
the REQUIRED `pytest-suite` would refuse the pull request until a two-repository
hand repair had run — the cost `proposal.md` measured at five payments in two
days. Under the grace now in force in both lanes, this pull request's own diff
creates the path, so the required lane should stay GREEN with the path reported
**covered-pending** (reason `created_by_candidate`) and the advisory lane should
print `pending_floor_extension` naming it. **Tasks 5.2 and 5.3 are therefore
NOT closable by any act before this one**: they are observations of THIS pull
request's own checks, and they are ticked in a later commit ON THIS PULL
REQUEST, with the run ids and the verbatim lines in their evidence, or they are
not ticked at all.

The evidence chain is read off `main` — every sha re-read from the GitHub API
for this act rather than remembered:

* **RATIFIED** 2026-09-05 by Brett Heap, repository owner, in session, verbatim
  *"ratify the companion when green, then realize it"* — a standing word applied
  at the first head where the condition held, `ce9a81ed`. The packet landed as
  **PR #676**, merge commit **`568fa370`** (2026-09-05T15:14:31Z). Record
  [`review/ratification-2026-09-05.md`](review/ratification-2026-09-05.md),
  archived with the packet. Authoring decisions **A–F STAND AS RECOMMENDED**
  under that word and none was separately ruled (task 6.2).
* **REALIZED** by **PR #686**, merge commit **`f6724f04`**
  (2026-09-05T17:30:54Z) — the pin advance in one act across five sites, the
  required lane's mirrored rule with its negative controls and the pinned core's
  own vector replay watched by name, and the advisory lane's step 8 IMPORTING
  `evaluate_floor_completeness` with `fetch-depth: 0` on its base checkout.
* **REGENERATED AT A LANDED COMMIT** by **codexFactory PR #212**, merge commit
  **`67a6ffc9`** (2026-09-05T18:08:23Z) — `generated_at` `3afd8a8c` →
  `f6724f04`, 59 entries unchanged, the first floor repair in this programme
  that did NOT block the pull request that caused it (task 4.1).
* **RE-PINNED** onto that regeneration by **PR #689**, merge commit
  **`b6804991`** (2026-09-05T18:39:13Z), the five sites moving in lockstep
  (task 4.2). **That is what makes the live test measurable**: the declared
  `generated_at` `f6724f04` IS an ancestor of this repository's `main`
  (`git merge-base --is-ancestor f6724f04 origin/main`, checked on this tree
  before this act), where the retired `3afd8a8c` was not — so B1's pin window
  resolves rather than fail-safing to `None` (task 4.3).
* **NO CONTRACT BUNDLE AND NO RELEASE TAG.** `proposal.md`'s `target_release:`
  says so in its own words: this packet adds no registered contract row, moves
  no digest set, spends no `contract_bundle_version` and owes no tag. Nothing
  was cut for it and nothing is owed.

**THE ESCAPE IS DISCLOSED RATHER THAN ROUTED AROUND.**
`python3 scripts/proposal-support.py . archive mirror-floor-addition-grace` was
run FIRST and REFUSED — exit 1, `change has incomplete tasks`, working tree
untouched. Its gate is

    tasks = directory / "tasks.md"
    if tasks.is_file() and re.search(r"^- \[ \]", tasks.read_text(), re.M):
        raise SupportError("change has incomplete tasks")
    (scripts/proposal-support.py:1079-1081)

— read off those three lines in this tree rather than remembered, and
**UNCONDITIONAL on WHICH box**: it matches the leading marker and can tell
nothing else about the task it refuses on.
`OPENSPEC_TELEMETRY=0 openspec archive mirror-floor-addition-grace --yes` was
run instead, verbatim:

    Proposal warnings in proposal.md (non-blocking):
      ⚠ Why section should not exceed 1000 characters
    Task status: 26/29 tasks
    Warning: 3 incomplete task(s) found. Continuing due to --yes flag.

    Specs to update:
      review-lane-floor-mirror: create
    Applying changes to openspec/specs/review-lane-floor-mirror/spec.md:
      + 7 added
    Totals: + 7, ~ 0, - 0, → 0
    Specs updated successfully.
    Change 'mirror-floor-addition-grace' archived as '2026-09-05-mirror-floor-addition-grace'.

**PRECEDENT, cited rather than invented**: `govern-sibling-added-modified-deltas`
(PR #571, squash `3bcde7e2`), `declare-spent-bundle-state` (PR #611, squash
`7af2725c`), `add-subject-establishment` (PR #647, squash `e4ff4fb3`),
`add-chain-anchoring` (PR #669, squash `66d11a24`) and
`amend-chain-anchoring-readiness-and-durability` (PR #670, squash `3d7b8f3b`) —
and, one repository over and one hour earlier, this packet's own parent
(codexFactory PR #218, `35c08994`), which recorded the same escape for the same
class of box.

**NOT ONE OF THE THREE OPEN BOXES IS UNDONE REALIZATION OF THIS CHANGE**, and
ticking any of them to satisfy the wrapper would be writing a false completion
past a gate that cannot tell "open by omission" from "open by design" apart.
They fall in two classes:

**(a) OBSERVATIONS THIS ACT PERFORMS — 5.2 and 5.3.** 5.2 asks for the
`pending_floor_extension` outcome *"OBSERVED ONCE on a real advisory run, with
its path list, its per-path reasons and its owed-regeneration message, quoted
verbatim in the archive record"*; 5.3 asks for *"a real promoting pull request
observed NOT RED in the required lane for the path it creates"*. **No earlier
act could close them, and the parent's own archive record says so**: codexFactory
PR #218 recorded its task 5.4 as PARTIAL, because openxFactory run
`33983590725` printed `covered-pending: 0 (tolerance 3, pin NOT measured
(fail-safe))` — the report SHAPE and the B1 fail-safe were seen, but no path was
ever covered-pending and the path list and the owed-regeneration message had
never been rendered live. **THIS PULL REQUEST IS THE FIRST CANDIDATE THAT
CREATES SUCH A PATH.** The observation is recorded below and the boxes are
ticked in the same commit that records it, or neither happens.

**(b) NOT OWED HERE — 6.3.** The box says so in its own first words: the D-3
escalation-tolerance NUMBER is codexFactory's to set in its own CODEOWNERS-routed
document, and option (b) from codexFactory issue #203 remains unruled and
undesigned. codexFactory PR #218's record states the same fact from the other
side — the tolerance stands PROPOSED at `pending_floor_extension_tolerance: 3`,
offered for veto, no veto exercised, and UNRULED. **An openxFactory archive
cannot close a codexFactory owner's box**, and no attempt is made here.

**THE PROMOTION WAS BYTE-CHECKED, NOT TRUSTED.** The capability is NEW, so the
check runs one way only — the archived delta's requirement text against the
created specification's, extracted from the first `### Requirement:` line on
both sides:

* `openspec/changes/archive/2026-09-05-mirror-floor-addition-grace/specs/review-lane-floor-mirror/spec.md`
  → **16 744 bytes**;
  `openspec/specs/review-lane-floor-mirror/spec.md` → **16 745 bytes**;
  `diff` reports exactly one difference, `182a183`, a single appended blank
  line at end-of-file — the same one-byte archiver signature #669 and #670 each
  recorded for their own promotions. **Not one other character moved.**
* **SEVEN requirements / 28 SCENARIOS on both sides**, counted by
  `^### Requirement:` and `^#### Scenario:` rather than by addition, and equal
  to the counts `proposal.md` and the ratification record each declared
  separately.
* `git status --porcelain -uall openspec/specs/` names **that one file and
  nothing else**, so no promoted requirement in any other capability moved a
  word.

**THE `## Purpose` WAS WRITTEN BY THIS ACT, AND THAT IS THE ONE THING IN THE
PROMOTED FILE THE ARCHIVER DID NOT AUTHOR.** `openspec archive` creates a new
capability's spec with the placeholder *"TBD - created by archiving change
mirror-floor-addition-grace. Update Purpose after archive."* and an instruction
addressed to nobody. Leaving it would have made this the ONLY promoted
specification in the corpus carrying that sentence — commit `552a3a76` had
repaired all 39 of the others on 2026-09-05 — so it was replaced here, in the
promoted specification directly, which is the only surface where such an edit
lands. It is prose ABOUT the capability, carries no SHALL, and is outside the
byte-checked requirement region above.
