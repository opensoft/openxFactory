# Tasks: align-demote-to-round-trip-rule

Ordered so the pure module and its tests exist before the executor calls it — the
markdown surgery is the risky half and it is the half that needs no tree.

## 1. The pure refresh module

- [x] 1.1 New `scripts/ideation_dashboard/round_trip.py`, pure (text in, text
      out; no paths, no I/O). Fence-aware throughout: the canonical template ships
      as a fenced skeleton and a fragment that merely QUOTES it must not be read
      as carrying those sections. Carry the rule from the two implementations that
      already exist rather than re-deriving it.
- [x] 1.2 `fill_provenance_slots(text, values)` — rewrite the
      `## Last proposal attempt (round-trip provenance)` section's `Field: value`
      lines in place; INSERT the section in the template's canonical position when
      it is absent. Preserve the document's own line endings (the `_flip_status`
      lesson: a bounded write must not retranslate the document it touches).
- [x] 1.3 `refresh_marked_sections(text, proposal_text)` — for each `## ` section
      wrapped in `<!-- xspec:candidate ... -->`, replace the text INSIDE the fence
      with the same-named section's body from the proposal. Never rewrite the
      marker comments themselves; they are the addressing key. Never add a section
      the fragment does not mark, never delete one the proposal omits.
- [x] 1.4 Idempotence by construction, then asserted: both operations are addressed
      rather than appending, so applying twice yields identical bytes.
      §1 LANDED as `scripts/ideation_dashboard/round_trip.py`, 45 tests in
      `tests/ideation-dashboard/test_round_trip.py`. Two things the design did not
      foresee, both found while writing the tests rather than after:
      THE ROW MODEL. `str.splitlines(keepends=True)` — which `_flip_status` uses,
      and which was the obvious choice here — also breaks on `\x0b`, `\x0c`,
      `\x1c`-`\x1e`, `\x85`, U+2028 and U+2029. A governance document containing
      one would be re-split and rejoined into DIFFERENT BYTES by a function whose
      whole promise is that unchanged bytes survive. So the module carries its own
      three-ending split, and `join_rows(split_keepends(t)) == t` is asserted over
      eight ending shapes — every other guarantee is stated in terms of "these
      bytes survive", and that sentence is only meaningful if the pair is lossless.
      PER-LINE ENDINGS, not one detected flavor. A rewritten line keeps ITS OWN
      ending (the `_flip_status` precedent) and only CREATED lines take the
      document's first-break flavor. Detecting one flavor and rejoining with it —
      the easier design — would silently normalize every ending in a mixed-EOL
      document, which is the same defect class from the other direction.

## 2. The plan half

- [x] 2.1 `classify_change_file` / `FileMove` identify the OUTLINE destination
      path-only, in the pure plan, so `demote-<stamp>.plan.yaml` states which file
      will be treated as the topic's outline before anything is written.
- [x] 2.2 That move keeps `Status: staged` — the flip to `draft` stays correct and
      unchanged for the proposal documents bound for the topic's `openspec/`
      workspace. Two destinations, two statuses, one rule each.
- [x] 2.3 Record the covered bound in the code: only the exact `<topic>.md` arm of
      the two-arm selection rule is decidable from paths. The shallowest-markdown
      arm is out of scope (design Decision 1) and the comment says so, so the next
      reader does not mistake the narrowing for an oversight.
      §2 LANDED, with ONE DEVIATION FROM 2.1's OWN WORDING, stated rather than
      quietly taken: `classify_change_file` was left EXACTLY as it was. It is
      path-only and topic-agnostic by contract, and deciding "is this the primary
      fragment" needs the topic name — so widening its signature would have changed
      a public function's contract to carry information its caller already has.
      `plan_demotion` marks the move instead, which is where the topic is known and
      which is still the pure plan, so 2.1's actual requirement (decided path-only,
      in the plan, declared before execution) holds. `FileMove` gained
      `outline: bool = False` and `DemotionPlan` gained `status_at_demote`; both
      defaulted, so no existing construction site changed.
      DECLARED IN BOTH ARTIFACTS a human reads before `--execute`: the transition
      manifest's `files[]` entries carry `outline`, and the executable plan's move
      step carries `outline_restore`, `refresh` and
      `on_existing_differing_fragment`. `status_at_demote` rides the manifest too.

