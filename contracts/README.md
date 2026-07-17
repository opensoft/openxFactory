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
| `hermes-runtime/` | Neutral Hermes customer-subject runtime contract family — topology/identity, trusted-scope authority/binding/approval/traceability records, the PostgreSQL 15/16 operational contract with the governed v1-to-v2 migration and quarantine, scoped v2 job/run/event lifecycle, supported-DomainxFactory regression denominator, and the Gate G0 consumer handoff receipt; governed by `hermes-runtime/contract-index.yaml` and realized (provider side) at `contract-v1.10` with the release digest inventory `releases/contract-v1.10.digests.yaml` (superseding `contract-v1.9`, whose immutable tag and `releases/contract-v1.9.digests.yaml` remain as provenance; see `hermes-runtime/README.md`) | `openxFactory` |
| `schemas/xfactory-document-*.schema.yaml` + `scripts/validate-document-catalog.py` | Neutral document-cataloging contract surface — six JSON-Schema contracts (immutable per-repository catalog snapshot, non-authoritative cataloger-recommendation evidence, namespaced topic-tag registry, owner override/disposition file, and the reusable opaque-locator and handling-gate `$defs` kernels) plus the strict validator; realized at `contract-v1.11` with per-file SHA-256 in `manifest.yaml` (the validator is a commit-content-addressed tool, no per-file digest). Reference examples at `examples/document-cataloging/`; adoption guidance in `docs/document-catalog-adoption.md` | `openxFactory` |
| `avatar-client-lab/` + adopted `examples/avatar-first-ui/fixtures/deterministic/` seeds | Neutral avatar-client-lab evidence surface — the P1 total avatar-state derivation table and the P10 22-capability-scenario register (gate (vi)/(ix)(a)/(ix)(b) sources), the 20 adopted deterministic fixtures closing the state-reachability denominator (P7/P8/P11/P12/P13), and the SCO-001-S05 successor deferral-discharge register `avatar-client/evidence-register.implement-avatar-client-lab.yaml`; realized at `contract-v1.12` with per-file SHA-256 in `manifest.yaml`. The `.md` prose companions and `avatar-client-lab/client-acceptance-map.yaml` are governed by the changelog / `check_client_lab_acceptance_map`, not per-file digests; the reference validators are commit-content-addressed tools. See `avatar-client-lab/README.md` | `openxFactory` |
| `schemas/xfactory-client-infrastructure-request.schema.yaml` + `schemas/xfactory-infrastructure-readiness-result.schema.yaml` + `scripts/validate-client-infrastructure.py` | Neutral client-infrastructure contract family — the durable `client_infrastructure_request` coordination record (six never-conflated identity-reference `$defs`, the three-mode `execution_binding` `client_managed\|managed_host\|opsxfactory_executed`, the closed 13-state `status` enum, embedded `handoff` acceptance record, digest-bearing `package_refs`, cancellation `child_acks`, `supersedes_request_ref`) and the signed/traceable `infrastructure_readiness_result` (never a bare boolean; `ready\|degraded\|not_ready\|unknown\|maintenance`, `valid_until`, per-check `mandatory`/`outcome`/evidence) plus the strict validator; realized at `contract-v1.13` with per-file SHA-256 in `manifest.yaml` (the validator is a commit-content-addressed tool, no per-file digest). Reference examples at `examples/client-infrastructure/`; governing role doc `docs/client-infrastructure-liaison.md` | `openxFactory` |

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
archives, at the registration task named in that family's note below.

