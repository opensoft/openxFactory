# Decision 0001: Install Repo Submodules

Status: Accepted for Omnigent pre-release branch tracking, deferred for Hermes

Date: 2026-06-26

OpenSpec change: `restructure-factory-repo-boundaries`

## Context

`openxFactory` is the canonical factory workflow repository. `Hermes-Install`
and `Omnigent-Install` are subsystem install, operations, backup, restore,
upgrade, and DR repositories.

The factory needs a way to pin known-good install repo revisions from
`openxFactory` without moving install scripts, manifests, worker runtime code,
or DR procedures into the workflow repo.

## Decision

Use Git submodules under `openxFactory/installs/` to pin install repository
versions after the repo boundary and install repo scope docs are approved.

During LedgerxFactory development, `Omnigent-Install` is intentionally allowed
to follow its active development branch. Git still records an exact submodule
commit in `openxFactory`; "latest" means maintainers periodically advance that
recorded commit to the current head of the configured branch.

Approved path for the first submodule:

```text
installs/omnigent-install -> git@github.com:opensoft/Omnigent-Install.git
```

Pre-release tracking branch:

```text
installs/omnigent-install branch -> main
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

- `openxFactory` owns factory policy and shared contract meaning.
- Install repos own subsystem install, operations, backup, restore, upgrade,
  and DR.
- Submodules pin compatible install repo commits; they do not transfer
  canonical policy ownership into install repos.
- Before LedgerxFactory release, Omnigent may be advanced to the latest
  configured branch head with `git submodule update --remote`.
- At LedgerxFactory release, Omnigent must be frozen to an approved commit or
  tag and treated as a release dependency.
- Submodule PRs must not also move files across repositories.
- Submodule PRs must not modify install repo contents through the submodule
  pointer change.
- Submodule PRs must include fresh clone and submodule initialization evidence.

## Update Procedure

To follow the latest Omnigent development branch before LedgerxFactory release:

```bash
git submodule sync installs/omnigent-install
git submodule update --init --remote installs/omnigent-install
git status --short installs/omnigent-install
git add .gitmodules installs/omnigent-install
git commit -m "Advance Omnigent install to latest development head"
```

To update a pinned install repo during release stabilization:

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
- compatibility notes for `openxFactory` contracts
- whether the update follows pre-release branch tracking or freezes a release
  dependency

## Rollback Procedure

To roll back a pinned install repo:

```bash
git checkout <previous-openxFactory-commit> -- installs/omnigent-install
git submodule update --init --recursive installs/omnigent-install
git commit -m "Roll back Omnigent install pin"
```

If the rollback is due to an install repo regression, record:

- failing install repo commit
- last known good install repo commit
- failing check or operational symptom
- whether `openxFactory` contract compatibility is affected

## Clone Procedure

Fresh clone with submodules:

```bash
git clone git@github.com:opensoft/openxFactory.git
cd openxFactory
git submodule update --init --recursive
```

Refresh existing clone:

```bash
git pull --ff-only
git submodule update --init --recursive
```

## Consequences

Benefits:

- `openxFactory` can pin install repo versions without absorbing install code.
- Before LedgerxFactory release, Omnigent can move quickly while still leaving
  an inspectable commit trail in `openxFactory`.
- Release mapping becomes inspectable in Git.
- Install repos keep their operational ownership.

Trade-offs:

- Contributors must understand submodule clone/update behavior.
- Submodule pointer changes need explicit validation.
- Branch tracking is not automatic at clone time; maintainers must run
  `git submodule update --remote` when they intentionally want the latest
  Omnigent commit.
- Hermes submodule remains blocked until the remote ownership decision is made.
