# Tasks: harden-ideation-readiness-check

**REALIZED 2026-08-26** — and this header said the opposite for one day, so
the history is kept rather than overwritten. As authored it read "NO
IMPLEMENTATION here is discharged. This packet is a PROPOSAL: it carries the
delta, the measurement, and the plan, and it changes no code." That was true
while it stood. § 1.1 and § 1.2 were discharged by Brett's admission on
2026-08-26; § 2, § 3 and § 4.1–4.5 are discharged by the realization, each
with its evidence written into the task rather than asserted. § 1.3 is
PARTIAL and says so: Q1 and Q2 were taken as measured decisions because the
implementation cannot be written without them, Q3 and the four flagged
decisions were NOT.

**§ 4.6 STAYS OPEN**: the change ships ACTIVE and archives only on
merged-plus-green, in its own commit after the merge.

**§ 5 is deliberately OPEN and stays open.** Two adjacent gaps are recorded
there rather than implied, and one of them is the follow-up packet the
proposal declines to write. § 5.1 (Q3) was not taken by the realization: the
three resolver spellings are fixed in place, exactly as § 2 prescribes.

**READ THE TWO PARAGRAPHS ABOVE AS HISTORY, NOT AS STATUS — ARCHIVED
2026-08-27.** "§ 4.6 STAYS OPEN" was true of the packet until PR #400 merged
at 2026-08-27T03:05:03Z; § 4.6 is now the archive act itself and is ticked
there with its evidence. The § 5 paragraph is still true and stays true: § 5.1,
§ 5.2 and § 5.3 survive the archive as named follow-ups, and § 5.1 does so
UNDER A RULING rather than by default — see § 1.3.

**§ 1.3 IS NO LONGER PARTIAL.** Brett ruled on all three open questions and
cleared all four flagged decisions on 2026-08-27, by a four-question
multi-choice put by the orchestrating session after 2026-08-26T23:31Z and
relayed the same day. Q1 RATIFIED (keep the narrowed skip), Q2 RATIFIED
(`4e57009c`), Q3 RULED LEFT OPEN deliberately, and the four § Orchestrator
decisions CLEARED as authored. Nothing in the packet moved as a result: every
ruling matched what the realization had already shipped.

## 1. Admission

- [x] 1.1 **DONE 2026-08-26 — Brett admitted the packet, with his approval.**
      As written, this task said no approval act existed and that
      `.openspec.yaml` therefore carried NO `approved_by` / `approved_on`,
      because the authoring session had none to record and the promoted origin
      requirement will not be satisfied by inventing one. That state lasted
      one day. The ruling was given against `proposal.md` § Open Questions Q0
      while the packet stood at PR #372 and reached the authoring session the
      same day; no verbatim wording came with it, so none is quoted anywhere
      in the packet — approver, date and record are stated instead. The two
      `ad-hoc origin lacks required` ERRORS this task predicted were the
      honest signal while they stood, and 1.2 clears them.
- [x] 1.2 **DONE 2026-08-26.** `.openspec.yaml` `approved_by` records Brett
      and the admission ruling of 2026-08-26; `approved_on` is `2026-08-26`;
      the `approval_pending` key that explained the blank pair is resolved
      into an `approval_note` that keeps the history legible rather than
      erasing it. `proposal.md`'s `Status:` moved `draft` → `ratified` with a
      single record-citing `Ratified:` line clearing the spelling's three-way
      floor on all three axes — approver, date, and a resolvable record path.
      The README's active-changes entry, which asserted `Status: draft` and
      UNADMITTED and predicted the two errors, is corrected in the same edit,
      because leaving it would make the README false about a fact the packet
      itself now records otherwise.
