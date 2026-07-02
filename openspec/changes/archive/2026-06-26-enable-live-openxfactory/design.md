# Design: Live openxFactory Factory Stack

## Baseline

`openxFactory` is canonical for workflow policy, contracts, and reference
examples. `Omnigent-Install` is the Omnigent/Polly install and worker runtime
repo. `Hermes-Install` is the Hermes runtime, backup, restore, and deployment
repo.

`Omnigent-Install` already contains local proof assets for the six-workstream
live factory flow. This change uses those assets as implementation sources but
keeps `openxFactory` as the policy and contract source of truth.

## Implementation Strategy

Work proceeds in feature slices:

1. OpenSpec proposal and runtime capability specs.
2. Contract pinning and compatibility checks in install repos.
3. Hermes runtime control-plane validation against canonical contracts.
4. Omnigent worker event bridge validation against canonical contracts.
5. Spec Kit stage control and clarification routing validation.
6. Project Alfa pilot evidence.
7. PR admission, Merge Council, and Merge Master runtime evidence.
8. CloudPC worker packaging, auth restore, memory, and operations evidence.
9. Final validation and archive.

Each slice must have:

- bounded source inventory;
- target files;
- validation commands;
- PR admission evidence;
- merge readiness evidence;
- explicit stop-condition check.

## Contract Pinning

Install repos must record the `openxFactory` commit and contract manifest they
implement. Validation must check:

- the referenced `openxFactory` commit exists;
- required contract files exist;
- local compatibility copies either match the canonical contract or declare an
  allowed adapter delta;
- runtime adapters are not moved as part of contract pinning.

## Runtime Control Loop

Hermes owns governance, state, approvals, and traceability. Omnigent owns repo
execution. GitHub owns PR and final merge enforcement.

Hermes must record:

- jobs;
- runs;
- events;
- artifacts;
- approval requests;
- approval decisions;
- traceability edges;
- Merge Council and Merge Master decisions.

Omnigent must emit:

- stage start and completion events;
- subagent dispatch and result events;
- artifact events;
- approval request events;
- terminal job state events.

## Pilot Shape

Project Alfa remains the default pilot. The selected feature must be low-risk,
small, and traceable. It should target less than 3,000 changed lines and must
remain under 10,000 changed lines unless Hermes explicitly approves an
exception.

The pilot must produce evidence from OpenSpec intent through Merge Master
decision. It may use dry-run Merge Master approval until a production GitHub App
or bot identity is installed.

## Stop Conditions

Stop immediately if:

- a secret appears in Git, logs, memory, artifacts, or PR text;
- a worker opens a PR before Hermes PR admission approval;
- a worker merges directly;
- Spec Kit answers are applied before Hermes approval;
- changed lines exceed policy;
- GitHub branch protection is disabled or bypassed;
- traceability is missing;
- auth profiles become shared writable homes across containers.
