# Tasks: fix-pin-value-boundary-and-sentinel-split

Every measurement quoted below was taken 2026-08-28 in a fresh worktree off
`origin/main` at `6612d3239cbc99b73eb32cf76a861929aa901276`. A task that cites a
number owes a re-measurement at realization, not a copy of the number.

## 1. Admission

- [x] 1.1 Land the packet as an ACTIVE change with `Status: ratified`
      (the admission spelling: an approval act exists and is cited, per
      `sanction-ratified-record-spelling`), its
      `.openspec.yaml` recording the 2026-08-28 ad-hoc origin — Brett's verbatim
      selection "lets do all 3 in order" of the orchestrating session's
      recommended "the measured-latents bundle" — with the two voices kept
      apart, and the sibling `fix-content-resolution-conflation` named in
      `related:`.
      **DONE — LANDED 2026-08-28 in pull request #463, merge commit
      `5314fac5`, verified an ancestor of `origin/main`.** The
      `.openspec.yaml` records the ad-hoc origin with the two voices kept
      apart and names `fix-content-resolution-conflation` in `related:`.
- [x] 1.2 README "OpenSpec Records" active entry, stating the two defects, the
      one ADDED requirement, the two-packet split and the parsed bundle
      measurement that justifies it.
      **DONE — landed with the packet; the active entry stands at
      `README.md:394` and is unchanged by this realization.**
- [x] 1.3 `OPENSPEC_TELEMETRY=0 openspec validate fix-pin-value-boundary-and-sentinel-split --strict`
      and `--all --strict` green. Baseline before the packet: **76 passed, 0
      failed**.
      **DONE — re-run at realization on the merged tree: the single
      change validates (`Change '…' is valid`, exit 0) and `--all --strict`
      reports 78 passed, 0 failed (78 items), exit 0. The count moved from
      76 to 78 because `main` landed two further changes between filing and
      realization, not because anything here changed.**
- [x] 1.4 § Orchestrator decisions OD-1 … OD-5 and § Open Questions Q1 … Q4 are
      open at filing and stay open until an act closes them. **OD-1 is the one
      that changes what was approved** and is the first thing to put to Brett;
      overruling it is a directory move plus one `.openspec.yaml` edit and is
      cheapest before either packet is reviewed.
      **DONE — RULED 2026-08-28, ALL NINE, AND NOT ONE OF THEM MOVED DELTA
      TEXT.** A four-question multi-choice put to Brett by the orchestrating
      session over pull request #463 and relayed the same day: all five
      orchestrator decisions CLEARED AS AUTHORED, **including OD-1's
      re-sequencing of the approved 1, 2, 3 into {1, 3} then {2}, accepted on
      the record**, and all four questions RULED on the packet's own
      recommendation — Q1 rides the existing undeclared-non-commit defect, Q2
      writes `unreadable-repository` for a failed `git log`, Q3 imports the
      declared constant across the package boundary, Q4 asserts the boundary
      rule by a test over the declaration. `specs/doc-health/spec.md` is
      byte-unchanged from the filing, which is checked rather than assumed.
      The mechanism, the date, the approver and the selections are recorded;
      no verbatim wording of the ruling reached this session, so none is
      quoted. Full record at `proposal.md` § Orchestrator decisions and
      § Open Questions.
      **WHAT THE SAME ACT ALSO SETTLED, and neither part is this session's to
      perform:** merge on green is APPROVED and is the ORCHESTRATING SESSION'S
      act; and both realizations are PRE-COMMISSIONED TO DISPATCH IN ORDER once
      the filing lands — THIS PACKET FIRST, realized and archived on its own
      green, then `fix-content-resolution-conflation`. The conditional branches
      § 3.4 carried ("if Brett rules against the cross-package import") and
      § 2.3's alternative are settled and do not fire.

## 2. Implementation — defect 1, the trailing hexadecimal boundary

