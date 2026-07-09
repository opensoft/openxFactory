# openxFactory Contract Changelog

Governed by [Contract Versioning Policy](../docs/contract-versioning-policy.md).

## contract-v1.3 — 2026-07-09 (additive)

Added:

- `contracts/schemas/xfactory-domain-stack.schema.yaml` — optional
  `xfactory.promoted_from` and `xfactory.specializes` promotion-provenance
  fields (refine-promotion-provenance change). Backward compatible; existing
  stacks remain valid.

## contract-v1.2 — 2026-07-03 (additive)

Added:

- `contracts/memory-gateway/` — canonical xFactory Memory Gateway contract
  surface for Customer Hermes memory and Domain Omnigent expert
  memory/knowledge access. Includes vocabularies, consent profile, gateway
  request/response, provider profile, binding, mapping, subject safety,
  context packet, expert context packet, expert source, promotion, migration,
  usage, revocation, erasure, break-glass, and audit event schemas.
- `scripts/validate-memory-gateway.py` — canonical validation for gateway
  contracts, provider profiles, conformance fixtures, domain examples, and the
  first local runtime smoke path.

## contract-v1.1 — 2026-07-03 (additive + deprecating)

Added:

- `contracts/schemas/xfactory-domain-stack.schema.yaml` — canonical
  stack.yaml shape. Introduces `hermes.layers`: an ordered list of authority
  layers each bound to a canonical role (`customer` = served subject,
  `client` = tenant/operator organization, `domain` = reusable expert
  domain, `extension` = declared intermediate layer with authority_scope).
  Fixes the cross-domain vocabulary collision where "Client Hermes" meant
  the subject layer in some domains and the tenant layer in others.
- `scripts/validate-domain-factory.py` — canonical conformance validator,
  consumed (not copied) by domain repos. Replaces per-domain hand-rolled
  validators as the conformance baseline; domain validators may extend it.
- `docs/contract-versioning-policy.md` and this changelog.

Deprecated (warnings, removal at contract-v2.0):

- `hermes` flat keys (`subject_overlay`, `subject_layer_name`,
  `care_organization_overlay`, flat `client_overlay`/`customer_overlay`
  styles) in favor of `hermes.layers`.
- `openworkflow_*` owner/layer tokens in workflow gates in favor of
  `xfactory`.

## contract-v1.0 — 2026-06-26 (baseline)

- Initial canonical contract set migrated from install repos: job
  envelope/event/run schemas, clarification packets, avatar-first UI
  profile, domain installation overlay, governance and merge-risk
  policies, hermes operational Postgres DDL.
