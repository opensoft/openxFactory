# Tasks: add-lens-gate-verbs

## 1. Gate routes (codexFactory)

- [x] 1.1 `gate_routes.py`: `lens-save-recipe` and `lens-add-as-cluster`
      beside dispose/ratify/propose — same human-only enforcement, same
      refusal/record mechanics; thin glue into `lens.py` / `workbench.py` /
      `human_seen.py` with NO engine changes.
- [x] 1.2 Refusal surface: reasonless override, duplicate set name, missing
      evidence contract, validation failure — each refuses with the
      engine's reason, persists nothing, prior state intact.
- [x] 1.3 `cli.py` parity verbs (the propose precedent).

## 2. Lens plan panel (codexFactory)

- [x] 2.1 `views/lens.js`: capability-gated execute affordance on the plan
      confirmation, posting the confirmed plan to the verb route; gate-off
      renders plan-only exactly as today (deployed static image unchanged).
- [x] 2.2 On success, render the landing confirmation (manifest path,
      pending-entry id, gate-action record) — on refusal, the engine's
      reason verbatim.

## 3. Verification

- [x] 3.1 Route tests: both verbs land their artifacts (manifest;
      manifest + pending_review entry) with gate-action records; index
      file untouched; every refusal case; agent path rejected; gate-off
      posture.
- [x] 3.2 Full dashboard suite green; Playwright smoke: build a set in the
      lens, execute save-recipe, see the landing confirmation; add-as-cluster
      lands the pending entry; zero page errors.
- [x] 3.3 Brett's dogfood pass: build a real set, land it, and find the
      manifest + pending entry where the confirmation said they would be.
      — DISCHARGED by disposition, ruled by Brett 2026-08-06 (decision
      round): the 3.1 route tests (both verbs' artifacts, every refusal
      case, agent-path rejection, gate-off posture) plus the 3.2
      Playwright smoke (the exact dogfood scenario — build a set, execute
      save-recipe, landing confirmation, add-as-cluster lands the
      pending_review entry, zero page errors) plus Brett's real
      wheel-verbs 4.4 human pass on the same gate console engine
      (2026-08-05, archived add-wheel-action-verbs) are accepted as
      sufficient realization evidence; Brett's first real lens set in
      ordinary dashboard work stands as retroactive confirmation, with
      any mismatch filed as an ordinary defect against the promoted
      capability.

## Bookkeeping correction (2026-09-11, `split-opendox-two-layer-product` § 5.9) — carry-forward

Edited (bookkeeping): 2026-09-11 by split-opendox-two-layer-product — carry-forward annotation

This packet's `specs/ideation-dashboard/spec.md` delta stays the record, unedited and unaugmented by anything below. The `ideation-dashboard` capability's artifacts — the `scripts/ideation_dashboard/` tree, `web/`, `tests/ideation-dashboard/`, the packaged examples under `examples/ideation-dashboard/`, the five dashboard governance docs, and the five dashboard contract schemas — were SHED from `openxFactory` by `split-opendox-two-layer-product` § 5.2, `opensoft/openxFactory` PR #940 → `cc4ae9d35b2dbd56743c8c19699fd685d4e49343` (merged 2026-09-11). They are now consumed at a pin from the `openDox`/`openXdox` legs per `docs/opendox-carve-manifest.yaml` (destinations `opendox_spec`, `opendox_code`, `openxdox_spec`, `openxdox_code`; `contracts/opendox-pin.yaml`, `contracts/openxdox-pin.yaml`). The five contract schemas this delta names — `gate-action-record`, `ideation-dashboard-snapshot-index`, `ideation-dashboard-snapshot`, `xfactory-workbench-chat-turn`, `xfactory-workbench-model-catalog` — were DEPRECATED at `contract-v3.7` (`opensoft/openxFactory` PR #970 → `45bd9ee250ad1125f9227ad511bee0fec2b16306`, tag `ec3c17292c6dc2ca6004d158d6cc26bf5e6523e2`, merged 2026-09-11) and LEAVE the bundle at `contract-v4.0` (§ 5.7; cut PR `TBD-CUT-PR`, a placeholder the landing lane fills in when the cut lands). Ruled by Brett Heap, 2026-09-11 20:27Z, session `openXfactory-4 (5)`, on `opensoft/openxFactory`#656 comment `5640246046` (§ 5.9), realizing `split-opendox-two-layer-product` `tasks.md` § 5.9 — "ANNOTATE the 30 archived changes carrying an `ideation-dashboard` delta with the carry-forward." Nothing this packet asserts is changed by this annotation; immutable records are annotated, never edited into agreement.
