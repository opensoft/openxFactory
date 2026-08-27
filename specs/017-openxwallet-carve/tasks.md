# Tasks: P2 — carve and scaffold `opensoft/openXwallet`

**Feature**: `017-openxwallet-carve` | **Date**: 2026-08-26
**Input**: [spec.md](./spec.md) · [plan.md](./plan.md) · [research.md](./research.md) · [data-model.md](./data-model.md) · [contracts/](./contracts/) · [quickstart.md](./quickstart.md)
**Realizes**: `openspec/changes/split-openxwallet-repo` tasks 3.1–3.31

**CARVE_COMMIT**: `30565e48ffe3d8a9773e10af33425701845e10f6` (frozen)

**Path conventions**
- `$SCRATCH` — the throwaway working area. Never committed, never referenced from a committed file.
- `$SCRATCH/openxFactory-src` — the fresh openxFactory clone at CARVE_COMMIT (READ ONLY).
- `$SCRATCH/openXwallet` — the carved repository under construction.
- `$FEAT` — `specs/017-openxwallet-carve/` in this openxFactory worktree.
- Paths without a prefix are relative to `$SCRATCH/openXwallet`.

**Hard limit, restated**: openxFactory gains `$FEAT/` and ticks in
`openspec/changes/split-openxwallet-repo/tasks.md`. Nothing else. No deletion, no
rename, no force-push, in any existing repository.

---

## Phase 1: Setup — the pre-carve gate (ratified 3.1, 3.3)

- [X] T001 Re-run the case-variant repository-name check at create time and record the raw output in `$FEAT/evidence/operator-log.md`: `gh repo view opensoft/openXwallet`, `openxwallet`, `OpenXWallet`, `openXWallet`, `OPENXWALLET`, plus `gh search repos openxwallet --owner opensoft` and an unscoped `gh search repos openxwallet`. ALL must be absent. **On any hit: stop, report, do not carve.**
- [X] T002 [P] Confirm `git filter-repo --version` succeeds and record the version string in `$FEAT/evidence/operator-log.md`; if absent, install via `pip install --user git-filter-repo` (or `pipx install git-filter-repo`) and record WHICH path was taken.
- [X] T003 [P] Create `$SCRATCH` and clone `git@github.com:opensoft/openxFactory.git` into `$SCRATCH/openxFactory-src`; `git fetch origin`; assert `git rev-parse origin/main` equals `30565e48ffe3d8a9773e10af33425701845e10f6` and check that commit out on a local branch. **If origin/main has moved, STOP** — the carve commit is frozen and a moved main means re-deciding it, which is a ratified act (3.3), not an implementation detail.
- [X] T004 Record the CONTROL in `$FEAT/evidence/byte-identity.md`: recompute all eight `sha256:` values from `$SCRATCH/openxFactory-src/contracts/manifest.yaml` over the files their rows name, at CARVE_COMMIT. Expected 8/8. Without this control a post-carve match proves the manifest stale, not the carve faithful.
- [X] T005 Write `$SCRATCH/expected-files.txt`: `git ls-tree -r --name-only <CARVE_COMMIT> --` over the twelve path sets, sorted. Assert the line count is **100** and record the per-set breakdown from `research.md` R2.

**Checkpoint**: the name is free, the tool is present, the tree is frozen and measured, and the control is recorded. Nothing irreversible has happened.

---

## Phase 2: Foundational — the runbook authored BEFORE the carve (ratified 3.2, 3.31)

**BLOCKING**: T006 must be complete before Phase 3. The runbook is authored before
the carve it describes; a rollback written after the phase is taken is not a
rollback.

