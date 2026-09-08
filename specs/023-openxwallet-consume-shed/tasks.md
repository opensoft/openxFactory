# Tasks: openxFactory consumes openXwallet and sheds the wallet paths (P3)

**Feature**: `023-openxwallet-consume-shed` · **Branch**: `023-openxwallet-consume-shed`

**Realizes**: `openspec/changes/split-openxwallet-repo` `tasks.md` §7 (7.1–7.33).
Each task below names the §7 item it discharges. Where §7 marks an item
**[OPERATOR]**, this file records what was prepared and leaves the act open.

## Phase 1: Reachability (fail-fast, before anything is written)

- [X] T001 Read how `.github/workflows/doc-health-reusable.yml` mints its App
      token (`:140-158`) and establish whether an openxFactory workflow can reach
      the private `opensoft/openXwallet`. **Result:** the org secret
      `XFACTORY_APP_ID` is visibility-`selected` and openxFactory is NOT one of
      its two repositories; this repository holds `OPENXFACTORY_APP_ID` /
      `OPENXFACTORY_APP_PRIVATE_KEY` for App `4253636`, installation
      `145372182`, `repository_selection: all`. The pattern is adopted, the
      secret names corrected. `research.md` R1.
- [X] T002 Confirm no installation edit is needed and record the decision NOT to
      issue one. `evidence/operator-acts.md`.
- [X] T003 Verify `wallet-v1.1` resolves to commit
      `63f5a1adac89f017e70bab9a4ffe7cf02d6e6705` through the annotated tag
      object, and that the eight digests at that tag equal the eight in
      `contracts/manifest.yaml`. `research.md` R2.

## Phase 2: The pin and its verifier (§7.2–7.7)

- [X] T004 §7.2 `git submodule add git@github.com:opensoft/openXwallet.git
      openXwallet`, recorded at `63f5a1ad…`; `.gitmodules` keeps `git@github.com:`
      because openXwallet is PRIVATE and an HTTPS URL only moves which credential
      helper needs a token while making every human clone prompt.
      `git -C openXwallet describe --tags` = `wallet-v1.1`.
- [X] T005 §7.3, §7.4 `contracts/openxwallet-pin.yaml`: `kind:
      pinned_contract_manifest` unchanged, `submodule_path: openXwallet`,
      `carve_commit: 30565e48…`, `revision_kind: commit`, eight `files:` with
      `sha256`, six `pinned_by_commit_only:` paths, `contract_bundle_tag:
      wallet-v1.1` as a LABEL. `verify_pin:` names the verifier, matching the
      sibling pin's own convention (clarification N3).
- [X] T006 §7.5, §7.6 `scripts/verify-openxwallet-pin.py`: six ordered checks;
      exit 2 with `pin-submodule-uninitialized`, `pin-gitlink-mismatch`,
      `pin-checkout-mismatch`, `pin-digest-mismatch`, `pin-member-missing`,
      `pin-tag-only`; one fixed remediation trailer on every refusal.
- [X] T007 §7.7 `--aggregation-root <path>` mode: the root-gitlink-equals-nested
      check P4 invokes, one implementation and one refusal vocabulary.
- [X] T008 `tests/openxwallet_pin/test_verify_pin.py` — 35 cases, all six codes
      reproduced hermetically, zero skips.

## Phase 3: The trust-anchor repoint (§7.8–7.10) — why the PR is atomic

- [X] T009 §7.8 `OPENXWALLET_REGISTRY_PATH` rebased to
      `ROOT/"openXwallet"/"contracts"/"openxwallet"/"openxwallet-custody.registry.yaml"`,
      module scope, plain `Path`, pure string join, NO I/O — two test modules
      resolve it at setup and an import-time failure would kill collection.
- [X] T010 §7.9 the bare file-absent exit replaced inside `main()` by the
      verifier's call; the verifier is loaded lazily; a verifier that will not
      load is itself a refusal, never a fallback to presence.
- [X] T011 §7.10 `tests/trust-anchor/test_openxwallet_pin_refusal.py` — the
      uninitialized-submodule and digest-disagreement refusals by NAMED CODE,
      plus the verifier-unloadable case, the literal-vs-`submodule_path`
      agreement check, and an import-with-nothing-on-disk probe.

