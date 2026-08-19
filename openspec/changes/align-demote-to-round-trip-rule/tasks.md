# Tasks: align-demote-to-round-trip-rule

Ordered so the pure module and its tests exist before the executor calls it — the
markdown surgery is the risky half and it is the half that needs no tree.

## 1. The pure refresh module

- [ ] 1.1 New `scripts/ideation_dashboard/round_trip.py`, pure (text in, text
      out; no paths, no I/O). Fence-aware throughout: the canonical template ships
      as a fenced skeleton and a fragment that merely QUOTES it must not be read
      as carrying those sections. Carry the rule from the two implementations that
      already exist rather than re-deriving it.
- [ ] 1.2 `fill_provenance_slots(text, values)` — rewrite the
      `## Last proposal attempt (round-trip provenance)` section's `Field: value`
      lines in place; INSERT the section in the template's canonical position when
      it is absent. Preserve the document's own line endings (the `_flip_status`
      lesson: a bounded write must not retranslate the document it touches).
- [ ] 1.3 `refresh_marked_sections(text, proposal_text)` — for each `## ` section
      wrapped in `<!-- xspec:candidate ... -->`, replace the text INSIDE the fence
      with the same-named section's body from the proposal. Never rewrite the
      marker comments themselves; they are the addressing key. Never add a section
      the fragment does not mark, never delete one the proposal omits.
- [ ] 1.4 Idempotence by construction, then asserted: both operations are addressed
      rather than appending, so applying twice yields identical bytes.

## 2. The plan half

- [ ] 2.1 `classify_change_file` / `FileMove` identify the OUTLINE destination
      path-only, in the pure plan, so `demote-<stamp>.plan.yaml` states which file
      will be treated as the topic's outline before anything is written.
- [ ] 2.2 That move keeps `Status: staged` — the flip to `draft` stays correct and
      unchanged for the proposal documents bound for the topic's `openspec/`
      workspace. Two destinations, two statuses, one rule each.
- [ ] 2.3 Record the covered bound in the code: only the exact `<topic>.md` arm of
      the two-arm selection rule is decidable from paths. The shallowest-markdown
      arm is out of scope (design Decision 1) and the comment says so, so the next
      reader does not mistake the narrowing for an oversight.

## 3. The executor half

- [ ] 3.1 Read the change's `supporting-docs/manifest.yaml` BEFORE the moves run —
      it is itself a returning supporting-doc and the change folder is removed at
      the end. `Raised` comes from its `transitioned_at`; an absent manifest means
      the slot records the value as unavailable, never a guess from an
      archive-date prefix or an mtime.
- [ ] 3.2 The three destination cases (design Decision 4): absent → restore then
      refresh; byte-identical → same; DIFFERS → refresh in place, snapshot NOT
      written to the destination, snapshot preserved as
      `<topic>.snapshot-<change-id>.md`.
- [ ] 3.3 The transition manifest and the README note both say whether the
      snapshot was APPLIED or PRESERVED, and name the preserved file. "Never
      byte-replace" must not become "silently discard the other copy", and a human
      who wants the snapshot's text has to be able to find it.
- [ ] 3.4 Fill the slots from the values the executor holds (design Decision 3).
      `Status at demote` is `active` by the current precondition — filled anyway,
      with the reason recorded, because a slot reading `n/a` after a real demote is
      worse than one reading a true constant.

## 4. Tests

- [ ] 4.1 The pure module, no tree: slot fill into a conforming fragment, into a
      pre-template fragment (section inserted), CRLF preserved, quoted-skeleton
      fence case, idempotence.
- [ ] 4.2 Marked-section refresh: real proposal text lands inside the fences; a
      section only the proposal has is not added; a section only the fragment has
      is not deleted; the marker comments are byte-identical afterwards.
- [ ] 4.3 Driven through the REAL console and executor, the way the defect was
      found — `plan_demotion` + `execute_demotion_plan` against a fixture tree.
      The fragment afterwards carries the proposal's real text, the filled slots,
      and `Status: staged`. Use DISTINCTIVE non-aspirational content so a snapshot
      echo cannot pass.
- [ ] 4.4 The guard, which is the test this change exists for: a destination that
      exists and differs is NOT byte-replaced; its untouched bytes survive exactly;
      the snapshot is preserved and named. This must fail against today's code.
- [ ] 4.5 The three-way fence-rule agreement: `round_trip.py`,
      `doc_health/families.py` and `web/views/outline-model.js` on a shared fixture
      set (design Decision 2's mitigation for a third implementation of one rule).
- [ ] 4.6 Regression: the existing eight demote tests in
      `tests/ideation-dashboard/test_gate_console.py` stay green, including the
      byte-exact CRLF cases — this change must not become a second
      corpus-integrity defect in the same verb.

## 5. Gates

- [ ] 5.1 `OPENSPEC_TELEMETRY=0 openspec validate align-demote-to-round-trip-rule
      --strict`, then `--all --strict`, from the `openxFactory/` root.
- [ ] 5.2 `python3 -m pytest tests/ideation-dashboard -q` and
      `python3 -m pytest tests/doc-health -q` — exit codes read DIRECTLY, never
      through a pipeline. `tests/doc-health` carries four known pre-existing
      failures in `test_client_identity_composition.py`; enumerate them and assert
      the set is unchanged rather than counting.
- [ ] 5.3 doc-health full run: 0 new findings. Note the live risk this slice
      carries — task 3.2 inserts a provenance section into fragments that lack
      one, so any run against a tree where a demote has executed will legitimately
      change the `staged-topic-template` family's output. Diff against a baseline
      run rather than assuming.
- [ ] 5.4 Live proof: demote a real change on a scratch branch and read the
      fragment afterwards. The defect was found by driving the verb, and the fix
      does not get to be believed on any weaker evidence.

## 6. Bookkeeping

- [ ] 6.1 README "OpenSpec Records" active block — done at proposal time.
- [ ] 6.2 Realization evidence in the front matter at the archive gate: merged
      commit/PR plus the green run. `target_release: implementation_pending` means
      this change does NOT archive on landing the requirement.

## 7. Handed back, not owned here

- [ ] 7.1 `add-staged-topic-outline-template` task 4.2 — the round-trip test —
      becomes writable once this lands, and STAYS THAT CHANGE'S TASK. Realizing
      this change is what unblocks it; discharging it is not this change's work.
      Left as an unchecked item here only so the dependency is visible from both
      sides.
- [ ] 7.2 Two open rulings this change deliberately did not take: whether
      `Status at demote` should carry the change's `task_progress` instead of a
      constant (design Decision 3), and whether the shallowest-markdown arm of the
      selection rule needs the same treatment (design Decision 1).