- [X] T006 Author `docs/openxwallet-cutover-runbook.md` in a staging copy (it is committed in Phase 4), carrying the six ordered reversible phases from the proposal § cutover: (1) the case-variant check, (2) repository creation + the carve + the completeness check with `specs/006-openxwallet-contracts/evidence/` and `contracts/openxwallet/examples/negative/` named explicitly, (3) CODEOWNERS + ruleset EVALUATE → one trivial PR → ACTIVE, (4) tag `wallet-v1.0` only after the proof, (5) submodule init in openxFactory and the aggregation with the proof re-run from each consuming checkout, (6) rollback per phase. Each phase's ROLLBACK is written before that phase's steps. The NAMED CARVE COMMIT appears as a 40-hex literal, never "HEAD".
- [X] T007 In the same runbook, state plainly that **day-one REQUIRED is impossible** — GitHub cannot require a check that has never reported — recorded as unachievable rather than promised (ratified 3.25).
- [X] T008 In the same runbook, record the two-part byte-identity proof TABLE shape (eight digest rows + the floor diff + the two-line spec diffs), to be filled by Phase 5 (ratified 3.2, 3.23, 3.24).
- [X] T009 Record the P2 rollback in `$FEAT/evidence/operator-log.md` BEFORE Phase 3 begins: nothing pins openXwallet yet, so the reversal is deleting the repository or leaving it unpinned; openxFactory is untouched either way (ratified 3.31).

**Checkpoint**: the procedure exists on paper, with its exits, before any of it is taken.

---

## Phase 3: User Story 1 — the wallet standard exists as its own governed product (P1)

**Goal**: a repository holding the twelve path sets with full path history, that validates itself offline.

**Independent test**: clone it, run its checks offline, read any carved file's history back to its original openxFactory commit.

### The carve (ratified 3.5–3.8)

- [X] T010 [US1] Copy `$SCRATCH/openxFactory-src` to `$SCRATCH/openXwallet` (a second clone, so the read-only source survives the rewrite) and check out CARVE_COMMIT on a branch named `main`.
- [X] T011 [US1] Run `git filter-repo` in `$SCRATCH/openXwallet` with one `--path` per set, exactly the twelve from `contracts/carve-surface.md`, verbatim: **NO globs, NO `--path-regex`, NO `--path-rename`**. Record the full invocation in `$FEAT/evidence/operator-log.md`.
- [X] T012 [US1] Completeness check (ratified 3.6): `git ls-files | sort` in the carved repo EQUALS `$SCRATCH/expected-files.txt`. Evidence is the diff of the two sorted listings, **empty**, plus the total 100. Record in `$FEAT/evidence/byte-identity.md`.
- [X] T013 [US1] Assert the counts (ratified 3.7) and record all four: `specs/006-openxwallet-contracts/` = **7** (its `evidence/` included); `contracts/openxwallet/examples/negative/` = **32**; `contracts/openxwallet-agent-profile/examples/negative/` = **4**; the two together = **36** — the ratified figure, in the precise form its shorthand collapsed (see `research.md` R3).
- [X] T014 [US1] Assert examples-prefix preservation (ratified 3.8): both `contracts/openxwallet/examples/` and `contracts/openxwallet-agent-profile/examples/` exist at IDENTICAL relative paths. Record WHY it is an acceptance line: the corpus exclusion keys on `"examples" in path.parts` AND an `openxwallet*` part, so a rename re-adjudicates 36 intended-invalid negatives as LIVE records inside a check that becomes REQUIRED.
- [X] T015 [US1] Assert full path history survived: `git log --oneline -- scripts/validate-openxwallet.py` shows the original openxFactory commits, not one import commit. Record the commit count.

### The carve layer is now frozen

- [X] T016 [US1] Tag the carve layer locally as `carve-base` (a local marker only, never pushed) so every subsequent diff has a stable referent inside the carved repository.

**Checkpoint**: US1's tree is complete and its history is real. Everything after this is additive.

---

## Phase 4: User Story 3 — the repository gates itself (P2, but scaffolded here because US2's proof needs the scaffold in place)

**Goal**: two workflows, a fail-closed pin verifier, CODEOWNERS, the manifest, and the governance documents.

**Independent test**: run all five gates offline in the carved repository; all exit 0. Then mutate the vendored copy and watch the verifier refuse.

### The vendored artifact and its pin (ratified 3.16, 3.17)

