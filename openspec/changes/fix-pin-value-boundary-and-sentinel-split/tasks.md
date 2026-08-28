# Tasks: fix-pin-value-boundary-and-sentinel-split

Every measurement quoted below was taken 2026-08-28 in a fresh worktree off
`origin/main` at `6612d3239cbc99b73eb32cf76a861929aa901276`. A task that cites a
number owes a re-measurement at realization, not a copy of the number.

## 1. Admission

- [ ] 1.1 Land the packet as an ACTIVE change with `Status: ratified`
      (the admission spelling: an approval act exists and is cited, per
      `sanction-ratified-record-spelling`), its
      `.openspec.yaml` recording the 2026-08-28 ad-hoc origin — Brett's verbatim
      selection "lets do all 3 in order" of the orchestrating session's
      recommended "the measured-latents bundle" — with the two voices kept
      apart, and the sibling `fix-content-resolution-conflation` named in
      `related:`.
- [ ] 1.2 README "OpenSpec Records" active entry, stating the two defects, the
      one ADDED requirement, the two-packet split and the parsed bundle
      measurement that justifies it.
- [ ] 1.3 `OPENSPEC_TELEMETRY=0 openspec validate fix-pin-value-boundary-and-sentinel-split --strict`
      and `--all --strict` green. Baseline before the packet: **76 passed, 0
      failed**.
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

- [ ] 2.1 Re-measure the defect on the realization branch before touching it,
      over all FOUR site-building expressions rather than the two the inherited
      record names: `_field_re` (`pin_class.py:204`), `_VOCAB_RE` (`:980`), the
      prose member pattern at `:347`, the prose member pattern at `:406`. Assert
      the fabricated forty-character prefix in each, and assert `LOOSE_SHA_RE`
      returns nothing on the same line. If any of the four has been fixed by
      another session in the meantime, say so and narrow the task rather than
      re-applying it.
- [ ] 2.2 Append `(?![0-9a-fA-F])` to the value group of all four. The
      construction is copied from `LOOSE_SHA_RE` rather than invented, so the
      module states the rule once. Do NOT add a leading `(?<![0-9a-fA-F])`: the
      group is already anchored by `\s*"?` and the guard would be inert
      (`design.md` § 3).
- [ ] 2.3 Prove the conforming path did not move. The six shapes measured at
      filing — bare, quoted, JSON, sequence item, comment-trailed, and each
      prose form — must still build the same site. This is the task that catches
      an over-tight boundary, which is the fix's real failure mode.
- [ ] 2.4 Prove the refused value still reaches the classification whole. A
      sixty-four-character value under a declared pin key must produce a
      DEFECT naming the full value, and NO pin site — the two halves asserted
      separately, because a test that only checks the absence of the pin would
      pass on a value silently dropped.
- [ ] 2.5 The declared class's own report must not move. Baseline at filing:
      **66 declared pin sites across 23 class members — 50 reachable, 0
      orphaned, 1 lost (declared unrecoverable, 0 awaiting a superseding
      record), 0 inconclusive; 0 uncovered, 0 vanished, 0 future members now
      carrying pins; 7 legal non-pins, 0 undeclared non-commit values, 3
      recognized legacy absences, 0 unused vocabulary members**, `clean` true.
      Every one of those numbers is expected IDENTICAL after the fix, because
      the corpus carries nothing the fix reclassifies — re-measured at filing:
      **1116 swept files, 0 values of 41 or more hexadecimal characters under
      any vocabulary key**. A number that moves is a finding, not a rounding.

## 3. Implementation — defect 3, the `"unknown"` split

- [ ] 3.1 Re-read all five emission sites before editing and confirm the
      condition each one means. The inherited record (`declare-sentinel-pin-vocabulary`
      § 5.6) names THREE sites; this packet measured FIVE, one of which fires on
      two conditions and one of which is already correct. Re-measure rather than
      trust either count.
- [ ] 3.2 `avatar_f0/cli.py` `_git_file_commit`: add the return-code branch that
      does not exist today. `out.returncode == 0` with empty stdout is
      `dirty-worktree` → `pin_sentinels.UNCOMMITTED_WORKTREE`; a non-zero return
      code is `unreadable-repository` → `pin_sentinels.UNCOMMITTED`. **This
      branch is the prerequisite for the whole split** — without it neither
      member can honestly be written at `:49` (`design.md` § 4).
- [ ] 3.3 `avatar_f0/cli.py` `_git_file_commit` `except Exception` (`:51`) and
      `_git_head` (`:60`, `:62`): all three become
      `pin_sentinels.UNCOMMITTED`. `rev-parse HEAD` producing nothing means it
      failed, so `:60` and `:62` are one condition wearing two spellings of the
      same failure.
- [ ] 3.4 `snapshot_registry.py:283`: the MEMBER does not change —
      `unestablished-revision` is the projector's actual condition — and the
      LITERAL does, to the imported constant. See Q3: if Brett rules against the
      cross-package import, leave the literal and record the ruling here rather
      than inventing a third home for the constant.
- [ ] 3.5 Update `pin_sentinels.SENTINELS` `emitters` tuples to follow the
      split, and update the `UNKNOWN` member's note, which currently states that
      its three call sites span three conditions and names the split as a
      follow-up. That note becomes false the moment this task lands; leaving it
      would make the declaration assert something the code contradicts.
- [ ] 3.6 `unused_sentinels()` must still report zero. Every member keeps at
      least one declared emitter after the split — assert it, because a split
      that stranded a member would fail the declaration's own
      declaration-against-corpus direction and the failure would look like an
      unrelated regression.
