# Tasks: openxwallet deprecation minor (P2.5)

**Feature**: `018-openxwallet-deprecation-minor` | **Branch**: `018-openxwallet-deprecation-minor`

**Input**: [spec.md](./spec.md), [plan.md](./plan.md), [research.md](./research.md),
[data-model.md](./data-model.md), [contracts/pin-check-cli.md](./contracts/pin-check-cli.md),
[quickstart.md](./quickstart.md)

**Realizes**: `openspec/changes/split-openxwallet-repo` `tasks.md` §5 (P2.5).

**Tests**: IN SCOPE. FR-013 requires them, and `tasks.md` 5.9 names the checker's
warning OUTPUT as the evidence row — so the output is proven, not asserted.

---

## Standing constraints (apply to every task below)

- **Byte-identity floor**: no byte may change under `contracts/openxwallet/`,
  `contracts/openxwallet-agent-profile/`, `scripts/validate-openxwallet.py`,
  `scripts/wallet-yaml-syntax-gate.py`, `tests/wallet_yaml_syntax_gate/`,
  `.github/workflows/wallet-validation.yml`.
- **No manifest row may be removed.** That is P3.
- **Commits use explicit pathspecs** (`git commit -m … -- <paths>`); the shared
  index is not trusted.
- Work only in the feature worktree. Never the root checkout.

---

## Phase 1: Setup

- [X] T001 Confirm the working tree is clean apart from `specs/018-openxwallet-deprecation-minor/` and that HEAD is on branch `018-openxwallet-deprecation-minor` at `origin/main`, via `git status -sb` in the feature worktree
- [X] T002 Record the doc-health baseline to compare against later: run `python3 scripts/doc-health.py --single-repo . --family release-inventory-drift` and confirm it matches the three findings recorded in research.md R8 (1 error on `scripts/validate-hermes-runtime-contracts.py`, 2 editorial infos)

## Phase 2: Foundational (blocking prerequisites)

*Nothing here is optional; every user story depends on these two facts holding.*

