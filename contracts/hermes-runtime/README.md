# Hermes Customer-Subject Runtime Contracts

Status: draft

This directory is the domain-neutral contract surface for running multiple
Customer Hermes instances in one xFactory installation. It separates the
three static Hermes role templates declared by a DomainxFactory from the
concrete layer instances registered at runtime.

This draft implementation realizes the topology, identity, lifecycle, and
exact-assembly-pin slice; the governed persistence, authority, binding,
artifact, approval, and trace slice; the v1-to-v2 migration and quarantine
slice; and the provider-side publication surfaces — the additive v2 job
family, the supported-Domain regression denominator, the release digest
inventory and verifier, and the consumer handoff receipt. Those contracts are
directly tested by portable validators and by a digest-pinned PostgreSQL
15/16 matrix. Release realization (version allocation, annotated tag,
promotion) and the exact landed consumer receipt remain later steps of the
same ratified change. The implemented slices do not authorize deployment or
Gate G0 closure.

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
v2 job-contract slice extends the same scope to work admission; the full
runtime claim is evidenced only through a published bundle.

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

## Additive v2 Job Bridge

The v2 job family is additive. The frozen v1 job surface at
`contracts/schemas/hermes-job-envelope.schema.yaml`,
`contracts/schemas/hermes-job-run.schema.yaml`, and
`contracts/schemas/hermes-job-event.schema.yaml` is not edited, moved, or
deprecated by this change. Unchanged v1 job fixtures continue to validate
byte-for-byte, and a consumer pinned to a published v1 path remains
conformant until it deliberately upgrades; nothing in the additive bundle
retroactively invalidates a valid v1 record or pin.

The v2 family lives in this directory as
`hermes-job-envelope-v2.schema.yaml`, `hermes-job-run-v2.schema.yaml`, and
`hermes-job-event-v2.schema.yaml` at contract schema version 2. Every v2
job, run, and event record requires the same neutral scope tuple of
`installation_id`, `stack_id`, and `layer_id`. No required v2 property or
enumeration encodes a project, repository, feature, patient, company, or any
other single domain's noun; domain overlays may re-tighten the neutral core
but must not push their vocabulary into it. Runs and events correlate to
their job through exact identifier coupling, event sequences are monotonic
and append-only, layers in a terminal or suspended lifecycle state cannot
admit new jobs, and retired layers retain read access to their recorded
artifact, approval, trace, and audit evidence. These semantics are enforced
by `scripts/hermes_runtime_validation/semantics/jobs.py` and proven by the
indexed `fixtures/jobs/` matrix, including the retired-layer new-job denial
and preserved retired-layer evidence cases.

## Supported-Domain Regression Denominator

`domain-regression-inventory.schema.yaml` defines the versioned
compatibility denominator and `fixtures/domain-regression-inventory.yaml` is
the realized instance. It names every supported DomainxFactory repository
with an exact published commit, `stack.yaml` path, raw-blob digest, domain
ID, and expected contract pin: `codeXfactory/codexFactory`,
`opensoft/AdxFactory`, `opensoft/LedgerxFactory`, `opensoft/MedxFactory`,
and `opensoft/OpsxFactory`. `opensoft/LegalxFactory` is recorded as an
explicit exclusion because it has no canonical `stack.yaml` yet. The
denominator is versioned evidence, never an implicit "all current domains"
scan.

Regression validation reads exact `commit:path` Git objects only; a dirty
working tree is never evidence. Repository resolution is deterministic:
repeatable `--domain-repo <canonical-repo>=<checkout>` mappings, or a
`--domain-repo-root <mirror-cache>` under which the canonical `owner/repo`
resolves only to `<root>/<owner>/<repo>` or `<root>/<owner>/<repo>.git`.
Ambiguous roots and missing objects are dependency failures (exit code 2),
never passes. `scripts/hermes_runtime_validation/domain_regression.py`
implements the resolver and the per-entry digest, pin, and stack checks.

## Release Digest Inventory

A published bundle carries a canonical release digest inventory at
`contracts/releases/<bundle-tag>.digests.yaml`, validated against the
self-contained `contracts/releases/release-digest-inventory.schema.yaml`
(deliberately outside this family root so the inventory can cover the family
without indexing itself through it). Each entry records an artifact ID,
repository-relative path, type, Git file mode, optional schema identity and
version, and the lowercase `sha256:<64hex>` digest of the raw Git blob bytes
— never a canonicalized, checkout-filtered, or working-tree rendition.
Entries are unique and sorted in bytewise UTF-8 path order. Membership is
closed over the release surface, the inventory excludes exactly itself, and
it carries no commit field: recording either would be circular, so the
annotated tag and the downstream compatibility manifest anchor the commit
and the inventory digest instead.

`scripts/validate-contract-release.py` verifies that identity with four
subcommands: `build` writes a candidate inventory from exact bytes,
`verify-commit` reproduces every digest from a pinned commit's Git objects,
`verify-promotion` proves pre-tag that the tag is absent, the version is the
next available, the reviewed candidate is reachable from remote main, and no
release-surface blob drifted, and `verify-tag` proves the published
annotated tag dereferences to the exact commit. Exit codes are 0 for pass,
1 for findings, and 2 for dependency failures.

## Consumer Handoff Receipt

`consumer-handoff-receipt.schema.yaml` defines the Gate G0 closure receipt.
The canonical consumer repository is the constant
`opensoft/xFactory-Hermes-Install`; a receipt naming any other repository —
including the distinct `FarHeap/Hermes-Install` product — fails with the
stable finding code `HGR-HANDOFF-CONSUMER-REPOSITORY` before any downstream
object is resolved. The indexed negative fixture
`fixtures/pins/consumer-receipt-wrong-repository.yaml` pins that rejection.

A valid receipt records the provider bundle coordinates (repository, tag,
peeled commit, manifest and inventory paths and digests), the exact landed
consumer commit, the closure packet at `evidence/gates/g0/<bundle-tag>.yaml`
with its digest, repository-relative compatibility-manifest, checker,
runtime-binding, and evidence paths with digests, and positive and negative
check results. `scripts/hermes_runtime_validation/consumer_handoff.py`
reproduces the closure packet and every recorded artifact as exact
`commit:path` Git objects from the landed consumer revision, using the same
deterministic-root resolution rules as the Domain regression denominator.
Downstream neutralization, the compatibility checker, and the pin itself
remain owned by the consumer repository's own feature; openxFactory accepts
the landed receipt only as external Gate evidence.

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

Every document describing this surface carries a controlled `Status:` header
from the xFactory document lifecycle. This README and the normative policy
and model documents that describe the bridge
(`docs/contract-versioning-policy.md`, `docs/xfactory-domain-factory-model.md`,
`docs/terminology-and-repo-topology.md`) remain `Status: draft`: they state
normative intent backed by the ratified change but are not yet promoted
canon. The ratified spec deltas under the change carry `Status: ratified`
naming the approving change. Generated verification evidence — provider gate
results, release-candidate reviews, publication records, and the consumer
handoff receipt evidence — is always `Status: record`: immutable,
non-authorizing provenance regardless of how normative its content sounds.