- [X] T017 [US3] Byte-copy `contracts/schemas/hermes-job-envelope.schema.yaml` from `$SCRATCH/openxFactory-src` to the IDENTICAL relative path in the carved repo — added by the SCAFFOLD, never by the carve, so `ENVELOPE_SCHEMA_PATH` and its `.relative_to(ROOT)` print need no edit and the empty-diff proof survives. Verify `sha256sum` equals `8ce2c89903a2f5a68ce3d73a7b8eb4f47cdef913da038b9a68e22735ee96cb7c`.
- [X] T018 [US3] Write `contract_pin.yaml` per `data-model.md` E5: `schema_version: 1`, `kind: pinned_contract_manifest`, `source_repository: opensoft/openxFactory`, `revision_kind: commit`, `commit: <CARVE_COMMIT>`, `pinned_bundle: contract-v1.44`, `verify_pin: scripts/verify-contract-pin.py`, one `files:` entry with its sha256, and `pinned_by_commit_only: []` present-and-empty. Carry openAvatar's fail-closed pre-sync doctrine as a header comment.
- [X] T019 [US3] Write `scripts/verify-contract-pin.py` per `contracts/verify-contract-pin.md`: no arguments, reads only the pin and the files it names, never the network and never `contracts/manifest.yaml`; exit 0 on all-match, 1 on drift / missing file / empty recorded digest / bad `commit`, 2 on environment failure; **every non-zero exit prints both remediation lines** — `git submodule update --init openXwallet` and `docs/pin-resync-runbook.md` (N1).

### The manifest (ratified 3.11–3.15)