- [x] 1.3 **CLOSED 2026-08-27 — ALL THREE QUESTIONS DISPOSED AND ALL FOUR
      DECISIONS CLEARED. See the note at the end of this item; the body below
      is kept as the state it recorded while it stood.** AS AUTHORED AND AS
      REALIZED: **PARTIAL, and the split is stated rather than blurred.** The
      realizing session took Q1 and Q2 as MEASURED DECISIONS, because § 2 and
      § 3 cannot be written without them, and recorded both against the
      questions in `proposal.md` with the evidence each rests on: **Q1 = KEEP
      the narrowed skip** (the recommendation on record; a skip that names an
      observed truncation is not the silence defect B was, and no runner that
      matters is shallow), **Q2 = `4e57009c`** (re-measured 2026-08-26 in this
      worktree, and the measurement moved: the derivation reproduces the
      committed 290-entry skeleton at `da9bf3b7`, at `4e57009c` and at the
      old `origin/main` of `31c931fa`, but at CURRENT `origin/main` it derives
      **288** — the corpus has moved since the packet was authored, so the
      "regenerate at current main" alternative now costs a body regeneration
      the packet did not price. Q2's recommendation is stronger than when it
      was written, not weaker). **Q3 IS NOT RULED and was deliberately not
      taken**: § 2 fixes all three helpers in place exactly as written, and
      § 5.1 stands open. The four decisions in § Orchestrator decisions were
      likewise NOT ruled — they remain flagged for veto, and the realization
      implements them as written rather than re-opening them.
      **THE CLOSURE, 2026-08-27.** A four-question multi-choice was put to
      Brett by the orchestrating session after 2026-08-26T23:31Z and relayed
      the same day. He ruled: **Q1 RATIFIED** — keep the narrowed skip, which
      fires only on an OBSERVED shallow clone; **Q2 RATIFIED** — the re-pin
      target is `4e57009c`; **Q3 RULED LEFT OPEN, DELIBERATELY** — the three
      helper copies stay in place with the parametrized anti-drift guard, and
      the collapse survives as a named follow-up at § 5.1; and **all four
      § Orchestrator decisions CLEARED as authored**, none vetoed (OD-1 the
      ADDED-in-`doc-health` shape, OD-2 the committed-revision read point, OD-3
      the re-pin target, OD-4 the repair riding this change). No verbatim
      wording of the ruling reached this session, so none is quoted anywhere in
      the packet — approver, date, mechanism and the option selected on each
      question are stated instead, which is the same shape this packet's own
      admission is recorded in.
      **TWO DISTINCTIONS WORTH HOLDING.** First, Q1 and Q2 were TAKEN by the
      realizing session as measured decisions and are now RATIFIED by Brett;
      those are two acts, not one, and both are recorded because a measured
      decision that later turns out to have been ruled all along is exactly the
      provenance blur this packet spent § 1.1 refusing. Second, **Q3 IS
      DISPOSED, NOT UNANSWERED**: "left open" is the ruling, so § 5.1 crosses
      the archive unticked BY DECISION. NOTHING IN THE PACKET MOVED — every
      ruling matched what the realization had already shipped, so the closure
      required no edit to a requirement, a delta, a task body or a design entry,
      the shape openxFactory PR #307 recorded when Brett cleared the two codex
      dispositions there.

## 2. Implementation — the three requirements

- [x] 2.1 **DONE.** `tests/doc-health/test_ideation_readiness.py` carries the
      resolution order `design.md` § 1 records: repository under test, then an
      explicit `fallback=` argument, then `OPENXFACTORY_ROOT`, then the walk.
      Every rung past the first announces the checkout it resolved and why
      (`ROOT_FALLBACK_MARKER`, injectable `announce=` so the announcement is
      assertable). The four call sites moved to a new
      `_openxfactory_root_or_skip()`, whose skip reason names what was searched
      — the delta's "No checkout can serve the proof" scenario, which the old
      `"openxFactory checkout unreachable"` did not satisfy.
- [x] 2.2 **DONE**, identically, in `tests/doc-health/test_derive_possibles.py`
      and `tests/doc-health/test_readiness_dispatch.py`. The three spellings
      are exercised TOGETHER by
      `tests/doc-health/test_readiness_proof_resolution.py::RESOLVERS` — every
      resolver test is parametrized over all three modules, so a module left
      behind by a future edit fails the suite rather than being trusted
      because its sibling was fixed.