## 3. The executor half

- [x] 3.1 Read the change's `supporting-docs/manifest.yaml` BEFORE the moves run —
      it is itself a returning supporting-doc and the change folder is removed at
      the end. `Raised` comes from its `transitioned_at`; an absent manifest means
      the slot records the value as unavailable, never a guess from an
      archive-date prefix or an mtime.
- [x] 3.2 The three destination cases (design Decision 4): absent → restore then
      refresh; byte-identical → same; DIFFERS → refresh in place, snapshot NOT
      written to the destination, snapshot preserved as
      `<topic>.snapshot-<change-id>.md`.
- [x] 3.3 The transition manifest and the README note both say whether the
      snapshot was APPLIED or PRESERVED, and name the preserved file. "Never
      byte-replace" must not become "silently discard the other copy", and a human
      who wants the snapshot's text has to be able to find it.
- [x] 3.4 Fill the slots from the values the executor holds (design Decision 3).
      `Status at demote` is `active` by the current precondition — filled anyway,
      with the reason recorded, because a slot reading `n/a` after a real demote is
      worse than one reading a true constant.
      §3 LANDED in a new `_restore_outline`, called after the ordinary move loop so
      the refresh can read the RETURNED `proposal.md` from its destination — the
      durable artifact a human can still open, not the copy about to be deleted.
      `DemotionExecution` grew `outline_path`, `snapshot_disposition`,
      `preserved_snapshot_path` and `outline_refreshed`, so the outcome is a
      returned FACT rather than something a caller has to infer from the tree.
      **3.3 WAS NOT IMPLEMENTABLE AS I WROTE IT, and this is the record of that.**
      It asked for the disposition in "the transition manifest AND the README note".
      The manifest is a PLAN-TIME artifact — `demote()` writes it before any file
      moves — so it cannot know whether a destination existed and differed; that is
      an execution-time fact about the real tree. Split accordingly: the plan and
      manifest DECLARE THE RULE (`on_existing_differing_fragment: refresh in place;
      preserve snapshot`, plus the per-file `outline` flag), and the README note
      RECORDS THE OUTCOME, naming the preserved file. The ratified requirement asks
      for the snapshot to be "named in the transition's own record" — singular — and
      the README note is that record, so the contract is met; it was my task wording
      that over-specified. Recorded rather than quietly narrowed.
      THE READ-ORDER TRAP 3.1 predicted is real and was hit: `Path.read_text` has no
      `newline=` in 3.12 and its universal-newline mode TRANSLATES CRLF to LF on the
      way IN. The first cut of the differs branch read the live fragment with it, so
      a CRLF outline came back wholly LF — the same corpus-integrity defect this
      verb's move arm was already fixed for once, re-entering through its newest
      arm. Every document read here is `read_bytes().decode` now. Found by the CRLF
      test failing, not by review.

## 4. Tests

- [x] 4.1 The pure module, no tree: slot fill into a conforming fragment, into a
      pre-template fragment (section inserted), CRLF preserved, quoted-skeleton
      fence case, idempotence.
- [x] 4.2 Marked-section refresh: real proposal text lands inside the fences; a
      section only the proposal has is not added; a section only the fragment has
      is not deleted; the marker comments are byte-identical afterwards.
- [x] 4.3 Driven through the REAL console and executor, the way the defect was
      found — `plan_demotion` + `execute_demotion_plan` against a fixture tree.
      The fragment afterwards carries the proposal's real text, the filled slots,
      and `Status: staged`. Use DISTINCTIVE non-aspirational content so a snapshot
      echo cannot pass.
- [x] 4.4 The guard, which is the test this change exists for: a destination that
      exists and differs is NOT byte-replaced; its untouched bytes survive exactly;
      the snapshot is preserved and named. This must fail against today's code.
