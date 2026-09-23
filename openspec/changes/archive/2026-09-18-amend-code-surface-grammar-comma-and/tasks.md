# Tasks: amend-code-surface-grammar-comma-and

Status: ratified
Ratified by: amend-code-surface-grammar-comma-and — 2026-09-18, Brett Heap, "Amend the text to admit ', and '" (record `review/ratification-2026-09-18.md`)
Kind: tasks

`code_surface: none`, `target_release: implemented`. There is no realization
group, because there is nothing to realize: the delta is requirement prose, the
behaviour it describes has been the module's real behaviour since
`scripts/code_surface.py` was written, and under `release-realization` an empty
code surface archives ON LANDING plus this task list rather than on
merged-plus-green realization evidence. **The "realization" of a wording
amendment IS its promotion at archive.**

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in this
pull request or a measurement recorded verbatim in its body. **§ 1
(ratification) IS TICKED AND NAMES THE WORD THAT TICKED IT** — Brett Heap's
*"Amend the text to admit ', and '"* of 2026-09-18, which is his act and not the
authoring lane's. **§ 4 (archive) STAYS ENTIRELY OPEN**: promotion is a separate
act on a separate word, so openxFactory #1092 closes at the archive and not at
this landing. § 5 records what was measured and deliberately not taken, and stays
open where the work is owed.

