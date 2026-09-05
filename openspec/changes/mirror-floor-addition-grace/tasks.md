# Tasks

Realization begins only after ratification. **NOTHING BELOW IS STARTED BY THE
AUTHORING OF THIS PACKET**, and the word that authorized the authoring
("companion") authorized none of it.

The order below is not a preference. Task 1 is a PREREQUISITE of tasks 2 and 3
by requirement 6: a mirror of a rule the pinned core does not implement is a
divergence, not a mirror.

## 1. The pin advance — FIRST, and in one act

- [ ] 1.1 Re-measure codexFactory `origin/main` and verify that `712fc8ca` (the
  merge commit of codexFactory PR #206, which realized `add-floor-addition-grace`)
  is an ancestor of it. The advance target is `origin/main`'s tip at realization
  time, not this sentence's value.
- [ ] 1.2 Advance all FIVE sites in ONE commit, and verify each by reading it
  back rather than by trusting the edit:
  `contracts/review-lane-pin.yaml` `core_commit`;
  `.github/workflows/merge-master-approval.yml` `PINNED_CORE_COMMIT`;
  that workflow's core checkout `ref:`;
  `.github/workflows/pytest-suite.yml`'s core checkout `ref:`;
  and `contracts/review-lane-floor-snapshot.yaml` re-copied byte for byte from
  the new `core_commit`, with `floor_snapshot.sha256` recomputed and
  `floor_snapshot.entry_count` updated.
- [ ] 1.3 Never hand-edit the snapshot. Re-copy it. It is a witness, and an
  edited witness proves nothing (the pin's own `refresh:` instruction).
- [ ] 1.4 Record the advance in `contracts/review-lane-pin.yaml`'s comment
  history in the voice the seven prior advances use: what moved, what it carries
  that the previous commit did not, and — new to this advance — that its object
  is the GRACE rather than a spec addition, so the floor's entry count does NOT
  move by one for a promotion.
- [ ] 1.5 `python3 -m pytest tests/review_lane_pin -q` green on the advance
  alone, before any test change.

## 2. The required lane

- [ ] 2.1 Add the mirrored completeness rule to
  `tests/review_lane_pin/test_floor_snapshot.py` beside `uncovered()`: given the
  surface, the floor entries, the created set and the pin window, return the
  uncovered paths and the covered-pending paths as two separate sorted results,
  with the reason carried per pending path.
- [ ] 2.2 Add the git measurements, fail-safe by default: the created set from
  `git diff --name-status --diff-filter=A <merge-base>..HEAD -- openspec/specs`
  against the resolved base branch; the pin window from
  `git log --diff-filter=A <generated_at>..<base> -- openspec/specs`, with
  `generated_at` read from the vendored snapshot's block header. Each returns
  "not measured" — never an empty set — when the base, the merge base or the pin
  will not resolve, or when the pin is not an ancestor of the base. `git` only:
  no network, nothing `tests/hermeticity.py` has anything to say about.
- [ ] 2.3 Move `test_every_tracked_openspec_spec_path_is_on_the_floor` onto the
  mirrored rule. Keep its anti-vacuity guard and its ordered two-repository
  repair message, and add the pending set to the message so a graced run says
  what is OWED.
- [ ] 2.4 Move the two negative controls that drive the same expression —
  `test_the_unmutated_surface_is_a_positive_first` and
  `test_a_fabricated_off_floor_spec_path_is_refused` — onto the graced
  expression, keeping each control's meaning. The fabricated path is created by
  no diff and lies in no window, so it stays REFUSED; assert that explicitly, in
  those words, so the grace cannot be misread as "additions are free".
- [ ] 2.5 Add the negative controls the grace itself needs: a created path is
  pending; a modification, a copy, a rename and a removal are NOT; an
  unmeasurable base grants nothing; an unmeasurable or non-ancestor pin grants
  nothing.
- [ ] 2.6 Add the VECTOR REPLAY against the pinned core's
  `tests/merge-master/fixtures/floor-addition-grace/vectors.json`, replaying
  BOTH `vectors` and `refused_vectors`, located through the existing
  `locate_pinned_core()` and skipping — never failing — when the core is absent.
  Assert the vector file is non-empty and that both lists were exercised, so a
  truncated fixture cannot pass vacuously.
- [ ] 2.7 Watch the replay BY NAME in `.github/workflows/pytest-suite.yml`,
  exactly as `FRESHNESS_CLASSNAME` / `FRESHNESS_TESTNAME` watch the snapshot
  comparison, and move `EXPECT_SKIPPED` 21 → 22 with the new skip's reason
  recorded beside the existing one. Add the live-node-id assertion for the new
  pair beside `test_the_required_suite_watches_the_verifier_by_name`, so a
  rename reds on a developer's machine naming the strings to move.
- [ ] 2.8 `python3 -m pytest tests/review_lane_pin -q` green, and green a second
  time with `PINNED_CORE_CHECKOUT` pointed at a real codexFactory checkout so
  the replay actually runs rather than skipping.

## 3. The advisory lane

- [ ] 3.1 In `.github/workflows/merge-master-approval.yml` step 8, import
  `evaluate_floor_completeness` from the pinned core and DELETE the hand-rolled
  `sorted(set(tracked) - set(floor.never_clearable_paths))`. Merge
  `completeness.report()` into the verdict; its keys already match what the step
  prints.
- [ ] 3.2 Measure the pin window in the step with
  `specs_floor_block.pin_window_for_document` (or `paths_added_after_pin`), and
  pass `added_since_pin=None` — NOT `()` — whenever it could not be measured.
  `None` and `()` are different facts and the core reads them differently.
- [ ] 3.3 Set the base checkout's `fetch-depth: 0` (decision C), with the
  measured cost stated in the step's comment, so the window is measurable at
  all. Verify by asserting the run resolved the pin rather than by assuming the
  checkout worked.
- [ ] 3.4 Extend the printed report and the rendered summary: a pending count
  and per-path reasons in the jq report, a table row in the verdict, and the
  escalation state when the core reports it. Keep every `// []` / `// "-"`
  default — the early refusal stages emit `stage` and `reason` alone and a
  missing key is a jq ERROR.
- [ ] 3.5 Extend the anti-vacuity step with a POSITIVE assertion that the
  pending computation produced a result, in the form its existing assertions
  take (`has("pending_floor_extension")`), so a computation that silently
  stopped is distinguishable from one that found nothing.
- [ ] 3.6 Keep `refusals[0]` semantics: assert, in a test or in the step, that a
  run carrying both a grace and a removal reports the REMOVAL's stage and still
  refuses.

## 4. The regeneration this change makes possible

- [ ] 4.1 After the mirror and the pin advance have LANDED, request ONE floor
  regeneration in codexFactory at a LANDED openxFactory commit — one reachable
  from `main` — being the first repair that does not block the pull request that
  caused it. The generator now refuses `--write` at an unlanded `--ref`, so this
  is enforced there and merely relied upon here.
- [ ] 4.2 Advance this repository's five pin sites onto the regenerated core
  commit, in the same one-act form as task 1.2.
- [ ] 4.3 Record that the live pin `3afd8a8c` — measured 2026-09-05 as NOT an
  ancestor of openxFactory `main`, one of three of the last five — is retired by
  4.1, and record the measurement rather than only the repair.

## 5. Observation and evidence (the archive gate)

- [ ] 5.1 `python3 -m pytest tests/review_lane_pin -q`, `tests/sequenced_after`,
  and the full `pytest-suite` green; `OPENSPEC_TELEMETRY=0 openspec validate
  --all --strict` clean; `python3 scripts/validate-sequenced-after.py .` and
  `--ledger-diff` clean.
- [ ] 5.2 The `pending_floor_extension` outcome OBSERVED ONCE on a real advisory
  run, with its path list, its per-path reasons and its owed-regeneration
  message, quoted verbatim in the archive record. An outcome nobody has seen is
  not evidence that it works.
- [ ] 5.3 A real promoting pull request observed NOT RED in the required lane for
  the path it creates — the falsification of the whole packet, and the thing the
  five hand repairs of 2026-09-03/04 were paying for.
- [ ] 5.4 Record the divergence check: the vector replay green on the same head,
  proving the two lanes agreed rather than merely both being green.

## 6. Owner's acts (not an agent's)

- [ ] 6.1 Ratify or refuse this packet. It is `Status: draft`; ratification is
  OWED and is Brett Heap's act. The 2026-09-05 word "companion" authorized the
  AUTHORING, not the content.
- [ ] 6.2 Rule on the authoring decisions A through F, and in particular on
  **A** (mirror-and-replay versus import, and its vendoring sub-decision), on
  **B** (a new capability, and its name) and on **C** (`fetch-depth: 0` versus a
  targeted fetch).
- [ ] 6.3 NOT OWED HERE, and named so it is not silently assumed: the D-3
  tolerance NUMBER is codexFactory's to set in its own CODEOWNERS-routed
  document, and option (b) from codexFactory issue #203 remains unruled and
  undesigned.
