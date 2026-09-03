# Tasks: add-drafted-proposal-origin

Status: ratified
Ratified by: add-drafted-proposal-origin

**PROPOSAL AND REALIZATION WERE AUTHORED TOGETHER, BY THE RULING.** Brett's
2026-09-03 word on issue #318 named the vehicle as "an OpenSpec change on
`doc-health` with a code surface (`scripts/doc_health/proposal_origin.py` +
fixtures), proposal and realization authored together", following the
`add-release-tag-publication-check` precedent for the same reason that packet
records: canon, the code that enforces it and the tests that pin them cannot
disagree across a merge boundary without reddening the gate that exists to
notice exactly that. Groups 1–3 are therefore all discharged in the branch
this packet lands on. Group 5 is the archive act, last, and open until the
merge it follows exists.

## 1. Ratification

- [x] 1.1 RATIFIED 2026-09-03 by Brett Heap in session, verbatim: "implement
      your recommendations on all these", over the lane's written
      recommendations for issues #561/#339, #318, #511, #553 and the #543 fix
      (b). For this issue the ruling resolves to SHAPE 1 of the two the issue
      offered — an origin state that declares provenance without asserting
      approval — and is recorded as the RULING comment on openxFactory issue
      #318. Record: `review/ratification-2026-09-03.md`.
- [x] 1.2 The ruling settles the SHAPE and authorizes the VEHICLE. It does
      NOT cover the six decisions taken inside that shape (D1–D6 in
      `proposal.md` § Orchestrator Decisions, argued in `design.md`), which
      are flagged for veto. D1 in particular — WHICH of the two spellings the
      ruling named — is a choice the ruling deliberately left open ("a
      `drafted` kind, or `proposed_on` without `approved_on`").

## 2. Realization — ONE slice

- [x] 2.1 `scripts/doc_health/proposal_origin.py`: the `ad_hoc` arm becomes
      three states — claims approval, claims drafting, claims neither —
      keyed on PRESENCE rather than completeness, so a half-written pair is
      reported as an incomplete claim of the state it reached for rather
      than silently re-classified as the other state. `APPROVAL_FIELDS` and
      `DRAFTING_FIELDS` become named module constants. The approval arm is
      byte-unchanged in rule text and action line (property (c)).
- [x] 2.2 `_declared_standing` — the ONE header read this family gained. It
      goes through `corpus.parse_status` + `promotion_fidelity.declared_standing`
      and compares against `promotion_fidelity.RATIFIED_OR_BEYOND`, which
      already exists and already means the thing the rule needs, so this
      family states no second opinion about what is beyond ratification. A
      packet with no `proposal.md`, no `Status:`, or an unrecognized status
      answers None and the class stays silent — `fam_status_validity` already
      reports that document.
- [x] 2.3 The two new finding classes, named in the module docstring's
      numbered list beside the existing five and in the doc-health delta's
      own enumeration: **`drafting-provenance-incomplete`** (ERROR,
      mechanical) and **`unapproved-origin-at-ratification`** (ERROR,
      resolution class `contested`).
- [x] 2.4 `scripts/proposal-support.py`: the same three-state arm in
      `origin_errors` (D5), the two field pairs copied with the file's own
      stated criterion for copying rather than importing,
      `write_origin_block` emitting whichever pair(s) the origin carries and
      refusing one that completes neither, and `declare-adhoc` gaining
      `--proposed-by`/`--proposed-on` with the approval pair no longer
      argparse-required (D6). The id stamp comes from `--approved-on` or
      `--proposed-on`, whichever is given, and never moves afterwards.
- [x] 2.5 `tests/doc-health/test_proposal_origin.py`: **18 new tests**, the
      matrix in both directions — the lawful draft silent (at every
      pre-ratification standing and with no status header at all), the same
      packet at every standing in `RATIFIED_OR_BEYOND` a `contested` ERROR,
      the half-declared drafting pair, the origin declaring neither state,
      the approval pair still owed in full at both fields, `reason` still
      owed by a drafting origin, a staged origin at `ratified` owing no
      approval, the approval-arrives-beside-the-drafting-record case, the
      gate's three arms, the writer's three arms, and the gate/family field
      agreement test. Fixtures are `tmp_path` packets built by this suite's
      own `_change` helper — the family's fixture idiom since it was
      written, because what it reads is `.openspec.yaml` text and one
      `Status:` line rather than a corpus of governed documents; the helper
      gains one optional `status=` argument and its default is unchanged.
- [x] 2.6 `EXPECTED_ACTIONS` in the family's action-pin table gains the three
      new action strings, and the table test gains the three behavioural
      cases that reach them, so the two-directional pin (`expected ==
      behavioral | static`) holds over fourteen strings rather than eleven.
- [x] 2.7 `tests/doc-health/test_lifecycle_scan_set.py`: the existing
      `proposal-origin` entry in `NON_READERS` gains a comment recording WHY
      it is still a non-reader after gaining a header read — one named
      packet's own `Status:`, not a sweep over a document list, exactly as
      `promotion-fidelity` and `duplicate-packet` are non-readers. No
      assertion moves and no count moves.
- [x] 2.8 DOCS — `docs/document-lifecycle.md` § Gates In Practice: the origin
      paragraph names the unapproved state and the two rules that bound it.
      The doc references the promoted requirements and never restates them,
      which is the discipline that paragraph already declares.
- [x] 2.9 SELF-GATE, RE-AIMED — `tests/doc-health/test_modified_block_currency_self_gate.py`:
      `_LEDGER_SUBJECTS` gains this packet's two rows. THE SELF-GATE FAILED
      FIRST, BY NAME, naming both subjects and telling the author what to do
      — which is the assertion working, not an obstacle: it is an EXACT set
      compared with `==` and never `<=`, so a newly lossy MODIFIED block
      cannot land unreported. Each row carries the per-unit explanation that
      set's convention requires and the retirement condition it requires
      ("when the packet archives and its blocks are promoted"), and the
      `_moved()` history sentence gains this packet's step (8 → 10).
      `_PAIRING_SUBJECTS` stays EMPTY — both blocks resolve against promoted
      canon rather than an active sibling's addition. No other assertion,
      count or fixture in the suite moved.

## 3. Evidence measured before the packet went up

- [x] 3.1 **No collision.** Every ACTIVE change's `specs/doc-health/spec.md`
      and `specs/document-lifecycle/spec.md` read for a live delta on either
      requirement this packet MODIFIES: `add-nightly-dashboard-refresh` ADDS
      seven unrelated requirements, `settle-aging-staging-topics` MODIFIES
      "Aging threshold defaults", `add-ideation-intent-plane` MODIFIES "Gates
      happen on main". Neither of this packet's two titles has another
      writer.
- [x] 3.2 **The MODIFIED blocks were copied from canon verbatim and then
      edited**, both of them, and the five doc-health scenarios plus the four
      document-lifecycle scenarios canon carries are all restated —
      `modified-block-currency`'s gate-bearing arm (scenario-title
      completeness, `error`) reads **0** on both blocks.