- [x] 2.3 **DONE.** `find_index_validator(start=None, *, announce=…)` tries
      `<repo>/scripts/validate-ideation-cross-reference.py` first, then
      `OPENXFACTORY_ROOT`, then the sibling walk, announcing on stderr. The
      measured defect is pinned by
      `test_the_validator_resolves_out_of_the_repository_under_test`, and
      reverting this resolver alone reddens it (mutation run recorded in § 4).
      A second, welcome consequence: a STANDALONE clone (this repo's own CI
      `validate` job) now resolves its own validator, where the sibling walk
      found none.
- [x] 2.4 **DONE.** `_committed_index(repo, ref="HEAD")` reads the index with
      `git show <rev>:ideation/cross-reference.yaml` and returns the resolved
      40-character revision with it; both assertions in the proof carry a
      message naming that revision and the pin the corpus was read at. It
      fails closed when the index is not committed at that revision, so no
      future edit can quietly restore the working-tree read.
- [x] 2.5 **DONE.** `_corpus_at_pin()` asks
      `git rev-parse --is-shallow-repository` and `git cat-file -e
      <rev>^{commit}` before deciding. Complete clone plus unresolvable pin →
      `pytest.fail`, naming the pin, the index that carries it, and both
      observations. Truncated history → `pytest.skip`, reason opening
      "TRUNCATED CLONE, observed not conjectured". The old
      `"(shallow clone?)"` string is gone, and a regression asserts it never
      returns.
- [x] 2.6 **DONE** — `tests/doc-health/test_readiness_proof_resolution.py`, 24
      tests, all four bullets and all nine delta scenarios. Fixture repos are
      real two-commit git repositories under `tmp_path` (corpus committed
      first, index committed second pinning the corpus commit, so the proof's
      two sides are genuinely independent); no checkout on the machine is
      read or written. The mutation check is
      `test_mutation_reverting_the_resolver_alone_reproduces_defect_a`, which
      spells the pre-change walk out verbatim and asserts it resolves the
      ancestor decoy over the SAME fixture where the shipped resolver resolves
      the repository under test — so the fixture is proved to reproduce defect
      A rather than merely to pass. Two further mutants were run by hand and
      recorded in § 4.
      **One discrimination worth naming**: the unreachable-pin regression
      catches `(Failed, Skipped)` and then asserts WHICH was raised. Catching
      only `Failed` would report a regression back to the skip as a SKIPPED
      test — a green scoreboard over an absent verification, which is defect C
      itself, in the test that exists to prevent it.

## 3. Repair of the current defect instance

- [x] 3.1 **DONE.** One line: `generation.source_revision`
      `f13a3b60…` → `4e57009c0a1aed9bdbe3c0f6cc5ca948e15ec8cc`. Re-measured
      before writing, in this worktree, by rebuilding the derivation from the
      corpus at each candidate and comparing skeletons against the COMMITTED
      body (290 entries):

      | revision | reachable | derived | reproduces committed body |
      | --- | --- | --- | --- |
      | `f13a3b60` (the orphan pin) | no ref | 290 | yes |
      | `da9bf3b7` (generated at) | no ref | 290 | yes |
      | **`4e57009c`** (landed the index) | **yes** | **290** | **yes** |
      | current `origin/main` (`275d065d`) | yes | **288** | **NO** |

      THE LAST ROW MOVED SINCE THE PACKET WAS AUTHORED and is reported rather
      than smoothed over: at `31c931fa` the proposal measured 290 at
      `origin/main`, and today's main derives 288. The corpus has grown past
      the index in the ordinary way, which is exactly the drift the pin exists
      to survive — and it means "regenerate at current main" would now owe a
      body regeneration. No regeneration is owed for `4e57009c`.
- [x] 3.2 **DONE.** Scratch `git clone --bare --no-local` (fetch-based, so no
      unreachable object is copied — `--local` would have hidden the defect):
      `rev-parse --is-shallow-repository` → `false`;
      `cat-file -t f13a3b60` → 128, `cat-file -t 4e57009c` → `commit`;
      `git archive f13a3b60 ideation` → 128, `git archive 4e57009c ideation`
      → 0. Complete clone, old pin absent, new pin readable.
