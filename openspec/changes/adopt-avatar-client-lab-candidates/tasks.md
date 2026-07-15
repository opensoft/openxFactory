# Tasks: adopt-avatar-client-lab-candidates

Source candidates: codexFactory `specs/002-avatar-client-lab/upstream-drafts/`
@ `3a8fbd5` (7/7 panel-confirmed; provenance in that folder's STATUS.md).
Land verbatim apart from the status-header swap (design D6); upstream
validators are the authoritative gate. Shared-checkout discipline: explicit
paths only; check `git status -sb` before every commit.

## 1. Preflight

- [x] 1.1 Verify the source commit: fetch codexFactory, confirm `3a8fbd5` is an ancestor of `origin/002-avatar-client-lab` (or of main once its PR merges), and record the exact source SHA in this change's notes.
- [x] 1.2 Baseline validation run: `validate-avatar-client.py` + `validate-avatar-first-ui.py --mode baseline` + `--mode realization` green BEFORE any landing (establishes that later failures are ours).
- [x] 1.3 Confirm no concurrent change touches `contracts/` or `examples/avatar-first-ui/` (`openspec list` + `git log --oneline -10 -- contracts examples`); note findings.

## 2. Fixture families (P7, P8, P11, P12/P13)

- [x] 2.1 Land the P7 intake-set (5 fixtures) into `examples/avatar-first-ui/fixtures/deterministic/` with the D6 header swap; re-run the baseline validator harness green.
- [x] 2.2 Land the P8 takeover/recovery set (4 fixtures) the same way; confirm the event-count revision arithmetic and the `command_rejected`/`second_instance_denied` epoch-fence vocabulary land byte-verbatim from source.
- [x] 2.3 Land the P11 `interrupted`/`handoff` pair (2 fixtures).
- [x] 2.4 Land the P12/P13 media-states set (9 fixtures: eight non-control closed `media.states` + `control_degraded`), verifying each evidences its denominator state via AVC-12 kernel fields only.
- [x] 2.5 Wire acceptance-map/evidence-register rows additively where a landed fixture discharges or newly evidences a scenario; any released `deferred` discharge goes through a successor-register entry only (locked decision 7); evidence-id parity green.

## 3. P10 — capability-scenario register (owning task per escalation memo)

- [x] 3.1 Land `contracts/avatar-client-lab/capability-scenario-register.yaml` (Option B, design D2) from the candidate; verify 9 requirements / 22 scenarios, titles byte-matched against the `implement-avatar-client-lab` capability spec delta in document order.
- [x] 3.2 Add the register fidelity check to `scripts/validate-avatar-client.py` (mirrors `check_client_lab_acceptance_map`; fail-closed; re-verifies against the promoted spec path after that change archives) + negative coverage (renamed title, dropped scenario, reordered entry each fail).

## 4. P1 — avatar-state derivation table (owning task per escalation memo)

- [x] 4.1 Ratify OQ-1..OQ-6 from the candidate's §8 against cited sources (standard §15, avatar-client-runtime spec, data-model §6/§7, the landed seeds); record each ratification (citation or replacement) in the table's prose; product-owner sign-off recorded before proceeding. [GATE]
- [x] 4.2 Land `contracts/avatar-client-lab/avatar-state-derivation-table.md` + `.yaml` with ratifications applied; add the §15 pointer line to `docs/avatar-first-ui-standard.md` (pointer only — the standard's text otherwise unchanged).
- [x] 4.3 Add `check_avatar_state_derivation_table` to `scripts/validate-avatar-client.py`: outputs == six states; `media_states` == closed ten; every landed deterministic seed resolves to its stated avatar state; named reachability combinations are exactly the gate (ix)(a) set; invariant-contradiction rows fail closed. Negative coverage included.

## 5. Release cut — contract-v1.12

- [x] 5.1 Re-run task 1.3's collision check; then register in `contracts/manifest.yaml` with computed sha256: the two client-lab artifacts, the 20 adopted fixtures, and `evidence-register.implement-avatar-client-lab.yaml` (the task-4.4 release-time registration that makes the SCO-001-S05 discharge effective).
- [x] 5.2 Verify every `contract-v1.7` / `contract-v1.8` released file is byte-identical (digest re-computation), write the changelog entry, bump `contract_bundle_version` to `contract-v1.12`, tag. — tag applied by coordinator at merge (a branch-commit tag would point at the wrong object; the annotated `contract-v1.12` tag lands on the main merge commit after review).
- [x] 5.3 Full validation sweep: `validate-avatar-client.py` (incl. both new checks + successor-register manifest membership under `--require-realization`) + `validate-avatar-first-ui.py` baseline + realization, all green.
- [x] 5.4 List this change in the openxFactory README "OpenSpec Records" block; `openspec validate adopt-avatar-client-lab-candidates --strict` + `--all --strict` green; commit + push per shared-checkout discipline.

## 6. Realization (code surface: codexFactory lab pin resync)

- [ ] 6.1 In codexFactory `apps/avatar-client-lab/`: run `sync_contracts.dart` against the `contract-v1.12` checkout; vendor the new artifacts; pin the register + derivation table as `vendored_evidence_inputs`; retire the interim P10 checklist + faithfulness guard (contract-pin.md rule 5); un-skip the two BLOCKED-on-P8 assertions in `p8_takeover_recovery_replay_test.dart`.
- [ ] 6.2 Wire gate (vi) to test `deriveAvatarState` against the vendored table and resolve the gate (ix)(a) combination half from the table's named combinations (retiring the interim-invariant scoping); `dart run melos run ci` — nine gates green.
- [ ] 6.3 Record realization evidence (resynced pin refs, green gate run) on this change; update the P-ledger rows (P1, P7, P8, P10, P11, P12, P13 → landed) in the 002 feature's plan.md via the codexFactory session that owns it.
- [ ] 6.4 Notify/unblock `implement-avatar-client-lab` §9 (its 9.3 pin-resync is satisfied by 6.1; its 4.4 manifest registration satisfied by 5.1); archive THIS change per release-realization once 6.2's green run is recorded.
