# Implementation Plan: repository identity — `opensoft/codexFactory` becomes `codeXfactory/codexFactory` in governed content

**Branch**: `030-realize-codexfactory-repository-identity` | **Date**: 2026-09-08 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/030-realize-codexfactory-identity/spec.md`

**Lane**: `provenance-autonomous-merge`

## Summary

Realize groups **1–8** of the ratified openxFactory change
`adopt-codexfactory-repository-identity` — runbook step **10.2** — as five
reviewed pull requests, split on ONE axis the packet does not carry: whether a
rename is correct **today**, with the transfer unperformed, or only **after** it.

The measured basis, re-taken at this feature's head `e8021fed`:

| class | hits | files | disposition |
| --- | ---: | ---: | --- |
| RENAME | **124** | **60** | split (a) safe-now 8/8, (b) gated 116/52 |
| FROZEN | **78** | **54** | byte-unchanged, proved by diff |
| NOT SWEPT | **125** | **49** | byte-unchanged (other lanes' packets, `ideation/`) |
| **TOTAL** | **327** | **163** | |

The eight `contract-v3.4` inventoried members that move were re-verified against
`contracts/releases/contract-v3.4.digests.yaml` (283 entries): all eight are
present, and **none** of the other 52 renamed files is, so the release-surface
arithmetic in the packet's `design.md` § 5 holds unchanged at this head.

## Technical Context

**Language/Version**: Python 3 (validators and pytest suites only — this feature
ships no runtime code). YAML `schema_version: 1` artifacts; Markdown governance
documents; GitHub Actions workflow YAML.

**Primary Dependencies**: the repo-local validators
(`scripts/validate-factory-identity.py`, `validate-clearing-dispatch.py`,
`validate-signed-execution-chain.py`, `validate-hermes-runtime-contracts.py`,
`validate-omnigent-contracts.py`, `validate-hermes-domain-overlay.py`,
`validate-contract-release.py`, `validate-sequenced-after.py`), the pinned
external `openspec` CLI, and `scripts/doc_health/`.

**Storage**: files in the git tree. No database, no service, no network write.

**Testing**: `python3 -m pytest` over
`tests/hermes_runtime_contracts`, `tests/clearing`, `tests/factory_identity`,
`tests/review_lane_pin`, `tests/sequenced_after`.

**Target Platform**: the openxFactory repository tree and its CI.

**Project Type**: contract/governance corpus — documentation, contracts,
fixtures, validators.

**Performance Goals**: N/A. The only time constraint is external: the transfer
window should spend minutes merging reviewed diffs, not hours writing them, which
is why every gated slice is authored now and held in draft.

**Constraints**:

- **The transfer is unperformed.** The runbook places the whole governed
  realization at **Phase 10**, after the Phase 1 transfer. This feature is
  launched early on the convener's word, so it authors everything and lands only
  what is true before the transfer.
- **`pytest-suite` and `merge-master-approval` are required checks and both
  resolve `opensoft/codexFactory` by `actions/checkout` today.** Respelling
  either today reds every openxFactory pull request.
- **Eight inventoried members must move in ONE slice.** Moving a subset reds
  `verify-commit` on a non-editorial member with no cut available to repair it,
  because the cut needs all eight.
- **`governance/factory-identity/` is permanently human-only** and is entered by
  name in codexFactory's never-clearable floor.
- **34 signed-execution-chain examples cannot be respelled**: the fixture key's
  private half exists nowhere in the repository.
- **This lane merges nothing** and never `git add -A`, never a bare `git commit`,
  never `git stash`, never a force-push, never an amend of a pushed commit.

**Scale/Scope**: 327 occurrences across 163 files measured; 124 across 60 in
scope for rename; 5 pull requests; 0 merges by this lane.

## Constitution Check

*GATE: passed before Phase 0, re-checked after Phase 1.*

| principle | gate | verdict |
| --- | --- | --- |
| **I. Contract-First, Domain-Neutral Core** | Does this land domain-specific behaviour, vocabulary or policy in the neutral repository? | **PASS.** No behaviour, vocabulary or policy moves. The engineering domain's OWNER SEGMENT is respelled in neutral content that already named it; no domain interpretation crosses the boundary and no `stack.yaml` is touched. |
| **II. Governed Change Flow** | Is there a ratified OpenSpec change before implementation? | **PASS.** `adopt-codexfactory-repository-identity`, ratified 2026-09-07T22:21:44Z, merged as PR #763 (`eb30db7a`). This feature is its Speckit realization and duplicates none of its task list: the packet's `tasks.md` stays the governance ledger and [tasks.md](./tasks.md) references it by task id. |
| **III. Document Lifecycle and Status Discipline** | Any silent status edit? Any `standard` claim without backing? | **PASS.** No `Status:` header moves. `ideation/` is untouched, which is also why its 19 occurrences are NOT SWEPT. |
| **IV. Schema and Artifact Discipline** | `schema_version` + `kind` present, stubs still stubs, README index current, no credentials, no host-absolute paths? | **PASS.** No schema, no `kind`, no `$id`, no `contract_id` and no `contract_schema_version` moves. `.example.yaml` files stay stubs. The evidence file is linked from the packet, and the feature is linked from the README doc index at the bookkeeping task. No credential and no host-absolute path is written; the evidence file records repo-relative paths only. |
| **V. Validation Gates (NON-NEGOTIABLE)** | Affected validators green and `openspec validate --all --strict` green before push? | **PASS WITH ONE DECLARED EXCEPTION.** All affected validators run green. `--all --strict` carries **one pre-existing failure**, `disposition-codexfactory-declared-renames` — a deltaless packet about declared SCENARIO retitles, unrelated to repository renames, neither caused nor repaired here. The packet predicts this exact result. Recorded, not silently absorbed. |
| **VI. Versioned, Content-Addressed Releases** | Are the five coordinated values moved atomically, and is the minor allocated at realization? | **PASS, DEFERRED.** Eight inventoried members move, so a bundle is owed. No minor is reserved by this feature; the cut is prepared and allocated only after the renames reach the final integration point, per `docs/contract-versioning-policy.md` § Bundle Realization Order. Because this lane merges nothing, the cut is recorded as owed rather than performed, and the pull request that will perform it is named. |
| **VII. Fail-Closed Authority Boundaries** | Any authority claim not backed by a ratified change? Any unredacted evidence? | **PASS.** Every act cites a packet task id. The origin re-issuance is a respell under design § 4.3 D-1 and widens nothing: `objects` stays a single element, `expires_at` is unextended, no key material moves. The evidence file carries counts and paths only. |

**Repository Constraints check**: this feature runs from the isolated worktree
`openxFactory-worktrees/030-realize-codexfactory-identity` (constitution:
"follow-on lifecycle commands run from that worktree, never the root checkout").
Every commit stages explicit pathspecs. The aggregation pin is **not** touched —
that is packet group 9.3 and a runbook step.

No Constitution Check violation requires justification, so **Complexity Tracking
is empty and omitted**.

## The gating rule, stated so it can be checked rather than trusted

An occurrence is **SAFE NOW** if and only if respelling it today

1. states nothing false about the present, and
2. breaks no resolution that works today.

Everything else is **GATED**, and its pull request names the runbook step at
which it lands. Applied mechanically:

| occurrence shape | (1) false today? | (2) breaks today? | verdict |
| --- | --- | --- | --- |
| synthetic example / negative fixture `repository:` illustrating a shape | no | no | **SAFE NOW** |
| the real domain's canonical key in the regression denominator | yes — it is the engineering domain's address, and the resolver key migrates "from the next bundle forward" | no | GATED |
| a workflow `repository:` consumed by `actions/checkout` | yes | **yes** — `pytest-suite`, `merge-master-approval` | GATED |
| `SOURCE_REPOSITORY` passed to `gh api repos/<x>` | yes | **yes** | GATED |
| the origin register a live sealed request is compared against | yes | **yes, in reverse** — it would refuse today's real dispatches | GATED |
| a `gh api` line an operator pastes from a runbook | yes | **yes, at the terminal** | GATED |
| a `https://github.com/opensoft/codexFactory/...` citation URL | yes | **yes** — 404 until the transfer | GATED |
| prose asserting where engineering content lives | yes | no | GATED |
| a mapping row carrying `transferred_on` | yes — the act has not happened | no | GATED |
| a dated record of a measurement or a completed act | — | — | **FROZEN** (records-and-assertions test, not this axis) |

