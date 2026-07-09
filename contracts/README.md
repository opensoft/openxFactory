# Factory Contracts

Status: draft

This directory is the canonical home for shared factory contracts owned by
`openxFactory`.

Contracts belong here when they define behavior between two or more factory
subsystems, including Hermes, Omnigent/Polly, OpenSpec, Spec Kit, GitHub,
merge council, and worker agents.

## Ownership Rule

```text
openxFactory/contracts/
  owns canonical contract meaning, versioning, and compatibility rules

Hermes-Install and Omnigent-Install
  may keep pinned copies, generated adapters, smoke fixtures, or runtime
  configuration derived from these contracts
```

Install repositories must identify the `openxFactory` contract version or
commit they consume before runtime adapters are treated as compatible.

## Planned Contracts

Copied contracts:

| Contract | Purpose | Initial Source |
|---|---|---|
| `schemas/hermes-job-envelope.schema.yaml` | Job request envelope from Hermes to Omnigent/Polly or other workers | `Omnigent-Install/schemas/` |
| `schemas/hermes-job-event.schema.yaml` | Structured event emitted by worker, bridge, or Hermes service | `Omnigent-Install/schemas/` |
| `schemas/hermes-job-run.schema.yaml` | Job run status and lifecycle record | `Omnigent-Install/schemas/` |
| `schemas/clarification-questions.schema.yaml` | Spec Kit clarification questions emitted by lead engineering roles | `Omnigent-Install/schemas/` |
| `schemas/clarification-answer.schema.yaml` | Single routed answer from an authority role | `Omnigent-Install/schemas/` |
| `schemas/clarification-answer-packet.schema.yaml` | Collected answer packet returned to the requesting lead | `Omnigent-Install/schemas/` |
| `schemas/hermes-operational-postgres.sql` | Hermes operational job/run/event/artifact/approval/traceability database contract | `Omnigent-Install/schemas/` |
| `policies/hermes-governance-agents.yaml` | Hermes profile/group governance and routing policy | `Omnigent-Install/policies/` |
| `policies/merge-risk-policy.yaml` | Merge Master risk classification and GitHub action policy | `Omnigent-Install/policies/` |

Native openxFactory contracts:

| Contract | Purpose | Initial Source |
|---|---|---|
| `schemas/avatar-first-ui-profile.schema.yaml` | Domain-neutral avatar-first UI profile contract for xFactory frontends and domain overlays | `openxFactory` |
| `schemas/domain-installation-overlay.schema.yaml` | Domain overlay contract for supplementing, replacing, constraining, or vetoing openxFactory installation stages | `openxFactory` |
| `memory-gateway/` | Product-neutral xFactory Memory Gateway contracts, vocabularies, provider profiles, bindings, context packets, migration, usage, erasure, break-glass, and audit | `openxFactory` |

Planned contracts:

| Contract | Purpose | Initial Source |
|---|---|---|
| `pr-admission-packet.schema.yaml` | Evidence packet used before opening a GitHub PR | To define |
| `merge-readiness-report.schema.yaml` | Merge council readiness report contract | To define |
| `repo-boundary-release-map.schema.yaml` | Mapping between `openxFactory` release and install repo commits | To define |

## Contract Manifest

The machine-readable inventory is:

```text
contracts/manifest.yaml
```

Each entry records:

- source path
- source compatibility reference
- copied schema or policy version when available
- intended consumers
- adapter ownership rule

## Version Pinning

Contract consumers must pin compatibility in one of these forms:

```yaml
openxfactory_contract_ref:
  repo: opensoft/openxFactory
  commit: <git-sha>
  contract: contracts/<contract-name>
  version: <semantic-version-or-date>
```

or:

```yaml
openxfactory_contract_ref:
  repo: opensoft/openxFactory
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
ownership. They must link back to the corresponding `openxFactory` contract.

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
  -> copy or summarize canonical contract into openxFactory/contracts/
  -> add version and compatibility notes
  -> update install repo adapter to reference canonical contract
  -> remove or mark legacy copies only after replacement checks pass
```

Do not move runtime adapters, generated clients, or smoke fixtures into this
directory unless they are part of the canonical contract itself.
