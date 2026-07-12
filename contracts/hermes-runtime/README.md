# Hermes Customer-Subject Runtime Contracts

Status: draft

This directory is the domain-neutral contract surface for running multiple
Customer Hermes instances in one xFactory installation. It separates the
three static Hermes role templates declared by a DomainxFactory from the
concrete layer instances registered at runtime.

This draft implementation realizes the topology, identity, lifecycle, and
exact-assembly-pin slice plus the governed persistence, authority, binding,
artifact, approval, and trace slice. Those contracts are directly tested by
portable validators and by a digest-pinned PostgreSQL 15/16 matrix. Migration,
quarantine, v2 job envelopes, release publication, and consumer-pin evidence
remain required later slices of the same ratified change. The implemented
slices do not authorize deployment or Gate G0 closure.

## Neutral Model

A DomainxFactory `stack.yaml` declares exactly one reusable template for each
canonical role:

- Customer Hermes: authority and private context for one served subject
- Client Hermes: authority for the tenant or operator organization
- Domain Hermes: reusable domain policy and expert authority

The singular Customer template does not imply a singular Customer runtime.
Once configured, one installation has one active Client layer, one active
Domain layer, and zero or more active Customer layers; an operational
installation requires at least one active Customer layer. Each Customer layer
is bound to exactly one governed `customer_subject` and receives a distinct
installation, stack, layer, and policy namespace. The governed-record slice
enforces that scope across persistence, artifacts, approvals, and traces. The
later v2 job-contract slice must extend the same scope to work admission before
the full runtime claim is evidenced.

Domain repositories supply names and stricter overlays without changing the
neutral identity shape:

| Domain factory | Customer Hermes alias | `customer_subject.kind` example |
| --- | --- | --- |
| codexFactory | Project Hermes | `software_project` |
| MedxFactory | Patient Hermes | `patient` |
| LedgerxFactory | Client Company Hermes | `client_company` |

Project, patient, and client-company fields are therefore not required by the
openxFactory core. The governed reference is an opaque pseudonymous subject
URN whose construction policy and issuer attestation are pinned.

## Static and Runtime Cardinality

Static validation continues to reject duplicate `customer`, `client`, or
`domain` role templates. A second Customer subject must be provisioned as a
runtime layer registration; it cannot be represented by adding another static
Customer role or disguising one as an extension layer.

The neutral isolation value is `per_customer_subject`. Existing specialization
aliases such as `per_customer`, `per_project`, `per_patient`, `per_ledger`, and
`per_campaign` remain accepted for compatibility. They do not introduce
different runtime isolation semantics.

## Lifecycle Authority

Installation, stack, and layer registrations have durable identity. Lifecycle
events are append-only and form one predecessor-linked linear history. Current
state is derived from the immutable registration plus that history; a stored
projection is a cache that must reconcile to the history, not an alternate
authority.

Direct registration mutation, lifecycle-event update or deletion, event forks,
and transitions out of `retired` fail closed. Retired layer IDs, policy
namespaces, and Customer subject tuples remain tombstoned and cannot be reused.
Provisioning retries with the same idempotency key and subject converge on the
same registration; conflicting key reuse fails.

## Assembly Integrity

Every schema, single-file template, and overlay used by a topology is resolved
from an exact repository commit and verified by digest. Directory overlays use
a governed manifest containing a complete, recursive, bytewise-sorted regular
file inventory. The external layer pin binds the canonical repository, exact
commit, overlay root, manifest path and digest, and manifest schema identity
and version. The manifest lives outside its inventoried overlay root so it does
not create a self-digest cycle. Branch-only or tag-only coordinates, traversal,
absolute paths, symlinks, gitlinks, unlisted members, extra members, and digest
drift fail closed.

## Validation and Evidence

`contract-index.yaml` is the canonical member catalog. `fixtures/index.yaml`
indexes positive and negative cases, `acceptance-map.yaml` maps every ratified
OpenSpec scenario to deterministic evidence, and `evidence-register.yaml`
records non-authorizing test bindings and planned evidence state. PostgreSQL
bindings point to deterministic development-matrix results for both supported
majors; empty `result_refs` remain explicitly unrealized. Neither form is
release authority. Only later recorded, exact-commit realization evidence may
participate in release authorization.

The canonical validator must prove at least one operational installation with
two distinct Customer layers and must validate the codexFactory, MedxFactory,
and LedgerxFactory mappings against the same neutral contracts.

## Controlled Provenance

The ratified OpenSpec change
`add-hermes-customer-subject-runtime-contract` controls the requirements and
acceptance intent for this implementation. OpenSpec and Speckit working
artifacts are development provenance; they are not runtime contract inputs and
do not authorize a consumer pin.

Runtime authority begins only with a verified, additive openxFactory contract
bundle whose manifest, annotated tag, exact commit, release digest inventory,
contract IDs, schema versions, and file digests agree. A consumer becomes
compatible only after it records and verifies that exact published bundle pin.