- [x] 3.3 **DONE.** `python3 scripts/validate-ideation-cross-reference.py
      ideation/cross-reference.yaml --repo . --strict` →
      `0 error(s), 0 warning(s)`, exit 0.
- [x] 3.4 **DONE.** Regenerated through
      `scripts/render-ideation-cross-reference.py` (never hand-edited);
      the renderer reported `290 clusters`, and `git diff` over
      `ideation/cross-reference.md` is EXACTLY ONE LINE — the
      `- Source revision:` line at line 9. Nothing else moved.

## 4. Verification

- [x] 4.1 **DONE — 920 passed, 0 failed** (`python3 -m pytest tests/doc-health
      -q`, in the realization worktree off `bb7d7ae8`). 896 before, 920 after:
      the 24 added are § 2.6's regressions, and no existing test moved. The
      packet's **1 failed / 895 passed** baseline was reproduced EXACTLY under
      the conditions that produced it — see 4.4.
- [x] 4.2 **DONE.** `openspec validate harden-ideation-readiness-check
      --strict` → "is valid"; `openspec validate --all --strict` → **77
      passed, 0 failed**.
- [x] 4.3 **DONE, AND IT IS THE FIRST EXECUTION.** Fresh fetch-based clones
      (`git clone --no-local file://…` — never `--local`, which copies
      unreachable objects and would have hidden the defect). Each is complete:
      `rev-parse --is-shallow-repository` → `false`, and NONE of them carries
      `f13a3b60`, which is the packet's defect-B measurement reproduced.

      | clone | code | ancestor checkout | verdict |
      | --- | --- | --- | --- |
      | fresh, isolated | pre-change | none | **SKIP** — "openxFactory checkout unreachable" |
      | fresh, isolated | this change | none | **PASS** |
      | fresh, under an aggregation root | pre-change | clean | **SKIP** — "pinned revision f13a3b600773 unreachable (shallow clone?)" |
      | fresh, under an aggregation root | this change | clean | **PASS** |

      A FINDING THIS RUN SURFACED, reported rather than suppressed: in an
      ISOLATED clone the pre-change resolver could not find the repository's
      OWN index at all, so the proof skipped before it ever reached the pin.
      This repository's own CI clones exactly that way. So the assertion was
      unreachable by two independent routes, not one, and the packet named
      only the second. Measured over the whole doc-health suite in that
      isolated shape: **pre-change 889 passed / 7 skipped**, **this change 920
      passed / 0 skipped** — seven real-corpus proofs (the derivation proof,
      the validator wiring, the pipeline proof) that no runner had ever run.

      **AND THE RUNNER HAS NOW RUN IT.** `pytest-suite` on PR #400, which
      checks out a fresh clone at `fetch-depth: 0` with no aggregation
      workspace above it: **6638 passed, 20 skipped, 0 failed** in 13m07s,
      green. That is the first execution of this assertion on continuous
      integration in the life of the test.
- [x] 4.4 **DONE — THE ACCEPTANCE SIGNAL.** Nothing was written to the shared
      checkout: the hazard was reconstructed instead, faithfully, as an
      aggregation root holding a checkout at `openxFactory/` with two fresh
      clones beneath it at `worktrees/`. The sibling was then dirtied into
      the exact 2026-08-26 shape — an uncommitted, hand-bumped pin
      (`source_revision` → its own HEAD) with the body left as generated and
      truncated to 67 `topic_entries`.

      | run | verdict |
      | --- | --- |
      | pre-change code, sibling dirty | **1 failed, 895 passed** — the packet's baseline, reproduced to the number |
      | this change, sibling dirty | **920 passed** |
      | this change, sibling clean | **920 passed** — same verdict, which is 4.4's whole question |

      The red the pre-change suite takes there is a verdict about another
      checkout's unsaved file. The fixed suite is indifferent to it.
