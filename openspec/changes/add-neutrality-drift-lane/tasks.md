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

- [ ] 3.1 Lane dry-run over the five domain factories from the pinned
      workspace: codexFactory (post-shed) yields no false-positive on
      the engineering core; a synthetic neutral-shaped fixture planted
      in a test workspace IS caught by stage 1 and drafted by stage 2.
- [ ] 3.2 One real nightly with the lane on: rolling PR carries the
      section (or a clean empty note), dispositions suppression proven
      by re-running against an unchanged rejected fixture.
      — First half EVIDENCED 2026-08-05 (not ticked; the suppression
      re-run remains): xFactory dispatch run 31001274147 — the first
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