## Phase 4: The gates (§7.12–7.19)

- [X] T012 §7.12, §7.13 `.github/workflows/openxwallet-consumer-gate.yml`
      replacing `wallet-validation.yml`, `jobs: wallet-validation:` RETAINED.
      Steps: app token → `insteadOf` → checkout → scoped
      `git submodule update --init openXwallet` → verify pin → pinned syntax gate
      → pinned validator (`| tee wallet-gate.log`, `shell: bash` for pipefail) →
      the POSITIVE register assertion.
- [X] T013 §7.14 `tests/openxwallet_consumer_gate/test_gate_invocation.py` — job
      id, the exact invocation, no `--strict`, pipefail, step ORDER, scoped init,
      no blanket `submodules:`, and that the retired file is gone.
- [X] T014 §7.15 the register assertion is the POSITIVE conjunction: `repo scan:`
      note AND `intake register read:` NOTE AND neither
      `no intake register at this tree` nor any `[register-*]` code.
- [X] T015 §7.16 `pytest-suite.yml` gains the app token, the `insteadOf` rewrite
      and the scoped init. `submodules: true` deliberately NOT used.
- [X] T016 §7.17 the pinned header count becomes a pinned TRIPLE — selected,
      passed, SKIPPED — read from the JUnit XML `<testsuite>` attributes, with
      failures and errors required to be zero.
- [X] T017 §7.18 the three `wallet-validation.yml` references renamed.
- [X] T018 §7.19 BOTH `doc-health-reusable.yml` init filters gain a second
      scoped init for the NESTED gitlink (`git -C openxFactory submodule update
      --init openXwallet`), guarded on the nested `.gitmodules` declaring it so it
      is inert until P4 bumps the aggregation's pin. NOT `--recursive`.

## Phase 5: The shed (§7.11)

- [X] T019 §7.11 delete nine of the twelve carved path sets — 92 files, which is
      the carve's 100 minus the three deliberate exceptions' 8.
- [X] T020 §7.11 the three exceptions left in place: `openspec/specs/openxwallet/`
      and `openspec/specs/openxwallet-agent-profile/` (emptied by `openspec
      archive` applying the ratified REMOVED deltas, not here) and
      `openspec/changes/archive/2026-08-08-add-openxwallet/` (a record, ANNOTATED).
- [X] T021 §7.27 assert `governance/review-authority/` is untouched — all four
      files, verified by `git diff --stat` over that path being empty.

## Phase 6: The MAJOR (§7.20, §7.21)

- [X] T022 §7.20 `contracts/manifest.yaml`: the eight rows and their family
      header comment deleted and replaced by a comment pointing at the pin; the
      SEVEN incoming citations REWORDED to the pin, never deleted, because the
      precedent each cites still holds; `contract_bundle_version: contract-v2.0`.
- [X] T023 §7.21 `contracts/CHANGELOG.md` MAJOR entry discharging all three
      `:250-254` clauses explicitly; `contracts/README.md` three rows → one
      "consumed at pin" row plus two trust-anchor rows repointed;
      `contracts/releases/contract-v2.0.digests.yaml` built by
      `validate-contract-release.py build` (192 entries, byte-reproducible).
- [X] T024 `docs/contract-versioning-policy.md`: the openxWallet deprecation
      moves from "Currently In Force" to a new "Deprecations Executed" section —
      recorded, not deleted, because a consumer upgrading ACROSS the removal
      needs the migration path readable at the version it upgrades to.

## Phase 7: The documents (§7.22–7.25)

- [X] T025 §7.22 `README.md` at every wallet-bearing range: the gate section
      rewritten for the consumer gate and the pinned readers, the contract index
      entry marked CONSUMED AT PIN, the trust-anchor citations repointed, the
      STALE "advisory until an operator marks it required" corrected, the S1
      successor sentence put in the past tense with the successor named, and the
      active-change ledger given a realization note.
- [X] T026 §7.22 the `add-openxwallet` archive-ledger entry ANNOTATED, never
      rewritten.
- [X] T027 §7.23 `.github/CODEOWNERS`: the two departing validator lines dropped;
      `/contracts/openxwallet-pin.yaml`, `/scripts/verify-openxwallet-pin.py`,
      `/openXwallet` and `/.gitmodules` added.
