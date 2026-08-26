# Tasks: harden-ideation-readiness-check

NO IMPLEMENTATION here is discharged. This packet is a PROPOSAL: it carries the
delta, the measurement, and the plan, and it changes no code. § 1.1 and § 1.2
ARE discharged — Brett admitted the packet on 2026-08-26 — and § 1.3 is not:
Q1, Q2, Q3 and the four flagged decisions all stand open, uncovered by the
admission.

**§ 5 is deliberately OPEN and stays open.** Two adjacent gaps are recorded
there rather than implied, and one of them is the follow-up packet the
proposal declines to write.

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
- [ ] 1.3 Rule the four decisions in `proposal.md` § Orchestrator decisions and
      the three questions Q1–Q3. Q1 (keep the narrowed skip) and Q2 (re-pin
      target) both change work below if reversed; Q3 changes only § 5.1.

## 2. Implementation — the three requirements

- [ ] 2.1 `tests/doc-health/test_ideation_readiness.py`: replace
      `_openxfactory_root()`'s bare ancestor walk with the resolution order
      `design.md` § 1 records — repository under test first, then an explicit
      argument, then `OPENXFACTORY_ROOT`, then the walk. When any step past
      the first is taken, the run says which checkout it resolved and why.
      Four call sites move with it: `:386`, `:556`, `:568`, `:934`.
- [ ] 2.2 The same helper is spelled twice more —
      `tests/doc-health/test_derive_possibles.py:29` and
      `tests/doc-health/test_readiness_dispatch.py:318`. Both move with 2.1.
      Leaving either behind leaves the hazard live in a module that will be
      trusted because its sibling was fixed.
- [ ] 2.3 `scripts/doc_health/ideation_readiness.py`: `find_index_validator()`
      at `:682-692` carries the identical walk and today resolves the SHARED
      checkout's validator from any worktree — measured 2026-08-26. Give it
      the same resolution order. The module already carries that order at
      `:1067-1077` for the renderer; this is the second use of an existing
      shape, not a new one.
- [ ] 2.4 `test_derivation_reproduces_the_real_bootstrap_clusters`: read the
      index with `git show <ref>:ideation/cross-reference.yaml` at `HEAD` of
      the repository under test instead of `(openx / "ideation" /
      "cross-reference.yaml").read_text()`, and name the revision read in the
      failure message. The corpus side already reads at the index's own pin
      and does not move.
- [ ] 2.5 Replace the unconditional `pytest.skip` at `:396-398` with the
      discrimination `design.md` § 3 records: on `git archive` failure, ask
      `git rev-parse --is-shallow-repository` and `git cat-file -e
      <rev>^{commit}`. Complete clone plus absent object → FAIL, naming the
      pin and the index file that carries it. Truncated history → skip, with a
      reason naming the truncation observed. Never the current conjecture.
- [ ] 2.6 Regression tests for all three requirements, each pinned to the
      defect rather than to the fix:
      - a run whose repository under test carries its own index resolves to
        it even when an ancestor checkout also carries one;
      - a fixture repository whose working-tree index differs from its
        committed index yields the committed verdict;
      - an index pinning an absent revision in a complete fixture clone FAILS,
        and the same fixture made shallow SKIPS with the distinguishing
        reason;
      - a mutation check in the style of
        `test_mutation_reverting_parse_header_alone_reproduces_the_f5_divergence`:
        reverting the resolver alone must reproduce the foreign-checkout
        resolution, proving the new tests are pinned to defect A and not
        merely passing.

## 3. Repair of the current defect instance

- [ ] 3.1 Re-pin `ideation/cross-reference.yaml`'s
      `generation.source_revision` from `f13a3b6007736292e1e157febef1ac733e534de9`
      to `4e57009c0a1aed9bdbe3c0f6cc5ca948e15ec8cc`, subject to Q2's ruling.
      ONE LINE. No regeneration of the body is owed: the derivation reproduces
      the committed 290-entry skeleton exactly at `da9bf3b7`, at `4e57009c`,
      and at `origin/main` alike (`proposal.md` § What was measured).
- [ ] 3.2 Verify the repair the way the requirement will: in a scratch
      `git clone --bare --no-local` of the repository, `git cat-file -t
      4e57009c` must succeed where `f13a3b60` fails today, and
      `git archive 4e57009c ideation` must return 0.
- [ ] 3.3 Re-run `scripts/validate-ideation-cross-reference.py` over the
      repaired index. The pin edit must not disturb schema validity, and the
      validator is the thing that says so.
- [ ] 3.4 `ideation/cross-reference.md` MOVES WITH THE PIN — verified
      2026-08-26, and the first draft of this task said the opposite. The
      rendered projection carries `- Source revision:
      \`f13a3b6007736292e1e157febef1ac733e534de9\`` at line 9, so re-pinning
      the yaml without re-rendering the md would leave the two artifacts
      disagreeing about the same fact. Regenerate the md through
      `scripts/render-ideation-cross-reference.py` — the pin line is the only
      line expected to move, and if any other line moves, that is a finding
      about the repair rather than something to commit past.

## 4. Verification

- [ ] 4.1 `python3 -m pytest tests/doc-health -q` green. Baseline on
      `origin/main` at `31c931fa`, measured 2026-08-26 in a scratch worktree:
      **1 failed, 895 passed** — the single failure is the test this change
      repairs, and it is defect A in flight.
- [ ] 4.2 `OPENSPEC_TELEMETRY=0 openspec validate harden-ideation-readiness-check --strict`
      and `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` both green.
- [ ] 4.3 THE GATE THAT MATTERS: run the readiness proof in a FRESH CLONE —
      `git clone --bare --no-local` plus a working tree, or a scratch
      `git clone` of the remote — and confirm it PASSES rather than skips.
      This assertion has never been executed in a fresh clone; 4.3 is the
      first time. If it fails there for a reason unrelated to these three
      requirements, that finding belongs to this change and is reported, not
      suppressed.
- [ ] 4.4 Confirm the proof is now indifferent to a concurrent edit: with an
      uncommitted change to `ideation/cross-reference.yaml` present in the
      shared checkout, the worktree run must return the same verdict it
      returns with the shared checkout clean.
- [ ] 4.5 A single-repo doc-health run whose severity counts move by exactly
      what this change predicts — which is by nothing, except the two
      `proposal-origin` ERRORS that § 1.1 explains and § 1.2 clears.
- [ ] 4.6 ARCHIVE AFTER REALIZATION. This change ships ACTIVE and archives
      only on merged-plus-green plus 4.3, following
      `add-family-enumeration-check` and `add-duplicate-packet-check`. The
      archive act is its own commit after the merge.

## 5. Open — deliberately not closed by this change

- [ ] 5.1 Should the three `_openxfactory_root()` spellings collapse into one
      shared fixture? § 2 fixes all three in place. A single fixture would
      make the next such repair one edit instead of three, but it moves test
      infrastructure three unrelated modules depend on. Q3 in the proposal;
      no recommendation is offered, because the tidying and the defect are
      genuinely separable.
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