- [ ] 3.7 Confirm no committed artifact carries `"unknown"` under a swept key,
      so the split moves no committed bytes. Measured at filing: seven legal
      non-pins, six `uncommitted-worktree` and one `not-applicable-ad-hoc`, and
      not one `"unknown"`.

## 4. Verification

- [ ] 4.1 `set -o pipefail; python3 -m pytest tests/doc-health -q` — exit code
      READ, never inferred from the tail of the output. Baseline at filing:
      **1249 passed, 0 failed, exit 0** in 163s.
- [ ] 4.2 New regressions live beside the suites that own the surfaces —
      `tests/doc-health/test_pin_reachability.py` for the boundary,
      `tests/doc-health/test_sentinel_vocabulary.py` for the split and the
      emitter tuples.
- [ ] 4.3 Mutation-pin both fixes at SOURCE level, because both are refusals and
      a refusal that stops refusing is invisible in a value assertion. Remove one
      trailing boundary → the truncation proof must fail. Collapse one split site
      back to `"unknown"` → the emitter proof must fail. A proof that still
      passes is unpinned and gets rewritten rather than accepted.
- [ ] 4.4 A structural assertion over the declaration, per Q4's recommendation:
      every site-building expression in `pin_class.py` refuses an over-long
      hexadecimal run. This is what stops a future prose member from declaring an
      unguarded `pattern`, and it pins behaviour rather than the spelling of a
      regex.
- [ ] 4.5 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green.
- [ ] 4.6 Re-affirm by PARSE, not `grep`, that no contract bundle is owed: load
      every `contracts/releases/*.digests.yaml`, walk its entries into member
      paths, and assert that none of the four edited files appears in any of
      them. Measured at filing against `contract-v2.0`, the declared bundle: 192
      entries, 22 `scripts/` members, 0 under `scripts/doc_health/`,
      `scripts/ideation_dashboard/` or `experiments/`.
- [ ] 4.7 Guard the two standing substring traps this repository has been bitten
      by, both of which are source scans rather than behaviour tests: the
      staging-workbench no-write-path scan, which fails on the upper-cased HTTP
      verb for a write appearing anywhere in the files it reads (it once fired
      on the word "posture"), and the session-verbs scan over the wallet CLI,
      which fails on an approver flag spelled as a bare approval switch. Neither
      file is edited by this packet, so the check is a confirmation rather than
      a change — but both have reddened a suite here before on prose alone.

## 5. Archive gate

- [ ] 5.1 Merged to `origin/main` with both required checks green, the merge
      commit re-verified an ancestor of `origin/main` and a real two-parent
      merge read out of `git cat-file -p` rather than off the pull request page.
- [ ] 5.2 On the merged tree: `pytest tests/doc-health` green under
      `set -o pipefail`, `openspec validate --all --strict` green, and the
      declared pin class reporting `clean` with § 2.5's numbers re-measured.
- [ ] 5.3 No contract tag is owed (§ 4.6). This is what lets the packet archive
      without waiting on its sibling, and it is the whole argument of OD-1 — so
      it is re-affirmed at the archive rather than carried from the filing.
- [ ] 5.4 Every § 6 follow-up carries a disposition rather than a blank box, and
      every OD and Q carries a ruling or an explicit carry-forward.

## 6. Open — deliberately not closed by this change

- [ ] 6.1 **THE OTHER UNREPAIRED GENERATORS.** `_head_sha()`
      (`ideation_dashboard/nightly_lane.py:117`), `git_head_revision()`
      (`dashboard_refresh_lane.py:643`) and `RealGit.head_sha()`
      (`doc_health/corpus.py:534`) all run `rev-parse HEAD` with no cleanliness
      check. `corpus.py` is the widest-fanout pin source in the repository and a
      check there moves six record families at once. Inherited from
      `declare-sentinel-pin-vocabulary` § 5.1, still open, and not narrowed by
      this packet.
- [ ] 6.2 **WHETHER A COMPOSED PROJECTION SHOULD CARRY A PIN KEY AT ALL.**
      Inherited § 5.3. A schema question about the snapshot index, adjacent to
      this packet's `snapshot_registry.py` edit and deliberately not answered by
      it: this packet changes a literal to a constant and asserts nothing about
      whether the key belongs there.
- [ ] 6.3 **THE PREFLIGHT HALF OF THE ENFORCEMENT HOME STAYS UNWIRED.**
      Inherited § 5.4. The classification rides inside a verification that is
      pytest-plus-entry-point rather than nightly-gated.
- [ ] 6.4 **WHETHER A GENERATOR MUST IMPORT A DECLARED SPELLING RATHER THAN
      RETYPE IT.** Q3 recommends doing it here and legislating nothing, on the
      ground that one instance is not evidence for a rule. If a second generator
      retypes a literal, that is the evidence, and this item is where the next
      reader should find that said.
- [ ] 6.5 **CROSS-REPOSITORY PINS STAY OUT**, on the boundary both sibling
      packets drew. Whether a boundary defect or a sentinel is even meaningful
      for a gitlink, a `pinned_contract_manifest` entry, a release digest or an
      image digest is a question answered against a different remote by a
      different authority. Worth naming HERE rather than only inheriting it,
      because a release digest is a sixty-four-character hexadecimal value and
      is therefore exactly the shape defect 1 is about — it is out of scope
      because of WHOSE question it is, not because of what it looks like.
