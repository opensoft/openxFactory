# Tasks: sanction-ratified-record-spelling

Nothing below §1 may start before §1 completes. This change proposes a rule
the ratifier's own instruction already operates under; the ratification is
what makes it a rule rather than an observation.

## 1. Ratification (Brett)

- [x] 1.1 Brett reads the proposal and rules OQ-1 through OQ-5. RULED
      2026-08-22, in-session, multiple-choice round: every recommended
      option adopted (OQ-3 unopposed in prose) — OQ-1 KEEP the `doc-health`
      delta; OQ-2 sanction BOTH spellings; OQ-3 floor stays at ONE of
      approver/date/resolvable-record; OQ-4 EXACTLY ONE citation line per
      document; OQ-5 a floor violation is CRITICAL, same tier as a dangling
      `Ratified by:` reference.
- [x] 1.2 Brett ratifies or declines. On ratification, flip `Status: draft` →
      `Status: ratified` in `proposal.md` front matter and add the citation
      line in the spelling this change itself sanctions: `Ratified by:` if an
      approving OpenSpec change is named, otherwise `Ratified:` naming
      approver, date, or record. The change is its own first conformance test.
      Ratified 2026-08-22; `proposal.md` front matter now carries
      `Status: ratified` and a `Ratified:` line (no approving OpenSpec change
      exists for this proposal, so it cites itself in the record-citing
      spelling it sanctions — approver, date, and a resolvable record all
      named, exceeding its own one-of-three floor).
- [x] 1.3 If OQ-1 is ruled "defer", delete `specs/doc-health/spec.md` from
      this change and record the deferral here, naming the follow-up.
      Re-validate `--all --strict` after the deletion. NOT TAKEN — OQ-1 was
      ruled KEEP, not defer; `specs/doc-health/spec.md` stays in this change.
- [x] 1.4 Record each ruling inline under its Open Question in `proposal.md`
      (the RULED-line convention `add-doxchat-model-intake` uses), so a later
      reader finds the decision beside the question rather than only in a
      commit message. Done: each of the five Open Questions in `proposal.md`
      carries its own RULED line in place (alternatives' text kept, not
      deleted), and design.md's D1 and D3 (where OQ-3 and OQ-1 are discussed)
      each carry a matching RULED note pointing back to proposal.md.

## 2. Realize the prose (`docs/document-lifecycle.md`)

