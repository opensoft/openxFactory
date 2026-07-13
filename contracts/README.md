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
| `schemas/avatar-first-ui-profile.schema.yaml` | Domain-neutral avatar-first UI profile contract for xFactory frontends and domain overlays; AVC-kernel-aligned and realized at `contract-v1.8` with per-file SHA-256 in `manifest.yaml` (consumes the `contract-v1.7` kernel read-only) | `openxFactory` |
| `schemas/domain-installation-overlay.schema.yaml` | Domain overlay contract for supplementing, replacing, constraining, or vetoing openxFactory installation stages | `openxFactory` |
| `memory-gateway/` | Product-neutral xFactory Memory Gateway contracts, vocabularies, provider profiles, bindings, context packets, migration, usage, erasure, break-glass, and audit | `openxFactory` |
| `avatar-client/` | Neutral avatar-client (AVC) contract kernel — 8 JSON-Schema contracts, 9 closed registries, acceptance map, frozen `interface-lock.yaml` baseline, and conformance fixtures; realized at `contract-v1.7` with per-file SHA-256 in `manifest.yaml` (see `avatar-client/README.md`) | `openxFactory` |

Planned contracts:

| Contract | Purpose | Initial Source |
|---|---|---|
| `pr-admission-packet.schema.yaml` | Evidence packet used before opening a GitHub PR | To define |
| `merge-readiness-report.schema.yaml` | Merge council readiness report contract | To define |
| `repo-boundary-release-map.schema.yaml` | Mapping between `openxFactory` release and install repo commits | To define |

### Contracts Pending Realization

Schemas already committed under `contracts/schemas/` for an **active, not yet
archived** OpenSpec change. Following the avatar-client kernel precedent
(`contracts/avatar-client/` existed for the whole `define-avatar-client-
contract-kernel` change before its `contracts/manifest.yaml` entries and
`contract-v1.7` tag were cut at realization), and the
[Contract Versioning Policy](../docs/contract-versioning-policy.md)'s rule
that `contract_bundle_version` is "allocated at realization after merge order
is known" and "a bundle is not published until its tag exists," these files
are **not yet** registered in `contracts/manifest.yaml` or
`contracts/CHANGELOG.md`. Registration happens when the owning change
archives (its task 8.7).

| Contract | Purpose | Owning change |
|---|---|---|
| `schemas/xfactory-document-catalog-snapshot.schema.yaml` | Immutable per-repository document-catalog snapshot | `add-document-cataloging` |
| `schemas/xfactory-document-cataloger-recommendation.schema.yaml` | Immutable non-authoritative cataloger-recommendation evidence | `add-document-cataloging` |
| `schemas/xfactory-document-tag-registry.schema.yaml` | Namespaced document-catalog topic-tag registry | `add-document-cataloging` |
| `schemas/xfactory-document-tag-overrides.schema.yaml` | Owner override/disposition file | `add-document-cataloging` |
| `schemas/xfactory-document-opaque-locator.schema.yaml` | Reusable canonical/opaque document-locator `$defs` kernel | `add-document-cataloging` |
| `schemas/xfactory-document-handling-gate.schema.yaml` | Reusable dispatch/handling-gate decision `$defs` kernel | `add-document-cataloging` |
| `scripts/validate-document-catalog.py` | Strict validator: schema conformance, coverage, unique identity, source freshness, taxonomy resolution, override standing, immutable path layout, baseline-mode exceptions | `add-document-cataloging` |

Reference examples exercising every schema (12 valid + 11 invalid fixtures,
one violation per negative file) live at `examples/document-cataloging/`. See
`openspec/changes/add-document-cataloging/specs/document-cataloging/spec.md`
for the requirements these schemas realize, and that change's `tasks.md`
task 2.1 completion note for the one documented shape discrepancy against
its own illustrative `supporting-docs/document-catalog.template.yaml`.

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
