# Tasks: add-shared-identity-seeds

## 1. The detector and drafter

- [x] 1.1 `shared_identities(documents, repositories=, minimum=, exactly=)`:
      identities carried by two or more of a member set, optionally exactly a
      named carrier combination; widest convergence first; malformed rows
      dropped; empty is an honest answer.
- [x] 1.2 `draft_seed(register_text, rows, project=, as_of=)`: the register's
      row + `### DTN-NNN:` section, numbered by `next_dtn_id`, quoting the
      candidate rule, listing carriers as evidence, and carrying the
      shared-path-is-not-a-shared-contract exclusion. Deterministic.
- [x] 1.3 `REGISTER_PATH` mirrored from `families` and pinned equal by test.

## 2. The route

- [x] 2.1 Loopback-only drafting route; recomputes carriers from the serve's
      own composed view; refuses an unknown/uncomposable project; writes
      nothing.

## 3. The affordance

- [x] 3.1 The repository lens's drill-in rows offer "draft DTN seed" for
      convergent regions, disabled with a reason on single-carrier rows.
- [x] 3.2 The drafted seed renders read-only with a copy control and states
      where it must be merged and that nothing was written.

## 4. Verification

- [x] 4.1 Detector tests: subset scoping, exact-combination narrowing, the
      widest-first order, malformed and empty inputs.
- [x] 4.2 Drafter tests: six-cell row grammar, seed status/priority, heading
      shape, quoted rule, carrier evidence, determinism, empty refusal,
      numbering with and without a register.
- [x] 4.3 Wire tests: bad requests, the uncomposable-plane refusal, and that
      the checkout is byte-for-byte unchanged after a call.
- [x] 4.4 Live browser check on the real multi-repository plane.
      (Verified 2026-08-07, project `domains`: the drill-in rows offered
      "draft DTN seed", enabled on the three convergent regions and disabled
      with its reason on all five single-carrier rows. Drafting from the
      3-carrier sector returned DTN-025 —
      "Shared across 3 factories: docs/credentialing.md" with that one
      identity as evidence, matching the row's own "1 doc" after the
      exact-combination fix the first run exposed. The panel states nothing
      was written and where to merge; the checkout was unchanged. Zero
      console errors, page errors, and >=400 responses.)
- [x] 4.5 Brett merges the first drafted seed into the register.
      (Ruled and merged 2026-08-26 — Brett ruled in-session to merge the
      first drafted seed; DTN-025 admitted to the register.)

## 5. Successor (not this change)

- [ ] 5.1 Promote the detector to a fifth neutrality-drift stage-1 signal so
      the nightly lane files these seeds unattended.
