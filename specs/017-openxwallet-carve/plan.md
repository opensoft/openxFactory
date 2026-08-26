# Implementation Plan: P2 — carve and scaffold `opensoft/openXwallet`

**Branch**: `017-openxwallet-carve` | **Date**: 2026-08-26 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/017-openxwallet-carve/spec.md`

**Governing change**: `openspec/changes/split-openxwallet-repo` group 3, ratified
2026-08-26 by Brett Heap (merged `5ef6d8d2`, PR #391). This plan realizes tasks
3.1–3.31 and reopens none of R1–R8.

**NAMED CARVE COMMIT**: `30565e48ffe3d8a9773e10af33425701845e10f6`
(openxFactory `origin/main`, resolved from a fresh clone on 2026-08-26; FROZEN
for this feature — never "HEAD").

## Summary

Carve `opensoft/openXwallet` out of openxFactory over exactly twelve ratified
path sets with full path history, scaffold it as a self-gating governed
repository, prove the move is byte-identical against the named carve commit,
bootstrap its branch-protection ruleset through the only sequence GitHub permits,
and tag `wallet-v1.0`.

**The technical approach is a copy, not a move.** `git filter-repo --path` (one
per set, no globs, no renames) over a throwaway clone produces a repository whose
history is openxFactory's own commits filtered to those paths. openxFactory is
never rewritten, never force-pushed, and — in this feature — never has a byte
deleted. The scaffold is added ON TOP of that carved history, so the carve's
bytes stay diffable against their origin and the scaffold's additions are a
separate, reviewable layer.

**The proof is the deliverable.** Two independent halves: eight recomputed
digests against the eight recorded in openxFactory's manifest at the carve
commit, and an empty tree diff over the whole floor plus a two-line-only diff
over each promoted spec. Nothing is tagged until both are green, because a move
whose diff is not provably empty cannot be bisected against — and P3's atomic
consume-and-shed rests on exactly that property.

## Technical Context

**Language/Version**: Python 3.12 (the carved validator and syntax gate);
YAML 1.2 (every contract, manifest and pin); Markdown (governance docs);
GitHub Actions workflow YAML.

**Primary Dependencies**: `git filter-repo` (the carve; available at
`ed61b4050b71`), `git` ≥ 2.40, `gh` (repository creation + rulesets),
`pyyaml`, `jsonschema`, `rfc3339-validator` (the carved validator's runtime),
`pytest` (the carved gate's tests), `openspec` CLI (strict validation).

**Storage**: Files in git. No database, no service, no runtime state.

**Testing**: The carved `tests/wallet_yaml_syntax_gate/` under `pytest`; the
carved `scripts/validate-openxwallet.py` self-test plus repo scan, plain and
`--strict`; the carved `scripts/wallet-yaml-syntax-gate.py`; the new
`scripts/verify-contract-pin.py`; `OPENSPEC_TELEMETRY=0 openspec validate --all
--strict`.

**Target Platform**: `ubuntu-latest` GitHub Actions runners; any POSIX host for
local verification. Every gate is OFFLINE — no gate reads the network or an
upstream tree.

**Project Type**: Governed contract repository — schemas, a registry, a packaged
corpus, two validators, and the governance documents that bind them. Not an
application.

**Performance Goals**: Not a performance surface. Both checks must complete
inside the workflow's 10-minute timeout, which the carved job already does in
openxFactory.

**Constraints**:
- **The byte-identity floor.** Zero content change to the eight owned artifacts,
  both contract families, the two validators, the gate's tests, the three Speckit
  sets or the archive packet. ONE named carve-out: two prose lines in each of the
  two promoted specs.
- **No renames.** Not one. `contracts/openxwallet*/examples/` prefixes are
  load-bearing: the corpus exclusion keys on `"examples" in path.parts` AND an
  `openxwallet*` part, so a rename re-adjudicates 36 intended-invalid negatives
  as live records inside a check that becomes REQUIRED.
- **`ENVELOPE_SCHEMA_PATH` is not edited.** The vendored schema goes to the
  identical repository-relative path, which is why the validator's diff is empty
  rather than "empty except one line".
- **The vendored schema arrives by SCAFFOLD, not by carve.** Otherwise it is a
  carved file and the empty-diff claim is about a file openxFactory never had at
  that path in that role.
- **openxFactory only gains.** This feature's entire openxFactory footprint is
  `specs/017-openxwallet-carve/` plus `[x]` ticks in the change's `tasks.md`.
- **Day-one REQUIRED is impossible** and is recorded as unachievable, not
  promised: GitHub cannot require a check that has never reported.

**Scale/Scope**: 12 path sets; ~135 carved files including 36 intended-invalid
negatives and 7 files under `specs/006-openxwallet-contracts/`; 8 digested owned
artifacts + 1 consumed; 2 workflows; 2 runbooks; 1 new verifier; 2 prose lines
per promoted spec; 31 ratified tasks.

## Constitution Check

*GATE: passed before Phase 0; re-checked after Phase 1 (below).*

| Principle | Verdict | Basis |
| --- | --- | --- |
| **I. Contract-First, Domain-Neutral Core** | **PASS** | The wallet families are domain-NEUTRAL and stay so; they move to a neutral product repository, not into a domain. No domain vocabulary enters either tree. R3 fixes the seam: openXwallet takes the standard, openxFactory keeps the factory-layer USE of it (`governance/review-authority/`, Speckit 013/014, the compositions). |
| **II. Governed Change Flow** | **PASS** | OpenSpec ratified first (`split-openxwallet-repo`, PR #391); Speckit builds. This feature records no new governance decisions — it realizes ratified ones, and its one divergence class (three points of fact) is recorded in `clarify-questions.md` rather than decided silently. |
| **III. Document Lifecycle and Status Discipline** | **PASS** | Carried documents keep their headers. New openXwallet documents are `record`-class evidence (the byte-identity proof) and operational runbooks; both are linked into the new README's doc index, per Principle IV's index rule. |
| **IV. Schema and Artifact Discipline** | **PASS** | Every new YAML carries `schema_version` and `kind` (`contract_pin.yaml`: `kind: pinned_contract_manifest`; `contracts/manifest.yaml`: `schema_version: 1`). No credentials. **No host-absolute paths in any committed file** — the carve, the proof and the runbooks all use repo-relative paths and runtime resolution, and the scratch clone location never appears in a commit. |
| **V. Validation Gates (NON-NEGOTIABLE)** | **PASS** | Nothing is pushed until, in openXwallet: the pin verify, the syntax gate, the validator (plain and `--strict`), `pytest`, and `openspec validate --all --strict` are all green; and in openxFactory: `openspec validate --all --strict` plus this repo's own gates on the feature branch. The evidence is deterministic and reviewable — recomputed digests and diffs, not assertions. **V8's red run is part of this gate**: a verifier that has never refused is not known to refuse. |
| **VI. Versioned, Content-Addressed Releases** | **PASS** | `wallet-v1.0` is allocated AT REALIZATION, not reserved: `contract_bundle_version: wallet-v1.0` in the manifest, a matching `contracts/CHANGELOG.md` entry, an annotated tag at the realized commit, and per-file SHA-256 for the eight owned artifacts. The carve commit is pinned as an exact 40-hex commit — never a branch, never a movable tag. |
| **VII. Fail-Closed Authority Boundaries** | **PASS** | `scripts/verify-contract-pin.py` fails CLOSED on a missing file, an absent recorded digest, or any drift, and its refusal carries the remediation (N1). It runs BEFORE the validator, because the validator checks only `.is_file()` — presence, not identity — while rule (g) reads the approval-scope vocabulary out of that very file. Committed evidence carries digests and diffs only: no credentials, no tenant data. |

**Post-Phase-1 re-check**: PASS, unchanged. Phase 1 added no new violation
surface; the one design choice with constitutional weight (Principle IV's
"no host-absolute paths") is discharged by generating the proof record with
repo-relative paths and by keeping the scratch clone out of every commit.

**Repository Constraints check**: this feature ADDS to openxFactory and rewrites
nothing. Shared-tree discipline is honoured by working in a dedicated worktree
(`openxFactory-worktrees/P2-openxwallet-carve`, branch `017-openxwallet-carve`)
and committing with explicit pathspecs — never `git add -A`.

## Project Structure

### Documentation (this feature)

```text
specs/017-openxwallet-carve/
├── plan.md                       # This file
├── spec.md                       # What P2 must deliver, and how it fails
├── clarify-questions.md          # Three points of fact, resolved not escalated
├── research.md                   # Phase 0 — the eight rows, the shapes, the hazards
├── data-model.md                 # Phase 1 — the entities and their exact fields
├── quickstart.md                 # Phase 1 — reproduce the proof from scratch
├── contracts/
│   ├── carve-surface.md          # The twelve path sets as a contract
│   ├── manifest-rows.md          # The 8 owned + 1 consumed row shapes
│   └── verify-contract-pin.md    # The verifier's CLI + refusal contract
├── evidence/                     # Filled during implementation
│   ├── byte-identity.md          # Both halves of the proof
│   └── operator-log.md           # The operator acts, with ids
├── checklists/requirements.md    # Spec quality gate
└── tasks.md                      # Phase 2 (/speckit-tasks)
```

### Source Code — `opensoft/openXwallet` (the repository this feature creates)

```text
openXwallet/                                     # NEW repository, private
├── README.md                                    # SCAFFOLD — doc index, descendants rule, byte-identity claim
├── CLAUDE.md                                    # SCAFFOLD — points at the global protocol
├── AGENTS.md                                    # SCAFFOLD — points at the global protocol
├── contract_pin.yaml                            # SCAFFOLD — kind: pinned_contract_manifest
├── .github/
│   ├── CODEOWNERS                               # SCAFFOLD
│   └── workflows/
│       ├── wallet-validation.yml                # CARVED, then the verify step prepended
│       └── pytest-suite.yml                     # SCAFFOLD — job id pytest-suite
├── contracts/
│   ├── manifest.yaml                            # SCAFFOLD — wallet-v1.0, 8 owned + 1 consumed
│   ├── CHANGELOG.md                             # SCAFFOLD — seeded from v1.31/v1.43 + wallet-v1.0
│   ├── schemas/
│   │   └── hermes-job-envelope.schema.yaml       # SCAFFOLD — vendored, byte-copied, identical path
│   ├── openxwallet/                             # CARVED — core family + examples/ (36 negatives)
│   └── openxwallet-agent-profile/               # CARVED — first profile + examples/
├── scripts/
│   ├── validate-openxwallet.py                  # CARVED — byte-identical, zero edits
│   ├── wallet-yaml-syntax-gate.py               # CARVED — byte-identical
│   └── verify-contract-pin.py                   # SCAFFOLD — new, fails closed
├── tests/wallet_yaml_syntax_gate/               # CARVED — byte-identical
├── docs/
│   ├── openxwallet-cutover-runbook.md           # SCAFFOLD — authored before the carve
│   ├── pin-resync-runbook.md                    # SCAFFOLD — openAvatar's shape
│   └── byte-identity-wallet-v1.0.md             # SCAFFOLD — the reproducible proof
├── openspec/
│   ├── config.yaml                              # SCAFFOLD — schema: spec-driven
│   ├── specs/openxwallet/spec.md                # CARVED + 2 prose lines
│   ├── specs/openxwallet-agent-profile/spec.md  # CARVED + 2 prose lines
│   └── changes/archive/2026-08-08-add-openxwallet/  # CARVED — record, byte-identical
└── specs/
    ├── 006-openxwallet-contracts/               # CARVED — 7 files, evidence/ included
    ├── 010-wallet-validator-ci/                 # CARVED
    └── 012-wallet-issuer-anchor/                # CARVED
