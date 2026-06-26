# Decision 0001: Install Repo Submodules

Status: Accepted for Omnigent first, deferred for Hermes

Date: 2026-06-26

OpenSpec change: `restructure-factory-repo-boundaries`

## Context

`openWorkflow` is the canonical factory workflow repository. `Hermes-Install`
and `Omnigent-Install` are subsystem install, operations, backup, restore,
upgrade, and DR repositories.

The factory needs a way to pin known-good install repo revisions from
`openWorkflow` without moving install scripts, manifests, worker runtime code,
or DR procedures into the workflow repo.

## Decision

Use Git submodules under `openWorkflow/installs/` to pin install repository
versions after the repo boundary and install repo scope docs are approved.

Approved path for the first submodule:

```text
installs/omnigent-install -> git@github.com:opensoft/Omnigent-Install.git
```

Deferred path:

```text
installs/hermes-install -> <pending Hermes remote ownership decision>
```

Do not add `Hermes-Install` as a submodule until Hermes governance approves
whether the canonical repo remains:

```text
git@github.com:FarHeap/Hermes-Install.git
```

or moves, mirrors, or forks to:

```text
git@github.com:opensoft/Hermes-Install.git
```

## Rules

- `openWorkflow` owns factory policy and shared contract meaning.
- Install repos own subsystem install, operations, backup, restore, upgrade,
  and DR.
- Submodules pin compatible install repo commits; they do not transfer
  canonical policy ownership into install repos.
- Submodule PRs must not also move files across repositories.
- Submodule PRs must not modify install repo contents through the submodule
  pointer change.
- Submodule PRs must include fresh clone and submodule initialization evidence.

## Update Procedure

To update a pinned install repo:

```bash
git submodule update --init --recursive
cd installs/omnigent-install
git fetch origin
git checkout <approved-commit>
cd ../..
git add installs/omnigent-install
git commit -m "Pin Omnigent install to <approved-commit>"
```

The PR must identify:

- previous pinned commit
- new pinned commit
- reason for the update
- validation run in the install repo
- compatibility notes for `openWorkflow` contracts

## Rollback Procedure

To roll back a pinned install repo:

```bash
git checkout <previous-openWorkflow-commit> -- installs/omnigent-install
git submodule update --init --recursive installs/omnigent-install
git commit -m "Roll back Omnigent install pin"
```

If the rollback is due to an install repo regression, record:

- failing install repo commit
- last known good install repo commit
- failing check or operational symptom
- whether `openWorkflow` contract compatibility is affected

## Clone Procedure

Fresh clone with submodules:

```bash
git clone git@github.com:opensoft/openWorkflow.git
cd openWorkflow
git submodule update --init --recursive
```

Refresh existing clone:

```bash
git pull --ff-only
git submodule update --init --recursive
```

## Consequences

Benefits:

- `openWorkflow` can pin install repo versions without absorbing install code.
- Release mapping becomes inspectable in Git.
- Install repos keep their operational ownership.

Trade-offs:

- Contributors must understand submodule clone/update behavior.
- Submodule pointer changes need explicit validation.
- Hermes submodule remains blocked until the remote ownership decision is made.
