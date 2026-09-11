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
      the nightly lane files these seeds unattended. THE NAMED SUCCESSOR, and
      the successor is named rather than gestured at: a fifth entry in
      `scripts/doc_health/neutrality.py`'s `SIGNAL_NAMES` — today exactly
      `("near_duplicate", "lexicon_absence", "cross_repo_consumer",
      "uninventoried_tooling")`, four — carrying `shared_identity` alongside
      them, so `neutrality_dispatch.py`'s nightly prepare/merge lane files
      these seeds with no human opening the dashboard. It is out of scope
      here and does not land with this change; the proposal's Impact section
      says so in its own words ("This change deliberately ships the
      human-driven path first, because the lens is where the question is
      already being asked"). Listed for traceability only.
      STILL A RECORDED BOUNDARY AT ARCHIVE, not an open gap. This box stays
      unticked deliberately, the same way `add-roster-device-admission-surface`
      archived its §6 unticked and `refine-demote-round-trip-mechanics` its §8
      by ruling: an unticked box here means "OWNED ELSEWHERE", and ticking it
      would claim work this change never did. Measured at archive against
      `origin/main` `42662b70`: `SIGNAL_NAMES` still carries four names, so
      the successor is genuinely unbuilt and no active change proposes it.

## Bookkeeping correction (2026-09-11, `split-opendox-two-layer-product` § 5.9) — carry-forward

Edited (bookkeeping): 2026-09-11 by split-opendox-two-layer-product — carry-forward annotation

This packet's `specs/ideation-dashboard/spec.md` delta stays the record, unedited and unaugmented by anything below. The `ideation-dashboard` capability's artifacts — the `scripts/ideation_dashboard/` tree, `web/`, `tests/ideation-dashboard/`, the packaged examples under `examples/ideation-dashboard/`, the five dashboard governance docs, and the five dashboard contract schemas — were SHED from `openxFactory` by `split-opendox-two-layer-product` § 5.2, `opensoft/openxFactory` PR #940 → `cc4ae9d35b2dbd56743c8c19699fd685d4e49343` (merged 2026-09-11). They are now consumed at a pin from the `openDox`/`openXdox` legs per `docs/opendox-carve-manifest.yaml` (destinations `opendox_spec`, `opendox_code`, `openxdox_spec`, `openxdox_code`; `contracts/opendox-pin.yaml`, `contracts/openxdox-pin.yaml`). The five contract schemas this delta names — `gate-action-record`, `ideation-dashboard-snapshot-index`, `ideation-dashboard-snapshot`, `xfactory-workbench-chat-turn`, `xfactory-workbench-model-catalog` — were DEPRECATED at `contract-v3.7` (`opensoft/openxFactory` PR #970 → `45bd9ee250ad1125f9227ad511bee0fec2b16306`, tag `ec3c17292c6dc2ca6004d158d6cc26bf5e6523e2`, merged 2026-09-11) and LEAVE the bundle at `contract-v4.0` (§ 5.7; cut PR `TBD-CUT-PR`, a placeholder the landing lane fills in when the cut lands). Ruled by Brett Heap, 2026-09-11 20:27Z, session `openXfactory-4 (5)`, on `opensoft/openxFactory`#656 comment `5640246046` (§ 5.9), realizing `split-opendox-two-layer-product` `tasks.md` § 5.9 — "ANNOTATE the 30 archived changes carrying an `ideation-dashboard` delta with the carry-forward." Nothing this packet asserts is changed by this annotation; immutable records are annotated, never edited into agreement.
