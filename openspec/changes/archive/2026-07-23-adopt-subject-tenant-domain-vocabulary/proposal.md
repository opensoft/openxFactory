code_surface: openxFactory
target_release: next additive contract bundle (allocated at realization per docs/contract-versioning-policy.md)
Status: ratified
Ratified: user approval of `adopt-subject-tenant-domain-vocabulary` on 2026-07-23

## Why

The canonical Hermes layer vocabulary — Customer / Client / Domain — names two
of its three layers after Opensoft's commercial relationships instead of the
layers' structural roles, and both commercial words are ambiguous in exactly
the way the 2026-07-03 review flagged as its top architecture defect (§A1):
LedgerxFactory's "Client Hermes" is its served-subject layer while canonical
"Client Hermes" is the tenant-operator layer, so the same term denotes
opposite layers depending on which README is read. "Customer" has the same
failure mode latent in every domain whose served subject is itself a company.

Brett selected the replacement vocabulary on 2026-07-22: **Subject / Tenant /
Domain**. The repository has already converged on these words organically —
canonical docs describe the layers as "subject / tenant-operator /
expert-domain", `isolation` blocks say `per_tenant`, the avatar-first UI
standard says "tenant administrators" and "served subject", and three of five
DomainxFactories already use a `subject` key. This change is the durable
lifecycle record that freezes the vocabulary, per review fix priority #2, and
defines how the rename reaches released machine surfaces without breaking
pinned consumers.

## What Changes

- Ratify the canonical Hermes layer vocabulary as **Subject Hermes** (the
  served party or work subject: patient, project, managed system), **Tenant
  Hermes** (the tenant-operator organization running the installation: its
  policy, staff, integrations, credentials, local knowledge), and **Domain
  Hermes** (unchanged: reusable expert-domain policy and standards).
- Add a `layer-vocabulary` capability defining: the canonical names and their
  one-line role definitions; the domain-alias model (Patient Hermes, Project
  Hermes, etc. specialize the canonical names, never replace them); a
  reserved-terms rule barring "Customer" and "Client" as layer names on new or
  substantively revised governance surfaces (both words remain legal in prose
  about commercial relationships); and a machine-identifier freeze that keeps
  released legacy spellings (`customer_subject_ref`, role kinds
  `customer|client|domain`, schema `$id`s) byte-stable until the next major
  contract bundle, with a published legacy-to-canonical mapping.
- Publish the vocabulary machine-readably as
  `contracts/policies/layer-vocabulary.yaml` (`schema_version: 1`): canonical
  names, legacy mapping, frozen-identifier inventory, and the per-domain alias
  table.
- Update `docs/terminology-and-repo-topology.md` and the layer prose in
  affected openxFactory docs to the canonical vocabulary, each with a
  legacy-vocabulary note so pinned consumers can still cross-reference.
- Explicitly out of scope (deferred follow-up changes): renaming released
  machine identifiers and schema `$id`s (lands only with the next major
  contract bundle); migrating the five DomainxFactory repos and
  `installs/hermes-install` (the latter only after the active Track 2
  realization of `add-hermes-customer-subject-runtime-contract` lands — it
  consumes openxFactory by pin and is unaffected until its pin bump).

## Capabilities

### New Capabilities

- `layer-vocabulary`: canonical Subject/Tenant/Domain layer names, the
  domain-alias model, reserved ambiguous terms, and the staged migration rule
  for legacy machine identifiers.

## Impact

- Affected specs: `layer-vocabulary` (new; ADDED requirements only).
- Affected contracts: `contracts/policies/layer-vocabulary.yaml` (new,
  additive); no released contract file changes.
- Affected docs: `docs/terminology-and-repo-topology.md`,
  `docs/architecture.md`, and other openxFactory docs whose layer prose uses
  the legacy names; README doc index and OpenSpec Records block.
- Downstream (follow-ups, not this change): five DomainxFactory repos,
  `installs/hermes-install`, and the v3/next-major machine-identifier
  migration in `contracts/hermes-runtime/`.