- [x] 3.3 **The new findings have an empty population by construction, and it
      is measured.** All **109** ad-hoc origins in this repository's active
      and archived corpus carry a complete approval pair; **0** carry
      neither, **0** carry half of one, and `proposed_by`/`proposed_on`
      appear in no packet. Nothing this change adds can fire on anything that
      exists today.
- [x] 3.4 **The direction of the one behavioural change to an existing class
      is strictly fewer findings** (D4): an ad-hoc origin declaring neither
      state produced two findings and now produces one. No input anywhere
      produces MORE findings than it did.
- [x] 3.5 The medx packets read as the evidence for what the missing shape
      cost: both were admitted by ruling on 2026-08-25, and both spend a
      paragraph of `approved_by` prose insisting in capitals that the
      approval is an admission and not a ratification — the vocabulary doing
      two jobs with one word.
- [x] 3.6 The `:adhoc:` id's date is the DECLARATION date, not the approval
      date — measured on `create-medxchart-overlay-boundary`, which carries
      `:adhoc:2026-08-23-…` and was approved 2026-08-25. That is what lets
      the durable id be minted once at drafting and never move (D1).

## 4. Recorded, not fixed

**A TICK IN THIS GROUP MEANS THE RECORDING IS DONE, NOT THAT THE THING IS
FIXED.**

- [x] 4.1 RECORDED, NOT FIXED. **Adding an approval to an existing drafted
      origin is a HAND amendment.** `write_origin_block` refuses to overwrite
      an existing declaration — that refusal is the immutability guard and is
      deliberately not relaxed — so the two approval lines are added by hand,
      as every ad-hoc `reason` block in this corpus already is. Automating
      the transcription of an authority's words is available as a later
      change; it is not available as an implementation detail of this one.
- [x] 4.2 RECORDED, NOT FIXED. **`kind: ad_hoc` no longer implies approval on
      its own.** A reader must look at the fields to know the state. Bounded
      (the fields were always the load-bearing part) and disclosed in
      `design.md` § D1 rather than left for a reader to discover.
- [x] 4.3 RECORDED, NOT FIXED. **A `staged` origin has no drafting state.**
      Its provenance is the topic and the transition record, it has never
      carried an approval pair, and this change does not ask it to. If a
      staged packet ever needs to declare "drafted but not admitted", that is
      a successor and a different argument.

## 5. Archive

- [ ] 5.1 ARCHIVE ON MERGED-PLUS-GREEN, never on landing. This packet carries
      a code surface, so under `docs/release-realization-flow.md` § The
      Archive Gate it archives only after the PR merges with green
      realization evidence on `main`: `python3 -m pytest tests/doc-health`,
      `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`, and a
      doc-health single-repo run moving by the predicted amount and no other
      line. Archived via `proposal-support.py archive`, never bare
      `openspec`.

## 6. Executed

| Command | Result |
| --- | --- |
| `OPENSPEC_TELEMETRY=0 openspec validate add-drafted-proposal-origin --strict` | `Change 'add-drafted-proposal-origin' is valid` |
| `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` | (recorded at the ratification commit — see `review/ratification-2026-09-03.md`) |
| `python3 -m pytest tests/doc-health -q` | (recorded at the ratification commit — see `review/ratification-2026-09-03.md`) |
| `python3 -m pytest tests/doc-health/test_proposal_origin.py -q` | **58 passed, 0 failed** (40 before this change) |
| `python3 scripts/doc-health.py --single-repo .` on `origin/main` (`2b0615da`, clean worktree) | **6 critical, 6 error, 29 warning, 14 info**; `proposal-origin`: no findings |
| the same run on this branch | **6 critical, 6 error, 29 warning, 16 info**; `proposal-origin`: no findings |
| the two reports diffed | **+2 `info` and nothing else** — both this packet's own MODIFIED blocks in `modified-block-currency`'s carriage ledger, the editorial arm every reworded active MODIFIED block in this corpus produces one of (8 in the baseline, from six other active changes). Zero new `critical`, `error` or `warning`. |
