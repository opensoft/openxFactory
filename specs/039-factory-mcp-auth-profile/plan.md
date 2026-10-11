# Implementation Plan: Factory MCP authorization profile

Status: draft
Kind: plan

**Branch**: `039-factory-mcp-auth-profile` | **Date**: 2026-10-09 | **Spec**: [`spec.md`](spec.md)
**Input**: the feature specification; the ratified change
[`amend-factory-mcp-conformance-auth-profile`](../../openspec/changes/amend-factory-mcp-conformance-auth-profile/proposal.md)
(`design.md` D1 to D10, its delta, and `tasks.md` § 2); and the surfaces
[feature 037](../037-factory-mcp-conformance/plan.md) built.
**Lane**: `openxfactory-5` (display `openXfactory-5`).

## Summary

The change adds an authorization block to a deployed service's factory MCP
declaration, narrows M5's *Unavailable dependency* scenario to dependency
failures reported through the error inventory, and states that error
vocabularies stay per domain. The realization amends feature 037's four
surfaces and adds nothing beside them:

- **Schema.** `contracts/factory-mcp/declaration.schema.json` gains an optional,
  closed `auth` object in the `deployed` branch of `service`, and the `auth` key
  in the evidence and gap concern vocabularies. A second synthetic example,
  deployed and carrying a block, sits beside the existing not-deployed one.
- **Validator.** `scripts/validate-factory-mcp.py` gains the semantic checks and
  stable codes of `design.md` D7. They run where the service is already
  checked, and the block's support citations reuse the tools' resolution.
- **Tests.** `tests/factory-mcp/` gains red-first tests for every new refusal,
  characterization tests for what `main` already does, and the M5 tests. The
  M5 tests are shown red against a mutant. Two existing tests whose premise the
  ratified *Compatibility* section reverses are amended.
- **Runbook.** `docs/factory-mcp-conformance.md` describes the block, its codes,
  the stdio rule, the narrowed M5 reading and the per-domain statement. Its
  release paragraph moves to the version the cut allocates.

The contract cut (task 2.6) registers the declaration in the bundle for the
first time. It waits for the version claim on #630.

## Technical Context

