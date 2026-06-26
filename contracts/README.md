# Factory Contracts

This directory is the canonical home for shared factory contracts owned by
`openWorkflow`.

Contracts belong here when they define behavior between two or more factory
subsystems, including Hermes, Omnigent/Polly, OpenSpec, Spec Kit, GitHub,
merge council, and worker agents.

## Ownership Rule

```text
openWorkflow/contracts/
  owns canonical contract meaning, versioning, and compatibility rules

Hermes-Install and Omnigent-Install
  may keep pinned copies, generated adapters, smoke fixtures, or runtime
  configuration derived from these contracts
```

Install repositories must identify the `openWorkflow` contract version or
commit they consume before runtime adapters are treated as compatible.

## Planned Contracts

Initial planned contracts:

| Contract | Purpose | Initial Source |
|---|---|---|
| `hermes-job-envelope.schema.yaml` | Job request envelope from Hermes to Omnigent/Polly or other workers | `Omnigent-Install/schemas/` |
| `hermes-job-event.schema.yaml` | Structured event emitted by worker, bridge, or Hermes service | `Omnigent-Install/schemas/` |
| `hermes-job-run.schema.yaml` | Job run status and lifecycle record | `Omnigent-Install/schemas/` |
| `clarification-questions.schema.yaml` | Spec Kit clarification questions emitted by lead engineering roles | `Omnigent-Install/schemas/` |
| `clarification-answer.schema.yaml` | Single routed answer from an authority role | `Omnigent-Install/schemas/` |
| `clarification-answer-packet.schema.yaml` | Collected answer packet returned to the requesting lead | `Omnigent-Install/schemas/` |
| `pr-admission-packet.schema.yaml` | Evidence packet used before opening a GitHub PR | To define |
| `merge-readiness-report.schema.yaml` | Merge council readiness report contract | To define |
| `merge-risk-policy.schema.yaml` | Merge master risk classification and escalation contract | To define |
| `repo-boundary-release-map.schema.yaml` | Mapping between `openWorkflow` release and install repo commits | To define |

## Version Pinning

Contract consumers must pin compatibility in one of these forms:

```yaml
openworkflow_contract_ref:
  repo: opensoft/openWorkflow
  commit: <git-sha>
  contract: contracts/<contract-name>
  version: <semantic-version-or-date>
```

or:

```yaml
openworkflow_contract_ref:
  repo: opensoft/openWorkflow
  tag: <release-tag>
  contract: contracts/<contract-name>
```

## Adapter Rule

An install repo may keep implementation-specific files derived from a contract,
including:

- generated clients
- service adapters
- smoke-test fixtures
- pinned schema copies
- runtime validation configs

Those files are not canonical unless the contract explicitly delegates
ownership. They must link back to the corresponding `openWorkflow` contract.

## Breaking Changes

A contract change is breaking when an existing Hermes or Omnigent adapter,
worker, smoke test, or workflow artifact would fail without coordinated
changes.

Breaking contract changes must be one of:

- split from adapter migration and staged behind compatibility support
- explicitly approved as a breaking change by Hermes governance
- paired with install repo PRs that update adapters and smoke tests

## Migration Rule

Contract migration is copy-first:

```text
existing install repo schema
  -> copy or summarize canonical contract into openWorkflow/contracts/
  -> add version and compatibility notes
  -> update install repo adapter to reference canonical contract
  -> remove or mark legacy copies only after replacement checks pass
```

Do not move runtime adapters, generated clients, or smoke fixtures into this
directory unless they are part of the canonical contract itself.
