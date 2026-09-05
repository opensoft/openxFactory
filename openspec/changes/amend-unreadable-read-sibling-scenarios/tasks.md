# Tasks: amend-unreadable-read-sibling-scenarios

Status: ratified
Ratified by: amend-unreadable-read-sibling-scenarios — 2026-09-05, Brett Heap, "ratify 688, land it when green" (record `review/ratification-2026-09-05.md`)
Kind: tasks

`code_surface: openxFactory`, `target_release: implemented`. The realization
group is § 3 and it is IN THIS PULL REQUEST: the tasks are individually
executable, so under `release-realization`'s decomposition rule this packet
realizes through its own task list rather than through a feature DAG.

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box is a diff in this pull
request or a measurement recorded verbatim in the pull request body. § 1 is NOT
ticked and names why.

## 1. Ratification — GIVEN 2026-09-05

- [x] 1.1 **RATIFIED 2026-09-05 by Brett Heap** (openxFactory operator
      authority), in session, verbatim *"ratify 688, land it when green"*.
      `proposal.md`, `design.md` and this file carry `Status: ratified` with ONE
      citation each, and `.openspec.yaml` gains the approval pair BESIDE the
      drafting provenance it was authored with — `kind` and `id` unmoved, which
      is the addition-not-rewrite shape `add-drafted-proposal-origin` defined.
      Record: `review/ratification-2026-09-05.md`.
- [x] 1.2 **THE VETO POINT WAS `design.md` D2 AND IT WAS NOT VETOED**: whether
      the third bullet — *the skip MUST say the commit is held and MUST state
      the presence* — is in scope at all, and with it the `openxFactory` code
      surface. Options A (two bullets, `code_surface: none`) and B (three
      bullets, code owing) were written out with their costs beside C's;
      **C is RATIFIED AS DESIGNED**, and the cost is ratified with it — under
      `release-realization` this packet archives on merged-plus-green
      realization evidence rather than on landing.

## 2. The sweep, and the false positives it raised

- [x] 2.1 **THREE ANGLES OVER `openspec/specs/`**, on this packet's own tree:
      the retired phrase (`commonest cause`), the fact it misnames (`not
      fetched` / `unfetched` / `has not fetched`), and the shape it sits in
      (`answers nothing` / `cannot be read`).
- [x] 2.2 **ONE LIVE SIBLING, AND IT IS THE ONE THIS PACKET AMENDS:**
      `openspec/specs/doc-health/spec.md:2818`, the `WHEN` of *The changelog
      cannot be read at the published tip*.
- [x] 2.3 **FALSE POSITIVE — `openspec/specs/doc-health/spec.md:2715`.** It
      carries the retired manifest clause, but it is the QUOTED UNIT inside
      #678's own ``**Removed from canon by …:**`` marker, not a live scenario
      bullet. The marker promotes into canon with the requirement by the same
      requirement that defines it, and rewriting its quoted unit would leave it
      declaring the removal of something that was never in canon. **It is
      carried byte-identical and is NOT amended.**
- [x] 2.4 **FALSE POSITIVE — `openspec/changes/archive/2026-09-05-amend-published-tip-unreadable-scenario/specs/doc-health/spec.md:484`.**
      The sweep found this as a second live site while that change was still
      active; **#685 archived it on 2026-09-05 and the path it was found at no
      longer exists.** An archived delta is a record of what was ratified: it
      does not re-promote, and `promotion-fidelity` compares it AGAINST canon,
      so editing it would both mutate history and manufacture the very
      divergence that family reports. **Not amended, and the reason is recorded
      in `proposal.md` § What this proposal does NOT claim.**
- [x] 2.5 **FALSE POSITIVE — `openspec/specs/doc-health/spec.md:1153`**, *A live
      main cannot be read*. Different family (promotion fidelity), different
      shape: it names no cause at all, and its `THEN` FALLS BACK to the checkout
      rather than reporting a skip. There is nothing here to establish and
      nothing misnamed.