- [x] 2.1 Re-measure the defect on the realization branch before touching it,
      over all FOUR site-building expressions rather than the two the inherited
      record names: `_field_re` (`pin_class.py:204`), `_VOCAB_RE` (`:980`), the
      prose member pattern at `:347`, the prose member pattern at `:406`. Assert
      the fabricated forty-character prefix in each, and assert `LOOSE_SHA_RE`
      returns nothing on the same line. If any of the four has been fixed by
      another session in the meantime, say so and narrow the task rather than
      re-applying it.
      **DONE — ALL FOUR STILL DEFECTIVE AT REALIZATION; none had been
      fixed by another session, so none of this task narrowed.** Measured
      on `source_revision: <64-hex>` (and each prose member's own line):
      `_field_re`, `_VOCAB_RE` and BOTH prose `line_re()` patterns each
      matched and each returned the fabricated forty-character prefix —
      4/4. `LOOSE_SHA_RE` returned `[]` on the identical line, which is the
      guard the module already carried and had not carried across.
      End-to-end through `_sites_in`, all three affected members built a
      forty-character `PinSite` from a sixty-four-character value.
- [x] 2.2 Append `(?![0-9a-fA-F])` to the value group of all four. The
      construction is copied from `LOOSE_SHA_RE` rather than invented, so the
      module states the rule once. Do NOT add a leading `(?<![0-9a-fA-F])`: the
      group is already anchored by `\s*"?` and the guard would be inert
      (`design.md` § 3).
      **DONE, AND THE RULE IS NAMED RATHER THAN RETYPED FOUR TIMES.** The
      construction is declared once as `pin_class.HEX_BOUNDARY` and
      referenced by all four expressions; `LOOSE_SHA_RE`, whose comment
      stated the rule before any site builder carried it, is rebuilt from
      the same constant so the module cannot drift against itself. No
      leading guard was added, per the ruling. Re-measured after: 0/4
      expressions match a sixty-four-character value, and each also refuses
      a forty-one-character run — the rule is on the VALUE, not on a list
      of lengths.
- [x] 2.3 Prove the conforming path did not move. The six shapes measured at
      filing — bare, quoted, JSON, sequence item, comment-trailed, and each
      prose form — must still build the same site. This is the task that catches
      an over-tight boundary, which is the fix's real failure mode.
      **DONE — ALL SIX SHAPES STILL BUILD THE SAME SITE, at the regex
      level and end-to-end.** bare, quoted, JSON, sequence item and
      comment-trailed all still yield the identical forty-character value
      from both `_field_re` and `_VOCAB_RE`; both prose members still lift
      their pin from the sentence they declare a pattern for. A conforming
      readiness record still verifies `PASS`, `clean` and `fully_verified`.
      Pinned by `test_a_whole_object_name_is_unaffected_in_every_serialization`.
- [x] 2.4 Prove the refused value still reaches the classification whole. A
      sixty-four-character value under a declared pin key must produce a
      DEFECT naming the full value, and NO pin site — the two halves asserted
      separately, because a test that only checks the absence of the pin would
      pass on a value silently dropped.
      **DONE — BOTH HALVES ASSERTED SEPARATELY, and the fixture is the
      COLLIDING case rather than the harmless one.** A readiness record was
      built carrying a sixty-four-character value whose first forty
      characters name a REAL commit the fixture's `main` reaches. PRE-FIX,
      run against the module as committed: one result, verdict `pass` — the
      verification certified a provenance claim the artifact never made.
      POST-FIX: `report.results == ()`, `swept_sites == []`, no orphan and
      no lost row; and exactly one undeclared-value defect carrying the
      value AS WRITTEN, all sixty-four characters, naming the artifact and
      the key. Q1's ruling holds in the measurement: no new finding class,
      `uncovered` and `uncovered_non_pins` both zero. The rendered report
      names the whole value and never names the prefix on its own.
- [x] 2.5 The declared class's own report must not move. Baseline at filing:
      **66 declared pin sites across 23 class members — 50 reachable, 0
      orphaned, 1 lost (declared unrecoverable, 0 awaiting a superseding
      record), 0 inconclusive; 0 uncovered, 0 vanished, 0 future members now
      carrying pins; 7 legal non-pins, 0 undeclared non-commit values, 3
      recognized legacy absences, 0 unused vocabulary members**, `clean` true.
      Every one of those numbers is expected IDENTICAL after the fix, because
      the corpus carries nothing the fix reclassifies — re-measured at filing:
      **1116 swept files, 0 values of 41 or more hexadecimal characters under
      any vocabulary key**. A number that moves is a finding, not a rounding.
      **DONE — EVERY NUMBER IDENTICAL, and the comparison was made on ONE
      TREE rather than across the merge.** `main` moved thirteen commits
      during this realization, so a naive before/after would have shown a
      difference `main` caused (`contracts/openxwallet-pin.yaml:44` carries
      a different cross-repository pin than it did at filing). The honest
      measurement runs the PRE-EDIT module and the POST-EDIT module against
      the SAME merged tree (`c79d6e54`): summary string identical, all 66
      site rows identical, all 7 non-pin rows identical, `clean` and
      `fully_verified` both True on both, and NOT ONE of the fifteen counts
      moved. The report reads **66 declared pin sites across 23 class
      members — 50 reachable, 0 orphaned, 1 lost (0 awaiting a superseding
      record), 0 inconclusive; 0 uncovered, 0 vanished, 0 arrived; 7 legal
      non-pins, 0 undeclared non-commit values, 3 recognized legacy
      absences, 0 unused vocabulary members**. Corpus re-measured: 1119
      scan-suffix files in the scan roots (1116 at filing — `main` added
      three), 182 actually read after non-member exclusion, and **0 values
      of 41 or more hexadecimal characters under any vocabulary key**. That
      last zero is why nothing moved, and it is re-asserted by
      `test_the_real_corpus_carries_nothing_the_boundary_reclassifies` so
      the day one arrives it is a finding rather than a silent change.

## 3. Implementation — defect 3, the `"unknown"` split

- [x] 3.1 Re-read all five emission sites before editing and confirm the
      condition each one means. The inherited record (`declare-sentinel-pin-vocabulary`
      § 5.6) names THREE sites; this packet measured FIVE, one of which fires on
      two conditions and one of which is already correct. Re-measure rather than
      trust either count.
      **DONE — THE FIVE ARE CONFIRMED, AND RE-MEASURING FOUND A SIXTH
      CONDITION NEITHER RECORD NAMED.** The five sites are exactly where
      the packet put them: `avatar_f0/cli.py` `:49`, `:51`, `:60`, `:62`
      and `snapshot_registry.py:283`, and `:283` is already correct.
      THE SIXTH: `_git_head` did not only fail empty. On an UNBORN `HEAD`,
      `git rev-parse HEAD` prints the literal string `HEAD` on stdout and
      exits 128 — measured, `rc=128`, `stdout='HEAD\n'` — so the committed
      code returned `"HEAD"` as the repository's revision. That is neither
      a commit name nor a declared sentinel, and it is the same class of
      defect this packet exists to fix, reached by a route § 3.3 assumed
      could not exist. Disposition in § 3.3.
- [x] 3.2 `avatar_f0/cli.py` `_git_file_commit`: add the return-code branch that
      does not exist today. `out.returncode == 0` with empty stdout is
      `dirty-worktree` → `pin_sentinels.UNCOMMITTED_WORKTREE`; a non-zero return
      code is `unreadable-repository` → `pin_sentinels.UNCOMMITTED`. **This
      branch is the prerequisite for the whole split** — without it neither
      member can honestly be written at `:49` (`design.md` § 4).
      **DONE, AND DRIVEN BY CONSTRUCTED CONDITIONS RATHER THAN MOCKED
      MESSAGES.** A real repository with an uncommitted file gives
      `git log` exit 0 with empty stdout and now returns
      `uncommitted-worktree` (condition `dirty-worktree`); a path that is
      not a repository gives a non-zero exit with empty stdout — the probe
      asserts BOTH facts about the fixture before trusting it — and now
      returns `uncommitted` (condition `unreadable-repository`). Without
      the branch those two are the same return, which is the whole reason
      one `"unknown"` covered both.
- [x] 3.3 `avatar_f0/cli.py` `_git_file_commit` `except Exception` (`:51`) and
      `_git_head` (`:60`, `:62`): all three become
      `pin_sentinels.UNCOMMITTED`. `rev-parse HEAD` producing nothing means it
      failed, so `:60` and `:62` are one condition wearing two spellings of the
      same failure.
      **DONE — ALL THREE WRITE `pin_sentinels.UNCOMMITTED`, AND A RETURN-
      CODE BRANCH WAS ADDED TO `_git_head` TOO, WHICH THIS TASK SAID WAS
      UNNECESSARY.** The task's REASON is false as measured (§ 3.1's sixth
      condition: an unborn `HEAD` fails with `HEAD` on stdout, not with
      nothing), while the task's RULED OUTCOME is untouched — every
      `_git_head` return still writes the same single member, and no ruled
      member assignment moved. The vocabulary already assigns the unborn
      case to this member BY NAME (`unreadable-repository`: "`rev-parse
      HEAD` failed, `HEAD` is unborn, or the path is not a repository"), so
      reading the return code legislates nothing new; it stops a third
      failure being spelled as a pin. Recorded here rather than performed
      quietly, because it corrects an inherited premise.
      THE `except` RETURN IS NOW GENUINELY PROVEN, and the first attempt to
      prove it was wrong: `git -C <missing-dir>` does NOT raise, it exits
      128, so a missing-directory fixture exercised the return-code branch
      under the exception test's name. The condition is constructed instead
      by emptying `PATH` so `subprocess.run` raises `FileNotFoundError` for
      real — the state a machine without git is actually in — and the
      non-zero-exit route keeps a test of its own.
- [x] 3.4 `snapshot_registry.py:283`: the MEMBER does not change —
      `unestablished-revision` is the projector's actual condition — and the
      LITERAL does, to the imported constant. See Q3: if Brett rules against the
      cross-package import, leave the literal and record the ruling here rather
      than inventing a third home for the constant.
      **DONE — Q3 WAS RULED FOR THE IMPORT on 2026-08-28, so the
      conditional branch does not fire.** The member is unchanged
      (`unestablished-revision`); only the literal moved, to
      `pin_sentinels.UNKNOWN`. `doc_health` is a sibling package under
      `scripts/` and this module already inserted `scripts/` on `sys.path`,
      so the import cost one line. The docstring now states WHY the weakest
      member is the honest one here. The avatar harness carries the genuine
      cross-package import — `experiments/` reaching `scripts/` — with the
      path insertion stated rather than hidden, on the pattern
      `scripts/proposal-support.py` already records for its own.
- [x] 3.5 Update `pin_sentinels.SENTINELS` `emitters` tuples to follow the
      split, and update the `UNKNOWN` member's note, which currently states that
      its three call sites span three conditions and names the split as a
      follow-up. That note becomes false the moment this task lands; leaving it
      would make the declaration assert something the code contradicts.
      **DONE — TUPLES AND NOTE BOTH.** `uncommitted-worktree` and
      `uncommitted` each gain the avatar site; `unknown` is down to its one
      remaining emitter, `snapshot_registry.index_entry`. The `UNKNOWN`
      note no longer claims three call sites across three conditions — it
      records that the follow-up landed, why the one remaining site
      genuinely cannot say more, and that the instruction it carries is now
      obeyed by every emitter. The module docstring's measurement paragraph
      is KEPT (it is the evidence the member rests on) and a paragraph
      added stating the split as built — five sites, not three, one of them
      firing on two conditions.
- [x] 3.6 `unused_sentinels()` must still report zero. Every member keeps at
      least one declared emitter after the split — assert it, because a split
      that stranded a member would fail the declaration's own
      declaration-against-corpus direction and the failure would look like an
      unrelated regression.
      **DONE — `unused_sentinels()` returns `()` over the real corpus, and
      `declaration_defects()` returns `()` too.** Asserted rather than
      assumed, in `test_the_split_leaves_every_declared_member_with_an_emitter`,
      which also pins the exact emitter tuple the weakest member keeps.
- [x] 3.7 Confirm no committed artifact carries `"unknown"` under a swept key,
      so the split moves no committed bytes. Measured at filing: seven legal
      non-pins, six `uncommitted-worktree` and one `not-applicable-ad-hoc`, and
      not one `"unknown"`.
      **DONE — RE-MEASURED, UNCHANGED, AND NO COMMITTED BYTES MOVED.** The
      seven legal non-pins are the same seven: six `uncommitted-worktree`,
      one `not-applicable-ad-hoc`, zero `unknown`. Pinned by
      `test_the_split_moves_no_committed_bytes`, which fails if a committed
      artifact ever carries the weakest member — at which point a migration
      would be owed and captured material is never edited after capture, so
      the finding is declared instead.

## 4. Verification

- [x] 4.1 `set -o pipefail; python3 -m pytest tests/doc-health -q` — exit code
      READ, never inferred from the tail of the output. Baseline at filing:
      **1249 passed, 0 failed, exit 0** in 163s.
      **DONE — EXIT CODE READ, NOT INFERRED, under `set -o pipefail` with
      the status captured to file rather than eyeballed off a tail.**
      Baseline re-measured on THIS branch before any edit: **1270 passed,
      0 failed, exit 0** in 167.45s (the packet's 1249 had aged — `main`
      moved). After: **1292 passed, 0 failed, exit 0** in 185.53s. The +22
      is +14 test functions from this packet (6 in
      `test_pin_reachability.py`, 8 in `test_sentinel_vocabulary.py`) and
      +8 collected from the three doc-health suites `main` landed in the
      thirteen commits merged in mid-realization. NOTHING WAS SKIPPED and
      nothing regressed.
- [x] 4.2 New regressions live beside the suites that own the surfaces —
      `tests/doc-health/test_pin_reachability.py` for the boundary,
      `tests/doc-health/test_sentinel_vocabulary.py` for the split and the
      emitter tuples.
      **DONE — no new test module; both surfaces stay with the suite that
      owns them.** The boundary work is six tests in
      `test_pin_reachability.py`; the split is eight in
      `test_sentinel_vocabulary.py`, one of which REPLACES the two source
      assertions in the inherited
      `test_unknown_is_not_folded_into_the_unreadable_repository_condition`
      that pinned the pre-split spellings. That test's SUBJECT — the member
      exists because three conditions were measured, not one — is kept and
      restated, because deleting it on the ground that the code moved would
      delete the evidence the member rests on.
- [x] 4.3 Mutation-pin both fixes at SOURCE level, because both are refusals and
      a refusal that stops refusing is invisible in a value assertion. Remove one
      trailing boundary → the truncation proof must fail. Collapse one split site
      back to `"unknown"` → the emitter proof must fail. A proof that still
      passes is unpinned and gets rewritten rather than accepted.
      **DONE — EIGHT MUTATIONS, EVERY ONE CAUGHT, AND ONE OF THEM CAUGHT A
      DISHONEST TEST OF MY OWN.** Each mutation was applied to the working
      tree, the two suites run, and the file restored from a byte copy
      taken beforehand (restoration verified by `diff -q`):

      | # | mutation | caught by |
      | --- | --- | --- |
      | M1 | `_field_re` boundary removed | 3 tests |
      | M2 | `_VOCAB_RE` boundary removed | 2 tests |
      | M3 | prose `cross-reference-rendered` boundary removed | the structural test ALONE |
      | M4 | prose `gate-action-record` boundary removed | the structural test ALONE |
      | M5 | dirty-tree branch collapsed to `"unknown"` | 3 tests |
      | M6 | `_git_file_commit` return-code branch deleted | 2 tests |
      | M7 | `_git_head` collapsed to `"unknown"` | 3 tests |
      | M8 | projector retypes the literal instead of importing it | 1 test |

      M3 AND M4 ARE THE WHOLE ARGUMENT FOR § 4.4: no value assertion caught
      either one. Only the structural test over the declaration did — which
      is the platform-inert-mutation lesson exactly, because a prose
      member's pattern is not exercised by anything in the corpus, so a
      boundary removed there stays invisible to every behavioural test until
      an artifact happens to carry the shape.
      M6 ALSO CAUGHT A TEST THIS SESSION HAD WRITTEN WRONG: the mutation
      reddened the exception test, which it should not have been able to
      reach. Measured, `git -C <missing-dir>` exits 128 rather than raising,
      so that fixture had been exercising the return-code branch under the
      exception test's name. Rewritten to construct the real condition (an
      empty `PATH`, so `subprocess.run` raises `FileNotFoundError`), with
      the non-zero-exit route given a test of its own. Recorded rather than
      quietly fixed, because a mutation run that improves the tests is the
      only evidence they were unpinned.
- [x] 4.4 A structural assertion over the declaration, per Q4's recommendation:
      every site-building expression in `pin_class.py` refuses an over-long
      hexadecimal run. This is what stops a future prose member from declaring an
      unguarded `pattern`, and it pins behaviour rather than the spelling of a
      regex.
      **DONE — AND IT EARNED ITS PLACE: it is the only thing that caught M3
      and M4.** `test_the_boundary_is_carried_by_every_site_building_expression`
      ENUMERATES the builders from the declaration rather than listing them
      by hand — `_VOCAB_RE`, a `_field_re` per declared field key, and every
      prose member's `line_re()` — then COMPILES AND RUNS each against a
      whole object name (must build), a sixty-four-character value (must not
      match) and a forty-one-character run (must not match). A prose member
      added later with an unguarded `pattern` fails on the day it lands. A
      second test asserts the rule has ONE home, `HEX_BOUNDARY`, with no
      executable string literal retyping it — read via `ast` so that a
      comment or docstring EXPLAINING the rule is not mistaken for a copy of
      it, since a substring count would have made writing the reasoning down
      a test failure.
- [x] 4.5 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green.
      **DONE — 78 passed, 0 failed (78 items), exit 0, on the merged tree.**
- [x] 4.6 Re-affirm by PARSE, not `grep`, that no contract bundle is owed: load
      every `contracts/releases/*.digests.yaml`, walk its entries into member
      paths, and assert that none of the four edited files appears in any of
      them. Measured at filing against `contract-v2.0`, the declared bundle: 192
      entries, 22 `scripts/` members, 0 under `scripts/doc_health/`,
      `scripts/ideation_dashboard/` or `experiments/`.
      **DONE — RE-VERIFIED AT REALIZATION, WIDER THAN THE FILING CHECK, AND
      NO BUNDLE IS OWED.** All **40** `contracts/releases/*.digests.yaml`
      were loaded with a YAML parser and every string in every document
      walked — **7396 entries in total** — rather than only the declared
      bundle, because a membership this packet's archive gate depends on
      should not rest on one file being the right one to read. NOT ONE of
      the six edited files appears in ANY bundle. `contract-v2.0`
      re-measured and unchanged from filing: **192 entries, 22 `scripts/`
      members, 0 under `scripts/doc_health/`, 0 under
      `scripts/ideation_dashboard/`, 0 under `experiments/`**. So
      `target_release: none` still holds and § 5.3's argument stands.
- [x] 4.7 Guard the two standing substring traps this repository has been bitten
      by, both of which are source scans rather than behaviour tests: the
      staging-workbench no-write-path scan, which fails on the upper-cased HTTP
      verb for a write appearing anywhere in the files it reads (it once fired
      on the word "posture"), and the session-verbs scan over the wallet CLI,
      which fails on an approver flag spelled as a bare approval switch. Neither
      file is edited by this packet, so the check is a confirmation rather than
      a change — but both have reddened a suite here before on prose alone.
      **DONE — BOTH CONFIRMED CLEAR, and the confirmation is a MEASUREMENT
      rather than an assertion that the files differ.** The workbench scan
      reads `web/views/staging-workbench.js` and the pure model module;
      this packet touches no file under `web/`. The session-verbs scan reads
      `scripts/ideation_dashboard/cli.py` and the pull-request port; this
      packet touches neither — `avatar_f0/cli.py` shares only a basename.
      Belt and braces, THE DIFF ITSELF was scanned: **zero** added lines
      across the six files carry an upper-cased HTTP write verb, and zero
      carry a bare approval switch. (Four such substrings exist in
      pre-existing lines of two edited files; none sits on a line this
      packet moves, and neither file is read by either scan.) Both suites
      pass.

## 5. Archive gate

**NONE OF § 5 IS THIS SESSION'S ACT AND EVERY BOX BELOW IS DELIBERATELY
UNTICKED.** The realization session was commissioned to execute § 2-§ 4,
prove the fixes and OPEN a pull request — explicitly not to merge and not to
archive. The merge is the orchestrating session's act on the same ruling
that pre-commissioned this realization, and every item here is a
measurement that can only be taken AFTER it: § 5.1 reads a merge commit
that does not exist yet, § 5.2 runs on the merged tree, § 5.3 is re-
affirmed at the archive rather than carried from here, and § 5.4 closes
over both. Ticking any of them from a branch would be recording a
measurement nobody took, which is the same falsification the packet's own
subject matter is about. WHAT THIS SESSION CAN SAY: § 5.2's suite and
validator are green on the branch and § 5.3's parse re-affirms no bundle is
owed (§ 4.1, § 4.5, § 4.6) — both owe a re-run on the merged tree, which is
what these boxes are for.

**THE ARCHIVING SESSION TOOK THEM ON 2026-08-29**, and the paragraph above is
kept as authored rather than rewritten, because it is the record of WHY the
realization left them blank. Every measurement below was taken in a fresh
worktree at `origin/main` = `82a28086`, which carries the merge these boxes
name; none is carried forward from the realization's own numbers, and where a
number MOVED since that run the move is stated with its cause rather than
smoothed to match.

- [x] 5.1 Merged to `origin/main` with both required checks green, the merge
      commit re-verified an ancestor of `origin/main` and a real two-parent
      merge read out of `git cat-file -p` rather than off the pull request page.
      **DONE — READ OUT OF GIT RATHER THAN OFF A PAGE.** Pull request #478
      merged 2026-08-28T11:33:42Z as merge commit `8690ec29`, an ancestor of
      `origin/main` by `git merge-base --is-ancestor` (exit 0) and a real
      two-parent merge (`31344941` + `0529fb4a`) by `git cat-file -p`. Green on
      the FINAL head `0529fb4a`, all four checks from the check-runs API:
      `pytest-suite` **selected 7650, passed 7629, skipped 21, 0 failures, 0
      errors** (run 33165708443, counts read out of the job log rather than off
      the conclusion field), plus `wallet-validation`, `merge-master-approval`
      and `copilot-pull-request-reviewer`, every one `success`.
- [x] 5.2 On the merged tree: `pytest tests/doc-health` green under
      `set -o pipefail`, `openspec validate --all --strict` green, and the
      declared pin class reporting `clean` with § 2.5's numbers re-measured.
      **DONE — AND ONE NUMBER MOVED, FOR A CAUSE THAT IS NAMED RATHER THAN
      ROUNDED AWAY.** `set -o pipefail; python3 -m pytest tests/doc-health -q`
      on the untouched tree at `82a28086`: **1333 passed, 0 failed**, exit code
      read from `$?` rather than inferred from a tail, 178.34s.
      `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`: **79 passed, 0
      failed** across 79 items. `python3 scripts/doc_health/pin_class.py --repo .
      --rev HEAD --remote origin` exits **0**, which is `clean` true, and reports
      **67 declared pin sites across 23 class members — 51 reachable, 0 orphaned,
      1 lost (declared unrecoverable, 0 awaiting a superseding record), 0
      inconclusive; 0 uncovered, 0 vanished, 0 arrived; 7 legal non-pins, 0
      undeclared non-commit values, 3 recognized legacy absences, 0 unused
      vocabulary members**. Against § 2.5's **66 sites / 50 reachable**, TWO
      counts moved and thirteen did not, and the move is not this packet's:
      `openspec/changes/add-worker-enrollment-broker/supporting-docs/manifest.yaml:21`
      is a NEW pin site, added by `21bc40ac` in pull request #489 on 2026-08-28,
      pinning `93f883f4` and reachable as an ancestor of `origin/main`. Proven
      rather than asserted — `git ls-tree 8690ec29 <path>` is empty and
      `git ls-tree HEAD <path>` is not, and `git log --diff-filter=A` names
      `21bc40ac`. Every full promotion writes a supporting-docs manifest and a
      manifest is a pin site, so the census reads 67 for a reason canon already
      states. The corpus sweep behind § 2.5's zero was re-run at this act as
      well: **1124 scan-suffix files in the scan roots** (1119 at realization —
      `main` added five), **184 read after non-member exclusion** (182), and
      **0 values of 41 or more hexadecimal characters under any vocabulary
      key**. That last zero is the one that must not move, and it did not.
- [x] 5.3 No contract tag is owed (§ 4.6). This is what lets the packet archive
      without waiting on its sibling, and it is the whole argument of OD-1 — so
      it is re-affirmed at the archive rather than carried from the filing.
      **RE-AFFIRMED AT THE ARCHIVE BY PARSE, AGAINST THE BUNDLE AS IT STANDS
      TODAY RATHER THAN AS IT STOOD AT FILING.** The declared bundle has MOVED
      since this packet was written — `contracts/manifest.yaml:3` now reads
      `contract-v2.1`, cut by the sibling packet's own realization — so the
      re-affirmation is worth more than a carry-forward would have been.
      `contracts/releases/contract-v2.1.digests.yaml` was LOADED and its **192**
      entries walked into their member paths: not one path under
      `scripts/doc_health/`, `scripts/ideation_dashboard/` or `experiments/`
      appears in it, exactly as at filing. No schema moves, no digest set
      changes, no release tag is owed by THIS packet, and doc-health's
      `release-inventory-drift` family reports **no findings** on this tree.
      OD-1's argument therefore holds at the archive: this packet archives on a
      green suite alone, and the sibling's tag is the sibling's.
- [x] 5.4 Every § 6 follow-up carries a disposition rather than a blank box, and
      every OD and Q carries a ruling or an explicit carry-forward.
      **DONE, AND THE BOXES THAT STAY OPEN STAY OPEN ON PURPOSE.** All five § 6
      items carried a realization disposition already; each now carries a second
      line taken AT THE ARCHIVE, re-measured rather than restated. None is
      ticked, because ticking a follow-up the archive did not perform is the
      same falsification § 5's own preamble refuses. On the other half: all five
      § Orchestrator decisions were CLEARED AS AUTHORED and all four § Open
      Questions RULED on 2026-08-28 — recorded in `proposal.md`, which is why
      this packet needed no header move at the archive: it already reads
      `Status: ratified` with a citation clearing the record spelling's
      three-way floor.

## 6. Open — deliberately not closed by this change

- [ ] 6.1 **THE OTHER UNREPAIRED GENERATORS.** `_head_sha()`
      (`ideation_dashboard/nightly_lane.py:117`), `git_head_revision()`
      (`dashboard_refresh_lane.py:643`) and `RealGit.head_sha()`
      (`doc_health/corpus.py:534`) all run `rev-parse HEAD` with no cleanliness
      check. `corpus.py` is the widest-fanout pin source in the repository and a
      check there moves six record families at once. Inherited from
      `declare-sentinel-pin-vocabulary` § 5.1, still open, and not narrowed by
      this packet.
      **DISPOSITION: STILL OPEN, AND NOW NARROWED BY ONE — deliberately not
      three.** This packet repaired the avatar harness's two generators and
      left `_head_sha()`, `git_head_revision()` and `RealGit.head_sha()`
      exactly as it found them, because they are a different lane's output
      and `corpus.py` in particular is the widest-fanout pin source in the
      repository — a change there moves six record families at once and owes
      its own packet with its own corpus measurement. WHAT THIS PACKET ADDS
      TO THE ITEM, and it is worth the next reader's attention: the unborn-
      `HEAD` measurement in § 3.1 applies to ALL THREE of them verbatim.
      Each runs `rev-parse HEAD` and reads only stdout, so each returns the
      literal string `HEAD` on an unborn repository today. That is no longer
      a conjecture about what they might do; it is measured, and the item is
      more urgent than when it was inherited.
      **AT THE ARCHIVE 2026-08-29: CARRIED, NOT DISCHARGED, AND STILL
      THREE.** Re-read on the merged tree at `82a28086`: `_head_sha()`
      (`ideation_dashboard/nightly_lane.py`), `git_head_revision()`
      (`dashboard_refresh_lane.py`) and `RealGit.head_sha()`
      (`doc_health/corpus.py`) are byte-unchanged by the merge and by this
      archive. The archive act performs none of them and must not be read as
      closing them; the owner is whoever next opens the widest-fanout pin
      source, and the archived record is where they will find the
      unborn-`HEAD` measurement that makes the item urgent.
- [ ] 6.2 **WHETHER A COMPOSED PROJECTION SHOULD CARRY A PIN KEY AT ALL.**
      Inherited § 5.3. A schema question about the snapshot index, adjacent to
      this packet's `snapshot_registry.py` edit and deliberately not answered by
      it: this packet changes a literal to a constant and asserts nothing about
      whether the key belongs there.
      **DISPOSITION: STILL OPEN, AND THIS PACKET DELIBERATELY DID NOT
      PREJUDGE IT.** The edit at `snapshot_registry.py:283` changes a
      literal to the declared constant and asserts nothing about whether a
      composed projection should carry a pin key at all. If the answer
      turns out to be that it should not, the line this packet touched is
      deleted rather than re-argued, and nothing here makes that harder.
      **AT THE ARCHIVE 2026-08-29: CARRIED AS A SCHEMA QUESTION,
      UNPREJUDGED AND NOW HARDER TO LOSE.** The promotion this act performs
      adds no requirement about whether a composed projection should carry a
      pin key, so the question is exactly as open in canon as it was in the
      delta. The one thing that changed is where a reader finds it: it is an
      archived record now rather than an active packet, which is why it is
      re-stated here instead of being allowed to lapse with the folder.
- [ ] 6.3 **THE PREFLIGHT HALF OF THE ENFORCEMENT HOME STAYS UNWIRED.**
      Inherited § 5.4. The classification rides inside a verification that is
      pytest-plus-entry-point rather than nightly-gated.
      **DISPOSITION: STILL OPEN, UNCHANGED, AND HONESTLY THE WEAKEST POINT
      IN THIS PACKET'S ENFORCEMENT.** Every proof this realization produced
      rides `pytest tests/doc-health` and the class's own entry point. That
      is real enforcement on every pull request and it is NOT nightly-gated,
      so a corpus that acquires an over-long value between runs is caught at
      the next pull request rather than the next night. No deterministic
      check family was added, per the delta's own statement.
      **AT THE ARCHIVE 2026-08-29: CARRIED, AND THE PROMOTION DOES NOT MOVE
      IT.** The requirement reaching canon by this act says in its own last
      paragraph that it adds no deterministic check family, and the family
      enumeration and its numerals are untouched by the archive — measured
      rather than assumed: doc-health's `family-enumeration` reports no
      findings on this tree. So the enforcement home is unchanged by
      promotion: `pytest tests/doc-health` plus the class's own entry point,
      on every pull request and not nightly. Still the weakest point, still
      open, still owed its own packet.
- [ ] 6.4 **WHETHER A GENERATOR MUST IMPORT A DECLARED SPELLING RATHER THAN
      RETYPE IT.** Q3 recommends doing it here and legislating nothing, on the
      ground that one instance is not evidence for a rule. If a second generator
      retypes a literal, that is the evidence, and this item is where the next
      reader should find that said.
      **DISPOSITION: STILL OPEN, AND THE INSTANCE COUNT IS NOW TWO RATHER
      THAN ONE — which is worth writing down precisely because it is NOT
      yet being treated as a rule.** This packet converted two generators in
      one act: `snapshot_registry.py` (a sibling-package import costing one
      line) and `avatar_f0/cli.py` (a genuine cross-package import from
      `experiments/` into `scripts/`, with the path insertion stated in the
      source rather than hidden). Counting the two pre-existing converts,
      `bootstrap-ideation-cross-reference.py` and `proposal-support.py`,
      FOUR generators now import the declared spelling and NONE retypes it.
      That is a practice with no exception left, which is the condition
      under which legislating it costs nothing — but Q3 ruled to legislate
      nothing here and this session did not. The next reader deciding
      otherwise now has the count.
      **AT THE ARCHIVE 2026-08-29: CARRIED, AND THE COUNT IS RE-READ RATHER
      THAN REPEATED.** Four generators import the declared spelling and none
      retypes it, unchanged on the merged tree. No rule was legislated here
      and none is legislated by the archive — Q3 ruled to leave it, and
      promoting the boundary requirement asserts nothing about import
      discipline. The item stays where the evidence would land.
- [ ] 6.5 **CROSS-REPOSITORY PINS STAY OUT**, on the boundary both sibling
      packets drew. Whether a boundary defect or a sentinel is even meaningful
      for a gitlink, a `pinned_contract_manifest` entry, a release digest or an
      image digest is a question answered against a different remote by a
      different authority. Worth naming HERE rather than only inheriting it,
      because a release digest is a sixty-four-character hexadecimal value and
      is therefore exactly the shape defect 1 is about — it is out of scope
      because of WHOSE question it is, not because of what it looks like.
      **DISPOSITION: STILL OUT, AND THE BOUNDARY HELD UNDER A REAL
      TEMPTATION TO CROSS IT.** The fix refuses a sixty-four-character
      hexadecimal value under a declared pin key, and a release digest is
      exactly that shape — so it would have been easy to extend the class to
      cover digests while the code was open. It was not extended. The
      declared class, its key vocabulary and its non-member exclusions are
      byte-unchanged by this packet; the only thing that moved is what a
      value must LOOK LIKE to build a site inside the class as it already
      stood. Measured consequence: `contract-v2.0`'s 192 entries and the
      other 39 bundles' 7204 remain outside the sweep entirely (§ 4.6), and
      the class still reports 66 sites across 23 members (§ 2.5).
      **AT THE ARCHIVE 2026-08-29: STILL OUT, AND THE ONE NUMBER IN THIS
      ITEM IS CORRECTED RATHER THAN LEFT TO AGE.** The class reports **67**
      sites across 23 members at `82a28086`, not 66 — the sixty-seventh is the
      supporting-docs manifest pull request #489 landed, not a digest that
      crossed the boundary (§ 5.2 proves which). The boundary itself held: the
      declared class, its key vocabulary and its non-member exclusions are
      byte-unchanged by both the realization and this archive, and the
      cross-repository values stay outside the sweep. A release digest is
      still sixty-four hexadecimal characters and still somebody else's
      question.
