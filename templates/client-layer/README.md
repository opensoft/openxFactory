# Client Layer Templates

Status: draft
Kind: template
Repository context: openxFactory
Purpose: provide reusable templates for Client Hermes overlays.

## Files

- [product-service-scaffold.yaml](product-service-scaffold.yaml) defines a
  domain-neutral Client Hermes scaffold for clients that sell or operate
  products, services, subscriptions, managed services, or hybrid offers.
- [installation-discovery-migration.yaml](installation-discovery-migration.yaml)
  defines how Client Hermes may use client documents, email history, and related
  records to discover workflows and migrate bad current practice to approved
  target practice.

The scaffold carries a `client_infrastructure_liaison` profile block — the
neutral coordination role for privileged infrastructure dependencies on a
client tenant, a contracted managed host, or OpsxFactory. It defaults to
`configured_but_inactive`, always requires a responsible operator and an
escalation path, and becomes `activation_blocking` when a declared component
needs an external operator. Governing contract:
[Client Infrastructure Liaison](../../docs/client-infrastructure-liaison.md)
(request/readiness schemas under `contracts/schemas/`, validated by
`scripts/validate-client-infrastructure.py`).

General installation spine templates live under
[templates/installation](../installation/README.md). Client-layer templates are
used inside that spine when the installer configures a tenant or Client Hermes
overlay.

The template is a design contract. Domain factories specialize it, and real
client or tenant instantiations bind it to actual staff, systems, approvers,
credential references, and offer catalogs.