**Language/Version**: Python 3.12 (CI's `pytest-suite` runs 3.12; local runs use 3.12.3).

**Primary Dependencies**: `jsonschema` 4.25.1 (Draft 2020-12) and the standard
library (`urllib.parse`). Nothing new. Tests run in a virtual environment built
from `requirements/hermes-runtime-contracts.lock` with `--require-hashes`, as
CI builds its own. See [`research.md`](research.md) R-11 for why a system
interpreter is not used.

**Storage**: N/A. The validator reads files under explicit offline snapshot
roots.

**Testing**: `unittest` test cases collected by `pytest`, in
`tests/factory-mcp/test_factory_mcp_conformance.py`. Sockets are blocked in
`setUp`.

**Target Platform**: Linux CLI and Python callable, offline.

**Project Type**: a contract (JSON Schema) and its offline validator (CLI and
library).

**Performance Goals**: none new. The authorization checks are constant work
per declaration. The input bound (256 KiB) and output bound (256 KiB) are
unchanged.

**Constraints**: offline only, with no network, server, token or key
material. Synthetic identifiers only, in a public repository. Stable diagnostic
codes, locations and ordering. Exit codes 0/1/2 unchanged.

**Scale/Scope**: one service block per declaration, with nine new codes and two
existing codes at new locations.

## Constitution Check

*GATE: checked before Phase 0 and again after Phase 1 design.* Each principle
is from [`.specify/memory/constitution.md`](../../.specify/memory/constitution.md).

| Principle | Check | Result |
| --- | --- | --- |
| I. Contract-first, domain-neutral core | The block and its codes are neutral profile rules. No domain's codes, schema or behavior enter the tree, and examples are synthetic. | PASS |
| II. OpenSpec before implementation | The change is ratified (2026-10-08) and its packet landed (#1274 → `93d13d6c`). This feature is the one Speckit realization the change names. | PASS |
| III. Lifecycle and status discipline | Every new document carries a controlled `Status:`: `draft` for feature documents, `record` for checklists and the verification record. None claims `ratified` or `standard`. | PASS |
| IV. Schema and artifact discipline | The JSON declaration schema keeps `schema_version: 1` (OQ-5). No credential, no host-absolute path, and no private repository path is written. The feature gets its own bullet in README's Documentation index, as features 034, 035 and 038 have, and the runbook links its records. | PASS (after analyze D1) |
| V. Validation gates | Tests are red first and committed before any schema or validator change. Every gate CI runs is run on the branch and on `main` in the same clone kind before the pull request is opened, and recorded in [`verification.md`](verification.md). | PASS (to be evidenced) |
| VI. Versioned releases | No version is reserved here. The cut is one candidate commit with the manifest row, changelog entry and release inventory, after the version is claimed on #630 row 4. | PASS (deferred by design) |
| VII. Fail-closed authority | The block is closed. Unknown algorithms are refused rather than tolerated, and the audience is refused whenever it could be shared. Validity never certifies (`verified_conformance: false`). | PASS |

No violation, so Complexity Tracking stays empty. **Re-check after Phase 1:**
the design adds no file kind, dependency or authority beyond the table above.
PASS.

**One recorded deviation from the shared workflow, not from the constitution.**
The repository's git extension would create the feature in a sibling worktree.
The lane's brief assigned an isolated full clone on the feature branch instead,
and the coordinator accepted that (spec § Clarifications). The constitution's
Repository Constraints describe the worktree mode as the default, and the
clone meets what the mode exists for: the feature is never worked on the base
branch, in a shared tree.

## Project Structure

### Documentation (this feature)

```text
specs/039-factory-mcp-auth-profile/
├── spec.md            # the specification, traced to the delta
├── plan.md            # this file
├── research.md        # realization decisions R-1 to R-17, with the lines that decide them
├── data-model.md      # the block, the binding, the concern, the codes
├── quickstart.md      # how to run the validator and the tests
├── contracts/
│   └── interface.md   # the declaration and diagnostic interface this feature changes
├── checklists/        # requirements-quality checklists (maximum coverage)
├── tasks.md           # the executable tasks
└── verification.md    # the red-first runs, the mutant runs, the gates and the suite
```

### Source code (repository root)

```text
contracts/factory-mcp/
├── declaration.schema.json                      # + service.deployed.auth; + "auth" concern
└── examples/
    ├── declaration.example.json                 # unchanged (not deployed)
    ├── declaration-deployed.example.json        # NEW: deployed, with a block
    └── outcome.json                             # unchanged
scripts/validate-factory-mcp.py                  # + authorization checks in the service pass
tests/factory-mcp/test_factory_mcp_conformance.py  # + red-first, characterization and M5 tests
docs/factory-mcp-conformance.md                  # + block, codes, stdio rule, M5 reading, vocabularies
```

At the cut (task 2.6, after the version claim): `contracts/manifest.yaml`,
`contracts/CHANGELOG.md` and `contracts/releases/<version>.digests.yaml`.

**Structure Decision**: amend feature 037's surfaces in place. The new tests
join the existing module and class, because its `setUp` and helpers build the
synthetic declaration every case starts from. A second module would import or
duplicate them. Importing a `TestCase` subclass would also re-collect every
existing test.

## Delivery sequence

Each step is one commit with explicit pathspecs.

1. **Feature documents**: spec, plan, research, data model, interface,
   quickstart, checklists and tasks, after analyze.
2. **Red-first tests (task 2.2)**: the new tests, with the two amended tests,
   and no schema, validator or example byte. Run against `main`'s validator in
   the same commit: every new refusal fails, the characterization and M5 tests
   pass. The M5 tests are then run against a mutant of `main`'s validator and
   fail. Both runs go in the verification record.
3. **Schema and example (task 2.3)**.
4. **Validator (task 2.4)**: `tests/factory-mcp/` goes green.
5. **Runbook (task 2.5)**, except its release paragraph, which waits for the
   version.
6. **STOP for the version (task 2.6)**: compute the version the policy
   allocates, re-check #630 row 4 and the open pull requests, record the
   reasoning in the lane's progress file, push the branch (no pull request
   yet), and report `NEED VERSION`.
7. After the coordinator's claim and resume: the cut commit (task 2.6),
   `release-tag-gate`, the verification record with every gate and the full
   suite on the branch and `main` (task 2.7), and the DRAFT pull request.

## Complexity Tracking

Empty: the Constitution Check found no violation.