- [x] 2.1 Replace the single § Status Claim Rules bullet ("A `ratified`
      header names the approving OpenSpec change (`Ratified by: <change>`)")
      with the two-spelling rule and the three-way floor, worded to match the
      ratified requirement text rather than paraphrasing it. Done: the bullet
      is now a lead-in plus two sub-bullets, one per spelling, carrying the
      requirement's own terms — "exactly one of two spellings", "never both,
      and never neither", the bare uncited header "is a violation whatever
      else the document says", and the floor's "at least one of an approver,
      a date, or a resolvable record path".
- [x] 2.2 State the condition of use explicitly in the prose — primary where
      an approving change exists, record-citing only where none does — since
      the prose is what authors actually read at authoring time. Done:
      `Ratified by:` is "required wherever an approving OpenSpec change
      exists to name"; `Ratified:` is "legal only where no approving OpenSpec
      change exists to name", with the delta's list carried whole: its FOUR
      named examples (in-session ruling, disposition, `.openspec.yaml`
      approval pair, archive or ratification commit) AND its catch-all, "or
      another durable record". FIX LAP (adversarial review F6): the prose
      first shipped with the list truncated — "an archive commit", full stop,
      dropping both the "or ratification" half of the fourth example and the
      catch-all — which read as a CLOSED list of four and would have made
      every honest record outside those four look illegal. Recounted and
      restored to match the delta word for word.
- [x] 2.3 State that the floor applies to `Ratified:` only, and that a
      `Ratified by:` line naming its change and nothing else is complete.
      Done, both in one place each: "That floor applies to `Ratified:` alone
      and never reaches `Ratified by:`, whose named change is itself the
      record", and "a line naming its change and nothing else is complete".
- [x] 2.4 Do NOT edit any other document. No existing citation line in the
      corpus is rewritten by this change; verify with
      `git diff --stat` that `docs/document-lifecycle.md` is the only
      governed document touched. Verified: `git diff --stat` lists exactly
      two tracked files, `docs/document-lifecycle.md` and
      `scripts/doc_health/families.py` (code, not a governed document), plus
      the new test module. One SECOND edit was made inside
      `docs/document-lifecycle.md` itself and is called out rather than
      buried: the Document Status Taxonomy table's `ratified` row read
      "Backed by an approved OpenSpec change; header names it", which
      contradicts the rule being written one screen below it, and now reads
      "…, or by a durable ratification record where no such change exists".
      Same document, one clause, no citation line anywhere in the corpus
      rewritten.

## 3. Realize the check (`fam_ratified_provenance`)

- [x] 3.1 Widen the read to TWO prefixes, `Ratified by:` and `Ratified:`.
      Per design D2, do NOT collapse them into `_header_line(doc, "Ratified")`
      — that matches body prose and would pass every test written against
      today's corpus while breaking on the first document whose header window
      opens with such a line. Done: two module constants,
      `_RATIFIED_BY_PREFIX` and `_RATIFIED_RECORD_PREFIX`, with D2's reasoning
      recorded above them. The prefixes are disjoint by construction — a
      `Ratified by:` line does not start with `Ratified:` — so no line is
      read under both rules, and `test_the_two_prefixes_are_disjoint` pins
      that neither constant is the bare word.
- [x] 3.2 Leave the `Ratified by:` path byte-for-byte behaviourally
      unchanged: change-id intersection, then `_link_targets` resolution,
      then the cross-repo `openxFactory` escape hatch. Done: the three steps
      and the finding they raise are moved under `if by_line:` and otherwise
      untouched, including the escape hatch's comment. The old function
      computed `ok = False` then guarded on `if line:`; with the line present
      the two forms are identical.
- [x] 3.3 Implement the floor for the `Ratified:` path: pass when the line
      names an approver, a date, or a resolvable record path; fail when it
      names none. Reuse `_resolves`/`_link_targets` for the record axis
      rather than adding a second resolution rule. Done, cheapest axis first
      — mirroring the primary path's own shape. Approver is
      `_CITATION_APPROVER`, a `by <Proper Name>` clause; date is
      `_CITATION_DATE`, an ISO calendar date; record is `_link_targets` +
      `_resolves`, unchanged and unduplicated. Both regexes carry a comment
      saying they are heuristics and why a narrow one is safe under a
      disjunctive floor.
- [x] 3.4 Emit a distinct finding message for the floor failure — the
      existing "Ratified by: missing or does not resolve to an OpenSpec
      change" is false when the document carries a `Ratified:` line. Severity
      per the OQ-5 ruling. Done: "Ratified: names none of an approver, a
      date, or a resolvable record path", at CRITICAL per OQ-5.
      `test_record_citation_naming_none_of_the_three_is_critical` asserts the
      message does not mention `Ratified by:` at all.
- [x] 3.5 Report a `ratified` document carrying NEITHER prefix under a
      message that names both spellings, not just the primary. Done:
      "ratified header carries no citation in either sanctioned spelling",
      with an action naming both spellings and their conditions of use. This
      case previously shared the dangling-reference message; it no longer
      does, and the dangling message is now reserved for a `Ratified by:`
      line that is present and does not resolve.
- [x] 3.6 Tests in `tests/doc-health/`, each pinning one boundary:
      (a) `Ratified by:` naming a change id — pass, unchanged;
      (b) `Ratified by:` naming a change id and nothing else — pass, the
      floor does not reach it (this is the 13-document regression guard);
      (c) `Ratified by:` dangling — CRITICAL, unchanged;
      (d) `Ratified:` with approver only, date only, and record only — three
      passing cases;
      (e) `Ratified:` with none of the three — finding;
      (f) `Status: ratified` with no citation line at all — finding;
      (g) a document whose header window opens with `Ratified together with…`
      or a `Ratified: <prose>` section label — NOT read as a citation;
      (h) a citation past `STATUS_SCAN_LINES` — not found, window unchanged.
      Done: `tests/doc-health/test_ratified_citation_spellings.py`, 15 tests,
      all eight boundaries covered — (a)/(b) `..._resolving_to_a_change...`
      and `..._naming_its_change_and_nothing_else_is_complete` (the latter
      asserts the line names no approver, no date and no path BEFORE
      asserting it is clean, so it fails if the floor is ever widened to the
      primary spelling); (c) `..._dangling_is_still_critical`, matching the
      message exactly; (d) three separate axis tests, the record-axis one
      asserting the other two axes really are absent from its fixture rather
      than trusting the wording, plus a fourth showing the record axis is
      RESOLVABLE-path and not path-shaped; (e) `..._none_of_the_three...`;
      (f) `..._no_citation_names_both_spellings`; (g) both shapes — the prose
      sentence placed INSIDE the header window, where the short-prefix
      collapse is observable, and the section label below it; (h)
      `..._past_the_window_is_not_found`. Two extra tests cover the OQ-4
      both-lines rule, one of them with both lines individually valid so the
      rule is pinned as structural rather than as a fallback.
      FIX LAP: five more tests, taking the module to 20 — see 6.2 (three on
      the one-total count) and 6.3 (two on the primary path's rejection).
- [x] 3.7 Mutation-validate the new assertions: revert each behavioural change
      one at a time and confirm the matching test fails. Per the
      platform-inert-mutation lesson, a mutation that survives because the
      assertion only checks a value that happens to coincide does not count —
      pin the structure, not the coincidence. Done: five mutations
      hand-applied to `families.py`, each run against the new module alone
      (so a kill by a pre-existing test does not mask a gap), each reverted
      with a byte-equality assertion afterwards. All five killed:
      M1 accept any `Ratified:` unconditionally → 2 failed;
      M2 floor inverted → 4 failed;
      M3 both-lines check dropped → 2 failed;
      M4 D2 short-prefix collapse to `"Ratified"` → 11 failed;
      M5 floor also applied to `Ratified by:` → 3 failed, led by the
      13-document regression guard, which is the mutation this change was
      most likely to ship.
      FIX LAP: this round of five was not enough — the adversarial review
      hand-applied two loosenings that ALL of it survived (F4 and F5). Three
      more mutations, M6-M8, are recorded at 6.4, each one run twice: once
      with the new guard deselected, to prove it really was surviving the
      whole suite before, and once with it active, to prove the kill.
- [x] 3.8 Measure, do not assume: run doc-health before and after over the
      same tree and record that the severity counts are identical. A moved
      count means the widening reached a document it should not have.
      Measured IN-TREE at `a316a10`, single-repo, same tree both times.
      Severity counts identical: 4 critical, 6 error, 68 warning, 4 info,
      before and after; the `ratified-provenance` section reads "No findings"
      in both reports. The ONLY textual difference between the two reports is
      the word census (+153 words on the one `standard` document this change
      edits), which is the edit itself and not a finding. Family-level
      measurement over the governed corpus, also before and after:
      327 documents examined (nonzero, asserted), 22 at `Status: ratified`,
      28 carrying `Ratified by:` inside the header window, ZERO carrying
      `Ratified:`, zero carrying both, zero findings. The 28 is the in-window
      count; the proposal's 29 counts one citation the proposal itself
      records as sitting past the window.

## 4. Gates, record, archive

- [x] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate sanction-ratified-record-spelling --strict`
      and `--all --strict`, exit codes read directly, not through a pipe.
      Both exit 0. `--all --strict` reports 68 passed, 0 failed (68 items:
      49 promoted specs + 19 active changes; the count is 68 rather than 67
      because `add-substantive-review-lane` was proposed after this change's
      authoring measurement).
- [x] 4.2 `python3 -m pytest tests/doc-health` and
      `python3 -m pytest tests/ideation-dashboard -k workbench`, both green,
      exit codes read directly (`pipefail` discipline: never `| tail`).
      Both exit 0: doc-health 719 passed (704 baseline + 15 new), workbench
      140 passed / 3858 deselected. Every line this change adds is free of
      the upper-case four-letter HTTP verb whose presence anywhere in prose
      breaks the staging-workbench no-write-path test — checked by grep over
      the diff, not assumed. FIX LAP (adversarial review F7): this read-back
      first stated that claim by spelling the token out, which made the
      sentence refute itself in the very file it was making the claim about.
      Re-run after the fix lap: doc-health 724 passed (719 + 5 new),
      workbench 140 passed.
- [ ] 4.3 README "OpenSpec Records" row updated from the Active block to the
      realization state as the change lands, and to the archived form at
      archive. NOT DONE IN THIS SLICE, deliberately: the row moves at the
      archive gate, which is a later slice.
- [ ] 4.4 Archive only on merge-plus-green on the openxFactory main line, per
      `target_release: implemented`. No contract bundle is cut and no release
      tag is owed; the archive-gate evidence is the merged PR plus the green
      runs, named in this file before the archive commit.
- [ ] 4.5 On archive, confirm the promoted `document-lifecycle` requirement
      carries all EIGHT scenarios (three restated, five added — the fifth
      added on the fix lap, see 6.1) and that the promoted `doc-health`
      requirement's other seven scenarios are byte-identical to their
      pre-change text — the MODIFIED-delta scenario-drop failure mode,
      checked rather than trusted. The whole-capability arithmetic to check
      against: `document-lifecycle` 52 → 57 scenarios, 13 requirements
      unchanged.

## 5. Explicitly out of scope

- [ ] 5.1 `openspec/` joining `GOVERNED_ROOTS` — the event that makes the 15
      latent lines live. Separate decision, much larger blast radius.
- [ ] 5.2 `2026-08-22-add-doxbench-editing-phase-b`'s missing citation and
      `2026-08-22-add-roster-device-admission-surface`'s out-of-window one.
      Both are archived-record edits, which the register routes through a
      citing change and a ruling per record.
- [ ] 5.3 Rewriting any existing citation line to a preferred shape.

## 6. Fix lap (adversarial review, 2026-08-22)

The review of the realization returned FIX FIRST on six confirmed findings,
each with a demonstration. This section records what each fix changed, and —
where a fix amended this change's own deltas — the ruling already on record
that the amendment EXECUTES. No amendment here decides anything new; each one
writes down a decision Brett already made.

- [x] 6.1 **F1 — the both-lines finding was a kind no delta enumerated.**
      The realization emits CRITICAL `carries both Ratified by: and Ratified:
      citations`, correctly and on instruction: OQ-4 was RULED on 2026-08-22
      as "EXACTLY ONE citation line per document; a document carrying both is
      itself a finding" (proposal.md, OQ-4). But the enforcement contract did
      not carry it — the `doc-health` delta's `Lifecycle conformance checks
      fire` WHEN clause enumerated three ratification violation kinds, not
      four, and the `document-lifecycle` delta carried the exactly-one rule
      in its requirement BODY with no scenario. The check therefore emitted a
      finding class the promoted contract did not authorize, which is the
      precise defect the §2 delta exists to prevent for the other kinds.
      **AMENDMENT TO THIS CHANGE'S OWN DELTAS, executing OQ-4's recorded
      ruling** — the ruling is the authority, this is only its transcription:
      (a) `specs/doc-health/spec.md` gains a fourth ratification bullet in
      the WHEN enumeration, "a `ratified` document whose lifecycle header
      carries more than one ratification citation (one of each spelling, or
      the same spelling twice)"; (b) `specs/document-lifecycle/spec.md` gains
      a fifth scenario, `A ratified header carries more than one citation`,
      in the sibling scenarios' WHEN/THEN/AND voice. Arithmetic recounted
      in-tree rather than carried forward: `openspec/specs/document-lifecycle/spec.md`
      holds 52 scenarios across 13 requirements today, three of them on the
      modified requirement, so the Impact line moves 52 → 56 to 52 → 57 and
      task 4.5's "seven scenarios (three restated, four added)" becomes eight
      (three restated, five added).
- [x] 6.2 **F4 — "exactly one citation" was enforced only ACROSS spellings.**
      `_header_line` returns the FIRST match per prefix, so two `Ratified by:`
      lines, or two `Ratified:` lines, passed clean; the reviewer demonstrated
      both. That is not what the requirement says — "a document SHALL carry
      exactly one ratification citation" is ONE TOTAL — nor what OQ-4 ruled
      ("EXACTLY ONE citation line per document"). A rule that says exactly one
      cannot be enforced by a reader that stops at the first one.
      Realization: new `_header_lines` returns ALL matching real lines in the
      window and `_header_line` now delegates to it (first match or None,
      unchanged for its four remaining call sites — `Backed by:`,
      `Superseded by:`, `Retired:`, `Reason:`); `fam_ratified_provenance` fires
      when `len(by_lines) + len(record_lines) > 1`. The message distinguishes
      the cases honestly rather than calling a same-spelling pair "both":
      `carries both Ratified by: and Ratified: citations` for one of each,
      `carries N Ratified by: citation lines, not one` / `carries N Ratified:
      citation lines, not one` for a duplicate.
      **AMENDMENT, executing OQ-4:** the delta's clause is sharpened from "and
      MUST NOT carry both" to state the count is one TOTAL and that the same
      spelling twice is the same violation — the reading the ruling's own
      words carry, made unmissable so no future reader repeats the
      first-match implementation.
      Three tests added: two `Ratified by:` where the FIRST resolves; two
      `Ratified:` where the FIRST clears the floor (both chosen so a
      first-match reader calls the document clean); and the cross-spelling
      pair in the REVERSE order, so the rule is pinned as order-independent.
      Baseline verified before enforcing: the governed corpus carries 22
      `ratified` documents, all 22 citing with `Ratified by:`, ZERO carrying
      a duplicate in either spelling and zero carrying both — so this
      enforcement moves no live count, which 6.5 confirms end to end.
- [x] 6.3 **F5 — nothing pinned the primary path's rejection.** Letting the
      floor rescue a non-resolving `Ratified by:` turned CRITICAL → CLEAN and
      the whole 719-test suite stayed green: the only dangling fixture,
      `Ratified by: ghost-change`, trips neither floor axis, so it cannot
      observe a rescue. The delta forbids the rescue ("The named change IS the
      citation"), and the shape at risk is the one the corpus writes 18 times
      under `openspec/` — `Ratified by: Brett Heap on 2026-08-22, in-session`
      — which goes live the moment 5.1 happens. No code change was needed;
      the defect was a missing guard. Two parametrized cases added, one
      tripping the DATE axis and one the APPROVER axis, because a rescue could
      be written on either. Each asserts its fixture really trips its axis
      before asserting the finding stands. The `document-lifecycle` prose
      gains the matching sentence: naming an approver and a date after
      `Ratified by:` instead of a change does not complete that spelling.
- [x] 6.4 **Mutations M6-M8, each run twice.** Every one is hand-applied to
      `families.py`, run against the FULL `tests/doc-health` suite (not the
      new module alone) first with the new guard deselected and then with it
      active, and reverted with a SHA-256 byte-equality assertion afterwards.
      M6 — count reduced to the both-spellings pair (`if by_lines and
      record_lines:`): 722 passed with the two 6.2 duplicate guards
      deselected, i.e. it was surviving everything shipped; 2 failed with them
      active.
      M7 — the exactly-one check disabled outright: 5 failed, the two 6.2
      guards plus all three both-lines tests.
      M8 — the three-way floor allowed to rescue a non-resolving `Ratified
      by:`: 722 passed with the two 6.3 guards deselected — the review's
      demonstration reproduced exactly — and 2 failed with them active.
- [x] 6.5 **F2 — approver-axis false CRITICALs, closed by DISCLOSURE.**
      `_CITATION_APPROVER` is `\bby\s+[A-Z][\w.'-]*`, which does not recognize
      an approver named inside a parenthetical — design D1's own row-3 shape,
      `Ratified: ruling round (Brett Heap presiding)`. Live impact is zero
      (no governed `Ratified:` line exists at all), so the choice was between
      widening the pattern and disclosing its edge. DISCLOSURE was chosen:
      a wider pattern guessing at proper names inside free prose would trade a
      rule an author can read for one an author discovers from a finding, and
      guessing is the failure OQ-3's reasoning rules against. Three places
      now say so — `docs/document-lifecycle.md` § Status Claim Rules states
      the recognized form is `by <Name>` and names the remedy (add the clause;
      never invent a date), the pattern's comment in `families.py` records the
      narrowing as deliberate and disclosed, and design D1 gains a paragraph
      stating the narrowing against its own table row and why widening was
      refused.
- [x] 6.6 **F6 — prose dropped the delta's catch-all**; fixed at 2.2, which
      also carries the corrected count.
      **F7 — a self-refuting read-back**; fixed at 4.2, reworded so the claim
      is true of the file that makes it.
- [x] 6.7 **A pre-existing guard the fix lap had to repair, called out rather
      than buried.** 6.2's `_header_lines` introduction moved the seam that
      `test_families_real_lines.py::test_mutation_reverting_header_line_alone_reproduces_the_false_finding`
      monkeypatches: that guard reverts the header reader to
      `str.splitlines()` and asserts the false CRITICAL reappears, and it
      patched `families._header_line`, which `fam_ratified_provenance` no
      longer calls. Left alone it went RED, so the refactor was caught by it
      immediately. The patch target is re-pointed at `_header_lines`, the
      reader the family now reads through and the one `_header_line`
      delegates to — so the mutation reverts BOTH readers at once, which is
      strictly the same single-seam mutation aimed at the seam's current
      name. Its intent, fixture and assertion are untouched, and it is
      self-checking: if the patch stopped reaching the family the fixture
      would come back clean and the guard would fail.
- [x] 6.8 **Gates re-run after the fix lap**, exit codes read directly.
      `openspec validate sanction-ratified-record-spelling --strict` exit 0;
      `--all --strict` exit 0, 68 passed / 0 failed (68 items, unchanged —
      `origin/main` is still `a316a10`, so nothing moved under this branch).
      `pytest tests/doc-health` exit 0, 724 passed (719 + 5 new).
      `pytest tests/ideation-dashboard -k workbench` exit 0, 140 passed.
      doc-health `--single-repo` over the same tree: 4 critical, 6 error,
      68 warning, 4 info — identical to the pre-fix-lap baseline and to §3.8's
      pre-change measurement, and `ratified-provenance` still reads "No
      findings". The one-total enforcement added in 6.2 moves nothing,
      exactly as the zero-duplicate census predicted.