```

### openxFactory (this repository) — the entire footprint

```text
specs/017-openxwallet-carve/                     # ADDED (this feature dir)
openspec/changes/split-openxwallet-repo/tasks.md # MODIFIED — group 3 ticks + evidence
```

Nothing else. No deletion, no rename, no force-push.

**Structure Decision**: two repositories, one direction of travel. The carved
history is the base layer of openXwallet's `main`; the scaffold is one or a few
commits on top, so `git diff <carve-commit-in-openxFactory> <carved-file>` stays
meaningful for every floored path. The scaffold/carve boundary is not cosmetic —
it is what makes the proof checkable by a third party who has only the two
repositories.

## Implementation phases

| Phase | What | Reversal |
| --- | --- | --- |
| **0** | Case-variant name check; `git filter-repo` present; fresh clone; FREEZE the carve commit; author the cutover runbook | Nothing has happened yet |
| **1** | The carve, in the scratch clone; completeness check; the two explicit counts; examples-prefix assertion | Delete the scratch clone |
| **2** | The scaffold commits on the carved `main`; the two prose edits; all local gates green | Reset the scratch clone to the carve layer |
| **3** | The byte-identity proof, both halves, written to a reproducible record | Proof fails ⇒ no tag, no push; fix or stop |
| **4** | Create the private repository; push `main` | Delete the repository — nothing pins it yet |
| **5** | Ruleset in EVALUATE; one trivial PR; both checks report; merge; PATCH to ACTIVE; capture `rules/branches/main` | PATCH back to EVALUATE, or delete the ruleset |
| **6** | The V8 red run (mutated vendored copy refuses), then revert | The mutation never leaves a branch |
| **7** | Tag `wallet-v1.0`, annotated, naming the carve commit | Delete the tag (unpinned by anything) |
| **8** | Back in openxFactory: tick group 3 with evidence; commit with explicit pathspecs; push; open the PR; do NOT merge | Close the PR; openxFactory is untouched |

Phases 0–3 are reversible by deleting a scratch directory. Phase 4 is the first
irreversible-ish act, and it is still reversible: nothing pins openXwallet until
P3, so deleting the repository restores the world.

## Divergences from the launching brief, and why

Recorded so the reviewer sees a choice rather than a slip. In every case the
**ratified artifacts win** over the brief.

1. **`.github/workflows/wallet-validation.yml` is NOT inside the byte-identity
   floor.** The brief proposed keeping it byte-identical and adding a separate
   `verify-contract-pin.yml` workflow. But ratified task 3.24 enumerates the
   floor and the workflow file is **not** in it, while task 3.19 and design D8
   positively require the verify step to run "BEFORE the validator" inside the
   job whose id is `wallet-validation`. A separate workflow cannot order itself
   before another workflow's step. So: the verify step is prepended INSIDE
   `wallet-validation.yml`, that file's post-carve edit is declared as the only
   edit to a carved file, and the floor is proven over exactly the paths task
   3.24 names. No `verify-contract-pin.yml` is created.
2. **The consumed row's `sha256` is computed, not copied.** openxFactory's
   manifest row for `contracts/schemas/hermes-job-envelope.schema.yaml` carries
   no `sha256` at all — see `clarify-questions.md` Q1. The digest is recomputed
   over the pinned bytes at the carve commit, which is the same value the ratified
   text intends, and the absence upstream is noted on the row.
3. **The ruleset requires both tokens.** Ruleset 21538893 — the shape D8 says to
   mirror — requires `wallet-validation` AND `pytest-suite` as of 2026-08-26
   17:39. Task 3.27's evidence names `wallet-validation`; requiring both
   satisfies that and mirrors the actual precedent. Recorded, not assumed.
4. **The feature number is 017, not 016.** 016 was taken by
   `016-openxwallet-split-bookkeeping` (merged as PR #396). The script minted 017;
   017 is used.

## Complexity Tracking

No Constitution Check violation. The table is intentionally empty.
