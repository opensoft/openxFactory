## Context

`openxFactory` now documents the factory-level architecture, workflow
contract, traceability model, feature decomposition standard, merge council
model, repo boundary audit, and repo boundary pilot plan.

`Omnigent-Install` currently contains both Omnigent worker installation
material and a broad local proof harness, including Hermes-like service code,
Hermes schemas, end-to-end Project Alfa examples, PR admission examples, merge
council examples, and pilot scripts. This was useful for discovery, but it
blurs the final boundary between workflow policy and subsystem installation.

`Hermes-Install` is closer to the desired install/DR scope, but it still
contains concepts that should be summarized at the factory level, including
company and cross-company Hermes group meaning and Hermes authority boundaries.

## Goals / Non-Goals

**Goals:**

- Make `openxFactory` the canonical source for integrated factory workflow
  policy.
- Keep `Hermes-Install` focused on Hermes install, operations, backup, restore,
  upgrade, and DR.
- Keep `Omnigent-Install` focused on Omnigent/Polly install, worker runtime,
  auth, operations, backup, restore, upgrade, and DR.
- Use a low-risk, doc-first pilot to test the factory workflow itself.
- Add a clear path for shared contracts and future submodule pins.
- Preserve all working proof harnesses until replacement locations and checks
  exist.

**Non-Goals:**

- Do not move runtime code in the initial feature.
- Do not delete duplicate policy docs in the initial feature.
- Do not add submodules in the initial feature.
- Do not move secrets, credential profiles, generated databases, runtime
  workspaces, or live service manifests.
- Do not resolve the `Hermes-Install` remote ownership decision in this first
  proposal unless Hermes explicitly approves that as a later feature.

## Decisions

### Decision: Use `openxFactory` as the policy source of truth

Factory behavior crosses subsystem boundaries. Policy that describes how
Hermes, Omnigent/Polly, OpenSpec, Spec Kit, GitHub, merge council, and agents
work together belongs in `openxFactory`.

Alternative considered: keep policy in whichever install repo implements it.
This would keep local implementation context close to scripts, but it would
make the install repos competing sources of truth and make future governance
harder to audit.

### Decision: Use copy-first migration

Canonical policy should be copied or summarized into `openxFactory` before
install repo copies are deleted or marked legacy.

Alternative considered: move files directly. Direct movement is faster, but it
risks breaking the current proof harness and obscuring which repo change caused
a failure.

### Decision: Split the change into small features

The migration will use the pilot slices documented in
`docs/repo-boundary-pilot-plan.md`:

```text
FEAT-RB-001 Canonical Boundary Policy
FEAT-RB-002 Contract Home Placeholder
FEAT-RB-003 Omnigent-Install Scope Link
FEAT-RB-004 Hermes-Install Scope Link
FEAT-RB-005 Submodule Decision Record
FEAT-RB-006 First Actual Submodule Add
```

Alternative considered: one PR that reorganizes all repos. That would better
show the intended final shape, but it would be too risky for the first real
system test.

### Decision: Treat contracts separately from install adapters

`openxFactory` should own shared schema and contract meaning. Install repos may
keep generated adapters, smoke fixtures, and pinned copies as implementation
artifacts.

Alternative considered: put contracts only in the repo that first needs them.
That would reduce duplication initially, but it would hide cross-system
contracts inside subsystem implementation repos.

### Decision: Defer submodules

Submodules should be documented and approved before they are added. The first
submodule should be `Omnigent-Install`; `Hermes-Install` should wait until its
remote ownership is resolved.

Alternative considered: add both submodules immediately. That would give the
umbrella layout quickly, but it combines governance, remote ownership, and Git
layout risk in one step.

## Risks / Trade-offs

- Repo split breaks working proof harness -> use copy-first migration and avoid
  deletions until replacement checks exist.
- Policy remains duplicated too long -> mark `openxFactory` canonical and add
  install repo links back to canonical policy.
- Submodules create operational confusion -> require a decision record before
  any `git submodule add`.
- Hermes runtime code moves too early -> defer runtime moves to a separate
  approved feature.
- Install repo tests fail -> require existing smoke tests for any install repo
  feature.
- Secret material moves accidentally -> first features are doc-only and must
  exclude `.local`, `.claude`, `.codex`, databases, token files, and runtime
  workspaces.

## Migration Plan

1. Create this OpenSpec proposal.
2. Use Hermes approval to authorize decomposition.
3. Implement FEAT-RB-001 as doc-only in `openxFactory`.
4. Add `openxFactory/contracts/` placeholder in FEAT-RB-002.
5. Update `Omnigent-Install` README scope and links in FEAT-RB-003.
6. Update `Hermes-Install` README scope and links in FEAT-RB-004.
7. Add a submodule decision record in FEAT-RB-005.
8. Add the first submodule only after the prior features and remote decision
   are approved.

Rollback for doc-only features is a normal Git revert. Runtime code moves and
submodules are not part of the initial implementation.

## Open Questions

- Should `Hermes-Install` move, fork, or mirror from `FarHeap/Hermes-Install`
  to `opensoft/Hermes-Install` before submodule use?
- Should end-to-end proof harnesses eventually live in `openxFactory`, a new
  `factory-lab` repo, or remain in `Omnigent-Install` until production
  adapters exist?
- Should canonical schemas be moved as plain YAML under `contracts/`, or should
  `openxFactory` generate pinned contract bundles for install repos?
