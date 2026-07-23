# client-content Contracts

Status: draft
Ratified by: add-client-layer-tuning-contracts (on ratification)

The neutral tenant-layer content contracts: what the client policy wizard
writes and the seeding runtime validates.

- `client-policy-overrides.schema.yaml` — the client's stored delta
  (`relation_to_domain: stricter_only`), including budget envelopes, the
  tracking-granularity contract, and the human-ratified auto-clear envelope.
- `client-memory-boundaries.schema.yaml` — the four per-tenant buckets with
  the `tenant_isolated` invariant, in the gateway vocabulary.
- `client-integration-boundaries.schema.yaml` — allowed integration classes;
  credential bindings are references only.
- `client-overlay.schema.yaml` — **`hermes_client_overlay`**, the seedable
  per-client document (canonical path
  `config/clients/<client_ref>/overlay.yaml` in the install repo, declared
  via the repo's `hermes_overlay_descriptor`, digest-pinned in the install's
  `client_overlays[]`). Composes the three content kinds as the enforceable
  tenant slice.
- `examples/` — the positive overlay + domain baseline + intended-reason
  negatives the canonical validator self-tests against.

Canonical validator: `scripts/validate-client-content.py` — structural
checks + the stricter-only comparability spec (allowlists ⊆, denylists ⊇,
ceilings ≤, envelope conjuncts add-only, ordered enums at-or-above; no
partial order → `review_required`, never a silent pass). One implementation,
two enforcement points: the wizard at write time, the seeder at validation.

Provenance: staged topic `openxFactory:staging:client-layer-tuning`;
brainstorm cluster Decided sections 2026-07-22.