- [x] 4.5 **DONE, and it moved by nothing — literally.** Single-repo
      `scripts/doc-health.py --single-repo . --as-of 2026-08-26` before and
      after the whole change: **5 critical / 7 error / 4 info / 41 warning**
      both times, family counts identical (`staged-topic-template` 27,
      `staged-candidate-aging` 15, `record-immutability` 5, `status-validity`
      4, `location-conformance` 3, `ideation-routing` 2, `document-catalog`
      1), and `diff before.md after.md` is EMPTY. `release-inventory-drift`
      and `proposal-origin` are both 0 before and after — § 1.2 had already
      cleared the two `proposal-origin` errors this task anticipated.
      RELEASE-BUNDLE MEMBERSHIP CHECKED, not assumed: none of
      `scripts/doc_health/ideation_readiness.py`, the four test modules,
      `ideation/cross-reference.yaml` or `ideation/cross-reference.md` appears
      in ANY `contracts/releases/*.digests.yaml` — the inventories carry only
      `contracts/`, `schemas/` and the `hermes_runtime_validation` surface. No
      bundle is owed.
- [x] 4.6 ARCHIVE AFTER REALIZATION. This change ships ACTIVE and archives
      only on merged-plus-green plus 4.3, following
      `add-family-enumeration-check` and `add-duplicate-packet-check`. The
      archive act is its own commit after the merge. **STILL OPEN AND
      DELIBERATELY SO**: 4.3 is discharged, but the realization PR is not
      merged, and this task is the one that must not be ticked early.
      **DONE 2026-08-27 — THE GATE IS FULLY DISCHARGED, AND THIS ENTRY IS THE
      ARCHIVE ACT.** The paragraph above is kept as the state it recorded while
      it stood; every arm below is checked rather than asserted
      (`release-realization/spec.md`). CODE MERGED ON THE IMPLEMENTED TARGET —
      pull request #400, merged 2026-08-27T03:05:03Z as merge commit
      `78ffb7f178ffd1c3343996470cb2e12a810ece1f`, re-verified here an ancestor
      of `origin/main` (`git merge-base --is-ancestor`, exit 0) rather than
      taken from the pull request page. THE RUNNABLE SURFACE RAN GREEN — on the
      final head `e9886d77685a56f2bd940974205625bcb5ac6804`, `pytest-suite` and
      `wallet-validation` both concluded `success` (read back from the
      check-runs API at this act, not from the merge notification):
      `pytest-suite` 00:37:54Z → 00:51:30Z, 13m36s, **6638 passed, 20 skipped,
      0 failed**. Locally on the merged tree, `python3 -m pytest tests/doc-health
      -q` → **920 passed, 0 failed, 0 skipped**, run BEFORE and AFTER the
      archive with the same verdict. 4.3'S OWN ARM, the one the code could not
      give: the pin is `4e57009c…` in both `ideation/cross-reference.yaml:10`
      and `ideation/cross-reference.md:9` on `main` as merged.
      NO BUNDLE WAS OWED and it stayed unowed — 4.5's membership check is
      re-affirmed by this act's own doc-health run, whose
      `release-inventory-drift` family reports **0 findings before and after**.
      **THE ACT.** ARCHIVED to
      `openspec/changes/archive/2026-08-27-harden-ideation-readiness-check/` by
      `OPENSPEC_TELEMETRY=0 openspec archive harden-ideation-readiness-check
      --yes` (openspec 1.2.0), which reported `doc-health: update`, `+ 3 added`,
      `Totals: + 3, ~ 0, - 0, → 0` and applied the delta into
      `openspec/specs/doc-health/spec.md`. It also reported `Task status: 18/22`
      and warned on four incomplete tasks, which is CORRECT and expected: this
      task was the eighteenth, and § 5.1, § 5.2 and § 5.3 survive the archive as
      named follow-ups — § 5.1 under Brett's 2026-08-27 ruling that Q3 stays
      open. **THE MECHANISM WAS `openspec archive`, NOT `proposal-support
      archive`, and the choice is deliberate.** `proposal_support.archive_change`
      refuses any change whose `tasks.md` still carries a `^- \[ \]` line — a
      blanket gate that cannot tell a ruled-open follow-up from unfinished work.
      The two things that wrapper adds were run anyway: the origin gate,
      `python3 scripts/proposal-support.py . verify
      harden-ideation-readiness-check` → `proposal support verification ok`
      BEFORE the move, and the whole-corpus sweep `verify` (no argument) → ok
      AFTER it; and packaging, a lawful no-op here because an ad-hoc origin with
      no `supporting-docs/` folder has nothing to bundle. The precedent is the
      sibling `2026-08-26-fix-release-reachability-race`, plus
      `ratify-doxbench-landed-context-surfaces` and the four archived siblings
      that carry unticked follow-ups through the archive.
      **THE KNOWN CLI HAZARD DID NOT FIRE, AND THAT WAS VERIFIED RATHER THAN
      ASSUMED.** The sibling archive one day earlier recorded that
      `openspec archive` DELETED `.openspec.yaml` instead of moving it, and had
      to restore the dotfile by blob id. Under openspec **1.2.0** the dotfile
      MOVED with the packet: it is present at
      `openspec/changes/archive/2026-08-27-harden-ideation-readiness-check/.openspec.yaml`,
      `git status` shows the old path deleted and the archive folder added (a
      move, not a loss), and its content is blob
      `2d0f76051ae3ccb5d1dff1a4d6ddefd4d1071c03` with `cmp` reporting no
      difference against the pre-archive copy. No restoration was needed. The
      check was performed anyway, because an archived ad-hoc change whose origin
      declaration had silently vanished would fail the origin-retention
      requirement on its own terms.
      **THE ORIGIN-RETENTION GATE, STATED PRECISELY RATHER THAN WAVED
      THROUGH.** That blob `2d0f7605` is byte-identical to the blob at the
      proposing-and-ratifying commit `5c10ce6d` ("The blank pair was the honest
      signal, and Brett's admission is what clears it"), so `kind`, `id`,
      `reason`, `approved_by`, `approved_on` and `approval_note` are ALL
      unchanged from ratification — nothing in the realization or in this
      archive touched the declaration. The one earlier move is the admission
      itself (`a1453e0c` blob `3576c969` → `5c10ce6d` blob `2d0f7605`, +24/-15),
      which COMPLETED the two required fields that had deliberately stood blank;
      that is the case the origin requirement demands be filled, not a rewrite
      of provenance, and it happened at ratification rather than after it. The
      four decisions cleared on 2026-08-27 were recorded in `proposal.md`
      § Orchestrator decisions and NOT in `.openspec.yaml`, for exactly this
      reason: a veto clearance is not origin provenance.
      **PROMOTION VERIFIED BYTE-FOR-BYTE, which is the whole point of the act.**
      `openspec/specs/doc-health/spec.md` goes **29 → 32 requirements** and
      **124 → 133 scenarios** (+3 and +9, the delta's own counts), 1177 → 1289
      lines. The diff is **112 lines inserted and ZERO deleted**, all of them at
      the tail (`@@ -1177,0 +1178,112 @@`), so the twenty-nine pre-existing
      requirements are byte-identical after the act — proved, not eyeballed:
      `head -1177` of the new file `cmp`s clean against the whole file as it
      stood before. The promoted block equals the delta text EXACTLY: the
      delta's requirement body (its lines 5-115, everything below
      `## ADDED Requirements`) and canon's appended block (its lines 1178-1288)
      are both 111 lines and share one digest,
      `sha256:7c0c30927f7c20ad9299ab5533c6125fcae63fcf66c1cb7dcb31dba847b66fc8`,
      with `cmp` reporting no difference; the 112th inserted line is the file's
      trailing newline. The archived
      `specs/doc-health/spec.md` is itself byte-identical to the authored delta,
      so the record of what was promoted stays in the packet.
      **GATES AFTER THE ACT.** `OPENSPEC_TELEMETRY=0 openspec validate --all
      --strict` → **76 passed, 0 failed**, one fewer item than the 77 before,
      because this packet left the active set. Single-repo doc-health
      (`--single-repo . --as-of 2026-08-26`) before and after the archive:
      **5 critical / 7 error / 41 warning / 4 info** both times, family counts
      identical (`staged-topic-template` 27, `staged-candidate-aging` 15,
      `record-immutability` 5, `status-validity` 4, `location-conformance` 3,
      `ideation-routing` 2, `document-catalog` 1), and `proposal-origin`,
      `promotion-fidelity` and `release-inventory-drift` all **0 before and 0
      after**. THE ARCHIVE ADDS NO FINDING. The only line that moved in the
      whole report is the canon-share arithmetic — 30.2% → 30.3%, promoted-spec
      words 136345 → 137478 — which is the promotion itself showing up in the
      corpus ratio, and is the one difference an honest archive SHOULD produce.
      The `record-immutability` critical on `ideation/cross-reference.md` is
      PRE-EXISTING and contested, present on pristine `main` before this act and
      unchanged by it: § 3.4 re-rendered that record's line 9 as part of the
      repair, and the finding is the family noticing a record document changed
      after capture. It is named here rather than left for a reader to
      rediscover.
      **WHAT SURVIVES AS A FOLLOW-UP RATHER THAN AS A CLAIM — three items, and
      none of them is asserted anywhere in canon.** § 5.1, the Q3 collapse:
      RULED OPEN by Brett on 2026-08-27, so it crosses the archive unticked by
      decision, with the parametrized `RESOLVERS` guard standing in for the
      tidying. § 5.2, the governance rule that a `source_revision` recorded on a
      branch must be re-derived when that branch lands rewritten: NAMED AND NOT
      WRITTEN. § 5.3, `git_generation()` pinning `HEAD` regardless of a dirty
      tree: still there. The three promoted requirements speak only to resolving
      the repository under test, reading the index from committed state, and
      failing rather than skipping on an unreachable pin in a complete clone —
      they say nothing about a shared fixture, about how packets land, or about
      the generator, so the archive promotes no unearned claim.

## 5. Open — deliberately not closed by this change

- [ ] 5.1 Should the three `_openxfactory_root()` spellings collapse into one
      shared fixture? § 2 fixes all three in place. A single fixture would
      make the next such repair one edit instead of three, but it moves test
      infrastructure three unrelated modules depend on. Q3 in the proposal;
      no recommendation is offered, because the tidying and the defect are
      genuinely separable.
      **STILL OPEN after realization, and deliberately not taken.** The
      realizing session was asked to prefer the smallest change that satisfies
      the requirement rather than to decide Q3 unbidden, and did: three
      spellings, three edits, no shared fixture. What the realization DID add
      is a guard against the duplication rotting —
      `test_readiness_proof_resolution.py` parametrizes every resolver test
      over all three modules (`RESOLVERS`), so the copies cannot drift apart
      silently while the question waits for a ruling. That lowers the cost of
      leaving Q3 open; it does not answer it.
- [ ] 5.2 THE FOLLOW-UP PACKET, NAMED AND NOT WRITTEN: the governance rule
      that a `source_revision` recorded on a branch must be re-derived when
      that branch lands rewritten. `4e57009c` is a squash of
      `codex/brainstorm-packet-migration`, and the squash is what made both
      the generated pin (`da9bf3b7`) and the hand-bumped one (`f13a3b60`)
      unreachable. That rule binds every generator that records a revision,
      reaches into how packets land, and interacts with the house rule against
      squash merges — so it is a packet of its own, on its own evidence. This
      change only makes its absence loud.
- [ ] 5.3 Adjacent and also not this change: `git_generation()` in
      `scripts/bootstrap-ideation-cross-reference.py` pins `rev-parse HEAD`
      regardless of whether the working tree is clean, so an index can record
      a provenance claim about content no commit holds. Observed on the same
      morning in the shared checkout. Recorded here so the next person does
      not have to rediscover it.
