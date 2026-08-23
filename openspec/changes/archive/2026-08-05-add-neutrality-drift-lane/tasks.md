# Tasks: add-neutrality-drift-lane

## 1. Lane implementation (openxFactory, after ratification)

- [x] 1.1 `scripts/doc_health/neutrality.py`: stage-1 deterministic
      pre-filter — near-duplicate similarity vs the openxFactory tree
      (generalize the contract-copy-drift machinery), domain-lexicon
      absence for schemas/scripts (each factory's ontology/term
      registry as the lexicon source), cross-repo consumer detection,
      stack.yaml-uninventoried tooling mass; per-repo incremental
      state (changed-since-last-run) with a recorded baseline marker.
- [x] 1.2 `scripts/doc_health/neutrality-prompt.md`: the versioned
      prompt contract — the sweep rubric ("would another domain need
      this essentially unchanged?"), required structured output
      (paths, neutrality evidence, counter-evidence, domain-local
      exclusions, suggested decision promote/split), refusal rules
      (no judgment from location alone; frozen records excluded).
- [x] 1.3 `scripts/doc_health/neutrality_dispatch.py`: bounded batch
      dispatch over stage-1 survivors + changed content, structured
      output validation, register-seed drafting (row + detail section
      in the register's format), ranked-plan items, dispositions
      suppression keyed (repo, path, content digest).
- [x] 1.4 Reusable workflow: `neutrality-drift` opt-out input (default
      on) + `neutrality-baseline` manual full-sweep input; runner.py
      wiring beside the organizer/cataloger lanes.
- [x] 1.5 Tests under `tests/doc-health/`: pre-filter signal fixtures
      (one per signal class), dispatch selection/suppression, seed
      drafting format (validates against the register's row/section
      shape), authority boundary (the lane's write surface is the
      rolling-PR content + its state file, nothing else).
- [x] 1.6 Record the codexFactory 2026-08-03 manual sweep as that
      repo's baseline marker so the lane starts incremental there.

## 2. Docs and register

- [x] 2.1 `docs/doc-health.md`: lane section (families/lanes table row,
      approval flow, dispositions keying).
- [x] 2.2 `docs/domain-to-neutral-promotion-process.md`: note the lane
      as a register intake path (machine-drafted seeds, human-approved).
- [x] 2.3 README doc-index + OpenSpec Records entry.

## 3. Verification

- [x] 3.1 Lane dry-run over the five domain factories from the pinned
      workspace: codexFactory (post-shed) yields no false-positive on
      the engineering core; a synthetic neutral-shaped fixture planted
      in a test workspace IS caught by stage 1 and drafted by stage 2.
      — Done 2026-08-05 (Brett-delegated takeover;
      `evidence/dry-run-2026-08-05.md`): fresh pinned-workspace sweep
      over all eight xFactories repos; codexFactory audited at post-shed
      main `f4d6963` (the aggregation pin `c617c31` PRE-dates the sheds —
      flagged for a routine pointer sync) — the real claude-CLI scout
      judged all four engineering-core docs and the ontology content
      domain-local, drafting only one evidence-sound `split` seed for the
      starter-scaffolded ontology README: no core false positive. The
      zephyrFactory synthetic fixtures (copied openxFactory schema +
      validator) were caught by stage 1 (near_duplicate + lexicon_absence
      + uninventoried_tooling) and BOTH drafted `promote` by the real
      stage-2 scout, format-valid seeds retained under evidence/.
- [x] 3.2 One real nightly with the lane on: rolling PR carries the
      section (or a clean empty note), dispositions suppression proven
      by re-running against an unchanged rejected fixture.
      — COMPLETE 2026-08-05: suppression second half proven
      (`evidence/dry-run-2026-08-05.md`): the rejected zephyrFactory
      fixture (disposition keyed repo + path + content_sha256
      `9831a3ba…`, non-empty cite) was counted `suppressed=1` on an
      unchanged re-run through the full merge primitive with fresh state
      and never re-dispatched or re-drafted; digest-keying proven both
      directions (one appended line re-files it). First half evidenced
      earlier the same day: xFactory dispatch run 31001274147 — the first
      nightly to complete since the lane landed — carries the full
      `## Neutrality Drift` section in the rolling PR's 2026-08-05
      report: stage 1 scanned 2128 files across the domain repos (263
      candidates; codexFactory=190), selection dispatched 8 with 230
      carried over, and the model scout recorded the graceful
      `worker_unavailable` skip with drafted seeds none. (The two
      preceding nightlies never reached the lane: openxFactory Actions
      access `none` blocked the repointed caller's compile, and the
      factory App lacked HealthLinc/MedxEHR/openAvatar grants — both
      fixed 2026-08-05, see adopt-neutral-tooling-home 5.2.)

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` real line 5 was respelled `Ratified by:` to `Ratified:` by slice
5B of `govern-openspec-corpus-membership` — the prefix only. Every byte after
the colon is carried verbatim, asserted identical at the edit, so the original
line is recovered exactly by reading `Ratified by:` back in its place and
nothing else on the page moved. The ruling is OQ-4's RULED extension of
2026-08-23 (Brett Heap, in-session), which widens the class to the sixteen
lines whose named change id is the DOCUMENT'S OWN. A change is not its own
approving change, and such a line passed `fam_ratified_provenance` only by
self-reference. This one emitted NO finding, so the respell is corrective
rather than a discharge and clears nothing from the census. The record that
justifies this line is Brett's approval of 2026-08-04 named on the line (PR
#64 review), recorded by commit `5a4747c` of that same 2026-08-04, "Record
Brett's 2026-08-04 ratification of add-neutrality-drift-lane". An append on a
single-valued header is mechanically impossible —
`doc_health.corpus.STATUS_RE` swallows any trailing annotation — so this is an
in-place overwrite and an extension of Brett's 2026-08-10 append ruling, named
as one, and it is entered in `docs/archive-record-discrepancies.md`.