**Result: 8 hits / 8 files are SAFE NOW; 116 / 52 are GATED.** The arithmetic
closes against the RENAME subtotal of 124 / 60 in both hits and files, and the
close is asserted in [tasks.md](./tasks.md) rather than left to the reader.

## Project Structure

### Documentation (this feature)

```text
specs/030-realize-codexfactory-identity/
├── plan.md              # This file
├── spec.md              # What and why, with the (a)/(b) axis
├── research.md          # Phase 0: every reading taken where the packet is silent
├── data-model.md        # Phase 1: the occurrence / class / gating entities
├── quickstart.md        # Phase 1: how to reproduce every claim here
├── contracts/
│   └── repository-identity-row.md   # the mapping row this feature prepares
├── checklists/
│   └── requirements.md  # spec quality checklist, validated
└── tasks.md             # Phase 2 (/speckit-tasks)
```

### Source Code (repository root)

The surfaces this feature edits, by slice. Nothing outside these paths is
touched, and that is proved by diff at the freeze-verification task.

```text
# SLICE A — safe now (normal pull request)
openspec/changes/adopt-codexfactory-repository-identity/
└── evidence/codexfactory-identity-sweep-2026-09-08.md   # group 2
contracts/omnigent/examples/
├── omnigent-install-manifest.example.yaml               # group 3.9
└── fixtures/negative/manifest-{dual-domain-overlay,legacy-vocabulary,
    missing-effective-profiles,parallel-identity,semantic-duplicate-worker}.yaml
contracts/hermes-domain-overlay/examples/                # group 3.10
├── hermes-subject-overlay.example.yaml
└── negative/subject-undeclared-kind/hermes/subject/project-alfa/overlay.yaml

# SLICE B1 — gated at runbook step 1.2: pin, workflows, operator tools
contracts/review-lane-pin.yaml                           # group 3.5
contracts/review-lane-repin-binding.template.yaml
.github/workflows/review-lane-repin.yml
.github/workflows/merge-master-approval.yml              # group 3.6
.github/workflows/pytest-suite.yml                       # group 3.7
.github/merge-approval-envelope.yml
scripts/review_lane_repin.py
scripts/doc_health/pin_class.py
scripts/mint-factory-origin-key.py                       # group 3.12
tests/review_lane_pin/test_{floor_snapshot,repin_lane,review_lane_caller}.py
tests/factory_identity/test_mint_script.py
docs/factory-origin-key-mint-runbook.md                  # group 4.5
docs/review-lane-repin-runbook.md

# SLICE B2 — gated at runbook step 1.2 AND HUMAN-ONLY: the origin identity
governance/factory-identity/register.yaml                # group 5.1
governance/factory-identity/wallets/wal-origin-codexfactory-0001.yaml   # 5.2
governance/factory-identity/grants/grant-origin-codexfactory-0001.yaml  # 5.3
tests/clearing/test_origin_signature.py                  # group 5.5
tests/clearing/test_attestation.py
contracts/clearing/examples/                             # group 3.8 (8 files)
contracts/clearing/examples/factory-identity-fixture/register.yaml      # 3.11
tests/factory_identity/test_validator.py                 # group 3.13

# SLICE B3 — gated at runbook step 1.2: the eight inventoried members
contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml      # 3.1
contracts/hermes-runtime/fixtures/regression/{digest-mismatch,
    duplicate-repository,missing-exclusion-reason}.yaml                 # 3.3
contracts/hermes-runtime/README.md                                     # 3.4
docs/contract-versioning-policy.md                                     # 4.2
docs/terminology-and-repo-topology.md                                  # 4.3
docs/xfactory-domain-factory-model.md                                  # 4.4
tests/hermes_runtime_contracts/test_domain_regression.py               # 3.1/3.2

# SLICE B4 — gated at runbook step 1.2: the remaining prose
docs/{architecture,roles-and-authority,traceability-model,
    omnigent-constitution,dogfood-content-migration-plan,
    deployment-worker-model,feature-decomposition,merge-council,
    merge-master,pr-admission,spec-kit-stage-ownership,
    workflow-contract,governed-reissuance-runbook}.md      # groups 4.1, 4.6, 4.7
README.md                                                  # group 4.8

# SLICE B5 — gated at runbook step 1.2 AND BLOCKED
contracts/policies/repository-identity.yaml                # group 1 — ABSENT
```

**Structure Decision**: five slices, one pull request each, because the split is
forced by four independent constraints and not by taste — the transfer gate
(safe-now vs gated), the required-check gate (`pytest-suite` and
`merge-master-approval` must not move early), the human-only gate
(`governance/factory-identity/` cannot ride an autonomous path), and the
release-inventory gate (all eight members move together or `verify-commit` reds
with no repair available). Within a slice, commits follow the packet's
one-commit rules: a fixture never lands without the artifact that pins it.