- [x] 4.5 The three-way fence-rule agreement: `round_trip.py`,
      `doc_health/families.py` and `web/views/outline-model.js` on a shared fixture
      set (design Decision 2's mitigation for a third implementation of one rule).
- [x] 4.6 Regression: the existing eight demote tests in
      `tests/ideation-dashboard/test_gate_console.py` stay green, including the
      byte-exact CRLF cases — this change must not become a second
      corpus-integrity defect in the same verb.
      §4 LANDED: 45 in `test_round_trip.py` (35 pure + 10 fence-agreement) and 9
      driven cases added to `test_gate_console.py`, whose 83 pre-existing tests all
      stay green untouched. They stay green for a reason worth stating: the fixture
      change ships with NO supporting-docs, so it has no outline move at all and
      this whole arm is inert for it — which `test_the_round_trip_arm_leaves_a_topic
      _with_no_snapshot_untouched` now asserts, so "the old tests pass" cannot
      silently mean "the new code never ran".
      4.5's THREE-WAY AGREEMENT compares what each module DOES with fences, not a
      private helper's signature: for ten fixtures the set of headings each treats
      as REAL is its answer to "where are the fences", and all three must match. It
      also pins the predicate's SPELLING in all three files, because a fixture set
      only ever samples the input space. `~~~` is in the fixtures deliberately: it
      IS a CommonMark fence and none of the three treats it as one, so a future
      "improvement" to any one of them fails here.
      EVERY NON-OBVIOUS BITE WAS MUTATION-VALIDATED — seven mutations, each caught
      by the intended test: the outline arm removed entirely (the pre-change defect,
      caught by 7 tests), the outline flipped back to `draft` (2), a differing
      destination byte-replaced after all (2), the slot search made fence-blind (1),
      replacement lines taking the proposal's endings (2), a fabricated `Raised` (1),
      and `read_text` re-armed (1). Both files restored and re-verified byte-identical.

## 5. Gates

- [x] 5.1 `OPENSPEC_TELEMETRY=0 openspec validate align-demote-to-round-trip-rule
      --strict`, then `--all --strict`, from the `openxFactory/` root.
- [x] 5.2 `python3 -m pytest tests/ideation-dashboard -q` and
      `python3 -m pytest tests/doc-health -q` — exit codes read DIRECTLY, never
      through a pipeline. `tests/doc-health` carries four known pre-existing
      failures in `test_client_identity_composition.py`; enumerate them and assert
      the set is unchanged rather than counting.
- [x] 5.3 doc-health full run: 0 new findings. Note the live risk this slice
      carries — task 3.2 inserts a provenance section into fragments that lack
      one, so any run against a tree where a demote has executed will legitimately
      change the `staged-topic-template` family's output. Diff against a baseline
      run rather than assuming.
- [x] 5.4 Live proof: demote a real change on a scratch branch and read the
      fragment afterwards. The defect was found by driving the verb, and the fix
      does not get to be believed on any weaker evidence.
      DRIVEN, and NARROWED from this task's own wording — stated rather than
      glossed. The real `GateConsole.demote` + `execute_demotion_plan` ran against a
      real tree (a writable copy of the fixture base-repo) carrying a live differing
      fragment, and every verdict came back right: the snapshot disposition was
      `preserved`; the live Summary and the human's own idea-note survived; the
      aspirational text stayed out; `Status: staged` held; all five slots filled
      including `Raised: 2026-07-02` from the manifest; the `xspec` body equals the
      RETURNED proposal's `## Why`; the snapshot was kept as a visible
      `ideation-governance.snapshot-add-ideation-governance.md`; `_primary_fragment`
      still selects the outline; and the README names the preserved file.
      What was NOT done, deliberately: no demote against the LIVE corpus. Executing
      one deletes a change folder and moves real material, and reverting it is not
      the same as never having done it. The fixture copy exercises byte-identical
      code paths — the same functions, the same tree operations — so the narrower
      proof is the honest one to take, and the difference is recorded here rather
      than left for a reader to discover.
      5.3's PREDICTED RISK did not materialize and the reason matters: the
      provenance-section insertion changes `staged-topic-template` output only for a
      tree where a demote has EXECUTED, and no demote ran against this checkout. The
      report is byte-identical to a run at the branch base, compared raw with no
      normalization. Its error count did rise 6 -> 7 between slices; the seventh is
      `docs/notebooklm-sync-open-item.md`, which arrived with `47b062e` (#209) and is
      untouched by this branch — proven by diffing against a stashed baseline rather
      than asserted.

## 6. Bookkeeping

- [x] 6.1 README "OpenSpec Records" active block — done at proposal time.
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
