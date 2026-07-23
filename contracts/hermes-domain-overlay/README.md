# hermes-domain-overlay Contract

Status: draft
Ratified by: add-hermes-domain-overlay-contract (on ratification)

The neutral contract for a domain's **seedable Hermes overlay** — the
document the hermes-install `seed-layer-content` verb loads digest-verified
from a domain repo pin (capability `layer-content-seeding`, realized
2026-07-22).

## Files

- `hermes-domain-overlay.schema.yaml` — the overlay shape: domain identity,
  non-empty `approval_scope_kinds` and `required_approval_fields`, and
  `authority_boundaries` (domain-owned list + `xfactory_owns` +
  `repository_owns`).
- `overlay-descriptor.schema.yaml` — the optional role→path declaration a
  domain repo MAY ship at `hermes/overlay-descriptor.yaml`. Keys are runtime
  layer **roles** (`domain`/`client`/`customer`), deliberately not directory
  names — the customer role's overlay may live under `hermes/subject/`.
- `examples/` — positive reference examples plus self-testing negatives
  (each declares its `# expected_failure:` reason).

## Rules the canonical validator enforces beyond the schema shape

`scripts/validate-hermes-domain-overlay.py` (run from the pinned openxFactory
checkout, never copied):

1. **Domain-owned list naming** — `authority_boundaries` carries exactly one
   domain-owned list named `<domain.id>_owns` (e.g. `codex_owns`), non-empty.
2. **No-overlap** — no authority item appears in more than one boundary list.
3. **Descriptor paths** — declared roles are limited to
   domain/client/customer, and every declared path exists when a domain repo
   path is supplied. A missing descriptor falls back to the documented
   convention: `domain → hermes/domain/overlay.yaml`.

## Consumers

- **hermes-install seeding (materialization increment)** — replaces its
  minimal structural check with validation against this contract, pinned at
  the `contract-v1.15` release.
- **DomainxFactory validate chains** — invoke the canonical validator against
  their own repo the same way as the other canonical validators.

Provenance: staged topic `openxFactory:staging:layer-content-materialization`;
design basis `ideation/brainstorm/hermes-layer-seeding-mechanism.md`
(Decided 2026-07-22). Realization proof: codexFactory's live 37-authority
overlay passes unmodified.
