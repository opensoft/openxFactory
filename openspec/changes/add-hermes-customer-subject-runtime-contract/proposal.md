code_surface: openxFactory
target_release: implemented
Status: ratified
Ratified by: user approval of `add-hermes-customer-subject-runtime-contract` on 2026-07-12

## Why

The neutral architecture already defines one Customer Hermes instance per customer subject, but the canonical machine-readable contracts still model only one layer per role and do not enforce subject-instance isolation across jobs, artifacts, approvals, or trace records. This gap blocks Hermes Install Gate G0 and prevents codexFactory projects, MedxFactory patients, LedgerxFactory client companies, and other domain subjects from sharing the same governed runtime pattern safely.

## What Changes

- Add a domain-neutral Hermes runtime-topology contract that distinguishes the single Customer, Client, and Domain role templates from their runtime layer instances.
- Allow one installation/stack to contain exactly one active Client instance, exactly one active Domain instance, and repeatable Customer instances keyed by a governed pseudonymous `customer_subject.kind` and `customer_subject.ref` rather than a domain-specific project identifier.
- Define lifecycle-aware cardinality so an installation may bootstrap before subject onboarding while an operational installation requires at least one active Customer instance.
- Define fail-closed isolation, immutable principal authority grants, and explicit directional bindings bounded to exact source and target resources, expiring and append-only-revocable; wildcard, inherited, and transitive authority is forbidden.
- Add parallel v2 job envelope, run, event, and Postgres operational contracts that enforce a common installation/stack/layer scope while retaining v1 contracts during the compatibility bridge.
- Require content-addressed available artifacts, immutable approval targets and decisions, approval expiry/cancellation/revocation events, and scoped trace edges tied to active binding authority.
- Add an executable, idempotent v1-to-v2 migration with a content-addressed mapping manifest, frozen source snapshot, reconciliation ledger, and structural quarantine that preserves legacy rows without promoting unverifiable artifacts, approvals, or trace edges to governed v2 authority.
- Add canonical validators and positive/negative fixtures, including at least two different Customer instances in one installation and proof that one subject cannot enumerate, read, write, approve, or trace through another subject without an exact active binding.
- Publish the contracts as a versioned additive bundle with an annotated release tag, exact repository commit, canonical digest inventory, and per-file SHA-256 digests; require Hermes Install to pin that evidence before multi-subject implementation proceeds.
- Keep domain aliases and semantics in DomainxFactory overlays: Project Hermes/project, Patient Hermes/patient, Client Company Hermes/client company, and future mappings specialize the same neutral Customer role.

## Capabilities

### New Capabilities

- `hermes-customer-subject-runtime`: Defines neutral role-template versus runtime-instance semantics, customer-subject identity and lifecycle, installation topology, content-addressed assembly pins, and cross-domain conformance.
- `hermes-governed-record-integrity`: Defines layer-scoped persistence, default-deny isolation, explicit cross-layer bindings, artifact integrity, approval authority, traceability, v1-to-v2 migration, validation, and release conformance.

### Modified Capabilities

- `neutral-job-envelope`: Introduces parallel v2 envelope, run, and event requirements with a shared neutral installation/stack/layer scope while preserving the existing v1 compatibility surface.
- `shared-contract-ownership`: Strengthens install-consumer pins for governed bundles to include the exact release, repository commit, contract paths, schema identifiers, and per-file digests.

## Impact

- Canonical schemas, migrations, fixtures, and release inventories under `contracts/hermes-runtime/` and `contracts/releases/`
- Contract bundle inventory, provenance, compatibility, and release records under `contracts/`
- Domain-stack and runtime-topology validators under `scripts/`
- Positive and negative contract/migration fixtures and automated tests
- Neutral architecture, terminology, migration, and versioning documentation
- Hermes Install compatibility manifest and its planned runtime/lifecycle interfaces
- DomainxFactory overlays that map neutral customer subjects to projects, patients, client companies, or other domain-owned subject kinds