**ONE CLAUSE OF THE PARAGRAPH ABOVE IS SUPERSEDED BY THE ARCHIVE ACT OF
2026-09-18, AND IT IS NAMED AND QUOTED IN PLACE RATHER THAN DELETED.** The
clause is ***"§ 4 (archive) STAYS ENTIRELY OPEN"***. It was true of the LANDING
of PR [#1108](https://github.com/opensoft/openxFactory/pull/1108) → `60d281a8`,
which is what it was written about, and it is no longer true of this file: § 4
is PERFORMED by the archive pull request § 4.1 itself names, and § 4.1, § 4.2
and § 5.2 tick there. **EVERY OTHER CLAUSE STANDS.** Nothing was ticked at that
landing that did not land; § 1 named the word that ticked it; and openxFactory
#1092 closes at the ARCHIVE and not at that landing, which is exactly what the
archive pull request's `Closes #1092` performs. **§ 5.1 IS NOT TICKED AND THE
WORK IS NOT DONE** — it carries the house's reserved DEFERRED marker `- [~]`
with what is owed written into the box. **AND THE ARCHIVE PULL REQUEST CARRIES
NO WORD OF ITS OWN**: it was prepared as a DRAFT and HELD, Brett Heap's separate
archive word had not been given when these boxes moved, and it lands on that
word and on no other act.

## 1. Ratification — GIVEN 2026-09-18

- [x] 1.1 **RATIFIED 2026-09-18 by Brett Heap** (openxFactory operator
      authority), verbatim *"Amend the text to admit ', and '"*, given in
      session at approximately **09:55Z** as a TERMINAL MULTIPLE-CHOICE answer
      directly to lane `openXfactory-5` over the two shapes openxFactory
      [#1092](https://github.com/opensoft/openxFactory/issues/1092) put, and
      recorded by that lane as a `RULED` line at **2026-09-18T10:15:10Z** in
      the LANE REGISTER, which is a SEPARATE REPOSITORY and not a path in this
      one — [`opensoft/brett-wip@055bea8b:lanes/log/openXfactory-5.md`](https://github.com/opensoft/brett-wip/blob/055bea8b215ad8b46d83cbf1e366c93c23b08897/lanes/log/openXfactory-5.md#L107), line 107. **THE WORD REACHED
      THE PACKET'S CONTENT BEFORE THE PACKET EXISTED**, so this packet has no
      drafting phase: `proposal.md`, `design.md`, this file AND
      `review/ratification-2026-09-18.md` carry `Status: ratified` from their
      first commit with **ONE** citation line each (`Ratified:` in
      `proposal.md` and in the ratification record, `Ratified by:` here and in
      `design.md`), which is what `ratified-provenance` counts.
      `.openspec.yaml` carries `proposed_by`/`proposed_on` and
      `approved_by`/`approved_on` written in ONE act beside a `kind` and `id`
      that never move. Record: `review/ratification-2026-09-18.md`.
- [x] 1.2 **THE RULED OPTION IS (a), THE TEXT — AND (b), THE CODE, IS WRITTEN
      OUT AS WHAT WAS DECLINED.** Issue #1092 put exactly two shapes and
      `design.md` **D1** carries both with their costs. The word takes the
      amendment, so **THE READER STAYS AS REALIZED**: no commit of this packet
      edits `scripts/code_surface.py`, `_SEPARATOR_RE` keeps all four
      alternatives in their existing order, and
      `test_every_ratified_list_separator_is_admitted` keeps its five
      parameters. The narrowing would have refused declarations the corpus
      already writes, redded that test, and put a realization gate in front of
      this packet's archive.
- [x] 1.3 **`design.md` D2 THROUGH D6 ARE CARRIED BESIDE THE RULED WORD AND ARE
      DECLARED VETO POINTS.** D2 (the exclusivity clause's antecedent stated as
      THOSE TWO HEAD FORMS) and D3 (the separators stated to be alternatives
      within one list, which a head may mix) are the two that reach text the
      ruled word does not name in so many words; both are MEASURED against the
      module rather than designed, both are separable, and the cost of vetoing
      either is written into D2 and D3 themselves — four words and one sentence
      respectively. D4 (the `parse_head` docstring left alone as residue), D5
      (the added scenario's placement) and D6 (byte-faithfulness by
      construction) carry no normative weight.

## 2. The delta — DONE IN THIS PULL REQUEST

- [x] 2.1 **ONE `## MODIFIED` REQUIREMENT, WRITTEN OVER CANON**, byte-faithful
      by CONSTRUCTION rather than by transcription (`design.md` D6): the block
      was generated by slicing `openspec/specs/release-realization/spec.md`
      lines 1014–1132 at `3e32d987` and applying each replacement as an exact
      single-occurrence substitution, so every unit not named in the marker is
      canon's own bytes.
- [x] 2.2 **THREE UNITS RETIRED AND REPLACED IN PLACE**: the opening SHALL
      sentence; the sentence that refused a head continued by `, and …` flatly;
      and the `WHEN` bullet of *An active proposal declares several
      repositories*. Each is REPLACED, none is dropped without replacement.
- [x] 2.3 **THE OPENING SENTENCE NAMES FOUR SEPARATORS** — a comma, `, and `,
      ` and `, ` + ` — and its exclusivity clause is said of **THOSE TWO HEAD
      FORMS** (`design.md` D2), which is the antecedent the originating packet's
      own `design.md:631-637` names and the only exclusivity `parse_head`
      enforces.
- [x] 2.4 **TWO BODY PARAGRAPHS ARE ADDED**: one states that `, and ` is ONE
      separator read AHEAD of the bare comma and that the four are alternatives
      WITHIN one list a head may mix (`design.md` D3); the other states the
      narrow residue the fourth separator leaves behind — admitted where the
      words after it are themselves an identifier followed by a gloss opener or
      the end, refused where they are an ordinary sentence.
- [x] 2.5 **ONE SCENARIO IS ADDED**, *A declaration spells its list out with an
      Oxford comma*, placed beside *An active proposal declares several
      repositories* rather than at the end of the block (`design.md` D5), and
      stating the three-identifier reading, the CONJUNCTION-AS-MEMBER misreading
      it forbids together with the refusal that misreading runs into, and the
      mixed-separator case.
- [x] 2.6 **ONE `Removed from canon` MARKER, THREE NAMES, NO CODE SPAN IN ITS
      REASON**, so that under the grammar `doc-health`'s modified-block-currency
      family enforces it names exactly three units and reports on none of the
      grounds. **PARSED WITH THAT MODULE'S OWN READER AFTER AUTHORING** —
      `parse_marker` returns `form: removed`, change
      `amend-code-surface-grammar-comma-and`, date `2026-09-18`, **3 names** —
      and the third name is CommonMark-padded because it ends on the code span
      `` ` + ` `` (`design.md` D6).
- [x] 2.7 **THE `AMENDED BY` NOTE STATES THE WHOLE ACCOUNTING** — what moves,
      what does not, that no behaviour changes and no module is touched, and why
      the two clarifications ride the correction.
- [x] 2.8 **README `## OpenSpec Records` CARRIES THE ACTIVE ROW**, in house
      style, naming the ruled word and the two declared veto points.
- [x] 2.9 **THE PER-CHANGE SWEEP LEDGER ROWS ARE SEEDED BY THE SANCTIONED
      TOOL**, never hand-written: `python3 scripts/validate-sequenced-after.py .
      --seed-ledger --moved-by '#1108'`, which wrote TWO rows and reported both
      — this change's own (`active`, `co-modifier`, `declares: []`) and
      `gate-code-surface-declarations`'s `class: sole` -> `co-modifier`, the
      partner flip this delta causes by writing the requirement key that
      archived change ADDED.
- [x] 2.10 **THE MOVEMENT LOG ENTRY THE PARTNER FLIP OWES IS APPENDED**, dated
      2026-09-18, inside `tests/sequenced_after/test_sweep.py`'s
      `test_the_LIVE_corpus_and_the_LEDGER_agree_row_by_row` docstring. That
      file's own rule (restated 2026-09-03) owes an entry for *"a PARTNER'S row
      moving because of someone else's delta, where the reason is not legible
      from the two rows alone"*, and the precedent is exact: `#921`'s identical
      flip was caught by a Copilot review and taken at `99cff89b`. The entry
      names the shared requirement key, the two-party measurement, and the
      arithmetic taken on BOTH trees with `--sweep` rather than adjusted by hand
      (`co_modified` 163 -> 165, `sole_modifiers` 56 -> 55, `change_ids`
      219 -> 220, `active` 48 -> 49, `active_co_modified` 29 -> 30,
      `active_sole` HOLDING at 19, `declaring` 41 -> 42, root claims 17 -> 18,
      prose headers and the 4-hop deepest chain both holding). It is a docstring
      addition: it asserts nothing and changes no test's outcome.

## 3. Verification — DONE IN THIS PULL REQUEST

- [x] 3.1 `OPENSPEC_TELEMETRY=0 openspec validate
      amend-code-surface-grammar-comma-and --strict` — PASSES.
- [x] 3.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — the failure
      set is byte-identical to `main`'s: this change appears in NEITHER, and no
      pre-existing failure is added, removed or changed by it.
- [x] 3.3 `python3 scripts/proposal-support.py . verify
      amend-code-surface-grammar-comma-and` — PASSES.
- [x] 3.4 `python3 scripts/validate-code-surface.py .` — PASSES, and the report
      is IDENTICAL to `main`'s: this packet's own declaration is a conforming
      `none` head with a gloss, no register entry moves, and `CLOSED_REGISTER`
      is untouched.
- [x] 3.5 `python3 scripts/validate-sequenced-after.py .` and `--ledger-diff` —
      both PASS, the ledger clean after the seed.
- [x] 3.6 `python3 scripts/doc-health.py --single-repo .` — **NO finding names
      this change**, and the modified-block-currency family reports NOTHING on
      this block: it carries canon and declares its three removals.
- [x] 3.7 `python3 -m pytest tests/sequenced_after -q` — **3 failed, 283
      passed**, and a control run at `origin/main` `3e32d987` reads **the same
      three, and the same 283**. **THE INHERITED RED IS NAMED RATHER THAN
      DISPOSITIONED**: all three are the one finding
      `archive-date-vs-commit: 2026-09-16-add-composed-view-authoring`
      (`test_archive_commit_dates.py::test_THE_LIVE_RECORD_DISPOSITIONS_ONLY_REAL_DISAGREEMENTS_and_NAMES_FACTS`,
      `::test_THE_LIVE_PLAIN_RUN_IS_GREEN_WITH_ZERO_UNDISPOSITIONED` and
      `test_validate.py::test_corpus_sequenced_after_all_validate`), left by
      another lane's squash landing. This packet inherits exactly those three
      and causes none of them; **no row is added to
      `tests/sequenced_after/archive-date-dispositions.yaml` and that file is
      not touched by this branch.**
- [x] 3.8 `python3 -m pytest tests/code_surface tests/doc-health -q` — **1987
      passed, 1 skipped**; the code-surface bench is GREEN in full, and the
      `tests/doc-health` failures are `main`'s: a control run of the five
      failing files at `3e32d987` reproduces seven of them byte for byte
      (`test_ideation_readiness.py` ×3, `test_readiness_dispatch.py`,
      `test_sentinel_vocabulary.py` ×2, `test_status_reader_real_lines.py`).
      **THE EIGHTH IS AN ARTIFACT OF THE CHECKOUT'S PATH AND IS PROVED TO BE
      ONE**: `test_tag_hygiene_pinned_targets.py::
      test_a_lexically_malformed_value_builds_no_path_and_reads_nothing`
      asserts that no resolved path contains the substring `one`, and the
      authoring clone is named `clone-1092` — `cl`**`one`**`-1092`. THE SAME
      COMMIT passes that file 31/31 in a worktree whose path lacks the
      substring, and `main` fails it in the same clone. Nothing in this packet
      is implicated and nothing is fixed here: it is a latent test-harness
      defect belonging to that file, not to this delta.
- [x] 3.9 **COPILOT ROUND 1 WAS TAKEN, THE FINDING WAS VERIFIED TRUE, AND THE
      TEXT WAS REWORDED RATHER THAN DEFENDED.** The review thread on
      `specs/release-realization/spec.md:54` held that the added paragraph's
      "two readings" framing does not match `parse_head`: the comma-first path
      yields no valid TWO-identifier reading. **MEASURED** on a scratch copy of
      the module OUTSIDE the repository, `, and ` removed from `_SEPARATOR_RE`
      and the other three alternatives left in their order —
      `openxFactory, openXwallet, and codexFactory` is then REFUSED with *"its
      head runs into prose at `codexFactory`"*, the conjunction having been
      taken as a member in its own right (`and` satisfies `_NAME`); and where a
      gloss opener follows the conjunction instead, the misreading stands
      SILENTLY with `and` in the derived set. `design.md` § 0 carries the
      counterfactual table. The added paragraph, the added scenario's second
      `AND` bullet, the block's preamble, `.openspec.yaml`'s `reason`,
      `proposal.md`, this file, the README row and the pull request body are
      reworded to the measured behaviour. **NO TRACKED FILE UNDER `scripts/`
      WAS EDITED** — `git status` over `scripts/` is empty at this head, the
      scratch copy lived outside the repository, and THE READER STAYS AS
      REALIZED.

## 4. Archive — OWED, NOT GIVEN

- [x] 4.1 **PROMOTE THE BLOCK AND ARCHIVE THE PACKET**, on Brett Heap's separate
      word and through `scripts/proposal-support.py . archive
      amend-code-surface-grammar-comma-and --date <UTC day>` rather than a bare
      `openspec archive`. Under `release-realization` an empty code surface
      archives on landing plus this task list; that archive is NOT performed at
      this landing, and nothing under `openspec/specs/` is edited by it.

      **PERFORMED IN THIS ARCHIVE PULL REQUEST, 2026-09-18**, through the
      sanctioned wrapper and never a bare `openspec archive`:
      `python3 scripts/proposal-support.py . archive
      amend-code-surface-grammar-comma-and --yes`. **`--date` WAS NOT PASSED**,
      deliberately: the wrapper's default IS today in UTC and its `--help`
      REFUSES any other day, so `2026-09-18` is the directory's date because it
      is the UTC day the wrapper ran and the UTC day its commit carries, and not
      because a flag asserted one. The ORIGIN RETENTION gate passed against the
      ratifying commit `60d281a8` — the squash landing of PR
      [#1108](https://github.com/opensoft/openxFactory/pull/1108), and the ONLY
      commit that has ever touched this packet's `.openspec.yaml` — and the CLI
      was resolved through `contracts/openspec-cli-pin.yaml`
      (`@fission-ai/openspec@1.12.0`, content-addressed artifact, integrity
      verified) rather than from `PATH`, which carries 1.13.1 in this checkout
      and would have been refused.

      **THREE THINGS MOVED AND THEY ARE THE WHOLE OF THE ACT.** (1) The packet
      directory, to
      `openspec/changes/archive/2026-09-18-amend-code-surface-grammar-comma-and/`.
      **FIVE OF ITS SIX FILES ARE PURE RENAMES AT `R100`, 0 CHANGED LINES
      EACH** — `.openspec.yaml`, `design.md`, `proposal.md`,
      `specs/release-realization/spec.md` and
      `review/ratification-2026-09-18.md`. **THE SIXTH IS THIS FILE, AND IT IS
      NOT A RENAME**, which is said here rather than left to a reader of a
      `--numstat`: `tasks.md` carries the § 4 and § 5 accounting, written in the
      commit BEFORE the move (the wrapper refuses an open box) and corrected at
      § 4.2 in a commit after it. No RATIFIED text in it is edited in either
      commit: every tick APPENDS beneath the text it records, and the one
      superseded preamble clause is quoted in place rather than deleted. (2) The `## MODIFIED` block, PROMOTED onto
      `openspec/specs/release-realization/spec.md`, where *Code-surface
      declaration grammar is gated* now names FOUR separators — a comma,
      `, and `, ` and `, ` + ` — with the exclusivity clause said of THOSE TWO
      HEAD FORMS, two body paragraphs added, the flat `, and …` refusal narrowed
      to what the reader does, the WHEN bullet of *An active proposal declares
      several repositories* naming the four, and the scenario *A declaration
      spells its list out with an Oxford comma* added beside it. (3) The README
      **OpenSpec Records** entry, from *Active changes* to the archived ledger.
      The per-change sweep-ledger row follows in its own commit, seeded by the
      sanctioned tool and by no hand. The wrapper's verbatim transcript, the
      promoted requirement's byte-identity against the archived delta and every
      validator's exit code are recorded in this pull request's BODY, which is
      where this file's own preamble says a measurement goes. **NOT ONE
      CHARACTER OF `scripts/code_surface.py` MOVES WITH IT**, which is the ruled
      shape and is checked rather than asserted: `git diff origin/main..HEAD`
      names no path under `scripts/` but the ledger's own.

      **AND THE ACT IS PREPARED, NOT AUTHORIZED.** Brett Heap's separate archive
      word had NOT been given when this box moved, so the tick records the DIFF
      and never a word. The pull request is a DRAFT held for that word; it lands
      by MERGE COMMIT (`gh pr merge --merge`) and NEVER by squash, because a
      squash re-dates the archive directory's adding commit and reds
      `archive-date-vs-commit` on `main`; and whoever lands it cites the word
      there.
- [x] 4.2 **CLOSE openxFactory #1092 AT THE ARCHIVE**, not at this landing. The
      pull request body carries `Refs`, never a closing keyword, for exactly
      that reason.

      **THE CLOSING KEYWORD IS PLACED, AND THAT IS THE WHOLE OF WHAT A TICK CAN
      RECORD.** `Closes #1092` is written in the BODY of this archive pull
      request, which is the instrument this box names. **AND IT APPEARS ONCE
      MORE, WHICH IS DISCLOSED HERE RATHER THAN LEFT TO BE FOUND**: the phrase
      is quoted inside the MESSAGE of this branch's first commit, `e37ab6bd`,
      where that commit describes the instrument it is ticking. A grep over
      `origin/main..HEAD` for a closing keyword beside an issue number — run
      rather than assumed — returns EXACTLY that one occurrence and no other,
      and no issue number but 1092 carries a keyword anywhere on this branch.
      GitHub reads a closing keyword in a commit message that reaches the
      default branch, so the two occurrences name the SAME act — the merge of
      this pull request — and neither can shut #1092 before it: no earlier act
      and no second effect. A first commit reworded to carry the sentence
      without the keyword was prepared and REFUSED by this repository's
      ruleset, verbatim *"Cannot force-push to this branch"*, so the correction
      is made in a commit on top, which is the house remedy for a message
      already pushed. So openxFactory #1092 shuts BY THE MERGE of this pull
      request — the landing lane's act on Brett Heap's
      archive word — and the tick records that the instrument is IN PLACE, never
      that the issue is shut. That is the shape PR
      [#899](https://github.com/opensoft/openxFactory/pull/899) took at its own
      § 5.2 and PR [#1076](https://github.com/opensoft/openxFactory/pull/1076)
      at its § 5.2. The ratified sentence above is about PR #1108's body, which
      carried `Refs #1092` and no closing keyword for exactly the reason it
      states.

## 5. Measured, and deliberately NOT taken here

- [~] 5.1 **`scripts/code_surface.py`'S `parse_head` DOCSTRING CARRIES THE SAME
      THREE-SEPARATOR SENTENCE AND IS NOT EDITED** (`design.md` D4). At
      `:447-448` it reads *"as `none`, or as repository identifiers separated by
      a comma, by ` and ` or by ` + `"*, twelve lines below a regular expression
      with four alternatives. Correcting it would give this packet a CODE
      SURFACE and move its archive behind merged-plus-green realization
      evidence for a comment, which is not what the ruling commissioned. **THE
      BOX TICKS ON THE RECORDING** (ruling of 2026-09-06T23:10Z, verbatim *"Tick
      on the recording"*): at the archive act it ticks by NAMING a filed
      successor issue, or by Brett Heap's word that a docstring needs no
      correction. It is NOT ticked here and the work is not done.

      **DEFERRED AT THE ARCHIVE ACT OF 2026-09-18 — OPEN, OWED, AND STILL NOT
      DONE.** The box takes the house's reserved DEFERRED marker `- [~]` rather
      than a tick. That form has been used at an archive act before
      (`openspec/changes/archive/2026-09-10-accept-sequenced-after-header-line/tasks.md`
      § 4.4, *"DEFERRED … AT THE ARCHIVE — OPEN, OWNED ELSEWHERE"*; and
      `…/2026-09-10-adopt-codexfactory-repository-identity/tasks.md` §§ 5.7,
      8.4, 9.1, 9.2), and the archive wrapper admits it because it refuses only
      a literal `- [ ]` (`scripts/proposal-support.py:4632-4633`), which is a
      fact about the gate and NOT a reason for the marker: the reason is that
      the work is not done.

      **THE RESIDUE IS RE-MEASURED AT THIS HEAD AND READS THE SAME.** At
      `c22c4fc3` the sentence sits at `scripts/code_surface.py:447-449`, its
      *"separated by a comma, by ` and ` or by ` + `"* on `:448`; and the
      module's own comment over `_SEPARATOR_RE` (`:148-151`) calls them
      *"EXACTLY THE THREE THE GRAMMAR ADMITS … plus the `, and ` the corpus
      writes when it spells a list out"*, which is the same divergence in a
      second place and is named here rather than left to be found. Both are the
      `design.md` D4 residue this packet declined to sweep; editing either would
      give the packet a CODE SURFACE and move its archive behind
      merged-plus-green realization evidence for a comment.

      **NO SUCCESSOR ISSUE IS FILED BY THIS ARCHIVE PULL REQUEST, AND NONE
      EXISTS TO NAME.** openxFactory was searched on 2026-09-18 for
      *"parse_head docstring"* and *"code_surface docstring separators"* (both
      return nothing) and over every open and closed issue carrying
      `code_surface` in its title: #1092 (this packet's own), #1074, #1087 and
      the closed #1013 and #1090 — none of them this docstring. The box
      therefore still ticks in one of the two ways its ratified text names, a
      successor issue FILED and named, or Brett Heap's word that a docstring
      needs no correction, and this draft takes NEITHER: it is prepared and
      HELD, and a successor filed for an act that has not landed would name an
      archive that did not happen. **Holder: this lane, at the un-draft, or
      Brett Heap by that word.**
- [x] 5.2 **NO OTHER PLACE IN THE CORPUS RESTATES THE THREE SEPARATORS, AND THE
      SEARCH IS RECORDED RATHER THAN ASSUMED.** Measured 2026-09-18 at
      `3e32d987`: `grep -rn "separated by a comma" scripts tests` returns one
      line (§ 5.1's), and `grep -rn "EXCLUSIVE alternatives\|the two being"
      scripts tests` returns none. The archived
      `gate-code-surface-declarations` delta carries the promoted wording and is
      NOT edited in either direction — an archived delta is a record of what was
      ratified. **THE BOX TICKS AT THE ARCHIVE ACT, ON THE RECORDING**, by
      re-taking the measurement at the head the archive lands on; nothing is
      owed by this packet if it still reads the same.

      **RE-TAKEN AT THE HEAD THIS ARCHIVE LANDS ON — `c22c4fc3`, the
      `origin/main` this branch is cut from and the tree the wrapper ran in —
      AND IT READS THE SAME.** `grep -rn "separated by a comma" scripts tests`
      returns exactly ONE line, `scripts/code_surface.py:448`, which is § 5.1's
      own and is deferred there; `grep -rnE "EXCLUSIVE alternatives|the two
      being" scripts tests` returns NONE and exits **1**, grep's
      no-lines-selected status, which is the proof of the zero rather than a
      claim about it. The archived `gate-code-surface-declarations` delta at
      `openspec/changes/archive/2026-09-16-gate-code-surface-declarations/specs/release-realization/spec.md`
      carries the promoted three-separator wording and is NOT edited by this
      pull request in either direction — `git diff --stat origin/main..HEAD`
      names no path under it — because an archived delta is a record of what was
      ratified. **NOTHING IS OWED BY THIS PACKET.**