| Contract | Purpose | Owning change |
|---|---|---|
| `schemas/ideation-dashboard-snapshot.schema.yaml` | Deterministic ideation-area dashboard projection snapshot | `add-ideation-dashboard` |
| `schemas/ideation-workbench.schema.yaml` | Gitignored user-assembled workbench reference-set manifest | `add-ideation-dashboard` |
| `schemas/ideation-possibles-register.schema.yaml` | Possibles-register consolidation `$defs` kernel (embedded in the cross-reference index) | `add-ideation-dashboard` |
| `schemas/project-register.schema.yaml` | Repository → project → project-group navigation hierarchy (D10) | `add-ideation-dashboard` |
| `schemas/gate-action-record.schema.yaml` | Human-authenticated gate-console action audit record (D16/D17) | `add-ideation-dashboard` |
| `scripts/validate-ideation-dashboard-contracts.py` | Strict validator: schema conformance (FormatChecker-enforced), snapshot referential integrity, workbench recipe/override + committed-manifest guard, possibles-register id-uniqueness + transition legality, project-register single-parent hierarchy, gate-action kickoff-ratification precondition | `add-ideation-dashboard` |
| `schemas/xfactory-idea-routing-record.schema.yaml` | Canonical cross-factory idea routing record (`routing.yaml`); one per unclassified, mixed, cross-domain, or claim-split idea | `add-cross-factory-ideation-routing` |
| `schemas/xfactory-idea-routing-reference.schema.yaml` | Reusable structured repository/path/revision reference `$defs` kernel (mirrors `xfactory-document-opaque-locator.schema.yaml`); no top-level envelope | `add-cross-factory-ideation-routing` |
| `schemas/xfactory-ideation-routing-index.schema.yaml` | Central Idea-ID allocation ledger (`ideation/routing-index.yaml`) | `add-cross-factory-ideation-routing` |
| `schemas/xfactory-ideation-organizer-recommendations.schema.yaml` | Immutable non-mutating ideation-organizer recommendation evidence | `add-cross-factory-ideation-routing` |
| `scripts/validate-ideation-routing.py` | Strict validator: schema/vocabulary conformance, central Idea-ID and Claim-ID uniqueness, legal transitions, destination-owner acceptance, structured repository-reference resolution, paired-document identity, prospective legacy compatibility | `add-cross-factory-ideation-routing` |
| `schemas/ideation-cross-reference.schema.yaml` | Unified cross-stage cross-reference readiness index (source of truth `ideation/cross-reference.yaml`; `.md` is a generated projection); four-schema co-load, embeds the possibles-register kernel | `add-ideation-cross-reference-readiness` |
| `scripts/validate-ideation-cross-reference.py` | Strict validator: four-schema-registry conformance (FormatChecker-enforced), extension-fit citation resolution against promoted/active-change capabilities, min>=8 gate arithmetic, spread-conflict consistency, topic-entry id uniqueness; delegates register-entry shape/transitions to `validate-ideation-dashboard-contracts.py` | `add-ideation-cross-reference-readiness` |
| `scripts/render-ideation-cross-reference.py` / `scripts/bootstrap-ideation-cross-reference.py` | Deterministic YAML→Markdown projection renderer, and the one-time header-derived bootstrap generator that seeds `ideation/cross-reference.yaml` + `.md` | `add-ideation-cross-reference-readiness` |

Reference examples for the ideation-dashboard family (8 valid + 21 invalid
fixtures + 5 register-transition pairs) live at `examples/ideation-dashboard/`;
`scripts/validate-ideation-dashboard-contracts.py` self-tests them, validates a
given file/directory by kind detection, runs register transitions via
`--transition OLD NEW`, and scans the checkout for committed workbench manifests.
Per this section's rule, these entries move to `contracts/manifest.yaml` and
`contracts/CHANGELOG.md` when `add-ideation-dashboard` archives (its task 2.5).

Reference examples for the ideation-routing family (8 valid + 8 invalid
fixtures, one violation per negative file) live at
`examples/ideation-routing/`; `scripts/validate-ideation-routing.py`
self-tests them (schema/`kind`-or-fragment validation) and additionally
validates any real `ideation/routing-index.yaml`, `ideation/**/routing.yaml`,
and `health/ideation-organizer/**/*.yaml` artifacts under a given checkout,
reporting absent paths as skipped rather than passed. See
`openspec/changes/add-cross-factory-ideation-routing/specs/ideation-routing/spec.md`
for the requirements these schemas realize. Per this section's rule, these
entries move to `contracts/manifest.yaml` and `contracts/CHANGELOG.md` when
`add-cross-factory-ideation-routing` archives (its task 8.4).

Reference examples for the ideation-cross-reference family (1 comprehensive
valid index + 2 negatives — one schema-layer, one validator-layer) live at
`examples/ideation-cross-reference/`; `scripts/validate-ideation-cross-reference.py`
self-tests them (four-schema co-load), then scans the checkout for the real
`ideation/cross-reference.yaml`. The index's `.md` sibling is a generated
projection produced by `scripts/render-ideation-cross-reference.py`; the initial
YAML+MD were seeded by `scripts/bootstrap-ideation-cross-reference.py` (task 2.4).
See `openspec/changes/add-ideation-cross-reference-readiness/specs/ideation-cross-reference/spec.md`
for the requirements these realize. Per this section's rule, these entries move
to `contracts/manifest.yaml` and `contracts/CHANGELOG.md` when
`add-ideation-cross-reference-readiness` archives (its task 5.2).

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