- [x] 2.6 **FALSE POSITIVE — `openspec/specs/ideation-cross-reference/spec.md:386`**,
      *"a commit an ancestor walk from `main` reaches is conforming even in a
      clone that has not fetched it"*. Raised by angle 2's own grep and MISSING
      from the first draft of this list (PR #688 adversarial review, P3). It is
      a different family and a different subject: PIN REACHABILITY, judged
      against refs rather than against a particular clone's object store, where
      "has not fetched" is used CORRECTLY — to say that a local store's contents
      are not the test. There is no read that answers nothing, no cause named as
      commonest, and nothing to amend.
- [x] 2.7 **NOT A SIBLING — the tag-peel read.** The manifest scenario's closing
      `AND` already binds it (*"the same MUST hold for the commit a tag peels
      to"*), `_tag_state` already calls `obtain_commit` on the peeled commit, and
      that bullet is carried byte-identical here. No second scenario is owed.

## 3. The realization — one skip's words

- [x] 3.1 `scripts/doc_health/release_tag_publication.py`, `check_repo`'s
      changelog guard: the `Skip` reason now STATES THE PRESENCE — the published
      tip *"WHICH THIS CLONE HOLDS — the commit is held in this store and no
      readable contracts/CHANGELOG.md blob is reachable at it, so this is not an
      unfetched commit"* — while keeping every substring the suite already pins.
      **IT STATES THE READ, NOT A TREE FACT** (PR #688 adversarial review, P3):
      a held commit licenses *"nothing readable came back at this path"*, not
      *"the commit carries no such file"*, because a store holding the commit
      AND its trees can still fail to produce the blob. `design.md` D4 records
      the narrowing.
- [x] 3.2 The comment above it no longer names *"a checkout that has not fetched
      the published tip"* as the commonest cause. It names BOTH facts, and then
      names which one holds here and why: `obtain_commit` ran above, and the
      manifest READ at this same commit, which `cat-file --batch` cannot do for
      a commit the clone does not hold.
- [x] 3.3 **NO CONTROL FLOW MOVES.** Same position, same `in_scope` gate, same
      return type; a below-floor repository with no changelog still returns
      `[]`. No probe is added — see `design.md` D3 for why a second one would be
      a round trip justified by nothing.
- [x] 3.4 `tests/doc-health/test_release_tag_publication.py`: one test ADDED
      (`test_an_absent_changelog_says_the_tip_is_held_rather_than_unfetched`)
      pinning the two new fragments as fresh literals and asserting NEGATIVELY
      on TWO counts — against the manifest arm's *"a bounded fetch of exactly
      that commit was attempted and did not obtain it"*, so the two skips cannot
      drift into each other's words, and against the OVER-CLAIMING form *"carries
      no contracts/CHANGELOG.md"*, so the tree assertion the read cannot support
      cannot come back. The existing changelog test is UNCHANGED and still
      passes: all three of its literals are still carried. 145 → 146 tests in
      that module. **AND THE HELD-TIP PRECONDITION IS DECLARED** (Copilot, PR
      #688 round 2): `FakeGit`'s object store is pessimistic by default, so the
      shim now sets `present_commits={"tip"}` and the test asserts
      `fetch_calls == []` — the held-tip words are pinned over a double that
      actually holds the tip, and holds it without a round trip.
- [x] 3.5 **THE REALIZATION EVIDENCE, WHICH IS WHAT THIS PACKET ARCHIVES ON.**
      `code_surface: openxFactory` is non-empty, so under `release-realization`
      § *Realization archive gate* this packet does NOT archive on landing: it
      archives on MERGE EVIDENCE PLUS A GREEN RUN of the surface, on the
      implemented target. Both now exist and are cited rather than asserted:
      - **MERGED** on the implemented target (`openxFactory` main) as
        **PR #688 → `a59d5463`**, *"Ratify and realize
        amend-unreadable-read-sibling-scenarios: the changelog read names both
        facts and its skip says which"*, 2026-09-05 21:53:14Z, through the
        repository's own required gates (all ten checks green on the merged
        head `d6fd07b1`).
      - **GREEN ON MAIN** afterwards: `pytest-suite` run
        **[33995187827](https://github.com/opensoft/openxFactory/actions/runs/33995187827)**,
        conclusion `success`, on `main` at `724a2a4f` — a commit that CONTAINS
        `a59d5463`. The runnable surface is the doc-health test suite that pins
        this skip's words, so a green run of it on a main containing the merge
        is the green run the gate names.
      **Neither half is a local assertion.** Both are references an outside
      reader can resolve: a merge commit on `main` and a workflow run id. The
      archive act that promotes this delta cites both.
- [x] 3.6 **NO DEPLOYMENT HANDOFF IS IN SCOPE.** The realization does not deploy
      onto a registered managed subject of another factory — it lands in this
      repository's own `scripts/` and `tests/` — so no correlation identifier is
      owed under `release-realization`'s managed-subject scenario, and none is
      claimed.

## 4. The delta

- [x] 4.1 `specs/doc-health/spec.md` carries ONE `## MODIFIED Requirements`
      block over the promoted *Release-tag publication*, restating it in full —
      every body unit and all 30 promoted scenario titles, byte-faithful,
      INCLUDING #678's amendment note and its `Removed from canon by` marker —
      and changing exactly one scenario: the `WHEN` bullet REPLACED, two `AND`
      bullets ADDED. Verified by diffing the block against canon lines
      2339–2873: the diff is those three edits and the new note, and nothing
      else.
- [x] 4.2 **THE ONE DROPPED UNIT IS DECLARED.** The block carries
      `**Removed from canon by amend-unreadable-read-sibling-scenarios
      (2026-09-05):**` naming the old `WHEN` bullet verbatim as a DOUBLE-backtick
      code span — double because the unit itself contains a single-backtick span
      — with the reason, and saying it is a REPLACEMENT rather than a deletion.
- [x] 4.3 NO FILE IS ADDED UNDER `openspec/specs/` — no codexFactory floor
      advance is owed.
- [x] 4.4 **`sequenced_after` IS ELECTIVE AND IS NOT DECLARED.** All four other
      writers of this requirement are ARCHIVED and no ACTIVE change writes it,
      so there is no ordering for a declaration to settle. `proposal.md`
      § Sequencing states the reading.

## 5. Verification

- [x] 5.1 `OPENSPEC_TELEMETRY=0 openspec validate
      amend-unreadable-read-sibling-scenarios --strict` and `--all --strict`.
- [x] 5.2 **THE SAME VALIDATION THROUGH THE PINNED 1.12 ENTRYPOINT**,
      `python3 scripts/validate-openspec-cli-pin.py --all --no-cache`, exactly as
      `openspec-cli-pin-gate.yml` invokes it. The prediction and the reason it
      holds: 1.12's scenario-currency check refuses a `## MODIFIED` block that
      OMITS a scenario the current spec carries; this block omits none and
      retitles none, so it adds NO undispositioned failure. The two the run
      reports are `#677`'s standing dispositions.
- [x] 5.3 `python3 -m pytest tests/doc-health tests/sequenced_after -q`.
- [x] 5.4 `python3 scripts/validate-sequenced-after.py .` and `--ledger-diff`.
- [x] 5.5 `python3 scripts/doc-health.py --single-repo .` against a SAME-CLOCK
      control at the CURRENT `main` tip, run minutes apart rather than against a
      stale baseline.
- [x] 5.6 **THE MUTATION PROBE, BOTH WAYS.** `modified-block-currency` reporting
      nothing about this block cannot be told from a block it never read, so the
      marker is removed and the family seen to FIRE on exactly one dropped unit,
      a promoted scenario title is mutated and the family seen to FIRE on the
      omitted scenario, and the delta is restored to silence. Recorded in the
      pull request.
- [x] 5.7 The corpus-sweep ledger row, seeded with the real pull request number.

## 6. What this packet does NOT do, and the successor it names as OWED

- [ ] 6.1 **OWED SUCCESSOR — the held-and-absent skip still SUPPRESSES the
      grading.** `scripts/doc_health/release_tag_publication.py`'s
      `if changelog is None:` guard stands ABOVE the `in_scope` loop and
      RETURNS, so a held tip carrying an in-scope bundle and no
      `contracts/CHANGELOG.md` is answered with a skip INSTEAD OF the tag
      findings the loop would emit. Measured on a shim: tag absent and no
      changelog blob → one `Skip`; the SAME shim with an EMPTY changelog → one
      `error` on the untagged bundle. **NOT A REGRESSION** — `origin/main`
      answers identically — and **NOT FIXED HERE**: moving that return changes
      which findings an in-scope repository receives, which owes its own
      scenarios, its own severity reading and its own measurement.
      `design.md` **D6** records the decision and says what the successor owes;
      `proposal.md` § What this proposal does NOT claim carries it as a named
      carve-out. **This box stays UNTICKED: it is the next packet's, exactly as
      #678's § 4.2 held this one.**
- [ ] 6.2 **The promoted `THEN` is what that successor amends.** It says the
      family MUST NOT treat the absence of a declaration *"it could not look
      for"* as the absence of a declaration — and at this arm, after the
      amendment, it CAN look. This packet carries the bullet byte-identical
      (`design.md` D1) rather than rewriting a promoted `THEN` under a
      ratification that did not reach it.

