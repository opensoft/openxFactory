# Tasks: amend-absent-changelog-is-an-answer

Status: draft
Kind: tasks

`code_surface: openxFactory`, `target_release: implemented`. The realization
group is § 3 and it is IN THIS PULL REQUEST: the tasks are individually
executable, so under `release-realization`'s decomposition rule this packet
realizes through its own task list rather than through a feature DAG.

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in
this pull request or a measurement recorded verbatim in the pull request body.
**§ 1 IS NOT TICKED AND NAMES WHY**: ratification has not happened.

## 1. Ratification — OWED, NOT GIVEN

- [ ] 1.1 **RATIFICATION IS OWED AND NOTHING HERE PERFORMS IT.** openxFactory
      issue **#750** records the defect and the shape of the remedy, and the
      ARCHIVED `amend-unreadable-read-sibling-scenarios` records this successor
      as OWED (`design.md` **D6**, `tasks.md` § 6). Neither decides a word of
      this text. Both are recorded as the ORIGIN in `proposal.md` front matter
      and in `.openspec.yaml`, which carries drafting provenance ONLY — no
      `approved_by`, no `approved_on`, the lawful unapproved shape
      `add-drafted-proposal-origin` defined. Every document in this packet
      carries `Status: draft`. When a word is given, this box is ticked with the
      verbatim utterance, ONE citation line is added to each document's front
      matter, the approval pair is ADDED beside the drafting provenance (`kind`
      and `id` never move), and the record is written to
      `review/ratification-<date>.md`.
- [ ] 1.2 **THE VETO POINT IS `design.md` D1** — option **A** (split the
      changelog arm on the fact the read already establishes, so a HELD tip with
      no readable changelog is graded with no declarations) against option **B**
      (keep the skip and give the held case a distinct reason class only). A is
      designed and encoded; B is written out beside it with its cost, which is
      that it leaves D6's suppression exactly where D6 found it and spends a
      packet saying so. **A veto of A is a veto of this delta's two bullets**,
      and the packet does not land on it.
- [ ] 1.3 **AND THE SECOND DECISION IS SEPARATELY VETOABLE — `design.md` D2**:
      whether the fact the retired skip carried is re-reported as an `info`
      beside the grading, or simply stops being reported. D2 takes the `info`,
      because `fam_release_tag_publication` turns every skip into an `info` so
      that a reason is *"recorded rather than omitted"*, and dropping it would
      silently retire the obligation #688 ratified — that the held case STATE
      THE PRESENCE. A veto of D2 removes one finding and one test and leaves
      § 3.1 and the delta's `THEN` untouched.

## 2. The reading D6 owed, and the measurement taken before the design

- [x] 2.1 **D6'S SHIM, RE-TAKEN ON THIS TREE RATHER THAN QUOTED.** One shim,
      two runs differing in ONE blob: `contracts/CHANGELOG.md` absent at a HELD
      tip against the same document present and empty. **THE BASELINE IS
      `origin/main` `d52e6b88`**, the head the measurement was RE-TAKEN at in the
      fix round; an earlier draft of this box cited `d5a549e4`, two main landings
      back, while `design.md` **D0** already carried the corrected sha, and the
      two documents now agree. **THE CITATION MOVED AND THE MEASUREMENT DID
      NOT**: `scripts/doc_health/release_tag_publication.py` and
      `tests/doc-health/test_release_tag_publication.py` are BYTE-IDENTICAL at
      `d5a549e4`, at `d52e6b88` and at the landing baseline `64aad02e` — blobs
      `6f627cb0` and `71662937` at all three — so nothing measured through those
      two modules is re-derived by the correction. At that baseline: ABSENT → one
      `Skip`, nothing graded; EMPTY → one `error`, *"contract-v2.0 is declared
      and has no published annotated tag more than 5 first-parent landings after
      the commit that declared it"*. On this branch: ABSENT → that same `error`
      PLUS one `info` recording the read; EMPTY → unchanged. The table is in
      `proposal.md` § Why and in `design.md` **D0**.
- [x] 2.2 **THE UNFETCHED FACT IS EXCLUDED AT THIS ARM, AND THAT IS WHY THE
      SPLIT IS SAFE.** `obtain_commit` runs before both reads; both `manifest is
      None` arms return before the changelog is consulted; `blobs_at` sends
      `<commit>:<path>` to `cat-file --batch`, which answers *missing* for EVERY
      spec of a commit the clone does not hold. So a manifest that READ is proof
      the commit is held. The split therefore consumes a fact the family already
      has and adds no probe and no round trip — `design.md` **D3**.