- [X] T028 §7.24 `docs/archive-record-discrepancies.md` row 7 gains the
      "carried to openXwallet" NOTE.
- [X] T029 §7.25 `add-wallet-carried-review-authority/tasks.md`: five
      live-change edits, plus an addendum recording that task 2.6's red-proof is
      RETARGETED at the consumer gate and that S3/S5's `openxwallet` /
      `openxwallet-agent-profile` core deltas are authored in openXwallet from
      here on. Its `tasks.md` 8.1 ruling is unchanged, as ratified.
- [X] T030 The prose-only citations reworded to the pin and NOT deleted:
      `scripts/validate-identity-brokering.py` (two docstring sites; the runtime
      finding STRING is deliberately not edited — it is machine-visible surface
      under R2, and a comment above it records why), `scripts/proposal-support.py`
      staged-origin comment, and the `contract-v1.43` CHANGELOG worked example
      ANNOTATED rather than reworded because it is a published record.

## Phase 8: Validation

- [X] T031 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — 75 passed.
- [X] T032 `python3 scripts/verify-openxwallet-pin.py` — exit 0, eight digests
      recomputed.
- [X] T033 `python3 scripts/validate-trust-anchor.py .` — exit 0.
- [X] T034 The gate's exact invocation run locally with the register conjunction
      asserted — all four assertions hold.
- [X] T035 `python3 -m pytest tests/ -q -m "not postgres"` — counts in
      `evidence/validation.md`; the CI triple is pinned from CI's own JUnit XML.
- [X] T036 `python3 scripts/doc-health.py --single-repo .` against the same run on
      `origin/main`: finding sets IDENTICAL, 65 = 65, zero new and zero resolved.
- [X] T037 `validate-contract-release.py build` re-run byte-identical; §5.8's
      `verify-tag --tag contract-v1.47` → `release verify-tag: pass`.
- [X] T038 grep proving no `contracts/openxwallet/` path reference survives
      outside `openXwallet/`, the pin, and the two deliberate pin-relative
      citations.

## Phase 9: Open by design — the operator's, and the wave's

- [ ] T039 §7.1 **[OPERATOR]** Sequencing guard: land before 2026-11-01 or
      re-issue `governance/review-authority/register.yaml`'s row before
      2026-11-23. **Chosen: land before 2026-11-01** — this pull request is
      opened 2026-08-27, 66 days inside the window.
- [ ] T040 §7.26 **[OPERATOR]** REBASE and RE-VERIFY the eight digests
      immediately before merge; that re-verification, not this authoring-time
      one, is what the evidence row carries.
- [ ] T041 §7.28 Evidence: green `wallet-validation` on this pull request's OWN
      head, from the renamed file.
- [ ] T042 §7.31 **[OPERATOR]** Evidence: ruleset 21538893 as an UNCHANGED-STATE
      row from `GET repos/opensoft/openxFactory/rules/branches/main`.
- [ ] T043 §7.32 **[OPERATOR]** Task 2.6's red-proof, retargeted: a deliberately
      malformed row under `governance/review-authority/` turns an openxFactory
      pull request RED with a `register-*` finding naming the full path.
- [ ] T044 §5.8 **[OPERATOR]** Cut the `contract-v2.0` annotated tag on the merged
      commit, and re-verify the number at merge order per `:30-31` — four places
      carry it (the manifest line, the changelog heading, the inventory filename,
      the policy's Executed entry) and they move together.
- [ ] T045 The MERGE itself. **P5a.2 must land first** (`tasks.md` §6): the
      LedgerxFactory `stack.yaml` bump to `contract-v1.47` plus the pinned-checker
      invocation that makes the relocation warning OBSERVED. Without it the
      deprecation window is unobserved and the policy precondition is a
      formality.

## Dependencies

Phase 1 gates everything (a gate that cannot clone is not a gate). Phase 2 gates
Phases 3 and 4 (both call the verifier). Phase 4 must be in the SAME COMMIT as
Phase 5 — the replacement gate and the removal of what it replaces cannot be
ordered. Phase 6 follows Phase 5 because the release inventory is computed over
the post-deletion tree. Phase 7 is last so every path it names is final.
