Status: draft

## Why

`openxFactory` now owns the canonical factory workflow, policy, contracts, and
static reference examples. `Omnigent-Install` and `Hermes-Install` are marked as
runtime/install companions. The next step is to prove the documented workflow as
a live, repeatable stack instead of a set of documents and local proof fixtures.

Omnigent already contains substantial local proofs for Hermes service APIs,
event bridges, worker lanes, Spec Kit control, PR admission, merge council,
Merge Master dry-run behavior, and CloudPC worker layout. This change governs
the work needed to pin those proofs to `openxFactory` contracts, make the
runtime path repeatable, and run one real pilot through the full control loop.

## What Changes

- Create a live-runtime OpenSpec change that governs the pilot implementation.
- Require Hermes and Omnigent install repos to pin the `openxFactory` contract
  commit they implement.
- Require install validation to fail when canonical contracts are missing or
  incompatible.
- Require Hermes to provide the live control-plane APIs for jobs, runs, events,
  artifacts, approvals, and traceability.
- Require Omnigent workers to emit structured Hermes events and respect
  approval gates.
- Require all Spec Kit stages and clarification routing to run under the
  canonical ownership map.
- Require one Project Alfa pilot feature to pass through decomposition, Spec
  Kit, branch work, PR admission, GitHub PR, Merge Council, Merge Master, and
  GitHub enforcement.
- Require CloudPC worker packaging, auth restore, memory rules, and operations
  runbooks to be sufficient for repeatable execution.

## Capabilities

### New Capabilities

- `live-factory-runtime`: Defines the live pilot runtime path from OpenSpec
  intent through Hermes, Omnigent, Spec Kit, branch work, PR admission, GitHub
  PR, Merge Council, and Merge Master.
- `hermes-omnigent-integration`: Defines the contract-pinned service/event API
  between Hermes and Omnigent workers.
- `worker-runtime-admission`: Defines worker lane registration, preflight,
  auth, memory, capacity, and CloudPC packaging requirements.
- `github-merge-enforcement`: Defines PR admission, Merge Council, Merge
  Master, human review routing, and GitHub final enforcement requirements.

## Impact

- Primary repo:
  - `opensoft/openxFactory`
- Related implementation repos:
  - `opensoft/Omnigent-Install`
  - `FarHeap/Hermes-Install`
- Pilot target:
  - Project Alfa, using the existing Omnigent Project Alfa proof artifacts
    unless a newer real Project Alfa repo is selected in later evidence.

## Non-Goals

- No broad migration cleanup.
- No deletion of install repo compatibility copies.
- No AKS production deployment until local/CloudPC pilot validation passes.
- No movement of runtime adapters into `openxFactory`.
- No bypass of GitHub branch protection.
- No use of personal GitHub credentials as the production Merge Master
  identity.
- No committed secrets, OAuth tokens, provider auth profiles, databases, logs,
  or generated runtime state.