- [X] T003 Verify the eight target rows and their exact ids in `contracts/manifest.yaml` against the table in data-model.md, by `grep -n '  - id: openxwallet' contracts/manifest.yaml` (expect 8 hits at lines 1999, 2017, 2030, 2043, 2056, 2069, 2082, 2095)
- [X] T004 Verify no manifest schema or strict-key validator would reject a new row key, per research.md R1 — re-confirm `scripts/validate-manifest-digests.py` `iter_entries()` keys only off co-present `sha256` + `path` (so `relocating:`'s three sub-keys are invisible to it)

---

## Phase 3: User Story 1 — The manifest and changelog state the relocation (P1) 🎯 MVP

**Goal**: The eight rows carry a machine-readable relocation declaration, and the
changelog + policy doc state the removal version and migration path. This alone
discharges the `docs/contract-versioning-policy.md:250-252` precondition for P3.

**Independent test**: read the eight rows and the changelog section; run
`scripts/validate-manifest-digests.py`. No checker change and no cut needed.

- [X] T005 [US1] Add the `relocating:` block mapping (`to: opensoft/openXwallet`, `tag: wallet-v1.1`, `since: contract-v1.46`) as the LAST key of each of the eight openxwallet rows in `contracts/manifest.yaml`, after `consumption_rule`, changing no other byte of those rows
- [X] T006 [US1] Bump `contract_bundle_version` from `contract-v1.45` to `contract-v1.46` at `contracts/manifest.yaml:3`
- [X] T007 [US1] Add the `## contract-v1.46` section to `contracts/CHANGELOG.md` above the `contract-v1.45` section, declaring **change class: DEPRECATING (minor)**, naming what relocates (the eight artifacts, by id), where (`opensoft/openXwallet` at `wallet-v1.1`), the removal version (`contract-v2.0`, the next major), and the migration path (the `contracts/openxwallet-pin.yaml` arriving at P3 plus `openXwallet/docs/pin-resync-runbook.md`); cite `split-openxwallet-repo` P2.5 / D5 / D6 and note that LedgerxFactory's P5a.2 bump observes this minor
- [X] T008 [US1] Add the deprecation entry to `docs/contract-versioning-policy.md`'s "Deprecations Currently In Force" list (`:274`+), following the `contract-v1.34` precedent's shape and ending "Deprecated at contract-v1.46; removal target contract-v2.0"
- [X] T009 [US1] Verify the floor: `git diff --name-only origin/main --` over the six frozen paths prints nothing, and `grep -c '  - id: openxwallet' contracts/manifest.yaml` still prints 8
- [X] T010 [US1] Run `python3 scripts/validate-manifest-digests.py` and confirm every per-file digest still verifies (the marker changes no contract file's bytes)
- [X] T011 [US1] Confirm the eight ids carrying `relocating:` by parsing the manifest with PyYAML per quickstart.md S1, and that no ninth row carries it

**Checkpoint**: US1 is independently complete. The relocation is stated and
readable. Nothing yet warns about it and nothing is published.

---

## Phase 4: User Story 2 — A pinned consumer is warned, not failed (P2)

**Goal**: `scripts/check-openxfactory-pin.py` emits the WARN-tier relocation
notice, with exit-code semantics and all four existing verdicts untouched.

**Independent test**: the pin tests in `tests/conformance-gate/`, plus the two
fixture runs of quickstart.md S4 (pinned to this bundle → WARN + exit 0; pinned
to `contract-v1.45` → no notice).

### Tests first (FR-013)

- [X] T012 [P] [US2] Add `test_pin_relocating_rows_extracted_in_manifest_order` to `tests/conformance-gate/test_conformance_checks.py` in the `# --- pin ---` section: a manifest mapping with three contract rows, two carrying `relocating:`, yields both in manifest order with `artifact_id` / `to` / `tag`
- [X] T013 [P] [US2] Add `test_pin_no_relocating_rows_yields_no_notice` — a manifest with no `relocating:` key anywhere returns `None` from the notice builder (the `contract-v1.45` case)
- [X] T014 [P] [US2] Add `test_pin_relocation_notice_names_every_artifact_target_and_tag` — the notice string contains the bundle name, the row count, and one `<id> -> <to> @ <tag>` line per relocating row
- [X] T015 [P] [US2] Add `test_pin_relocation_notice_absent_when_manifest_unreadable` — a manifest that is absent, unparseable, or not a mapping produces no notice and raises nothing
- [X] T016 [P] [US2] Add `test_pin_relocation_does_not_change_exit_semantics` — assert the exit expression still yields 0 for PASS/WARN/SKIP and 1 for ERROR when a relocation notice is present

### Implementation

- [X] T017 [US2] Add `relocating_rows(manifest)` to `scripts/check-openxfactory-pin.py` — pure; returns the ordered list of `(artifact_id, to, tag)` for every `contracts` row carrying a `relocating:` mapping; tolerant of a non-mapping manifest and of rows missing sub-keys
- [X] T018 [US2] Add `relocation_notice(manifest)` to the same file (refined from the plan's `(rows, bundle)` — the bundle name comes from the same document, so one argument is enough and there is no way to pass mismatched halves) — pure; returns the multi-line WARN message per `contracts/pin-check-cli.md` § Output grammar, or `None` when `rows` is empty
- [X] T019 [US2] Add `manifest_at_commit(openx_root, commit)` to the same file — reads `git -C <openx_root> show <commit>:contracts/manifest.yaml`; returns the parsed mapping, or `None` on any failure (missing commit, missing file, YAML error, non-mapping)
- [X] T020 [US2] Wire it into `main()`: after printing the pin verdict, resolve the pinned manifest from `aggregation_root / "openxFactory"` at the consumer's `pin`, print the relocation notice to **stdout** if there is one, and leave the return expression as `1 if verdict == ERROR else 0`
- [X] T021 [US2] Extend the module docstring to record the WARN tier's new second use AND the `tasks.md` 5.5 reason `scripts/validate-domain-openxfactory-pins.py` is NOT the emitter (no `warn` token in its 138 lines → a relocation notice there would be an ERROR and would red every domain pinning this legal bundle) — FR-011
- [X] T022 [US2] Confirm `classify()` is byte-unchanged and `scripts/validate-domain-openxfactory-pins.py` and `scripts/validate-openxwallet.py` are untouched, via `git diff origin/main -- scripts/`
- [X] T023 [US2] Run `python3 -m pytest tests/conformance-gate/ -q` — the five pre-existing pin tests pass unchanged alongside the new ones

**Checkpoint**: US2 is independently complete. The marker is now observed.

---

## Phase 5: User Story 3 — The minor is a properly published bundle (P3)

**Goal**: the bundle has its own release inventory over a surface that still
contains all eight artifacts, and the three bundle names agree.

**Independent test**: quickstart.md S2 and S3.

- [X] T024 [US3] Generate the inventory LAST, after every content edit: `python3 scripts/validate-contract-release.py build --tag contract-v1.46 --output contracts/releases/contract-v1.46.digests.yaml` (the manifest, changelog and policy doc are all release-surface members, so their new bytes must already be on disk)
- [X] T025 [US3] Verify the three-way name agreement per quickstart.md S2: `contract_bundle_version`, the newest `## contract-v` changelog heading, the inventory filename, and the inventory's own `bundle_tag` all read `contract-v1.46`
- [X] T026 [US3] Verify the inventory is reproducible — regenerate to a scratch path and `diff` against the committed file; expect no diff (proves it was tool-produced, not hand-edited)
- [X] T027 [US3] Verify the eight openxwallet registrations are still on the release surface TRANSITIVELY per research.md R11: inventory membership is catalog-driven and the eight artifact files are not members (0 hits, at v1.45 too), so check instead that `contracts/manifest.yaml` IS a member, that its recorded digest equals `git hash-object contracts/manifest.yaml`, and that the manifest still carries 8 openxwallet rows
- [X] T028 [US3] Run `python3 scripts/doc-health.py --single-repo . --family release-inventory-drift` and confirm **no findings** — the pre-existing error on `scripts/validate-hermes-runtime-contracts.py` plus the two editorial infos are discharged by this cut, per research.md R8
- [X] T029 [US3] Do NOT create the annotated tag. Confirm `git tag -l 'contract-v1.46'` is empty — the tag is an operator act at merge (research.md R4)

**Checkpoint**: the bundle is authored and internally consistent. Publication
completes at merge, when the operator cuts the tag.

---

## Phase 6: Evidence, OpenSpec bookkeeping and validation

- [X] T030 Run the two end-to-end fixture scenarios of quickstart.md S4 and capture the literal output: S4a (consumer pinned to this bundle → the eight-line WARN, exit 0) and S4b (consumer pinned to `contract-v1.45` → no relocation line, exit 0)
- [X] T031 Save the S4a output verbatim into `specs/018-openxwallet-deprecation-minor/evidence/warn-sample.txt` as the `tasks.md` 5.9 evidence artifact (the checker's OUTPUT, not the manifest rows)
- [X] T032 Tick `openspec/changes/split-openxwallet-repo/tasks.md` §5 items that are COMPLETE — 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.9, 5.10 — each with a one-line evidence note naming the file or the evidence artifact. **Touch no other group's items** (a concurrent PR owns §4)
- [X] T033 Leave `openspec/changes/split-openxwallet-repo/tasks.md` 5.8 UNTICKED with a note that the number is allocated and the tag cut at merge by the operator, and that this feature authors `contract-v1.46` subject to merge-order re-verification
- [X] T034 Run `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` and confirm it passes
- [X] T035 Run `python3 -m pytest -q` (the whole suite, as CI's `pytest-suite` collects it) and confirm green
- [X] T036 Run `python3 scripts/doc-health.py --single-repo .` and confirm **no NEW finding** versus the T002 baseline; the release-inventory-drift trio should be gone (an improvement, not a suppression)

## Phase 7: Polish, commit and pull request

- [X] T037 Re-verify the byte-identity floor one final time across the whole diff: `git diff --stat origin/main` names only the expected files and none of the six frozen paths
- [ ] T038 Commit with explicit pathspecs and a house subject ≤72 chars, body citing P2.5 / D5 / D6 / `split-openxwallet-repo`, ending `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`
- [ ] T039 Push the branch and open the pull request with `gh pr create -R opensoft/openxFactory --base main`, body covering: what/why, the eight rows, the WARN sample, the cut mechanics, the renumber-at-merge note, the `wallet-v1.1`-vs-D5's-`wallet-v1.0` deviation, the discharged pre-existing inventory error, the tag-is-the-operator's note, and validation results
- [ ] T040 Watch `wallet-validation` and `pytest-suite` with `gh pr checks --watch` (≤15 min) and report. **Do not merge.**

---

## Dependencies & execution order

```
Phase 1 (T001-T002)  ─ setup, baseline
        ↓
Phase 2 (T003-T004)  ─ foundational facts
        ↓
Phase 3 US1 (T005-T011) ── the statement          [MVP — independently shippable]
        ↓ (US2 needs a manifest that HAS relocating rows to warn about)
Phase 4 US2 (T012-T023) ── the observation
        ↓ (US3 must be LAST: the inventory digests the files US1 edited)
Phase 5 US3 (T024-T029) ── the publication
        ↓
Phase 6 (T030-T036)  ─ evidence + gates
        ↓
Phase 7 (T037-T040)  ─ commit, PR, checks
```

**Hard ordering constraints** (not merely conventional):

1. **US1 before US2.** The fixture runs in T030 need eight rows that actually
   carry `relocating:`; a checker with nothing to read proves nothing.
2. **US3 strictly last among the three.** `contracts/manifest.yaml`,
   `contracts/CHANGELOG.md` and `docs/contract-versioning-policy.md` are all
   release-surface members (research R9). Generating the inventory before those
   edits settle records stale digests and the drift family reds.
3. **T031 before T032.** Task 5.9's evidence row cites the artifact; ticking it
   before the artifact exists is the ticking-without-evidence failure the parent
   change warns about.
4. **T024 after T005–T008 AND after T017–T021.** The script is a release-surface
   member too, so its new bytes must be on disk before the inventory is built.

## Parallel opportunities

- **T012–T016** are `[P]`: five test functions in one file, no interdependence.
  They can be authored together in a single edit pass, and they are expected to
  FAIL until T017–T020 land.
- **T005 and T007–T008** touch three different files and could be parallel, but
  T006 shares `contracts/manifest.yaml` with T005, so in practice T005+T006 are
  one edit and T007, T008 are the parallel pair.
- Nothing in Phase 5, 6 or 7 is parallelizable — each is a gate on the previous.

## Independent test criteria per story

| Story | Independently testable by | Ships value alone? |
|---|---|---|
| **US1** (P1) | quickstart S1 + `validate-manifest-digests.py` | **Yes** — the deprecation is stated and readable; this is the policy precondition |
| **US2** (P2) | `pytest tests/conformance-gate/` + quickstart S4 | Yes — but warns about nothing until US1 exists |
| **US3** (P3) | quickstart S2 + S3 | Yes — makes the minor a real bundle P5a.2 can pin |

## Suggested MVP scope

**US1 alone** (T001–T011). It is the `docs/contract-versioning-policy.md:250-252`
precondition in the narrowest form that satisfies it: the eight rows say where
they are going, and the changelog says when they leave and how to follow. US2 is
what makes the window *observed* rather than merely declared, and `tasks.md` 5.9
names the checker's output as evidence — so the honest full delivery is US1+US2+US3
in one bundle, which is what this feature does.

## Total: 40 tasks

| Phase | Tasks | Count |
|---|---|---|
| 1 Setup | T001–T002 | 2 |
| 2 Foundational | T003–T004 | 2 |
| 3 US1 — the statement | T005–T011 | 7 |
| 4 US2 — the observation | T012–T023 | 12 |
| 5 US3 — the publication | T024–T029 | 6 |
| 6 Evidence + gates | T030–T036 | 7 |
| 7 Commit + PR | T037–T040 | 4 |