- [x] 2.3 **THE ARM IS UNREACHABLE IN THIS REPOSITORY, MEASURED.** openxFactory
      carries a readable `contracts/CHANGELOG.md` at its published tip, so
      `--family release-tag-publication` reads the same single `info` (the
      `contract-v2.6` SPENT record) before and after. The packet's behaviour
      change is exercised by shims and by the family's own test suite, and that
      is said rather than dressed up as a live measurement.

## 3. The realization — one guard, split on a fact the read already had

- [x] 3.1 `scripts/doc_health/release_tag_publication.py`, `check_repo`'s
      changelog guard: `if changelog is None:` becomes `if changelog is None and
      not tip_present:`. The UNFETCHED case keeps the skip, keeping the
      in-scope gate and the `return []` for a below-floor repository exactly
      where they were. The HELD case FALLS THROUGH: `read_changelog(None)`
      already answers an empty read — no declarations, no refusal — so the
      `in_scope` loop grades the bundles with NO declarations, which is what the
      same tip carrying an EMPTY changelog receives.
- [x] 3.1a **THE THIRD STATE IS ESTABLISHED BEFORE ANYTHING IS GRADED** (Codex,
      PR #753 round 1, P2, TAKEN). A held commit and a per-path `None` still
      stand for two facts — the tree carries no such path, or it carries it and
      the blob object is missing or corrupt — and GRADING is a claim about the
      FILE, which the held commit alone does not license. So `ls_tree_paths` is
      called once on that arm with the document's own path: where the tree does
      not list it the absence is ESTABLISHED and the bundles are graded; where
      the tree DOES list an ENTRY at it and no readable blob comes back the read
      FAILED and the SKIP STANDS, saying those two facts and naming no cause the
      listing did not check (§ 3.7b); where the listing itself fails the fact is
      UNESTABLISHED and the skip stands, saying that. Without it a damaged
      object store would read a REAL SPENT declaration as absent and answer an
      EXTINGUISHED obligation with a FALSE `error`. `design.md` **D3a**.
- [x] 3.2 **THE FACT IS RE-REPORTED, NOT DROPPED.** One `info` is appended,
      gated on `in_scope` being non-empty, carrying the words #688 ratified —
      the published tip *"WHICH THIS CLONE HOLDS"*, *"the commit is held in this
      store and no readable contracts/CHANGELOG.md blob is reachable at it"* —
      and saying what the family did with it: no SPENT declaration exists, the
      bundles in scope are graded with none. It lands on
      `contracts/CHANGELOG.md`, NOT on `contracts/manifest.yaml`, because a
      finding's identity is `(family, repository, path)` and a trace sharing the
      manifest's identity with the grading findings beside it would be masked by
      any one of them.
- [x] 3.3 **IT CLAIMS NO MORE THAN THE PRESENCE GIVES IT** (PR #688 adversarial
      review, P3, carried rather than re-derived). A held commit licenses *"no
      readable blob came back at this path"*, not *"the commit carries no such
      file"*: a store holding the commit AND its trees can still fail to produce
      the blob. The over-claiming form is pinned against NEGATIVELY in the same
      test, so it cannot come back.
- [x] 3.4 **THE UNFETCHED SKIP IS RE-WORDED, AND ONLY BECAUSE ITS BRANCH
      NARROWED.** It kept #688's held-tip words while now standing on the arm
      where the commit is NOT held, which would have made it assert the opposite
      of its own condition. It says instead that this clone does NOT hold the
      tip and that a bounded fetch of exactly that commit was attempted and did
      not obtain it — the manifest arm's own true words for the same fact — and
      it carries unchanged all three substrings the existing suite pins
      (`contracts/CHANGELOG.md could not be read at the published tip`, `not the
      same fact as there being none`, and the in-scope bundle name), so
      `test_an_unreadable_changelog_at_the_published_tip_skips` passes
      UNCHANGED.
- [x] 3.5 **THE UNREACHABLE BRANCH IS KEPT ON PURPOSE.** On real git the
      manifest read at the same commit proves the tip is held, so the unfetched
      arm cannot be reached through `check_repo`. Deleting it would make that
      proof load-bearing forever: any later change to the manifest arm — a
      cached read, a second source, a manifest served from another commit —
      would silently turn an unfetched tip into a graded one. It costs one
      comparison and fails closed. `design.md` **D3** records the decision and
      the comment in the module says it in place.
- [x] 3.6 **NO OTHER CONTROL FLOW MOVES.** Same reads, same order, same fetch
      window, same floor, same `return []` for a below-floor repository with no
      changelog, same skip for every other unaskable question. No severity of an
      existing finding changes and no existing finding's path moves.
- [x] 3.7 `tests/doc-health/test_release_tag_publication.py` **146 → 152**: SIX
      ADDED and ONE CONVERTED.
      - ADDED `test_a_held_tip_with_no_changelog_grades_exactly_as_an_empty_one_does`
        — D6's pair kept as a regression test: two shims one blob apart must
        produce the SAME grading, with a positive control asserting the empty
        run FIRES (or the comparison is two empty lists agreeing).
      - ADDED `test_an_unfetched_tip_still_skips_the_changelog_read` — the
        fail-closed half, asserting the new words, the absence of the held-tip
        words, and that the bounded fetch the skip claims was really attempted.
      - ADDED `test_a_below_floor_repository_with_no_changelog_gains_no_trace` —
        the floor holds over the trace as well as over the grading, held tip or
        not.
      - ADDED `test_a_held_tip_whose_tree_lists_the_changelog_still_skips` —
        D3a's third state: the tree carries the path, the blob does not come
        back, and the skip STANDS in words that say which fact it has.
      - ADDED `test_a_held_tip_whose_tree_cannot_be_listed_fails_closed` — the
        listing itself fails, nothing is established, nothing is graded.
      - ADDED `test_a_below_floor_repository_reaches_no_third_state_skip_either`
        — see § 3.7a.
      - CONVERTED `test_an_absent_changelog_says_the_tip_is_held_rather_than_unfetched`
        — see § 3.8.
      A shared `_EmptyChangelog` shim is added beside `_NoChangelog`, differing
      from it in one blob, so any difference the tests observe is attributable to
      that blob alone.
- [x] 3.7a **THE `in_scope` GATE ON D3a'S TREE CONSULTATION IS PINNED, AND IT
      WAS NOT** (PR #753 fix round). Dropping `and in_scope` from that guard
      left all 151 tests GREEN: the below-floor control ran through
      `_NoChangelog` alone, whose tree lists nothing, so it reached neither
      branch the gate holds back, and the `info` below carries a gate of its
      own. Unpinned, the mutation would give a repository nobody obliged to
      write a changelog a permanent "not checked" whose skip names an EMPTY set
      of bundles it declined to look for.
      `test_a_below_floor_repository_reaches_no_third_state_skip_either` runs
      the below-floor control through `_TreeListsChangelog` AND `_UnlistableTree`
      — held tip and unfetched, four combinations — asserting `[]` from each,
      with a POSITIVE CONTROL one version up so it cannot pass over a deleted
      branch. The mutation now fails exactly this test and nothing else; § 3.9
      carries the measurement.
- [x] 3.7b **THE TWO SKIPS D3a KEEPS ARE REWORDED TO WHAT THEY ESTABLISHED, AND
      BOTH NOW STATE THE PRESENCE** (PR #753 fix round). The damaged-store skip
      said the read was *"an object store that cannot serve what it lists"* — a
      CAUSE, and one this arm never checks: `ls_tree_paths` runs `ls-tree -r
      --name-only`, which filters by no object type, so a GITLINK whose target
      this clone does not hold lists exactly as a lost blob does (measured on a
      constructed repository: the submodule path lists while `cat-file --batch`
      answers `missing`). It now says the two facts it has — the tree at that
      commit LISTS AN ENTRY at that path, and no readable blob came back for it
      — and the conclusion they support: a READ THAT FAILED. The listing was NOT
      made type-aware: it would widen the seam to buy a distinction neither arm
      acts on. AND both skips now say the tip is one *"WHICH THIS CLONE HOLDS"*,
      because both stand BELOW the held-tip split and a skip that leaves the
      presence unstated is the unfetched case's words — #688's rule, applied to
      the two skips a held tip still emits. Both wordings are pinned, and the
      retired cause is pinned against NEGATIVELY.
- [x] 3.7c **THE `info`'S CLAIM IS QUALIFIED TO THE PATH IT READ** (PR #753 fix
      round, NOTE taken). *"NO SPENT DECLARATION EXISTS"* was unqualified, and a
      declaration written at a differently-cased or differently-placed path
      would still yield it; it now reads *"NO SPENT DECLARATION EXISTS at
      `contracts/CHANGELOG.md`"*. Its NEGATION is brought into line with the
      reworded arms in the same breath — *"neither an unfetched commit nor a
      listed entry whose blob did not come back"*, where it had named the
      retired cause — so the module states the same three answers in one
      vocabulary. The module comment claiming the tree is
      consulted *"ONCE, AND ONLY HERE"* is corrected to ONCE ON THIS ARM:
      `cut_bundles` already lists the tree under `contracts/releases/` on every
      run of every repository, so this is the second listing and not the first.
      No finding's severity, path or identity moves.
- [x] 3.8 **ONE EXISTING TEST IS EDITED, AND THE REASON IS THAT ITS ASSERTION
      BECAME FALSE.** `test_an_absent_changelog_says_the_tip_is_held_rather_than_unfetched`
      asserted `isinstance(out, Skip)` for the HELD case — the exact report this
      packet retires — so it cannot survive unchanged under any option that
      fixes D6. It is CONVERTED rather than deleted: every literal it pinned is
      re-asserted, unchanged, on the `info` that now carries them (the held
      words, the unreachability words, the negative pin against the manifest
      arm's fetch wording, the negative pin against the over-claiming tree
      assertion, and `fetch_calls == []`), plus one new negative pin so the
      record cannot be mistaken for a skip. **No other existing test is touched**
      — the other two changelog tests reach the unfetched arm, which does not
      move.
- [x] 3.9 **THE MUTATION PROBE ON ALL THREE GUARDS, RE-MEASURED AT THE
      FIX-ROUND HEAD.** The numbers below replace an earlier draft's, which were
      arithmetic from the pre-D3a design and were never re-taken after D3a
      landed. Reverting the held-tip split to `if changelog is None:` fails
      FIVE — the converted test, the D6 pair, both D3a third-state tests, and
      the below-floor third-state test (5 failed, 147 passed). Disabling D3a's
      tree consultation fails THREE — both third-state tests and the below-floor
      one (3 failed, 149 passed). Dropping `and in_scope` from that same
      consultation fails ONE (1 failed, 151 passed), and § 3.7a is the only
      thing that catches it. Restoring all three returns 152 passed. The
      results are carried in the pull request.
- [x] 3.10 **NO DEPLOYMENT HANDOFF IS IN SCOPE.** The realization lands in this
      repository's own `scripts/` and `tests/`, not onto a registered managed
      subject of another factory, so no correlation identifier is owed under
      `release-realization`'s managed-subject scenario and none is claimed.

## 4. The delta

- [x] 4.1 `specs/doc-health/spec.md` carries ONE `## MODIFIED Requirements`
      block over the promoted *Release-tag publication*, restating it in full —
      every body unit and all 30 promoted scenario titles, byte-faithful,
      INCLUDING #678's and #688's amendment notes and their `Removed from canon
      by` markers — and changing exactly TWO bullets of ONE scenario. Verified by
      diffing the block against canon: the diff is those two bullets, this
      packet's own amendment note and its two markers, and nothing else.
- [x] 4.2 **EACH DROPPED UNIT IS DECLARED BY ITS OWN MARKER, AND TWO MARKERS
      ARE WHY.** Under the boundary `amend-marker-reason-boundary` promoted (PR
      #719, archived #739) a marker's names are the code spans closing BEFORE
      its first ` — ` standing outside every span, so ONE marker naming two units
      separated by that sequence would declare only the first and REPORT the
      second. **A SEMICOLON WOULD HAVE WORKED** — canon's own written-out
      example at `openspec/specs/doc-health/spec.md:1778` separates two names
      with `; `, which the boundary leaves intact — **and two markers are still
      the right shape here, because a marker carries ONE reason and these two
      removals have DIFFERENT ones**: one bullet required a skip that suppressed
      a grading, the other constrains the wording of a skip no longer emitted.
      Two markers, one unit each, each quoted as a DOUBLE-backtick span with the
      list marker stripped, each saying the unit is REPLACED rather than
      deleted, each with its own reason.
- [x] 4.3 **NEITHER MARKER'S REASON CARRIES A CODE SPAN**, which is the
      self-reference hazard (`design.md` **D4**). With no span in the reason,
      the RETIRED grammar (the reason is everything after the LAST span's
      following ` — `) and the AMENDED one (the names are the spans before the
      FIRST ` — ` outside a span) derive the same single name and the same
      reason from each marker. Measured on this branch: `derive_units` reads
      four markers over the block — #678's, #688's and these two — each with
      exactly ONE name.
- [x] 4.4 **NO SCENARIO IS ADDED, AND THE ALTERNATIVE WAS CONSIDERED.** Both
      amended sentences live INSIDE the scenario *The changelog cannot be read at
      the published tip*, which pins them where they stand; appending scenarios
      would add a title, and a block that adds a title has `suppression`'s
      scenario-title cascade withheld from it. Nothing here needs a new title,
      so none is written.
- [x] 4.5 NO FILE IS ADDED UNDER `openspec/specs/` — no codexFactory floor
      advance is owed.
- [x] 4.6 **`sequenced_after` IS ELECTIVE AND IS NOT DECLARED.** Every other
      writer of this requirement is ARCHIVED and no ACTIVE change writes it, so
      there is no ordering for a declaration to settle. `proposal.md`
      § Sequencing states the reading, and the ledger row is seeded with the real
      pull request number.

## 5. Verification

- [x] 5.1 `python3 scripts/validate-openspec-cli-pin.py --all --no-cache` — the
      pinned 1.12 route `openspec-cli-pin-gate.yml` invokes — and
      `OPENSPEC_TELEMETRY=0 openspec validate amend-absent-changelog-is-an-answer
      --strict` through that same route. The prediction and why it holds: 1.12's
      scenario-currency check refuses a `## MODIFIED` block that OMITS a scenario
      the current spec carries; this block omits none and retitles none, so it
      adds NO undispositioned failure. Output carried verbatim in the pull
      request.
- [x] 5.2 `python3 -m pytest tests/doc-health -q` and the module count 146 →
      152. Carried in the pull request § Verification.
- [x] 5.3 `python3 scripts/doc-health.py --single-repo .` DIFFED against a
      SAME-CLOCK control: a temporary worktree of `origin/main` inside this
      clone, run minutes apart rather than against a stale baseline, and removed
      afterwards. The new active block must raise ZERO
      `modified-block-currency` carriage findings. Both columns are carried in
      the pull request.
- [x] 5.4 `python3 scripts/doc-health.py --single-repo . --family
      release-tag-publication`, before and after: the same single `info`, this
      repository never reaching the amended arm.
- [x] 5.5 **THE MUTATION PROBE ON THE DELTA, BOTH WAYS.**
      `modified-block-currency` reporting nothing about this block cannot be told
      from a block it never read, so a marker is removed and the family seen to
      FIRE on exactly the unit it declared, a promoted scenario title is mutated
      and the family seen to FIRE on the omitted scenario, and the delta is
      restored to silence. Results with the finding text in the pull request.
- [x] 5.6 `python3 scripts/validate-sequenced-after.py .`, `--ledger-diff`, and
      the origin gate `python3 scripts/proposal-support.py . verify
      amend-absent-changelog-is-an-answer`; `python3
      scripts/validate-scope-globs.py .`.
- [x] 5.7 The corpus-sweep ledger row, seeded with the real pull request number.
      **THE TICK PRECEDES THE SEED BY ONE COMMIT, AND THAT IS SAID RATHER THAN
      SMOOTHED OVER**, exactly as #688 § 5.7 said it: the row is seeded with the
      REAL pull request number and that number does not exist until the pull
      request does.

## 6. What this packet does NOT do, and what is owed

**THE TICKS IN THIS SECTION ARE ON THE RECORDING, NOT ON THE DOING** — Brett
Heap's ruling of 2026-09-06, *"Tick on the recording"*. What a packet owes about
work it is not doing is to NAME it, with the reading its successor needs. The
boxes below tick that naming and nothing else.

- [x] 6.1 **THE ESTATE-WIDE RUN IS NAMED AND IS NOT TAKEN HERE.** The
      measurement in this packet covers openxFactory only. `doc-health.py
      --repo-root` reads every governed submodule and `obtain_commit` FETCHES
      into each one where a tip is absent, so an estate-wide run WRITES INTO
      CHECKOUTS THIS LANE DOES NOT OWN; it is not a read-only measurement and it
      is not taken from here. The DIRECTION is safe by construction — the arm
      only ever turns a `Skip` into a grading, and a grading is what an empty
      changelog already receives — but a repository that really does hold its
      published tip and carry no readable `contracts/CHANGELOG.md` while
      declaring an in-scope bundle would begin receiving tag findings it was
      previously skipped past. **THAT IS THE FINDING THIS PACKET EXISTS TO
      SURFACE**, not a regression, and the estate-wide run belongs at landing, in
      an owner-run nightly, recorded there. #612's measurement says the nine
      other governed repositories return at the MANIFEST arm long before this
      one, so the expected estate delta is zero.
- [x] 6.2 **THE SKIP-TO-`info` SHAPE IS NOT GENERALIZED.** Other arms of this
      family still return a `Skip` for questions that genuinely cannot be asked —
      unlistable refs, an unresolvable declaring commit, a whole-batch read
      failure — and this packet touches none of them. Whether any of THOSE is
      also an answer wearing a question's clothes is a separate reading with its
      own scenarios, and it is not opened here.
- [x] 6.3 **THE ARCHIVED DELTAS THAT CARRY THE RETIRED BULLETS ARE NOT EDITED.**
      They are records of ratified acts, `promotion-fidelity` compares them
      against canon, and editing one would both mutate history and manufacture
      the divergence that family reports. Recorded so a later reader does not
      read the omission as an oversight.
- [ ] 6.4 **ARCHIVE.** `code_surface` is non-empty, so under `release-realization`
      this packet does NOT archive on landing: it archives on MERGE EVIDENCE PLUS
      A GREEN RUN of the surface on the implemented target, and on a separate
      word. Neither exists yet, and this box is where they will be cited — a
      merge commit on `main` and a workflow run id, both resolvable by an outside
      reader.
- [x] 6.5 **THE FLOOR EXEMPTION OVER THE SKIP IS RECORDED, NOT WIDENED** (PR
      #753 fix round; TICK ON THE RECORDING). The amended `THEN` requires a skip
      *"wherever the document's own absence has not been established"* with no
      qualification, and a BELOW-FLOOR repository is given neither the skip nor
      the grading: nothing is in scope, the tree is never consulted, and the arm
      returns `[]`. **The reading is PRE-EXISTING and this packet does not
      disturb it** — the promoted `THEN` carried the same unconditional MUST over
      the same `if not in_scope: return []`, put there by
      `declare-spent-bundle-state` on Copilot's PR #584 round 3 finding — and it
      is named here rather than fixed because making the floor exemption explicit
      in canon is a unit this MODIFIED block does not declare and would want its
      own scenario. **SUCCESSOR**: a change that states the enforcement floor's
      reach over this family's SKIPS as well as over its findings, in one added
      scenario, and that carries the same qualification into the sibling manifest
      read if it holds there too. `design.md` **D2**.
- [x] 6.6 **A LATE SKIP IN THE BUNDLE LOOP STILL DROPS THE TRACE** (PR #753 fix
      round; TICK ON THE RECORDING). The `info` § 3.2 appends is discarded whole
      by any of three arms below it that `return Skip(...)` — unlistable tag
      refs, unlistable refs for a named superseding bundle, an unresolvable
      declaring commit — so on those paths the amended `AND`'s *"the fact MUST
      STILL BE RECORDED"* is not honoured. **Measured**: a held tip with a bundle
      in scope, no readable changelog and a tag-ref seam that answers nothing
      returns `Skip("alphaFactory: the published refs for contract-v2.0 could not
      be consulted")` and the trace is gone. **The shape is PRE-EXISTING and
      general**: `check_repo` returns `Skip | list[Finding]` and
      `fam_release_tag_publication` branches on `isinstance`, so no return
      carries a skip beside findings — the raw-HTML `error`, every
      accepted-SPENT `info`, and any LIGHTWEIGHT or MISPLACED `error` raised for
      an earlier bundle in the same loop die on those same returns today. This
      packet adds one member to that set and does not create it. **SUCCESSOR**: a
      change that widens `check_repo`'s return contract so a partial skip travels
      WITH the findings already established, re-reads
      `fam_release_tag_publication`'s `len(skips) == len(scoped)` accounting for
      partial skips, and rules what a partial skip means to the cut-time gate,
      which fails closed on any skip. **AND THE SUCCESSOR HAS TWO REMEDIES, NOT
      ONE, SO ITS AUTHOR IS HANDED BOTH** — Copilot raised this same gap on the
      delta at PR #753 round 5, from the `AND`'s side rather than the loop's, and
      named the other one: **qualify the requirement** so it governs the case
      where the family ANSWERS for the repository at all, a repository-level skip
      being the family reporting that it could not, which
      `fam_release_tag_publication` already records as its own `info`. That is a
      wording change inside a bullet THIS BLOCK ALREADY REPLACES and would cost
      nothing in carriage — it is declined HERE only because it changes normative
      text a ratification word has not yet been given over, and a fix round does
      not move canon on a bot's reading. It is named so the ruling can take
      either. It belongs with § 6.2's reading of the other arms and is not opened
      here. `design.md` **D6**.