- [X] T020 [US3] Write `contracts/manifest.yaml` with `schema_version: 1`, `kind: contract_manifest`, `contract_bundle_version: wallet-v1.0`, and `carved_from: {repository: opensoft/openxFactory, commit: <CARVE_COMMIT>}` — the machine-read provenance record (ratified 3.14). **No bare `CARVE_COMMIT` file.**
- [X] T021 [US3] Carry the EIGHT owned rows into that manifest VERBATIM from openxFactory's rows at CARVE_COMMIT — all nine publisher fields, `sha256` UNCHANGED — rewriting only `source_path` (`openxFactory/…` → `openXwallet/…`). Carry the content-addressed-by-commit note for the validator, the syntax gate, both `examples/` trees and both family READMEs.
- [X] T022 [US3] Add the CONSUMED-member row per `data-model.md` E4: the nine publisher fields with `compatibility: canonical_openxfactory_contract` and `adapter_owner: openxFactory`, `sha256` computed over the pinned bytes, plus `member_class: consumed`, `release_surface: false`, `pinned_openxfactory_bundle: contract-v1.44`. Comment the row with WHY the digest is computed (openxFactory's own row records none) and with the two-hop upstream chain (Omnigent-Install → openxFactory → openXwallet).
- [X] T023 [US3] Declare the release-surface selection rule in the manifest as a comment and in `contracts/CHANGELOG.md`: `wallet-vN.M.digests.yaml` selects `member_class: owned` ONLY — exclusion by DECLARED FIELD, never by a `contracts/schemas/` path heuristic, which breaks the day openXwallet publishes a schema of its own there (ratified 3.13).
- [X] T024 [US3] Write `contracts/CHANGELOG.md` seeded from openxFactory's `contract-v1.31` (the openxWallet core + first profile) and `contract-v1.43` wallet entries, plus a `wallet-v1.0` entry recording: a byte-identical carve from openxFactory `<CARVE_COMMIT>`, the twelve path sets, the two prose edits, and NO content change (ratified 3.15).

### The workflows (ratified 3.19, 3.20)

- [X] T025 [US3] Edit the CARVED `.github/workflows/wallet-validation.yml`: keep job id `wallet-validation` and its absent display name, and insert `python3 scripts/verify-contract-pin.py` as the FIRST run step, before the syntax gate and the validator. Record in `$FEAT/evidence/byte-identity.md` that this is the ONLY post-carve edit to a carved file, and that task 3.24's floor does not include this path (see `plan.md` § Divergences item 1).
- [X] T026 [US3] [P] Write `.github/workflows/pytest-suite.yml`: job id `pytest-suite`, no display name, `pull_request` → `main`, `permissions: contents: read`, checkout → setup-python 3.12 → `pip install pyyaml jsonschema rfc3339-validator pytest` → `python3 -m pytest tests/ -q`.

### The governed-repo scaffold (ratified 3.9, 3.10, 3.18)

- [X] T027 [US3] [P] Write `README.md`: what the repository is; the two contract families; a doc index linking every document in the tree; the "Domain descendants: pin and profile, never fork" section in openAvatar's shape (`MedxWallet`, `LedgerxWallet`, `codexWallet`, `OpsxWallet`, `AdxWallet` per R7, with `LedgerxWallet` named first per R8); the consumption rule; the pin relationship in BOTH directions (openxFactory pins openXwallet by commit + per-file sha256; openXwallet vendors exactly one openxFactory artifact at a digest pin); and the byte-identity statement naming CARVE_COMMIT.
- [X] T028 [US3] [P] Write `CLAUDE.md` and `AGENTS.md` pointing at `$HOME/.agents/AGENTS.md` and the two protocol files, in openxFactory's house form, with repository documents authoritative for openXwallet product facts.
- [X] T029 [US3] [P] Write `.github/CODEOWNERS`: `/scripts/validate-openxwallet.py @brettheap`, `/scripts/wallet-yaml-syntax-gate.py @brettheap`, `/scripts/verify-contract-pin.py @brettheap`, `/contracts/ @brettheap`, `/contract_pin.yaml @brettheap`, `/.github/workflows/ @brettheap`.
- [X] T030 [US3] [P] Write `docs/pin-resync-runbook.md` on openAvatar's shape: Preconditions, Checklist, re-verify the pin offline, re-run the offline gate suite — plus the reason it exists from day one (an `openxwallet` core delta costs a wallet release, an openxFactory pin bump and a LedgerxFactory re-pin) and the offline law (no gate reads an upstream tree or the network).
- [X] T031 [US3] Commit `docs/openxwallet-cutover-runbook.md` from T006–T008 into the carved repository.

### OpenSpec init and the two prose edits (ratified 3.21–3.23)

- [X] T032 [US3] Write `openspec/config.yaml` with `schema: spec-driven`.
- [X] T033 [US3] Prose edit one of two (ratified 3.21): in BOTH `openspec/specs/openxwallet/spec.md` and `openspec/specs/openxwallet-agent-profile/spec.md`, rewrite every `openxFactory SHALL` to `openXwallet SHALL` across the eleven requirement bodies. Record the per-file occurrence count.
- [X] T034 [US3] Prose edit two of two (ratified 3.22): replace line 4 of each promoted spec — `TBD - created by archiving change add-openxwallet. Update Purpose after archive.` — with a real `## Purpose` sentence for that family. **Nothing else in either file changes.**

### Local gates — all of them, before anything is pushed (Constitution V)

- [X] T035 [US3] Run in the carved repository and record every exit code in `$FEAT/evidence/operator-log.md`: `python3 scripts/verify-contract-pin.py`; `python3 scripts/wallet-yaml-syntax-gate.py .`; `python3 scripts/validate-openxwallet.py .`; `python3 scripts/validate-openxwallet.py . --strict`; `python3 -m pytest tests/ -q` (assert collection is NON-ZERO — a silently empty suite must be distinguishable from a passing one); `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`. **All must exit 0.**
- [X] T036 [US3] The V8 RED proof (ratified 3.30): append a comment line to `contracts/schemas/hermes-job-envelope.schema.yaml`, run `python3 scripts/verify-contract-pin.py`, assert exit 1 AND that the output carries both remediation strings; capture the refusal text; then `git checkout --` the file and re-assert exit 0. A verifier that has never refused is not known to refuse.

**Checkpoint**: the repository gates itself offline, and its one fail-closed path has been observed to fail closed.

---

## Phase 5: User Story 2 — the move is provably empty (P1)

**Goal**: both halves of the byte-identity proof, reproducible by a third party.

**Independent test**: run `quickstart.md` §1–§7 with only the two repositories; every claim lands where the record says.

- [X] T037 [US2] Part ONE (ratified 3.23): for each of the eight digested artifacts, `sha256sum` in the carved tree EQUALS the `sha256:` recorded at CARVE_COMMIT. Write the eight-row table into `$FEAT/evidence/byte-identity.md` AND into `docs/byte-identity-wallet-v1.0.md`.
- [X] T038 [US2] Part TWO (a) (ratified 3.24): `diff -r` against `$SCRATCH/openxFactory-src` at CARVE_COMMIT over `contracts/openxwallet/`, `contracts/openxwallet-agent-profile/`, `tests/wallet_yaml_syntax_gate/`, `specs/006-openxwallet-contracts/`, `specs/010-wallet-validator-ci/`, `specs/012-wallet-issuer-anchor/`, `openspec/changes/archive/2026-08-08-add-openxwallet/`, and plain `diff` over `scripts/validate-openxwallet.py` and `scripts/wallet-yaml-syntax-gate.py`. **EMPTY.** Record each path's result individually, not as one aggregate claim.
- [X] T039 [US2] Part TWO (b) (ratified 3.24): `diff` each promoted spec against CARVE_COMMIT and assert the change is limited to `:4` and the `openxFactory SHALL` → `openXwallet SHALL` subject, asserted LINE BY LINE. Paste the literal diffs into the record — the declared scope of the one carve-out, rather than a described one.
- [X] T040 [US2] Record the ONE declared post-carve edit to a carved file: the one-hunk diff of `.github/workflows/wallet-validation.yml`, with the ratified basis (task 3.19 requires the verify step before the validator; task 3.24's floor does not include this path).
- [X] T041 [US2] Write `docs/byte-identity-wallet-v1.0.md` in the carved repository as the reproducible record — every command with repo-relative paths and a `$` placeholder for checkout locations. **No host-absolute path in any committed file** (Constitution IV). Link it from `README.md`'s doc index.
- [X] T042 [US2] Fill the runbook's proof table (T008's shape) with the actual results.

**GATE**: T037–T039 must all be green before Phase 6 pushes anything, and before any tag (ratified 3.28).

---

## Phase 6: User Story 4 — the operator's acts, ordered and reversible (P2)

**Goal**: the repository exists on GitHub, gates its default branch, and carries the tag.

**Independent test**: `gh api repos/opensoft/openXwallet/rules/branches/main` and `git tag -l -n99 wallet-v1.0` read back as the record says.

- [X] T043 [US4] Create the repository (ratified 3.4): `gh repo create opensoft/openXwallet --private --description "openXwallet — the neutral wallet standard: contracts, validator, corpus (split from openxFactory at <CARVE_COMMIT>)"`. Record the URL.
- [X] T044 [US4] `git remote add origin git@github.com:opensoft/openXwallet.git` and push `main`. Record the pushed head sha.
- [X] T045 [US4] Create the ruleset (ratified 3.25) via `gh api -X POST repos/opensoft/openXwallet/rulesets` at `enforcement: evaluate`, mirroring 21538893's shape: `target: branch`, `conditions.ref_name.include: ["~DEFAULT_BRANCH"]`, one `required_status_checks` rule with `strict_required_status_checks_policy: false`, `do_not_enforce_on_create: false`, contexts `wallet-validation` and `pytest-suite`. Record the ruleset id.
- [X] T046 [US4] Land ONE trivial pull request (ratified 3.26) — a README touch — so both checks report once and become selectable. Record both run ids and both conclusions.
- [X] T047 [US4] Capture the V8 GREEN evidence (ratified 3.30) from that run's `wallet-validation` log: the line showing the vendored envelope schema digest-verified against `contract_pin.yaml` BEFORE the validator step started. Pair it with T036's red refusal.
- [X] T048 [US4] Merge the trivial pull request.
- [X] T049 [US4] PATCH the ruleset to `enforcement: active` (ratified 3.27) and capture `GET repos/opensoft/openXwallet/rules/branches/main` showing the required status checks. Record the raw response in `$FEAT/evidence/operator-log.md`.
- [X] T050 [US4] **Only now** (ratified 3.28), and only if T037–T039 are green: `git tag -a wallet-v1.0 -m "wallet-v1.0 — byte-identical carve of openxFactory@<CARVE_COMMIT>"` and push the tag. Record the tag's target sha.
- [X] T051 [US4] Verify `wallet-validation` and `pytest-suite` are green on `main` at the tagged commit; record the run ids as the P2 realization evidence rows (ratified 3.29).

---

## Phase 7: Polish & cross-cutting — the openxFactory bookkeeping

- [X] T052 Tick `openspec/changes/split-openxwallet-repo/tasks.md` group 3 tasks 3.1–3.31 with evidence notes: the repository URL, CARVE_COMMIT, the completeness result, the eight-row proof, the run ids, the ruleset id and enforcement, and the tag (ratified 3.29, 3.30). **Touch no other group.**
- [X] T053 Verify the openxFactory footprint is exactly two paths: `git status --short` shows only `specs/017-openxwallet-carve/` and `openspec/changes/split-openxwallet-repo/tasks.md`. Zero deletions, zero renames.
- [X] T054 Run `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` from the openxFactory worktree root; must be green.
- [X] T055 Commit with EXPLICIT pathspecs (`git commit -m … -- specs/017-openxwallet-carve openspec/changes/split-openxwallet-repo/tasks.md`), house-style subject ≤ 72 chars, shared-tree discipline — never `git add -A`; inspect `git diff --cached --stat` for foreign entries first.
- [X] T056 Push `017-openxwallet-carve` and `gh pr create -R opensoft/openxFactory --base main` with a body carrying: P2 of the ratified split; CARVE_COMMIT; the byte-identity proof summary; the repository, ruleset and tag; what remains for P2b; and the Claude Code footer. **Do NOT merge.**

---

## Dependencies

```
Phase 1 (T001-T005)  ──►  Phase 2 (T006-T009)  ──►  Phase 3 / US1 (T010-T016)
                                                             │
                                                             ▼
                                                  Phase 4 / US3 (T017-T036)
                                                             │
                                                             ▼
                                                  Phase 5 / US2 (T037-T042)  ◄── GATE
                                                             │
                                                             ▼
                                                  Phase 6 / US4 (T043-T051)
                                                             │
                                                             ▼
                                                  Phase 7 (T052-T056)
```

**Why the story order is not the priority order.** US1 (P1) and US2 (P1) are the
two things the wave consumes, but US2's proof cannot be taken until US3's scaffold
is in place — the proof must state the scaffold's one edit to a carved file, and
the local gates must be green before anything is pushed. So US3 (P2) is built
between them. US4 (P2) is last because it is the only phase with irreversible-ish
acts, and it is gated on US2.

**Hard gates**
- T001 blocks everything: a name collision costs the carve.
- T006 blocks the carve: the runbook is authored before the procedure is taken.
- T037–T039 block T050: no tag before the proof (ratified 3.28).
- T035 blocks T044: nothing is pushed until every local gate is green.

## Parallel opportunities

- **Phase 1**: T002 and T003 are independent (`[P]`).
- **Phase 4 scaffold**: T026, T027, T028, T029, T030 touch disjoint files (`[P]`).
- **Phase 5**: T037 and T038 read the same two trees but write different sections; safe to interleave, not marked `[P]` because both feed one record.
- Everything in Phase 6 is strictly sequential — it is an operator procedure, and its order IS the requirement.

## Independent test criteria

| Story | Criterion |
| --- | --- |
| US1 | Clone the new repository; the twelve prefixes hold 100 files matching the carve commit's listing; any carved file's history reaches its original openxFactory commits; the validator and syntax gate exit 0. |
| US2 | With only the two repositories, `quickstart.md` §1–§7 reproduces 8/8 digests, an empty floor diff, and exactly two changed lines per promoted spec. |
| US3 | All five local gates exit 0; the verifier refuses a mutated vendored copy with both remediation strings; branch protection reads back with the required checks. |
| US4 | The runbook alone is sufficient to take and reverse each phase; the carve commit appears as a 40-hex literal. |

## Implementation strategy

**MVP is US1 + US2 together**, not US1 alone: a carved repository whose move is
not provably empty delivers nothing the wave can use, because P3's atomic
consume-and-shed rests on the empty diff and nothing else. US3 makes the
repository able to refuse a change; US4 makes GitHub enforce it.

**Incremental delivery**: Phases 1–3 are reversible by deleting a scratch
directory. Phase 4 changes nothing outside that directory. Phase 5 either passes
or stops the feature. Only Phase 6 touches the outside world, and it is reversible
until P3 pins the result.

**Total**: 56 tasks — 5 setup, 4 foundational, 7 US1, 20 US3, 6 US2, 9 US4, 5 polish.
