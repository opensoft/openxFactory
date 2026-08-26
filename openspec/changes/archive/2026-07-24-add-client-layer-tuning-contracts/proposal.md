---
code_surface: openxFactory (templates/client-layer/roles/ + scaffold delta, contracts/client-content/ schemas + fixtures, scripts/validate-client-content.py)
target_release: contract-v1.17 (released at realization 2026-07-23; annotated tag verified)
Status: ratified
Ratified: user approval of `add-client-layer-tuning-contracts` on 2026-07-24
Realized: live-proven — the opensoft tenant tuned and seeded on aks-opensoft-platform-qa-01
  (hermes-install docs/release/phase-2-flip-evidence.md)
---

# Proposal: add-client-layer-tuning-contracts

## Why

Phase 1 of the activation path is live: the Domain layer seeds, materializes,
and governs on the QA install. Phase 2 is the tenant layer — and its first
exit is neutral: every operating organization needs the same house-team
functions, content shapes, and validation, so they belong in openxFactory
before codexFactory specializes them or the wizard tunes them. All design
decisions were made in the 2026-07-22 review pass (client-layer brainstorm
cluster, staged as `client-layer-tuning`): the roles/ shape, the Finance &
Accounting Officer, the voice floor, the facts rule, the stricter-only
comparability spec, and the unified wizard-writes-an-overlay seeding path.

## What Changes

- **`templates/client-layer/roles/`** — the neutral Plane-1 house team: the
  `house_style` baseline (respect + discretion locked, warmth floored at
  `moderate`, per-axis tunable ranges) and eleven persona objects — Company
  Policy Lead, Change Approvals Authority, Client Security & Compliance
  Officer (flagships), Integrations & Credentials Steward, Delivery & SLA
  Lead, Customer & Communications Lead, Legal & Compliance Counsel,
  Reputation & Brand Steward, Product Liability & Insurance Officer,
  **Finance & Accounting Officer** (owns cost reporting + the
  tracking-granularity contract), and the Client Infrastructure Liaison as a
  **composed capability, not a member** (10 deciders + 1 capability).
- **Scaffold delta** (`product-service-scaffold.yaml`): the
  `cost_reporting_steward` worker (FAO's Plane-2 hands; count 19 → 20) and
  the `roles/` reference.
- **`contracts/client-content/`** — the schemas the wizard writes and the
  seeder validates: `client_policy_overrides`, `client_memory_boundaries`,
  `client_integration_boundaries`, and **`hermes_client_overlay`** — the
  seedable per-client document (decided here: canonical path
  `config/clients/<client_ref>/overlay.yaml` in the install repo, declared
  to the seeder via the repo's `hermes_overlay_descriptor`; digest pin
  recorded in the install's compatibility manifest `client_overlays[]`,
  mirroring `domain_overlays[]`). Self-testing examples + intended-reason
  negatives.
- **`scripts/validate-client-content.py`** — the canonical validator
  implementing the **stricter-only comparability spec** (allowlists ⊆,
  denylists ⊇, ceilings ≤, floors ≥, clearance requirements add-only,
  conjunctive envelopes add-only, ordered enums at-or-above; anything with
  no partial order → `review_required`, never a silent pass), consumed by
  the wizard at write time and the seeder at validation time — one
  implementation, two enforcement points.

## Capabilities

### New Capabilities
- `client-layer-tuning`: the neutral tenant-layer contract set — house-team
  roster, client content schemas, the seedable client overlay, and the
  stricter-only comparability validator.

## Impact

- Unblocks: codexFactory `hermes/client/` defaults (phase 2b) and the
  hermes-install wizard + client-seeding increment (phase 2c).
- Provenance: staged topic `openxFactory:staging:client-layer-tuning`
  (first of its three exits); brainstorm sources with dated Decided
  sections (2026-07-22).
- Release: registered in the contracts manifest and published as the next
  additive bundle at realization.
